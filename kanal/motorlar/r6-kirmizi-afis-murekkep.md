# kirmizi-afis-murekkep (r6)

Kullanıcının 25 Kasım 2026'da gönderdiği üslup örneği: kırmızı zemin + mürekkep yıkaması afiş; gözlüklü yaşlı adam, yürüyen adam.
- Örneğin kendisi depoda yok (telif; yalnız başvuru).
- Çözümleme ve yön metni Fable'ın; yön metni ayrı bir ajanla sınandı (telif, kanal kuralları, mevcut motorlarla çakışma).

## Karar: mevcut bir motora ek
Ayrı motor gerekmez; görselin kodla alınabilen her parçası iki mevcut motorda var.

- **Ran (`ran/lib/ink.bundle.js`, mürekkep):** kuru fırça kenarlı leke, basamaklı yıkama, kâğıt greni. Cinecode'daki `ink-wash.md` tarifi de "beş ton mürekkep + tek kırmızı" diyor; fark şu ki orada kırmızı küçük bir mühür, burada karenin %15'i düz zemin.
- **İkaros (`ikaros/lib/silk.js`, serigrafi afiş):** düz, sert kenarlı mürekkep alanı ve afiş kompozisyonu. Kırmızı zemin buradan gelir.
- **Çernobil (`cernobil/lib/baski.js`):** "tek renk + siyah" kuralı zaten kurulu; plaka mimarisi kırmızı alanı ayrı plakada tutmaya uygun.

Ek olarak yazılacak şey küçük: Ran'ın mürekkep katmanının arkasına düz bir renk plakası (kırmızı zemin, figüre değmeyen maske) ve yırtık kâğıt şeridi çizen bir yardımcı. Motor yazmak en pahalı aşama; burada yeni bir gölgelendirici ya da figür sistemi gerekmiyor.

Görseli asıl güzel yapan eller ve yüz hiçbir motorla gelmez. Yeni motor yazmak bu açığı kapatmaz, yalnız paleti yeniden üretir. Bu yüzden değer en çok kapakta ve tek tek "afiş plan"larında (bölüm açılışı, ölçek montajı) çıkar, bütün bir filmin dili olarak değil.

## Çözümleme
**Kaynak:** tek durağan görsel, 736×977 dikey. Hareket ölçümü yok; aşağıdaki hareket maddesi öneridir, gözlem değil. Görseldeki bozuk yazı ("robf") ve ellerin anatomisi yapay zekâ üretimi olabileceğini düşündürüyor; kökeni doğrulanmadı.

**Palet (olcum.json, k-means):**
- Mürekkep siyahı `#292625` %25,5
- Kâğıt krem `#DDD2B2` %25,4
- Üç gri basamak: `#4B463F` %14,2, `#756E61` %10,2, `#A49C89` %8,7 (toplam %33)
- Kırmızı `#D43822` + `#E44128` %15,2; geçiş tonu `#9F3E2D` %0,7
- Özet: iki mürekkep (siyah, kırmızı) + kâğıt. Siyah mürekkep dört basamakta, kırmızı tek düz ton.

**Onu güzel yapan şey (sırayla):**
1. **Kırmızı yalnız zemin.** Üst üçte birde düz bir alan; hiçbir figüre, nesneye değmiyor. Kırmızının parlaklığı siyahla kremin ortasında, bu yüzden hem koyu figürü hem açık gözlüğü taşıyor.
2. **Ölçek montajı.** Karenin üst yarısını dolduran dev baş, altında onun onda biri boyunda yürüyen adam. İkisi aynı mekânda değil; yırtık kâğıt şeritleri iki ölçeği birbirine bağlıyor. Hikâyeyi tek karede anlatan bu: biri bakmıyor, öteki yürüyor.
3. **Göz yok.** Gözlük camları boş kâğıt rengi iki disk; karenin en parlak noktası orası. Yüzün alt yarısı ellerle kapalı. Yüz neredeyse hiç çizilmemiş, ifade ellerden okunuyor.
4. **Sert kenarlı kütle + kuru fırça saçak.** Gölge yumuşak değil; koyu leke doğrudan kâğıda oturuyor, kenarı kuru fırça ve sıçramayla dağılıyor. Gri basamaklar yıkama gibi ama kenarları basamaklı.

**Çizgi:** ince kontur az; biçimi çizgi değil leke kuruyor. Var olan çizgi 1–3 px, siyah, kuru fırça ucu (kopuk, incelip kalınlaşan). Yıkıntıda ince tel ve direk çizgileri tek kalınlıkta.

**Doku:** kâğıtta ince gren, kırmızıda hafif baskı lekesi (alan tam düz değil, ±birkaç ton). Mürekkepte tuz/su lekesi benzeri benek.

**Figür kuruluşu:** öndeki adam yaklaşık 7 baş boyunda, gerçekçi oran; şapka gölgesi yüzü kapatıyor, yüz iki üç lekeden ibaret. Dev başta kırışık, sakal ve eller ayrıntılı: görselin en emek isteyen yeri.

**Kompozisyon:** dikey afiş, üç bant: kırmızı + baş (üst), yırtık kâğıt geçişi (orta), krem zemin + figür + ufukta koyu yıkıntı şeridi (alt). Odak gözlük, ikinci odak öndeki adam; ikisi aynı dikey eksende.

