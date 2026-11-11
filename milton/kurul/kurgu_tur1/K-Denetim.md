# K-Denetim (kaynak denetçisi): İlk tam kurgu, tur 1

Alan: kaynak ve doğruluk (veto alanı). Mercek: ekrandaki her alıntı, künye, tarih, ad ve görsel olgu kaynakla ve anlatımla çelişiyor mu?
Bakılan malzeme: `animatik/planlar.json` (142 plan, bütün `yazi` alanları), `lib/acts/*.js` içindeki bütün `quote/etiket/txt/kit_yaz/chapterCard` çağrıları, `kaynak/kayip_cennet_1674_dizeler.json`, `kaynak/notlar.md`, `senaryo.json`, `youtube.md`, orta özet sayfalarının tamamı (8 sayfa), son özet sayfası 6, tam boy kareler (t0026.70, t0470.20, t0547.77, t0584.17, t1243.04, t1278.04, t1371.13, t1380.89).

## 1. Puan ve karar

| Ölçüt | Ağırlık | Puan |
|---|---|---|
| Ekran alıntılarının dizeye sadakati | 0,30 | 9,5 |
| Künye, tarih ve ad doğruluğu | 0,20 | 8,5 |
| Görsel olguların metne sadakati | 0,30 | 8,3 |
| `youtube.md` kaynak künyeleri ve zaman damgaları | 0,10 | 9,3 |
| Ekran / anlatım / açıklama tutarlılığı | 0,10 | 8,8 |

**Ağırlıklı ortalama 8,85. Karar: RED (hafif).** Hiçbir ölçüt 7'nin altında değil. Aşağıdaki 1. ve 2. maddeler (görsel olgu çelişkisi) düzeltilirse ONAY veririm; yeniden bakmam yeterli olur, tam tur gerekmez.

**Engelleyici (yanlış bilgi) bulgu: yok.** Ekranda basılan hiçbir alıntı, dize numarası, yıl ya da ad yanlış çıkmadı. Aşağıdaki iki görsel çelişki "yüksek öncelik": ikisi de metni çelişkiye düşürüyor ama anlatım cümlesini yanlış yapmıyor; bu yüzden veto saymadım. Başkan farklı görürse ben veto yönünde okumayı da savunabilirim (ikisi de kolay düzeltilir).

## 2. Engelleyici bulgular

Yok. (Bkz. yukarı; en yakın adaylar 3.1 ve 3.2.)

## 3. Düzeltilmesi gereken bulgular (sıralı)

### 3.1 P116 (K02, 19:55): Şeytan, Âdem ile Havva'nın tövbesinin yanında duruyor
- Görüntü: iki figür diz çökmüş, sağ köşede yükseltide dik duran kanatlı Şeytan (`lib/acts/adn.js:1031–1051`, `kiy_seytan` x:1690; özet orta/sayfa06 P116).
- Kaynak: X.1086–1104 (tövbe sahnesi). Bu sahnede Şeytan yok. Şeytan bu noktada X.504–521'de yılana dönüşmüş, cehennemdedir; X.1097'de bahçede ya da yakınında olması Milton'a aykırı. Anlatım K02 ("Onlar, Şeytan'ın yapmadığını yapmışlardı") karşıtlık kuruyor, ama görüntü onu olay yerinde bir gözlemci gibi gösteriyor; ilk kez gören biri "Şeytan onları izliyordu" sanar.
- Düzeltme: Şeytan'ı kareden çıkar ya da J06'daki gibi çerçeveyle ayrı bir yarıya al (solda tövbe, sağda "Nifates'te dik duran siluet" ayrı çerçevede). Ya da yerine yalnız uzun, tek başına bir gölge/boş yükselti bırak.
- Kazanç: kaynak sadakati +0,3.

