# gri-firca-storyboard (r7)

Kullanıcının 25 Kasım 2026'da gönderdiği üslup örneği: gri kaba fırça eskiz storyboard: tren, buhar, siluetler, tek turuncu ateş.
- Örneğin kendisi depoda yok (telif; yalnız başvuru).
- Çözümleme ve yön metni Fable'ın; yön metni ayrı bir ajanla sınandı (telif, kanal kuralları, mevcut motorlarla çakışma).

## Karar: mevcut bir motora ek
Ayrı motor gerekmez. Örneğin üç bileşeni kanalın üç plakalı mimarisine (`cernobil/lib/baski.js`, `stanford/lib/ekran.js`) bire bir oturuyor:
- gri opak değer boyası → TON plakası (`B.k`);
- siyah tarama darbeleri ve düz siluet → ÇİZGİ plakası (`B.l`);
- tek turuncu → RENK plakası (`B.c`).

Eksik olan iki parça var, ikisi de ek:
1. **Fırça kitaplığı** (`firca.js` gibi): tohumlu, sivrilen düz tarama demeti; kuru geniş darbe (önceden yazılmış gürültü maskeli damga); yırtık kenarlı değer lekesi.
2. **Üçüncü gösterim modu** (`mod: 'eskiz'`): tram ve tarama çizgisi yok, renk plakası toplamalı ışıma olarak basılır (ateş dumanı içeriden aydınlatır).

Figür, çekim sistemi, hareket ve araçlar olduğu gibi kullanılır.

