# isik-sisi-siluet (v4)

Kullanıcının 25 Kasım 2026'da gönderdiği üslup örneği: ışık sisi içinde geyik silueti, katmanlı ağaçlar, huzmeler (video 8 sn).
- Örneğin kendisi depoda yok (telif; yalnız başvuru).
- Çözümleme ve yön metni Fable'ın; yön metni ayrı bir ajanla sınandı (telif, kanal kuralları, mevcut motorlarla çakışma).

## Karar: ayrı motor
Kanalın bütün motorları baskı ve kâğıt mantığında: gravür, vazo, kâğıt kesme, ağaç baskı, mürekkep, gazete tramı, sessiz film, monitör. Hepsinde görüntü bir yüzeye basılmış mürekkep. Bu örnek tersini yapıyor: görüntüyü ışık kuruyor, biçimler ışığın önünde duran karanlık. Hiçbir mevcut motorda derinliğe bağlı ışık karışımı, huzme ve arkadan aydınlatma yok.

Çakışmalar:
- Orfeus (kâğıt kesme) katmanlı siluet kullanıyor, ama kâğıt gölgesiyle; buradaki ışık sisi oraya eklenirse kâğıt okuması bozulur.
- cinecode'da `shadow-puppet` ve `paper-lantern` en yakın tarifler; ikisi de perde/fener arkası düz ışık, atmosfer perspektifi yok. Yeni motor yazılırken önce bu ikisi ve `BIZIM_NOT.md` okunmalı, işe yarayan parça oradan alınır.
- Stanford `ekran.js` ve Çernobil `baski.js` üç plakalı mimarisi (çizim plakası + gölgelendirici) burada da iskelet olabilir: siluet katmanları plakaya, ışık gölgelendiriciye.

