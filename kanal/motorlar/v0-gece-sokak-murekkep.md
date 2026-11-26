# gece-sokak-murekkep (v0)

Kullanıcının 25 Kasım 2026'da gönderdiği üslup örneği: gece sokağında küçük araba ve sarı robot; kaba mürekkep, canlı duman (video 3 sn).
- Örneğin kendisi depoda yok (telif; yalnız başvuru).
- Çözümleme ve yön metni Fable'ın; yön metni ayrı bir ajanla sınandı (telif, kanal kuralları, mevcut motorlarla çakışma).

## Karar: ayrı motor
Kanalın bütün motorları bir baskı ya da eski malzeme taklidi: gravür, vazo, kâğıt kesme, ağaç baskı, mürekkep, sessiz film, gazete tramı, gözetim monitörü. Temiz, düz renkli, değişken kalınlıkta mürekkep çizgili çağdaş çizgi roman karesi yok. Bu yüzden 20. yüzyıl ve sonrası konular hep "eskitilmiş" görünüyor.

Çakışmalar:
- `ran` (mürekkep): fırça lekesi ve ıslak kâğıt; çizgi kontur değil leke. Çizgi üretme kodu başlangıç olabilir, ama düz dolgu + kapalı kontur mantığı yok.
- `cernobil/lib/baski.js`: tek vurgu rengi fikri aynı, ama tram dokusu bu üslubun tersi.
- cinecode `line-boil.md`: titreyen kontur, ikilerde tutma, elle çizilmiş duman topakları. Hareket dili neredeyse aynı; yeni oturum buradan başlamalı. Ama o bir tarif, depoda çalışan bir motoru yok. (`styles/` klasöründe `BIZIM_NOT.md` bulunamadı; CLAUDE.md onu önce okutuyor, yeni oturum yerini doğrulamalı.)
- cinecode `urban-sketch.md`: "tek renkli dünya, tek renkli nesne" ve "nesne kahraman" fikri orada da var; ama suluboya ve kâğıt dokulu.
- cinecode `scifi-toon.md`, `cel-anime-80s.md`: kalın kontur + düz renk, ama biri karikatür yüze, öbürü airbrush fona dayanıyor. İkisi de kanalın yüz kuralına ters.

Motorun asıl maliyeti tek parça: genişlik profilli çizgi (kalın dış kontur, ince iç çizgi, sivri uç, 3 karede bir titreme). Gerisi düz dolgu. Diğer motorlara göre ucuz ve SwiftShader'da hızlı olur (doku yok, bulanıklık yalnız far konisinde).

Kazancı: kanalın en güçlü yanı olan nesne, siluet ve ışık bu üslupta doğrudan işe yarıyor. "Bir nesnenin yolculuğu" bakışı için hazır bir dil.

Çekince: bu tek örneğe bakarak verilmiş bir karar. Öteki dört örnekle karşılaştırmadım; aralarında aynı düz renk + mürekkep ailesinden biri daha varsa ikisi tek motorda birleştirilmeli.

## Yön metni (yeni bir oturuma verilir)

