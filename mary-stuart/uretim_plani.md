# Mary Stuart ve I. Elizabeth (Zweig'in anlatımıyla): üretim planı (rev0, 18 Kasım 2026)

Durum: talep kontrolü ölçüldü; yorum kullanıcıyla kurulacak (sorular soruldu). İskelet, başlık adayları ve kapak taslakları sorulardan sonra, senaryodan önce.
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
