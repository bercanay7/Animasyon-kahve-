# Lale Çılgınlığı: üretim planı

Başlangıç: 22 Kasım 2026. Seri: Tarihin Dönüm Noktaları. Konu seçimi: `analiz/2026-11-22-turkce-bosluk.md` (2. sıra), `analiz/2026-11-21-konu-adaylari-3.md`.
**Çalışma düzeni (kullanıcının kararı, 22 Kasım):** kurul, puanlama ve çok ajanlı akış yok; başkan tek başına yapar. Fable 5.2'ye yalnız emin olunmayan yerde bağımsız danışılır (aşağıda "Fable danışmaları"). Kredi harcayan her çağrıdan önce karakter × çekim hesabı kullanıcıya bildirilir ve onay alınır. Kaynak araştırmasında web sayfalarını okumak için okuma ajanları kullanıldı (kurul değil, sayfa okuma).
**Yayın tarihi:** kullanıcıyla kesinleşecek. Takvim kuralı haftada bir video, Cuma 18:00: Narkissos 27 Kasım, Dorian Gray 4 Aralık, yani ilk boş Cuma **11 Aralık 2026**.

## 1. Talep kontrolü (22 Kasım 2026)
`python3 araclar/talep/talep.py …` (Türkçe otomatik tamamlama + ilk 10 videonun izlenmeleri) ve `araclar/talep/iki_dil.py` (Türkçe/İngilizce boşluk). Medyan gürültülü.

| Sorgu | Öneri | İlk 10 en çok / medyan | Öne çıkan öneriler |
|---|---|---|---|
| lale çılgınlığı | 2 | 16,8 B / 198 | "lale final" (konu dışı) |
| **lale devri** | 14 | 34 M / 600 B | **dizi ve şarkı** ("Lale Devri 1. bölüm", Sibel Can) |
| lale devri osmanlı | 7 | 185 B / 31,6 B | osmanlı dönemi, animasyon, **11. sınıf** |
| lale devri nedir / tarihi | 3 / 4 | 185 B / 9–20 B | kısaca, dönemi, "tarihin arka odası" |
| lale | 14 | 24 M / 718 B | lale devri, şarkılar, kişiler |
| patrona halil | 14 | 154 B / 35 B | isyanı, **dizi**, ölümü, kimdir |
| nevşehirli ibrahim paşa | 2 | 0 | |
| iii ahmed | 4 | 152 B / 13 B | |
| tarihin ilk ekonomik krizi | 2 | 1,7 M / 193 B | ekonomik krizler tarihi |
| ekonomik kriz | 14 | 783 B / 47 B | türkiye, ne zaman bitecek |
| balon ekonomisi | 2 | 700 B / 35 B | |
| ekonomik balon / borsa balonu / yatırım balonu | 4 / 1 / 2 | ≤ 161 B / ≤ 2 B | konu dışı |
| kripto balon | 3 | 221 B / 7 B | konu dışı (eğitim, alım) |
| hollanda lale | 8 | 421 B / 1,7 B | bahçeler, festival, **hollanda lale borsası** |
| lale soğanı | 14 | 99 B / 2,8 B | nasıl dikilir (bahçe) |
| *kontrol:* sisifos / dönüşüm kafka | 14 / 14 | 9,0 M / 198 B; 1,0 M / 38 B | |

**İki dil** (`iki_dil.py`):

| TR / EN | TR en çok | TR medyan (Türkçe başlıklı) | EN en çok / medyan |
|---|---|---|---|
| lale çılgınlığı / tulip mania | **16,8 B** ("Tarihin İlk Finansal Balonu Lale Çılgınlığı Nedir?") | 89 | 1,5 M / **204 B** |
| lale balonu / tulip bubble | 16,8 B | 177 | 1,3 M / 265 B |
| lale devri / tulip era ottoman | 34 M (şarkı) | 292 B (dizi) | 101 B / 356 |

