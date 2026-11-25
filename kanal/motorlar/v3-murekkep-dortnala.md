# murekkep-dortnala (v3)

Kullanıcının 25 Kasım 2026'da gönderdiği üslup örneği: dörtnala atlı okçu; sınırlı palet, mürekkep çizgi, hız çizgileri (video 3,4 sn).
- Örneğin kendisi depoda yok (telif; yalnız başvuru).
- Çözümleme ve yön metni Fable'ın; yön metni ayrı bir ajanla sınandı (telif, kanal kuralları, mevcut motorlarla çakışma).

## Karar: ayrı motor
Ayrı motora değer, ama dar tanımlı bir motor olarak: "düz boya + ince kontur + poz döngüsü".

Mevcut motorlarla çakışma:
- **Mürekkep (`ran`)**: en yakın akraba ama ıslak fırça, yayılan leke ve kâğıt üstüne kurulu. Buradaki görüntü kuru, düz boyalı ve keskin; Ran motoruna ek yapmak onun gölgelendiricisini devre dışı bırakmak olur.
- **Serigrafi afiş (`ikaros`) ve vazo (`sisifos`)**: düz boya ve siluet ortak, ama ikisi de kontursuz ve hareketi kaydırma düzeyinde. Palet ve dolgu mantığı oradan alınabilir.
- **cinecode `cel-anime-80s`, `line-boil`, `ukiyoe`**: tarif olarak başvurulur, ama hiçbiri poz döngüsü vermiyor. (`BIZIM_NOT.md` bu dalda `styles/` altında değil, `cinecode/` kökünde.)
- **`araclar/hareket`**: yalnız iki ayaklı yürüyüş ve koşu. Dört ayaklı döngü, binici katmanı ve sürtünme yok.

Asıl yeni olan görünüm değil, hareket: az sayıda anahtar pozdan kurulan döngü, üstünde bağımsız zamanlanan ikinci katman, 12 kare/sn basamaklı zaman ve sürtünme lekesi. Kanalın bugüne kadarki hiçbir motorunda bu yok; "animasyon hiç durmasın" isteğine de en doğrudan cevap bu.

Çekince: en pahalı parça at. ¾ açıdan dörtnal kodla zor; motor bunu profil ve siluetle çözmezse üslup kapısından geçemez. Poz döngüsü çekirdeği `araclar/hareket` altına yazılırsa öteki motorlar da kullanır; görünüm katmanı ayrı kalır.

## Yön metni (yeni bir oturuma verilir)

> Yeni çizim motoru: düz boya, ince kontur, poz döngüsü. Kararlar senin.
>
> Kullanıcının beğendiği bir örnek var: dörtnala at üstünde okçu, üç saniyelik döngü. O örneği yeniden çizme. Atın koşumu, zırhın deseni, miğfer, o patlıcan moru at ve haki bozkır birleşimi çizerin imzası; hiçbiri alınmaz, örnek depoya da girmez. Alınacak olan teknik: karenin onda yedisi tek renk ailesinden soluk bir zemin, onun üstünde tek koyu kütle, yüzde beşi geçmeyen vurgu rengi, tek ağırlıkta ince kontur, geçişsiz düz boya.
>
> Görüntünün kuralı şu: hareket az çizimle, hiç durmadan. Örnekte at altı çizimlik bir döngüde koşuyor, binici onun üstünde kırk iki karelik tek bir eylem yapıyor; saniyede on iki çizim, tutulan kare yok, hızlı kol iki üç karede uzamış bir leke. Peşinden gideceğin şey bu ikili zaman: döngü taşır, eylem anlatır; eylem anlatımdaki sözcüğe bağlanır. Kamera figüre kilitli kalsın, hızı zemin ve gök söylesin.
>
> Kodla zor olanı örnek zaten atlatmış: yüz görünmüyor, eller tek leke. Sen de yüzü gizle ama kendi çözümünle (başlık, gölge, uzaklık); okunurluk dış çizgiden gelsin. Perspektifli at kodla çıkmaz; profilden ve siluetten kur, dörtnalı poz tablosuyla çöz, ayak yere bastığı karede kaymasın. Tabloyu örneğin karelerinden değil, kamu malı hareket etütlerinden (Muybridge) ya da kendi gözleminden çıkar. Döngü çekirdeğini `araclar/hareket` yanına, oradaki yürüyüş çözücüsünün dilinde yaz ki öteki motorlar da kullansın: kare t'nin saf fonksiyonu, rastgelelik tohumlu, hız SwiftShader'da önce ölçülür. Düz boya ve adımlı zaman için cinecode'daki cel tariflerine bir bak, sıfırdan icat etme. Kanalın görüntü kuralları ve hassasiyet listesi geçerli; kalkmış düz kol, yüze ya da alna giden el, yay ile okun kesiştiği haç biçimi ve hedef halkası gibi okumalara tam boy karede bak.
>
> Üslup kapısı tek kare değil: bir manzara, orta planda bir figür, bir yakın plan ve on beş saniyelik kesintisiz hareket. On beş saniyede döngü tekrarı sırıtıyorsa motor hazır değildir.
>
> Nereye yarar: atlı, yürüyüşlü, kovalamacalı her tarih ve mit videosu; bozkır, sefer, kurye. Kuryenin kendisi de bu motorla koşabilir.
>
> Gerisi senin kararın.
>
> Fable

