# gri-kalem-kahve (r3)

Kullanıcının 25 Kasım 2026'da gönderdiği üslup örneği: kahvede gazete okuyan yaşlı adam; gri kalem eskiz.
- Örneğin kendisi depoda yok (telif; yalnız başvuru).
- Çözümleme ve yön metni Fable'ın; yön metni ayrı bir ajanla sınandı (telif, kanal kuralları, mevcut motorlarla çakışma).

## Karar: ayrı motor
Ayrı motora değer, ama örneğin en çekici yanı (karikatür yüz ve eller) için değil. Motorun kuralı "derinlik = bitmişlik" olur: aynı nesne katmanına göre arama çizgisi, tonlu çizim ya da koyu leke olarak çizilir. Bu kural mevcut motorların hiçbirinde yok.

Çakışmalar:
- Gravür (`milton/lib`): çizgi var ama ton taramayla kurulur, düzlemler eşit bitmiş. Değişken kalınlıklı kontur mantığı oradan alınabilir.
- Mürekkep (`ran`): leke ve yıkama var, ama fırça ve kâğıt emişi üzerine kurulu; arka plan yarım eskiz değil.
- Gazete baskısı (`cernobil/lib/baski.js`): tram ve tek renk. Buradan yalnız gazete içi doku alınır.
- Sessiz film (`mary-stuart`): gri ölçek ortak, ama fotoğrafik gren ve titreme; çizgi yok.
- cinecode `urban-sketch`: en yakın tarif (arama çizgisi, taşan köşe), ama sepya çizgi + renkli suluboya; burada renk yok, ton var. `line-boil`: hareket için başvuru (çizgi titremesi, ikişer kare).

Kanalda boş duran yer: iç mekân ve gündelik sahne (kahve, oda, masa, bekleme). Kullanıcının bekleyen önerisi olan psikolojik anlatım (Zweig, Dostoyevski: tek karar anı, iç dünya) tam bu mekânları ister ve mevcut motorlar orada ya fazla süslü ya fazla tarihsel.

Uyarı: motor yazmak en pahalı aşama. Üslup kapısında figür yüzsüz hâliyle "kâğıt kesme" ya da karikatür okunursa durulur ve kural `urban-sketch` tarifine ek olarak küçültülür.

## Yön metni (yeni bir oturuma verilir)

> Yeni çizim motoru: eskiz defteri. Önce üslup kapısı; kapı geçmeden film kurulmaz.
>
> Elinde bir başvuru karesi var: loş bir kahvede gazete okuyan yaşlı adam, gri kalem eskizi. Onu yeniden çizme. O adamı, o yüzü, o kahveyi, o çizerin abartılı burunlarını ve el yazısını taklit etme; kare depoya girmez, üstünden geçilmez. Karikatür yüzün peşine de düşme: o yüz elle verilmiş bir asimetri, kodla yapılınca ya boş kalıyor ya alay gibi okunuyor.
>
> Peşinden gideceğin şey karenin kuralı: derinlik bitmişlikle kurulur. Arkadaki dünya yarım kalmış arama çizgisidir, ortadaki kişi tonlanmış ve konturlanmıştır ve arkasındaki dünyadan koyu bir kütle olarak ayrılır (kanalın koyu siluet kuralı burada da geçer), öndeki nesne yalnız koyu bir lekedir. Karenin en açık yeri bakılacak tek nesnedir. Renk yok; griler hafif sıcak, saf beyaz ve saf siyah yok. Kural bir fikre de bağlanabilir: bir şey ancak biri ona dikkat ettiğinde bitmiş çizilir.
>
> Yüzü çizmeden insanı anlat: sırt, profil, eğik baş, gazetenin ya da elin arkasında kalan yüz, masadaki bardak. Duruş ve nesne ifadeyi taşısın. Elleri kapalı şekil olarak tut.
>
> Hareketi çizimin kendisinden çıkar: çizginin soluk alması, bir düzlemin gözümüzün önünde bitmesi ya da eskize geri dönmesi, ışığın kayması. Donuk plan yok; figür kıpırdamasa da her plan ilk saniyeden kımıldar. Beden hareketi az ve yavaş.
>
> Kapı: bir iç mekân manzarası, orta plan oturan figür, yakın plan (el ve nesne), 15 saniye hareket. Dördünde de karikatür ve kâğıt kesme okumasına, tam boy karede hassasiyet listesine bak.
>
> Önce gravür, mürekkep ve gazete baskısı motorlarının geriye bakışlarını oku; çizgi ve tram oralarda hazır olabilir. Sonra cinecode'da line-boil (çizginin soluması) ve urban-sketch (çizim sırasının oynatılması) tariflerine bak, önce BIZIM_NOT.md. Motor Canvas 2D / WebGL2, tohumlu, SwiftShader'da ölçülerek yazılır.
>
> Yarayacağı yer: iç dünyası olan, odada geçen hikâyeler; Zweig, Dostoyevski, tek karar anı.
>
> Gerisi senin kararın.
>
> Fable

