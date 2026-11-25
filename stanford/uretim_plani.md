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

| Aşama | İçerik | Cümleler |
|---|---|---|
| Kanca | sayımda kenarda duran gardiyan; soru; bant (ikinci kanca); soruşturma sorusu | A01–A04 |
| Ki (giriş) | ilan, yazı tura, Zimbardo'nun yönlendirmesi, polis, numaralar, gözlük, levhalar | B01–B10 |
| Shō (gelişme) | altı gün: gülüşme, isyan, dolap, gece vardiyası (Eshelman), 416, Maslach, son; 1973 sonucu | C01–C13 |
| Ten (dönüş) | bant: Jaffe ve Mark; amaç (reform, basın); Jaffe'nin görevi ve yurt deneyi; Zimbardo 2018 ↔ Le Texier 2019 | D01–D15 |
| Ketsu (birleştirme) | iki gardiyan: Eshelman'ın sözleri (1971, 2011, 2018, 2024) ↔ Zimbardo; Mark'ın sözleri ↔ belge yokluğu; "hiçbiri araya girmedi"; üçte bir ↔ üçte iki | E01–E16 |
| Son | bandın sonu: "Tamam. Deneyeceğim."; Jaffe'nin "iyi bir amaç" cümlesi; çıkış sorusu | F01–F07 |

**Merak döngüleri (soru → cevap olay):**
1. **L1:** "zalim olur muydun?" (A02) → E15–E16 ("hiçbiri araya girmedi"; üçte bir ↔ üçte iki) → F05.
   - Cevap tek değil; bodrumun üç davranışı.
2. **L2:** "bantta ne isteniyor?" (A03) → D04–D10. Kapak B.
3. **L3:** "kendiliğinden mi, biri mi istedi?" (A04) → D (istendi) → D13–D15 (ne kadar istendi: Zimbardo ↔ Le Texier) → E09–E10 (Eshelman istenenin ötesi mi?).
   - Çözülmeden kalır, iki belge yan yana.
4. **L4:** "gardiyan ne cevap verdi?" (D10'da açıkça ertelenir) → F01–F02.
   - "Tamam. Deneyeceğim."; filmin son olayı.
5. **L5 (küçük):** "Jaffe bunu nereden biliyordu?" (D11) → D12 (yurt deneyi, on yedi kuralın on biri).

**Bölüm damgaları ve küçük soruları:**
- 0:00 Kanca
- I. Yazı tura ("kim gardiyan olacak?")
- II. Altı gün ("bodrumda ne oldu?")
- III. Bant ("müdür gardiyandan ne istedi?")
- IV. İki gardiyan ("biri neden ileri gitti, öteki neden gitmedi?")
- V. Cevap ("gardiyan ne dedi?")

**Kanalın imzası ("yolculuk nerede kırıldı?"):** D10 → F02. İtiraz eden gardiyanın "deneyeceğim" dediği an.

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
