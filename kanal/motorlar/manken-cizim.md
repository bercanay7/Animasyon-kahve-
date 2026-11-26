# manken-cizim: 3B manken + çizim gölgelendiricisi (aday ortak araç)

Kullanıcının sorusundan doğdu (25 Kasım 2026): "Bu kadar ayrıntılı çizimler kodla yapılabilir mi?"
- Yüz, el ve beden kodla çizimin zayıf yanı. Bu yolda anatomiyi, perspektifi ve gölgeyi basit bir 3B manken veriyor, elle çizilmiş görünümü gölgelendirici veriyor.
- Başvurular r8 (gri kuru fırça storyboard) ve r1 (ışık kamaları). Çözümlemeleri bu klasörde.
- Yön metni Fable'ın. Ayrı bir ajan sınadı (yollar, lisans, SwiftShader, kanal kuralları); bulguların hepsi işlendi.
  - Sınamanın en önemli iki bulgusu:
    - deneme sahnesi tek lamba altında sorgu masasına kaymasın (tek figür, çalışma masası);
    - Mixamo ve Sketchfab'ın CC-BY ya da "Standard" lisanslı modelleri yok; lisans temiz değilse kodla kurulan manken.

**Kullanım:** yeni bir sohbete aşağıdaki metni yapıştır ve r8 ile r1 görsellerini elle ekle. Yeni oturum görselleri kendiliğinden göremez; görseller depoda yok.

## Yön metni

> Yeni bir ortak araç: 3B manken + çizim gölgelendiricisi. Baştan sona kur; kararlar senin. Önce CLAUDE.md'yi oku. `stanford/lib/ekran.js` ve `kanal/motorlar/` henüz `main`'de yok: önce `origin/claude/confident-einstein-jrw1sy` dalını al. İki başvuru görseli (r8 ve r1) bu mesaja ekli değilse başlama, iste.
>
> Ekteki iki görsel başvurudur; videoya ve depoya girmez. Gri olan (r8) kaba kuru fırça bir storyboard: tepeden ışık alan masa, koridordan gelen siluetler, parlayan gözlük camları. Renkli olan (r1) sert kenarlı ışık kamaları, düz dolgu, düzlemlere bölünmüş yüzler. Kareleri yeniden kurma: üniformayı, miğferi, viski bardağını, tablodaki adamı, panel düzenini, çizerlerin el yazısını alma. Aldığımız şey yalnız şu kural.
>
> Biçimi ışık kurar, çizgi değil. Ton iki ya da üç sert basamaktır; aradaki geçişi yumuşatma değil, fırçanın sürtmesi verir. Karanlık kütleler birbirine karışır, kenar yalnız ışığın değdiği yerde belirir. Işık bir kama ya da konidir, sınırı keskindir.
>
> Kodun zayıf yanı yüz, el ve beden. Bu yüzden anatomiyi elle çizme: basit bir 3B insan modelini WebGL2'de iskeletle pozla (ters kinematik), perspektifi ve gölgeyi model versin. `araclar/hareket/` 2B bir çözücüdür (px uzayı); ondan yürüyüş zamanlamasını ve ayak basma mantığını al, 3B'ye uyarla, ayağın kaymadığını oradaki `test.js` ölçütüyle sına. Görünümü gölgelendirici versin: kuru fırça sürtmesi, düşey sürtme izleri, sert gölge basamakları, kontur, gren. Yüzü ayrıntıyla değil düzlemle çöz; göz çukuru gölgede kalsın. Fırça dokusu kareden kareye kaynamasın, ekrana da yapışmasın; tohumlu olsun, iki karede bir değişsin.
>
> Hazır olana önce bak: plaka mimarisi `cernobil/lib/baski.js` ve `stanford/lib/ekran.js`'te (ikisi de Canvas 2D plaka + tek tam ekran gölgelendirici; 3B geçiş içermezler, 3B katmanın plakalara nasıl gireceği senin kararın). Tarifler `.claude/skills/cinecode/styles/` altında; ondan önce `.claude/skills/cinecode/BIZIM_NOT.md`. Sonra `araclar/lemo/KATALOG.md`.
>
> Lisans kapısı ilk iş: model ve her doku CC0 olacak; `lisans-kontrol` becerisi, `araclar/ASSETS.md` kaydı. Mixamo yok (Adobe şartları); Sketchfab'ın CC-BY ya da "Standard" lisanslı modelleri yok. Bakılabilecek adaylar Quaternius ve MakeHuman çıktısı; ikisini de ham lisans metninden doğrula. Temiz model bulamazsan durma: mankeni kodla kur (kapsül uzuvlar, düzlemli baş); lisans sorunu yoktur ve bu üsluba yetebilir. Lisansı belirsiz modelle ilerleme. Kullandığın her kütüphane de (three.js vb.) `ASSETS.md`'ye girer: sürüm sabit, render CDN'den değil depodaki kopyadan, lisans metni dosyanın yanında.
>
> Önce ölç: render SwiftShader'da, kare kare, dört işçiyle, yerel http sunucusu üzerinden (`dorian-gray/tools/sunucu.js`). SwiftShader'da gölge haritası, kontur için ek tampon ve çok geçişli son işlem pahalıdır. Başlangıç sınırı: tek ışık, tek gölge haritası, son işlem en çok bir iki geçiş, sürtme düşük çözünürlükte yapılıp büyütülsün. Bütçe: kare başına tek işçide en çok ~1 sn (Çernobil gölgelendiricisi ~0,5 sn; `cernobil/geriye_bakis.md`); aşarsa 15 kare/sn dene. Tek karede çizim süresini üslup kapısından önce al; bütçeye sığmıyorsa sadeleştir ya da bırak.
>
> Üslup kapısı tek kare değil: bir manzara, bir orta plan figür, bir yakın plan ve 15 saniye hareket (yürüyen ve çalışma masasına eğilen tek figür). Deneme sahnesinde figür tektir: karşısında oturan ikinci kişi, ayakta bekleyen nöbetçi, sıra hâlinde yürüyen kol yok. Her birini r8 ile yan yana koy ve tam boy bak.
>
> Başarısızlık sayılanlar: görüntü 3B oyun ya da ön izleme render'ı gibi okunuyorsa; yüz vitrin mankeni gibi duruyorsa; hareket fazla pürüzsüz ve ağırlıksızsa; doku figürün üstünde yüzüyorsa; figür koyu siluet olarak okunmuyorsa. Böyleyse motoru bırak, nedenini yaz.
>
> Kanal kuralları geçerli: bembeyaz göz + yuvarlak baş + çıkık ağız yok (gözlük parlaması küçük ve sıcak tonda kalsın), donuk plan yok, y > 880 boş (`lale-cilginligi/tools/alt_bant.js` ile ölç), yaşayan kişiye, film ya da çizgi roman karakterine benzeyen yüz yok. Hassasiyet taramasını ilk karede yap: sıra hâlinde üniformalı siluetler, tek lamba altında sorgu masası. Poz kütüphanesindeki her pozu da tam boy karede tara: havaya kalkmış düz kol, alna giden el, sıra hâlinde eğilen figürler.
>
> Yeri: `araclar/` altında ortak araç; projeler çağırır, hiçbir projeye gömülmez. Arayüz `lale-cilginligi/lib/film.js` çekim sistemiyle (`S('B04')`, `Wd(...)`) ve `render.js` işçileriyle uyumlu olsun; aynı kare her işçide aynı çıksın. Kendi dalında çalış, her iş parçasından sonra Türkçe commit ve push. Navitas dosyalarına dokunma. Kredi harcayan üretim yok.
>
> Gerisi senin kararın.
>
> Fable
