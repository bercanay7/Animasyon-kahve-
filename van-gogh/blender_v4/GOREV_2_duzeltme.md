# GÖREV v4-2: A01 ve G02 düzeltmeleri (başkanın eleştirisinden)

Bu görev bilgisayardaki (RTX 4070) Blender oturumu içindir. `GOREV_1_oda.md` geçerliliğini korur; bu dosya onun §5 sıra 4'ün eleştirisidir.
Bulgular önizleme karelerinde (`onizleme/A01_*`, `G02_*`) ve saniyede 2 video karesinde ikişer bağımsız doğrulamadan geçti.
Sözcük zamanları `oda_planlari.json`'dan (G02: kardeş 2,98 · beşiğin 3,65 · gözleri 5,98 · yaşlıydı 6,40 · tığ 8,64 · örtüyü 9,34 · gösterip 9,76 · şaka 10,16 · yapar 10,48; A01: inandı 1,82 · yazı 4,02 · masası 4,32).

**Sıra:** önce A01 ve G02 bu listeye göre düzeltilir, önizlemeler yeniden çıkarılır ve push edilir. Başkan bakmadan kalan on plana geçilmez.
**Son filmde kareler gri dünyaya çevrilecek** (yalnız Vincent'in tabloları ve sarı zarflar renkli). Her düzeltme hem renkli hem gri karede okunmalı (bkz. genel kural 11).

---

## ENGELLEYİCİ

### E1. G02: Vincent bugünün giysisini giyiyor (kot, kemer, modern gömlek)
- **Sorun:** içeri sokulmuş düğmeli sivri yakalı lacivert gömlek, kemer köprülü kot pantolon, metal tokalı deri kemer, ceket yok. Hasır şapka ve bıyıksız çene sakalıyla bugünün çiftçisi ya da kovboyu gibi okunuyor. Duygusal doruğun ortasında, 1890 sahnesinde en görünür anakronizm. Gri karede de kemer, toka ve kot kesimi okunur. RAPOR_1'deki "mavi iş takımı gibi okunuyor" karede tutmuyor. GOREV §2'deki "mavi iş ceketi" yok.
- **Kanıt:** G02_25/50/75, Vincent x 370–545, kemer y≈255–265; v4k G02_001–026'nın hepsi.
- **Düzeltme:**
  - Gömlek ve kot (`male_casualsuit01` türevi) kaldırılır, kot dokusu ve dikiş normali silinir.
  - **Ceket (bleu de travail / bourgeron):** bol, kalçayı örten, düz mat pamuk (koyu-orta mavi, dokuda hafif solma), önde 4–5 düğme, küçük devrik yaka, 2–3 yama cep, bol kol. MPFB'de uygun giysi yoksa Blender'da modellenir (gövdeye shrinkwrap + solidify, sonra kısa cloth sim ya da kıvrım normal haritası). Kemer hattını örtecek boyda.
  - **İçi:** açık renk keten gömlek, küçük yaka, boyunda ince koyu bağ (A01'deki otoportrede ceketin altında açık gömlek görünüyor).
  - **Pantolon:** koyu yün ya da kadife, düz bol paça, kemer köprüsü ve toka yok.
  - **Sakal ve bıyık:** Vincent'in otoportrelerindeki gibi kızıl bıyık + kısa dolgun sakal; çene ve dudak altını örter (E1'in Amiş okumasını da kırar; ayrıca bkz. O1).
  - **Şapka kalır** (A01'deki otoportreyle bağ), kenar biraz daraltılır, tepe yumuşak ve hafif çökük, görünür hasır örgü dokusu (bkz. Y2).
- **Aynı model G01 ve G05'te de kullanılacak; düzeltme onlara da geçer.**

### E2. G02: bebek ve "tığ işi örtü" ölü kumaş kütlesi gibi okunuyor (tek kök: kumaş simülasyonu yok, beyaza yakın düz bez)
- **Sorun:**
  - **Kundak:** dikişsiz, kıvrımsız, kolsuz, beyaza yakın düz bir torba (ölçüm: medyan RGB ≈ 129/114/94, parlak uç ≈ 211/204/198; ışıkta beyaz okunuyor). Baş küçük ve kel, oyuncak bebek gibi; torba boyunun ≈ 1/6'sı. Bebek 12 sn boyunca hiç kıpırdamıyor.
  - **Örtü:** desensiz, sert, düz gri-beyaz bir levha. 020–023'te elden bağımsız havada eşkenar dörtgen gibi duruyor (avuç açık, parmaklar kavramıyor). 023→024'te ara kare olmadan kundağın üstüne geri sıçrıyor. "Tığ işi" ve "şaka" görüntüde hiç yok. Üstelik kundağın üstünden kaldırılıyor.
  - **Okuma:** iki doğrulayıcı kefen ya da morg okumasının şiddetinde ayrıştı. Yüz açık olduğu için kesin değil, ama "gözleri yaşlıydı" cümlesi ve Vincent'in iki ay sonraki ölümüyle birlikte olası. GOREV §6'nın "kundak beyaz değil" kuralına da ancak sınırda uyuyor. Planın tek eylemi okunmadığı için düzeltme şiddetten bağımsız olarak zorunlu.
- **Kanıt:** G02_25/50/75 beşik içi (x≈415–600, y≈330–450); v4k G02_019–024; G02_021'de havada duran levha açıkça görülüyor.
- **Düzeltme:**
  - **Bebek modeli:** 4 aylık oran (baş ≈ toplam boyun 1/4'ü). MPFB yaş 1 + 0,55 ölçek yetmiyor. Ya başı ve kafatası kemiğini 1,3–1,4 kat büyüt, ya da lisansı doğrulanmış (CC0 / CC BY / Standard) bir bebek modeli al (`lisans-kontrol` + ASSETS.md). İnce saç tutamı, yanakta hafif kızarıklık (deri dokusunda), açık gözler, ara sıra göz kırpma.
  - **Kundak:** göğüs hizasında açık, **bir ya da iki kol dışarıda**, yumruk eller. Kumaş krem-bej (`#D8C8A8` civarı, gri karede kundak ≤ %75 değer), üstünde ince mavi ya da gül kurusu çizgi ya da küçük desen, kenarı dantel. Kıvrım için ya bebeğe çarpışmalı cloth sim (birkaç kare oturt, sonra dondur) ya da sculpt ile kat yeri + normal haritası. Düz torba geometrisi kalmaz.
  - **Bebek hareketi:** plan başından itibaren nefes (göğüs ölçeği %2–3, 0,6–0,7 Hz). 0–2 sn'de bir el kalkıp iner. "örtüyü"de (9,34) baş örtüye doğru 15–20° döner.
  - **Örtü:** kundaktan ayrı bir nesne, ≈ 40×40 cm, ekru `#E8DCC0` (kundaktan farklı değerde). Başta **beşik korkuluğuna asılı** durur, bebeğin üstünde değil.
    - **Doku:** delikli tığ işi ağı alfa ile verilir. Prosedürel olabilir (Voronoi ya da Brick + daire eşiği → Alpha; lisans gerektirmez). Kenarda fistolu sıra. Işık deliklerden geçer, arkadaki kundak görünür.
    - **Fizik:** cloth sim. Pin grubu bir köşede; o köşe Vincent'in sağ el işaret ve başparmak kemiğine (`mixamorig:RightHandIndex2` / `RightHandThumb2`) hook ya da Child Of ile bağlanır. Parmaklar kıstırma pozunda kapanır.
    - **Zaman:** "tığ" (8,64) uzanma → "örtüyü" (9,34) korkuluktan kalkar, kendi ağırlığıyla sarkar → "gösterip" (9,76) Vincent örtüyü göğsünün önünde iki eliyle açıp Theo'ya ve kameraya doğru tutar (şaka jesti) → plan sonuna kadar elde kalır. Sıçrama ya da ara karesiz yer değiştirme olmaz.
  - **Beşik (ek gözlem, doğrulanmadı):** baş ucundaki gölgelik de beyaz, dolgulu düz bir blok gibi duruyor ve şilte kalın, beyaz. §6'daki "yastıklı uzun düz yatak" kuralına yakın. Gölgelik dökümlü krem tül (cloth sim, kenardan sarkan), şilte ince, çarşafı desenli olsun.

---

## YÜKSEK

### Y1. G02: 8,6 sn eylemsiz aralık; Theo'nun "şaka" tepkisi yok
- **Sorun:** 001–018 (0–8,5 sn) iki figür aynı pozda duruyor. Tek hareket kameranın yaklaşması (`planlar.py`'deki nefes ±1° görünmüyor). Kural 5 sn. "Şaka"dan sonra Theo'nun başı hâlâ beşiğe eğik, kardeşine dönmüyor. RAPOR_1'de yazan baş dönüşü render'da yok. Sessiz okuma "beşik başında yas".
- **Kanıt:** v4k G02_001, 009, 018 (aynı poz); G02_024–026 (Theo'nun başı eğik).
- **Düzeltme (sözcüğe bağlı; iki adam aynı anda öne eğilmez):**
  - 0,0: bebek eli ve nefes (E2), ağırlık kaydırma.
  - "kardeş" (2,98): Vincent sol elini Theo'nun omzuna koyar (≈ 0,5 sn), 7,6'da çeker.
  - "beşiğin" (3,65): Theo'nun sağ eli beşik korkuluğuna iner ve tutar.
  - "gözleri" (5,98): Theo başını 10° kaldırır, sol işaret parmağının yan yüzüyle **göz altını** siler (el alna gitmez: selam). Vincent bu sırada kıpırdamaz.
  - "yaşlıydı" (6,40): Vincent başını kaldırır, yüzü görünür (Y2'deki kamerayla).
  - "tığ" → "gösterip": E2'deki örtü eylemi.
  - "şaka" (10,16): Theo başını Vincent'e çevirir (yaw ≥ 35°, pitch +15°, 0,5 sn içinde).
  - "yapar" (10,48): Theo'da 2–3 küçük gülme sarsıntısı (omuz ±1,5 cm, ≈ 4 Hz, sönümlü) ve gülümseme.
    - Gülümseme MPFB2'nin yüz ifadesi (face/expression) birimleriyle verilir.
    - Mixamo iskeletinde yüz kemiği olmadığı için ya başa ayrı bir yüz armatürü bağlanır, ya da ağız köşesi ve yanak için iki shape key sculpt edilir.
  - Hareketlerin büyüklüğü 640 px karede seçilmeli. Raporu yazmadan önce her sözcük anının karesine bak.

### Y2. G02: kamera ölçeği, açısı ve kadrajı (Vincent'in yüzü görünmüyor; şapka bozuk)
- **Sorun:**
  - Tabloda "yakın" yazıyor, kare orta ya da geniş-orta: iki adam baştan bileğe, yüzler ≈ 60 px. G01 de "orta"; iki ardışık plan aynı ölçekte.
  - Kamera tepeden bakıyor, geniş şapka kenarı 0–9 sn Vincent'in gözlerini örtüyor. "Gözleri yaşlıydı" görüntüde yok.
  - Şapka tepeliğinin önünde kızıl-kahve bir oval var: saç şapkadan taşıyor (clipping). 001–019 arasındaki her karede görünüyor.
  - G02_021'de baş kalkınca şapka başın arkasında havada kalıyor (bağlantı hatası).
  - Yaklaşma sonunda baş boşluğu sıfır: G02_021–026'da şapka tepesi kesik, Theo'nun saçı y≈0–3'te.
- **Kanıt:** G02_25/50/75 (şapka x 395–520, y 10–85); v4k G02_001–019 (gözler kapalı), G02_021 (şapka kayık), G02_026 (kesik baş).
- **Düzeltme:**
  - **Gerçek yakın plan:** 50–65 mm. İki adam göğüsten yukarı, ön planda beşik korkuluğu, bebeğin başı ve elleri. Kamera yüksekliği göz hizasının 10–15° üstü, gözler şapka kenarının altından görünür.
  - **Alan derinliği:** f/2.8, odak yüzlerde (örtü anında örtüde). Ön plandaki korkuluk hafif yumuşak, bebek okunur kalır.
  - **Yaklaşma:** %10–15 ile sınırlı, son karede baş üstü boşluk ≥ kare yüksekliğinin %6–8'i.
  - **Şapka:** saç proxy'si şapkanın altında maskelenir (Mask modifier + vertex group) ya da kısa saç modeline geçilir. Şapka `mixamorig:Head` kemiğine bone-parent edilir, kenar alnın 2–3 cm üstüne oturur. Baş hareketinde kaymaz. İç yüzü koyu mat.
  - **Ölçek notu:** G01 "orta" kaldığı için G02 artık yakın; ardışık ölçek kuralı da böylece çözülür.

### Y3. A01 + G02: Theo'nun takımı ve başı 1880'ler değil (aynı model, aynı kök)
- **Sorun:**
  - **G02:** alçak düğmeli tek sıra blazer, kutu omuz. Yelek yok, beyaz dik yaka yok (yaka gri), geniş paisley desenli kravat ya da plastron, dar pantolon. RAPOR_1'deki "yaka beyaz, kravat ince" karede yok.
  - **Saç:** kafaya oturmuş düz kahverengi kask, tel ve kenar yok. A01'de arkadan makineyle kazınmış ya da kel gibi okunuyor, ense çıplak, yaka şeridi yok. Ceket arkadan kazak ya da softshell gibi.
  - **Sakal:** A01'de çene hattına oturmuyor, kulağın önünden sarkan bir yumru gibi duruyor (A01_75 x≈115–135, y≈150–190; A01_013).
  - **Pantolon:** A01'de bacakta eşofman şeridi gibi açık bir dikiş çizgisi var.
- **Kanıt:** G02_25/50/75 (Theo x 570–740, yaka x 600–690, y 70–200); A01_25/50/75 (x 0–300); v4k A01_007, A01_013.
- **Düzeltme:**
  - **Ceket:** sack coat, göğüste yüksek kapanan (3–4 düğme, en üstteki göğüs kemiği hizasında), dar ve yüksek yaka, dolgusuz doğal omuz, kalça altına inen etek. Arka orta dikiş ve yaka katı görünür. Kumaş koyu yün, hafif doku ve kıvrım normali.
  - **Yelek:** aynı ya da koyu kumaştan, göğse kadar kapalı.
  - **Yaka:** ayrı nesne olarak kolalı beyaz dik ya da wing collar, önde 3–4 cm, arkada ceket yakasının üstünde 1–2 cm şerit. Beyaz mat, takımın en açık yüzeyi.
  - **Kravat:** önde ince, düz koyu kravat ya da küçük fiyonk, desensiz. Kravatlı olduğu için papaz yakası okunmaz (§6).
  - **Pantolon:** düz, hafif bol, yan şerit yok.
  - **Giysi kaynağı:** `toigo_male_suit_tie_and_jacket` / `male_casualsuit01` bırakılır. Önce Fab, Sketchfab ya da CGTrader'da Victorian takım aranır (lisans-kontrol; ücretliyse fiyatıyla kullanıcıya sorulur). Bulunmazsa Blender'da modellenir. Referans: Woodbury & Page Theo fotoğrafları.
  - **Saç:** kısa, yandan ayrık, taranmış saç. Tepede birkaç cm, ensede kısa ama makine kesimi değil, açık kumral. Proxy'nin üstüne Hair Curves ile kenar telleri (Interpolate Hair Curves).
  - **Sakal:** shrinkwrap ile çeneye oturtulur, bıyıkla bağlanır, kulak önünden sarkan öbek silinir.
- **Aynı model C06, D01, D06, F03, G05 ve G10'da da kullanılacak.**

---

## ORTA

### O1. G02: Vincent'in sakalı tepeden bakışta boynu saran bir halka gibi
- **Sorun:** sakal çeneyi örtmüyor. Çene çıplak, altında boynu U biçiminde saran kızıl, boncuk dokulu bir bant var; tasma ya da kolye gibi okunuyor. Hassasiyet (ip) okuması zayıf: Van Gogh tabancayla öldü. Bu bir figür kusuru.
- **Kanıt:** G02_75 (x 425–475, y 75–112); v4k G02_008, G02_018–020.
- **Düzeltme:** sakal mesh'i (`wdg_scruffy_beard`) çene, çene ucu ve dudak altını örtecek biçimde fit edilir ya da değiştirilir. Boyun arkasına taşan kısım silinir. Bıyık eklenir (E1). Y2'deki alçak kamerayla birlikte denetlenir.

### O2. G02: eller gergin pençe pozunda
- **Sorun:** Theo'nun kalçadaki eli 11,77 sn boyunca açık "C" pençe; Vincent'in elleri ilk yarıda açık ve gergin. Manken etkisi veriyor.
- **Kanıt:** G02_50 (x≈660–705, y≈295–335); G02_25 (x≈380–530, y≈285–330).
- **Düzeltme:** dinlenme pozu: parmak eklemleri 20–40° kademeli bükük, başparmak içe yakın. Theo'nun eli korkulukta (Y1), Vincent'in eli Theo'nun omzunda ya da örtüde. Pençe pozu kütüphaneden silinir.

### O3. A01: kapak A odağı ve Theo okunmuyor
- **Sorun:**
  - Karenin en parlak noktası tablo değil: lamba (tepe 251) ve ay (236) daha parlak, tablo tepe 210.
  - Gri sürümde odak.py üç odak buluyor (lamba, ay, tablo).
  - 168 px'te Theo yüzsüz kara bir sırt; GOREV'deki "sırttan ¾" değil, tam sırt.
  - Kamera ne tuvale ne lambaya gidiyor; merkez sandalye. A01_013'te Theo'nun omuz ve sırtı sol kenarda kesik.
  - "İnandı" ve "yazı masası"ndaki baş hareketleri 640 px'te seçilmiyor.
- **Kanıt:** A01_25/50/75; v4k A01_001 (ay tam daire), A01_013; ölçümler bulgu kaydında.
- **Düzeltme:**
  - **Lamba:** görünen alev ve cam meshinin emisyonu düşürülür (camda hafif buz ya da is). Odayı aydınlatan ışık ayrı bir nokta ışık olur (Ray Visibility → Camera kapalı).
  - **Tablo:** karenin en parlak noktası olur (tablo yayımı biraz artırılır ya da çevre kısılır).
  - **Ay:** ilk karede kadraj dışında kalır ya da gücü tablonun altına iner.
  - **Theo:** soğuk ay kenar ışığı (saç ve omuz çizgisi pencereden ayrılır) ve ılık lamba dolgusu alır.
  - **Theo eylemleri:**
    - "inandı" (1,82): baş 10–12° kalkar.
    - "yazı" (4,02): baş ve omuz lambaya doğru 20–30° döner. Böylece ¾ profil (elmacık, bıyık, sakal) son karelerde görünür; kapak kuralı karşılanır.
  - **Kamera:** yay çizer, tuvalden "yazı masası"nda lamba ve masaya doğru kayar (truck + pan). Son karede Theo'nun omzu sol ön planda kadrajda kalır.

### O4. A01 + G02: genel görüntü kalitesi ("oyun ara sahnesi" görünümü)
- **Sorun:**
  - Yüzler plastik, deri gözeneksiz.
  - Kumaşlarda kıvrım yok.
  - DOF etkisiz: 36–38 mm f/3.5–4, arka plan en az ön plan kadar keskin.
  - Hacim ışığı yok.
  - A01'de siyahlar ezik (%26'sı L<10), ara tonlar tek turuncu-kahve.
  - A01 bekâr dekorunda GOREV §2'nin istediği raflar ve dayalı tuvaller yok.
  - Gri sürümde biçim ve doku zayıf kaldığı için kare düzleşiyor.
- **Kanıt:** A01_50, G02_50, G02_75.
- **Düzeltme:**
  - **Deri:** Subsurface Weight 0,1–0,2, gözenek normal haritası (`toigo_light_skin_male_ginger` normali varsa açılır).
  - **Giysi:** cloth sim ya da en az kıvrım normal haritası.
  - **Kamera:** Y2'deki lens ve diyafram.
  - **Hacim ışığı:** oda kutusuna Principled Volume (yoğunluk 0,002–0,005). G02'de pencereden giren hüzme, A01'de lamba çevresi.
  - **Ton:** AgX kalır. A01'de gölgelere düşük ılık dolgu verilir, siyah ezilmez. Kompozitte hafif gren ve vinyet.
  - **A01 dekoru:** §2 bekâr listesi tamamlanır: duvara konsollu raf, kitaplar, duvara dayalı 2–3 tuval (yüzleri maskeye, tarihleri genel kural 10'a göre).

### O5. G01, G02, G05: şövaledeki "Güller" o tarihte Paris'te değildi (yanlış bilgi, zorunlu)
- **Sorun:** Vincent'in Theo'ya c. 13 Mayıs 1890 mektubu (Complete Letters 633): güller ve irisler kurusun diye Saint-Rémy'de bırakılacak, sonra gönderilecek. Met'in sergi kaydına göre tablolar Haziran sonunda Auvers'e vardı. 17–20 Mayıs 1890 ziyaretinde Theo'nun odasında olamaz. Renkli kalacağı için gri dünyada vurgulanmış bir hata olur.
- **Kanıt:** G02_25/50/75 (x 840–960, y 40–250); GOREV §3 G01, G02, G05 satırları.
- **Düzeltme:**
  - Şövaledeki doku bir değişkene bağlanır (`--sovale <dosya>`).
  - Yeni tabloyu başkan, kaynakla (`kaynak/DOGRULAMA.md`, künye ile) Theo'da Mayıs 1890'dan önce bulunduğu doğrulanmış ve lisansı temiz bir tuvalden seçip bildirecek. Gelene kadar G02 Güller'le çizilmez; geçici olarak boş tuval arkası kullanılır.
  - Güller G10, G11 ve H01'de kalabilir; tarihlerine başkan bakar.
  - Duvara dayalı İrisler ve Zeytinlik de aynı gözle sınanacak. Met'in 1890 İrisler'i de Mayıs 1890'da kurumaya bırakılmıştı. Hangi dosyanın kullanıldığı RAPOR'a yazılsın.

---

## DÜŞÜK

### D1. A01: pencere ve dışarısı dönem okutmuyor
- **Sorun:** iri camlar, ≈ 20 px kalın dikey kayıt. Dışarıda düz simsiyah blok ve üstünde 2–3 parlak beyaz yatay çizgi (jaluzi ya da şerit gibi). Tek baca, çatı yok. RAPOR_1'deki "3×2 küçük cam, çatılar" karede yok.
- **Kanıt:** A01_25/50 (x 0–165, y 0–355; çizgiler y≈185, 265, 333).
- **Düzeltme:** iki kanatlı croisée, kanat başına 3–4 küçük cam, ince kayıtlar, ortada espanyolet çubuğu ve pirinç kol. Beyaz yatay çizgilerin kaynağı bulunup silinir. Dışarıda ay ışığında çinko kaplı mavi-gri mansart çatılar, lucarne'lar, sıra hâlinde toprak bacalar (alçak poligon yeter). Gri sürümde kayıtların haç oluşturmadığına tam boyda bakılır.

### D2. G02: raf ve kitaplar bugünün katalog odası gibi
- **Sorun:** blok ayaklı yüzer raf; 16–20 aynı boy, aynı turuncu-bej sırtlı, aynı bantlı kopya cilt.
- **Kanıt:** G02_25/50/75 sol üst (x 0–230, y 0–200).
- **Düzeltme:** profilli ahşap konsol ya da ayaklı étagère, koyu cila. Kitaplar farklı boy ve kalınlıkta, koyu deri ve bez ciltler; kimi eğik, kimi yatık. Poly Haven kitap varlığından en az 5–6 farklı sırt dokusu, rastgele ölçek ±%15.
  - **Reddedilen öneri:** sarı kapaklı Fransız romanları eklenmez. Sarı, filmde Vincent'in zarflarının sinyali; gri dünyada bile sarı nesne çoğaltmak bu dili sulandırır.

### D3. G02: renkli kalacak tablolar yalnız köşelerde ve kenarda yarım
- **Sorun:** İrisler sol alt köşede kesik, Güller sağ kenarda gittikçe kesiliyor. Gri dünyada bakışı bebekten kenara çeker.
- **Kanıt:** G02_75 (Güller x≈865–960, İrisler x≈0–100, y≈410–540); G02_026.
- **Düzeltme:** Y2'deki yakın planla çoğu kadrajdan çıkar. Kalan tablo ya bütün olarak, başların arkasında ve odak dışında durur ya da hiç görünmez. Kenarda kesik renkli şerit olmaz.

### D4. A01: hassasiyet temiz (kayıt)
- Şövalede kesişen çıta yok, papaz yakası yok, kırmızı leke, hale ya da asılı beden yok, pencere ızgarası haç okutmuyor. Düzeltme sonrası (yeni yaka, yeni pencere, gri sürüm) tam boyda yeniden bakılacak. Duvardaki sandalye gölgesi çömelmiş bir baş-omuz silueti andırıyor; ışık değişince bir kez bakılsın.

---

## Şiddeti düşürülen okumalar (bilgi için)
- **"Amiş/Menonit giysisi":** dinî bir okuma olarak zayıf; Türk izleyici tanımaz. Asıl sorun dönem hatası (E1). Bıyık ve iş ceketi bu okumayı da kapatır.
- **"Morgda çarşaf kaldırma":** yüz açık olduğu için kesin değil; asıl sorun okunmayan eylem (E2).
- **"Sakal-ip":** ölüm biçimi tabanca, ip çağrışımı zayıf (O1).

---

## Kalan on plana taşınacak genel kurallar
1. **Dönem giysisi denetimi her figürde:** kot, kemer köprüsü ve tokası, sokulmuş modern gömlek, alçak düğmeli kutu omuz blazer, makine saçı, eşofman şeridi yok. Theo her planda yelek + beyaz dik yaka + ince kravat; Vincent iş ceketi; Jo GOREV §2'deki gibi (baştan ayağa siyah değil).
2. **Kumaş levha gibi durmaz:** kundak, örtü, perde, gölgelik, Jo'nun eteği, giysiler ya cloth sim ya da kıvrım normaliyle. Elde tutulan her nesne parmak kemiğine bağlı ve parmaklar onu kavrar. Hiçbir nesne havada durmaz, ara karesiz yer değiştirmez.
3. **Beyaz bez kütlesi yok:** kundak, çarşaf, örtü ve yatak krem-bej, desenli, birbirinden farklı değerde; gri karede de desen okunur.
4. **Bebek** (F03, G01, G05, H01): E2'deki düzeltilmiş model. Yüz ve en az bir el görünür, plan boyunca nefes alır ve kıpırdar.
5. **Eylem:** her plan ilk saniyeden hareket eder. 5 sn'yi aşan figür eylemsiz aralık olmaz. Her eylem bir sözcüğün `t`'sine bağlıdır ve 640 px'te seçilecek büyüklüktedir (baş ≥ 15–20°, kol ya da el yer değiştirir). Kamera yaklaşması tek başına eylem sayılmaz.
6. **Kamera:** tablodaki ölçek gerçekten tutturulur; ardışık iki plan aynı ölçekte olmaz. Duygu taşıyan planlarda kamera göz hizasının ±15° içinde, yüz ¾. Şapka kenarı gözü örtmez. Son karede baş üstü boşluk ≥ %6. Figür kazara kadrajdan kesilmez. DOF görünür (≥ 50 mm ya da f/2.8).
7. **Saç, sakal, şapka:** kask saç ya da clipping yok. Şapka baş kemiğine bağlı, altındaki saç maskeli. Sakal çeneyi örter ve bıyıkla bağlanır.
8. **Eller:** dinlenme pozu, gergin pençe yok. Boşta kalan el bir yere değer (korkuluk, masa, cep, omuz). Erkeğin kolu kadının beline ya da kalçasına uzanmaz.
9. **Işık ve odak:** karenin en parlak noktası tablo (G11 hariç). Lamba alevi ve ay onu geçmez. Renkli kalacak tablo kadrajda ya bütün durur ya hiç görünmez.
10. **Tablo tarihi:** şövalede ya da duvarda görünen her Vincent tuvali, o planın tarihinde Theo'nun elinde olduğu kaynakla doğrulanmış olmalı. Dosyayı başkan verir. G01 ve G05'te Güller değişir.
11. **Gri önizleme:** `onizle.py` her plan için ayrıca `<PLAN>_50_gri.jpg` üretir (RGB gri + maske bölgesi renkli). Hassasiyet taraması (§6 + CLAUDE.md listesi) hem renkli hem gri tam boy karede yapılır. Düzeltilen her plan yeniden bakılır; düzeltme yeni simge üretebilir.
12. **Rapor karede görüneni yazar:** RAPOR_1'deki "beyaz yaka, ince kravat", "Theo kardeşine döner", "mavi iş takımı gibi okunuyor" ve "3×2 küçük cam, çatılar" karede yoktu. Her iddiadan önce ilgili sözcük anının karesi açılır. Karede olmayan yazılmaz.
13. **Set:** kitaplar çeşitli, raf dönem konsollu, pencere croisée ve dışarıda mansart çatılar. Bekâr ve evli dekor GOREV §2 listesine tam uyar. Sarı zarf dışında sarı kâğıt nesne yok.
14. **Teslim:** A01 ve G02 düzeltilip önizlemeleri (25/50/75, gri, mp4) push edilir ve RAPOR_2.md yazılır. Bu listedeki her madde için "yapıldı / yapılamadı + neden" yazılır. Başkanın onayından sonra kalan on plana geçilir.