## Sınamanın bulduğu ve yön metnine işlenenler
- Telif açığı: metin örneği yeniden çizmeyi yasaklıyor ama dörtnala poz tablosunun örneğin 42 karesinden çıkarılmasını yasaklamıyor. Kareleri kopyalayarak ya da üstlerinden geçerek tablo kurmak, çizerin animasyonunu birebir almak demek. Tablonun kaynağı kamu malı hareket etütleri (Muybridge, 1878) ya da kendi gözlem olmalı.
- İç çelişki: 2. paragraf miğferi imza sayıp yasaklıyor, 4. paragraf ise 'yüz miğferin altında… sen de öyle yap' diyor. Alınacak olan yüzü gizleme tekniği; miğfer alınmaz, yüz kendi çözümüyle gizlenir (başlık, gölge, uzaklık).
- Hassasiyet listesi okçuluğa göre eksik. Gerilen yayın üstündeki ok bir haç biçimi kuruyor; kirişi çeken el yüze ya da alna gidiyor ve 'alna giden el (selam)' okuması doğuyor. Kalkmış düz kol ve hedef halkasının yanına bu ikisi de yazılmalı.
- Kanalın çekim sistemi eksik: CLAUDE.md'ye göre her eylem bir cümleye ya da kelimeye (S/Wd) bağlanıyor. 'Eylem anlatır' cümlesi eylemi anlatımdaki sözcüğe bağlamıyor.
- Belirlenimcilik ve SwiftShader'da ölçme kuralları anılmıyor. Çekirdek ortak araç olacağı için araclar/hareket'in dilinde yazılmalı: kare t'nin saf fonksiyonu, rastgelelik tohumlu, hız önce ölçülür. Doğrulandı: hareket.js'de yalnız iki ayaklı yürüyüşler var (yuru/surun/kos), dört ayaklı yok; yani dörtnala çekirdeği gerçekten yeni.
- Gereksiz yeniden yazma riski küçük: mevcut motorların hiçbiri düz boya + ince kontur + adımlı zaman yapmıyor, yeni motor yerinde. Yine de CLAUDE.md'nin 7. adımındaki sıraya göre önce cinecode'daki cel tariflerine (cel-anime-80s: 12/8 kare/sn adımlama, düz cel, tutulan çizim) bakılması söylenmeli.
- Doğrulananlar: çözümleme doğru. Kare farklarında her 6 karede bir tepe var (altı çizimlik döngü), 42 karenin 41'i değişiyor, zemin ailesi %71, kontur %5. At örnekte ¾ açıdan çizilmiş; metnin profile yönlendirmesi kodun sınırlarına uygun ve kopyalamayı da azaltıyor. Telifli karakter yok. Metin adım adım talimat değil, yön veriyor.

## Çözümleme
## v3: dörtnala at üstünde okçu (3,36 sn, 42 kare, 500×578, 12,5 kare/sn)

**Güzelliğin kaynağı tek cümleyle:** dar ve soluk bir zemin paleti üstünde tek koyu kütle (at), ince ve kendinden emin bir kontur, ve hiç durmayan ama çok az çizimle kurulmuş bir döngü.

### Palet (olcum.json, k-means 8)
| Rol | Hex | Pay |
|---|---|---|
| Zemin ve gök, zeytin-haki ailesi | `#808065`, `#ABAD90`, `#8E8F70`, `#C1C2A3` | %71 |
| Ufuk bandı, yer gölgesi (sıcak gri) | `#635B53` | %10 |
| At gövdesi (patlıcan moru) | `#3A2D36` | %10 |
| Kontur, toynak, yele (siyaha yakın) | `#1E191C` | %5 |
| Bulut ve ot parıltısı (krem) | `#E7E9BF` | %5 |

