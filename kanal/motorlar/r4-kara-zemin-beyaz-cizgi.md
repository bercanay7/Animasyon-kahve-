# kara-zemin-beyaz-cizgi (r4)

Kullanıcının 25 Kasım 2026'da gönderdiği üslup örneği: siyah zemin üstüne beyaz kaba çizgi; sırtı dönük adam, tek lamba.
- Örneğin kendisi depoda yok (telif; yalnız başvuru).
- Çözümleme ve yön metni Fable'ın; yön metni ayrı bir ajanla sınandı (telif, kanal kuralları, mevcut motorlarla çakışma).

## Karar: ayrı motor
**Karar: ayrı motor, ama acelesi yok ve Stanford için değil.**

**Neden ayrı**
- Görüntünün kuralı mevcut hiçbir motorda yok: ışığın düştüğü yerde zemin ile çizginin yer değiştirmesi.
- Kanalın bekleyen önerisine birebir oturuyor: psikolojik anlatım, tek karar anı (Zweig, Dostoyevski). Tek oda, tek lamba, sırtı dönük adam; yüz çizmeden iç dünya.

**Mevcut motorlarla çakışma**
- **Gravür (`milton/lib`):** en yakın akraba. Tarama mantığı aynı, ama gravür açık kâğıtta düzenli ve paralel; burada zemin siyah, çizgi gevşek ve titrek. Milton'a "ters kutup" eki denenebilir, ancak düzenli tarama bu görüntüyü öldürür; tarama üreticisi yeniden yazılmalı.
- **Ağaç baskı (`kafka`):** siyah-beyaz ve sert kenar ortak. Kafka kütleyle çalışır (oyulmuş leke), bu çizgiyle.
- **Mürekkep (`ran`):** ters kutup; ıslak kenar ve geçiş var, burada yok.
- **Gözetim monitörü (`stanford/lib/ekran.js`):** karanlık pay benzer, ama tarama satırı, gren ve parlama var; çizgi değil görüntü.
- **cinecode `line-boil.md`:** titreme yöntemi (tohum döngüsü) oradan alınır. `one-line.md` ve `urban-sketch.md` çizgi dili için okunur. Hiçbiri kutup çevirmeyi içermiyor.

**Alınacak hazır parça**
- `film.js` Lale'den, tarama fikri milton'dan, titreme line-boil'den. Yeni yazılacak olan: akış alanlı tarama ve ışık maskesiyle kutup çevirme.

**Çekince**
- Motor yazmak en pahalı aşama. Bu motor, onu isteyen bir konu (psikolojik anlatım videosu) seçildiğinde yazılmalı; konusuz yazılmamalı.
- İddiam tek kareye dayanıyor; 15 saniyelik hareketin tutup tutmadığı üslup kapısında görülür.

## Yön metni (yeni bir oturuma verilir)

> Yeni bir çizim motoru: kara zemin üstünde beyaz çizgi. Baştan sona kur; kararlar senin.
>
> Kullanıcının beğendiği bir örnek var: karanlık oda, sırtı dönük oturan adam, tavandan tek lamba. O kareyi yeniden çizme. Sandalyesini, masasını, şişesini, kadrajını alma; çizerin el yazısını da taklit etme. Aldığımız şey bir kural.
>
> Kural şu: ışık renk değil, kutup değişimidir. Karanlıkta zemin siyah, çizgi beyazdır; ışığın düştüğü yerde zemin beyaza, çizgi siyaha döner. Sınır serttir. Ton dolguyla değil, çizgi sıklığıyla verilir ve tarama biçimi izler. Karenin üçte ikisi boş karanlık kalsın; tek bir sıcak ton olsun ve yalnız ışık kaynağında dursun, kişinin ya da nesnenin üstünde değil.
>
> Düzenli tarama gravüre döner; bizde gravür var (`milton/lib`). Kara zemin, oyulmuş beyaz çizgi ve tek renk de bizde var: ağaç baskı (`kafka/lib`, cinecode `woodcut`). Önce kutup değişimini ve titremeyi onun üstüne kurmayı dene; yeni motoru ancak o tutmazsa yaz. Bu motorun farkı gevşek, titrek, kapanmayan çizgi. `line-boil` tarifinden yalnız titreme yasasını al: tohumlu olsun, iki karede bir değişsin. Rengini ve dolgusunu alma. `film.js`'i Lale'den al.
>
> Yüz çizme. Figür sırttan, profilden ya da ışığın dışında dursun; ne düşündüğünü oda söylesin. Işığa girse de koyu kütle olarak okunsun. El gerekiyorsa nesneyi çiz, eli değil. Figür durabilir; hareketi ışık yapsın: lamba sallanır, sınır döşemede kayar, bir kapı açılır ve oda çevrilir. Yine de her plan ilk saniyeden hareket etsin; titreme tek başına hareket sayılmaz.
>
> Üslup kapısı tek kare değil: bir manzara, bir orta plan figür, bir yakın plan ve 15 saniye hareket. Kutup maskesi her karede yeniden çizilir; SwiftShader'da kare süresini önce ölç. Hareket tutmuyorsa motoru bırak, söyle.
>
> Hassasiyet taramasını ilk karede yap: sarkan kablo ile altındaki boş sandalye, tek lamba altında oturan adam (sorgu) nasıl okunuyor, tam boy karede bak.
>
> Nereye yarar: tek karar anını anlatan psikolojik videolar (Zweig, Dostoyevski), Kafka'nın diğer metinleri, gece geçen her hikâye.
>
> Gerisi senin kararın.
>
> Fable

