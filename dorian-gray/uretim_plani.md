# Oscar Wilde, *Dorian Gray'in Portresi*: üretim planı

Başlangıç: 19 Kasım 2026. Seri: Kitapların Sorduğu Sorular. Yayın hedefi: 30 Kasım 2026 (en geç 29 Kasım'da yüklemeye hazır).

**Çalışma düzeni (kullanıcının kararı, 19 Kasım):** bağımsız kurul, puanlama ve çok ajanlı akış yok. Başkan işi tek başına yapar ve denetler; CLAUDE.md ölçütleri ve kanal kuralları aynen geçerli. Fable'a yalnız takılınan yerde tek soru, tek cevap (her danışma aşağıdaki "Fable danışmaları" bölümüne konu ve gerekçesiyle yazılır). Render ve kapaklardan sonra, yayından önce Fable bütün işi bir kez yorumlar; bulgular `geriye_bakis.md`'ye.

## 0. Hazırlık (19 Kasım)
- `claude/kod-uslubu-onerileri-yap056` (Narkissos) zaten `main`'deydi; `claude/beautiful-allen-ci4fzv` (konu taraması) `main`'e birleştirildi ve gönderildi.
- Özgün metinler (`kaynak/`):
  - `wilde_1891_pg174.txt`: Project Gutenberg #174, 1891 kitap sürümü (Önsöz + 20 bölüm). gutenberg.org bakımdaydı, pglaf aynasından alındı. **Satır numaraları bu dosyaya göredir** ("1891: 8403").
  - `wilde_1890_lippincott_archive.txt`: 1890 *Lippincott's Monthly Magazine* metni (13 bölüm), archive.org `ThePictureOfDorianGray1890` OCR metni. OCR'da "th" çoğu yerde "di" okunmuş ("die" = "the"); alıntı yapılacaksa yazım 1891 metnine ve sayfa görüntüsüne (aynı öğedeki PDF) bakılarak düzeltilir.
- **Narkissos benzetmesi doğrulandı:** I. bölüm, Lord Henry: "he is a Narcissus" (satır 159); VIII. bölüm, Dorian portrenin dudaklarını "in boyish mockery of Narcissus" öpmüştü (satır 4058). Bu yüzden açı "kendini sevmek" olmayacak (kullanıcının kararı).


## 1. Talep kontrolü (19 Kasım 2026)
`python3 araclar/talep/talep.py …` (YouTube Türkçe otomatik tamamlama + aramadaki ilk 10 videonun izlenme medyanı; medyan gürültülü).

| Sorgu | Öneri | İlk 10 medyan | Öne çıkan öneriler |
|---|---|---|---|
| **dorian gray** | 14 | **204 B** | dorian gray'in portresi, sesli kitap, **kitap yorumu**, tiyatro, **inceleme** |
| dorian gray'in portresi | 14 | 8,7 B | sesli kitap, kitap yorumu, inceleme, **özet** |
| dorian gray kitap yorumu | 2 | 7,1 B | |
| oscar wilde | 14 | 81 B | sesli kitap, "oysa herkes öldürür sevdiğini", dorian gray'in portresi, mutlu prens |
| güzellik / güzellik lanet mi | 14 / 1 | 130 B / — | güzellik subliminali, tüyolar, dua: konu dışı. "güzellik lanet mi" aranan bir söz değil |
| yaşlanmamak | 5 | 4 B | "yaşlanmamak mümkün mü", "için ne yapmalı" |
| kimse görmese | 6 | 0,7 B | "kimse görmese de Allah görür", "kimse görmese de işini iyi yap" (gündelik söz, arama değil) |
| vicdan | 14 | konu dışı | "vicdansız" dizisi |
| *kontrol:* sisifos / dönüşüm kafka | 14 / 14 | 67 B / 38 B | |

**Okuma:**
- (a) **Tanıdık kapı güçlü ve konunun kendisi:** "dorian gray" Sisifos'un ~3, Kafka'nın ~5 katı. Öneriler kitap okuru aramaları (kitap yorumu, inceleme, özet): kanalın "Kitapların Sorduğu Sorular" serisine doğru kitle. Kapı kelimesi başlıkta öne alınır (Mary Stuart dersi: akış ~45–50 karakterde keser).
- **"Güzellik", "vicdan", "kimse görmese" kapı değil:** aramaları konu dışına gidiyor. Bunlar başlığın **soru** kısmına girer (b şartı), kapı kısmına değil.
- (b) Kişisel soru doğal: "kimse görmese ne yapardın?" gündelik dilde zaten dolaşan bir söz ("kimse görmese de…"); izleyici kendi hayatından tanır.

## 2. Kullanıcıyla kurulan yorum (19 Kasım) ve kaynakla sınanması
Kullanıcının cevapları: çeviri İş Bankası Kültür Yayınları (Hasan Âli Yücel Klasikleri; çevirmen bilinmiyor). Suçlu/kurban sorusuna "yeterince hatırlamıyorum". Açı önerisi (gizli benlik + bedeli başkasına ödetmek, ikinci damar Lord Henry) kabul. Dava kısa. Ad sayısı sade (öneri: Dorian, Henry, Basil). Kitabın bıraktığı soru: **"Güzellik bir lanet mi?"**

| Kullanıcının görüşü | Kaynak | Sonuç |
|---|---|---|
| Son sahnede tabloyu açınca kendi güzelliğini değil çökmüş yaşlı bir adam görüyor | 20. bölüm: Dorian örtüyü çekince portrede "sinsilik bakışı" ve "ikiyüzlülüğün kıvrımı" görür (1891: 8443–8447); bıçağı saplar; hizmetçiler içeri girince **duvarda genç ve güzel portreyi, yerde "buruşmuş, kırışmış, yüzü iğrenç" ölü bir adamı** bulur, onu ancak yüzüklerinden tanırlar (8521–8527). Çökmüş yüzü portrede ilk gören Basil'dir (13. bölüm) | **Kısmen doğru, düzeltilerek kullanılır.** Hafıza iki sahneyi birleştirmiş. Asıl son daha güçlü: **yer değiştirme**. Videonun son görüntüsü bu olur |
| Wilde üç karakterde kendini anlattı: Dorian olmak istediği, Henry dışarıdan görünüşü, üçüncüsü (Basil) aslında olduğu kişi | Wilde'ın Ralph Payne'e mektubu (1894): "Basil Hallward is what I think I am: Lord Henry what the world thinks me: Dorian what I would like to be—in other ages, perhaps." (*The Letters of Oscar Wilde*, ed. Hart-Davis, 1962, s. 352; ikincil aktarım Victorian Web, Dawson. **Mektubun tam tarihi birincil kaynaktan doğrulanacak**) | **Doğru, bir düzeltmeyle:** Basil "aslında olduğum" değil "**olduğumu sandığım**" kişi; Dorian'ın sonundaki "başka çağlarda, belki" kuyruğu da önemli. Bu üçlü, sade kadronun (Dorian–Henry–Basil) gerekçesi olur ve videonun sonuna tek cümle olarak girer (bölüm sonu analizi değil, Wilde'ın kendi sözü) |
| Ad sayısı: yalnız Dorian, Henry, Basil | Portredeki **ilk değişiklik** Sibyl Vane'e yapılan zulmün gecesi olur: ağzın çevresinde "zalimlik çizgisi" (7. bölüm, 1891: 3485–3519). Sibyl o gece kendini öldürür (8. bölüm) | **Kısmen kabul.** Henry, Basil, Dorian ana kadro. **Sibyl dördüncü ad olarak kalır**: o olmadan portrenin ilk çizgisinin sebebi yok ve "bedeli başkası öder" fikrinin ilk örneği o. İlk perdede adı ve yüzüyle ekilir (Ran dersi). James Vane, Alan Campbell, Hetty Merton **adsız ya da hiç**: Hetty yalnız "bir köy kızı" olarak son bölümde |
| "Güzellik bir lanet mi?" | **Bu soruyu kitapta Dorian kendisi soruyor ve cevaplıyor:** 20. bölümde aynayı ayağıyla kırar, "Onu mahveden güzelliğiydi, dua edip istediği güzellik ve gençlik… Güzelliği ona yalnızca bir maske olmuştu" (1891: 8402–8406). **Bu paragraf 1890 metninde yok;** Wilde 1891'de eklemiş. Ama hemen ardından (her iki sürümde) suçu sırayla başkalarına verir: "Her şeyi yapan portreydi", Basil'in sözleri dayanılmazdı, cinayet "bir anlık delilik", Alan Campbell'ın intiharı "kendi seçimi" (1891: 8421–8425; 1890: ~5983–5988). 19. bölümde Henry'ye "Beni bir kitapla zehirledin" (8321) | **Omurga bu olur.** Kullanıcının sorusu Dorian'ın kendi mazereti. Kitap onu sınar: güzellik yüzün suçu göstermemesiydi. Toplum güzel yüze inanır (11. bölüm, 4855–4860: kötü söylentileri duyanlar bile "onu görünce" inanamaz). Basil "günah insanın yüzüne yazılır, gizlenemez" der (12. bölüm, 5591–5592) ve Dorian'ın yüzünde yazılmaz. Cevabı izleyiciye bırakılır, ama kanıtı kitap verir |

