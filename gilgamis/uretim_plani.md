# Gılgamış: üretim planı

Başlangıç: 23 Kasım 2026. Bu video bir deneyin yarısı (`analiz/2026-11-23-deney-yon-promptu.md`): oturuma ayrıntılı talimat değil, yalnız bir yön verildi (`analiz/2026-11-23-gilgamis-yon-prompt.md`). Kurul, puanlama ve çok ajanlı akış yok (19 Kasım kararı); başkan tek başına.

**Yön (kullanıcının, özet):** ölümsüzlük arayan kahramanın macerası değil; dostunun ölüsünün başından kalkamayan, sonra korkudan dünyanın ucuna kaçan bir adam. Soru izleyicinin kendi sorusu: öleceğini bile bile nasıl yaşanır? Cevap kavramla değil olayla: buluyor, yılana kaptırıyor, eli boş dönüyor. Peşinden gidilecek şey dönüş: her şeyi kaybeden biri surları neden bir yabancıya gururla gösteriyor? Canavar, tanrı, tufan yalnız bu soruya hizmet ettiği kadar. Güç Enkidu'nun yatağının başından. İzleyici kendi suruna bakarak çıkar.

## 1. Talep kontrolü (23 Kasım 2026)
Ölçüm: `python3 araclar/talep/talep.py …` ve `araclar/talep/iki_dil.py` (YouTube Türkçe otomatik tamamlama + ilk 10 videonun izlenmeleri).

| Sorgu | Öneri | İlk 10 medyan | En çok | Öne çıkan öneriler |
|---|---|---|---|---|
| **gılgamış** | 14 | **122 B** (iki_dil: 79 B) | 15,4 M (İngilizce, oyun/anime karışık) | destanı, sesli kitap, Kürşat Demirci, okumaları, şarkısı |
| **gılgamış destanı** | 14 | **67 B** | 1,36 M | sesli kitap, Kürşat Demirci, özet, "diamond tema" |
| gılgamış ve enkidu | 3 | 100 B | 1,36 M | gilgamesh vs enkidu, gilgamesh fate (anime) |
| gılgamış ölümsüzlük | 4 | 3 B | | hikayesi, kimdir, mezarı |
| ölüm korkusu | 14 | 45 B | 234 B | nasıl yenilir, neden olur, panik atak |
| ölümü düşünmek | 5 | 37 B | | psikoloji, "sürekli ölümü düşünmekten nasıl kurtulurum" |
| ölümsüzlük | 14 | 69 B | | oyun (totem), "ölümsüzlük mümkün mü" |
| öleceğini bilmek | 5 | 1,5 B | | |
| *kontrol:* sisifos / dönüşüm kafka | 14 / 14 | 198 B / 34 B | | |

**Okuma:**
- (a) **Tanıdık kapı güçlü:** "gılgamış" Kafka'nın ~3, Sisifos'un ~yarısı kadar. Türkçe en çok izlenen ikinci video "Mağrur Olma Gılgamış, Senden Büyük Ölüm Var" (1,36 M): Türk izleyicinin bu destanda aradığı şey zaten ölüm. Yönün açısı talebin kendisiyle örtüşüyor.
- "gılgamış" araması anime (Fate) ile karışıyor; "gılgamış destanı" temiz. Başlıkta "Gılgamış" önde, açıklamanın ilk satırında "Gılgamış Destanı".
- (b) **Kişisel soru güçlü:** "öleceğini bile bile nasıl yaşanır?" izleyicinin hayatına sorulan soru. "Ölüm korkusu" aramaları (45 B) yardım arayan izleyiciden geliyor ("nasıl yenilir", "panik atak"): başlık tedavi ya da tavsiye vaat etmez; video kimseye öğüt vermez, bir hikâye anlatır ve soruyu geri verir.
- Türkiye kapısı: Hattuşa (Çorum). Başlıkta değil, açıklamada ve filmin sonunda tek cümle.

