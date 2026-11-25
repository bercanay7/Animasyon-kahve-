# hardal-noir-cizgi-roman (r1)

Kullanıcının 25 Kasım 2026'da gönderdiği üslup örneği: çizgi roman sayfası: iki adam bir odada, hardal/kahve/mor palet, keskin ışık huzmeleri.
- Örneğin kendisi depoda yok (telif; yalnız başvuru).
- Çözümleme ve yön metni Fable'ın; yön metni ayrı bir ajanla sınandı (telif, kanal kuralları, mevcut motorlarla çakışma).

## Karar: ayrı motor
Ayrı motora değer, ama dar kapsamla: değerli olan çizimin kendisi değil, iki fikir.

- **Panel dilbilgisi:** tek anı şeritlere bölmek ve tek resmi aralığın iki yanında sürdürmek.
- **Işığın sert geometrik kama olarak çizilmesi.**

**Mevcut motorlarla çakışma**
- İkaros (serigrafi afiş): düz dolgu ve sınırlı palet zaten var. Dolgu katmanı oradan alınabilir, yeniden yazılmaz.
- Çernobil `baski.js`: tram ve tek renk kullanıyor; bu örnekte tram yok, çakışma az.
- Dorian ve Lale: iç mekân gravürle çözülmüş; sıcak, düz renkli iç mekân kanalda yok.
- cinecode'da `silkscreen-poster`, `midcentury-toon`, `risograph` düz renge yakın tarifler; panel düzeni olan tarif yok.

**Neden ek değil:** panel sistemi çekim sisteminin üstüne oturan ayrı bir katman (maske, aralık, aralığı aşan sahne) ve ışık kaması sahne kuruluşunu baştan belirliyor. İkisi birlikte kanalın hiçbir motorunda yok.

**Neye yarar:** bekleyen "psikolojik anlatım" önerisinin (Zweig, Dostoyevski: tek karar anı, tek oda, iki kişi) doğal üslubu bu.

**Maliyet uyarısı:** yüz ve el bu sayfadaki düzeyde yapılamaz. Motor ancak yüzü kadraj, el ve ışıkla kestiği sürece ayakta kalır. Üslup kapısı geçilmezse panel katmanı tek başına `film.js`'e ek olarak yaşar; düşüş yolu budur.

Doğrulanmayan: `styles/BIZIM_NOT.md` belirtilen yolda yok, cinecode tariflerinin içeriğini okumadım; çakışma değerlendirmesi dosya adlarına ve CLAUDE.md'ye dayanıyor.

## Yön metni (yeni bir oturuma verilir)

> Yeni bir çizim motoru: çalışma adı "oda". Kullanıcının beğendiği bir çizgi roman sayfasından yola çıkıyor, ama o sayfayı yapma. Sayfa depoya girmez, karakterleri çizilmez, çizerin fırçası taklit edilmez, sayfanın panel düzeni de aktarılmaz; düzen 16:9 için baştan kurulur. Ondan yalnız iki fikir alıyoruz.
>
> Birincisi: bir an panellere bölünür. Bu, aynı saniyenin üç dar şeridi olabilir (masaya bırakılan bir kalem, bir kapı kolu, duvarda büyüyen bir gölge). Tek bir resmin aralıkla ikiye kesilmiş hâli de olabilir. Kurgu kesmeyle değil, panelin açılmasıyla yürüsün. Ama açılan şerit donmaz: her şerit ilk saniyesinden hareket eder, hiçbir şerit 5 saniyeden uzun eylemsiz kalmaz.
>
> İkincisi: ışık bir biçimdir. Duvarda sert kenarlı, çapraz bir kama olur; lamba görünmez, izi görünür. Kama panel aralığını aşıp öteki şeritte sürer ve sözcüğe bağlı olarak kayar.
>
> Görüntünün kuralı: tek oda, tek renk ailesi, en çok beş ton, saf siyah ve saf beyaz yok; çizgi de renkli. Panel aralığının rengi de aileden seçilir. Ana figür ailenin en koyu tonunda bir siluettir; açık dolgulu, konturlu figür kâğıt kesme gibi okunur. Hangi renk ailesi olacağı videonun kararı.
>
> Kodun zayıf yanını üslubun kuralı yap: yüz hiçbir panelde bütün görünmez. Kadraj keser, el kapatır, kama gölgede bırakır. Düzlemli gerçekçi yüz çizmeye kalkma; ense, omuz, profil ve elin silueti yeter. Hareketi figürden bekleme; panel, ışık ve nesne hareket etsin.
>
> Düz dolguyu yeniden yazma; İkaros'a bak. Çekim sistemi kanalın en yeni film.js'i; panel onun üstünde, başka motorların da kullanabileceği bir katman olsun. Kama kenarı ve çizgi titreşimi tohumlu olsun. Panel başına ayrı tuvalin SwiftShader'daki maliyetini önce ölç.
>
> Üslup kapısı: boş oda, orta planda iki figür, yüzü kesilmiş bir yakın plan ve 15 saniyelik hareket (şeritler açılır, kama kayar). Bunları sayfanın sırasını kopyalamadan kur. Kapıda tam boy karede simge taraması yap; özellikle şunlara bak:
> - kesişen dikey ve yatay aralık (haç);
> - kesişen iki kama (dört kollu yıldız);
> - dökülen sıvının kana benzemesi.
> Panel içinde yazı olacaksa alt banda (y > 880) girmez. Kapı geçilmezse önce panel katmanını bırak; düz dolgu ve kamayı tek kadrajda dene. O da geçmezse motoru bırak ve kararın gerekçesini yaz.
>
> Yarayacağı yer: tek karar anını anlatan psikolojik videolar (Zweig, Dostoyevski), sorgu, pazarlık, iki kişinin bir masada oturduğu her hikâye.
>
> Gerisi senin kararın.
>
> Fable