> Yeni motor: düz renkli mürekkep çizgisi. Baştan sona yaz; kararlar senin.
>
> Elimizde beğenilmiş bir örnek var: gece sokağında rölantide titreyen küçük bir araba. Onu çizme. Arabayı, tavandaki robotu, afişi, o çizerin elini taklit etme; örnek depoya girmez. Peşinden gideceğin şey örneğin kuralı: dünya tek bir soğuk ton ailesinde durur, çizgi siyah mürekkeptir, karede yalnız bir doygun renk vardır ve o renk hikâyenin taşıdığı şeydir. Hiçbir şey ilerlemese de kare canlıdır; motor titrer, duman çıkar, ışık kıpırdar.
>
> Motorun işi tek şey: kalınlığı değişen, ucu sivrilen, yer yer kapanmayan bir çizgi. Dış kontur kalın, iç çizgi ince. Çizim birkaç karede bir yeniden çizilmiş gibi titrer (tohumlu; her işçide aynı kare); çizimde ara kare ve bulanıklık yoktur, kamera akıcı kalır. Titremenin bedelini SwiftShader'da önce tek karede ölç. Dolgu düzdür, yüzey başına iki ton, kenar sert. Doku, gren, tram ekleme; onlar başka motorların işi. Az çiz: duvarın bütün tuğlalarını değil, üç kümesini.
>
> Yüz ve el bu motorda da zayıf. Onları çizmeye çalışma; insan pencerede ışık, kapıda siluet, direksiyonda bir omuz olsun. Kahraman nesne olsun: bir araç, bir bavul, bir makine, bir mektup.
>
> Üslup kapısı tek kare değil: bir manzara, bir orta plan figür, bir yakın plan ve on beş saniyelik hareket. Hareket karesinde kamera dursun, sahne yine de yaşasın. Filmde bu rölanti, yavaş yaklaşmanın ve sözcüğe bağlı eylemin yerine geçmez. Hassasiyet taramasını o karelerde başlat.
>
> Önce `ran`'ın çizgi koduna ve cinecode'daki line-boil tarifine bak; işe yarayanı al, yeniden yazma. Çekim sistemi Lale'nin `film.js`'i.
>
> Yarayacağı yerler: yirminci yüzyıl ve sonrası, bir nesnenin yolculuğu, sıradan birinin gözünden anlatılan tarih, film videoları.
>
> Gerisi senin kararın.
>
> Fable

## Sınamanın bulduğu ve yön metnine işlenenler
- (2) Donuk plan kuralıyla gerilim: 'Hareket karesinde kamera dursun, sahne yine de yaşasın' ve 'Hiçbir şey ilerlemese de kare canlıdır' yalnız üslup kapısındaki sınama için doğru, ama motorun filmde rölantiyi (titreme, duman) kanalın varsayılan yavaş yaklaşmasının ve sözcüğe bağlı eylemin yerine koymasına kapı açıyor. CLAUDE.md her planın ilk saniyeden hareket etmesini, eylemsiz 5 sn'yi aşan aralıkların listelenmesini istiyor. Tek yan cümleyle sınırlandı.
- (2) Belirsizlik: 'ara kare ve bulanıklık yoktur' cümlesi kamera hareketine de uygulanırsa film.js'in yavaş yaklaşması ikişer karede bir sıçrar ve titrek görünür. Kuralın çizime ait olduğu, kameranın akıcı kalacağı belirtildi.
- (2) Belirlenimcilik ve SwiftShader: kalınlığı değişen çokgen kontur her tutuşta yeniden üretiliyor. Titremenin tohumlu olması (işçiler arası aynı kare; ran'ın ink.bundle.js'indeki boil zaten tohumlu) ve bedelinin önce tek karede ölçülmesi yön metninde yoktu. CLAUDE.md her oturumda yüklendiği için küçük bir eksik; yine de motorun temel işi titreme olduğu için iki sözcükle eklendi.
- (1) Telif: sorun yok. Metin örneği, arabayı, robotu, afişi ve çizerin elini taklit etmeyi açıkça yasaklıyor; örneğin depoya girmemesini söylüyor. Alınan şey genel bir üslup dilbilgisi (soğuk tek ton ailesi, mürekkep çizgi, tek doygun vurgu, rölanti). Duffy ya da başka bir telifli karakter anılmıyor. Kahraman olarak 'bir araç' örneklenmesi, gece sokağında küçük araba sahnesinin yeniden kurulmasına kaymamalı; ancak bu 'Onu çizme' cümlesiyle zaten kapatılmış.
- (3) Yeniden yazma yok: ran/lib/ink.bundle.js'de boil parametreli, profilli ve kalınlığı değişen fırça konturu var (satır ~149, ~902). cinecode/styles/line-boil.md tohumlu ve tutuşlu boil tarifini veriyor. Metin ikisinden de almayı söylüyor. Yeni motor mevcutlardan ayrı: ran mürekkep yıkaması ve gradyanla, cernobil tram ile çalışıyor; burada düz dolgu ve tek doygun renk var. Kullanıcı ayrı motor istedi. Not: CLAUDE.md'nin andığı cinecode/styles/BIZIM_NOT.md depoda yok, metin de onu anmıyor; sorun değil.
- (4) Vaat gerçekçi: sivrilen ve yer yer kırık kontur, yüzey başına iki ton sert dolgu, tutuşlu titreme, duman öbekleri ve kıpırdayan ışık Canvas 2D'de yapılabiliyor. Yüz ve el zaten dışarıda bırakılmış.
- (5) Biçim yerinde: metin adım adım talimat değil, yön veriyor (kural, yasaklar, kapı, başvurular, kullanım alanı). Ana figürün siluet olması, karikatür okumasından kaçınma (yüz çizilmiyor) ve hassasiyet taramasının üslup karelerinde başlaması kanal kurallarıyla uyumlu.