**1890 ile 1891 arasındaki farklardan bu videoya girenler** (kaynak sayılır, senaryoda kullanılabilir):
- Dilek: 1890'da "Bunun için… her şeyimi verirdim!" (1890: 1036); 1891'de "**ruhumu verirdim**" (1891: 1021). Pazarlığın bedeli 1891'de adını alır.
- "Güzelliği onu mahvetti" ve kırılan ayna paragrafı 1891'de eklendi (yukarıda).
- Önsöz ("Ahlaklı ya da ahlaksız kitap diye bir şey yoktur") 1891 kitabında var, dergide yok. Önsöz 1895'te mahkemede Wilde'a okundu (aşağıda).
- 1891'de eklenen James Vane kolu videoya girmez.
- Ayrıntılı karşılaştırma senaryoda kullanılacak her satır için kaynak denetiminde yapılır.

**Wilde ve 1895 (kısa, sonda):** 3 Nisan 1895'te Queensberry'ye açtığı iftira davasında savunma avukatı Edward Carson romandan pasajları (Basil'in Dorian'a duyguları) ve Önsöz'ü Wilde'a okuyup soruyor; Wilde Önsöz için "Sanata dair görüşüm, evet" ve bir okuma için "Ancak kaba ve cahil biri öyle okur" diye cevap veriyor (Famous Trials, Linder; Old Bailey aktarımları). Kanalın kuralı: tek sahne, saygılı dil, Wilde'ın cinsel yönelimi davanın konusu olarak tek cümleyle ve yargısız söylenir; hassasiyet taraması bu sahnede yapılır. **Doğrulanacak:** hangi sürümün okunduğu (Lippincott's mı, kitap mı) ve alıntıların tam sözü (birincil: Holland, *Irish Peacock and Scarlet Marquess*, 2003, tutanak).