## Sınamanın bulduğu ve yön metnine işlenenler
- Kopya riski (telif): ilk fikirdeki örnek şeritler (dökülen bardak, yarım bir yüz, uzanan el) r1'in üst sırasındaki üç panelin birebir içeriği. Üslup kapısı da (orta planda iki figür, yüzü kesilmiş yakın plan, üç şerit) sayfanın sırasını yeniden sahneliyor. Örnekler sayfada olmayan nesnelerle değiştirildi ve 'sayfanın panel düzeni aktarılmaz, 16:9 için yeniden kurulur' cümlesi eklendi. Bilinen telifli bir karakter yok (Duffy ya da benzeri görülmedi). Figür tasarımlarını (kel takım elbiseli adam, ak perçemli adam) 'karakterleri çizilmez' cümlesi zaten dışarıda bırakıyor.
- Donuk plan kuralı: 'kurgu panelin açılmasıyla yürüsün' cümlesi çizgi roman sayfası gibi açılıp donan şeritlere izin veriyor. Her şeridin ilk saniyeden hareket etmesi ve 5 sn kuralı eklendi.
- Ana figür koyu siluet olmalı: 'saf siyah yok' ve 'çizgi de renkli' kuralları, figürü açık dolgulu ve konturlu çizmeye götürebilir; bu 'kâğıt kesme' gibi okunur. Ana figürün ailenin en koyu tonunda siluet olacağı eklendi.
- Panel aralığı: r1'de sayfa beyazı (#FEFEFE) %30,5 pay alıyor. Yön metni 'saf siyah yok' diyor ama aralık rengini söylemiyor. 16:9'da ve TV'de geniş, saf beyaz aralıklar parlak çubuk ve boş kâğıt gibi okunur. Aralığın renginin aileden seçileceği eklendi.
- Simge riski panel düzeninin kendisinde: kesişen bir dikey ve bir yatay açık aralık haç okunur (kurallardaki 'açık dikey şerit + yatay kuşak'). Kesişen iki çapraz kama dört kollu yıldız okunabilir. Dökülen koyu kırmızı sıvı kan gibi okunabilir. Genel 'simge taraması yap' cümlesinin yanına bu üçü adıyla eklendi.
- Alt bant: çizgi roman dili yazı kutusu çağrıştırıyor. Panel içi yazının y > 880'e konmayacağı tek cümleyle eklendi.
- Kapı geçilmezse ne yapılacağını anlatan cümle belirsizdi ('panel katmanını bırak, motoru bırakma kararını gerekçesiyle yaz' iki türlü okunuyor). Açıkça yeniden yazıldı: önce panel katmanı bırakılır, düz dolgu ve kama tek kadrajda denenir; o da geçmezse motor bırakılır ve gerekçesi yazılır.
- Çekim sistemi: CLAUDE.md 'Lale'nin film.js'i' diyor, ama stanford/lib/film.js bugün güncellenmiş ve Çernobil'den türemiş daha yeni bir sürüm (çapa hata günlüğü var). 'Kanalın en yeni film.js'i' olarak genelleştirildi; hangisi olduğu başkanın kararı.
- Belirlenimcilik ve SwiftShader yön metninde hiç anılmıyor. Kama kenarı ve çizgi titreşiminin tohumlu olacağı, panel başına ayrı tuval maliyetinin önce ölçüleceği tek cümleyle eklendi.
- Yeniden yazma ve vaat açısından sorun yok: düz dolgu İkaros'tan, çekim sistemi film.js'ten alınıyor; yüzü kesmek kodun zayıf yanını kural yapıyor. Metin adım adım talimat değil, yön veriyor.