## Sınamanın bulduğu ve yön metnine işlenenler
- (3) Gereksiz motor riski: yön metni yalnız gravürü (milton/lib) anıyor, en yakın akrabayı anmıyor. Kafka'nın ağaç baskı motoru (kafka/lib/woodcut.bundle.js, cinecode `woodcut`) zaten kara zemin üstünde oyulmuş beyaz çizgi. Tonu çizgi genişliği ve sıklığıyla veriyor, tarama biçimi izliyor ve 'yalnız yanan şeyde tek renk' kuralı var (Kafka'da aralık kapı ve ışık şeridi). CLAUDE.md'ye göre hazır motor işe yarıyorsa yenisi yazılmaz. Önce kutup değişimi ve titreme bu motorun üstüne denenmeli; yeni motor ancak o tutmazsa yazılmalı.
- (2) Ana figür koyu siluet kuralıyla gerilim var. Kutup değişiminde ışığın düştüğü yerde zemin beyaza, çizgi siyaha dönüyor. Figür ışığa girerse siyah çizgili açık bir figür olur; kanal kuralı ana figürün koyu siluet olmasını istiyor. Örnekte de adam karanlıkta koyu kütle, beyaz olan yalnız sandalye. Yön metni figürün ışıkta da koyu kütle kalmasını söylemeli.
- (2) 'Donuk plan yok' kuralıyla gerilim var. 'Figür durabilir; hareketi ışık yapsın' doğru bir yön, ama her planın ilk saniyeden hareket etmesi gerektiği söylenmiyor. line-boil titremesi tek başına eylem sayılmamalı; aksi hâlde lamba sallanmayan planlar donuk kalır (Kafka'nın bilinen zayıflığı: yalnız yavaş yaklaşmayla geçen planlar).
- (2) line-boil tarifine 'bak' demek eksik. Tarif renkli, düz dolgulu ve 'asla saf siyah değil' diyen bir çizgi filmi tarif ediyor; bu motorun iki değerli, siyah zeminli mantığıyla çelişiyor. Tariften yalnız titreme yasası alınmalı: tohumlu kayma, iki karede bir değişir, 3–4 tohum döner. Bu hem belirlenimciliği sağlar hem de Kafka'daki dosya şişmesi dersine (gürültü iki karede bir değişsin) uyar.
- (2, küçük) SwiftShader'da önce ölçme kuralı anılmıyor. Kutup değişimi her karede bir ışık maskesiyle iki kutbun birleştirilmesini istiyor; sallanan lamba maskeyi her karede değiştirir. Üslup kapısında kare süresi ölçülmeli.
- (1) Telif: sorun yok. Metin örneğin nesnelerini, kadrajını ve çizerin el yazısını açıkça yasaklıyor, yalnız kuralı alıyor; telifli karakter yok. (4) Vaat edilenler kodla yapılabilir: sert kenarlı kutup maskesi, biçimi izleyen tarama, titrek ve kapanmayan çizgi, sallanan lamba. Yüz ve el zaten dışarıda bırakılmış. (5) Metin büyük ölçüde yön veriyor; hassasiyet maddesi (sarkan kablo ve boş sandalye, lamba altında oturan adam) kanalın darağacı ve sorgu listesine uygun. Bunlar değişiklik gerektirmiyor.

## Çözümleme
**Örnek tek kare (720×1280, dikey). Hareket verisi yok; hareket satırı gözlem değil, öneridir.**

**Palet (olcum.json + kendi sayımım)**
- Saf siyah `#000000` %57,4; yakın siyahlarla (`#0E0D0E` %6,0, `#201F20` %5,2) birlikte karanlık ≈ %69. Parlaklık < 40 olan piksel %70,9.
- Beyaz `#FAF8FA` %12,4; parlaklık > 215 olan piksel %17,2.
- Ara griler (`#373638`, `#5C5A5C`, `#929093`, `#C8C6C7`) toplam ≈ %12. Bunlar ayrı ton değil: çizgi kenarı yumuşatması, JPEG ve masadaki tek gri örtü parçası. Gerçekte iki değerli bir resim.
- Tek renk: lambanın içi, soluk limon-krem (ortalama ≈ `#E2E5C2`), karenin yalnız %0,36'sı. Karede başka sıcak piksel yok.

**Onu güzel yapan dört şey**
1. **Işık çizgiyi değil zemini çevirir.** Karenin alt %22'sinde beyaz pay %62: lambanın düştüğü döşeme beyaz zemin + siyah çizgi, geri kalan her yer siyah zemin + beyaz çizgi. Geçiş sert, geçişsiz, kenarı düzensiz. Işık bir "aydınlatma" değil, bir kutup değişimi.
2. **Ton, çizgi sıklığıyla verilir.** Gölge dolgusu yok. Gömleğin sırtı omuzdan bele kıvrılan yatay taramayla, saç ışınsal kısa çizgilerle, döşeme perspektif çizgileriyle kurulmuş. Üç yüzey, üç tarama yönü; tarama biçimi izler.
3. **Karanlığın %70'i boş.** Sol üst çeyrek tamamen siyah. Göz üç yere gider: lamba (tek renk), sırt (en sık tarama), sandalye (en parlak beyaz).
4. **Yüz yok, hikâye var.** Adam sırtı dönük; ne düşündüğünü masa (şişe, bardaklar, boş ikinci sandalye) söylüyor.

**Çizgi**
- Kalınlık kadraj eninin ‰2–4'ü (720'de 1,5–3 px), neredeyse sabit; basınç değişimi az.
- Uç yuvarlak, renk tek (beyaz ya da siyah, zeminin tersi).
- Çizgiler titrek, köşelerde birbirini aşıyor, kapanmıyor; sandalye çift çizgiyle çizilmiş (iki paralel kontur, arası zemin rengi dolu).
- Boş karanlıkta birkaç başıboş ince çizgi ve nokta: "el" izlenimi buradan geliyor.