## 3. Açı (19 Kasım; kullanıcıyla)
**Büyük soru:** kimse görmese insan ne yapar? Dorian'a bu imkân verildi: yaptığı her şeyin izi başka bir yüze, kilitli odadaki portreye yazıldı. Bedeli hep başkası ödedi (portre, Sibyl, Basil). **İkinci damar:** her şey Lord Henry'nin bir bahçede söylediği birkaç cümleyle başladı. Ama dileği Dorian kendi ağzıyla diledi. **Kullanıcının sorusu** ("Güzellik bir lanet mi?") hikâyenin sonunda Dorian'ın ağzından gelir ve sınanır.

**Narkissos'tan ayrışma:** konu kendini sevmek değil, **görünmemek ve bedeli başkasına yazmak**. Narkissos benzetmesi (1. bölüm) videoda kullanılmaz; bir önceki videoya köprü gerekirse yalnız bitiş ekranında.

**Bitiş fikri (iksir):** Basil "günah yüze yazılır" der; Dorian'ın yüzüne yazılmadı, ama bir yere yazıldı. Son görüntüde yer değiştirme. Soru izleyiciye: senin portren nerede asılı?

## 4. İskelet (19 Kasım; senaryodan önce)
**Seçim: Harmon çemberi** (önceki videolar: Ran Harmon, Mary Stuart Kahramanın Yolculuğu, Narkissos Kişōtenketsu; art arda değil). Gerekçe: hikâye bir dilekle açılan, kazanılan ödülün bedelinin ödendiği ve dönüş denemesinin başarısız olduğu kapalı bir daire; Harmon'un 5 (ödül) ve 6 (bedel) adımları romanın iki yarısı.