## Çözümleme
**Ne:** tek sayfalık, durağan bir çizgi roman sayfası (736×1117). Ahşap kaplamalı bir odada iki takım elbiseli adam, bir sürahi ve bardaklar var. Hareket ölçümü yok; aşağıdaki "hareket" başlığı sayfanın ima ettiği zamanı anlatır. Yapı ve palet dışındaki sayılar gözle tahmindir.

**Palet (k-means, pay)**
- `#FEFEFE` %30,5: sayfa beyazı, yani panel aralıkları ve sol üstteki çerçevesiz boşluk. Resmin içinde beyaz neredeyse yok.
- `#E8A23C` %22,6: kehribar, ışık alan duvar.
- `#95633D` %17,8: gölgedeki ahşap.
- `#55363D` %11,0: mor-kahve. En koyu ton bu; saf siyah hiç yok.
- `#B29C6A` %9,3: haki, soğuyan gölge.
- `#F4C66F` %4,6: ışık kaması.
- `#E5D8B5` + `#F6F0E0` %4,3: gömlek, ak saç, bardak.
- Beyaz çıkarılınca resim tek renk ailesinde, beş basamakta kalıyor. Soğuk ton yalnız haki ile ceketlerdeki grimsi yeşil.

**Çizgi**
- İnce: 736 genişlikte yaklaşık 1,5–2 px, 1920'de 4–5 px eder.
- Kalınlığı hafif oynuyor, ucu kuru fırça gibi kesik.
- Renkli çizgi: duvar panoları koyu kehribarla, figürler mor-kahveyle çizilmiş. Siyah kontur yok.
- Bardak ve sürahide çizgi açık renkte, zeminden açığa çıkarılmış.

**Dolgu ve gölge**
- Her yüzeyde düz zemin ve tek gölge tonu var (yüzde en çok üç). Kenarlar sert, geçiş yok.
- Saçta ve takım kumaşında koşut kuru fırça taraması var; bu doku işi görüyor, gölge değil.

**Işık biçimi**
- Sayfanın asıl buluşu bu: ışık, sert kenarlı çapraz geometrik kamalar (yamuk, üçgen) olarak duvarın ve portrenin üstünden geçiyor.
- Aynı kama panel aralığını aşıp alttaki şeritte sürüyor.
- Abajur yalnız sağ üstte bir köşe olarak görünüyor; ışığın kaynağı değil, izi çizilmiş.

**Doku ve gren**
- Hafif kâğıt greni, dolguda fırça lekesi, yer yer serpme benek.
- Tram yok, baskı kayması yok.

**Figür kuruluşu**
- Gerçekçi oran, yaklaşık 7,5 baş.
- Yüzler tam çizilmiş (kaş, göz, burun gölgesi, çene düzlemleri), ama düzlemlere bölünmüş ve köşeli.
- Her yakın planda yüzün bir bölümü kadrajla ya da elle kapatılmış: dikey şeritte yarım yüz, ağzı örten yumruk, altta profil.
- Eller ayrıntılı ve yük taşıyor: bardağı tutan el, sürahiyi uzatan el.

**Kompozisyon**
- Üç kat:
  - Üstte çerçevesiz, beyaza açılan kuşbakışı iki figür; yanında üç dar dikey şerit (dökülen içki, yarım yüz, sürahiye uzanan el).
  - Ortada tek bir resmi ikiye bölen iki yatay şerit; duvardaki portre aralığın altında devam ediyor.
  - Altta paneli üstten taşan yakın profil ve bardak.
- Aralık genişliği sayfa eninin yaklaşık %2–3'ü.
- Ölçek sırası: geniş → ayrıntı → yakın → ayrıntı → orta → yakın. Ardışık iki panel aynı ölçekte değil.