**Çakışmalar:**
- **Mürekkep (`ran`):** fırça ilkelleri (`mk`, `draw`, `mass`, kuru darbe) en yakın akraba; darbe profilleri oradan örnek alınır. Ama Ran saydam mürekkep mantığıyla çalışıyor (yalnız koyulaştırır, pirinç kâğıdı, ıslak yayılma, vermilyon mühür). Bu örnekte açık ton koyunun üstüne sürülüyor ve ışık toplamalı; Ran'ın katmanına sığmaz.
- **Dorian / Lale karma üslup:** "tek renk yalnız bir şeyde" fikri kanalda iki kez kullanıldı. Burada yenilik renk değil, rengin ışık kaynağı olması.
- **cinecode tarifleri:** `ink-wash` (Ran'ın kaynağı), `line-boil`, `impasto` komşu; hiçbiri bu gri değer eskizini doğrudan vermiyor.

**Ne zaman yazılmalı:** Motor yazmak en pahalı aşama. Bu ek, ters ışık, duman ve tek ateş isteyen bir konu seçildiğinde yazılmalı; şimdiden değil. Aday konular: Frankenstein, Oppenheimer, Dostoyevski'nin idam sehpası, sanayi ve savaş konuları.

**Ek yazılırken yön:**
- Görüntünün kuralı: figür her planda en parlak lekenin önünde durur.
- Renk yalnız yanan şeydedir ve olay olduğunda gelir.
- Duman gradyanla değil darbeyle boyanır.
- Darbe titremesi iki karede bir, yalnız figür ve ateşte.
- Üslup kapısı dört parça: manzara + orta plan + bu örnekte hiç olmayan yakın plan + 15 sn yürüyüş.

## Çözümleme
## r7: gri kaba fırça eskiz storyboard (tek görsel, 736×1313, 2×5 = 10 panel)

**Sınır:** Bu tek bir durağan görsel. Kare farkı ölçümü yok; hareketle ilgili her şey aşağıda çıkarımdır, ölçüm değil. Görsel büyük olasılıkla yapay zekâ üretimi (vagon üstündeki harfler okunmuyor, lokomotif panelden panele tutarsız, boyut Pinterest ölçüsü). `BIZIM_NOT.md` `styles/` altında değil, `.claude/skills/cinecode/BIZIM_NOT.md` yolunda.

### Palet (olcum.json)
| Hex | Pay (tüm görsel) | Ne |
|---|---|---|
| #010101 | %37,5 | büyük kısmı panel arası siyah çerçeve |
| #F2F3F1 | %11,6 | kâğıt beyazı: buhar, far, zemin |
| #C3C3C2 | %10,6 | açık gri yıkama |
| #959390 | %10,5 | orta gri |
| #6F6B66 | %9,5 | orta-koyu, hafif sıcak |
| #474442 | %8,8 | koyu |
| #201F1F | %8,7 | siyaha yakın: siluet, lokomotif |
| #EAA557 | %2,8 | tek renk: turuncu ateş |

- Panellerin alanı görselin yaklaşık üçte ikisi (kaba tahminim). Buna göre panel içinde turuncu yaklaşık %4, saf siyah yalnız %5–6 dolayında.
- Turuncu 10 panelin 4'ünde var (2, 4, 6, 9). O panellerde alanın kabaca onda biri, ötekilerde sıfır. Renk "olay olduğunda" geliyor.
- Griler nötr değil, hafif sıcak (#6F6B66, #474442). Beyaz ise hafif soğuk. Turuncu bu yüzden bağırmadan oturuyor.
- Değer dağılımı neredeyse düz: beş gri basamağın her biri %9–12. Yüksek kontrastlı siyah-beyaz değil, tam merdivenli bir değer resmi.

### Çizgi
- İki ayrı çizgi ailesi var:
  - **İnce, hızlı, düz tarama darbeleri:** yaklaşık 1–3 px (1080 ölçeğinde 3–8 px), uçları sivrilen, demet hâlinde 5–15 paralel çizgi. Ray, vagon cephesi, direk, zemin gölgesi bunlarla kurulu.
  - **Geniş kuru fırça darbeleri:** panel genişliğinin %10–30'u, kenarı yırtık. Duman ve gökyüzü bunlarla.
- Kontur çizgisi yok. Biçim, değer lekesinin kenarından okunuyor.
- Çizgi rengi yalnız siyah ve koyu gri. Renkli çizgi yok.
- Darbelerin hemen hepsi çapraz (yaklaşık 15–35°) ve kaçış noktasına akıyor. Panelin enerjisi buradan geliyor.

### Dolgu ve gölge
- 5–6 ton, opak boya mantığı: açık gri koyunun üstüne de sürülüyor. Buhar, lokomotifin önünü beyazla "kesiyor". Bu saydam mürekkep (yalnız koyulaştıran) mantığı değil.
- Kenarlar karışık: siluet ve yakın nesnede sert, duman ve uzak planda yumuşak ve yırtık. Odak sert kenarla seçiliyor.
- Gölge ayrı bir katman değil; zemine atılmış birkaç koyu darbe.

### Işık biçimi
- Ters ışık: figür her zaman panelin en parlak lekesinin önünde (beyaz buhar, far, ateş). Okunurluğun tamamı bu.
- Derinlik değerle: öndeki figür #201F1F, ortadaki #6F6B66, arkadaki #C3C3C2 (panel 4, 8, 10).
- Işık kaynakları yuvarlak ve basit: lokomotif farı düz beyaz daire, ateş sarı çekirdekli turuncu bulut.
- Turuncu hem kaynak hem yansıma: zemine yatay turuncu çizgi (panel 6), vagon penceresine küçük turuncu dikdörtgen (panel 2, 6).

### Doku ve gren
- Kâğıt dokusu yok denecek kadar az. Doku fırçanın kendi kuruluğundan geliyor.
- Hafif JPEG yumuşaklığı var. Film greni yok.

### Figür kuruluşu
- Yüz hiç çizilmemiş: %0. Baş bir şapka lekesi.
- Boy yaklaşık 6–7 baş; uzun palto gövdeyi tek kütle yapıyor, bacaklar iki sivri darbe.
- El yok. Bir panelde (3) elde küçük açık bir leke var.
- Figür panel yüksekliğinin %25–55'i; çoğu sırttan ya da karşıdan yürüyor. Profil yok.
- Bu, kodla çizimin güçlü yanına tam oturuyor (siluet, ışık). Zayıf yan (yüz, el) üslubun kendisinde zaten yok.

### Kompozisyon
- Ufuk alçak (panel yüksekliğinin alt %20–30'u), tek kaçış noktası, raylar ve gölgeler figüre akan yönlendirici çizgi.
- Ölçek dizisi: geniş → orta → geniş → orta → geniş. Yakın plan ve ayrıntı yok; kanalın "ardışık iki plan aynı ölçekte olmaz" kuralı için yakın plan ayrıca icat edilmeli.
- Büyük koyu kütle (lokomotif, vagon) bir kenarda, figür ortada ya da karşı üçte birde.

### Hareket (çıkarım; ölçüm değil)
- Bu üslup hareket edince genelde şöyle çalışır:
  - çizim 2–3 karede bir yenilenir (30 fps'te 10–15 çizim/sn);
  - darbeler "çizilerek" belirir;
  - duman kütleleri yavaş kayar;
  - ateş 2 karede bir titrer;
  - kamera yavaş yaklaşır ya da katmanlar paralaksla kayar.
- Ara kare ve sürtünme (smear) için kanıt yok. Eskiz dokusu zaten bulanıklık işini görür.
- Kanal notu: karede değişen doku dosyayı şişirir. Darbe titremesi en çok iki karede bir, tercihen yalnız figürde ve ateşte olmalı.

### Kodla yapılabilirlik
- **Kolay:**
  - ters ışıklı siluet ve değerle derinlik;
  - düz tarama demetleri (tohumlu, sivrilen çizgi);
  - tek turuncu ışık ve ışıması;
  - far dairesi;
  - alçak ufuk ve kaçış çizgileri.
- **Orta:**
  - kuru geniş fırça (damga dizisi + tohumlu gürültü maskesi; önceden dokuya yazılmalı, SwiftShader'da karede hesaplanmamalı);
  - duman kütlelerinin "boyanmış" kalması (yumuşak gradyan kullanılırsa dijital sis olur, üslup kaybolur);
  - yürüyen palto silueti (`araclar/hareket/` ile; palto eteği ayrı sallanmalı).
- **Zor:**
  - lokomotif gibi karmaşık makinenin "eskiz gibi ama doğru" görünmesi (az darbeyle doğru kütle; kod fazla düzgün çizer);
  - darbelerin rastlantısal ama isabetli görünmesi (her nesne için elle darbe listesi gerekir).
- **Yapılamaz:** yok. Ama "bir insanın hızla çizdiği" duygusu tam tutmaz; "eskiz üslubunda düzenli çizim" olarak okunur.

## Hukuk
**Risk düşük, iki dikkat noktasıyla.**

- **Kaynak ve çizer belirsiz.** Görsel büyük olasılıkla yapay zekâ üretimi bir Pinterest görseli (okunmayan harfler, tutarsız lokomotif). Belirli bir çizerin imzası ya da tanınan bir filmin storyboard'u olarak tanımlayamadım.
- **Üslubun kendisi korunmaz.** Gri değer eskizi, ters ışıklı siluet ve tek vurgu rengi ortak storyboard ve hızlı boyama grameridir. Alınan yalnız teknik.
- **Kopyalanmayacak olan:** bu on panelin kompozisyonları, tren–ateş–paltolu adam dizisi ve panel sırası. Görsel depoya girmez, videoda ya da kapakta kullanılmaz. Kaynak belirsiz olduğu için "esinlenildi" künyesi de verilemez.
- **Karakter riski yok.** Şapkalı, uzun paltolu siluet jenerik kara film tipidir. Yine de kendi figürümüz dönemine göre çizilmeli, bu siluet aynen alınmamalı.
- **Hassasiyet (kanal listesi), bu üslup kendi videomuzda kullanılırsa:** tren + duman + bavullu ya da paltolu sıra hâlinde figürler + ateş, sürgün ya da toplama kampı olarak okunabilir (listedeki "baraka + çantalı figür" maddesi). Dikey direk ve sarkan çizgi darağacı, turuncu lekeler kan ya da yangın felaketi olarak okunabilir. Üslup karesinden itibaren tam boy karede taranmalı.
- **Stanford'da ek risk doğmaz:** alınan yalnız ışık düzeni. Yaşayan kişiler için yüz yok kuralı aynen sürer.

## Stanford için notu (kismen)
Fırça dokusu ve eskiz görünümü alınmaz. Stanford'un kuralı (§4) bodrumu yalnız siyah-beyaz gözetim monitöründe gösteriyor; monitörde fırça darbesi kaydın "belge" duygusunu bozar ve cevabın bir kayıt olduğu fikrini zayıflatır. Motor da zaten yazılmış (`stanford/lib/ekran.js`).

Alınacak olan ışık ve kompozisyon grameri; dördü de mevcut motorla, yeni kod yazmadan yapılır:

1. **Koridor monitörü, ters ışık:** figür karenin en parlak lekesinin önünde durur. Koridorun ucundaki kapı ya da lamba monitörde patlamış beyaz olur; gardiyan silueti onun önünde. Yüz yok kuralı böylece eksik değil, tercih gibi görünür.
2. **Koridor ve sayım planları, değerle derinlik:** öndeki gardiyan tam siyah, sıradaki mahkûmlar orta gri, en arkadaki açık gri. TON plakasında üç basamak yeter. Numaralar yalnız öndeki figürde okunur.
3. **Bant sahnesi (ters açı, gözlem odası), tek sıcak rengin ışık kaynağı olması:** teybin kehribarı yalnız lamba noktası olarak değil, masaya ve iki sandalyedeki siluetlerin kenarına vuran ışık olarak kullanılır. Örnekteki turuncunun payı ölçü olabilir: renkli planlarda karenin yaklaşık onda biri, öteki planlarda sıfır. Kırmızı kayıt lambası küçük ve tek kalır.
4. **Geniş planlar, alçak ufuk ve yönlendirici çizgi:** koridorun zemin çizgileri ve duvar-zemin birleşimi figüre akar. Kamera sabit gözlem yerinde kalır, bu yüzden Kural 1 ile çelişmez.

**Belge planlarına bir şey alınmaz:** daktilo ve sıcak kâğıt kendi dilinde kalır.

**Dikkat:** örneğin içeriği (tren, duman, paltolu sıra hâlinde figürler) Stanford'a taşınmaz.