## Çözümleme
## v0: gece sokağında küçük araba (1024×576, 30 kare, 3,06 sn, ≈ 9,8 kare/sn; döngülü GIF kökenli)

**Onu güzel yapan şey:** hiçbir şey ilerlemiyor ama her şey canlı. Araba yerinde duruyor; motoru titriyor, egzozu öksürüyor, tavandaki sarı robot kendi ritminde sallanıyor. Hareket yer değiştirme değil, "rölanti".

### Palet (olcum.json, k-means)
| hex | pay | görev |
|---|---|---|
| #4C535F | %30,8 | duvar, araba gövdesi (orta mavi-gri) |
| #9CAAC1 | %23,2 | gökyüzü, ön zemin, far konisi (açık soğuk gri) |
| #353A41 | %17,7 | gölge tonu |
| #717A87 | %11,9 | kaldırım, ışık alan yüzey |
| #636974, #585D66 | %10,2 | ara tonlar (çoğu sıkıştırma artığı) |
| #101316 | %5,1 | mürekkep çizgisi ve dolu siyah |
| #C39C31 | %1,1 | sarı robot: tek doygun vurgu |

- Karenin yaklaşık %94'ü tek bir mavi-gri ailesi, %5'i mürekkep, %1'i sarı. Pencere içindeki turuncu-kırmızı o kadar küçük ki kümelemeye girmiyor.
- "Gece" siyahla değil, bütün yerel renkleri tek bir mavi-griye çekerek kurulmuş. Bu yüzden her çizgi okunuyor.