**Hareket (ima edilen)**
- Dikey şeritler aynı anın üç dilimi: dök, bak, uzan.
- Yatay şeritler tek bir bakışın iki yarısı.
- Filme çevrilirse hareket figürden değil panelden gelir: şeridin açılması, kamanın duvarda kayması, panel içinde yavaş kaydırma.

**Kodla yapılabilirlik**
- Kolay: düz dolgu, iki tonlu sert gölge, renkli çizgi, ışık kaması (kırpma yolu ve çokgen), panel maskesi, gren, ahşap pano deseni.
- Orta: kuru fırça taraması (tohumlu koşut çizgiler), açık renkle cam çizimi, aralığı aşan tek resim.
- Zor: düzlemli gerçekçi yüz, bardağı kavrayan el, kuşbakışı kısaltılmış beden. Bunlar sayfanın en çekici yerleri ve kodun en zayıf yanı.
- Yapılamaz: yok. Ama yüzü bu düzeyde üretmeye çalışmak üslup kapısında düşer.

## Hukuk
**Orta risk; üslup düzeyinde kalınırsa düşük.**

- Örnek büyük olasılıkla yayımlanmış bir çizgi romanın sayfası. Çizeri ve eseri doğrulamadım. Karakterler (kel, takım elbiseli iri adam ve duvardaki portresi; şakakları ak saçlı adam) telifli ve belki markalı karakter tasarımı olabilir. Sayfa videoya, kapağa ve depoya girmez.
- **Serbest olanlar** (fikir ve teknik, korunmaz): panel bölmesi, sınırlı sıcak palet, sert ışık kaması, düz dolgu, renkli çizgi.
- **Kopyalanmayacaklar:**
  - bu sayfanın belirli düzeni birebir (üstte kuşbakışı + üç dikey şerit + portreli iki yatay şerit + altta bardaklı profil);
  - bu iki figürün tasarımı;
  - çizerin tanınır fırça ve yüz üslubu.
- Paletin hex değerleri ölçüm içindir, birebir alınmaz; yeni motor kendi renk ailesini seçer.
- **Stanford'a özel:** yaşayan kişiler için tanınabilir yüz ya da portre çizilmez. Panel yüz kestiği için bu yönde yardımcı.
- **Görsel hassasiyet:** panel aralıkları dikey ve yatay açık şeritler üretir; kesiştikleri yerde haç okunabilir. Koyu figür önünde açık dikey + yatay şerit birleşimi tam boy karede taranmalı. Bu sayfadaki içki ve bardak kanal videosuna taşınmaz; nesne videonun kendi nesnesi olur.

## Stanford için notu (kismen)
Stanford için yeni motor yazılmaz; iki teknik alınır, palet alınmaz.

**Alınacaklar**
- **Gözlem odası, bölünmüş şerit:** aynı anın üç dar şeridi (dönen makara, kayıt düğmesindeki el, masadaki kâğıt). Yüz göstermeden "biri dinliyor" duygusunu verir ve "yüz yok" kuralıyla örtüşür: şerit omuzda ya da elde keser.
- **Bant sahnesi (ekipten birinin gardiyandan sertlik istediği kayıt):** tek resmi aralıkla ikiye bölen yatay şerit. Üstte isteyen, altta dinleyen; ikisi de siluet ya da sırttan. Aralık ikisi arasındaki mesafeyi gösterir.
- **Koridor monitörü ile gözlem odası yan yana:** bir şerit siyah-beyaz monitör, bir şerit sıcak kâğıt. Bakan ve bakılan aynı karede olur.
- **Işık kaması:** gözlem odasında sıcak kâğıt üstünde tek sert kama (kapı aralığından ya da masa lambasından), sözcüğe bağlı kayar. Donuk planı çözer.
- **Belge planları:** belge birkaç panele bölünür ve altı çizili satır kendi şeridinde açılır. Levha süresi sınırına (≤ 8 sn) yardım eder.

**Alınmayacaklar**
- Kehribar doygunluğu: "renk yalnız kayıtta" kuralını bozar. Sıcak kâğıt soluk kalır, kama yalnız bir ton açık olur.
- Çizilmiş yüzler ve portre gibi tanınabilir kişi resmi: yaşayan kişiler var.
- Bodrum planları: monitör motorunda kalır, panel bölmesi oraya girmez.

Panel aralığı beyaz değil, kâğıt tonunda olmalı. Beyaz aralık monitörün yanında ikinci bir parlak odak üretir.

`stanford/uretim_plani.md` §4'ü açmadım; uygunluk görev tanımındaki özete dayanıyor.
