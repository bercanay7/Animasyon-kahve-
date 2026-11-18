# Mary Stuart ve I. Elizabeth (Zweig'in anlatımıyla): üretim planı (rev0, 18 Kasım 2026)

Durum (18 Kasım, son): senaryo rev1, seslendirme, 220 planlık film, müzik ve miks, iki kapak, Shorts, SRT ve yayın metinleri hazır; render ve teslim kopyaları sürüyor. Kayıt: `KURUL.md`, `geriye_bakis.md`.
Bölüm: **Tarihin Dönüm Noktaları** (ana); Zweig kapısı yüzünden **Kitapların Sorduğu Sorular** listesine de eklenir.
Kullanıcının çerçevesi (18 Kasım): Stefan Zweig'in *Maria Stuart*'ından okudu; Zweig'in iç dünyaya inen psikolojik anlatımı; ana odak Mary'nin yolculuğu ve iki kraliçe arasındaki çekişme; Elizabeth "uzaktan bir profil"; uzun video (25–30 dk, gerekirse fazlası; karar başkanın). Üslup için cinecode'da hazır tarif varsa o. **Kurul yok**; gerektiğinde Fable tek danışman/denetmen.

## Talep kontrolü (a): tanınırlık
Araçlar: `tools/talep_ac.py` (YouTube otomatik tamamlama, `suggestqueries-clients6.youtube.com`, hl=tr, gl=tr) ve `tools/talep_yt.py` (YouTube arama sonuçları, izlenme sayıları; `ytInitialData`). 18 Kasım 2026.