### Çizgi
- Tek renk, siyaha yakın mürekkep (#101316). Kalınlık değişken: dış kontur ve lastik kemerleri kalın (576 yükseklikte kabaca 3-4 px), iç ayrıntı ince (1-1,5 px).
- Uçlar sivrilerek bitiyor (fırça kalem). Çizgi yer yer kapanmıyor: tuğlalar yalnız birkaç kümede, tahta perdenin kenarı kırık, çim tek tek virgül vuruşları.
- Dolu siyah yalnız üç yerde: araba altı gölgesi, lastik içi, cam içi karanlık.

### Dolgu, gölge, ışık
- Düz dolgu; gradyan yok. Yüzey başına 2 ton (yerel + bir gölge), kenarlar sert.
- Tek yumuşak öge far konisi: açık tonda yarı saydam bir yamuk, yalnız ucunda eriyor.
- Sıcak ışık yalnız arabanın içinde (pencere). Soğuk dünya içinde sıcak küçük bir oda okunuyor.

### Doku ve gren
- Kâğıt dokusu, gren ya da tram yok; temiz dijital düz renk. Bütün doku çizginin kendisinden geliyor (tuğla, çim, taş).

### Figür
- Yüz çok az çizilmiş: pencere içinde iki küçük baş, gözlük halkası, tek çizgi ağız; karenin %1'inden küçük.
- Asıl "karakter" nesneler: araba ve kutu başlı robot (iki nokta göz, iki anten).

### Kompozisyon
- Tam yandan, düz cepheden sahne; perspektif yok denecek kadar az. Üç yatay bant: duvar (üst %55), yol-kaldırım, ön çim (alt %20).
- Araba karenin ortasında, yüksekliğin kabaca %45'i. Solda afiş, sağda tahta perde çerçeve yapıyor.
- En parlak doygun nokta (sarı) dikey orta eksenin hemen üstünde: göz oraya gidiyor.

### Hareket (30 kareyi bölge bölge ölçtüm)
- **Kamera:** yok. Sol duvar ve çim bölgesinde kareler arası fark 0,00-0,05; yalnız 9 karede bir küçük sıçrama var (0,4-0,8; döngü ya da sıkıştırma dikişi).
- **Araba:** her karede yeniden çizilmiş (bölge farkı 6-13, hiç sıfır değil). 8 karelik çevrim (≈ 0,8 sn): 5 kare aşağıda, 3 kare yukarıda; tavan çizgisi ±1 px oynuyor. Motor titremesi.
- **Robot:** arabadan bağımsız fazda sallanıyor (fark 7,6-11,4; kendi 4+4 düzeni).
- **Duman:** her karede yeni biçim. Kıvrık konturlu, açık dolgulu topaklar; borudan çıkıyor, büyüyor, parçalanıyor, tahta perdenin önünde ince bir şeride dönüp kayboluyor. İki öksürük var (kare 8-15 yoğun, kare 24-26 neredeyse boş).
- **Ara kare, sürtünme (smear):** yok. Hareket bulanıklığı yok. 30 karenin 27'sinde çizim değişiyor: yaklaşık 10 kare/sn'de "birler", yani 30 kare/sn'lik filmde her çizim 3 kare tutulur.
- Hareketli alan karenin kabaca üçte biri; geri kalanı tam sabit.

### Kodla yapılabilirlik
- **Kolay:** düz dolgulu yatay bantlar, duvar, tahta perde, afiş, far konisi, tek tonlu gece paleti, 3 karede bir tutulan titreme (tohumlu gürültüyle birkaç piksel kaydırma), tekerlek, gölge.
- **Orta:** değişken kalınlıkta, uçları sivrilen mürekkep çizgisi (yol boyunca genişlik profili verilmiş dolu çokgen; düz `stroke` ile olmaz, bu motorun asıl işi). Yer yer kapanmayan çizgi ve "az ama doğru" tuğla-çim vuruşları. Elle çizilmiş duman: metaball ya da birleşen dairelerden kontur çıkarıp 3 karede bir yeniden tohumlamak gerekir.
- **Zor:** pencere içindeki iki yüz ve direksiyondaki el. Kodla ikna edici olmaz; siluet ya da ışıklı cam olarak çözülür.
- **Yapılamaz:** çizerin el kararı (hangi tuğlayı çizmeyip bıraktığı). Kural yazılabilir, ama o zevk kopyalanamaz ve kopyalanmamalı.

## Hukuk
**Risk: orta. Üslup serbest, bu karenin kendisi değil.**

- Kaynak belirsiz. Kullanıcıya WhatsApp'tan gelmiş, künyesi yok. Duvardaki afiş Lehçe ("Rzeczy niemożliwe robimy od ręki…"), araba Fiat 126p'ye benziyor: büyük olasılıkla Polonyalı bir çizerin ya da stüdyonun telifli işi. Çizeri kareden tanıyamadım; ad vermiyorum. Örnek depoya, videoya, kapağa girmez.
- Üslup (düz renk, mürekkep kontur, tek vurgu, gece tonu) korunmaz; ortak bir çizgi roman dili. Korunan şey belirli ifade: bu araba + tavanda sarı kutu başlı antenli robot + bavul + bu sokak düzeni birlikte. Bu birleşim ya da robot tasarımı yeniden çizilmez.
- Çizerin imza görünümü: bu çizgi karakteri, duman biçimleri ve "az tuğla" kararı birlikte tek bir ele işaret ediyor. Motor kuralı alsın, eli almasın. Üslup kapısı kareleri örnekle yan yana konup "aynı çizerin işi sanılır mı?" diye bakılmalı.
- Gerçek otomobil tasarımı: tanınan bir modelin birebir yan görünüşü kullanılacaksa tarihî bağlamda olmalı; logo ve marka yazısı çizilmemeli. Bağlam yoksa genel bir küçük araba.
- Afişteki metin kopyalanmaz. Duvar yazısı gerekiyorsa kendi Türkçe metnimiz.
- Hassasiyet (yeni motor için): tahta perde sıra hâlinde dik, yuvarlak tepeli nesne kalıbına yakın (mezar taşı okuması); uçları düz ya da kırık çizilmeli. Sarı kutu baş + iki nokta göz bazı tanınmış robot ve maskot tasarımlarını çağrıştırır; kullanılmamalı.
- Stanford'a alınan üç teknik (rölanti hareketi, tek vurgu oranı, ton sıkıştırma) soyut yöntem; hukuki risk taşımaz.

## Stanford için notu (kismen)
Üslubun kendisi alınmaz. Stanford'un görüntü kuralı kurulmuş: bodrum siyah-beyaz gözetim monitöründe, gözlem odası ve belgeler sıcak kâğıtta, renk yalnız kayıtta. Çizgi roman sıcaklığı ve sevimli nesne dili, yaşayan kişilerin anıldığı bir deney videosunun tonuna uymaz. Düz renkli üçüncü bir dil kuralı da bulandırır.

Alınabilecek üç teknik (hepsi `stanford/lib` içinde çözülür, yeni motor gerekmez):

1. **Rölanti hareketi (bant sahnesi, gözlem odası).** Örnekte kamera hiç oynamıyor, karenin üçte biri her karede yaşıyor. Stanford'un en durağan planları tam böyle: masada dönen makaralı ses bandı, gözlem odasında bekleyen siluet. Makara dönüşü, VU ibresinin titremesi, sigara ya da kahve dumanı, flüoresan kırpışması 3 karede bir tutulan küçük oynamalarla verilirse "donuk plan yok" kuralı kamera hilesi olmadan karşılanır. Dikkat: makaraya halka tarama verilmez (hedef tahtası okuması).

2. **Tek tonlu dünya + tek küçük vurgu (bant sahnesi, belge).** Örnekte doygun renk karenin %1'i ve göz yalnız oraya gidiyor. Stanford'da "renk yalnız kayıtta" kuralı aynı oranla uygulanabilir: kayıt lambası ya da bant etiketi karenin %1-2'sini geçmesin, başka hiçbir yerde doygun renk olmasın. Renk kırmızı seçilirse kan gibi okunan leke ve dolu daire biçimi taranmalı.

3. **Gece tonu siyahla değil, ton sıkıştırmayla (koridor monitörü).** Örnekte gece, bütün değerleri dar bir orta-gri aralığına çekip çizgiyi en koyu değer bırakarak kurulmuş. Koridor monitöründe siluet ve numara okunmuyorsa çözüm kontrastı açmak değil bu olabilir: zemin orta gri, siluet en koyu, numara en açık.

Alınmayacaklar: pencere içi yüzler (Stanford'da yüz yok), sevimli robot-araba dili, mavi-gri palet (monitör nötr gri kalmalı), değişken kalınlıklı mürekkep çizgisi (monitörün tarama çizgisiyle çatışır).