### 3.2 P022 (C05, 3:40): Lucifer'in kuzeydeki sarayı Dor sütunlu Yunan tapınağı
- Görüntü: sağ üstte sütunlu, alınlıklı tapınak (`lib/sahne/cennet.js:288–299` `cen_saray`, çağrı `cen.js:129`; yorumda "Dor sütunlu, alınlıklı tapınak").
- Kaynak: V.756–761: "High on a hill, far blazing, as a mount raised on a mount, with **pyramids and towers from diamond quarries hewn, and rocks of gold**; the palace of great Lucifer". Dor sütunlu tapınak Milton'da cehennemin Pandemonium'udur (I.713–717). İki yapı aynı dille çizilince cennetteki saray, cehennemdekinin tekrarı gibi okunuyor (bilinçli bir koşutluk değilse çelişki).
- Düzeltme: sarayı "dağ üstünde dağ" biçiminde kademeli kule/piramit siluetine çevir; altın kayalar için kenar ışığı. Dor sütun yalnız Pandemonium'da kalsın.
- Kazanç: +0,2.

### 3.3 Künye eksikliği: açıklama "ekrandaki numaralar" diyor, ekranda yalnız beş künye var
- Ekranda künye olanlar: I. 254–255 (E06), I. 263 (E07), III. 41–42 (B06), III. 51–52 (L09), (I. 26) (K06). Hepsi doğru.
- Senaryo A01 için "Ekranda künye: John Milton · Kayıp Cennet · IV.75" diyor (`senaryo.json` A01 kaynak alanı); ekranda yok (`nif.js:470`: yalnız “Ben cehennemim.”, `kaynak` verilmemiş). G07 (P072) aynı. Filmin en önemli dizesi künyesiz.
- `youtube.md` açıklaması: "ekrandaki numaralar kitap ve dize numarasıdır". Altı yedi başka alıntıda (IV.75, VI.181, IV.363…) numara yok.
- Düzeltme: ya A01'e (ve G07'ye) "KAYIP CENNET · IV. 75" künyesini ekle (G07'de yeter), ya da açıklamayı "bazı dizelerin altında kitap ve dize numarası görünür" diye yumuşat. Tercihim: A01/G07'ye künye + açıklamayı olduğu gibi bırak değil, "kimi dizelerin altında" yap.
- Kazanç: +0,15.

### 3.4 P013 (B05, 1:58): "1667" yılı, anlatımın söylediğiyle kayıyor
- Ekranda: el yazması yığını üstünde sağ üstte "1667" (`oda.js:686`). Anlatım B05: "Destanına, devrim henüz ayaktayken başlamıştı. Bu yenilginin içinde bitirdi." `senaryo.json` B05 kaynak alanı bu planda "'1660' ekran yazısı" diyor; kodda 1667 var.
- 1667 yayım yılı (Simmons sözleşmesi 27 Nisan 1667, DNB s. 35), bitiş yılı değil (Aubrey: 1663). "Bitirdi" derken "1667" görünce izleyici bitiş yılı sanar. Yanlış değil ama kaynakla kayıtlı sözleşmeyle (1660) uyuşmuyor.
- Düzeltme: "1667" yerine "1658–1663" (DNB s. 34) ya da "yayım: 1667"; 1667 zaten P006 başlık sayfasında var. Seçenek 2: yazıyı kaldır.
- Kazanç: +0,1.

### 3.5 P121 (K07, 20:43): "WILLIAM BLAKE · 1793" ve `notlar.md` çelişiyor
- `notlar.md`: *The Marriage of Heaven and Hell* (1790–93); `youtube.md`: "1793 dolayları". Ekran: kesin "1793".
- Doğrulayamadığım: eserin tek bir basım yılı; yaygın kaynaklar 1790–93 ya da c. 1790 verir (levha 3 üstündeki tarih 1790 olarak biliniyor; hatırımdan, bakmadım). Kesin "1793" yazmak iddiayı gereğinden keskinleştiriyor.
- Düzeltme: "WILLIAM BLAKE · 1790–93" (ya da "yak. 1793"). Açıklamadaki "1793 dolayları" ile aynı olsun.
- Kazanç: +0,1.

### 3.6 P028 (C11, 4:39): tırnak içinde bir yaklaşıklık
- Ekran: “binlerce hainin arasında sadık kalan tek kişi”; anlatım "Milton onu şöyle anlatır:" diyor.
- Özgün: V.896–899 "faithful found among the faithless, faithful only he; among innumerable false". "Innumerable" = sayısız; "binlerce" bir yuvarlama. Tırnak içinde özgüne yaklaşık söz var.
- Düzeltme: "sayısız hainin arasında sadık kalan tek kişi" (ses değişmeyecekse yalnız ekran yazısını değiştir; ses "binlerce" diyorsa tırnağı kaldır ve "Milton onu şöyle anlatır" yerine "anlatıcı" biçimine çevir). Önerim: ekranı sesle aynı tut, tırnağı bırakma.
- Kazanç: +0,05.

### 3.7 P057 (F02, 9:44): Günah'ın alt gövdesi kuyruk gibi ince, kedi kuyruğu okunuyor
- Görüntü (t0584.17): örtülü kadın siluetinin soluna ince, kıvrık bir kuyruk çıkıyor.
- Kaynak: II.650–653: beline kadar güzel kadın, ötesi "many a scaly fold … a serpent armed with mortal sting" (kıvrım kıvrım pullu yılan gövdesi, zehirli iğne); II.653–659 belinde cehennem köpekleri havlar.
- Düzeltme: kuyruğu kalın, birkaç halkalı ve sivri uçlu yap (pullu kıvrım). Köpekler istenirse atlanabilir (anlatım söylemiyor).
- Kazanç: +0,05.

### 3.7b P057: "dokuz katlı" kapı sayılamıyor
- Kodda 9 band var (3 pirinç, 3 demir, 3 elmas: `kap.js:2, 25–35`), ama t0584.17 karesinde yedi sekiz yatay bant seçiliyor ve alt kısım figürlerle örtülü; pirinç/demir/elmas ayrımı okunmuyor. F02 anlatımı "Dokuz katmanlı kapı" diyor. Kaynakla çelişki değil, ama "dokuz" iddiası görüntüde doğrulanamıyor.
- Düzeltme: P057'nin açılışında (ya da P056 bölüm kartının arkasında) kapıyı bir an sabit geniş planda göster, dokuz bandı üçerli üç grup olarak ayrı ayrı ton/doku ile vur (pirinç parlak, demir perçinli, elmas sivri).
- "Elmas": Milton'da "adamantine rock" (II.646). Türkçede elmas yerine "çelik gibi sert kaya" daha doğru olurdu; `kap.js` yorumunda "elmas" yazıyor, ekranda yazı yok, yani sorun yok.

### 3.8 P004 / P041 (A04, E02): "ışık yok" denirken kare ışıklı
- Anlatım A04: "Etrafında alev var ama ışık yok; yalnızca görünür bir karanlık" (I.62–63). Ekran yazısı "GÖRÜNÜR / KARANLIK".
- Görüntü (t0026.70): figürün arkasında kare içinde en parlak alan olan geniş soluk ışık diski ve sağ üstten gelen ışık huzmeleri; alevler beyaz kenarlı. `KURUL.md` (Kapı 2) "alevler figürü aydınlatmaz" kararı vermiş; bu karar alevler için uygulanmış, ama gökteki disk ve huzme hâlâ "ışık" okunuyor.
- Savunma: E05'te (I.209–213) huzme "göğün izni" olarak anlamlı. Ama A04 (anlatım "ışık yok" derken) huzme zaten var.
- Düzeltme: A04 anlatım süresince arka plan diskini kısık (tek ton, gri) tut; huzmeyi yalnız E05'te "izin" anında başlat. Alternatif: A04'te disk kalsın, ama "karanlık görünür" sözcüğünde diski söndür.
- Kesin kanım: kısmi çelişki. Doğrulayamadığım: izleyici bunu "çelişki" okur mu, yoksa Doré dili olarak mı. Bu yüzden orta öncelik.

### 3.9 Küçük ve bilinçli sapmalar (kayıt için, düzeltme istemem)
- H04/H08 (P086, P090): Âdem ile Havva örtülü/giyinik siluet. Milton: "naked majesty" (IV.290), çıplak. Bu, H-Hukuk ve H-Hassasiyet kararıyla bilinçli; senaryo çıplaklıktan söz etmiyor. Çelişki yok. (Not: örtülü çizim anlatımdaki "örtülü" kelimesiyle uyuyor.)
- P115 (K01): gün doğumu. Milton XII'de saat belirtmez (XII.629'daki "evening-mist" bir benzetme); gün doğumu bir tercih. Doğrulayamadım ki akşam mı sabah mı. Dokunmayın, ama "akşam benzetmesi" ile çatışabileceğini bilin.
- Büyük harf yazım tutarsızlığı: P027 "ABDIEL", P063 "URIEL", P020 "LUCIFER", P052 "PANDEMONIUM" noktasız I ile; Türkçe büyük harf kuralında "İ" kullanılan yerlerde ("İRADE", "KAPIDAKİ") bu adlar yabancı özel ad olduğu için doğru. Tutarsızlık değil, kaynak bulgusu değil; tipografi üyeleri değerlendirsin.

