# pastel-buro-eskiz (r2)

Kullanıcının 25 Kasım 2026'da gönderdiği üslup örneği: büroda gazete okuyan adam, arkada gömlekli memur; kaba çizgi, pastel gren.
- Örneğin kendisi depoda yok (telif; yalnız başvuru).
- Çözümleme ve yön metni Fable'ın; yön metni ayrı bir ajanla sınandı (telif, kanal kuralları, mevcut motorlarla çakışma).

## Karar: ayrı motor
**Karar: ayrı motor, ama şartlı.**

**Neden ayrı:**
- Kanalın bütün motorları baskı tekniği taklidi: gravür, ağaç baskı, tram, vazo, mürekkep, sessiz film.
- Hiçbiri düz renk + fırça kontur + iç mekân ışığı yapmıyor.
- 20. yüzyıl büro, oda ve masa başı hikâyeleri için elimizde yalnız Çernobil'in gazete tramı var.
- Bu örnek o boşluğa oturuyor: modern çağ, kapalı oda, iki kişi arasındaki bakış.

**Çakışmalar:**
- `ran` mürekkep motoru fırça çizgisini yapıyor ama renk ve iç mekân yok. Çizgi zarfı oradan alınabilir.
- `dorian-gray` karma üslubun örtü maskesi, düz renk katmanı için yeniden kullanılabilir.
- cinecode tarifleri `midcentury-toon`, `risograph` ve `line-boil` komşu. Önce `BIZIM_NOT.md` ile bunlara bakılmalı; yarısı oradan gelebilir.

**Şart:**
- Motorun değeri yüzde değil, yerleşim ve ışıkta.
- Üslup kapısında yüzsüz hâli (profil, ense, kesik ön plan) hâlâ "çizgi roman karesi" gibi okunuyorsa motor yazılır.
- Okunmuyorsa motor yazılmaz, yalnız palet ve omuz üstü yerleşim mevcut motorlara not edilir.

**Sınır:** yalnız r2'ye bakarak karar verdim. Öteki örnekler aynı aileden çıkarsa tek motor yeter; her örneğe ayrı motor yazılmaz.

## Yön metni (yeni bir oturuma verilir)

> Yeni motor: düz renkli, fırça konturlu iç mekân. Çalışma adı "oda". Bir video değil, bir çizim motoru ve üslup kapısı yap; kararlar senin.
>
> Kullanıcının beğendiği bir örnek var: büroda gazete okuyan bir adam, arkasında ona bakan iki kişi. O kareyi yeniden çizme. Karakterlerini, yerleşimini ve çizerin el yazısını (o köşeli yüzler, o bıyık, o gömlek kıvrımı) taklit etme. Örnek depoya girmez. Ondan alacağın şey bir kural.
>
> Görüntünün kuralı şu: iki sıcaklık, bir mürekkep. Oda soğuk gri-yeşil, ışık hardal. Işık boyanmaz, kesilir: duvara düşen düz bir şekildir. Her yüzey iki ton, gölgenin kenarı sert. Mürekkep karenin ellide biri kadar; kontur ışık alan kenarda açık kalır. Ama ana figür gölge tonunda koyu bir kütledir; açık kalan figür iç çizgisiz bırakılmaz, yoksa kâğıt kesme okunur. Doygun renk yok. Bir videoda üçüncü bir renk girecekse tek nesneye girer ve bir sözcüğe bağlanır.
>
> Peşinden gideceğin şey çizgi değil, bakış. Derinlik bir dağarcıktır, sabit yerleşim değil: önde kadraja sığmayan biri ya da bir şey, ortada asıl figür, arkada küçük bir ayrıntı; izleyici çoğu zaman birinin omzunun üstünden bakar. Kodla yüz çizemeyiz; bunu saklama, kurala çevir. Profil, ense, inik göz kapağı, ışığa ters duran koyu gövde. Önden ifadeli yüz ve parmak hüneri yok; el bir nesneyi tutarken, nesne öndeyken görünür.
>
> Hareket az çizimli olsun: tutuşlar, tek tek oynayan parçalar (sayfa, baş, lamba ışığı), yavaş paralaks. Her plan ilk saniyeden kıpırdar. Gren ve çizgi kaynaması tohumlu olur ve iki karede bir değişir; SwiftShader'da önce ölç.
>
> Önce `cernobil` ve `stanford`un plakalı baskısına ve figürlerine (`baski.js`, `figur.js`, `hareket.js`) bak; düz ton plakası ve figür iskeleti orada. Sonra `ran`ın fırça çizgisine, `dorian-gray`in örtü maskesine ve cinecode'da `midcentury-toon`, `risograph`, `line-boil` tariflerine bak (önce `BIZIM_NOT.md`). Bu tariflerden yalnız malzemeyi ve kaynamayı al, karakter gramerini alma. Hazır olanı yeniden yazma.
>
> Üslup kapısı: bir oda manzarası, orta plan figür, yakın plan, 15 saniye hareket. Kapının odası, eylemi ve nesnesi örnekten farklı olsun: büro yok, gazete yok. Hassasiyet taraması o karelerde başlar: kayıtlı pencere haç, asılı lamba kandil, göğüste rozet amblem okunmasın. Alt bant (y > 880) yazısız kalır. Yüzsüz hâli hâlâ çizgi roman karesi gibi okunmuyorsa motoru yazma, nedenini yaz.
>
> Nereye yarar: Zweig ve Dostoyevski'deki karar anları, Kafka'nın bürosu, Oppenheimer, 20. yüzyılın masa başı hikâyeleri.
>
> Gerisi senin kararın.
>
> Fable

