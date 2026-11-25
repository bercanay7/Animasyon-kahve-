# pastel-boyali-sinematik (v1)

Kullanıcının 25 Kasım 2026'da gönderdiği üslup örneği: pastel gökyüzü, eski araba, araba içi (video 4,6 sn; telifli karakter içeriyor).
- Örneğin kendisi depoda yok (telif; yalnız başvuru).
- Çözümleme ve yön metni Fable'ın; yön metni ayrı bir ajanla sınandı (telif, kanal kuralları, mevcut motorlarla çakışma).

## Karar: ayrı motor
Kanalın bütün motorları ya tek renkli ya da baskı taklidi: gravür, vazo, ağaç baskı, mürekkep, sessiz film, gazete tramı, monitör. Hepsi çizgi ya da tarama üzerine kurulu. Bu örnek tersini yapıyor: çizgisiz, tam renkli, düz boya lekesi ve derinlik katmanı. Kâğıt kesme (orfeus) en yakını ama o da kâğıt dokusu ve düşen gölgeyle "kesilmiş" okunuyor, hava ve ışık taşımıyor. Dorian'ın yağlıboya katmanı tek bir nesne için yazıldı, sahne motoru değil.

Bu yüzden mevcut bir motora ek olmaz; ayrı motor. Ama dar tutulmalı: motorun işi manzara, araç, ışık ve katman kayması. Örneğin iç plandaki yüzlü figürler motorun kapsamına girmez.

Değer gerekçesi: kanal 20. yüzyıl konularına kayıyor (Çernobil, Stanford) ve bu konulara gravür yakışmıyor. Renkli, modern, yol ve şehir taşıyan bir motor eksik. Maliyet düşük sayılır, çünkü hareket katman kaymasından geliyor; kare kare çizim yok.

Önce bakılacak: `cinecode/styles/` altında `cel-anime-80s.md`, `hd-2d.md` ve `midcentury-toon.md` var. Adlarından yakın görünüyorlar; içlerini okumadım. Motoru yazacak oturum önce bunları okumalı, işe yarayan tarif varsa oradan başlamalı.

## Yön metni (yeni bir oturuma verilir)