**Hareket (öneri):** bu bir afiş, canlandırma dili yok. Kodda karşılığı: katman kayması (baş, kâğıt şeritleri, figür, yıkıntı ayrı derinlikte), lekenin kâğıda yayılarak belirmesi, öndeki figürde 12 kare/sn yürüyüş (`araclar/hareket/`). Ara kare ve sürtünme bu üsluba uymaz.

**Kodla yapılabilirlik:**
- Kolay: düz kırmızı alan, krem kâğıt, gren, yırtık kâğıt şeritleri, ufukta yıkıntı silueti, gözlük diskleri, ölçek montajı.
- Orta: kuru fırça saçaklı leke kenarı ve basamaklı yıkama (Ran'ın mürekkep motoru bunu yapıyor).
- Yapılamaz: görseli taşıyan eller ve kırışıklı yüz. Kodla çizilirse kanalın bilinen zayıf noktasına düşer; el yerine siluet kütle, yüz yerine gözlük parıltısı konmalı. O zaman görselin en güçlü yanı gider, geriye palet ve montaj fikri kalır.

**Not:** bu adım yalnız dosyadaki görseli çözümledi. Kullanıcının tarayıcı paneli sorusu bu adımın kapsamı dışında; ana oturumun cevaplaması gerekir.

## Hukuk
**Telif ve imza:**
- Görselin kökeni bilinmiyor; yapay zekâ üretimi olabilir (bozuk yazı, el anatomisi). Yine de belirli bir çizerin mürekkep-afiş diline yakın duruyor olabilir; bu doğrulanmadı. Güvenli yol: görselin kendisi, kompozisyonu (dev baş + şapkalı adam + yıkıntı) ve figürleri kopyalanmaz, depoya girmez.
- Alınan şeyler korunmayan genel teknikler: iki mürekkepli baskı paleti, düz renk zemin, ölçek montajı, boş disk gözlük. Hex değerleri birebir alınmak zorunda değil; kırmızıyı kanalın kendi vurgu tonuna çekmek benzerliği de azaltır.

**Hassasiyet taraması (kanal listesiyle, görselin kendisinde):**
- Sağdaki çapraz kollu direk ve soldaki sivri kule: haç / darağacı / minare okumasına açık. Benzer bir ufuk çizilirse direk ve kule biçimleri tam boy karede bakılır.
- Kırmızı + siyah + krem ve yıkıntı birlikte savaş/propaganda afişi okunur. Stanford gibi yaşayan kişilerin olduğu bir konuda bu çağrışım kapakta da tartılmalı.
- Kırmızı düz alan kalmalı; damla, sıçrama ya da figüre değen kırmızı kan okunur.
- Kırmızı zemin üstünde açık renkli iki disk: yan yana durduklarında sorun yok, ama tek disk + kırmızı zemin bayrak/hedef okumasına yaklaşır.

**Stanford'a özel:** dev baş gerçek bir kişiye (Zimbardo, Jaffe) benzetilmez; sakal, saç, gözlük çerçevesi gibi tanıtıcı ayrıntı verilmez. Siluet ve levha yeter.

## Stanford için notu (kismen)
Filmin üslubu seçilmiş ve motoru yazılmış (`stanford/lib/ekran.js`); değiştirilmez. Üç şey alınabilir, biri alınmaz.

**Alınır:**
1. **Gözlük camı karenin en parlak noktası (bodrum monitörü, gardiyan yakın planı).** Plan zaten "gardiyanda tek yüz öğesi aynalı gözlüğün parıltısı" diyor. Örnekten gelen ölçü: iki cam boş kâğıt/fosfor beyazı düz disk, içinde göz ya da yansıma ayrıntısı yok, çevresi karenin en koyu kütlesi. Monitörde ışıma camdan taşabilir.
2. **Ölçek montajı (III. bölüm, bant sahnesi ya da bölüm açılışı).** Büyük gözlemci silueti üstte, altında küçük gardiyan figürü: "gözlemci yalnız gözlemci miydi?" sorusunun tek karelik hâli. Kâğıt modunda (`mod: 'kagit'`) kurulur; üstteki kütle siluet kalır, yüz ve el çizilmez. Kural 2'yi bozmaması için III. bölümden önce kullanılmaz.
3. **Kapak adayı.** Koyu siluet + iki parlak cam + tek vurgu rengi, kanalın kapak kuralına (tek odak, en parlak nokta) doğrudan uyuyor. Kırmızı düz zemin yalnız kapakta denenebilir; küçük boyda (120×68) iki camın okunup okunmadığı test edilir.

**Alınmaz:**
- **Filmin içinde kırmızı zemin.** Kural 3 rengi yalnız teybin kehribar ışığına ve kırmızı kayıt lambasına veriyor. Kırmızı alan girerse kayıt lambası tek renk olmaktan çıkar ve filmin fikri zayıflar.
- **Elleriyle yüzünü kapatan figür.** Kodla el zor; ayrıca yaşayan kişilere (gardiyan, araştırmacı) pişmanlık jesti yakıştırmak iç dünya uydurmaktır.
- **Yıkıntı, mürekkep sıçraması.** Bodrumla ilgisi yok; koridor monitörü ve belge planlarına uymaz.