### Otomatik tamamlama
| Arama | Otomatik tamamlama (seçki) | Okuma |
|---|---|---|
| "mary stuart" | edit, scene pack, **türkçe**, klip, **kimdir**, after francis death, elizabeth tudor, reign, death | **Orta.** Büyük bir uluslararası "edit" kitlesi (*Reign* dizisi); Türkçe "kimdir" ve "türkçe" var |
| "iskoç kraliçesi" | **iskoç kraliçesi mary, iskoç kraliçesi mary idamı**, mary'nin idamı | Türkçe ad "İskoç(ya) Kraliçesi Mary"; idam en çok aranan an |
| "maria stuart" | Schiller, Zusammenfassung, Hörbuch (Almanca) | Türk izleyici için kapı değil |
| "1. elizabeth" | filmi, **elleri**, **kimdir**, edit, **dönemi**, **hayatı** | **Güçlü.** |
| "kraliçe 1. elizabeth" | elleri, hayatı, belgesel, mezarı | |
| "kraliçe elizabeth" | II. Elizabeth (cenaze, Türkiye ziyareti) | Ad II. Elizabeth'le karışır: başlıkta "I. Elizabeth" ya da "1. Elizabeth" şart |
| "elizabeth tudor" | **safiye sultan**, anne boleyn, mary stuart, golden age | Türk kapısı: Safiye Sultan ve III. Murad mektuplaşması (*Muhteşem Yüzyıl: Kösem*) |
| "anne boleyn" | idamı, **kimdir, hikayesi, hayatı, kızı elizabeth** | Elizabeth'in annesi; Türkçe ilgi var |
| "stefan zweig" | **sesli kitap, satranç, korku**, olağanüstü bir gece, mecburiyet, **hayatı, okuma rehberi**, bilinmeyen bir kadının mektubu | **Güçlü edebî kapı.** Türk okurunun en çok okuduğu yabancı yazarlardan |
| "stefan zweig mary stuart" | stefan zweig mary stuart, marie antoinette | Var ama ince |
| "satranç zweig" | özeti, sesli kitap, **Okan Bayülgen**, filmi | Zweig'in Türkiye'deki en bilinen kitabı *Satranç* |
| "darnley", "bothwell", "rizzio" | konuya ulaşmıyor | Yan karakter adları başlıkta ve kapakta kullanılmaz |
| "iki kraliçe", "two queens" | konuya ulaşmıyor | |
| Kontrol: "kral lear" (Ran'ın kapısı) | sesli kitap, Haluk Bilginer, tirad | |

### Türkçe videoların izlenme sayıları (YouTube araması, 18 Kasım)
| Video | Kanal | Süre | İzlenme |
|---|---|---|---|
| İskoçya Kraliçesi Mary Stuart'ın Trajik Hikayesi | Bilgi Damlası | 8:09 | 96 B (4 yıl) |
| Kraliçe Elizabeth'in En Büyük Rakibi Mary Stuart'ın Hikayesi | ViBio | 13:07 | 65 B (3 yıl) |
| İskoçya Kraliçesi MARY: 1. Elizabeth ve Mary Stuart'ın Mücadelesi | Dilimin Ucunda | 8:01 | 40 B (5 yıl) |
| Mary Stuart, Kuzeninin Emriyle İdam Edilen İskoçya Kraliçesi (uyku belgeseli) | Tarih Fısıldıyor | 1:24:59 | 14,5 B (**2 hafta**) |
| Elizabeth ve Mary: İki Kraliçenin Ölümcül Savaşı (uyku) | Uyku Zamanı Bilgileri | 1:03:56 | 16 B (11 ay) |
| *İskoçya Kraliçesi Mary* (2018) Türkçe fragman / "İki Kraliçe" klibi | UIP | 2:24 / 0:30 | 88 B / 190 B |
| 1. Elizabeth: Bakire Kraliçe'nin Sıra Dışı Hükümdarlığı | ViBio | 12:05 | **478 B** |
| I. Elizabeth'in Biraz Tuhaf Olduğunu Gösteren 12 Şaşırtıcı Gerçek | OLUMLU BAK | 10:22 | 562 B |
| I. Elizabeth, Altın Çağa Taşıyan Bakire Kraliçe (uyku) | Tarih Fısıldıyor | 1:22:32 | 182 B (2 ay) |
| I. Elizabeth'in 3. Murat'la İlişkisinin Başladığı O An | ViBio | 8:01 | 165 B |
| İngiltere'nin Altın Çağ Kraliçesi I. Elizabeth Neden Hiç Evlenmedi? | Bilgi Damlası | 9:04 | 39 B |
| Anne Boleyn'in Entrikalarla Dolu Hayatı | ViBio | 15:01 | 377 B |
| Stefan Zweig Okuma Rehberi | Harun Çelik | 55:05 | 102 B |
| Mary Stuart / Stefan Zweig / Bir Kraliçenin Hazin Hikayesi | Harun Çelik | 6:16 | 13,5 B |
| Mary Stuart / Stefan Zweig sesli kitap (1. bölüm) | Marjinal Kraliçe | 26:52 | 6,9 B |
| Kontrol: Kral Lear (Cüneyt Gökçer, 1983) | Celil Efendiler | 1:30:12 | 115 B |

**Sonuç (a):** Konu Ran'dan (Kral Lear kapısı) daha güçlü bir talep tabanında. En güçlü Türkçe kapı **I. Elizabeth** (yüz binlerce izlenme); Mary Stuart tek başına orta (40–96 B), ama "Elizabeth'in rakibi" çerçevesiyle aranıyor ve en çok **idamı** merak ediliyor. Üçüncü kapı **Stefan Zweig** (okur kitlesi). Uyku belgeselleri bu konuyu son iki ayda yeniden işliyor: ilgi canlı, ama alan kalabalık; bizim farkımız animasyon + Zweig'in iç dünya anlatımı + tek büyük soru olmalı.
- Başlıkta "Kraliçe Elizabeth" tek başına yazılmaz (II. Elizabeth'e gider): "I. Elizabeth" ya da "1. Elizabeth".
- Darnley, Bothwell, Rizzio adları başlık ve kapakta yok; videonun içinde.

## Talep kontrolü (b): kişisel soru (yorum kurulduktan sonra seçilecek)
Arama damarları (otomatik tamamlama):
| Damar | Otomatik tamamlama | Not |
|---|---|---|
| Akıl / kalp | "akıl mı kalp mi", "**akıl ile kalp arasında kalmak**", "kalp mi mantık mı", "mantık mı duygu mu" | Zweig'in iki kraliçe karşıtlığı (kalbiyle yaşayan / aklıyla yaşayan) tam bu damar |
| Aşk / kariyer | "aşk mı kariyer mi" (Enes Batur, Devrim Özkan…), "evlilik mi kariyer mi" | Elizabeth evlenmedi, Mary üç kez evlendi |
| Kıskançlık | "kıskançlık nasıl yenilir", "kıskançlıktan nasıl kurtulurum", "kıskançlık duygusunu yenmek" | İki kraliçe birbirini hiç görmeden kıskandı |
| Yanlış insana güvenmek | "yanlış kişiye aşık olmak" | Mary'nin İngiltere'ye geçişi: rakibine sığındı |

Aday sorular (kaynakla ve kullanıcıyla sınanacak):
- "Kalbinle mi yaşarsın, aklınla mı?" (Zweig'in omurgası; damar güçlü; ama genel soru riski)
- "Hiç görmediğin birini neden bu kadar kıskanırsın?" (iki kraliçe hiç karşılaşmadı; sosyal medya çağına doğrudan değer)
- "Düşmanına sığınır mısın?" (Mary'nin 16 Mayıs 1568 kararı: Zweig'in "yıldız anı")
- "Kaybeden mi kazandı?" (Mary öldü; 1603'te İngiliz tahtına onun oğlu oturdu)

## Açık işler
- Yorum (kullanıcıyla), iskelet, on başlık adayı, iki kapak (iki ayrı vaat), kaynak klasörü (birinci el kaynaklar satır numaralı: Mary'nin ve Elizabeth'in mektupları, Melville'in anıları, idam tutanağı).
- Üslup kararı (cinecode tarifi önce; kendi motorlarımız yeniden kullanılabilir mi).
- Kredi hesabı (senaryo kesinleşince; 25–30 dk ≈ 2 çekimle 45–55 B karakter).

## Kullanıcının cevapları (18 Kasım)
| Soru | Cevap |
|---|---|
| Zweig'de en çok etkileyen an | **Solway'i geçiş kararı** (16 Mayıs 1568) ve **Fotheringhay'deki idam** (8 Şubat 1587) |
| Okuma | **Zweig'in okuması:** Mary kalbiyle, Elizabeth aklıyla yaşadı; Mary'yi tutku yıktı |
| Haftalık kullanım | %50'nin altında → Fable danışman 3–4 noktada (kaynak/doğruluk + hassasiyet, paketleme, üslup karesi, ilk kurgu); çizim iki ajana bölünebilir |
| ElevenLabs kredisi | 60 B'den fazla → kanalın kuralı: bölüm başına iki çekim |

## Yorum (başkan; kullanıcının okumasıyla, kaynakla sınanarak)
- **Omurga Zweig'in okuması:** iki kraliçe iki ilke. Mary kararlarını kalbiyle verir (Darnley'yi kendi seçer, Bothwell, Solway); Elizabeth aklıyla ve kararsızlıkla yönetir (evlenmez, bekletir, fermanı imzalar ve inkâr eder). Zweig'in tezini anlatıcı "Zweig'e göre" diye taşır; Zweig bir kaynak ve bakış olarak adıyla anılır.
- **Sınama (doğruluk vetosu, kurulsuz da geçerli):** Zweig, Casket mektuplarını ve soneleri gerçek sayar ve Bothwell tutkusunu bunlara dayandırır. Mektupların asılları kayıptır; yalnız kopya ve çevirileri kalmıştır; bugün birçok tarihçi (Fraser 1969, Guy 2004) değiştirildiklerini ya da sahte olduklarını düşünür; Melville'in anılarında Bothwell'in Mary'yi Dunbar'da zorladığına dair tanıklık var (ajan birinci el metinden doğruluyor). **Karar:** omurga Zweig'de kalır, ama bu noktada tek dürüst cümle verilir ("Zweig bu mektuplara inandı; asılları kayıp, birçok tarihçi inanmıyor") ve anlatı "Zweig'e göre" kipine geçer. Tutku olgu gibi değil, Zweig'in okuması gibi anlatılır. Kullanıcıya bildirildi.
- **Zweig'in kanıtsız psikanalitik yorumları kullanılmaz:** Elizabeth'in evlenmemesini bedensel bir kusura bağlayan spekülasyon gibi (kaynağı yok; hassasiyet). Elizabeth "kıskanç kadın" kalıbına indirgenmez: kıskançlığı yalnız birinci el tanığın (Melville) anlattığı kadarıyla verilir.
- **Elizabeth uzaktan (kullanıcının isteği), görsel kural olarak:** Mary canlı çizilmiş figürdür; **Elizabeth hiç yakından canlanmaz.** Yalnız başkalarının gözüyle görünür: elçi Melville'in anıları (1564: "hangimiz daha güzel?"; 1566: oğlan doğdu haberi), mektupları, Parlamento'ya cevapları ("cevapsız cevap", 1586), Paulet'e yazdırılan mektup ve dönem portreleri (kendisinin denetlediği resmî yüzü). Çizimde en çok uzak siluet, pencere, mühür, taç. İki kraliçe hayatta hiç karşılaşmadı: film de onları aynı karede hiç buluşturmaz (son sahnedeki Westminster mezarları hariç).
- **Psikolojik anlatım kuralı:** iç dünya uydurulmaz. Mary'nin iç dünyası kendi mektuplarından (17 Mayıs 1568 Workington, 8 Şubat 1587 son mektup), işlemelerindeki sözlerden ("En ma fin est mon commencement") ve tanıkların gördüklerinden; Elizabeth'inki kendi sözlerinden ve tanıklardan. Zweig'in yorumu "Zweig'e göre" diye işaretlenir.

## Tek büyük soru ve talep (b)
**Seçilen soru: "Kalbinle mi yaşarsın, aklınla mı?"**
- Gerekçe: Zweig'in iki kraliçe tezi (kullanıcının seçtiği okuma) doğrudan izleyicinin hayatına sorulan bir soruya dönüşüyor; arama damarı güçlü ("akıl mı kalp mi", "akıl ile kalp arasında kalmak", "kalp mi mantık mı"). Sisifos'taki iki koşul birlikte: tanıdık ad (I. Elizabeth, Mary Stuart) + kişisel soru.
- Cevap ikiye bölünür, izleyiciye kalır: akıl tahtı korudu (Elizabeth 44 yıl hüküm sürdü), kalp tahtı kaybetti ama 1603'te İngiliz tahtına Mary'nin oğlu oturdu ("Sonumda başlangıcım"). Kim kazandı?
- Elenen damarlar: "Hiç görmediğin birini kıskanır mısın?" (güçlü ama vaadi Elizabeth'in kıskançlığına kurar; filmin merkezi Mary ve Zweig'in "kıskanç kadın" kalıbı hassas); "Düşmanına sığınır mısın?" (kimsenin gündelik hayatında yok; Solway sorusu bölüm sorusu olarak kalır).

## Hikâye iskeleti: Kahramanın Yolculuğu (Vogler) + bölüm başına ABT (seçildi)
- **Neden:** 25–30 dk'lık biyografi/tarih (yönetmenlik tablosu). Önceki üç video: İkaros Harmon, Kafka Kişōtenketsu, Ran Harmon; art arda değil.
- **Süs:** **çift yolculuk, hiç kesişmeyen iki yol.** Kahraman Mary; Elizabeth onun "eşik bekçisi" ve gölgesi, ama ekranda hiç buluşmazlar. Kanalın imzası "yolculuk nerede kırıldı?" = **Solway** (kullanıcının sahnesi): kahraman yanlış eşikten geçer, dönüşü olmayan dünyaya. Doruk ve "diriliş" = **Fotheringhay** (kullanıcının ikinci sahnesi): Zweig'e göre ölümünü bir zafere çevirir.
- **Açılış:** sondan başla (Zweig de *Yıldızın Parladığı Anlar*'da karar anına doğrudan girer). 0:00 kırmızı (kapak B'nin vaadi), 0:08 Solway (kapak A'nın vaadi), 0:25 büyük soru, **hikâye ~0:40'ta başlar** (Ran kuralı: ≤0:45).

| Adım (Vogler) | Bölüm (YouTube damgası) ve içerik | Cümleler (taslak) |
|---|---|---|
| 0. Kanca | **Kırmızı ve deniz:** 8 Şubat 1587 sabahı siyah elbisenin altından kırmızı; 19 yıl önce bir balıkçı teknesi; "iki kraliçe birbirini hiç görmedi"; soru: kalp mi akıl mı? | A01–A07 |
| 1. Sıradan dünya | **Altı günlük kraliçe:** 1542; beş yaşında Fransa; en mutlu yıllar; 16 yaşında evlilik; 1559 arması: İngiltere tahtına sahip çıkmak (L3 açılır); 18 yaşında dul | B01–B12 |
| 2. Çağrı / eşik | **Siste dönüş:** 1561 Leith; Knox'un "sis"i; Katolik kraliçe, Protestan ülke | C01–C06 |
| 3. Sınavlar, dostlar, düşmanlar | **Görmediği kuzen:** Melville'in 1564 elçiliği (Elizabeth'in soruları, L5 açılır); Elizabeth'in kendi gözdesini koca olarak önermesi; Mary'nin kalbiyle seçtiği Darnley | C07–C18 |
| 3b | **Holyrood'daki gece:** Rizzio; James'in doğumu; Elizabeth'in "kısır kütük" tepkisi (Melville) | D01–D10 |
| 4. Mağaraya yaklaşma | **Bothwell:** Kirk o'Field; Dunbar; evlilik; Casket mektupları (Zweig'in okuması + dürüst cümle) | E01–E14 |
| 5. Büyük sınav | **Gölün ortasındaki ada:** Carberry, Lochleven, tahttan feragat; kaçış (ödül: özgürlük, ordu) | F01–F10 |
| 6. Kırılma (kanalın imzası) | **Solway:** Langside; Dundrennan; yandaşları Fransa der; Mary İngiltere'yi seçer; balıkçı teknesi; Workington'dan Elizabeth'e mektubu (kendi sözleri). L2 kapanır | G01–G12 |
| 7. Uzun sınav | **On dokuz yıl:** esaret; Casket mektupları mahkemesi kararsız; işleme ve "Sonumda başlangıcım" (L6 açılır); Elizabeth'in çıkmazı: bırakamaz, öldüremez | H01–H12 |
| 7b | **Bira fıçısındaki mektuplar:** Walsingham'ın tuzağı; Babington; mektup; Fotheringhay davası ("dünya sahnesi İngiltere'den geniştir") | I01–I10 |
| 7c | **Elizabeth, Elizabeth'e karşı:** cevapsız cevap; ferman; Paulet'e gizlice öldürme önerisi ve reddi; Davison (L5 kapanır) | J01–J09 |
| 8. Diriliş | **Kırmızı:** gece 2'deki son mektup; idam sabahı (tutanaktan, kan ve darbe gösterilmez); peruk ve köpek; Elizabeth'in tepkisi. L1 kapanır | K01–K14 |
| 9. İksirle dönüş | **Sonumda başlangıcım:** 1603; Mary'nin oğlu İngiliz tahtında; Westminster'de birkaç metre arayla iki mezar; Zweig'in hükmü ve izleyiciye soru (L3, L4, L6 kapanır); abone çağrısı doruk anında; bitiş ekranı Şarlken (aynı yüzyıl, tahtını kendi bırakan) + Sisifos | L01–L10 |

Toplam ~140–150 cümle, ~2.800 kelime → tahmini **27–30 dk** (Ran 96 kelime/dk).

### Merak döngüleri
- **L1 (A01 → K):** "Neden kırmızı giydi?" (Katolik şehitlik rengi; tutanaktan)
- **L2 (A04 → G):** "Neden rakibine sığındı?"
- **L3 (B → L):** 16 yaşında İngiliz armasını taşıdı: İngiltere'ye hiç sahip oldu mu? (1603: oğlu)
- **L4 (A07 → L):** Kalple yaşayan mı kazanır, akılla yaşayan mı?
- **L5 (C → J):** Hiç görmediği kuzeni hakkında Elizabeth ne hissediyordu?
- **L6 (H → L):** İşlemesindeki söz: "Sonumda başlangıcım" ne demek?
- **ABT:** her bölümde bir AMA (ör. "ama sisin içinde bir vaiz bekliyordu", "ama kalbiyle seçtiği adam onu kıskanacaktı", "ama Elizabeth'in verdiği söz bir yüzükten ibaretti" (doğrulanacak), "ama mektuplarının hepsi okunuyordu").

## Paketleme taslağı (senaryodan önce)
### On iki başlık adayı (eleme: 1 hayatına soru mu, 2 tek nefes mi, 3 cevabı yarı tahmin ettirip ele vermiyor mu, 4 tanıdık kapı içinde mi, 5 bağlamsız anlaşılır mı)
| # | Aday | 1 | 2 | 3 | 4 | 5 | Not |
|---|---|---|---|---|---|---|---|
| 1 | **Kalbinle mi Yaşarsın, Aklınla mı? \| Mary Stuart ve I. Elizabeth** (63 kr.) | ✓ | ✓ | ✓ | ✓ | ✓ | Seçilen |
| 2 | Aklınla mı Karar Verirsin, Kalbinle mi? \| I. Elizabeth ve Mary Stuart | ✓ | ✓ | ✓ | ✓ | ✓ | 1'in yedeği; "karar" Solway'e bağlanır ama "yaşamak" daha geniş |
| 3 | Mary Stuart Neden Rakibine Sığındı? \| I. Elizabeth'in 19 Yıllık Esiri | ✗ | ✓ | ✓ | ✓ | ✓ | Bilgi merakı; İkaros'taki eksik (kişisel soru yok) |
| 4 | Düşmanına Sığınır mısın? \| Mary Stuart ve I. Elizabeth | ~ | ✓ | ✓ | ✓ | ✓ | Soru yapay: kimsenin hayatında "düşmana sığınmak" yok |
| 5 | İki Kraliçe Birbirini Hiç Görmedi \| Mary Stuart ve I. Elizabeth | ✗ | ✓ | ✓ | ✓ | ✓ | Şaşırtıcı bilgi; soru yok |
| 6 | Hiç Görmediğin Birini Kıskanır mısın? \| I. Elizabeth ve Mary Stuart | ✓ | ✓ | ✓ | ✓ | ✓ | Güçlü; ama vaat Elizabeth'in kıskançlığına kayar ve "kıskanç kadın" kalıbı hassas |
| 7 | I. Elizabeth Ölüm Fermanını Neden İmzalayıp İnkâr Etti? | ✗ | ✗ | ✓ | ✓ | ✓ | Uzun; Elizabeth merkezli (film Mary merkezli) |
| 8 | Kalbine Uyan Kraliçe Neden Kaybetti? \| Mary Stuart | ~ | ✓ | ✗ | ✓ | ✓ | Cevabı veriyor (kaybetti); 1603 tersini söylüyor |
| 9 | Stefan Zweig'in Anlattığı Kraliçe: Mary Stuart | ✗ | ✓ | ✗ | ✓ | ✓ | Yalnız okur kapısı |
| 10 | Neden Kırmızı Giydi? \| Mary Stuart'ın Son Sabahı | ✗ | ✓ | ✓ | ✓ | ✗ | Bağlam ister (kim, nerede?); kapak B'nin işi |
| 11 | Kalbiyle Kaybetti, Oğlu Kazandı \| Mary Stuart ve I. Elizabeth | ✗ | ✓ | ✗ | ✓ | ~ | Sonu ele veriyor |
| 12 | Rakibine Güvenen Kraliçe: Mary Stuart ve I. Elizabeth | ✗ | ✓ | ~ | ✓ | ✓ | Konu anlatıyor |

**Seçilen: 1.** Kişisel soru önde, tanıdık iki ad arkada (Sisifos ve Ran kalıbı: soru | kapı). "Kraliçe Elizabeth" değil "I. Elizabeth" (II. Elizabeth'e gitmesin). Mobilde ilk satır sorunun kendisi. Kalıp çeşitlemesi: önceki başlıklar "Yaptıkların Sana Döner mi?" (Ran) ve "Neden … ?"; bu "… mi, … mı?" ikilemi. Açıklamanın ilk satırı: "Stefan Zweig'in *Mary Stuart*'ından: iki kraliçe, bir hiç karşılaşmama, on dokuz yıl." (Zweig kapısı açıklamada ve etiketlerde.) Paketleme Fable danışmana gösterilecek.

### İki kapak: iki ayrı vaat (kanal ortalaması bulgu 7)
| | A: karar (Çatışma + hareket oku) | B: son (ortadan başlamak, tek renk) |
|---|---|---|
| Görüntü | Gece, sisli deniz; küçük bir teknede pelerinli kadın (kırmızı tek vurgu: pelerinin astarı); karşı kıyıda devasa, taçlı koyu siluet (İngiltere / Elizabeth), tekne ona doğru gidiyor | Kapkara bir salon; sırtı dönük kadın figürü, siyah elbisenin altından tek kırmızı; yüz yok, kütük ve balta yok |
| Yazı | **RAKİBİNE SIĞINDI** | **İDAMINA KIRMIZI GİYDİ** (4–6 kelime denemesi için yedek: "İDAMA KIRMIZILAR İÇİNDE ÇIKTI") |
| Vaat | Neden rakibine sığındı? (Solway) | Neden kırmızı? (şehitlik rengi) |
| Filmde karşılandığı yer | 0:08 (A04: tekne) | 0:00 (A01: kırmızı) |
| Kompozisyon | Mario Joos listesinden "çatışma" + "hareket oku" | "ortadan başlamak" + tek odak |

- Ortak kurallar: Bebas Neue, büyük harf ≥ %18 (1080 ölçeğinde font ≥ 290 px), sağ alt rozet bölgesi (x 1440–1874, y 829–1034) boş, tek odak karenin en parlak yeri.
- Hassasiyet: idam kapağında kan, balta, kütük, kesik baş yok; "kırmızı" Katolik şehitlik rengi olarak doğru bilgi. Gerçek kişi yüzü çizilmez (siluet).

## Üslup (kullanıcının kararı, 18 Kasım): cinecode `silent-film` + `archive-lighttable` araları
- **İlk deneme (Milton gravür motoru) bırakıldı.** Kullanıcı: "Milton motoru bu videoya uygun değil; yeni motor yazmayalım, cinecode'da vardır." Başkan katıldı: Milton'ın dili kozmik mit için kurulmuş siyah siluet ve güneş ışını; bu ise iki kadının yakın, iç dünya dramı. Üç deneme karesi Milton'ın tekrarı gibiydi. Denemeler commit edilmedi.
- **Seçilen: `silent-film`** (cinecode tarifi; LemoLab demo motoru `engine/redraw.js` + `engine/film.js` + `engine/cards.js`, MIT, commit 3a7132b). Mürekkep çizgisi, gümüş yıkama ve tarama; 4:3 kadraj kadife perdeler arasında; ton ve hasar duyguya göre (soğuk ve sert: kötüleşme; sıcak ve temiz: şefkat).
  - **Yüzler gerçek:** kamu malı dönem portreleri ve gravürler (Clouet, Hilliard, Met ve Rijksmuseum CC0 baskıları) yeniden çizim geçişinden geçer; yüz uydurulmaz. Deneme: Clouet'nin beyaz yaslı Mary'si, kare başına ~1,4 sn (`ornek/` çalışma alanında; kullanıcıya gönderildi).
  - **Çizilmiş figürler** (motorun kendi figürleri kaba ve komik): yalnız uzak ve orta planda, siluet; yakın plan ve yüz her zaman gerçek portreden.
  - **Mekânlar** (kale, deniz, salon) ton resmi olarak çizilir ve aynı geçişten geçer: film tek elden çıkmış gibi görünür.
  - Mary'nin kendi sözü çerçeveyi taşır: "bütün dünya sahnesi İngiltere krallığından geniştir" (K29). Ara yazı kartları yalnız onun ve Elizabeth'in kendi sözleri ve bölüm başlıkları için.
  - Müzik: özgün, piyano ya da org (sinema eşlikçisi); Rönesans ezgisi taklidi yok.
- **`archive-lighttable` araları:** gerçek belgeler masada, büyüteçle: mektuplar, Babington şifresi, idam çizimi (1587), Kirk o'Field krokisi, portreler. Künye kartı her birinde.
- **Elenenler:** `paper-popup` (çocuk kitabı havası), `stained-glass` (kilise imgesi; konu din çatışması), Çin ve Japon gelenekleri, `woodcut` (Kafka), `impasto`, `art-deco`, `spy-titles`.

## Kurul (kullanıcının kararı, 18 Kasım): kurul yok, Fable danışman
Kapılar başkan denetimiyle geçer; `KURUL.md`'ye "kurulsuz" diye yazılır. Fable (bağımsız, tek ajan) yalnız gereken yerlerde: (1) senaryo: kaynak/doğruluk + hassasiyet (veto alanları), (2) paketleme: başlık + iki kapak, (3) gerekirse üslup karesi ya da ilk kurgu (sessiz okuma testi). Fable'ın önerileri de iddiadır; başkan ölçüp karar verir.

## Kredi (tahmin)
~2.800 kelime ≈ 21.500 karakter × 2 çekim ≈ **43.000 kredi** (+ ~500 okunuş testi). Kesin sayı senaryo kesinleşince bildirilir ve onay alınır.
