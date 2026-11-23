# Gılgamış: geriye bakış (23 Kasım 2026; kurulsuz üretim, başkan)

Bu video bir deneyin yarısıydı (`analiz/2026-11-23-deney-yon-promptu.md`): oturuma adım adım talimat değil, yalnız ~115 kelimelik bir yön verildi. Kullanıcının sonraki iki notu: "Bütün tercihler %100 senin" ve alt ajanlar başkanın takdirinde. Fable seslendirmeden önce bir kez senaryoyu okudu; ayrı bir okuyucu ajan bütün planları yazısız karelerden okudu ve hassasiyet taraması yaptı.

## Deney kaydı: neyi kendim seçtim, yön nerede yetmedi
**Yönün verdikleri:** soru ("öleceğini bile bile nasıl yaşanır?"), cevabın biçimi (kavram değil olay: bulur, kaptırır, eli boş döner), peşinden gidilecek an (surların bir yabancıya gösterilmesi), filmin ağırlık merkezi (Enkidu'nun yatağının başı), çıkış duygusu (izleyici kendi suruna bakar).

**Başkanın seçtikleri** (yönde yoktu):
- **Üslup: kil kabartma.** Gerekçe destanın kendi malzemesi: Enkidu kilden yaratılır, tufandan sonra insanlık kile döner, son sahne pişmiş tuğla ve kil çukuru, hikâye de kil tablette kaldı. Kendi motorlarımızda ve Lemo/cinecode kataloğunda karşılığı yoktu; yeni ve küçük bir motor yazıldı (aşağıda).
- **İskelet: Harmon, dönüşten başlayan halka.** Kanca dönüşü ve surları gösterir; destan da aynı halkayı kurar (I 18–23 = XI 323–326).
- **Cevabın olayı: yabancı = okuyucu.** Gılgamış'ın kayıkçıya söylediği sözler, ilk tablette okuyana yapılan davetle aynı. Ardından tablet ve sandık, kâtipten kâtibe geçen hikâye, Hattuşa (Boğazkale) ve "bugün o yabancı sensin". Yönün "neden bir yabancıya?" sorusuna kaynakta bulunan bir olayla cevap verdi.
- **Yapı zincirleri** (anlatılmadan görüntüde ve sözde yankılanır): "altı gün yedi gece" üç kez (Şamhat, yas, uyku sınavı); ekmek zinciri (Şamhat'ın ekmeği → Şamaş'ın hatırlatması → Siduri'nin "karnını doyur"u → uyku sınavının ekmekleri → surun içindeki fırınlar); kapı ve duvar zinciri.
- **Bırakılanlar:** İştar (ad yükü), 1872 keşfi (ayrı bilim tarihi bölümü açmamak için), tufanın kuşları (dinî karşılaştırma çağrısı), Gılgamış'ın Enkidu heykeli, XII. tablet.
- **Başlık:** "Gılgamış: Öleceğini Bile Bile Nasıl Yaşanır?" (yönün sorusu kelimesi kelimesine). Talep ölçümünde Türkçede en çok izlenen ikinci Gılgamış videosu zaten ölüm temalıydı.

**Yönün yetmediği yerler:**
- **Kaynağın ayrıntısı:** yön "adam aradığını buluyor" diyordu, ben de ilk taslakta "ölmemenin yolunu buldu" yazdım. Bitki ölümsüzlük değil gençlik veriyor ("Yaşlı adam gençleşir"); ölümsüzlük şansı uyku sınavında kaybediliyor. Fable yakaladı. Yön bir okumayı veriyor, kaynağın kendisini vermiyor; ayrıntı doğrulaması yine kaynakla yapılmalı.
- **Kancanın ikinci kapak vaadi:** yön kapaktan söz etmiyordu; "7 GÜN GÖMMEDİ" kapağı ile anlatımın "altı gün yedi gece"si çelişiyordu (Fable). Kapak "7 GECE GÖMMEDİ" oldu, A02 "gömdürmemişti" sözcüğünü taşıyor.
- **Yön, kanalın sonradan gelen kuralını kapsamadı:** "iskeletten önce kullanıcının fikri sorulur" kuralı (CLAUDE.md, 22 Kasım) bu oturuma iskelet ve senaryo yazıldıktan sonra geldi. Kullanıcının yön metni o adımın yerini tuttu ve kullanıcı tercihleri başkana bıraktı; ayrıca sorulmadı. Deney için not: yön metni, "kullanıcının bakışı" adımının yazılı hâli gibi çalıştı.
- **Görüntüdeki tuzaklar yönle önlenmez:** kod çizimi yine kendiliğinden simge üretti (aşağıda). Bunu bulan yön değil, ayrı bir okuyucuydu.

**Deneyin ölçüleri:** kullanıcının üretim sırasındaki düzeltmesi: 0 (bu yazı yazılırken). Atlanan kanal kuralı: 1, "kullanıcının fikri" adımı (yukarıda). Başkanın kendi yakaladığı kural ihlali: kancanın kapak B vaadi (Fable'la birlikte). 48. saat ve 7. gün ölçüleri `analiz/tahminler.md` (G1–G3) ve deney tablosuna yazılır.

## Kil kabartma motoru (`lib/kil.js`)
- Sahne üç tuvale çizilir: yükseklik (gri), ayrıntı (128 nötr; oyuk ya da kabarık çizgi), malzeme rengi. JS'te kutu bulanıklığıyla yumuşatılır, eğimden normal çıkarılır, yönlü ışık + meşale gibi noktasal ışıklar + üç örnekli kabartma gölgesi + geniş bulanıklıktan oyuk gölgesi hesaplanır. Yazılımsal WebGL'e girilmedi; tam boy kare ~0,3–0,6 sn (4 işçi), animatik yarım çözünürlükte 0,08 sn.
- **Işık duygu taşır:** yatağın başı meşale (alçak, titrek), karanlık yol neredeyse sıfır ışık, tufan şimşek, sur sahnesi alçak akşam ışığı. Aynı sahne yalnız ışık yönü döndürülerek "altı gün yedi gece" geçer.
- **Kabartma yükseltme:** Enkidu'nun kilden doğuşu, figürün yüksekliği zeminden yükselerek; tufanda insanlığın kile dönüşü ters yönde; sondaki yabancı aynı yolla kile çekilip yerine parmak izi basılıyor.
- **Dünya koordinatında doku:** kil rengi ve kabarcık deseni kamera dönüşümüyle çizilir; kaydırmada doku yüzmez.
- **Geçiş: silindir mühür.** Yeni sahne sağdan sola kile basılır (mekân sıçramalarında ve bölüm kartlarında). Bölüm başlıkları kile oyulmuş yazıdır.

## Ne zorladı, ne öğrendik
- **Figür iskeleti:** ilk kapsül figürler "çubuk bacaklı" ve oturuşta bozuktu; Mezopotamya oranlarıyla (geniş önden omuz, kalın baldır, büyük baş, etek kalçadan) yeniden yazıldı. Yakın planlar küçük figürü büyüterek değil, figürü büyük çizerek kuruldu (`SET.yakin`); ayrıntı keskin kaldı.
- **Görüntü okumasının yakaladıkları** (ayrı ajan, yazısız 198 kare; engelleyici yok):
  - Uzuvların yuvarlak uç konturu yakın planda omuzda yarım daire bıraktı ve **kıllı erkeğin göğsünde meme** gibi okundu; eklemlerde "delik" halkalar. Kök neden: kapsülün iki ucu da konturlu. Düzeltme: uzuv ikinci parçalarda ve omuzda **açık başlı kontur** (`uzuv(..., acik)`).
  - Tufanda T kollu, aynı boyda sıra hâlinde figürler **haç sırası** okundu. Pozlar çeşitlendi, yükseklikler ve aralıklar bozuldu.
  - Kat kat sivri sedirler ve yuvarlak başlı maymunlar **Noel ağacı ve kardan adam** okundu. Sedir Lübnan sediri gibi yassı ve düzensiz katlı, maymun profil, çıkık burunlu ve sarkan kuyruklu çizildi.
  - Akrep insanların boğumlu kuyruğu boncuk dizisi (tespih) okundu; ilk düzeltme kuyruğu halka yaptı; ikinci düzeltmede sırttan başın üstüne kıvrılan kuyruk.
  - Kapı + ortasından geçen sürgü haç; iki sürgü ve opak kanat.
  - Çizgili oval örtü ve aslan postu **kalkan** okundu; örtü yatağın kenarından sarkan saçaklı kumaş, post pençeli sarkan deri oldu.
  - Sakaldaki 3×4 halka ızgara yakın planda **telefon tuş takımı** okundu; kaydırılmış C bukleler.
  - Güneş diskinin başın hemen üstünde durması **hale**; güneş yukarı ve iki figürün arasına alındı.
  - Tanrıları simgeleyen boynuzlu taçlar "pasta, arı kovanı" okundu; kanal kuralına da uygun olarak tanrılar **ışık** oldu (C10, B03'teki yaratılış).
  - **Ders (Lale'yle aynı):** her düzeltme yeni bir simge üretebilir; akrep kuyruğu düzeltmesi halkaya döndü, tam boy karede yeniden bakıldı.
- **Fable'ın senaryo okuması** (seslendirmeden önce) bir engelleyici bulgu getirdi: C03'teki "İnsanlar kapılarda bundan söz eder", Jastrow ve Clay'in 1920'deki eskimiş okumasıydı (*ba-ba-nu*). Bugünkü okuma "insanın günleri sayılıdır; ne yapsa yeldir"; Akadca harf çevirisinde (depodaki kaynak dosyası) başkan doğruladı. **Ders:** kamu malı çeviri lisans için güvenli, ama okuması eskimiş olabilir; tırnak içi her dize bugünkü okumayla karşılaştırılır. Ayrıca kayıtta Thompson'da "yok" yazılan iki yer (kapıya lanet, kile dönüş) aslında vardı.
- **Kil/kıl:** "kilden doğdu"nun hemen ardından "kıl içindeydi" seste aynı sözcük gibi duyulurdu (Fable). Filmin ana motifine yakın sözcükler seste ayrı tutulur.
- **Yer tutucu ses dosyası depoya girdi:** `build_vo.py` çekim yokken sessizlikten 70 MB'lık `vo.wav` yazıyor; ilk commit'te girdi, sonraki commit'te çıkarıldı (`gilgamis/.gitignore`). Geçmişi temizlemek için zorla push izni yoktu; birleştirmede sıkıştırılırsa geçmişten de çıkar.


## İzleyici gözüyle son okuma (Fable, ilk render üstünde; üç kişilik: telefonda öğrenci, TV'de abone öğretmen, yas içindeki izleyici)
- **Ortak düşüşler iki yerde, ikisi de kanalın kendi derslerinin yerinde:**
  - **4:55 "Ben de ölmeyecek miyim?":** filmin tez cümlesi 12 sn geniş planda, yüzsüz; arkadaki aslan "tasmalı köpek" okundu. Düzeltme: aslan çıktı, "Ben de"den itibaren yakın yüz (akşam ışığı).
  - **5:12–5:37:** yeni ve zor ad (Utnapiştim) neredeyse boş karede, ardından 8 sn tek pozlu karanlık. Düzeltme: Utnapiştim adıyla birlikte kıyıda görünür; karanlıkta "ne önünü… ne arkasını"da baş döner, figür küçülür; karanlık telefon için bir kademe açıldı.
- **Doruğun sürekliliği** (kapak A'nın vaadi): bitki dipte kalıyordu (koparılınca ele bağlandı); "derisini bıraktı" denirken kıyıda başlı bir yılan yatıyordu (başsız, içi boş kabuk); Gılgamış yılana bakıp bir şey yapmıyordu (yıkanırken sırtı dönük, bitki gidince döner).
- **Yazı:** kart sesten farklı cümleydi ("bırakırım" / "bırakmış olurum"); "Süleymaniye Müzesi" İstanbul sanılır (", Irak" eklendi); altyazıda sayı yazıyla kalmıştı ("2011'de", `tools/merge.json`).
- **Bölüm kartı I kaldırıldı:** kancanın sorusundan 4 sn sonra gelen kart "ders başlıyor" hissi veriyordu (köprü kuralı). Öteki kartlar kaldı.
- **Hassasiyet:** sedir gövdesinin en üst katı aşması ağaç tepelerinde haç okuması üretiyordu; gövde en üst katın altında bitiyor. Havada oturan figürlere tabure ve yatak kenarı.
- **Yas içindeki izleyici için:** okuyucunun hükmü "kötü gelmez, büyük ihtimalle iyi gelir; teselli vaaz değil kanıt olarak (ekmek, giysi, dost, sur)". İki keskin yer kaynağın kendi sözü ("burnundan kurt", "karın koynunda sevinsin"); değiştirilmedi, kurt gösterilmiyor. Açıklamaya tek satırlık not eklendi.
- **Reddedilen/ertelenen:** parmak izinin alt yarısını doldurmak (iç içe tam halka hedef tahtası okunur; yay biçimi korundu); ceylan ve Humbaba'nın biçim incelikleri (zevk payı); kapak A ile filmdeki gölet farkı (kanca simge olarak elde gösteriyor, kapak da öyle; doruğun kendisi gölette).
- **Ders:** üç kişilik okuma Lale'deki gibi işe yaradı; ortak düşüşler soyutluk değil bu kez **görüntünün bilgi taşımadığı** yerlerdeydi (yüzsüz tez cümlesi, boş karede yeni ad). Ses sabitken ikisi de yeni planla karşılandı.

## Render ve teslim
- **İkinci render ilk karede çöktü:** kanca su halkasının fazı `(st.lt*.6 + k/3) % 1` ilk karede eksi çıktı (JS'te `%` eksi kalanı korur), elips yarıçapı eksi oldu. Düzeltme `((x % 1) + 1) % 1`; ardından bütün planlar tek karede tarandı. **Ders:** zaman eksi olabilen her `%` çift modla yazılır; render'dan önce her planın ilk ve son karesi çizdirilir.
- **Zincir koşulsuz kurulmuştu:** render çöktüğü hâlde teslim betiği eski `gilgamis.mp4`'ten kopya üretti. Render → teslim zinciri `&&` ile bağlanır, kopyanın süresi ve tarihi render'la karşılaştırılır.
- **x265 iki geçiş günlüğü** (`x265_2pass.log.cutree`, 168 MB) çalışma dizinine yazılıp commit'e girdi; push reddedilince fark edildi. `.gitignore`'a eklendi; teslim betiği günlüğü `teslim/` dışında, `-x265-params stats=` ile scratchpad'e yazmalı.
- Son kopyalar: YouTube 255 MB (H.264 CRF 21), telefon 97 MB (H.265 2 geçiş 1000k); ikisi de 677,35 sn.

## Açık kalanlar
- Kulakla son onay kullanıcıda (`yayin.md` → "Kulakla bakılacaklar").
- Shorts yapılmadı (adaylar `youtube.md`).
- Yayın: 6 Aralık 2026 18:00. Sonuçlar 48. saat (8 Aralık) ve 7. gün (13 Aralık) verisiyle `analiz/tahminler.md` (G1–G3) ve deney tablosuna (`analiz/2026-11-23-deney-yon-promptu.md`) yazılır.