Neden değer: kodla çizimin güçlü yanlarının (siluet, profil, ışık, dönüşüm) tam üstüne oturuyor ve yüz gerektirmiyor. Parçaların çoğu kolay; tek zor yer baş dönüşü, o da atlatılabilir. Mit ve doğa sahneleri olan videolarda (Gılgamış'ın sedir ormanı tipi sahneler, Frankenstein, Prometheus köprüleri) gravürden farklı, renkli bir seçenek açar.

Uyarı: bu görünüm stok vektör manzara ve duvar kâğıdı estetiğine çok yakın. Fikir (görüntünün kuralı) olmadan kullanılırsa kanalın en sıradan görünen videosu olur. Motor, bir video onu istediğinde yazılmalı; önden yazılmamalı.

## Yön metni (yeni bir oturuma verilir)

> Yeni çizim motoru: ışık sisi. Kanalın motorlarının çoğu mürekkeple çiziyor; bu motor ışıkla çizecek.
>
> Başvuru olarak verilen geyik sahnesini yeniden yapma. O geyik, o mor-sarı gün batımı, o çam dizisi, o kadraj alınmayacak. Stok manzara duvar kâğıdı da yapma; bu görünümün en kolay düştüğü yer orası. Alınacak olan tek ilke: en koyu biçim en parlak noktanın önünde durur, uzaklaşan her şey ışığa erir.
>
> Görüntünün kuralı şu olsun: karede tek ışık kaynağı var ve hikâyede bir anlamı var. Figür ona göre okunur; ışığa dönen, ışıktan çıkan, ışığı kapatan. Paleti her video kendi tek renk ekseniyle kurar; saf siyah ve saf beyaz yok.
>
> Işığın kıpırtısı hareket sayılmaz; sis içinde duran güzel bir manzara donuk plandır. Her plan sözcüğe bağlı bir eylemle yaşar, eylem ışığın kendisi de olabilir: yanar, söner, yer değiştirir, biri önüne geçer.
>
> Yüz çizme. Karakteri siluet, duruş ve baş açısı taşısın. Perspektifte dönen baş ve yürüyen bacak kodla zor: birkaç anahtar poz, kısa geçiş ve bedeni ota, sise, ön plan kütlesine saklamak yeter. Yürüyen figürde `araclar/hareket/` kullanılır. Yumuşak ışığı SwiftShader'da ölçmeden kurma; bulanıklık pahalı. Sis, toz ve huzme kıpırtısı tohumlu gürültüyle üretilir, işçiler arasında aynı kare.
>
> Hassasiyet taramasına ilk kareden başla: arkadan aydınlatılmış figür hale okunur, huzmeler kutsal ışık okunur, parıltıya verilen yıldız ya da çapraz parlama haç okunur. Tanrı ışıkla gösterilir kuralı bu motorda her ışığı şüpheli yapar.
>
> Üslup kapısı tek kare değil: bir manzara, bir orta plan figür, bir yakın plan, 15 saniye hareket. Yakın plan bu üslubun en zayıf yeri; orada ne göstereceğini bulamazsan motor hazır değildir.
>
> Hangi videoya yarar: orman, gece, ateş ve şafak sahnesi olan mitler, Frankenstein, doğa içinde geçen tek kişilik hikâyeler. Belge ve arşiv ağırlıklı videolara uymaz.
>
> Önce `shadow-puppet` ve `paper-lantern` tariflerine, sonra Çernobil ve Stanford'un plaka mimarisine bak.
>
> Gerisi senin kararın.
>
> Fable

## Sınamanın bulduğu ve yön metnine işlenenler
- (2) Donuk plan kuralı açıkta kalıyor: bu üslubun doğal hâli yavaş kıpırdayan bir manzara (örnekte 8 sn boyunca yalnız huzme saydamlığı ve geyiğin başı oynuyor). Işık kıpırtısının hareket sayılacağı sanılabilir. CLAUDE.md her planın ilk saniyeden hareket etmesini ve 5 sn'yi aşan eylemsiz aralıkların ölçülmesini istiyor. Bir cümle eklendi: tek ışık kaynağının kendisi (yanması, sönmesi, yer değiştirmesi, kapanması) sözcüğe bağlı eylem olabilir.
- (2) Hassasiyet listesinin bu motora en çok dokunan maddesi anılmamış: parıltıya verilecek yıldız ya da çapraz parlama dört kollu yıldız (haç) okunur. Hale ve huzme uyarısının yanına yarım cümle eklendi.
- (2) Belirlenimcilik anılmamış: huzme saydamlığı, toz ve sis kıpırtısı işçiler arasında aynı kare için tohumlu gürültüyle üretilmeli. SwiftShader cümlesine yarım cümle eklendi.
- (Olgu) 'Kanalın bütün motorları mürekkeple çiziyor' doğru değil: vazo, kâğıt kesme, monitör ve yağlıboya katmanı mürekkep değil. 'çoğu' diye düzeltildi.
- (1) Telif sorunu yok. Yön metni geyiği, mor-sarı paleti, çam dizisini ve kadrajı almayı açıkça yasaklıyor ve yalnız genel bir kompozisyon ilkesini alıyor (koyu biçim parlak noktanın önünde, atmosfer perspektifi). Telifli karakter yok.
- (3) Gereksiz yeniden yazma yok. Mevcut motorlarda sis ya da huzme katmanı yok (eşleşmeler yalnız 'Sisifos' sözcüğünden). Metin önce shadow-puppet ve paper-lantern tariflerine, sonra cernobil/lib/baski.js ile stanford/lib/ekran.js'teki plaka mimarisine yönlendiriyor; bu dosyaların hepsi var.
- (4) Kodla yapılamayacak bir vaat yok. Dönen baş ve yürüyen bacağın zorluğu açıkça kabul edilmiş, anahtar poz ve saklama çözümü önerilmiş. Yakın plan zayıflığı da üslup kapısına bağlanmış.
- (5) Metin adım adım talimat değil, yön veriyor. Son paragraftaki bakma sırası kısa ve 'Gerisi senin kararın' ile bitiyor.

## Çözümleme
## v4: ışık sisi içinde geyik (8 sn, 800×600, 115 kare ≈ 14,4 kare/sn)

**Onu güzel yapan tek şey:** en koyu biçim, en parlak noktanın tam önünde duruyor. Geri kalan her şey bu karşıtlığı korumak için susuyor.

### Palet (olcum.json, k-means 8)
| Grup | Hex | Pay |
|---|---|---|
| Koyular (ön plan, köşe kararması) | `#140717`, `#2E1824`, `#37294F`, `#51323A` | %56 |
| Ara tonlar (çayır, dağ, geyik gövdesi) | `#6D4064`, `#A16877`, `#CBA882` | %31 |
| Işık | `#EFEC96` | %13 |

- Tek renk ekseni var: mor-patlıcan koyudan soluk limon sarısına. Yeşil, mavi, kırmızı yok.
- Saf siyah ve saf beyaz yok; en koyu ton mora, en açık ton sarıya çekilmiş.
- Karenin yarısından fazlası karanlık; ışık yalnız %13 ama gözün gittiği tek yer.

### Çizgi
- Kontur yok. Hiçbir biçimin dış çizgisi çizilmemiş; her şey dolgu lekesi.
- Kenarlar sert (ağaç, kaya, boynuz), yumuşaklık yalnız ışıkta ve siste.

### Dolgu ve gölge
- Geyik 3 ton: koyu baş ve boynuz, orta mor gövde, sırtta ince açık kenar ışığı. Tonlar arası sınır sert, yüzeyli (düşük poligon hissi).
- Ağaçlar düz tek ton; derinlik tonla veriliyor, gölgeyle değil.

### Işık biçimi
- Ufukta, figürün arkasında tek yumuşak parıltı (radyal geçiş).
- Sol üstten sağ alta inen 6-8 çapraz huzme; kenarları yumuşak, saydamlıkları yavaşça değişiyor.
- Atmosfer perspektifi üç kademeli: yakın ağaç koyu ve opak, orta ağaç altın ve yarı saydam, uzak ağaç ışığa neredeyse erimiş hayalet. Dağ da iki kat, tepesi mor, eteği ışıkta kaybolmuş.
- Köşelerde belirgin kararma.

### Doku ve gren
- İnce gren bütün karede; çayırda dikey kısa fırça/ot dokusu.
- Havada tek tük ışıklı toz zerresi.

### Figür kuruluşu
- Yüz çizilmemiş: göz, ağız yok. Karakteri boynuzun siluetiyle baş-boyun açısı taşıyor.
- Geyik boynuzuyla birlikte kare yüksekliğinin ~%25'i; gövde çayıra gömülü, bacak hiç görünmüyor (en zor kısım saklanmış).

### Kompozisyon
- Ufuk ~%58'de. Figür soldan üçte bir çizgisinde, parıltının tam önünde.
- Sağ üçte bir koyu ön plan kütlesiyle (kaya, çalı) kapatılmış; sol alt köşede ikinci koyu kütle. Kare kendi içinde çerçeveli.
- 5 derinlik katı: ön plan çerçeve, çayır + figür, yakın ağaçlar, uzak ağaçlar, dağ + gök.

### Hareket (karelerde sayıldı)
- Geyik bölgesinde 114 kare geçişinin ~102'si değişiyor, yalnız ~12'si tutuluyor: **birler üzerinde, yumuşak ara değerli hareket.** Elle çizilmiş ikiler/üçler yok.
- Sürtünme (smear) yok, ezme-uzatma yok.
- Baş dönerken boynuz perspektifte dönüyor (önden çatal açık, profilde üst üste biniyor): büyük olasılıkla 3B model ya da çok katmanlı kukla.
- Eylem döngüsü: otlama → baş kalkar → ¾'ten profile döner → bekler → yeniden otlar.
- Ağaçlar tamamen sabit (fark 0,0). Kamera sabit, kaydırma ve yaklaşma yok.
- Gök ve ön planda sürekli küçük titreşim (0,3-1,2): huzmeler ve gren.
- 30, 60 ve 90. karelerde bütün kareye yayılan sıçrama var; düzenli aralığı sıkıştırma anahtar karesine işaret ediyor, çizim değişimi değil (varsayım).

### Kodla yapılabilirlik
| Parça | Zorluk | Neden |
|---|---|---|
| Katmanlı siluet manzara, atmosfer perspektifi | Kolay | Düz dolgu yollar + katman başına ışık rengine karıştırma |
| Parıltı, huzme, köşe kararması, gren | Kolay | Gölgelendiricide radyal geçiş + yumuşak şeritler; gürültü dokuya önceden yazılır |
| Toz zerresi, huzme titreşimi | Kolay | Tohumlu gürültü |
| Siluet figür, sert 3 ton | Orta | Yüz yok; kenar ışığı siluetin kaydırılmış kopyasıyla |
| Başın perspektifte dönmesi | Zor | 2B yolla olmaz; ya birkaç anahtar pozun arasında geçiş ya da basit 3B nokta iskeleti |
| Yumuşak ışık bulanıklığı | Dikkat | SwiftShader'da canvas blur pahalı; düşük çözünürlüklü tuvale çizilip büyütülür |

## Hukuk
**Üslup riski düşük, eser riski orta.**

- Örneğin kaynağı ve çizeri bilinmiyor (800×600 döngü; tasarımcı portfolyo paylaşımı biçiminde). Sahibi bilinmeyen bir eser olduğu için videoya, kapağa ya da depoya girmez; yalnız başvuru olarak bakılır.
- Korunmayanlar: katmanlı siluet manzara, atmosfer perspektifi, arkadan aydınlatma, ışık huzmesi. Bunlar ortak teknik, serbestçe kullanılır.
- Korunanlar: bu belirli sahnenin bütünü. Geyik + mor-sarı gün batımı + sağda çam kümesi + üçgen dağ + sağdan kaya çerçevesi birleşimi yeniden kurulursa uyarlama sayılabilir. Geyiğin model tasarımı da öyle.
- İkinci dikkat: bu görünüm, katmanlı turuncu orman ve geyik siluetiyle tanınan bir bağımsız oyunun afiş diliyle akrabadır. O oyunun paleti, gözetleme kulesi ve kadraj düzeni akla gelecek biçimde birleştirilmemeli.
- Önlem: palet her video için kendi konusundan kurulur, kadraj ve figür sıfırdan tasarlanır, üslup kapısı karelerinde örnekle yan yana bakılıp "aynı sahne mi?" diye sorulur.
- Karakter ve 5816 riski yok. Hassasiyet tarafı ayrı: arkadan aydınlatılmış figür hale, huzmeler kutsal ışık okunabilir; tarama listesine bu iki okuma eklenmeli.

## Stanford için notu (kismen)
Üslup olarak alınmaz: Stanford'un kuralı bodrumu siyah-beyaz monitörde, belgeyi sıcak kâğıtta göstermek ve rengi yalnız kayıtta tutmak (üretim planı §4). Mor-sarı gün batımı paleti, manzara katmanları ve romantik huzmeler bu kuralı bozar ve konunun tonuna ters düşer.

Alınabilecek olan yalnız ışık ilkesi, üç dar yerde:

1. **Gözlem odası (bant sahnesi, ters açı):** karanlık odada tek ışık kaynağı monitör. Masa, makaralı teyp ve iki sandalye monitör parıltısının önünde koyu siluet olur; "en koyu biçim en parlak noktanın önünde" ilkesi burada birebir işe yarar. Monitörden odaya yayılan soluk bir ışık konisi ve içinde birkaç toz zerresi, odanın kapalı ve havasız olduğunu söyler. Renk kuralı korunur: koni gri-soğuk kalır, kehribar teyp ışığı ve kırmızı kayıt lambası tek renk olmaya devam eder.
2. **Koridor monitörü:** atmosfer perspektifinin siyah-beyaz karşılığı. Kameraya yakın siluet en koyu, koridorun ucundaki figürler bir-iki kademe açık ve düşük kontrastlı. Sayım ve isyan planlarında derinliği numaraya ve tarama çizgisine yük bindirmeden verir.
3. **Köşe kararması:** monitör modunda zaten varsa dokunulmaz; yoksa eklenebilecek en ucuz parça.

Belge planlarına hiçbir şey alınmaz; kâğıt düz ve eşit aydınlık kalmalı, yoksa daktilo dökümü okunmaz.

Kısıt: film üretimde. Bu eklemeler yalnız render'dan önce ve yalnız `ekran.js`'e dokunmadan sahne düzeyinde yapılabiliyorsa değer; motoru yeniden açmayı gerektiriyorsa bırakılır. Karar başkanın.