## 4. Ekrandaki bütün metinler: dizeye sadakat tablosu

Hepsini doğruladım (özgün: `kayip_cennet_1674_dizeler.json`). Hatalı olan yok; yaklaşık olan tek madde 3.6.

| Plan | Ekrandaki metin | Künye (ekranda) | Özgün dize | Sadakat |
|---|---|---|---|---|
| P001 / P072 | “Ben cehennemim.” | yok (bkz. 3.3) | IV.75 "myself am Hell" | doğru |
| P003 / P114 / P136 | Onu orada tutan ne(ydi)? | – | senaryo sorusu (IV.18–23) | doğru |
| P004 | görünür karanlık | – | I.63 "darkness visible" | doğru |
| P006 | KAYIP CENNET · John Milton, 1667 / PARADISE LOST. A POEM / JOHN MILTON | – | 1667 ilk baskı on kitap | doğru; bkz. 5.1 |
| P008 | KÖR ŞAİR | – | A06 | doğru |
| P011 | Londra, 1660 | – | DNB s. 33 | doğru |
| P013 | 1667 | – | yayım yılı | doğru ama kayıyor (3.4) |
| P014 | “…ama bana gün dönmez.” | III. 41–42 | III.41–42 "not to me returns day" | doğru |
| P018 / P020 | IŞIK TAŞIYAN / LUCIFER · ışık taşıyan | – | V.760, VII.131–133, X.425 | doğru |
| P025 | üçte biri | – | V.710 "the third part" | doğru |
| P027 | ABDIEL | – | V.803 | doğru |
| P028 | “binlerce hainin arasında sadık kalan tek kişi” | – | V.896–899 | yaklaşık (3.6) |
| P030 / P038 | DOKUZ GÜN; VIII… "dokuz gün" (I–IX sayacı) | – | VI.871 "Nine days they fell" | doğru; sayaç IX'a ulaşıp 'yuttu'da bitiyor (`sav.js:270–279`) |
| P031 | “Sen de özgür değilsin; kendi kendinin tutsağısın.” | – | VI.181 | doğru |
| P032 | “…krallık değil, zincir bekle.” | – | VI.186 "chains in Hell, not realms, expect" | doğru |
| P040 | CEHENNEMDE KRAL | – | I.263 | doğru |
| P041 | “Ah, ne kadar düşmüş, ne kadar değişmişsin!” | – | I.84 | doğru |
| P042 | irade · intikam · nefret · yüreklilik | – | I.106–108 | doğru |
| P046 | “Zihin kendi dünyasıdır.” | I. 254–255 | I.254–255 | doğru |
| P047 | “Cehennemde hükümdar olmak, cennette hizmetkâr olmaktan yeğdir.” | I. 263 (soluk, alev çizgileri üstünde; t0470.20) | I.263 | doğru |
| P048 | cennette köle olacağıma, cehennemde kral olurum (tırnaksız, "bildiğimiz hâli") | – | I.263 yaygın söyleniş | doğru, yöntem uygun |
| P050 | gurur · pişmanlık | – | I.603–605 | doğru |
| P052 | PANDEMONIUM | – | I.756 | doğru |
| P055 | Diz çökmeyi reddeden melek… | – | II.477–478 | doğru |
| P056 | KAPIDAKİ BEKÇİLER | – | II.645–673 | doğru |
| P058 / P059 | GÜNAH / ÖLÜM · kendi oğlu | – | II.746–760; II.781–787 "Thine own begotten" | doğru |
| P060 | KAOS | – | II.890–916 | doğru |
| P063 | URIEL | – | III.634–735 | doğru |
| P064 | Nifates Dağı | – | III.742 | doğru |
| P068 | “Ey güneş… ışınlarından nefret ediyorum.” | – | IV.32–37 | doğru (elips) |
| P069 | “Hak etmemişti.” | – | IV.42 | doğru |
| P071 | “O hâlde kimi suçlayacaksın?” | – | IV.67 | doğru |
| P074 | “Pişmanlığa hiç yer kalmadı mı?” | – | IV.79–80 | doğru |
| P075 | boyun eğmek | – | IV.81 "submission" | doğru |
| P080 | “Kötülük: sen benim iyiliğim ol.” | – | IV.110 | doğru |
| P083 | ADEN'DE BİR YABANCI | – | – | doğru |
| P087 | “Onları sevebilirim bile.” | – | IV.363 "could love" | doğru |
| P089 | “zorbaların bahanesi: zorunluluk” | – | IV.393–394 | doğru |
| P090 | “Bense… bir cehenneme itildim.” | – | IV.508 | doğru |
| P093 | “Şimdi günahına benziyorsun.” | – | IV.839–840 | doğru |
| P095 | YILANIN İÇİNDE | – | IX.182–190 | doğru |
| P096 | V / yedi gece (I–VII) | – | IX.63 "seven continued nights", IX.67 "on the eighth returned" | doğru; sayaç VII'ye kadar, 'sekizinci'de kesiliyor (`sav.js:532–537`) |
| P097 | “Ne iğrenç bir alçalış!” | – | IX.163 | doğru |
| P098 / P125 | “yükseldiği kadar alçalmak zorundadır” / “yükseldiği kadar alçalır” | – | IX.169–170 | doğru |
| P099 | sersem bir iyilik | – | IX.465 "Stupidly good" | doğru |
| P103 | Kazanmıştır. | – | – | doğru |
| P104 | ALKIŞ | – | X.505 | doğru |
| P106 | “Hem de bir elmayla!” | – | X.487 | doğru |
| P109 | Önünde diz çökülen kral, şimdi karnının üstünde. | – | X.513–514 | doğru |
| P112 | günah hangi kılıkta, ceza o kılıkta | – | X.516 | doğru |
| P115 | “Bütün dünya önlerindeydi.” | – | XII.646 | doğru |
| P117 | İnsan aldatıldı → merhamet \| Asi melek kendi kendini ayarttı → yok | – | III.129–132 (özgün çoğul "the first sort") | doğru (tekil sadeleştirme) |
| P118 | 1674 | – | ölüm: 8 Kasım 1674; ikinci baskı 1674 | doğru |
| P119 | İKİ OKUMA / Bu destanın kahramanı kim? | – | – | doğru |
| P120 | Tanrı'nın yollarının adil olduğunu göstermek | (I. 26) | I.26 | doğru |
| P121 | WILLIAM BLAKE · 1793 | – | c. 1790–93 | bkz. 3.5 |
| P122 | “Cehennemde hükümdar…” “Zihin…” “Meydanı kaybettik; ne çıkar?” “Ben cehennemim.” | – | I.263, I.254, I.105, IV.75 | doğru |
| P123 | C. S. LEWIS · Kayıp Cennet'e Önsöz · 1942 | – | *A Preface to Paradise Lost* (OUP, 1942) | doğru |
| P124 | kahraman · general · politikacı · casus · (pencere) · kurbağa · yılan | – | Lewis: hero, general, politician, secret service agent, peeper at bedroom/bathroom windows, toad, snake | doğru; yedi basamak, sıra aynı |
| P127 | Tanrı insanı, insanın efendisi yapmadı. | – | XII.69–71 (Âdem konuşuyor) | doğru |
| P129 | Cromwell, 1657 | – | tacı Mayıs 1657'de reddetti | doğru |
| P130 | Başkaldırı her zaman özgürlük müdür? | – | senaryo | doğru |
| P131 | BİR DAMLA YAŞ | – | – | doğru |
| P132 | Alexandre Cabanel · Düşmüş Melek, 1847 | – | *L'Ange déchu*, 1847 | doğru |
| P135 | gurur mu? / pişmanlık mı, | – | I.603–605 | doğru |
| P137 / P138 | gururu / gururu mu, açılmayan kapı mı? | – | IV.82 "Disdain"; III.129–132 | doğru |
| P139 | Belki herkesin, söylemeyi kendine yasakladığı bir söz vardır. | – | senaryo | doğru |
| P140 | “göksel ışık, içime parla” | KAYIP CENNET · III. 51–52 | III.51–52 "celestial Light, shine inward" | doğru |
| P141 | O gözyaşı pişmanlık mıydı, gurur mu? / Başkaldırı ne zaman özgürlük? | – | senaryo | doğru |
| P142 | ZAMAN KURYESİ | – | – | doğru |