- Vurgu renkleri (zırhta gri-mavi, kiremit kırmızısı, hardal) kümelemeye girmeyecek kadar az; karede gözle tahminim toplam %5'in altında. Göz oraya, yani biniciye gidiyor.
- Saf siyah ve saf beyaz yok. Bütün kare aynı sarı-yeşil filtreden geçmiş gibi; uyum buradan geliyor.

### Çizgi
- Tek ağırlıkta, ince (500 px genişlikte yaklaşık 1,5–2 px), koyu mor-siyah kontur. Uçlar sivri, fırça inceltmesi yok denecek kadar az.
- İç çizgi çok seyrek: atın boynunda ve sağrısında 3–4 kas çizgisi, o kadar.
- Koyu at üstünde açık renkli ince çizgi (dizgin, göğüslük kenarı): koyu kütlenin içinde okunurluğu bu veriyor.

### Dolgu ve gölge
- Düz boya, alan başına tek ton. Geçişli gölge (gradyan) yok.
- Biçim gölgesi neredeyse yok; yalnız yerde yumuşak kenarlı tek bir düşen gölge var.
- Sert kenar figürde, yumuşak kenar arka planda: derinlik bu karşıtlıktan çıkıyor.

### Işık, doku, gren
- Işık biçimi yok; yön duygusunu yalnız yerdeki gölge ve bulutların krem şeritleri veriyor.
- Kâğıt dokusu ya da gren görünmüyor (WhatsApp sıkıştırması ince dokuyu silmiş olabilir; bundan emin değilim).
- Yerde kısa, eğik, krem ot taramaları: hem doku hem hız göstergesi.

### Figür kuruluşu
- At uzun bacaklı ve ince bilekli, gövde tek büyük koyu şekil. Binici ata göre küçük; baş, gövdenin yaklaşık beşte biri.
- **Yüz çizilmemiş:** miğfer ve siperlik yüzü kapatıyor. Eller yumruk biçiminde tek açık leke. Kodla çizimin iki zayıf noktası örnekte zaten atlatılmış.
- Okunurluk siluetten geliyor: yay, miğfer tepeliği, atın kulakları ve bacak aralıkları dış çizgide.

### Kompozisyon
- Dikeye yakın kadraj, figür ortada ve karenin yaklaşık %70'ini kaplıyor. Ufuk alt üçte birde; koyu yatay bir bant figürü yere bağlıyor.
- Hafif alt açı, at kameraya doğru ¾ dönük: perspektifli bir poz, düz profil değil.