**Kahraman:** Dorian. **Karşıt güç:** Lord Henry'nin sözü (kişi değil fikir). **Tanık:** Basil (portreyi yapan, "günah yüze yazılır" diyen). **Bedel:** Sibyl ve Basil.
**Mekânlar:** stüdyo/bahçe (açılış), tiyatro, kilitli oda (çatı katındaki eski okul odası, 10. bölüm), sokak/Londra sisi. Bölüm başına tek mekân.

| Adım | İçerik | Kaynak (1891 bölüm) | Cümle aralığı* |
|---|---|---|---|
| **0. Kanca** (0–~15 sn) | Kilitli oda, lamba, mor örtü kalkar: altında tablo, izleyiciye dönük yüzü görünmez. Soru ilk cümlede: "Yaptığın her şey yüzüne değil, bir tabloya yazılsaydı… ve o tabloyu kimse görmeseydi?" Kimlik tek cümle kancanın içinde: Oscar Wilde, 1890 | XX, XIII | A |
| **1. Konfor** | Stüdyo, yirmi yaşında Dorian, Basil'in bitirdiği portre. Basil: "Bu tabloya kendimden fazlasını koydum" | I | B |
| **2. İhtiyaç** | Bahçe: Lord Henry'nin sözü (gençlik geçer, güzellik geçer, "yaşamak tek şey"). Dorian portreye bakar ve ilk kez yaşlanacağını anlar | II | B |
| **3. Eşik** | Dilek: "Ben hep genç kalsam, tablo yaşlansa… ruhumu verirdim." Basil tabloyu yok etmek ister, Dorian engeller | II | B |
| **4. Uyum** | Sibyl Vane: küçük tiyatroda Shakespeare oynayan genç kız. Dorian âşık olur; Henry'nin sözleriyle | IV–VII | C |
| **5. Ödül** | Sibyl âşık olunca oyunculuğu kötüleşir; Dorian onu acımasızca bırakır. Eve döner: portrenin ağzında zalimlik çizgisi. **Dileği tuttu.** Ertesi gün Sibyl'in öldüğünü öğrenir; Henry'nin yorumu bir oyun gibidir. Dorian tabloyu örter, odayı kilitler | VII–X | C–D |
| **6. Bedel** | Yıllar geçer, yüz değişmez; söylentiler dolaşır, ama onu görenler inanamaz (XI). Basil gelir: "günah yüze yazılır" (XII). Dorian onu yukarı çıkarır, tabloyu gösterir; Basil çökmüş yüzü görür, dua etmesini ister. Dorian Basil'i öldürür (XIII). Kanıt yok edilir (tek cümle, adsız) | XI–XIV | E |
| **7. Dönüş** | İyi olmaya karar verir: bir köy kızını bırakır (adsız). Henry'ye "Beni bir kitapla zehirledin" der. Tabloya bakmaya çıkar: düzelmiş olmalı | XIX–XX | F |
| **8. Değişim** | Portrede yalnız ikiyüzlülük kıvrımı. "Onu mahveden güzelliğiydi" der (ayna kırılır), suçu sırayla tabloya, Basil'e, ötekilere verir; itirafı düşünür, güler: "Kim inanır?" Bıçağı tabloya saplar. Yer değiştirme. **İksir:** Wilde'ın üç karakter sözü (tek cümle) + 1895'te romanın mahkemede okunması (tek sahne) + soru izleyiciye. Abone çağrısı son anın içinde | XX; mektup 1894; dava 1895 | G |