**Okuma:**
- **Boşluk doğrulandı:** İngilizcede ilk 10 medyanı ~204 B, Türkçede en çok izlenen 16,8 B, gerisi 1,7 B'nin altında. 21 Kasım taramasıyla aynı.
- **(a) Tanıdık kapı konunun kendisi değil, "lale":** "lale çılgınlığı" aranan bir söz değil (2 öneri). "Lale Devri"ni herkes okuldan tanıyor ("11. sınıf" önerisi), ama çıplak arama diziye ve şarkıya gidiyor. Bu yüzden başlıkta "Lale" sözcüğü önde olur, "Lale Devri" ise açıklamada, bölüm adında ve etiketlerde. "Tarihin ilk ekonomik krizi" sözü dolaşıyor (1,7 M): açıklamanın ilk satırına girer.
- **"balon", "kripto", "borsa" kapı değil:** aramaları konu dışına gidiyor. Bugünün yatırımcısına başlığın **soru** kısmı seslenir (b şartı), kapı kısmı değil. Kullanıcının kuralı: bugünden belirli bir varlık, kişi ya da kurum adı anılmaz.
- **(b) Kişisel soru doğal:** "Herkes alıyorsa sen de alır mısın?" gündelik bir yatırım konuşması; izleyici kendi hayatından tanıyor.

## 2. Başlık adayları (en az 10; beş soru)
**K**işisel soru mu · **N**efes · **Y**arı tahmin ettirir, ele vermez · **Ka**pı ("lale") içinde mi · **B**ağlamsız anlaşılır mı. Uzunluk ≤ 45 karakter (mobil akış). Dorian'ın kalıbı ("…Ne Yapardın?") ve Narkissos'unki ("Ne Zaman …?") tekrar edilmez.