### Hareket (kareleri tek tek saydım)
- **Çizim her karede değişiyor:** 42 karenin 41'inde fark var; tutulan kare yok. Yani 12,5 kare/sn'de "birlerde", 24–25 kare/sn'ye göre "ikilerde" animasyon.
- **At 6 çizimlik bir dörtnal döngüsünde:** kare farkları her 6 karede bir tepe yapıyor (18–19'a karşı 13–15) ve 7. kare 1. kareyle aynı pozda. Bir sıçrama 0,48 sn; klipte 7 tur.
- **Binici ayrı katmanda ve döngüye bağlı değil:** yayı kaldırma, germe, bırakma, indirme 42 kareye yayılmış tek eylem. Altı çizimlik at, kırk iki karelik eylemi taşıyor; ucuzluk ve zenginlik buradan geliyor.
- **Ara kare yok denecek kadar az, sürtünme (smear) var:** kol yayı kaldırırken 2–3 karede bulanık, uzamış tek leke olarak çizilmiş (10. ve 39. kare çevresi).
- **Kamera:** figüre kilitli takip. At kadrajda 20–30 px yukarı aşağı ve ileri geri oynuyor; hareket duygusu arka plandan geliyor: yatay bulanık bulut şeritleri ve ters yöne akan ot taramaları.

### Kodla yapılabilirlik
| Parça | Derece | Neden |
|---|---|---|
| Palet, düz boya, tek ağırlıkta kontur | kolay | Path2D dolgu + çizgi; Canvas 2D'nin doğal işi |
| Akan zemin, bulanık bulut, yer gölgesi, ot taraması | kolay | tohumlu gürültü + düşük çözünürlüklü tuvalde bulanıklık |
| 12 kare/sn basamaklı zaman, sürtünme lekesi | kolay | zamanı kareye yuvarlamak; hızlı uzvu uzatılmış tek şekil olarak çizmek |
| Profilden dörtnal (6 anahtar poz, döngü) | orta | poz tablosu ve eklem zinciri gerekir; `araclar/hareket` yalnız iki ayaklı yürüyüşü çözüyor |
| ¾ açıdan, perspektifli at ve kısalan bacaklar | zor | her pozda hacim yeniden çizilmeli; 2B iskelet bunu veremez, elle 6 ayrı siluet yazmak gerekir |
| Zırh ayrıntısı, eller, kıvrılan gövdede binici | zor | çok parçalı ve üst üste binen şekiller; küçük ölçekte ve siluet olarak atlatılır |
| Çizerin el kararlılığı (her karede yeniden çizilmiş canlı çizgi) | yapılamaz | bizde çizgi parametrik; canlılık ancak poz seçimi ve zamanlamayla yaklaştırılır |

## Hukuk
- **Kaynağı bilinmiyor.** Klip WhatsApp'tan geldi; hangi yapımdan ya da çizerden olduğu belli değil. Profesyonel bir animasyon işinden kesit gibi duruyor, yani telifli sayılmalı. Videoya girmez, depoya kopyalanmaz, kapakta ya da Shorts'ta kullanılmaz.
- **Karakter tasarımı riski yüksek.** Koyu mor at + V biçimli perçinli göğüslük + kırmızı püskül + tepelikli miğfer + katmanlı zırh eteği birleşimi belirli bir karakter tasarımı. Tek tek öğeler tarihsel, ama bu birleşim ve oranlar kopyalanırsa "telifli karakter tasarımı kopyası" olur. Dönem giysisi gerekiyorsa müze kaynağından (Met Open Access, kamu malı) ayrıca kurulur.
- **Çizer imzası riski orta.** Haki zemin + patlıcan moru kütle + krem parıltı paleti ve ince konturlu uzun bacaklı at biçimi tanınır bir el. Teknik (dar palet, düz boya, tek ağırlıkta kontur, poz döngüsü) korunmaz ve serbestçe alınır; aynı renkler ve aynı at oranları alınmaz. Yeni motor kendi paletini konusundan çıkarmalı.
- **Hareket verisi.** Dörtnalın evreleri doğa gözlemidir, kimseye ait değildir; ama örnekteki altı pozu kare kare izlemek (rotoskop) türev iş sayılır. Poz tablosu kamu malı bir kaynaktan (Muybridge'in at fotoğrafları, 1887) ya da sıfırdan kurulmalı.
- **Hassasiyet.** Örnekte kanalın görüntü listesinden bir şey görmedim. Yeni motorda dikkat edilecek iki okuma: gerilmiş yayda ileri uzanan düz kol (selam) ve hedef olarak çizilecek yuvarlak nesnede halka.

## Stanford için notu (degil)
Görünüm olarak alınmaz. Stanford'un kuralı (`stanford/uretim_plani.md` §4) bodrumu siyah-beyaz gözetim monitöründe, gözlem odasını ve belgeleri sıcak kâğıtta gösteriyor; renk yalnız kayıtta. v3 ise renkli, düz boyalı, açık havada ve hız üstüne kurulu: palet, kontur ve akan zemin üç kuralla da çelişir. Sabit gözlem kamerası fikri de v3'ün figüre kilitli takip kamerasının tersi.

Yalnız iki teknik fikir taşınabilir, ikisi de görünüme dokunmadan:
- **Koridor monitörü ve bodrum planları:** basamaklı zaman. Monitördeki siluetlerin hareketi saniyede 12 çizime yuvarlanırsa hem kapalı devre kaydı duygusu güçlenir hem de `ekran.js`'in bulanıklığıyla iyi geçinir. Bu bir öneri; denenmeden karar verilmez, çünkü motor ve figürler zaten yazılmış durumda.
- **İsyan ve sayım gibi hızlı anlar:** sürtünme lekesi. Hızlı kol ya da cop hareketi iki üç karede uzamış tek koyu leke olarak çizilirse, yüzsüz siluetlerde eylem daha iyi okunur.

Gözlem odası, bant sahnesi ve belge planlarına alınacak bir şey yok: oralar durağan, nesne ve yazı üstüne kurulu.
