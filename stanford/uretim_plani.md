# Stanford Hapishane Deneyi, 1971: üretim planı

Başlangıç: 25 Kasım 2026. Yön usulüyle (`analiz/2026-11-23-deney-yon-promptu.md`, dördüncü yön videosu).
- Yön: bu oturumun ilk mesajı (Fable'ın yön metni, kullanıcının gönderdiği hâliyle).
- Malzeme dosyaları bağlayıcı değil: `analiz/2026-11-25-stanford-yon-notlari.md`, `2026-11-25-konu-adaylari-4.md`.

**Yön (özet):**
- İki dogma yok: "üniforma insanı zalimleştirir" de değil, "deney sahteydi, insan iyidir" de değil.
- Soru izleyicinin: gardiyan olsan zalim olur muydun?
- Peşinden gidilecek: gardiyanlar kendiliğinden mi sertleşti, biri mi istedi?
- Cevap kavramla değil, bantla.
- Sonra iki adam: biri istenenin ötesine geçip "rol yapıyordum" dedi, öteki istendiği hâlde yapmadı.
- Zimbardo da onu çürüten de kendi belgesiyle konuşur; hüküm yok.
- Çıkış sorusu: "biri iyi bir amaç uğruna benden sertlik istediğinde ne derim?"

**Kullanıcının fikrini sorma adımı (iş akışı 2):** yön metni bu adımın yazılı hâli; kullanıcı "kararlar senin" dedi. Ayrıca sorulmadı.

**Takvim:** 18 Aralık 2026, 18:00 (öneri; takvim kullanıcının). Çernobil 14 Aralık'ta. Oynatma listesi: Tarihin Dönüm Noktaları.

**Araştırma (kullanıcının isteği, senaryodan önce):**
- `arastirma/kanca_kaynaklari.md`: dış kaynaklar.
- `arastirma/kanal_karsilastirma.md`: kanal verisiyle karşılaştırma ve karar.
- Bu videoya getirdiği iki şey:
  - (1) sorudan sonra ikinci kanca, yani bandın kendisi;
  - (2) bant kancada görünür, içeriği söylenmez.

## 1. Talep kontrolü (25 Kasım; `araclar/talep/talep.py`)
| Sorgu | Öneri | İlk 10 medyan | En çok | Not |
|---|---|---|---|---|
| **stanford deneyi** | 4 | **130,8 B** | 17 M | kapı; "fragman" ve "film" önerileri 2015 filminden |
| stanford hapishane deneyi | 5 | 47,7 B | 1,4 M | "evrim ağacı" önerisi: klasik anlatım |
| zimbardo | 14 | 68,7 B | 3 M | "zimbardo kırık cam deneyi", "tedx" |
| hapishane deneyi | 6 | 31,1 B | 10,1 M | |
| gardiyan deneyi | 3 | 2,1 B | 1,3 M | zayıf |
| *kontrol:* sisifos | 14 | 68,6 B | 9 M | |

**Okuma:**
- (a) Kapı güçlü: "stanford deneyi" medyanı Sisifos'un iki katı. Kapı kelimesi "Stanford" başlıkta ilk sözcük.
- (b) Türkçede çürütme yok; arşivin bozduğu taraf anlatılmamış (konu taraması 4).

## 2. Başlık adayları
Eleme ölçütleri:
- **K:** kişisel soru
- **N:** tek nefeste okunuyor
- **Y:** yarı tahmin ettirir, ele vermez
- **Ka:** kapı kelimesi önde
- **B:** bağlamsız anlaşılır

| # | Aday | Kr. | K | N | Y | Ka | B | Not |
|---|---|---|---|---|---|---|---|---|
| 1 | **Stanford: Gardiyan Olsan Zalim Olur muydun?** | 43 | ✓ | ✓ | ✓ | ✓ | ✓ | Yönün sorusu; "Ad: soru?" kalıbı Çernobil'in iki noktasız kalıbından farklı |
| 2 | Stanford Deneyi: Sertliği Biri mi İstedi? | 41 | ✗ | ✓ | ~ | ✓ | ✓ | Cevabın yarısını veriyor ("biri istedi") |
| 3 | Stanford Deneyi: Gardiyanlara Ne Söylendi? | 42 | ✗ | ✓ | ✓ | ✓ | ✓ | Kapak B'nin vaadi; kişisel değil |
| 4 | Stanford Deneyi: Bantta Ne İstendi? | 35 | ✗ | ✓ | ✓ | ✓ | ✗ | "Bant" bağlamsız anlaşılmıyor |
| 5 | Stanford: Senden Sertlik İstense Ne Dersin? | 43 | ✓ | ✓ | ✗ | ✓ | ~ | Çıkış sorusu; başta söylenirse filmin dönüşünü ele verir |
| 6 | Stanford Deneyi Yalan mıydı? Bant Ne Diyor | 42 | ✗ | ✗ | ✓ | ✓ | ✓ | "Yalan" kesin hüküm imasına kayar (yön notu, hukuk) |
| 7 | Stanford Deneyinin Saklanan Bandı | 33 | ✗ | ✓ | ✓ | ✓ | ✓ | "Saklanan" doğru değil: bant arşivdeydi, saklanmadı |
| 8 | Stanford Deneyi: Zalimliği Biri mi İstedi? | 42 | ✗ | ✓ | ~ | ✓ | ✓ | "Zalimlik istendi" bandın söylediğinden fazlası ("sert" istendi) |
| 9 | Gardiyan Olsan Zalim Olur muydun? | 33 | ✓ | ✓ | ✓ | ✗ | ~ | Kapı kelimesi yok |
| 10 | Stanford Bodrumunda Gardiyana Ne Söylendi? | 42 | ✗ | ✓ | ✓ | ✓ | ✓ | Belgesel başlığı |
| 11 | Stanford Deneyi: İyi Bir Amaç İçin Sert Olur musun? | 51 | ✓ | ✗ | ✗ | ✓ | ~ | Uzun; cevabı veriyor |

**Seçim: 1 (43 karakter).**
- Kalıp: Çernobil'de iki noktasız tek soruydu ("Çernobil'in Çayını Sen İçer miydin?"); bu kez "Ad: soru?".
- Kapı kelimesi ilk sözcük.
- Vaat "evet ya da hayır"; senaryo bunu bodrumdaki iki gardiyan ve "üçte bir ↔ üçte iki" okumasıyla karşılar, tek cevap vermez.
- **Yedek:** 3.

## 3. Kapaklar (iki ayrı vaat)
- **A "YAZI TURAYLA SEÇİLDİ"**
  - Görsel: monitör görüntüsünde (siyah-beyaz, tarama çizgili) ¾ duran bir gardiyan, aynalı gözlüğünde koridorun ışığı. Tek vurgu: gözlükteki parıltı.
  - Vaat: "sıradan biri; sen de olabilirdin". A01–A02'de (ilk 10 sn) karşılanır: aynı figür, sayımda kenarda; "yazı turayla gardiyan olmuş bir öğrenci".
- **B "18 DAKİKALIK BANT"**
  - Görsel: kâğıt dünyada makaralı teyp, kırmızı kayıt lambası tek renk.
  - Vaat: "bantta ne var?" A03'te (≈0:15) bant görünür; III. bölümde çalar.
- Kapak yazıları başlığın sözcüklerini (gardiyan, zalim, olsan) tekrar etmez.
- **Hassasiyet:**
  - gardiyan Türk polisi ya da askeri gibi okunmamalı (gömlek, cop, aynalı gözlük; şapka ve rütbe yok);
  - "yalan", "sahte" sözcükleri kapakta yok.

## 4. Üslup: gözetim monitörü ve belge (başkanın seçimi)
**Neden:** filmin cevabı bir kayıt. Deneyin kendisi de kameralarla ve teyplerle izlendi; Zimbardo'nun "iyi gardiyan / kötü gardiyan" okuması o kayıtlara dayanıyor. Bodrumu kendi kayıt cihazlarının gözünden göstermek, sonra o cihazların başında oturanları göstermek yönün sorusunu görüntüye çeviriyor: gözlemci gerçekten yalnız gözlemci miydi?
- **Kural 1: bodrum yalnız monitörde.** Hücreler, koridor, sayım, isyan siyah-beyaz bir 1971 kapalı devre monitöründe görünür: tarama çizgisi, yumuşak yatay bulanıklık, ışıma, gren. Kamera sabit gözlem yerindedir: koridorun ucu, hafif yüksek.
- **Kural 2: gözlemciler III. bölüme kadar görünmez.** Müdür ve amir yalnız kapıdaki levhayla ("WARDEN", "SUPERINTENDENT") ve sesle vardır. Bant çaldığında görüntü ilk kez döner (ters açı): monitörün önündeki masa, makaralı teyp, iki sandalye.
- **Kural 3: renk yalnız kayıtta ve belgede.** Belgeler sıcak kâğıtta, daktilo harfiyle. Teybin kehribar ışığı ve kırmızı kayıt lambası filmin tek renkleri.
- **Kişiler siluet ve numara.** Yüz yok (yaşayan kişiler: Eshelman, Mark, Jaffe, Maslach, Ramsay). Gardiyanlarda tek yüz öğesi aynalı gözlüğün parıltısı.
- **Motor (`lib/ekran.js`):**
  - Çernobil'in üç plakalı mimarisi korunarak yeni bir gölgelendirici yazıldı: `mod: 'video'` monitör, `mod: 'kagit'` belge.
  - Kâğıt sahnenin içindeki monitör, renk plakasının mavi kanalıyla maskelenir.
  - Çekim sistemi `film.js`, figür kütüphanesi ve araçlar Çernobil'den.
  - Figüre gardiyan, mahkûm, araştırmacı ve müdür tipleri eklendi.
- **Sesler ve sözler:**
  - Arşiv sesi çalınmaz (telif; Stanford SC0750 "All Rights Reserved").
  - Bant konuşması ekranda daktilo dökümü olarak satır satır basılır, Türkçesi bizim; anlatıcı okur.

## 5. İskelet: Kişōtenketsu, kahraman isteksiz gardiyan
**Seçim gerekçesi:**
- Önceki video (Çernobil) Harmon çemberiydi.
- Bu filmin yapısı bir dönüşe dayanıyor: herkesin bildiği hikâye anlatılır, sonra arşivden beklenmedik bir bilgi gelir.
- Kişōtenketsu'da çatışma şart değil; "ten" (dönüş) bant.
- Frankenstein (iki video önce) iç içe çerçeve + Kişōtenketsu'ydu. Süs değişiyor: soruşturma.

**Kişiler:**
- **Kahraman:** John Mark. Sayımda kenarda duran, mahkûm olmak isteyen gündüz gardiyanı.
  - A01'de adsız ekilir, C01'de yeniden görünür, D'de adıyla konuşur, E ve F'de doruğu taşır.
- **Karşıt:** bir kişi değil, istek. "İyi bir amaç için sertlik."
- **Doruğu taşıyan ikinci kişi:** Eshelman. C05–C07'de eylemle ekilir.
- **Mekân:** tek (bodrum ve onun ucundaki gözlem masası).

| Aşama | İçerik | Cümleler (rev1) |
|---|---|---|
| Kanca | sayımdaki gardiyan ve soru; kimlik + bant (ikinci kanca); soruşturma sorusu | A01–A03 |
| Ki (giriş) | ilan, yazı tura, Zimbardo'nun yönlendirmesi, polis, numaralar, gözlük, levhalar, kayıt | B01–B10 |
| Shō (gelişme) | altı gün: gülüşme ve isyan, dolap, akşam vardiyası (Le Texier ↔ Zimbardo; Eshelman ekilir), 416, Maslach, son; 1973 sonucu ↔ Fromm; bilinen anlatım | C01–C13 |
| Ten (dönüş) | bant: müdür ve Mark (VTT zaman damgalarıyla); müdürün görevi ve yurt deneyi; Zimbardo 2018 ↔ Le Texier; Zimbardo'nun savunmasıyla kapanış | D01–D19 |
| Ketsu (birleştirme) | Eshelman: 1971, 2011, 2018, Zimbardo 2018, 2024 (ölümden sonra); Mark: 2011, belge yokluğu; "hiçbiri araya girmedi" ve vardiya ayrımı | E01–E14 |
| Son | müdürün "iyi bir amaç" cümlesi; bandın sonu: "Peki."; çıkış sorusu; çağrı | F01–F05 |

**Merak döngüleri (rev1):**
1. **L1** "zalim olur muydun?" (A01) → C11–C12 (üçte bir ↔ üçte iki) → E13–E14 → F04 ("bilemezsin; ama ne diyeceğini düşünebilirsin").
2. **L2** "bantta ne isteniyor?" (A02, kapak B) → D04–D14.
3. **L3** "kendiliğinden mi, biri mi istedi?" (A03) → D05–D14 (istendi) → D15–D19 (ne kadar: müdür, Zimbardo, Le Texier) → E07–E09. Çözülmeden kalır.
4. **L4** "Mark'ın son cevabı" (D14'te açıkça ertelenir) → F02–F03: iki "deneyeceğim", "kendim olarak", son kelime "Peki."
5. **L5** "müdür bunu nereden biliyordu?" (D15) → D16 (yurt deneyi).

**Bölüm damgaları ve küçük soruları:**
- 0:00 Kanca
- I. Yazı tura ("kim gardiyan olacak?")
- II. Altı gün ("bodrumda ne oldu?")
- III. Bant ("müdür gardiyandan ne istedi?")
- IV. İki gardiyan ("biri neden ileri gitti, öteki neden gitmedi?")
- V. Cevap ("gardiyan ne dedi?")

**Kanalın imzası ("yolculuk nerede kırıldı?"):** D14 → F03. On sekiz dakika itiraz eden gardiyanın son sözü: "Peki."

## 6. Kaynak ve hukuk kararları
Kaynaklar `kaynak/DOGRULAMA.md`'de.

**Doğrulamanın yönü değiştirdiği iki yer:**
- **"Öteki istendiği hâlde yapmadı":**
  - Bantta Mark tekrar tekrar itiraz ediyor ama iki kez "deneyeceğim" diyor.
  - Sonra sertleşmediğini gösteren bağımsız belge yok; yalnız 2011'deki kendi anlatımı var.
  - Senaryo bunu söyler (E13). Filmin sonu da "hayır" değil "deneyeceğim" olur.
- **Eshelman'ın "rol de olsa yaptıklarım gerçekti" sözü yok.** Denge 2011 pişmanlığıyla ("Buna kesinlikle pişmanım") ve 2024'te suçu Zimbardo'ya yüklemesiyle kurulur.

**Diğer kararlar:**
- **Kaydın günü:**
  - Le Texier "üçüncü gün" diyor, Zimbardo 2018'de ilk güne koyuyor.
  - Dökümün içeriği (isyan, kapı kırılması, ilçe hapishanesi) üçüncü güne uyuyor.
  - Senaryo "Le Texier'e göre üçüncü gün" der; künyede çelişki not edilir.
- **"Pigs"** (1971 Amerikan öğrenci argosunda polise küçültücü ad):
  - Anlatımda "polisleri nasıl hayal ediyorsan öyle davran" diye verilir, sözcüğün kendisi okunmaz.
  - Görüntüde Amerikan bağlamı kurulur: 1971 Amerikan polis arabası silueti, İngilizce levhalar.
  - Türk polisi okuması yok.
- **Yaşayan kişiler:**
  - yalnız yayımlanmış söz, tarihiyle;
  - "zalim", "sadist", "yalancı" anlatıcının hükmü değil;
  - Le Texier'nin "çürük çalışma" yargısı alınmadı, yalnız belgeye dayanan cümlesi alındı.
- **Aşağılama sahneleri:**
  - "Deve" oyunu anılmaz.
  - Tuvalet yürüyüşünde başlardaki torba yalnız sözle ("başları örtülü") verilir, görüntüde çizilmez (Abu Ghraib okuması).
  - Şınav yandan, tek mahkûm. Sıra hâlinde eğilen figür yok.
- **Reklam uygunluğu:** Korpi'nin küfürlü çığlığı ve Mark'ın esrar sözü kullanılmaz.
- **Kalabalığı azaltmak (sadelik kuralı):**
  - Korpi (8612) adsız bir olay olarak kalır; "taklit ettim" iddiası ayrı bir tartışma.
  - Prescott, Haney, Banks, BBC Prison Study, Abu Ghraib ve Haslam ekibinin kuramı dışarıda.

## 7. Fable'ın senaryo okuması ve rev1 (25 Kasım; seslendirmeden önce)
Okuma: `fable_senaryo_okumasi.md` (6 engelleyici, 12 önemli, 21 küçük).
- **Yeni kaynak:** arşivin zaman damgalı altyazısı (VTT, purl wn708sg0050). Başkan indirip okudu; bulgular doğrulandı. Depoya kopyalanmadı (Zimbardo telifi).
  - Alıntılar artık dakika:saniyeyle künyelendi (senaryo `kaynak` alanı).
- **Engelleyiciler, hepsi uygulandı:**
  1. "Sonunda: deneyeceğim" yanlıştı. Mark bunu 15:12 ve 18:55'te diyor, sonra itiraza devam ediyor. Bant "All right" ile bitiyor (26:52).
     - Son yeniden kuruldu: iki "deneyeceğim" (F02), 22:33'teki "kendim olarak elimden gelenin en iyisi" (başkanın VTT okumasından), son kelime "Peki" (F03).
  2. "Bağır" (TA) ile "yardım et" (VTT) çelişiyor. Bu cümle kullanılmadı; yerine iki kaynakta da aynı olan "biraz fazla yumuşak … biraz daha işin içine gir" alındı.
  3. Bandın üç yerinden birleştirilmiş tek alıntı ayrıldı.
     - D09: iki alıntı, arada anlatıcı.
     - D10: 23:56, D09'un ikinci alıntısının hemen ardı.
  4. Eshelman 2024: "birçoğunu" diye çevrildi. "Suçu Zimbardo'ya veriyor" anlatıcı hükmü olduğu için çıkarıldı.
  5. Zimbardo'nun ölümü (14 Ekim 2024) Eshelman'ın 2024 sözünden önce söyleniyor. Zimbardo'nun 2018 cevabı 2024 sözüne verilmiş gibi durmuyor (E07 → E08).
  6. Sayımdaki gardiyan ilk güne ya da üçüncü güne bağlanmadı. Bağ bandın kendi cümlesiyle kuruluyor (D04: "sayım yapılırken dışarıda oturmak istediğinde"). Günle ilgili çelişki D02'de iki taraflı veriliyor.
- **Önemliler:**
  - Zimbardo'nun iki savunması eklendi ve bölüm onun belgesiyle kapanıyor (D17, D19).
  - Konuşan her bant sözünden önce sözle belirtiliyor ("Mark'ın cevabı:", "Müdür:").
  - Tek taraflı iddialar sahibine atfedildi (B02, B05, C04, C06, C11, D15, E05, E11).
  - "Başları örtülü" yerine "başlarına torba geçirilmiş" (sözde; görüntüde yok).
  - "Pigs" anlatıcının aktarımıyla Amerikan bağlamında. Mark'ın cevabı ("çok polis gördüm") eklendi.
  - Fromm ilk yarıya alındı (C12).
  - İfşadan sonra iki cümle kaldı (F04–F05).
  - Maslach sesle anılmıyor, künyede.
  - Jaffe bantta hep "müdür", Mark hep "Mark".
  - "Aynı isteği duyan gardiyanlar" yerine "en az bir gardiyandan".
- **Geri çevrilen:**
  - Ö10'un "tarih sona" önerisi tam alınmadı. Soru A01'de (≈8 sn), tarih ve yer A02'nin ilk sözü (tek kimlik cümlesi; kanal kuralı buna izin veriyor).
  - Fromm'un adı sesle kaldı (Türk izleyici tanır; ikinci yarıdan ilk yarıya alındığı için "yeni ad" kuralı da tutuyor).
- **Küçükler:** K1, K3–K5, K7–K11, K13–K14, K16–K17, K20–K21 uygulandı. K15 ("bir oyun gibi") çıkarıldı.
- **Yönün yetmediği yer (geriye bakışa):** yön "öteki istendiği hâlde yapmadı" diyordu. Belge bunu söylemiyor: bantta itiraz var, iki "deneyeceğim" var, son söz "Peki"; sonrasına dair bağımsız belge yok. Film bunu saklamıyor, filmin sonu yapıyor.