## Sınamanın bulduğu ve yön metnine işlenenler
- (2) Kanal kuralı: CLAUDE.md'ye göre ana figür koyu siluettir. Metin ortadaki kişiyi yalnız 'tonlanmış ve konturlanmış' diye tarif ediyor. Başvuru karesinde adam orta-koyu bir kütle (#504B50/#666468, kontur #1A171A) ve açık arka plandan koyu duruyor. Bu söylenmezse orta grilerde açık, iç çizgili bir figür çıkabilir. Bu da 'kâğıt kesme' ya da soluk okunur. Bir yan cümleyle eklendi.
- (2) Donuk plan kuralı: metin hareketi çizginin soluk alması, düzlemin bitmesi ve ışıkla kuruyor ama 'beden hareketi az ve yavaş' deyip bırakıyor. Kanal kuralı her planın ilk saniyeden hareket etmesini istiyor. Bu açıkça yazılmazsa sabit oturan figürlü durgun planlara izin verilmiş gibi okunabilir. Bir cümle eklendi.
- (3) Yeniden icat riski: CLAUDE.md adım 7 sırasına göre kendi motorlardan sonra cinecode tarifleri gelir (önce .claude/skills/cinecode/BIZIM_NOT.md). Orada bu üslubun iki parçası hazır duruyor. line-boil.md tohumlu, karelerle dönen çizgi titremesini anlatıyor ('çizginin soluk alması'). urban-sketch.md çizgilerin çizim zamanını piksel başına önceden yazıp çizim sırasını oynatmayı anlatıyor ('düzlemin gözümüzün önünde bitmesi'). Metin yalnız gravür, mürekkep ve gazete baskısına yönlendiriyordu, bu iki tarif eklendi.
- (1) Telif: sorun yok. Metin kareyi, yüzü, çizerin abartılı burunlarını ve el yazısını açıkça yasaklıyor ve karenin depoya girmeyeceğini söylüyor. Telifli karakter yok. Gazetedeki el yazısı başlık da taklit edilmiyor.
- (4) Kodla yapılabilirlik: sorun yok. Karikatür yüz bilerek dışarıda bırakılmış, eller kapalı şekil, beden hareketi az. Basınçlı kontur, arama çizgisi, düzlemin bitip eskize dönmesi ve ışığın kayması Canvas 2D / WebGL2 ile tohumlu yapılabilir.
- (5) Yön ve talimat dengesi doğru: kural, fikir, kapı ve okunacak yerler veriliyor, adım adım kod istenmiyor. Not: imza 'Fable'. Kullanıcı Fable ağzından bir prompt istediği için bırakıldı. Ama metni Fable değil ana oturum yazdı; kullanıcıya bu söylenmeli.

## Çözümleme
## r3: kahvede gazete okuyan yaşlı adam (tek kare, 750×593)

**Güzel yapan şey tek cümleyle:** derinlik renkle ya da bulanıklıkla değil, *bitmişlik derecesiyle* kurulmuş. Arka plan yarım bırakılmış eskiz, orta plan tonlanmış çizim, ön plan koyu leke. Göz kendiliğinden tek bitmiş şeye, adama ve gazetesine gider.

### Palet (olcum.json, 8 küme)
| Hex | Pay | Görev |
|---|---|---|
| #9B999C | %18,3 | arka duvar, orta gri zemin |
| #332F33 | %15,7 | ön plan koltuk arkası, masa |
| #B2ADAE | %14,9 | arka planın açık yüzeyleri |
| #504B50 | %11,6 | gömlek gölgesi |
| #666468 | %10,7 | ten ve gömlek orta tonu |
| #868589 | %10,3 | arka figürlerin çizgisi ve soluk tonu |
| #D0C8C9 | %9,3 | gazete kâğıdı, tabelalar (en açık) |
| #1A171A | %9,1 | kontur, kaş, en koyu gölge |

