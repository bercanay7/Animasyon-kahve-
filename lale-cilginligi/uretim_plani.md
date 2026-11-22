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

## Fable danışmaları
(henüz yok)