**Dolgu, gölge, doku**
- İki ton, kenar sert. Geçiş, bulanıklık, gren yok.
- Yere düşen gölge dolgu değil: sandalyenin altındaki taramanın sıklaşması.

**Figür**
- Oturan, sırttan ¾; baş kadraj yüksekliğinin ≈ %9'u, gövde geniş tek kütle.
- Yüz %0 çizilmiş (yalnız kulak ve ense çizgisi). El yalnız dirsekte bir yumru; parmak yok.

**Kompozisyon**
- Dikey; lamba üst kenardan kesik, figür sağ yarıda, masa sol orta, ışık havuzu altta. Lamba–baş–sandalye sağda tek dikey eksen.

**Hareket (öneri)**
- Çizgi 2–3 karede bir yeniden çizilir (3–4 tohum döner); tarama çizgileri kontura göre daha az titrer.
- Ara kare ve sürtünme gerekmez: figür durur, ışık hareket eder (lamba sallanır, kutup sınırı döşemede kayar).
- Kamera yavaş yaklaşma.

**Kodla yapılabilirlik**
- **Kolay:** siyah zemin, sandalye, masa, şişe, lamba; kutup çevirme (ışık maskesi + `difference` ya da iki tuval); çizgi titremesi (tohumlu sapma).
- **Orta:** biçimi izleyen tarama (bir akış alanı boyunca kesikli çizgiler, sıklık = ton).
- **Zor:** gömlek kıvrımının ve saçın "elle çizilmiş" inandırıcılığı; düzenli tarama hemen gravüre (milton) döner.
- **Bu örnekte gerekmiyor:** yüz ve el. Sırttan figür kodun zayıf yanını kendiliğinden atlatıyor.