## Sınamanın bulduğu ve yön metnine işlenenler
- (3) Gereksiz yeniden yazma riski: yön metni ran, dorian-gray ve cinecode'u gösteriyor ama en yakın hazır altyapıyı atlıyor. cernobil/lib/baski.js ve stanford/lib (core, figur, dekor, hareket) plakalı çizimi (ton, çizgi, renk plakası, sonra gölgelendirici) zaten yapıyor; figür kütüphanesi hassasiyet kuralları içine gömülü olarak 20. yüzyıl masa başı tiplerini (takım, gazeteci, laborant) taşıyor. Bunlar anılmazsa motor plaka birleştirmeyi ve figürleri sıfırdan yazar. Düzeltme: bu ikisi bakılacaklar listesine eklendi, ilk sırada.
- (2) 'Ana figür koyu siluettir; iç çizgisiz açık figür kâğıt kesme okunur' kuralıyla gerilim var. 'Mürekkep %2', 'kontur ışık alan kenarda açık kalır' ve iki tonlu açık gömlek birleşince ana figür iç çizgisi olmayan açık bir figüre dönüşebilir. Düzeltme: ana figür gölge tonunda koyu bir kütle olur; açık kalan figür iç çizgisiz bırakılmaz.
- (1) Telif ve özgünlük: metin yerleşimi taklit etmeyi yasaklıyor ama hemen ardından örneğin yerleşimini kural olarak koyuyor (önde kadraja sığmayan biri, ortada ayakta biri, arkada küçük bir şey; omzun üstünden bakış). Ayrıca 'Nereye yarar: Kafka'nın bürosu' dendiği için üslup kapısı büyük olasılıkla büroda gazete okuyan bir sahneyle kurulur ve örnek yeniden sahnelenmiş olur. Düzeltme: üç derinlik sabit yerleşim değil, bir sinema dağarcığı olarak anlatıldı. Üslup kapısının odası, eylemi ve nesnesi örnekten farklı olacak (büro yok, gazete yok). Kopyalanmış bir telifli karakter yok (Duffy ya da benzeri); çizerin el yazısını yasaklayan cümle yerinde bırakıldı.
- (2) Hassasiyet taraması anılmıyor. Örnekte ve bu tür iç mekânlarda kanalın yakalama listesine giren öğeler var: kayıtlı pencere (haç), asılı lamba (kandil/mihrap), gömlekteki rozet (resmî amblem), siyah giysi üstünde beyaz yaka. CLAUDE.md'ye göre tarama üslup karesinde başlar. Düzeltme: bunlar tek cümleyle eklendi.
- (2) Belirlenimcilik ve ölçüm yok. Örneğin duvarındaki püskürtme gren ve line-boil'un kaynaması kare kare değişirse dosya şişer (CLAUDE.md: gürültü iki karede bir) ve işçiler arasında aynı kare çıkmaz. Düzeltme: gren ve kaynama tohumlu, iki karede bir; önce SwiftShader'da ölçülür.
- (2) Alt bant: öndeki nesneler (sayfa, gazete, belge) üzerindeki yazı y > 880 bandına düşebilir. Düzeltme: alt bant yazısız kalır.
- (küçük) Bakılacak cinecode tarifleri: midcentury-toon yumurta baş ve dört parmaklı eldiven kullanıyor, line-boil ise parlak palet, smear ve squash. Bu tarifler karakter grameriyle alınırsa yasak olan karikatür okumasına ve doygun renge kayılır. Düzeltme: yalnız malzeme (kaymış baskı, kopuk çizgi, düz gölge) ve kaynama mekanizması alınır diye yazıldı.
- (4) ve (5) için engelleyici bulgu yok. Yüz zayıflığı kurala çevrilmiş (profil, ense, inik kapak, koyu gövde) ve el yalnız nesne tutarken görünüyor, bu kodla yapılabilir. Metin adım adım talimat değil, yön veriyor; üslup kapısı ve 'motoru yazma, nedenini yaz' çıkışı yerinde.