| # | Aday | Kr. | K | N | Y | Ka | B | Not |
|---|---|---|---|---|---|---|---|---|
| 1 | Lale Çılgınlığı: Herkes Alıyorsa Alır mısın? | 44 | ✓✓ | ✓ | ✓ | ✓ | ✓ | Kapı önde, soru bugünkü yatırımcıya; şimdiki zaman (Dorian'ın "-ır mıydın"ından ayrı) |
| 2 | Bir Lale Soğanına Ev Verir miydin? | 34 | ✓✓ | ✓ | ✓ | ✓ | ✓ | En somut vaat (Alkmaar). Ama vaat yalnız fiyat; videonun yarısı (efsane, İstanbul) dışarıda kalıyor. Kalıp Dorian'a yakın ("Ne Yapardın?") |
| 3 | Lale Devri Gerçekten Yaşandı mı? | 32 | ✗ | ✓ | ✓ | ✓✓ | ✓ | Okuldaki bilgiyi sarsan güçlü merak, ama bilgi merakı (İkaros'un zayıflığı); "Lale Devri" araması diziye gidiyor; revizyonist tık tuzağı gibi okunabilir |
| 4 | Tarihin İlk Balonu Hiç Patlamadı mı? | 35 | ✗ | ✓ | ✓ | ~ | ✓ | Yanlış: fiyat gerçekten çöktü; yanıltır |
| 5 | Balonu Fiyat mı Büyütür, Hikâye mi? \| Lale | 42 | ~ | ✓ | ~ | ✓ | ~ | Videonun iksiri; başlık için soyut |
| 6 | Bir Çiçek İçin Her Şeyini Satar mıydın? | 39 | ✓ | ✓ | ✓ | ✗ | ✓ | Kapı yok; "satmak" vaadi Mackay'in efsanesine yaslanıyor, video onu çürütüyor |
| 7 | Lale Çılgınlığı: Sen de Alır mıydın? | 36 | ✓ | ✓ | ~ | ✓ | ~ | 1'in kısa hâli; "herkes" düşünce soru bağlamsız kalıyor |
| 8 | Lale Soğanı Neden Ev Fiyatına Satıldı? | 38 | ✗ | ✓ | ✓ | ✓ | ✓ | Bilgi merakı; cevabı tek cümle |
| 9 | Hollanda'yı Çıldırtan Lale İstanbul'dan Gitti | 44 | ✗ | ✓ | ~ | ✓ | ✓ | Türkiye bağı güçlü, kişisel soru yok |
| 10 | Komşun Zengin Oluyorsa Sen de Alır mısın? | 41 | ✓✓ | ✓ | ~ | ✗ | ✓ | Güçlü kişisel soru, ama kapı yok; konu başlıktan okunmuyor |
| 11 | İki Lale Çılgınlığı, İki Efsane | 31 | ✗ | ✓ | ~ | ✓ | ~ | Omurga fikri; izleyiciye soru sormuyor |
| 12 | Herkes Aldı, Sonra Ne Oldu? \| Lale Çılgınlığı | 44 | ~ | ✓ | ✓ | ✓ | ✓ | Sonucu merak ettiriyor ama kişisel değil; "sonra ne oldu" sık kullanılan kalıp |

**Başkanın seçimi: 1. aday, "Lale Çılgınlığı: Herkes Alıyorsa Alır mısın?"** (44 karakter).
- Kapı sözcüğü ("Lale") en önde; konu adı tam olarak arandığında da çıkar.
- Soru izleyicinin bugününe soruluyor ve gündelik bir yatırım konuşmasının diliyle tanıdık.
- Cevabı yarı tahmin ettiriyor ("almamalısın" gibi görünür), ama videonun asıl dönüşünü vermiyor: "herkes alıyor" sözü de bir hikâyedir.
- Videonun ilk ve son cümlesi bu soru.
- **Yedek ve kapak vaadi:** 2. aday ("Bir Lale Soğanına Ev Verir miydin?") kapak A'nın vaadi olarak yaşar.

## 3. Kapak taslakları (iki ayrı vaat, iki ayrı kompozisyon)
Kural: filmde renk yalnız lalede (§6). Kapakta da tek renk lale, geri kalanı gravür.
- **A, "karşıtlık" (değer farkı): BİR SOĞAN, BİR EV.** Gravür bir terazi: bir kefede küçük, renkli tek lale soğanı (üstünde alevli yaprakları açılmış çiçek), öbür kefede koca bir Hollanda kanal evi; terazi soğana doğru eğik. Tek odak: renkli lale (karenin en parlak ve tek renkli yeri). Yazı 3 kelime: "BİR EV FİYATINA". Vaat: absürt değer. Film ilk saniyede bu teraziyle açılır.
- **B, "hareket oku" (sonuç gizli): HERKES ALIYORDU.** Meyhane mezadı: karanlıkta yukarı uzanan onlarca el (gravür, sırtlar), hepsinin hedefi masanın üstündeki tek renkli lale; lalenin sapından tavana doğru kırık bir fiyat çizgisi gibi yükselen bir ok, ucu kadraj dışında. Yazı 2 kelime: "HERKES ALIYORDU". Vaat: sürünün içinde olmak, sonucun ne olduğu. Film 0:15 civarında mezat salonuyla karşılar.
- Hassasiyet: kaldırılmış düz kollar selam gibi okunur (Mary Stuart dersi): eller dirsekten kırık, avuç açık, farklı yüksekliklerde. Dinî simge yok (Kalvinist vaaz, cami içi). Yazı: "ALIYORDU" argo çağrışımı yok. "ÇILGINLIK" kapakta tek başına kullanılmaz (ruh sağlığı damgası gibi okunabilir).

## 4. İskelet (22 Kasım; senaryodan önce)
**Seçim: Kahramanın Yolculuğu, kahraman lale** (gidiş ve dönüş). Önceki videolar: Mary Stuart Kahramanın Yolculuğu, Narkissos Kişōtenketsu, **Dorian Gray Harmon çemberi** (art arda aynı iskelet yok).
**Gerekçe:** konu kolektif bir tarih; tek bir insan kahramanı yok. Lale, kanalın "kurye" fikrinin kendisi: İstanbul'dan çıkar, Hollanda'da sınanır, yüz yıl sonra İstanbul'a döner ve iki şehirden de aynı soruyu getirir. İnsanlar her durakta değişir; bu yüzden her bölümün tek bir insan yüzü olur (Medici dersi: ad yükü). Kalıba uymayan aşama zorlanmaz.

**Ad yükü:** seste anılan kişiler Mackay, Goldgar, III. Ahmed, İbrahim Paşa, Patrona Halil, Ahmed Refik. Busbecq, Clusius ve Wouter Winkel yalnız ekran etiketinde ("bir elçi", "bir botanikçi", "bir meyhaneci"). Doruğu taşıyan İbrahim Paşa ve Patrona Halil kancada adıyla ve görüntüsüyle ekilir (Ran dersi).

| Adım | İçerik | Kaynak |
|---|---|---|
| **0. Kanca** (0–~30 sn) | Terazi: bir lale soğanı, bir ev. İlk cümle başlığın sorusu. Alkmaar, 5 Şubat 1637: ölen bir meyhanecinin yedi yetim çocuğu için mezat; tek soğan 5.200 gulden. İkiz hikâye ekilir: 90 yıl sonra İstanbul'da aynı çiçek, bir sadrazam (İbrahim Paşa), bir isyancı (Patrona Halil). Somut vaat: ikisinin de bildiğimiz sonu sonradan yazıldı | Dash 1999 bölüm 12; "Lijste van eenighe tulpaen…" (1637) |
| **1. Sıradan dünya** | Edirne–İstanbul yolu, kış: bir Habsburg elçisi yol kenarında çiçekler görür, Türkler bunlara "tulipan" diyor diye yazar; Türkler güzel bir çiçeğe akçe vermekten çekinmez. Ad karışıklığı (tülbent) tek cümle | Busbecq, 1. mektup (1581) |
| **2. Çağrı ve eşik** | Lale Leiden'e gider (1593, bir botanikçi); bahçesinden soğanlar çalınır, lale Hollanda'ya yayılır. En pahalısı alevli yapraklı "kırık" laleler: aslında hastaydılar (virüs; o gün kimse bilmiyordu). Semper Augustus: yalnız bir düzine var, sahibi satmıyor | Leiden Üniv.; Wassenaer 1624–25 |
| **3. Sınavlar** | 1636–37 kışı: soğanlar toprakta, satılan bir kâğıt; meyhanelerde ticaret; dokumacılar, fırıncılar giriyor; ucuz bir çeşidin fiyatı bir ayda 12 kat. Kancaya dönüş: Alkmaar mezadı, kâğıt üstünde 90.000 gulden | Goldgar 2007; Samenspraeck 1637; Dash |
| **4. Büyük sınav** | Şubat 1637: bir satışta kimse el kaldırmaz; alıcılar kaybolur. Para haziranda, soğanlar topraktan çıkınca ödenecekti. Mahkemeler karışmaz; 1638'de Haarlem'de anlaşma: fiyatın %3,5'i | Samenspraeck; Posthumus; Haarlem kararları 1638 |
| **5. Bedel (ve ilk kırılma: efsane 1)** | 1637 broşürleri: dokumacı tezgâhını satar (satirik diyalog). 1841 Mackay: soğanı soğan sanıp yiyen denizci, "ülke ticareti yıllarca toparlanamadı". Goldgar arşive bakar: iflas bulamaz; ekonomi büyümeyi sürdürür. Fiyat gerçekten uçtu; yıkım hikâyesi sonradan büyüdü (tek cümle) | Mackay 1841 (kaynak/); Goldgar 2007 |
| **6. Dönüş** | Lale eve döner: İstanbul, III. Ahmed ve İbrahim Paşa (1718). Lale bahçeleri, çırağan geceleri (kaplumbağa sırtında mum: "anlatılır"). Fiyatlar artar; Hollanda'nın mahkemesi karışmamıştı, İstanbul'da devlet karışır: 1722 fermanı, laleye narh | TDV "Lâle Devri", "Lâle"; Ahmed Refik, *İstanbul Hayatı*; Aktepe 1954 |
| **7. Sınav ve kırılma (efsane 2)** | 1730: İran cephesi, yeni vergiler; Patrona Halil'in ayaklanması; İbrahim Paşa öldürülür (gösterilmez), III. Ahmed tahtı bırakır, bahçeler ve köşkler yıkılır. Sonra ad: 18. yüzyıl kroniklerinde "Lale Devri" yok; adı 1913'te Ahmed Refik (ve Yahya Kemal) koyar; bugün tarihçiler sefahat anlatısını abartı, 1730'u iktidar kavgası sayar | TDV; Karahasanoğlu 2025 (*Lale Devri Mi?*), Kafadar 1993 |
| **8. İksir ve bitiş** | İki çılgınlık da bir fiyatla başladı, ama bildiğimiz hâline iki yüz yıl sonra yazılan bir hikâyeyle geldi. Soru izleyiciye: herkes alıyorsa sen de alır mısın? Ve "herkes alıyor" sözünü sana kim anlatıyor? Abone çağrısı son anın içinde; bitiş ekranı | |

**Açık merak döngüleri (soru → cevabı olan olay):**
1. Kanca: "Bir soğan neden bir ev fiyatına?" → 2–3: kırık lale, kıtlık, kâğıt üstünde ticaret, meyhane.
2. Kanca: "O para ödendi mi?" (kâğıt üstünde 90.000) → 4: haziranda alıcılar gelmez, 1638'de %3,5. Alkmaar'daki paranın ne kadar ödendiği bilinmiyor; anlatım bunu söyler.
3. 2: "En pahalı laleler neden alevliydi?" → 2 sonu: hastalık (görünür vaat: renk yapraklarda bir alev gibi).
4. 5: "Hollanda gerçekten battı mı?" → 5: Goldgar'ın arşivi (olay: aranır, bulunamaz).
5. Kanca: İbrahim Paşa ve Patrona Halil → 6–7.
6. 7: "Bu döneme neden Lale Devri deriz?" → 7: 1913, bir gazete tefrikası.

**Uygulanacak dersler:** kancadan hikâyeye köprü sıfır cümle (kanca sorusundan sonraki ilk cümle Busbecq'in yolu); hikâye ~0:35'te başlar (kural ≤ 0:45). Kavram anlatımı yok: "vadeli sözleşme" sözcüğü kullanılmaz, kâğıt görüntüsüyle anlatılır. Karşılaştırma olaydan sonra tek cümle (§5 ve §7 sonu). Hikâye bitince yorum uzatılmaz.

## 5. Kaynak ilk bulguları (ayrıntı `kaynak/DOGRULAMA.md`'de)
- **Alkmaar, 5 Şubat 1637:** Alkmaar'daki Oude Schutters-Doelen'in meyhanecisi Wouter Bartelmiesz. Winckel'in mirası; yedi çocuk yetimhaneye alınır; Admirael van Enkhuizen (yavrusuyla) özel satışta 5.200 gulden; en pahalı mezat kalemi 658 asen'lik bir Viceroy 4.203; toplam 90.000 gulden (Dash 1999, bölüm 12; 1637 broşürü *Lijste van eenighe tulpaen…*, STCN). Sözleşmeler haziranda teslim ve ödemelikti.
- **Ölçü:** bir marangozun yıllık kazancı ~250 gulden; 1.000 gulden Haarlem'de küçük bir ev (Grout, *Encyclopaedia Romana*, Posthumus ve Goldgar'a dayanarak).
- **Switsers:** 31 Aralık 1636'da pound başına 125, 1 Şubat 1637'de 1.500 gulden (Goldgar'dan aktaran Grout).
- **Goldgar:** "I couldn't find anybody that went bankrupt" (Smithsonian, 2017); mahkemeler sözleşmeleri zorla uygulamadı.
- **Mackay 1841:** denizci ve ringa balığı hikâyesi (kaynağı Blainville'in seyahatnamesi), "yıllarca toparlanamadı" sözü (`kaynak/mackay_1841_tulipomania.txt`).
- **Osmanlı:** narh fermanı Ekim 1722 (TDV, Özcan; Ahmed Refik, *İstanbul Hayatı*, s. 94–95); 239 adlık narh listesi (Aktepe 1954). İbrahim Paşa 1 Ekim 1730'da öldürüldü (TDV, Aktepe). "Lâle Devri" adı 18. yüzyıl kroniklerinde yok; ilk Yahya Kemal kullandı, Ahmed Refik 1913 İkdam tefrikası ve 1915 kitabıyla yaydı (TDV); Karahasanoğlu 2025: "Lale Devri hiç yaşanmamıştır" (giriş; editörün tezi).

## 6. Üslup (22 Kasım; başkan)
**İnceleme sırası (CLAUDE.md):** kendi motorlarımız → cinecode → Lemo.
- **Kendi motorlarımız:** gravür (`milton/lib`, Dorian'da karma üslupla yeniden kullanıldı), vazo, kâğıt kesme, Python. Konuya uyan gravür: 1637 Haarlem broşürleri ve dönemin hicivli baskıları (Crispijn van de Passe, *Floraes Mallewagen*, 1637) gravürdür; 1630'ların lale kitapları ise elle boyanmış suluboyadır. Botanik baskılar (Hortus Eystettensis, 1613) bakır gravür + el boyamasıdır. Yani "gravür dünya + boyalı lale" dönemin kendi baskı dili.
- **cinecode:** `watercolor` (bitkisel levha + not dili; bütün film suluboya olursa kalabalık, meyhane, mezat ve İstanbul gecesi zayıf kalır: figür ve iç mekân suluboyanın zayıf yanı), `engraving` (bizim motorumuzun akrabası), `ukiyoe` ve `stained-glass` (konuya yabancı; vitray dinî çağrışım).
- **Lemo** (`KATALOG.md`): `vintage-collage` (eski gravürlerden kolaj; Dorian'da şakacı dili yüzünden elenmişti, burada da ton fazla hafif), `gilded-illumination` (Hristiyan el yazması çağrışımı; Osmanlı minyatürüne benzetilmez kuralı), `watercolor` ve `impasto` (uzun film için yavaş: 5–10 sn/kare).
- **Elenen:** bütün film suluboya (figür/kalabalık zayıf, iki şehir aynı yumuşak dile düşer); minyatür taklidi (Levnî'yi kodla taklit etmek hem zayıf olur hem bir geleneği karikatürleştirme riski taşır).

**Seçim: gravür dünya + yalnız lalede el boyaması** (kullanıcının önerisi, kaynakla da destekleniyor).
1. **Fikir görüntünün kuralı:** renk = değer. Fiyat yükseldikçe sahnelerde boyalı lale çoğalır; Şubat 1637'de renk çiçeklerden çekilir (gravür kalır). İstanbul'da da aynı: narh defterinde renk, 1730'da bahçeler yıkılınca söner. Sonda Mackay'in ve Ahmed Refik'in sayfalarında lale yeniden boyanır: hikâye rengi geri getirir (iksir görüntüsü).
2. **Dönem dili:** gravür + el boyaması 1600'lerin botanik baskısının kendisi; filme gerçek görseller (1637 broşürleri, lale kitabı sayfaları) dikişsiz girer.
3. **Maliyet:** `lib/lale.js` gravür geçişinde çiçeği çizer, basmadan sonra yaprakları çarpma (multiply) karışımıyla suluboya gibi boyar (granül dokusu, kenar birikmesi, 2 px kayık boya). Kapı karelerinde 0,35–0,65 sn/kare (tek işçi), Dorian'ın portresiz planlarıyla aynı; WebGL yok.
4. **Dorian'dan ayrışma:** Dorian'da renk yağlıboya ve tek bir nesnede (portre) karanlık iç mekânda; burada suluboya, çok sayıda küçük nesne, gündüz dış mekân (tarla) ve İstanbul gecesi. Yine de iki gravür filmi art arda (4 ve 11 Aralık): fark kapakta da korunur (Dorian kapakları koyu oda, bu filmin kapakları açık kâğıt + renkli lale).

**Kapı (manzara + orta plan figür + yakın + 15 sn hareket + İstanbul gecesi; `kapi/`):**
- Manzara: Haarlem dışı lale tarlası, ufukta alçak kasaba ve değirmen (kilise kulesi yok). Gökyüzü temiz kâğıt.
- Orta plan: Alkmaar mezadı; mezatçı ve kâtip masada, ışıkta tek boyalı lale (Admirael van Enkhuizen), sırtı dönük alıcılar 1630'lar giysisiyle (geniş kenarlı şapka, düz beyaz yaka, pelerin). Teklif eli dirsekten kırık, avuç yukarı (düz kalkık kol selam okunur: Mary Stuart dersi).
- Yakın: tek Semper Augustus, beyaz zemin + lal alevler.
- 15 sn: tarlaya el boyaması iner (0–2,5 sn), kamera tarlaya yaklaşır; terazi: soğan bir evden ağır basar, sonra renk söner.
- İstanbul gecesi: köşk, serviler, badem gövdeli hançer uçlu İstanbul laleleri, kandiller, sırtında mum taşıyan kaplumbağa.
- İlk taslakta bulunup düzeltilenler: yaprakları kopuk ve alevleri zemini boğan çiçek (yumurta çanak, ince alev diline çevrildi); gökdelen gibi okunan evler (ufukta alçak, koyu siluet); yatay uzanan kollar (silah/selam okunuyordu); gaga gibi okunan şapka siperliği.
- Açık kalan: tarlanın toprak çizgileri ağır; uzak ağaçlar; figürlerin bacakları pelerin altında iki çubuk. Üretimde düzeltilir.

## 7. Tempo kontrolü (seslendirmeden önce; `tempo_kontrol.py`, rev2)
Art arda soyut dizi yok; köprü adayı yok. Kanca 596 karakter (≈ 44 sn; hikâye B01'de ~0:45, sınırda: seslendirmeden sonra ölçülür).

| Cümle | Bayrak | Karar |
|---|---|---|
| A02, A07 | T | A02 → A05 (ev: olay, Alkmaar fiyatı); A07 "adı kim koydu?" → I03 (olay: 1913 gazete tefrikası) |
| B02 | E (göre) | **olay**: "yazdığına göre" yalnız atıf; çiçek sunulması sahne |
| B03 | (rev1'de E) | **olay/nesne**: ad karışıklığı sarığa takılı lale görüntüsüyle verilir; tek cümle |
| C03 | (rev1'de E) | **olay**: "alevler bir virüsün izi" görünür vaadin cevabı (C01–C02'nin merakı); tek cümle |
| E01 | M (göre) | **olay**: "anlatıldığına göre" atıf |
| F04, F08 | Y, A | **olay**: yazar bir şey yapıyor (kitap yazıyor; arşive dönüyor) |
| F06 | M | **olay**: Mackay'in somut iddiaları (bacacılar; ticaret) |
| F11 | (karşılaştırma) | **soyut**, olaydan sonra tek cümle |
| G03 | M | **olay**: kandiller, kaplumbağa ("anlatılanlara göre") |
| G06 | M | **olay + tek karşılaştırma** (Hollanda'da mahkeme karışmamıştı) |
| I04–I05 | Y | **olay**: Ahmed Refik'in rakamı ve arşivin cevabı (efsane 2'nin somut kanıtı) |
| I06 | Y | **soyut** (anlatının özeti); ardından I07 olay (kitap, cümle) |
| I08 | M | **soyut**; I06 ile arasında olay var (art arda değil) |
| J02 | Y | **soyut**, tek karşılaştırma; J03 somut dönüş (meyhane) |
| J04, J05 | T | başlığın sorusu ve iksir |

**İkinci yarıda yeni adlar:** Mackay (F04), Goldgar (F08), Ahmed Refik ve Yahya Kemal (I03), Karahasanoğlu (I07). Doruğu taşıyan İbrahim Paşa ve Patrona Halil kancada (A06) ekildi. Ahmed Refik kancada adıyla ekilmez (cevabı ele verir); A07'nin görüntüsünde bir gazete sayfası ekilir. I. Mahmud, İkdam, Busbecq, Clusius, Winkel, Aktepe yalnız ekran etiketinde.

## Fable danışmaları
1. **Senaryo rev1, seslendirmeden önce (22 Kasım).** Neden: seslendirme kredi harcayan ve geri dönülmesi pahalı adım; Mary Stuart ve Dorian'da Fable bu kapıda engelleyici bulgu getirmişti. Tek tur, puansız bulgu listesi. Bulgular başkanca kaynakla tartıldı:
   - **Uygulananlar:** I07 bağlamı ("kışkırtıcı bir cümle") ve I08 açıklaması (laleler de köşkler de vardı; ayrı bir sefahat çağı anlatısı sonradan kuruldu: Karahasanoğlu s. 11–12); **I06 Ahmed Refik'in rolü düzeltildi**: dönemi kınamadı, "zevk ve yenilik çağı" olarak anlattı (Karahasanoğlu s. 11: İbrahim Paşa'nın "en keyif alacağı eser" Refik'in kitabı; Erimtan tanıtımı); "sefahate karşı halk öfkesi" ders kitabı anlatısı; J02 "birer kitap"; H05 ve A06 yıkım ifadesi yumuşatıldı (kapsam tartışmalı); F09–F11 Goldgar tam aktarıldı (kriz paranın değil tutulmayan sözlerin krizi; "adını saptayabildiği" kişiler); D05 "yalnız zenginler yok" (Mackay çizgisi) kaldırıldı; F04 Mackay broşürleri değil onlara dayanan kitapları kullandı (Beckmann); **A05 kapak A'nın "ev" vaadi karşılandı** (1.000 gulden = Haarlem'de küçük ev → beş küçük ev); B02 "yazdığına göre"; A06 "Nevşehirli Damat" (Pargalı ile karışmasın); kanca kısaldı; B01 "Önce seksen yıl geriye" (zaman zikzağı); I01 ve J01 çıkarıldı; E03 uzlaşma önerisi tutmadı; G02 Kâğıthane/Boğaz; G06 tarih ekrana, seste "1726 yazında"; G08 "üç yüz yevmiyeye yakın"; H04 I. Mahmud etikete; I03 İkdam etikete; okunuşlar ("En Goldgar", "Mıkay", "Ekim'in ilk gecesi", "Nizeyi Rummani", "Svitsers", "Saadabad", yıllar yazıyla); F07, J03, J05 dil.
   - **Reddedilen:** F05'e "güya" (Mackay hikâyeyi olgu diye anlatır; izleyici bunun efsane olduğunu F08–F11'de öğrenir, önceden ele vermek merakı bozar). A05'teki marangoz ölçüsü korunmadı (kanca süresi); D08'deki zanaatkâr ölçüsü yeterli.