## 2. Başlık adayları (en az 10; beş soruyla elenir)
Sorular: **K**işisel soru mu · **N**efes · **Y**arı tahmin ettirir, ele vermez · **Ka**pı kelimesi içinde · **B**ağlamsız anlaşılır. Karakter sayısı mobil kesim için (≤ 45).

| # | Aday | Kr. | K | N | Y | Ka | B | Not |
|---|---|---|---|---|---|---|---|---|
| 1 | **Gılgamış: Öleceğini Bile Bile Nasıl Yaşanır?** | 44 | ✓ | ✓ | ✓ | ✓ | ✓ | Yönün sorusu kelimesi kelimesine. Cevabı tahmin ettirmiyor ama "bir cevap var" diyor; video cevabı olayla veriyor |
| 2 | Gılgamış: Ölümsüzlüğü Buldu, Bir Yılana Kaptırdı | 47 | ✗ | ✓ | ✓ | ✓ | ✓ | Bilgi merakı (İkaros'un zayıflığı); kapak yazısına daha uygun |
| 3 | Gılgamış Destanı: Dostun Ölünce Ne Yapardın? | 44 | ✓ | ✓ | ~ | ✓✓ | ✓ | Güçlü ve duygusal; ama videonun sorusu dostun ölümü değil kendi ölümün. Vaadi bir bölüm |
| 4 | Gılgamış: Her Şeyini Kaybeden Kral Neden Övündü? | 47 | ✗ | ✓ | ✓ | ✓ | ~ | Yönün peşinden gidilen sorusu; konu sorusu, izleyicinin hayatına değil |
| 5 | Ölümden Kaçılır mı? \| Gılgamış Destanı | 37 | ~ | ✓ | ✗ | ✓ | ✓ | Genel soru ("hayır" diye bilinir) |
| 6 | Gılgamış Destanı: Ölüm Korkusuyla Nasıl Yaşanır? | 47 | ✓ | ✓ | ✓ | ✓✓ | ✓ | İki kapı ("ölüm korkusu" + destan). Ama "nasıl yenilir" arayana tavsiye vaadi gibi okunur; video tavsiye vermiyor. Hassasiyet: kaygı bozukluğu arayan izleyici |
| 7 | Gılgamış: Ölmeyeceğini Bilseydin Ne Yapardın? | 45 | ✓ | ✓ | ✗ | ✓ | ✓ | Ters soru; destanın cevabını karşılamaz |
| 8 | Gılgamış: Ölümsüzlüğü Kaybedince Elinde Ne Kalır? | 49 | ~ | ✓ | ✓ | ✓ | ✓ | Uzun; cevabı (sur) zor tahmin edilir, iyi; ama "kalır" izleyiciye değil krala |
| 9 | Gılgamış: Eve Eli Boş Dönen Kral | 31 | ✗ | ✓ | ✓ | ✓ | ✓ | Kısa, soru değil |
| 10 | Gılgamış Destanı: Bir Gün Öleceksin, Sonra? | 41 | ✓ | ✓ | ~ | ✓✓ | ✓ | Sert, doğrudan; "sonra" ölümden sonrasını (din) çağırabilir: yanlış kapı |
| 11 | Gılgamış: En Yakın Dostunu Kaybetseydin? | 39 | ✓ | ✓ | ✗ | ✓ | ✓ | 3'ün yumuşağı |
| 12 | 4000 Yıllık Soru: Öleceğini Bile Bile Nasıl Yaşanır? | 51 | ✓ | ~ | ✓ | ✗ | ✓ | Kapı kelimesi yok, uzun |

**Seçim: 1. aday, "Gılgamış: Öleceğini Bile Bile Nasıl Yaşanır?" (44 karakter).** Gerekçe: tanıdık kapı önde; soru izleyicinin kendi hayatına; filmin ilk ve son sorusu bu (A05, H10). Dorian Gray'in başlığıyla aynı biçim ("Ad: soru?"); kapak kalıbı kuralı (art arda aynı kapak kalıbı yok) kapak için, başlık biçimi Dorian'da tuttuğu için korunur. **Yedek:** 3. aday (Test ve karşılaştır başlık değil kapak sınadığı için yalnız yayın sonrası yeniden paketleme seçeneği).

## 3. Kapak taslakları (iki ayrı vaat, iki ayrı kompozisyon)
- **A, "ortadan başlamak":** gölette Gılgamış'ın açık eli, elinden kayan dikenli bitki ve bitkiyi ağzında götüren yılan; yılanın arkasında bıraktığı deri. Tek odak: bitki (tek vurgu rengi, lacivert taş tonu ya da yeşil ışık). Yazı 2–3 kelime: **"ELİNDEYDİ"** ya da "YILANA KAPTIRDI". Vaat: "aradığını buldu ve kaybetti". Filmin ilk karesi (A01) bu kompozisyonla aynı eksende.
- **B, "karşıtlık":** solda yüzü örtülü ölü Enkidu (yatay, durgun), sağda dik oturan, başını ellerine almış Gılgamış; arkadaki duvarda yedi çentik. Yazı (4–6 kelime denemesi; CLAUDE.md'deki deneme önerisi): **"7 GÜN GÖMMEDİ"** ya da "DOSTUNU 7 GÜN GÖMMEDİ". Vaat: "bir kayıp". A02'de (ilk 10 sn) karşılanıyor.
- Kapak yazısı hassasiyetten geçer: ceset gösterilmez, yalnız örtülü beden; kurt gösterilmez.

## 4. Üslup: kil kabartma (silindir mühür baskısı) — başkanın seçimi
**Neden:** destanın kendisi kildir. Enkidu kilden yaratılır (I 101–104), tufandan sonra "bütün insanlık kile döner" (XI 133), Gılgamış'ın son gösterdiği şey "bir parça kil çukuru" ve fırında pişmiş tuğladır (XI 324–328), hikâye de pişmiş kilden tablette dört bin yıl kaldı. Görüntünün malzemesi hikâyenin cevabıyla aynı olunca kavramı söylemeye gerek kalmaz: film baştan sona yaş kil, son sahne pişmiş tuğla.
- **Malzeme yasası:** sıcak yaş kil (oker, toprak), kabartma figürler yükseklik haritasından ışıkla çıkar; kazınmış çizgiler (saç, sakal, kumaş kıvrımı) oyuk. Işık sahnenin duygusu: gündüz yukarı soldan yumuşak; yatağın başı meşale ışığı, alçak ve titrek; karanlık yol neredeyse sıfır ışık; tufan şimşek.
- **Renk:** kil tek renk + tek vurgu: **lacivert taş** (lapis lazuli: lacivert tablet, ölüm suları, gölet, bitkinin ışığı). Ateş ve fırın sıcak ışık olarak (renk değil ışık).
- **Figür:** Mezopotamya kabartma geleneği gibi profil gövde, önden göz; Gılgamış kıvırcık sakallı, Enkidu uzun saçlı ve kıllı, Utnapiştim uzun ak sakal, Urşanabi sırıklı kayıkçı, Siduri uzun saçlı. Kodla çizimin zayıf yanı (yüz, el) geleneğin kendi biçimine dönüşür.
- **Kamera:** silindir mühür gibi soldan sağa kayan friz; mühür yuvarlanınca yeni sahne kile basılır (mekân sıçramalarında geçiş). Aynı mekânda kesme.
- **Motor:** kendi motorlarımızda ve cinecode/Lemo kataloğunda kabartma yok (`araclar/lemo/KATALOG.md` tarandı). Yeni, küçük bir motor: Canvas 2D ile yükseklik + ayrıntı + malzeme tuvalleri, JS'te bulanıklık ve ışık (yazılımsal WebGL'in yavaşlığına girmeden). Çekim sistemi Narkissos'un `film.js`'i (`S()`, `Wd()`, `plan()`), render `render.js`.
- **Sınanacak (üslup kapısı):** manzara (Uruk ve surlar), orta plan figür (Gılgamış ve Enkidu), yakın plan (yatağın başı, meşale), 15 sn hareket (yılan bitkiyi alır, deri kalır); kare süresi; 168 px okunurluk; hassasiyet (secde, çıplaklık, dinî imge).

## 5. İskelet (senaryodan önce seçildi)
**Seçim: Harmon çemberi.** Önceki videolar: Narkissos Kişōtenketsu, Dorian Gray Harmon (arada Lale Çılgınlığı var; art arda değil). Gerekçe: yön tam bu çemberin alt yarısını anlatıyor. Harmon'da kahraman istediğini bulur (5), bedelini öder (6), dönen kişi giden kişi değildir (7–8). Gılgamış ölümsüzlüğü ister, ihtiyacı başka bir şeydir; buluyor, kaybediyor, dönüyor, ve dönüşte değişmiş olan bakışıdır: aynı surlara bakıyor, ama bu kez bir yabancıya gösteriyor. "Ölümsüzlük arayan kahramanın macerası" okumasından kaçmak için çember **dönüşten başlar** (halka: kanca A03 dönüşü gösterir, H01–H09 aynı ana döner); destan da aynı halkayı kurar (I 18–23 = XI 323–328).

**Kahraman:** Gılgamış. **Bedeli ödeyen:** Enkidu. **Yabancı:** kayıkçı Urşanabi; sonra okuyucu, yani izleyici.

| Adım | İçerik | Cümleler |
|---|---|---|
| 0. Kanca | bitki eldeyken yılan; ölü dost; eli boş dönüş ve surlar; "neden övünür?"; "öleceğini bile bile nasıl yaşanır?" | A01–A05 |
| 1. Sen (rahat bölge) | Uruk'un zorba kralı | B01–B02 |
| 2. İhtiyaç | kilden bir denk: Enkidu, Şamhat, ekmek-bira-giysi, dostluk | B03–B11 |
| 3. Git | ölüme ilk cevap: "adımı bırakırım", ormana | C01–C04 |
| 4. Ara | orman, Humbaba, kapı, boğa; tanrıların kararı; **yatağın başı**; korku ve kaçış; karanlık yol, Siduri, ölüm suları; Utnapiştim, uyku sınavı | C05–F12 |
| 5. Bul | denizin dibindeki bitki | G01–G05 |
| 6. Öde | yılan; "kimin için yoruldu bu kollar?" | G06–G10 |
| 7. Dön | Uruk, kayıkçıya surlar | H01–H04 |
| 8. Değiş | aynı sözler destanın başında: davet okuyana; yabancı sensin; senin surun | H05–H11 |

**Merak döngüleri (soru → cevap olay):**
1. **L1** "Her şeyini kaybetmiş bir adam neden övünür?" (A04) → H01–H09: sur bir yabancıya gösterilir, aynı davet okuyana yapılır, tablet kâtipten kâtibe geçer: yabancı sensin. Cevap bir olay dizisi (gösteriş, davet, tabletin yolculuğu), kavram değil.
2. **L2** "Altı gün yedi gece başından kalkamadı" (A02) → D11–D13 (çığlığıma kalkar diye; burnundan kurt düşene kadar).
3. **L3** "Ekmek, bira, giysi… ölüm döşeğinde hatırlayacaktı" (B09) → D04–D06 (Şamaş'ın sorusu ve kutsama).
4. **L4** "Bir tek insan ölümsüz" (E01) → F05 (tanrılar bir kez verdi) → F06 (senin için kim toplayacak?).
5. **L5** "Sen nasıl ölümsüz oldun?" (F02) ve uyku sınavı → F10 (ekmekler).
6. **L6** bitki yenmedi, Uruk'a götürülüyor (G05) → G07 (yılan). Kancanın (A01) cevabı.
7. **Başlığın sorusu** (A05) → D06 (Enkidu'nun cevabı, olayla), E07 (Siduri), H04 ve H10 (izleyiciye geri verilir; cevap verilmez).

**Bölüm kartları (YouTube bölümleri; ekran sorusu anlatılmaz):** I. Yabani adam · II. Ormanın bekçisi · III. Yatağın başı · IV. Dünyanın ucu · V. Tufandan kurtulan adam · VI. Yılan · VII. Surlar.

## 6. Tempo kontrolü (seslendirmeden önce; `araclar/analiz/tempo_kontrol.py senaryo.json --yazar "Thompson,George"`)
Art arda soyut dizi yok; ilk iki dakikada soyut aday yok; köprü adayı yok.

| id | bayrak | karar |
|---|---|---|
| A04, A05 | T | olay: cevap H01–H09 (olay dizisi) |
| C03 | T | olay (alıntı); C04 tek soyut cümle, olaydan hemen sonra |
| D04 | T | olay (Şamaş'ın sözü; B09'un ödemesi) |
| D14 | T | olay (kendi sözü); kaçışı başlatır |
| E06 | T | olay (Siduri'nin sözü) |
| **E09** | **A** (Urşanabi, ikinci yarıda yeni ad) | **riskli, kabul**: Urşanabi destanda X. tablette girer. Önlem: kancada rolü ("yolda tanıştığı yabancı bir kayıkçı") ve görüntüsü ekildi (A03); adı E09'da, sonra hep "kayıkçı". Doruk (H) onun yüzüne değil, surun görüntüsüne dayanıyor |
| F01 | M | olay (bakış; "farkı yok" görülen şey) |
| F02, F06, F12 | T | olay |
| G01 | M ("tıpkı") | olay + tek gözlem cümlesi; E07'nin yankısı, yorum uzatılmaz |
| G09 | T | olay (kendi sözü) |
| H02 | T | olay |
| H08 | A (Hititler, Hattuşa, Çorum) | kabul: kişi değil yer; doruğu taşımıyor, tek cümle |
| H10 | MT | iksir: olaydan (H09) sonra tek soyut cümle + soru |
| H11 | A | abone çağrısı ve bitiş ekranı |

**Hikâye nerede bitiyor:** G10/H04 (dönüş ve surlar). Ardından H05–H11 (~50 sn) destanın kendi açılışı, Hattuşa ve izleyiciye soru. "Hikâye bitince izleyici gider" dersi: bu kuyruk somut (tablet, sandık, kilit, Çorum), yorum H10'da tek cümle. Tahmin olarak `analiz/tahminler.md`'ye yazıldı.

## 7. Yönden kendi seçtiklerim (deney kaydı; `geriye_bakis.md`'ye taşınacak)
Yön şunları vermedi; başkan seçti:
- **İskelet:** Harmon, dönüşten başlayan halka.
- **Üslup:** kil kabartma; gerekçesi destanın kendi malzemesi (kil, tuğla, tablet).
- **Yabancı = izleyici:** destanın açılışındaki davetin (I 18–28) sondaki sözlerle aynı olması, yönün sorusuna olayla verilen cevap oldu.
- **"Altı gün yedi gece" kalıbı:** Şamhat'la insanlaşma, dostun başında yas, uyku sınavı: üç kez aynı süre, hiç açıklanmadan.
- **Ekmek zinciri:** Şamhat'ın ekmeği (B08) → Şamaş'ın hatırlattığı ekmek (D04) → Siduri'nin "karnını doyur"u (E07) → uyku sınavının ekmekleri (F10) → surun içindeki fırınlar (H04).
- **Kapı ve duvar zinciri:** kapıda boğuşma, eşik yıkılır (B10) → ormandan kesilen kapı, ölüm döşeğinde lanetlenir (C08, D02) → Siduri kapıyı sürgüler (E05) → günler duvara çizilir (F08) → sur (H).
- **Bırakılanlar:** İştar (ad yükü; boğa "tanrıların gönderdiği" diye), 1872 George Smith (bilim tarihi bölümü açmamak için), Gılgamış'ın Enkidu heykeli, XII. tablet, tufanın kuşları (dinî karşılaştırma çağrısı ve süre).
- **Hattuşa:** kanca ve başlık yerine sonda tek cümle; "yabancı sensin"in Türk izleyici için somut hâli (yabancılardan biri bu topraklardaydı).