> Yeni bir çizim motoru: çizgisiz, renkli, düz boya lekesiyle manzara. Kanalda çizgisiz düz boya zaten var: İkaros'un serigrafi motoru (`ikaros/lib/silk.js`) opak katman basıyor, paleti günün saatinden alıyor ve sözcükte değiştiriyor. Oradan başla. Bu motorun ekleyeceği şey "hava ve ışık": derinlik, atmosfer, nesne başına ton.
>
> Başvuru karesini taklit etme. O kırmızı araba (tanınan marka ızgarası ve logosu dahil), o ayı başlıklı sürücü (Disney'in Duffy'si, köşedeki "Mr.DUFFY" yazısıyla telifli karakter), o pembe-turkuaz gök bir çizerin imzası; hiçbiri alınmaz. Aldığımız şey usul: kontur yok, nesne başına iki ya da üç ton, gölge sert kenarlı ve renkli, karede tek doygun vurgu.
>
> Görüntünün kuralı şu: figür durur, dünya kayar. Hareketi çizimden değil derinlik katmanlarından çıkar; uzak katman neredeyse sabit, en öndeki bulanık ve hızlı. Yol yoksa da donuk plan yok: durağan mekânda katmanlar kamerayla kayar. Işık yumuşak geçişle değil, bir sözcükte tek basamakla değişsin. Paleti her video kendi saatine göre seçsin (sabah, öğle, akşam); motor paleti dayatmasın.
>
> Yüzün peşinden gitme. Başvurudaki yüzlü orta plan kodla tutmaz. İnsanı sırttan, profilden, camdaki yansımadan ya da ışığa karşı koyu siluet olarak ver; kanalın siluet ve karikatür kuralları burada da geçerli. Yürüyen figür gerekiyorsa `araclar/hareket/` var.
>
> Başlamadan İkaros'un motorunu ve `geriye_bakis.md`'sini, sonra `cinecode/styles/` altındaki `cel-anime-80s` (konturu ve CRT'si değil; bir kez boyanıp kaydırılan arka plan ve kaydırılmış şekille sert gölge), `hd-2d` ve `midcentury-toon` tariflerini oku; işe yarayan varsa sıfırdan yazma. SwiftShader'da render edilecek: katmanları önceden ve tohumlu çiz, kaydır; bulanıklığı küçük tuvalde üret. Önce ölç.
>
> Üslup kapısı tek kare değil: bir manzara, bir orta plan figür, bir yakın plan ve 15 saniyelik hareket. Dördü de tutmadan motor bitmiş sayılmaz. Hassasiyet taraması ilk karede başlar; tek doygun vurgu kırmızıysa kan gibi okunup okunmadığına özellikle bak.
>
> Yarayabileceği yerler: 20. yüzyıl ve sonrası konular, yol ve yolculuk hikâyeleri, bir nesnenin yolculuğu, film videoları (*Oppenheimer* köprüsü gibi). Mit ve eski tarih için değil.
>
> Gerisi senin kararın.
>
> Fable

## Sınamanın bulduğu ve yön metnine işlenenler
- (3) Mevcut motor atlanmış, üstelik yanlış bir öncülle: 'Kanalın bütün motorları tek renkli ve çizgili; bu ilk hava ve ışık motoru' doğru değil. İkaros motoru (ikaros/lib/silk.js, LemoLab MIT) zaten çizgisiz, opak düz boya katmanlarıyla çalışıyor. Günün saatine göre palet seçiyor (şafak, öğle, gün batımı, gece) ve paleti sözcüğe bağlı raklede değiştiriyor (ikaros/geriye_bakis.md 27-29; kapak_a.jpg). Dorian'ın portresi ve Lale'nin laleleri de renkli. Yön metni okuru doğrudan cinecode'a gönderiyor; bu, CLAUDE.md adım 7'deki 'önce kendi motorlarımız' sırasına aykırı ve yarı yarıya var olan bir katman ve palet altyapısını sıfırdan yazdırma riski taşıyor. Düzeltme: başlangıç noktası İkaros. Yeni olan kısım nesne başına 2-3 ton, renkli sert gölge, atmosferik derinlik ve paralaks.
- (1) Telif doğru ele alınmış (araba, ayı başlıklı sürücü, pembe-turkuaz gök alınmıyor; palet videonun saatine bırakılmış). Ama telifli karakter ve marka adıyla anılmamış. Sürücü Disney'in Duffy ayısı, köşede 'Mr.DUFFY' yazısı var. Araba da tanınan bir marka ızgarası taşıyor. Motoru yazan bunu açıkça bilmeli. Düzeltme: Duffy adı ve 'marka ızgarası ya da logosu yok' ibaresi eklendi.
- (2) Donuk plan kuralı yalnız yol sahnesinde güvence altında. 'Figür durur, dünya kayar' yolculuk yoksa (oda, durağan mekân) donuk plana kapı açıyor. İkaros'ta da ilk kurgunun %25,7'si donuktu. Düzeltme: durağan mekânda katmanların kamerayla kaydığı yazıldı.
- (2) Karikatür okuması yasağı anılmamış. Yalnız 'siluet kuralları' deniyor; renkli bir motorda yüzlü figüre kayma riski yüksek. Düzeltme: 'siluet ve karikatür kuralları' yapıldı.
- (2) Bu motora özgü bir hassasiyet riski var. Başvurudaki tek doygun vurgu kırmızı; koyu ve pastel zeminde tek kırmızı leke 'kan gibi okunan kırmızı leke' tuzağına düşer. Düzeltme: hassasiyet cümlesine kısa bir uyarı eklendi.
- (2) Belirlenimcilik anılmamış. Ağaç leke yığınları ve katman dokuları rastgele üretilmeye çok müsait. Düzeltme: 'tohumlu' sözcüğü eklendi.
- (küçük) cinecode tarifleri için not: cel-anime-80s renkli kontur ve CRT katmanı taşıyor, 'kontur yok' ile çelişir; hd-2d piksel diorama. Metin 'işe yarayan varsa' dediği için engel değil. Yine de cel-anime-80s'ten yalnız 'arka planı bir kez boya, sonra kaydır' ve 'kaydırılmış şekille sert gölge' usullerinin alınacağı belirtildi.
- (4) ve (5) Sorun yok. Vaat edilenlerin hepsi Canvas 2D ve SwiftShader'da yapılabilir: katman kaydırma, küçük tuvalde bulanıklık, camdaki yansıma, sert renkli gölge. Metin büyük ölçüde yön veriyor; teknik cümleler kısa ve kanal kuralıyla örtüşüyor ('önce ölç').

## Çözümleme
## v1: pastel yol, kırmızı araba, araba içi

**Ne baktım:** 66 karenin 24'ünü (1-12 ve 37-48) tek tek, kalanını özet şeritten gördüm; ölçüler `olcum.json`'dan. 66 kare / 4,6 sn, yani yaklaşık 14 kare/sn (büyük olasılıkla GIF kaynaklı). Kare boyu 1000×476 (2,1:1).

**Güzel yapan şey (tek cümle):** az sayıda düz boya lekesi, sert kenarlı gölge ve tek sıcak vurgu rengi; hareket çizimden değil katman kaymasından geliyor.

### Palet (k-means, pay)
| Hex | Pay | Ne |
|---|---|---|
| `#F8DEE9` | %17,2 | gökyüzü pembesi |
| `#584344` | %17,2 | gölge moru-kahve |
| `#E4D6E2` | %16,0 | açık leylak (gök, yol) |
| `#251C16` | %13,4 | en koyu: ağaç içi, araba içi |
| `#806B69` | %11,7 | orta gölge |
| `#CABDC6` | %10,1 | duvar, yol grisi |
| `#BA9091` | %7,9 | gül kurusu (yol, ten) |
| `#BBDFE9` | %6,6 | gökte turkuaz şerit |

- Karenin yaklaşık yarısı açık pastel, üçte biri sıcak koyu. Saf siyah ve saf beyaz yok; en koyu ton kahve.
- Arabanın ve koltukların kırmızısı kümeye girmiyor (%7'nin altında): doygun renk küçük alanda, odak orada.
- Soğuk renk tek: turkuaz, yalnız gökte ve camlarda.

### Çizgi, dolgu, gölge
- **Kontur yok.** Biçimi leke kenarı kuruyor. İnce çizgi yalnız ayrıntıda (ızgara, gözlük, direksiyon).
- **Nesne başına 2-3 ton:** ışık, gölge, bazen kenar ışığı. Geçişler sert; yumuşak geçiş yalnız gökte.
- **Ağaçlar:** koyu yuvarlak leke yığını, üst kenarında sarı-yeşil ışık lekesi. Gövde ince ve eğri.
- **Gölge renkli:** yoldaki gölge gri değil mor.

### Işık
- Alçak güneş, yandan. Farlar beyaz daire + hafif hare; tek "ışık kaynağı" efekti bu.
- İç sahnede 42. karede ölçülen sıçrama (fark 22,3; çevresi 2-7): bir karede sıcak ışık dalgası giriyor, saç ve koltuk turuncuya dönüyor. Işık basamaklı değişiyor, yumuşak geçişle değil.

### Doku
- Kendi greni yok denecek kadar az; görülen kirlilik sıkıştırma izi. Fırça dokusu yalnız gökteki uzun yatay lekelerde.

### Figür
- Kadın: baş büyük, yüz 4-5 lekeyle (gözlük dairesi, kapalı göz yayı, dudak). Göz çoğu karede kapalı. Eller direksiyonda, sabit.
- Sürücü ayı başlıklı: yüz yerine maske. Bu, yüz sorununu atlatmanın hazır bir örneği.

### Kompozisyon
- Dış plan: ufuk karenin alt üçte birinde, araba sağ-orta, gök karenin yarısından fazlası. En önde bulanık koyu-kırmızı lekeler (ön plan katmanı).
- İç plan: ön camdan içeri, simetrik iki figür, camlar çerçeve içinde çerçeve.

### Hareket (kare sayımı)
- **Kesme tek:** 30. karede (fark 90,6).
- **Dış plan (1-30):** 65 karenin 65'i değişiyor, ortalama fark 20-60. Ama araba 12 karede aynı çizim, aynı yerde. Değişen şey arka plan: en az 4 derinlik katmanı farklı hızda kayıyor (uzak tepeler neredeyse sabit, duvar yavaş, ağaç ve palmiyeler hızlı, öndeki bulanık lekeler en hızlı). Yani "her karede yeni çizim" yok; her karede katman kayması var.
- **İç plan (31-66):** fark 2-7. Figürler tutuluyor. Yeni çizim yalnız göz kırpmada (kadın 37-41 arası, ayı 46. karede) ve camın dışındaki manzarada.
- **Ara kare, sürtünme (smear), ezme-uzatma:** baktığım 24 karede yok.
- **Kamera:** yana izleme, sabit hız. Yaklaşma yok.

### Kodla yapılabilirlik
- **Kolay:** düz leke manzara, gök şeritleri, çok katmanlı kayma, sert gölge, basamaklı ışık değişimi, far haresi. Canvas 2D yolları yeter; katmanlar önceden tuvale çizilip kaydırılırsa SwiftShader'da ucuz.
- **Orta:** leke yığını ağaç (tohumlu daire kümeleri + ışık kenarı), ¾ açıdan araba (tek sabit çizim olduğu için el emeği, hareket yok).
- **Zor:** araba içindeki kadının yüzü ve eller. Örnekte de neredeyse hiç oynamıyor; biz de oynatmayız ama çizmek bile kanalın zayıf yanı.
- **Yapılamaz sayılmalı:** bu düzeyde yüz ifadesi olan orta plan. Karşılığı: sırttan, profil, camdaki yansıma ya da koyu siluet.

**Not:** `cinecode/styles/BIZIM_NOT.md` belirtilen yolda yok; tarifleri açıp okumadım, yalnız adlarını gördüm.

## Hukuk
Risk yüksek; örnek yalnız başvuru olarak kalmalı.

- **Telifli karakter:** köşedeki "Mr.DUFFY" yazısı ve ayı başlığı Disney'in Duffy ayısına işaret ediyor (kucaktaki ve arka koltuktaki peluşlar da aynı tasarım). Ayı başlıklı sürücü fikri, yüz deseni ve denizci şapkası hiçbir biçimde alınmaz.
- **Çizer imzası:** "CANZONE 2019" bir çizerin imzası. Bu pembe-turkuaz gök, leke ağaçlar ve kırmızı araba birleşimi onun tanınır görünümü; birebir palet + kompozisyon kopyası yapılmaz. Yön metni bunu açıkça yasaklıyor.
- **Marka ve tasarım:** araba tanınır bir BMW (çift böbrek ızgara, dört yuvarlak far, amblem). Motorla çizilecek araç genel bir dönem arabası olmalı; ızgara ve amblem kopyalanmaz.
- **Serbest olan:** çizgisiz düz boya, sert gölge, katman kayması, pastel gök gibi genel teknikler korunmaz; bunlar alınabilir.
- Örnek dosyalar videoya girmez, depoya kopyalanmaz.

## Stanford için notu (degil)
Stanford'a üslup olarak girmez. Videonun kuralı "bodrum siyah-beyaz monitörde, renk yalnız kayıtta"; pastel, sıcak, tatil havası taşıyan bu görüntü o kuralı bozar ve konunun ağırlığıyla çelişir. Yüzlü figür de "yüz yok, siluet ve numara" kararına aykırı.

Palet ve görünüm dışında, yalnız iki teknik fikir ödünç alınabilir; ikisi de mevcut `stanford/lib/ekran.js` içinde çözülür, yeni motor gerektirmez:

- **Koridor monitörü:** "figür durur, dünya kayar". Siluetler tutulur; hareket katmandan gelir (ön planda parmaklık ya da kapı kasası, arkada duvar). Donuk plan kuralını çizim yükü olmadan karşılar.
- **Gözlem odası ve belge planları:** ışığın sözcüğe bağlı tek basamakla değişmesi (örnekte 42. karedeki sıçrama). Sıcak kâğıtta lamba açılması ya da bandın dönmeye başlaması için uygun.

Bant sahnesine (renkli kayıt) bir şey alınmaz; oradaki renk bu pastel palet olmamalı.