- Tek renkli, ama nötr gri değil: bütün kümelerde R ≥ B > G, yani hafif mor-sıcak gri. Doygunluk %3–5.
- Saf beyaz ve saf siyah yok: aralık #1A171A–#D0C8C9. En açık değer gazete; karenin en parlak yeri odakla aynı yer.
- Kaba dağılım: koyu (≤#50) ~%36, orta ~%39, açık ~%24. Düşük anahtar, loş iç mekân.

### Çizgi
- Üç ayrı çizgi sınıfı var ve sınıf derinliğe bağlı:
  - arka plan: 1–1,5 px, orta gri (#868589), kesik kesik, üst üste binen, köşede taşan arama çizgisi; dolgusu yok ya da tek soluk ton;
  - ana figür: 2–4 px, neredeyse siyah, kalınlığı değişen (basınçlı) kontur; gölge tarafında kalınlaşır, ışık tarafında kırılır;
  - ön plan (koltuk arkası): kontur yok, yalnız koyu leke.
- Uçlar sivri ve açık; şekiller tam kapanmıyor. İç çizgi az: gömlekte birkaç kırışık, yüzde kırışıklar.

### Dolgu ve gölge
- Figürde 3 ton (ışık / orta / gölge) + kontur. Kenarlar çoğunlukla sert (hücre gölgesi), yalnız yanak ve alında yumuşak geçiş.
- Arka planda 1–2 ton, kenarları dağınık; duvar düz, hafif alacalı bir yıkama.
- Gazetedeki fotoğraflarda nokta tramı ve karalama yazı: kâğıt içinde ikinci bir doku.

### Işık
- Sol üstten yumuşak tek kaynak (pencere hissi). Gölge tarafı sağ ve alt. Köşelerde hafif kararma; sol alt köşe en koyu, çerçeve görevi görüyor.

### Doku ve gren
- İnce, eşit dağılmış gren; kâğıt lifi yok. Fırça ucunun hafif pütürlü kenarı çizgide okunuyor. Dijital eskiz, kurşun kalem taklidi.

### Figür kuruluşu
- Baş bedene göre büyük (~1:4,5 oturur hâlde), burun ve kulak abartılı, omuz dar: karikatür oranı.
- Yüz tam çizilmiş: sarkık göz kapağı, kaş, bıyık, kırışık. Karenin çekiciliğinin yarısı bu ifade.
- Eller ayrıntılı (boğumlar, saat). Arka figürlerde yüz iki üç çizgiyle geçilmiş, biri sırtı dönük.

### Kompozisyon
- Üç düzlem: ön (sol alt koyu koltuk arkası, bulanık okunur), orta (adam, gazete, bardak), arka (tezgâh, şişeler, iki müşteri).
- Gazete, bakışı sola taşıyan açık üçgen; adamın bakışı aşağı. Odak karenin sağ üst üçte birinde.
- Bardak ve tabak tek küçük natürmort: sahneye zaman veriyor.

### Hareket
- Tek kare; ölçülecek hareket yok. Kare farkı verisi bu örnek için yok.

### Kodla yapılabilirlik
| Öğe | Durum | Neden |
|---|---|---|
| Sıcak gri palet, 3 ton dolgu, köşe kararması, gren | kolay | tek gölgelendirici geçişi |
| Derinliğe bağlı çizgi sınıfı (bitmişlik katmanı) | kolay–orta | çizim çağrısına katman değeri vermek yeter; arama çizgisi tohumlu gürültüyle üretilir |
| Basınçlı, kırılan kontur | orta | değişken kalınlıklı yol; gravür motorundaki çizgi mantığına yakın |
| Gazete tramı | kolay | Çernobil `baski.js` zaten yapıyor |
| Arka plan mekânı (şişe, tabela, sandalye) | orta | çok nesne ama kaba çizilebilir; kabalık üslubun parçası |
| Karikatür yüz ve ifade | zor / yapılamaz | çekicilik elle verilmiş asimetride; kodla yüz kanalın bilinen zayıf yanı |
| Boğumlu eller | zor | aynı gerekçe |

**Sonuç:** kareden alınabilen şey yüz değil, sahne kuruluşu: bitmişlikle derinlik, tek açık nesne, ön plan lekesi.

## Hukuk
**Risk: orta (kopyalanırsa yüksek, yalnız kural alınırsa düşük).**

- **Kaynak belirsiz.** Kare WhatsApp'tan gelmiş, çizeri ve lisansı bilinmiyor; büyük olasılıkla yaşayan bir illüstratörün telifli işi (İspanyolca gazete başlığı, çağdaş dijital eskiz). CC0 ya da kamu malı sayılamaz: videoya, kapağa, depoya girmez; üstünden çizilmez, görsel üretim aracına başvuru olarak verilmez.
- **Üslup korunmaz, ifade korunur.** Gri eskiz, üç düzlem, tek açık nesne serbest. Korunan ve alınmayacak olanlar: bu adamın karakter tasarımı (burun, bıyık, kulak, kaş birleşimi), bu kompozisyon (gazete + bardak + sol alt koltuk + arkada iki müşteri aynı yerleşimle), çizerin imza sayılabilecek abartı dili ve harf karakteri.
- **Marka.** Arka plandaki tabelada gerçek bir bira markası okunuyor. Kendi sahnemizde gerçek marka, gerçek gazete adı, okunur logo olmaz; tabela ve başlık uydurma ya da karalama.
- **Karikatür okuması (kanal kuralı).** Abartılı burun ve çıkık yüz hatları bir halkı ya da yaşlıları alaya alan klişeye kayabilir; kanalın karikatür yasağı (koyu siluet + beyaz göz + çıkık ağız) aynı aileden. Motor yüzsüz kurulmalı.
- **Gerçek kişi.** Bu üslupla yaşayan ya da yakın dönem kişisi çizilirse karikatür oranı kişilik hakkı ve hakaret riski doğurur; Stanford'da ve Atatürk içeren hiçbir işte kullanılmaz (5816).
- **İç mekân taraması.** Kahve ve meyhane sahnelerinde şişe rafı alkol özendirmesi gibi okunmasın; tam boy karede hassasiyet listesiyle birlikte bakılır.
- **Künye.** Videoya hiçbir şey girmediği için künye gerekmez. Çizer bulunursa adı yalnız iç notta başvuru olarak yazılır.

## Stanford için notu (kismen)
Üslup olarak alınmaz: Stanford'un kuralı (bodrum yalnız monitörde, renk yalnız kayıtta, yüz yok) kurulmuş ve `stanford/lib/ekran.js` yazılmış. Karikatür yüz ise yaşayan kişiler (Eshelman, Mark, Jaffe, Maslach) yüzünden zaten yasak. Üretim ortasında motor değiştirilmez.

Üç kuruluş fikri `mod: 'kagit'` planlarına taşınabilir, motor değişmeden:

1. **Gözlem odası (III. bölümdeki ters açı): bitmişlikle derinlik.** Masa, makaralı teyp ve monitör tam tonlu ve konturlu; arkadaki duvar, dolap ve kapı levhası yalnız soluk, ince, kesik çizgi. Seyircinin gözü teybe gider. Kural 2'yi de güçlendirir: gözlemciler "yarım çizilmiş" kalır, kayıt cihazı bitmiştir.
2. **Ön plan lekesi.** Örnekteki sol alt koltuk arkası gibi: gözlem odasında kadrajın alt köşesinde konturu olmayan koyu bir sandalye arkası ya da gözlemcinin omzu. Yüz göstermeden "burada biri oturuyor ve izliyor" der; yönün sorusunu (gözlemci yalnız gözlemci miydi?) tek lekeyle sorar.
3. **En açık değer = belge.** Belge ve bant dökümü planlarında kâğıt karenin tek açık yüzeyi olsun, çevresi orta-koyu sıcak gri (#332F33–#9B999C aralığı); ikinci bir açık leke bırakılmasın. İlan (gazete kupürü) planında fotoğraf yerine nokta tramı ve karalama satırlar, Çernobil `baski.js` ile.

Alınmayacak yerler:
- **Bant sahnesi ve koridor monitörü:** monitörün dili tarama çizgisi ve bulanıklık; kalem çizgisi oraya girerse Kural 1 bozulur.
- **Palet:** örneğin mor-sıcak grisi monitörün soğuk siyah-beyazıyla karışmasın; yalnız kâğıt modunda, kehribar ve kırmızı lambanın tek renk kalmasını bozmayacak doygunlukta (≤ %5).

Bunlar öneri; plan listesini başkan değiştirir, düzeltilen planlar tam boy karede hassasiyet taramasından yeniden geçer.