\* Cümle numaraları senaryo kesinleşince yazılır (Kafka numara kayması dersi).

**Açık merak döngüleri (soru → cevap):**
1. Kanca: "kimse görmeseydi?" → G: hizmetçilerin gördüğü son oda.
2. B: Basil "kendimden fazlasını koydum" (neyi?) → E: Basil'in gördüğü yüz ve ölümü; G: Wilde'ın "olduğumu sandığım kişi" sözü.
3. C: "Tablo ilk kez ne zaman değişti?" → C sonu: Sibyl gecesi, zalimlik çizgisi (somut, görünür vaat: Kafka'daki "böceği hiç görmeyeceksiniz" türü).
4. F: "İyilik tabloyu düzeltir mi?" → G: ikiyüzlülük kıvrımı.
5. Kullanıcının sorusu "Güzellik bir lanet mi?" → G: Dorian'ın kendi cevabı ve kitabın tanıklığı.

**Uygulanacak dersler:** kancadan hikâyeye köprü sıfır cümle (B'nin ilk cümlesi hikâyenin ilk cümlesi; hikâye ~0:20'de başlar). Bölüm sonuna analiz kuyruğu yok; 1890/1891 farkı yalnız sahnenin içinde tek cümle (ör. dilek sahnesinde "ruhumu"). Hikâye bitince yorum uzatılmaz: Wilde mektubu ve 1895 tek sahne, ardından soru ve bitiş.

## 5. Başlık adayları (en az 10; beş soru)
**K**işisel soru mu · **N**efes · **Y**arı tahmin ettirir, ele vermez · **Ka**pı kelimesi ("Dorian Gray") içinde mi · **B**ağlamsız anlaşılır mı. Kalıp yasağı: Narkissos'un "Ne Zaman …?" kalıbı; Ran'ın vaadi ("Yaptıkların Sana Döner mi?") tekrar edilmez.

| # | Aday | K | N | Y | Ka | B | Not |
|---|---|---|---|---|---|---|---|
| 1 | Dorian Gray'in Portresi: Kimse Görmeseydi Ne Yapardın? | ✓✓ | ✓ | ✓ | ✓✓ | ✓ | Kapı önde (48 karakter), soru doğrudan izleyiciye. Videonun kancasıyla aynı soru |
| 2 | Güzellik Bir Lanet mi? \| Dorian Gray'in Portresi | ~ | ✓ | ✓ | ✓ | ✓ | Kullanıcının sorusu ve Dorian'ın kendi sözü. Ama genel soru, izleyicinin hayatına sorulmuyor; "güzellik" araması güzellik tüyolarına gidiyor; Narkissos'un konusuna (görünüş) yakın |
| 3 | Suçların Yüzüne Yazılsaydı? \| Dorian Gray'in Portresi | ✓ | ✓ | ✓ | ✓ | ~ | Güçlü imge; "yüzüne yazılmak" deyimi tanıdık ama soru yarım cümle |
| 4 | Hiç Yaşlanmasaydın, İyi Kalır mıydın? \| Dorian Gray | ✓ | ✓ | ✓ | ✓ | ✓ | Konu taramasındaki öneri. Vaadi gençlik/yaşlanma; video ağırlığı gizlilik ve bedelde, kayma riski |
| 5 | Bedelini Başkası Ödese, Yapar mıydın? \| Dorian Gray | ✓ | ✓ | ✓ | ✓ | ~ | Ran'ın vaadine yakın (yaptıkların döner); "neyin bedeli?" bağlam istiyor |
| 6 | Dorian Gray Tabloyu Neden Bıçakladı? | ✗ | ✓ | ✓ | ✓✓ | ✓ | Bilgi merakı (İkaros'un zayıflığı); kişisel değil, sonu ima ediyor |
| 7 | Bir Cümle Seni Yoldan Çıkarabilir mi? \| Dorian Gray | ✓ | ✓ | ✓ | ✓ | ✓ | İkinci damar (Henry); ana vaat değil |
| 8 | Dorian Gray'in Portresi: Vicdanın Bir Yüzü Olsaydı? | ~ | ✓ | ~ | ✓✓ | ~ | Soyut |
| 9 | Kimse Görmüyorsa Suç Sayılır mı? \| Dorian Gray'in Portresi | ✓ | ✓ | ✗ | ✓ | ✓ | Cevabı belli ("sayılır"); ahlak dersi gibi |
| 10 | Dorian Gray'in Portresi: Ruhunu Neye Satardın? | ✓ | ✓ | ~ | ✓✓ | ✓ | Pazarlık vaadi (Faust); video pazarlığın kendisini değil sonucunu anlatıyor |
| 11 | Dorian Gray Hiç Yaşlanmadı. Peki Bedelini Kim Ödedi? | ~ | ~ | ✓ | ✓✓ | ✓ | İkaros başlık kalıbı (iki cümle); uzun |
| 12 | Asıl Yüzünü Kimse Görmeseydi? \| Dorian Gray'in Portresi | ✓ | ✓ | ✓ | ✓ | ✓ | 1'in şiirsel hâli; daha belirsiz |

**Başkanın seçimi (senaryodan sonra kesinleşir): 1. aday**, "Dorian Gray'in Portresi: Kimse Görmeseydi Ne Yapardın?". Gerekçe: kapı kelimesi en önde ve akışta kesilmeden okunuyor; soru izleyicinin kendi hayatına soruluyor ve gündelik dildeki "kimse görmese de…" sözüyle tanıdık; cevabı yarı tahmin ettiriyor (bir şey saklanacak) ama neyin, nasıl bedel ödeneceğini vermiyor; videonun kancası aynı soruyla açılıyor. Kalıp Narkissos'tan ("Ne zaman…?") ve Ran'dan ("…döner mi?") farklı.
**Kullanıcının sorusu (2. aday) başlıkta değil, filmin içinde ve kapakta yaşar:** "Güzellik bir lanet mi?" sonun sorusu olur (Dorian'ın kendi cevabıyla sınanır). Başlıkta zayıf olmasının nedeni: genel bir soru ve "güzellik" kapısı konu dışına gidiyor.

## 6. Kapak fikirleri (iki ayrı vaat, iki ayrı kompozisyon; "yüz ve yansıma" yok)
- **A, "ortadan başlamak" (gizli oda):** karanlık çatı odası, Dorian'ın eli lambayla mor örtünün köşesini kaldırıyor; örtünün altı görünmüyor, yalnız tablonun altın çerçevesinin köşesi ve karanlık. Tek odak: lamba ışığının örtü kenarına düştüğü yer (karenin en parlak noktası). Dorian'ın yüzü yok ya da arkadan. Yazı: "KİMSE GÖRMEDİ" (2 kelime). Vaat: gizlenen bir şey var. Film ilk saniyede bu odayla açılır.
- **B, "A, B'yi etkiliyor" (bir sözle başladı):** bahçe/stüdyo; solda Lord Henry'nin koyu silueti, sigara dumanı bir çizgi gibi sağdaki genç Dorian'ın kulağına uzanıyor; arkada şövalede örtülü tablo. Yazı 4–6 kelime deneme: "HER ŞEY BİR CÜMLEYLE BAŞLADI" ya da daha kısa "ONU BİR CÜMLE BOZDU". Vaat: başkasının sözü insanı yoldan çıkarır mı? Film ~0:20'de bahçe sahnesiyle karşılar.
- Hassasiyet: kırmızı leke kan gibi okunur (Mary Stuart dersi); bıçak ve ceset kapakta yok. "BOZDU" fiilinin argo çağrışımı yok (kontrol edilecek); Henry–Dorian yakınlığı romantik/cinsel okunmayacak mesafede.