## 5. Ad, yıl ve sayı soruları (istenen 2. madde)

1. **1667 / 1674 ve P006 başlık sayfası:** 1667 ilk baskı on kitaptı, 1674 ikinci baskı on iki kitap; ikisini de ekran ya da anlatım karıştırmıyor. P006 sayfası "bizim çizimimiz" ve 1667 sayfasında özgün olarak "Written in Ten Books" ibaresi bulunur; film sayfasında "PARADISE LOST. A POEM / JOHN MILTON" var, ibare yok. Bu bir kopya iddiası değil; Türkçe "KAYIP CENNET · John Milton, 1667" altyazısı onu bizim yorum yapıyor. Makul. İsterseniz "A POEM" altına "WRITTEN IN TEN BOOKS" ekleyin (özgün başlık sayfasıyla uyum, +0,05); zorunlu değil.
2. **LONDRA, 1660:** doğru (Defensio'nun yakılması, DNB s. 33; cellat eliyle yakma). Sahne "cellat + kitap + saklanan şair" metinle uyumlu.
3. **Cromwell, 1657:** doğru (tacı reddetti). K15b'deki "yerini oğluna bıraktı" (Richard, 1658) doğru.
4. **WILLIAM BLAKE · 1793:** bkz. 3.5.
5. **C. S. LEWIS · Kayıp Cennet'e Önsöz, 1942:** doğru. Doğrulayamadığım: "bölüm 13" numarası (`notlar.md`'de var, ekranda yok, bu yüzden önemsiz).
6. **Alexandre Cabanel · Düşmüş Melek, 1847:** doğru. Doğrulayamadığım: müzeye giriş yılı (`notlar.md`'de 1889; ekranda ve açıklamada yok).
7. **LUCIFER · ışık taşıyan:** Lucifer adı Milton'da V.760, VII.131–133, X.425'te geçer ("so call him"); "ışık taşıyan" Latince anlamdır, dizede yazmaz. Anlatım C03 bunu doğru sunuyor ("Lucifer adını yakıştırır: ışık taşıyan"). Doğru.
8. **URIEL, NİFATES DAĞI:** doğru (III.648 vd., III.742, IV.1 vd.).
9. **"VIII / dokuz gün" (P038):** düşüşün dokuz günü I–IX sayacıyla sayılıyor (`sav.js:270–279`); ortada VIII görünmesi sayaç ilerlerken doğru (özet orta karesi 6:20'de). Sayaç 'yuttu' sözcüğünde IX'a ulaşır. VI.871 ile uyumlu. İnce nokta: I.50–52 destanda ayrıca "dokuz gün" gölde yatışı da söyler; film yalnız düşüşü sayıyor, çelişki yok.
10. **"V / yedi gece" (P096):** sayaç 'yedi' sözcüğünden 'sekizinci'ye I–VII gösteriyor (`sav.js:532–537`), IX.63–67 ("seven continued nights … on the eighth returned") ile uyumlu. Orta karedeki "V" ara sayım.

## 6. Görsel olgu denetimi (istenen 3. madde)

| Konu | Görüntü | Sonuç |
|---|---|---|
| Dokuz gün düşüş | P038 sayaç I–IX | doğru |
| Gölde zincir (I.48, I.210) | P005 bilekte halkalı zincir; P137 gölün zincirleri yerde | doğru; L07 "gölün zincirleri çözülmüştü" E05'in "izin"iyle (I.209–213) tutarlı |
| "No light … darkness visible" | P004 ışıklı disk ve huzme | kısmi çelişki, bkz. 3.8 |
| Kalkan "ay gibi" + mızrak (I.284–294) | P049: yuvarlak, parlak, omuzda kalkan; direkten uzun mızrak | doğru |
| Pandemonium Dor sütunlu (I.713–717) | P052 yorumu "10 Dor sütunu, triglifli friz, altın tavan"; P053 sütunlu salon, taht (II.1) | doğru. Doğrulayamadığım: P052 kareyi tam boy bakmadım |
| Cehennem kapısı dokuz kat (II.645–646) | `kap.js` dokuz bant, üç pirinç / üç demir / üç elmas | kodda doğru, karede sayılamıyor (3.7b) |
| Günah ve Ölüm (II.648 vd.) | örtülü kadın + taçlı gölge (Ölüm "kingly crown", II.672–673) | doğru; Günah'ın alt gövdesi zayıf (3.7) |
| Uriel güneşte (III.621–622) | P063 güneş diski üstünde Uriel; yanında küçük genç melek (III.636) | doğru |
| Nifates Dağı (III.742, IV başı) | P064–P082 dağ tepesi, güneş | doğru |
| Karabatak hayat ağacında (IV.194–196) | P085, P088 (yüksek ağaç, karabatak); P086'da boynu uzun kuş heron gibi | P085/P088 doğru; P086'da karabatak/balıkçıl ayrımı doğrulayamadım |
| Kurbağa Havva'nın kulağında (IV.800), Ithuriel'in mızrağı (IV.810) | `adn.js:725–745` kurbağa, rüya dumanı, mızrak dokunuşu ile biçim geçişi | kodda doğru. Doğrulayamadığım: P091–P092'yi tam boy görmedim |
| Yedi gece dünyayı dolaşma (IX.63–66) | P096 gece yanı taralı küre, figür onu sarıyor | doğru |
| Yılana giriş (IX.182–190) | P097–P098: kıvrık yılan, siluet duman olup ağızdan giriyor | doğru ("in at his mouth") |
| Yılana dönüşüm (X.504–521), tıslama | P108–P110 yılan, tıslayan kalabalık; yüzüstü düşüş (X.513–514) | doğru |
| Küle dönen meyve (X.547–570) | P113 meyveli ağaç, beyaz noktalar; "meyve dağılır" | doğrulayamadım (orta karede meyve duruyor, kül anını görmedim) |
| XII sonu: el ele, "Bütün dünya önlerindeydi" | P115 iki figür yan yana, kapıda ring-alev | doğru (XII.646, 648). Gün doğumu notu 3.9 |
| Milton'un körlüğü ve yazdırması | P007 körlük, P009 kızı yazıyor, P010 kızlar okuyor | doğru; harfler İbranice/Yunanca/Latince tek harf (`oda.js:373`) |
| 1660'ta kitapların yakılması | P011–P012 meydan, cellat, saklanan şair | doğru |
| Blake'in cümlesi | P121 kitapta zincirli melekler / serbest şeytanlar; anlatım K07 (Blake "zincirliydi … özgür") | doğru |
| Lewis küçülme sırası, K11 basamak sayısı | P124 yedi basamak: kahraman, general, politikacı, casus, pencerede bakan, kurbağa, yılan | doğru |
| Cabanel: gözyaşı ve kollar | P132/P133 çapraz kollar, gözün üstü, kıvırcık saç; damla "süzülür" (damlayı t1380.89'da görmedim) | kollar doğru; gözyaşını doğrulayamadım (orta kare öncesi) |
| Kuzeydeki saray (V.756–761) | P022 Yunan tapınağı | yanlış, bkz. 3.2 |
| Tövbe sahnesinde Şeytan | P116 Şeytan kenarda | yanlış, bkz. 3.1 |
| Diz çökme (E15 ↔ J07) | P055 selam; P109 yılan | doğru |
| Âdem ve Havva çıplak | örtülü siluet | bilinçli sapma (3.9) |

## 7. Açıklama taslağı, `youtube.md` Kaynaklar (istenen 4. madde)

| Künye | Sonuç |
|---|---|
| John Milton, Paradise Lost (1667; on iki kitaplık ikinci baskı 1674) | doğru |
| William Blake, The Marriage of Heaven and Hell (1793 dolayları) | doğru; ekranla uyumlu hâle getirin (3.5) |
| C. S. Lewis, A Preface to Paradise Lost (1942) | doğru |
| Percy Bysshe Shelley, Prometheus Unbound, önsöz (1820) | doğru. Alıntı: "The only imaginary being resembling in any degree Prometheus, is Satan … exempt from the taints of ambition, envy, revenge" (L11 özeti uyuyor). Eser 1820'de yayımlandı, önsöz 1819 tarihli; "(1820)" kabul edilebilir |
| Alexandre Cabanel, Düşmüş Melek (L'Ange déchu, 1847), Musée Fabre, Montpellier | doğru |
| Doré, 1866 Kayıp Cennet gravürleri | doğru (Cassell, Londra, 1866) |

Bölüm zaman damgaları (`bolum_damga.py` çıktısı) `tools/plan_zaman.py` ile elle karşılaştırıldı, hepsi planların başlangıcıyla uyuşuyor: 0:56 (P008 56,86), 2:45 (P018 165,95), 4:57 (P030 297,03), 6:31 (P040 391,07), 9:32 (P056 572,38), 10:56 (P065 656,33), 14:09 (P083 849,09), 16:01 (P095 961,96), 17:37 (P104 1057,86), 19:34 (P115 1174,43), 20:21 (P119 1221,08), 22:44 (P131 1364,37). İlk damga 0:00. Açıklama gövdesi: "üç yüz elli yıl" (1667'den 2026'ya ≈ 359) kabul edilebilir yuvarlama; "Hangi yana kaçsam cehennem. Ben cehennemim." IV.75 ile uyumlu; açıklama künye iddiası için 3.3'e bak.

## 8. Önerilen düzeltmeler (sıralı)

1. P116: Şeytan'ı çıkar ya da ayrı çerçevede göster (3.1).
2. P022: sarayı "dağ üstünde dağ, kule ve piramit, altın kaya" silueti yap (3.2).
3. A01/G07: "KAYIP CENNET · IV. 75" künyesini ekle, açıklamayı "kimi dizelerin altında" diye yumuşat (3.3).
4. P013: "1667" yerine "1658–1663" ya da "yayım: 1667" (3.4).
5. P121: "1790–93" (3.5).
6. P004: A04 süresince ışık diskini kıs, huzmeyi E05'e ayır (3.8).
7. P028: "sayısız" ya da tırnağı kaldır (3.6).
8. P057: dokuz bandı tek karede okunur yap, Günah'ın gövdesini kalın yılan halkaları yap (3.7, 3.7b).

## 9. Doğrulayamadıklarım

- P052 (Pandemonium) ve P091–P092 (kurbağa ve mızrak) tam boy karelerini açıp bakmadım; yalnızca kodu ve özet sayfasını okudum.
- P113'te meyvenin küle dönüşü (X.563–570) sahnenin sonunda mı görülüyor; orta ve son sayfalarda net değil.
- P133'te gözyaşı damlasının görünüp görünmediği (t1380.89 karesinde yok; "damla süzülür" planın sonunda olabilir).
- Blake eserinin kesin tarihi (1790 / 1793); `notlar.md` 1790–93 diyor, ben web'den doğrulamadım.
- Lewis'in "Satan" bölümünün numarası (13); ekranda yok.
- Cabanel tablosunun Musée Fabre'a giriş yılı (1889); ekranda ve açıklamada yok.
- P086'daki kuşun karabatak mı balıkçıl mı okunduğu.
- Ses: kurul sesi dinleyemez; anlatımın "binlerce" mi "sayısız" mı dediğini `senaryo.json` metninden okudum (C11: "binlerce"), kaydı dinlemedim.