## Hukuk
**Risk düşük, üç koşulla.**

- **Kaynak belirsiz.** Tek kare; kimin çizdiği bilinmiyor, sol alt köşede imzaya benzer bir karalama var (yapay zekâ üretimi de olabilir). Kaynağı bilinmeyen görsel depoya girmez, videoda ya da kapakta kullanılmaz, üzerinden çizilmez. Yalnız başvuru.
- **Üslup korunmaz, belirli çizim korunur.** Kara zemine beyaz çizgi (kazıma tahta, ters çizim) yüz yıllık ortak bir teknik; kullanılabilir. Bu karenin kendi düzeni (sırttan adam + bu sandalye + şişeli masa + konik lamba, aynı kadraj) yeniden kurulmaz.
- **Çizer imzasına yaklaşma riski.** Sert siyah-beyaz + tek renk lekesi, Frank Miller'ın *Sin City*'siyle özdeşleşmiş bir görünüm; özellikle siyah-beyazda tek sarı. Rengi bir kişinin ya da nesnenin üstüne koymak o imzaya yaklaştırır. Renk yalnız ışık kaynağında kalırsa ve çizgi gevşek taramayla kurulursa (Miller düz kütle kullanır) ayrışır. Yön metnine bu yüzden yazdım.

**Stanford'a özgü**
- Kişiler yaşıyor. Sırttan kadraj benzerlik riskini azaltır, ama içki, sorgu ışığı gibi kaynakta olmayan imalar kişilik hakkı sorunudur; üslup değil içerik riski. Yukarıda "alınmayacaklar"da.

**Hassasiyet (hukuk değil, tarama)**
- Sarkan kablo + boş sandalye (asılma) ve tek lamba altında oturan adam (sorgu) yeni motorun ilk karesinde tam boy bakılmalı.

## Stanford için notu (kismen)
**Üslup alınmaz, üç kompozisyon kararı alınır.**

**Neden üslup alınmaz**
- Stanford'un kuralı kurulu (§4): bodrum monitörde, gözlem odası ve belge sıcak kâğıtta, renk yalnız kayıtta. Beyaz çizgi-kara zemin üçüncü bir dil olur ve "hangi görüntü kayıt, hangisi anlatım" ayrımını bulandırır.
- Motor (`stanford/lib/ekran.js`) yazılmış, senaryo okuması yapılmış; üretimin ortasında üslup değişmez.

**Alınacaklar**
1. **Bant sahnesi: sırttan iki kişi, tek ışık.** Ekip üyesi ile gardiyanın konuşması sırttan ya da masanın üstünden kurulur; görüntüyü makara ve masa taşır, yüzü ses taşır. Yaşayan kişiler için en güvenli kadraj da bu. Örnekteki "tek sıcak ton yalnız ışıkta" fikri filmin "renk yalnız kayıtta" kuralıyla aynı mantık: sıcak ton makaranın ya da kayıt ışığının üstünde tek nokta olur (örnekte renk payı %0,36; bu ölçü hedef alınabilir).
2. **Gözlem odası: karanlığın payı.** Kadrajın büyük kısmı boş bırakılır, tek ışık havuzu masaya ya da monitörün önüne düşer. Sıcak kâğıt zemini bozmadan yapılır: koyu sepya boşluk, saf siyah değil.
3. **Koridor monitörü: tarama yönü.** Monitör görüntüsünde döşeme ve duvar çizgileri perspektifi taşısın; örnekte derinliği veren tek şey döşeme çizgileri. Ekran greninin altında bile okunur.

**Alınmayacaklar**
- Masadaki şişe ve bardak: yaşayan kişilerin sahnesinde içki iması olur.
- Tek lamba altında sandalyede tek adam: Stanford bağlamında sorgu ya da işkence okunur. Kaynakta olmayan bir sertlik iması görüntüyle eklenmiş olur; bant sahnesinde iki kişi aynı masada, eşit ışıkta durmalı.
- Sarkan lamba kablosu ile altında boş sandalye yan yana gelmemeli (asılma okuması).

**Belge planları**
- Alınacak bir şey yok; belge kendi kâğıdında kalır.