## Çözümleme
**Örnek:** tek kare (900×753), hareket yok. Büroda üç derinlik planlı bir iç mekân: önde kadraja sığmayan sakallı profil, ortada gömlekli ayakta adam, arkada küçük bir baş, sağ altta çapraz giren gazete. Aşağıdaki sayılar `olcum.json` paletinden ve karenin gözle okunmasından geliyor; çizgi kalınlıkları ölçüm değil, göz kararı.

**Palet (8 küme):**
- Açık zemin: `#EBEEDA` %27,5 ve `#ECE3BD` %14,0. Toplam yaklaşık %41; karenin "havası" bu.
- Soğuk aile (adaçayı grisi): `#B2B49E` %12,3, `#9B9C89` %13,7, `#77766C` %10,0. Toplam yaklaşık %36.
- Sıcak aile (hardal): `#E2C089` %11,6, `#C2A173` %8,7. Toplam yaklaşık %20.
- Mürekkep: `#302E28` yalnız %2,1. Saf siyah değil, sıcak koyu kahve.
- Kural: iki sıcaklık ailesi ve bir mürekkep. Doygun renk, kırmızı ve mavi yok. Ten bile hardalın bir tonu.

**Çizgi:**
- Fırça kalem: kalınlık 900 px genişlikte yaklaşık 1–6 px arasında değişiyor (1080p'de yaklaşık 2–13 px).
- Uçlar sivriliyor, çizgi yer yer kopuyor.
- Kontur her yerde kapanmıyor: gömleğin ışık alan kenarı çizgisiz, zemine açılıyor.
- Tarama yok denecek kadar az: gazetede birkaç kuru fırça izi, kaş ve sakalda dolu siyah lekeler.

**Dolgu ve gölge:**
- Her malzemede iki ton: ışık ve tek gölge.
- Gölge kenarı sert; gömlekteki kıvrımlar düz bir leke.
- Yumuşak geçiş yalnız duvarda, o da gradyan değil püskürtme gren.

**Işık:**
- Işık bir "aydınlatma" değil, düz bir şekil: duvarda hardal dikdörtgenler, lamba başlığı tek hardal leke.
- Pencere beyaza yakın boşluk.
- Yön sağ üstten; öndeki figür ışığa ters, bu yüzden koyu aileden.

**Doku:**
- Bütün yüzeyde ince kâğıt greni.
- Renk lekelerinin kenarında kuru fırça ve hafif kayma (dolgu konturun dışına taşıyor ya da içinde kalıyor).
- Gazetede okunmayan satır dokusu.

**Figür:**
- Gerçekçi oranlı, köşeli sadeleştirme.
- Yüzler tam çizilmiş: kaş, göz, burun, bıyık. Kodla en zor kısım bu.
- Bir kolaylık var: öndeki profilde göz, inik bir kapak çizgisi; göz bebeği yok.
- Eller iki yerde görünüyor (bel, gazete) ve çizerin hüneri burada.

**Kompozisyon:**
- Omuz üstü çerçeve: ön plan karenin yaklaşık %40'ını kaplıyor ve kesik.
- Bakış üçgeni: okuyan adam, ona bakan adam, arkadan bakan baş.
- Gazetenin çaprazı gözü ortadaki figüre taşıyor.
- Güzelliğin yarısı çizimde değil, bu yerleşimde.

**Hareket:** kare tek; çizim sıklığı, ara kare ve sürtünme sayılamaz. Bu görünüm canlandırılacaksa dildeki karşılığı az çizimli tutuş, tek tek oynayan parçalar (gazete sayfası, baş dönüşü) ve yavaş paralaks olur.

**Kodla yapılabilirlik:**
- **Kolay:** iki aileli palet, düz ışık şekilleri, sert iki ton gölge, gren, dolgu-kontur kayması, üç planlı paralaks, gazete dokusu.
- **Orta:** değişken kalınlıklı, sivrilen ve kopan fırça çizgisi (yol boyunca kalınlık zarfı ve tohumlu titreme).
- **Zor:** kıvrımlı gömlek, eller.
- **Yapılamaz (bu kalitede):** önden ifadeli yüz. Profil, ense, kesik ön plan ve inik göz kapağıyla atlatılır.

## Hukuk
**Örneğin kendisi:**
- Çağdaş, telifli bir illüstrasyon. Gazetede Fransızca "Avis de décès" okunuyor; büyük olasılıkla bir Fransız-Belçika çizgi romanı ya da animasyon ön çalışması.
- Çizeri bilinmiyor; Pinterest ve WhatsApp yolu künyeyi silmiş.
- Videoya, kapağa ve depoya girmez.

**Üslup ve ifade ayrımı:**
- Korunmayan: düz renk, fırça kontur, iki aileli palet.
- Korunan: belirli ifade. Aynı üçlü yerleşim (sakallı profil, bıyıklı gömlekli adam, gazete), aynı karakter tasarımları ve aynı kare birebir yeniden kurulursa işleme eser sayılır.
- Yön metni bu yüzden kareyi değil kuralı veriyor.
- Hex değerleri de birebir kopyalanmaz; aile alınır, tonlar kendi kâğıdımıza göre yeniden seçilir.

**Çizerin imzası:** köşeli yüz kısaltması ve fırça el yazısı taklit edilmez. Yüzsüz kural bunu kendiliğinden sağlıyor.

**Stanford'a özgü:**
- Deneydeki kişiler yaşıyor. Bu üsluptaki gibi ayırt edici yüz çizmek benzerlik ve kişilik hakkı riski doğurur; siluet ve numara kuralı korunur.
- Rozet ve gömlek gerçek bir kurumun üniforması gibi okunmamalı.

**Motor için:**
- Yeni font ya da doku eklenirse `lisans-kontrol` becerisi ve `araclar/ASSETS.md` kaydı gerekir.
- Lemo ve cinecode tariflerinden yalnız teknik alınır; belgeler kopyalanmaz.

## Stanford için notu (kismen)
**Kısmen uygun: yalnız kâğıt dünyaya, üslup olarak değil yerleşim ve ışık olarak.** Stanford'un motoru ve kuralı kurulmuş; üretimin ortasında motor değiştirilmez.

**Alınır:**
- **Gözlem odası, omuz üstü üç plan:**
  - önde kadraja sığmayan bir ense ve omuz (gözlemci; koyu, yüzsüz);
  - ortada monitör;
  - arkada kapı ya da teyp.
  - Bodrumu izleyen birinin omzundan bakmak, "biri izliyordu ve istiyordu" fikrini görüntüyle söyler.
- **Bant sahnesi, düz ışık şekli:**
  - masa lambasının ışığı kâğıtta düz bir hardal leke olur;
  - teyp ve eller o lekenin içinde, oda soğuk gri-yeşilde kalır.
  - Renk yalnız kayıtta kuralı bozulmaz: hardal kâğıdın sıcak tonu sayılır, kırmızı kayıt lambası tek doygun renk olarak kalır.
- **Belge planları, ön planda çapraz kâğıt:**
  - belge kadraja alt köşeden çapraz girer, satırlar okunmayan doku olur;
  - okunacak tek satır sözcüğe bağlı olarak vurgulanır.
- **Gren:** kâğıt dünyasında gölge kenarına kuru gren; gradyan yerine.

**Alınmaz:**
- **Koridor monitörü ve bodrum planları:** siyah-beyaz tarama çizgili monitör kuralı aynen kalır; düz renk oraya girmez.
- **Çizilmiş yüz, bıyık, ifade:** plan "yüz yok, siluet ve numara" diyor. Kişiler yaşıyor.
- **Gömlekteki rozet:** kapak hassasiyet notu şapka ve rütbe istemiyor. Rozetli gömlek Türk polisi ya da memuru gibi okunur.
