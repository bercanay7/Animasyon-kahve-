# Şarlken — Ses Kontrol Listesi (insan kulağıyla denetim)

**Ses:** ElevenLabs `eleven_v4`, Emrullah Uzun sesi; 14 bölüm ham dosyası `ses_ham/cN_v1.mp3` -> birleştirilmiş `out/voice.wav` (20:58). Zamanlar `out/timeline.json` video eksenidir (mm:ss, sözcüğün başlangıcı; 1-2 sn önceden başlayın).
**Bu liste sesi DİNLEMEDEN hazırlandı.** Kanıt olarak şunlar kullanıldı: (1) ElevenLabs Scribe v1 dökümü (`out/scribe_words.json`, birleştirilmiş sesin tamamı), (2) yerel Whisper dökümü (`ses_ham/olc_log.txt`, yalnız ham c2-c13), (3) dalga biçimi ölçümleri, (4) `script.py` PRON sözlüğü. Hiçbiri kulağın yerini tutmaz.

**Sürüm damgası:** `out/voice.wav` sha256 ca50c8312f76, `out/timeline.json` sha256 ae653495b42f, `script.py` sha256 5146ad40e058. Bu dosyalardan biri değişirse zamanlar kayar.

> **Kısa özet.** Scribe dökümüne göre 174 cümlenin hiçbirinde sözcük atlama/ekleme yok; fark yalnız yazım biçimlerinde (özel adlar, şapkalı harfler, sıra sayıları; 57 cümle). Sayı/tarih içeren 57 ifadenin hepsi aynı sayıya çözülmüş. Asıl kulak işi: aşağıdaki 10 yer (≈4 dakika). En kuvvetli şüpheler: **Şarlken'in söylenişi** (21 geçiş), **'Yörg'** (iki ASR de 'York/Yörk' duydu), **'Halkulvadi'**, **'Tenoçtitlan'**, **'Komünero'**, **'Flandre' (ekran) / 'Flandra' (kulak)**, **'yedi sekiz yüz kişi'** (7.800 gibi anlaşılabilir). Bir yer bozuksa hangi bölümün yeniden üretileceği §7'de.

## 1. Şu 10 yeri dinlemen yeterli

Her satır tek oturuşta dinlenecek 10-30 sn'lik bir pencere (bazılarında iki pencere, aynı bölümden). Sıra videonun akışıdır. Sütun sonundaki bölüm, hata duyulursa yeniden üretilecek bölümdür (ayrıntı §7).

| # | Zaman | Cümleler | Ne dinlenecek | Neden bu yer | Hata varsa -> bölüm |
|---:|---|---|---|---|---|
| 1 | 00:43–01:03 | c0s12–c1s2 | Şarlken (00:45 ve 00:49), Flandre/Flandra (00:52), Gent, Huana (00:57), Filip | Videonun başlık sözcüğü (21 geçiş); Whisper bölümlerde 17 geçişin 13'ünü farklı yazdı. Scribe 'Flandra' yazdı (Whisper c6s5'te de) ama ekranda 'Flandre' var. | c0, c1 |
| 2 | 04:28–04:57 | c3s3–c3s7 | Komünero (04:30), Vilyalar, Padilya, Paçeko ('Pacheko' yazımı), Hermanya | Kastilya adları bir arada. İki ASR de 'Cominero' yazdı. Whisper WER bu bölümde 0,193 (c2-c13 arasında 2. en yüksek). | c3 |
| 3 | 06:51–07:02 | c4s15 | Vartburg, 'Şövalye Yörg' (06:56) | İki ASR de 'York/Yörk' duydu. 'Yörk' Almancaya uygun; ama İngiliz 'York' gibi söylenmişse düzeltilmeli. | c4 |
| 4 | 07:42–07:54 ve 08:24–08:39 | c5s6 + c5s11–c5s12 | Aogsburg (07:44), Melanşton (07:52); Moritz (08:30), İnsbruk (08:35), 'sedyeyle' (08:36) | Alman adları; Whisper WER 0,214 ile bölümler arasında en yüksek. 'Sedyeyle' için Whisper 'Sedia'yla' yazdı. | c5 |
| 5 | 11:04–11:27 ve 12:00–12:08 | c7s3–c7s5 + c7s11 | Mohaç (11:07), 'İkinci Lajoş' (11:11), Zapolya (11:23); Güns ve 'yedi sekiz yüz kişi' (12:03) | Lajos için ASR'ler ayrıştı (Layoş/Lajos). 'Yedi sekiz yüz' Whisper'da '7800' çözüldü: dinleyici 7.800 anlayabilir. | c7 |
| 6 | 12:47–12:54 ve 12:58–13:08 | c8s2 + c8s4 | 'kaptan-ı derya' (12:50), 'Halkulvadi Kalesi' (13:01) | Scribe 'Halkul Vadi' (iki sözcük), Whisper 'Halkülvadi'; Whisper 'kaptan-ı derya'yı 'Kaptanı Deryağı' yazdı. | c8 |
| 7 | 14:00–14:13 ve 14:28–14:44 | c9s2 + c9s5–c9s6 | Tenoçtitlan (14:11), Kahamarka (14:30), Pisarro, Atawalpa (14:34), '1.326.539 peso' (14:36) | Whisper 'Tenoç Ditlan' (iki parça) yazdı. En uzun sayı (bir milyon üç yüz yirmi altı bin beş yüz otuz dokuz) burada. | c9 |
| 8 | 15:02–15:13 ve 15:26–15:45 | c9s10 + c9s13–c9s14 | Valyadolid (15:04), Sepulveda, Las Kasas; Macellan, Elkano (15:30), 'Primus sirkumdedisti me' (15:39) | Whisper c9'da 'Valhadollit' yazdı; Latince tamlama PRON'da özel yazılmış ('sirkum'). | c9 |
| 9 | 18:11–18:26 ve 19:02–19:14 | c12s3 + c12s8 | 'Oranj Prensi Vilhelm' (18:17-18:18), 'Meri' (18:24); 'Yuste Manastırı' (19:10) | Whisper 'Yüste' (ü ile) yazdı; c12s3'te üç yabancı ad bir arada. | c12 |
| 10 | 08:55–09:02 ve 20:29–20:41 | c6s1 + c13s7 | Şarlken'in başka bölümlerdeki söyleniş tutarlılığı: 08:56 (c6) ve 20:37 (c13). Ayrıca bölüm ilk sözcükleri: Tacı (04:19), Nisan (05:11), Şarlken (13:55), Brüksel (18:00) | Whisper bu bölümlerde 'Şarlke'nin' ve 'Schalken' yazdı; Whisper beş bölümün ilk sözcüğünü bozdu (c3, c4, c6, c9, c12). Scribe hepsini doğru çözdü: muhtemelen ASR kusuru, ama başlık sözcüğü için kulak testi şart. | c6, c13 (+ bölüm girişleri) |

**Zaman kalırsa (+7):**

| Zaman | Ne | Not |
|---|---|---|
| 03:17–03:23 (c2s7) | Augsburglu bankacı Yakob Fugger | Whisper 'Oxfordlu' yazdı. |
| 03:57–04:01 (c2s12) | Aahen, Şarlman | Alman şehir adı; tek geçiş. |
| 05:11–05:21 (c4s1-s2) | Vorms, Martin Luter | Whisper 'Lüter' yazıyor; Türkçede yaygın iki biçim. |
| 09:51–09:58 (c6s8) | Kastel Sant Anjelo; yüz seksen dokuz / yüz kırk yedi | Sayılar bir arada. |
| 10:28–10:44 (c6s12-s13) | Kambre, Fransuva, iki milyon altın ekü | Whisper 'eki' yazdı. |
| 01:30–01:54 (c1s7-s10) | Huana, Tordesiyas, Margareta, Mehelen | c1 Whisper ile ölçülmedi; yalnız Scribe doğru çözdü. |
| 00:44–00:48 ve 46:30 civarı (c0 sonu) | Bölüm sonu 'tık' | c0'ın son örneği sıfıra ani düşüyor (aşağıda §6). |

**Kulak notu için kısa işaretleme önerisi:** her yer için `+` (doğru), `~` (kabul edilebilir ama tuhaf), `-` (yanlış -> yeniden üret) yazmanız yeter.

## 2. Kanıtlar neyi gösterir, neyi göstermez

- **Scribe v1** (birleştirilmiş sesin tamamı): modelin dil bilgisi yabancı adları *kanonik yazıma* çevirir (Hernán Cortés, Cajamarca, Sepúlveda, Primus circumdedisti me...). Yani Scribe'ın 'doğru yazması' telaffuzun doğru olduğunu **kanıtlamaz**, yalnız anlaşılabilir olduğunu gösterir. Scribe'ın kanonik olmayan bir yazım seçtiği yerler (Flandra, Cominero, York, Halkul Vadi, Layoş) ise **güçlü şüphe** işaretidir.
- **Whisper (yerel)**: daha zayıf bir ASR; özel adlarda fonetik yazar ve hata yapar. Tek başına kanıt değil; Scribe ile **aynı yönde** saptığı yerler (York/Yörk, Cominero, Halkul(Vadi)) önemli. Whisper yalnız ham c2-c13'ü ölçtü; **c0 ve c1 için Whisper verisi yok**.
- **Sözcük düzeyi fark taraması:** speech metni ile Scribe dökümü sözcük sözcük karşılaştırıldı (rakamlar sözcüğe çevrilerek). 174 cümlenin 57'sinde fark var; **hepsi yazım biçimi farkı** (özel adlar: Vorms/Worms, Huana/Juana, Aogsburg/Augsburg, Yörg/York; şapkalı harfler: hikâyesi/hikayesi; sıra sayıları: Birinci/I.; bir bitişik-ayrı fark: Halkulvadi/Halkul vadi). Atlanan ya da eklenen sözcük yok. Bölüm içi en uzun sessizlik 0,94 sn (sıkıştırma sonrası).
- **Kulakla ayırt edilebilecek bir şey Scribe'a görünmez:** vurgu, ünlü rengi (ü/u), yumuşak ünsüzler, ses tonu, 'yabancı aksan' izlenimi. Bu yüzden §1'deki dinleme gerekli.

## 3. Özel ad ve terim tablosu (risk sırasına göre)

Sütunlar: **Gönderilen okunuş** = `script.PRON` / speech alanında ElevenLabs'e giden yazım; **Beklenen** = özgün dile uygun okunuş (Türkçe harflerle yaklaşık); **Scribe** = birleştirilmiş sesin dökümünde yazılan biçim; **Whisper** = ham bölümün yerel dökümü; **Geçtiği yerler** = video zamanı (mm:ss) ve cümle kimliği; **Bölüm** = hata varsa yeniden üretilecek bölüm(ler).

### 3.1 YÜKSEK — önce bunlar

| Terim (gösterim) | Gönderilen okunuş | Beklenen doğru okunuş | Scribe | Whisper (c2-c13) | Geçtiği yerler | Bölüm | Not |
|---|---|---|---|---|---|---|---|
| **Şarlken** | Şarlken | Şarlken [ʃarlˈken] (Fr. Charles Quint; son hecede vurgu; 'rlk' kümesinde araya ünlü girmemeli) | Şarlken'in ×7, Şarlken ×14 | 17 geçişte (c2-c13) yalnız 4'ünü doğru yazdı (c2s6, c6s12, c6s14, c8s3); 13'ünde: Şarken, Şarlke'nin, Şalken, Şerken-, Şarliken, Charl Ken, Şalke'nin, Şar iken, Charl Kent, Şalke'n, Schalken | 00:45, 00:49, 01:48, 02:15, 03:12, 07:54, 08:56, 10:34, 10:48, 11:17, 11:45, 12:36, 12:54, 13:34, 13:55, 15:34, 15:55, 17:25, 19:03, 19:50, 20:37 | c0, c1, c2, c5, c6, c7, c8, c9, c10, c11, c12, c13 | Scribe 21/21 'Şarlken' çözdü; Whisper'ın dağınık çıktısı 'rlk' kümesinin bölümden bölüme farklı söylenebildiğini düşündürür (ör. 'Şarliken'/'Şarken'). Videonun başlık sözcüğü: ilk (00:45), orta (08:56) ve son (20:37) geçişi dinleyin. |
| **Flandre** | Flandre | Türkçe yerleşik biçim 'Flandra'; Fransızca 'Flandr'. Ekran 'Flandre', kulak muhtemelen 'Flandra' | Flandra'daki ×2 | c6s5'te 'Flandra'daki' (c1 ölçülmedi) | 00:52 (c1s1); 09:32 (c6s5) | c1, c6 | Scribe iki geçişte, Whisper c6s5'te 'Flandra' yazdı: ekrandaki 'Flandre' ile kulaktaki 'Flandra' ayrışıyor. Ya ekranı 'Flandra' yapın ya da sesi 'Flandr' söyletin. **PRON önerisi:** Flandra (hem gösterim hem okunuş). |
| **Augsburglu** | Augsburglu (Aogsburglu) | 'Aoksburglu' (Augsburg + lu) | Augsburg'lu | 'Oxfordlu bankacı Jakob Fugger' (!) | 03:20 (c2s7) | c2 | Scribe 'Augsburg'lu' yazdı; Whisper 'Oxfordlu': sözcük birleşik/ek ile belirsiz söylenmiş olabilir. Fugger'in şehri; kısa ama bankacı cephesinin ilk tanıtıldığı yer. |
| **Komünero** | Komünero | Kastilyaca 'comunero' [komuˈnero] -> 'Komünero/Komunero' | Cominero | 'Cominero İsyanı' | 04:30 (c3s3) | c3 | İki ASR de aynı biçimi ('Cominero') yazdı: ses 'Kominero' (ü yerine i) gibi çıkmış olabilir. |
| **Jörg** | Yörg | Almanca [jœʁk] -> 'Yörk' (sondaki g sertleşir). 'York' (İngiliz şehri) ya da 'Jorj' OLMAMALI | York | 'Yörk' yazdı (Şövalye Yörk adıyla saklandı) | 06:56 (c4s15) | c4 | İki ASR de 'York/Yörk' duydu. 'Yörk' Almancaya uygundur; ama 'York' (o ünlüsü) olursa İngiliz şehri gibi duyulur. Ekranda 'Jörg' görünüyor. **PRON önerisi:** Yörk. |
| **sedyeyle** | sedyeyle | 'sedyeyle' [sedˈjejle]; 'sedya' ya da 'sedia' çıkmamalı | sedyeyle | 'Sedia'yla' | 08:36 (c5s12) | c5 | Scribe 'sedyeyle' yazdı, Whisper 'Sedia'yla': ses 'sedya/sedia' gibi çıkmış olabilir. Metinde de kaynaksız ayrıntı (kaynaklar.md H21): çıkarılması önerilir, o zaman ses sorunu da kalkar. |
| **Lajos (II. Lajos)** | İkinci Lajoş | Macarca [ˈlɒjoʃ] -> 'Layoş' (j = y). Türkçe okuyuşla 'Lajoş' (j = jüri) olursa Macarcadan uzaklaşır | Layoş | 'Kral 2. Lajos' (Lajos) | 11:11 (c7s3) | c7 | Scribe 'Layoş', Whisper 'Lajos' yazdı: ses 'Layoş' ya da 'Lajos' olabilir; ikisi de kabul edilebilir, tutarlılık yeter. **PRON önerisi:** Layoş. |
| **yedi sekiz yüz** | yedi sekiz yüz | 'yedi yüz ile sekiz yüz arası' (700-800). Kulak 'yedi bin sekiz yüz' (7.800) diye duyabilir | yedi - sekiz yüz | 'Günz 7800 kişi ile' | 12:03 (c7s11) | c7 | Scribe 'yedi - sekiz yüz' yazdı; Whisper rakam olarak '7800' çözdü. Gerçek anlam 700-800: dinleyici '7.800' anlayabilir. **PRON önerisi:** yedi yüz ile sekiz yüz arası. |
| **Halkulvadi** | Halkulvadi | Hal-kul-va-di (tek sözcük; La Goulette'in Osmanlıca adı) | Halkul Vadi | 'Halkülvadi Kalesi' (ü ile) | 13:01 (c8s4) | c8 | Scribe iki sözcük yazdı ('Halkul Vadi'), Whisper 'Halkülvadi': arada duraklama ya da 'ü' olabilir. Kale adı olduğu için dinleyin. |
| **Tenochtitlan** | Tenoçtitlan | Nahuatl [te.notʃˈtit.ɬan] -> 'Tenoçtitlan' (tek sözcük, vurgu 'tit') | Tenochtitlan | 'Tenoç Ditlan düştü' (iki parça, d ile) | 14:11 (c9s2) | c9 | Scribe tek sözcük ve doğru yazımı çözdü; Whisper araya boşluk ve 'd' koydu: 'Tenoç-titlan' diye bölünmüş ya da 'tit' yumuşamış olabilir. |
| **Yuste** | Yuste | Kastilyaca [ˈjuste] -> 'Yuste' (u = u; 'Yüste' olmamalı) | Yuste | 'Yüste Manastırı' (ü ile) | 19:10 (c12s8) | c12 | Scribe 'Yuste' yazdı, Whisper 'Yüste': ünlü ü'ye kaymış olabilir. |

### 3.2 ORTA — yabancı adlar, ASR'ler uyumlu

| Terim (gösterim) | Gönderilen okunuş | Beklenen doğru okunuş | Scribe | Whisper (c2-c13) | Geçtiği yerler | Bölüm | Not |
|---|---|---|---|---|---|---|---|
| **Juana** | Huana | Kastilyaca [ˈxwana] -> 'Huana' (j = h) | Juana'ydı, Juana ×2 | 'Huan'a' (c12) | 00:57 (c1s2); 01:30 (c1s7); 18:08 (c12s2) | c1, c12 | 3 yerde; 'Juana' (j = jüri) okunursa yanlış. |
| **Habsburg** | Habsburg(lar) | Almanca [ˈhaːpsbʊʁk] -> 'Habsburg/Hapsburg' (s'li) | Habsburglar, Habsburg ×4 | 'Habsburg' (c7, c11), 'Hapsburg' (c13) | 01:20 (c1s5); 09:02 (c6s2); 12:30 (c7s15); 16:57 (c11s2); 19:52 (c13s3) | c1, c6, c7, c11, c13 | 5 geçiş; 'Habzburg' (z'li) olursa tutarsız. |
| **Tordesillas** | Tordesiyas | Kastilyaca [toɾðeˈsiʎas] -> 'Tordesiyas' | Tordesillas'ta | (c1: ölçülmedi) | 01:33 (c1s7) | c1 | Tek yerde. |
| **Mechelen** | Mehelen | Flemenkçe [ˈmɛxələn] -> 'Mehelen' | Mechelen'de | (c1: ölçülmedi) | 01:51 (c1s10) | c1 | Tek yerde. |
| **Valladolid** | Valyadolid | Kastilyaca [baʎaðoˈlið] -> 'Valyadolid' (son hecede vurgu) | Valladolid, Valladolid'de | c9s10: 'Valhadollit de' | 02:38 (c1s16); 15:04 (c9s10) | c1, c9 | 2 yerde (Kortes ve Tartışma); Whisper c9'da 'Valhadollit' duydu: 'Valhadolid' gibi çıkmış olabilir. |
| **Fugger** | Fugger | Almanca [ˈfʊɡɐ] -> 'Fuger' (tek g sesi); 'Fugger' (iki g) de kabul edilebilir | Fugger'den, Fugger | 'Fugger'den' (c2), 'Fugger' (c10) | 03:22 (c2s7); 16:20 (c10s5) | c2, c10 | Bankacı cephesinin adı. |
| **Aachen** | Aahen | Almanca [ˈaːxən] -> 'Aahen' | Aachen'de | 'Ahen'de' | 04:00 (c2s12) | c2 | Tek yerde. |
| **Villalar** | Vilyalar | Kastilyaca [biʎaˈlaɾ] -> 'Viyalar/Vilyalar' | Villalar'da, Villalar'ın | 'Vilyalarda', 'vilyaların' | 04:35 (c3s4); 05:00 (c3s8) | c3 | 2 yerde. |
| **Padilla** | Padilya | Kastilyaca [paˈðiʎa] -> 'Padilya' | Padilla, Padilla'nın | 'Padilla' | 04:42 (c3s5); 04:46 (c3s6) | c3 | 2 yerde. |
| **María Pacheco** | Maria Pacheko | Kastilyaca [paˈtʃeko] -> 'Paçeko' (ch = ç) | Pacheco | 'Maria Paçeko' (doğru okunmuş görünüyor) | 04:48 (c3s6) | c3 | PRON 'Pacheko': 'c' Türkçede /dʒ/ olduğundan 'Paceko' riski vardı; Whisper 'Paçeko' yazdığı için ch -> ç okunmuş görünüyor. **PRON önerisi:** Paçeko. |
| **Germanía** | Hermanya | Kastilyaca [xeɾmaˈni.a] -> 'Hermanya/Hermania' | Hermania | 'Hermanya İsyanı' | 04:55 (c3s7) | c3 |  |
| **Worms** | Vorms | Almanca [vɔʁms] -> 'Vorms' ('Vörms' ya da İngilizce 'Vorm-s' olmamalı) | Worms ×3, Worms'dan | 'Worms', 'Wormstan' | 05:14 (c4s1); 06:31 (c4s12); 07:08 (c5s1); 07:32 (c5s4) | c4, c5 | 4 geçiş. |
| **Wartburg** | Vartburg | Almanca [ˈvaʁtbʊʁk] -> 'Vartburg' | Wartburg | 'Wartburg' | 06:52 (c4s15) | c4 | Yörg ile aynı cümlede. |
| **Speyer** | Şpayer | Almanca [ˈʃpaɪ̯ɐ] -> 'Şpayer' | Speyer'de | 'Schpeier'de' | 07:30 (c5s4) | c5 | Tek yerde. |
| **Augsburg** | Aogsburg | Almanca [ˈaʊ̯ksbʊʁk] -> 'Aoksburg/Auksburg' | Augsburg'da, Augsburg ×2 | 'Augsburg'da', 'Augsburg Barış'ı' | 07:44 (c5s6); 08:41 (c5s13); 20:06 (c13s4) | c5, c13 | Üç bağlam: 1530 İtirafı, 1555 Barışı, c13. (Augsburglu için yukarıya bakın.) |
| **Melanchthon** | Melanşton | Almanca [meˈlançtɔn] -> 'Melanhton/Melanşton' | Melanchthon'du | 'Melançton'du' | 07:52 (c5s6) | c5 | Tek yerde. |
| **Mühlberg** | Mülberg | Almanca [ˈmyːlbɛʁk] -> 'Mülberk/Mülberg' | Mühlberg'de | 'Mülberg'de' | 08:10 (c5s9) | c5 | Tek yerde. |
| **Tiziano** | Tiziano | İtalyanca 'Tiçiano' [titˈtsjaːno]; Türkçede yaygın 'Tiziano/Tisiyano' | Tiziano | 'Tiziano' | 08:18 (c5s10) | c5 | PRON'suz. |
| **Moritz** | Moritz | Almanca [ˈmoːʁɪts] -> 'Morits/Moriç' (z = ts) | Moritz | 'Moritz' | 08:30 (c5s11) | c5 | PRON değiştirmedi; Türkçe okuyuşta 'tz' belirsiz (Moriz/Morits/Moriç). **PRON önerisi:** Morits. |
| **Castel Sant'Angelo** | Kastel Sant Anjelo | İtalyanca [kaˈstɛl sant ˈandʒelo] -> 'Kastel Sant Anjelo' | Castel Sant'Angelo'ya | 'Castel Sant'Angelo'ya' | 09:52 (c6s8) | c6 | Tek yerde. |
| **Cambrai** | Kambre | Fransızca [kɑ̃bʁɛ] -> 'Kambre' | Cambrai'de | 'Kambrede' | 10:29 (c6s12) | c6 | Tek yerde. |
| **Mohaç** | Mohaç | Macarca Mohács [ˈmohaːtʃ] -> 'Mohaç' | Mohaç'ta | 'Muhac'da' (c7s3) | 11:07 (c7s3) | c7 | Whisper o->u, ç->c yazdı; Scribe doğru. |
| **Güns** | Güns | Osmanlıca 'Güns' (Kőszeg'in Almanca adı) | Güns | 'Günz' (c7s11) | 12:03 (c7s11) | c7 | Whisper z ile yazdı; Scribe 'Güns'. |
| **kaptan-ı derya** | kaptan-ı derya | Osmanlıca 'kaptan-ı derya' [kaptanɯ dɛɾja] | kaptan-ı derya | 'Kaptanı Deryağı' | 12:50 (c8s2) | c8 | Scribe doğru ('kaptan-ı derya') yazdı; Whisper 'deryağı' duydu: tamlama bitişik söylenmiş olabilir. |
| **Cortés / Hernán** | Kortes / Hernan | Kastilyaca [koɾˈtes] [eɾˈnan] -> 'Kortes' (son hecede vurgu), 'Hernan' | Cortés ×3 | 'Henan Cortes' (c8), 'Hernan Cortes' (c9) | 13:49 (c8s11); 14:03 (c9s2); 14:13 (c9s3) | c8, c9 | 3 yerde. |
| **Cajamarca** | Kahamarka | Kastilyaca [kaxaˈmaɾka] -> 'Kahamarka' | Cajamarca'da | 'Cajamarca'da' | 14:30 (c9s5) | c9 | Tek yerde. |
| **Pizarro** | Pisarro | Kastilyaca [piˈsaro]/[piˈθaro] -> 'Pisaro/Pizaro' | Pizarro | 'Pizarro' | 14:32 (c9s5) | c9 | Tek yerde; 'rr' abartılırsa tuhaf. |
| **Atahualpa** | Atawalpa | Keçuva/Kastilyaca [ataˈwalpa] -> 'Atawalpa' | Atahualpa'yı, Atahualpa | 'Atavalpa' | 14:34 (c9s5); 14:44 (c9s7) | c9 | 2 yerde. |
| **Sepúlveda** | Sepulveda | Kastilyaca [seˈpulβeða] -> 'Sepulveda' | Sepúlveda | 'Sepulveda' | 15:10 (c9s10) | c9 | Tek yerde. |
| **Las Casas** | Las Kasas | Kastilyaca [las ˈkasas] -> 'Las Kasas' | Las Casas | 'Las Casas' | 15:11 (c9s10) | c9 | Tek yerde. |
| **Elcano** | Elkano | Kastilyaca [elˈkano] -> 'Elkano' | Elcano | 'Elcano' | 15:30 (c9s13) | c9 | Tek yerde. |
| **Primus circumdedisti me** | Primus sirkumdedisti me | Latince: Klasik [ˈprimus ˈkirkumdedisti me]; Kilise [... tʃirkum...]. PRON'daki 's' ('sirkum') ikisi de değil | Primus circumdedisti me | 'Primus circum dedistime' | 15:39 (c9s14) | c9 | Scribe doğru Latince yazımı çözdü; yine de tek yerde dinleyin (c -> s mi, k/ç mi?). **PRON önerisi:** Primus kirkumdedisti me. |
| **Potosí** | Potosi | Kastilyaca [potoˈsi] -> 'Potosi' (son hecede vurgu) | Potosi | 'Potosi' | 16:12 (c10s4) | c10 | Tek yerde. |
| **Welser** | Velzer | Almanca [ˈvɛlzɐ] -> 'Velzer' | Welserler | 'Welserler' | 16:29 (c10s7) | c10 | Tek yerde. |
| **Orange** | Oranj | 'Oranj' Prensi | Orange | 'Oranj' | 18:17 (c12s3) | c12 | c12s3'te üç ad bir arada. |
| **Willem** | Vilhelm | Hollandaca Willem [ˈʋɪləm] -> 'Vilem'; Almanca biçim 'Vilhelm' da yaygın | Wilhelm'in | 'Wilhelm'in' | 18:18 (c12s3) | c12 | PRON Almanca biçimi seçti. |

### 3.3 DÜŞÜK — Türkçeleşmiş / yaygın adlar

| Terim (gösterim) | Gönderilen okunuş | Beklenen doğru okunuş | Scribe | Whisper (c2-c13) | Geçtiği yerler | Bölüm | Not |
|---|---|---|---|---|---|---|---|
| **Brüksel** | Brüksel | Türkçe yerleşik | Brüksel'de ×2, Brüksel | 'Bruksel'de' (c9s4), 'Blüksel' (c12s1) | 00:03 (c0s2); 14:22 (c9s4); 18:00 (c12s1) | c0, c9, c12 | Whisper c12'nin ilk sözcüğünü 'Blüksel' yazdı; c12 sesi bölüm başından 0,05 sn sonra başlıyor (diğerleri ~0,2 sn). |
| **Margareta** | Margareta | Halanın adı (Latinleştirilmiş 'Margareta') | Margareta'nın | (c1: ölçülmedi) | 01:49 (c1s10) | c1 |  |
| **Santander** | Santander | Kastilyaca [santanˈdeɾ] -> 'Santander' | Santander'di | (c1: ölçülmedi) | 02:28 (c1s14) | c1 |  |
| **Tazones** | Tazones | Kastilyaca [taˈθones] -> 'Tazones' | Tazones'a | (c1: ölçülmedi) | 02:31 (c1s14) | c1 |  |
| **Kortesi (Cortes)** | Kortesi | 'Cortes' (parlamento) -> 'Kortes' (Cortés ile eşsesli) | Kortesi | (c1: ölçülmedi) | 02:38 (c1s16) | c1 | Cortés ile eşsesli; bağlam ('Valladolid Kortesi') ayırt ediyor. |
| **Maksimilian** | Maksimilian | Türkçe yerleşik 'Maksimilyan/Maksimilian' | Maximillian | 'Maksimilyan' | 02:52 (c2s1) | c2 |  |
| **François** | Fransuva | Fransızca [fʁɑ̃swa] -> 'Fransuva' | Fransuvay'dı, Fransuva'ydı, Fransuva ×2, Fransuva'nın | 'Fransuaydı' (c2s3, c6s1: v düşmüş gibi), 'Fransuva' (c6s3) | 03:01 (c2s3); 08:59 (c6s1); 09:15 (c6s3); 10:32 (c6s12); 10:39 (c6s13) | c2, c6 | 5 yerde (I. François). |
| **Catherine / Henry** | Katerina / Henri | 'Katerina' (Aragonlu Catherine), 'Henri' (VIII. Henry) | Henry, Caterina'nın, Henri | 'Katerina'nın', 'Henri' | 03:04 (c2s4); 10:13 (c6s10); 10:16 (c6s10) | c2, c6 |  |
| **Jakob** | Yakob | Almanca [ˈjaːkɔp] -> 'Yakop/Yakob' | Jakob ×2 | 'Jakob' (c2), 'Yakup' (c10) | 03:22 (c2s7); 16:19 (c10s5) | c2, c10 |  |
| **Şarlman** | Şarlman | Charlemagne'ın Türkçe adı | Şarlman'ın | 'Şarlman'ın şehri' | 03:59 (c2s12) | c2 |  |
| **Plus ultra** | Plus ultra | Latince [plus ˈultra] | Plus | 'Plus ultra' | 04:03 (c2s13) | c2 |  |
| **Valensiya** | Valensiya | Türkçe yerleşik biçim | Valencia'da | 'Valencia'da' | 04:52 (c3s7) | c3 |  |
| **Luther / Lutherciliği** | Luter / Luterciliği | Türkçede yerleşik 'Luter' (bazı konuşurlar 'Lüter' der; ikisi de kabul) | Luther ×5, Luther'in, Lutherciliğe, Lutherciliği | 'Lüter' (c4-c5 boyunca; Türkçe yazım) | 05:20, 05:44, 06:32, 06:38, 07:20, 07:51, 08:43, 20:07 | c4, c5, c13 | 8 geçiş. |
| **Şmalkalden** | Şmalkalden | Almanca 'Schmalkalden' [ˈʃmalkaldn̩] -> 'Şmalkalden' | Şmalkalden | 'Şmalkal'den' | 07:58 (c5s7) | c5 | PRON gerekmedi. |
| **Innsbruck** | İnsbruk | Almanca [ˈɪnsbʁʊk] -> 'İnsbruk' | Innsbruck'dan | 'Innsbruck'tan' | 08:35 (c5s12) | c5 |  |
| **Pavia** | Pavya | İtalyanca [paˈviːa] -> 'Pavia/Pavya' | Pavya'da | 'Pavia'da' | 09:14 (c6s3) | c6 |  |
| **ecü** | ekü | Fransızca écu [e.ky] -> 'ekü' | ekü | 'eki' | 10:43 (c6s13) | c6 | Tek yerde. |
| **Zapolya** | Zapolya | Türkçe yerleşik (Macarca Szapolyai) | Zapolya | 'Zapolya' | 11:23 (c7s5) | c7 |  |
| **Barbaros Hayreddin** | Barbaros Hayreddin | Türkçe | Hayreddin | 'Barbaros Hayreddin Paşa' | 12:46 (c8s1) | c8 |  |
| **Andrea Doria** | Andrea Doria | İtalyanca [anˈdrɛa ˈdɔrja] | Andrea | 'Andrea Doria'nın' | 12:55 (c8s3) | c8 |  |
| **Preveze** | Preveze | Türkçe yerleşik | Preveze'de | 'Preveze'de' | 13:19 (c8s7) | c8 |  |
| **Dürer** | Dürer | Almanca [ˈdyːʁɐ] -> 'Dürer' | Dürer | 'Dürer' | 14:21 (c9s4) | c9 |  |
| **Magellan** | Macellan | Türkçede yerleşik 'Macellan' | Macellan | 'Magellan' | 15:27 (c9s13) | c9 |  |
| **İsabel** | İsabel | Kastilyaca/Portekizce -> 'İsabel' | Isabel'le, Isabel | 'İzabelle' (c11; z ile) | 17:18 (c11s4); 17:22 (c11s5) | c11 | 2 yerde. |
| **Mary** | Meri | 'Meri' (Macaristan Kraliçesi Maria / Mary of Hungary) | Mary | 'Meri' | 18:24 (c12s3) | c12 |  |

## 4. Rakam ve tarih okunuşları

### 4.1 Riskli olanlar

| Zaman · cümle | Gösterim | Gönderilen okunuş | Risk | Scribe | Öneri |
|---|---|---|---|---|---|
| 00:00 · c0s1 | 25 Ekim 1555. | Yirmi beş Ekim, bin beş yüz elli beş. | Videonun ilk sözcükleri; virgül duraksaması | '25 Ekim 1555.' (aynı) | Dinleyin: 'bin beş yüz elli beş' bitişik değil, doğal ritimde mi? |
| 00:49 · c1s1 | 24 Şubat 1500'de | yirmi dört Şubat bin beş yüzde | 'bin beş yüzde' ek birleşmesi | '24 Şubat 1500'de' (aynı) | Yıl+ek biçimlerinin ilkini dinleyin; diğer 'bin beş yüz...' okunuşları aynı kalıp. |
| 03:12 · c2s6 | 850.000 florin | sekiz yüz elli bin florin | Birim 'florin' söyleniyor, ASR sözcükle aynı | 'sekiz yüz elli bin florini' (aynı) | — |
| 03:17 · c2s7 | 543.000 florin | beş yüz kırk üç bin florin | Kaynaklarda aralıklı (500-550 bin) | 'beş yüz kırk üç bin florin' (aynı) | Metinde 'yaklaşık' eklenmesi önerilir (kaynaklar.md §5). |
| 09:51 · c6s8 | 189 ... 147'si | yüz seksen dokuz ... yüz kırk yedisi | İki sayı bir cümlede; '-si' eki | 'Yüz seksen dokuz ... yüz kırk yedisi' (aynı) | — |
| 12:01 · c7s11 | yedi sekiz yüz kişi | yedi sekiz yüz kişiyle | **ANLAM BELİRSİZLİĞİ:** 700-800 yerine 7.800 anlaşılabilir | 'yedi - sekiz yüz' (Scribe); Whisper '7800' | **Yeniden üret:** 'yedi yüz ile sekiz yüz arası' (c7). |
| 14:36 · c9s6 | 1.326.539 peso | bir milyon üç yüz yirmi altı bin beş yüz otuz dokuz peso | En uzun sayı; binler basamağı | Sözcüklerle aynı | Dinleyin; 'otuz dokuz' sonrası 'peso' bitişikliğine dikkat. |
| 15:55 · c10s3 | on milyonun, dokuz milyonun, beş milyondan | (aynı sözcükler) | Birim eksik ('ne milyonu?') | Sözcüklerle aynı | Metin önerisi: 'dükat' ekleyin (kaynaklar.md §5). |
| 03:01 · c2s3; 08:59 · c6s1 | I. François | Birinci Fransuva'ydı | Roma rakamı sıra sayıya çevrildi | 'I. Fransuvay'dı' / 'Birinci Fransuva'ydı' | — |
| 03:04 · c2s4 | VIII. Henry | Sekizinci Henri | Roma rakamı | 'VIII. Henry' | — |
| 11:05-11:14 · c7s3 | II. Lajos | İkinci Lajoş | Sıra sayısı + ad | 'İkinci Layoş' | Lajoş/Layoş tutarlılığı (§3.1). |
| 17:04 · c11s3 | 2019'daki | iki bin on dokuzdaki | Yıl ek | '2019'daki' (aynı) | — |
| 18:00 · c12s1 | Öğleden sonra saat üç | (aynı) | — | 'Öğleden sonra saat 3' / aynı | — |
| 19:25 · c12s10 | 31 Ağustos 1558'de ... 21 Eylül'de ... Elli sekiz | otuz bir Ağustos bin beş yüz elli sekizde ... yirmi bir Eylül'de ... Elli sekiz | Üç sayı arka arkaya | Üçü de aynı | Bölümün en yoğun sayı cümlesi; hızlı geçiyorsa not alın. |
| 13:33 · c8s9 | beş yüz yelkenli, yaklaşık yirmi dört bin asker | (aynı) | — | Aynı | — |
| 12:22 · c7s14 | otuz bin altın | (aynı) | Birim belirsiz (altın ne?) | Aynı | Kaynaklar birimde ayrışıyor (florin/duka). |

### 4.2 Tüm rakam/tarih okunuşları (otomatik karşılaştırma)

Gösterimde rakam içeren 57 ifade; hepsinin okunuşu Scribe dökümüyle aynı sayıya çözüldü (fark yok). Bu yüzden bu tablo yalnız başvuru içindir; kulakla ancak 4.1'dekiler denetlenmeli.

| Zaman · cümle | Gösterim | Gönderilen okunuş | Scribe |
|---|---|---|---|
| 00:00 · c0s1 | 25 Ekim 1555 | yirmi beş Ekim bin beş yüz elli beş | aynı (rakamla yazdı) |
| 00:49 · c1s1 | 24 Şubat 1500'de | yirmi dört Şubat bin beş yüzde | aynı (rakamla yazdı) |
| 01:30 · c1s7 | 1509'dan | bin beş yüz dokuzdan | aynı (rakamla yazdı) |
| 02:11 · c1s13 | 1516'da | bin beş yüz on altıda | aynı (rakamla yazdı) |
| 02:21 · c1s14 | Eylül 1517'de | Eylül bin beş yüz on yedide | aynı (rakamla yazdı) |
| 02:38 · c1s16 | 1518'de | bin beş yüz on sekizde | aynı (rakamla yazdı) |
| 02:49 · c2s1 | Ocak 1519'da | Ocak bin beş yüz on dokuzda | aynı (rakamla yazdı) |
| 03:12 · c2s6 | 850.000 | sekiz yüz elli bin | aynı (sözcükle yazdı) |
| 03:17 · c2s7 | 543.000 | beş yüz kırk üç bin | aynı (sözcükle yazdı) |
| 03:24 · c2s8 | 28 Haziran 1519'da | yirmi sekiz Haziran bin beş yüz on dokuzda | aynı (rakamla yazdı) |
| 03:57 · c2s12 | 23 Ekim 1520'de | yirmi üç Ekim bin beş yüz yirmide | aynı (rakamla yazdı) |
| 04:29 · c3s3 | 1520'de | bin beş yüz yirmide | aynı (rakamla yazdı) |
| 04:33 · c3s4 | 23 Nisan 1521'de | yirmi üç Nisan bin beş yüz yirmi birde | aynı (rakamla yazdı) |
| 05:11 · c4s1 | Nisan 1521 | Nisan bin beş yüz yirmi bir | aynı (rakamla yazdı) |
| 07:19 · c5s3 | 1524'te | bin beş yüz yirmi dörtte | aynı (rakamla yazdı) |
| 07:28 · c5s4 | 1529'da | bin beş yüz yirmi dokuzda | aynı (rakamla yazdı) |
| 07:43 · c5s6 | 1530'da | bin beş yüz otuzda | aynı (rakamla yazdı) |
| 08:00 · c5s8 | 1546'da | bin beş yüz kırk altıda | aynı (rakamla yazdı) |
| 08:07 · c5s9 | 24 Nisan 1547'de | yirmi dört Nisan bin beş yüz kırk yedide | aynı (rakamla yazdı) |
| 08:25 · c5s11 | 1552'de | bin beş yüz elli ikide | aynı (rakamla yazdı) |
| 08:38 · c5s13 | Eylül 1555'te | Eylül bin beş yüz elli beşte | aynı (rakamla yazdı) |
| 09:12 · c6s3 | 24 Şubat 1525'te | yirmi dört Şubat bin beş yüz yirmi beşte | aynı (rakamla yazdı) |
| 09:44 · c6s7 | 6 Mayıs 1527'de | altı Mayıs bin beş yüz yirmi yedide | aynı (rakamla yazdı) |
| 09:51 · c6s8 | 189 | yüz seksen dokuz | aynı (sözcükle yazdı) |
| 09:51 · c6s8 | 147'si | yüz kırk yedisi | aynı (sözcükle yazdı) |
| 10:19 · c6s11 | 1528'de | bin beş yüz yirmi sekizde | aynı (rakamla yazdı) |
| 10:28 · c6s12 | 1529'da | bin beş yüz yirmi dokuzda | aynı (rakamla yazdı) |
| 11:05 · c7s3 | 29 Ağustos 1526'da | yirmi dokuz Ağustos bin beş yüz yirmi altıda | aynı (rakamla yazdı) |
| 11:27 · c7s6 | 1529'da | bin beş yüz yirmi dokuzda | aynı (rakamla yazdı) |
| 11:27 · c7s6 | 27 | yirmi yedi | aynı (rakamla yazdı) |
| 11:51 · c7s10 | 1532'de | bin beş yüz otuz ikide | aynı (rakamla yazdı) |
| 12:22 · c7s14 | 1547'de | bin beş yüz kırk yedide | aynı (rakamla yazdı) |
| 12:47 · c8s2 | 1534'te | bin beş yüz otuz dörtte | aynı (rakamla yazdı) |
| 12:59 · c8s4 | Temmuz 1535'te | Temmuz bin beş yüz otuz beşte | aynı (rakamla yazdı) |
| 13:16 · c8s7 | 28 Eylül 1538'de | yirmi sekiz Eylül bin beş yüz otuz sekizde | aynı (rakamla yazdı) |
| 13:33 · c8s9 | 1541'de | bin beş yüz kırk birde | aynı (rakamla yazdı) |
| 14:01 · c9s2 | 1519'da | bin beş yüz on dokuzda | aynı (rakamla yazdı) |
| 14:01 · c9s2 | 13 Ağustos 1521'de | on üç Ağustos bin beş yüz yirmi birde | aynı (rakamla yazdı) |
| 14:29 · c9s5 | 1532'de | bin beş yüz otuz ikide | aynı (rakamla yazdı) |
| 14:36 · c9s6 | 1.326.539 | bir milyon üç yüz yirmi altı bin beş yüz otuz dokuz | aynı (sözcükle yazdı) |
| 14:51 · c9s9 | 1542'de | bin beş yüz kırk ikide | aynı (rakamla yazdı) |
| 15:02 · c9s10 | 1550'de | bin beş yüz ellide | aynı (rakamla yazdı) |
| 16:07 · c10s4 | 1545'te | bin beş yüz kırk beşte | aynı (rakamla yazdı) |
| 16:16 · c10s5 | 1523'te | bin beş yüz yirmi üçte | aynı (rakamla yazdı) |
| 16:35 · c10s8 | 1556'da | bin beş yüz elli altıda | aynı (rakamla yazdı) |
| 16:35 · c10s8 | Nisan 1557'de | Nisan bin beş yüz elli yedide | aynı (rakamla yazdı) |
| 17:04 · c11s3 | 2019'daki | iki bin on dokuzdaki | aynı (rakamla yazdı) |
| 17:15 · c11s4 | 26 | yirmi altı | aynı (sözcükle yazdı) |
| 17:20 · c11s5 | 1539'da | bin beş yüz otuz dokuzda | aynı (rakamla yazdı) |
| 18:00 · c12s1 | 25 Ekim 1555 | yirmi beş Ekim bin beş yüz elli beş | aynı (rakamla yazdı) |
| 18:32 · c12s5 | Ocak 1556'da | Ocak bin beş yüz elli altıda | aynı (rakamla yazdı) |
| 18:32 · c12s5 | 1556 | bin beş yüz elli altı | aynı (rakamla yazdı) |
| 18:32 · c12s5 | 1558 | bin beş yüz elli sekiz | aynı (rakamla yazdı) |
| 19:03 · c12s8 | Eylül 1556'da | Eylül bin beş yüz elli altıda | aynı (rakamla yazdı) |
| 19:03 · c12s8 | Şubat 1557'de | Şubat bin beş yüz elli yedide | aynı (rakamla yazdı) |
| 19:25 · c12s10 | 31 Ağustos 1558'de | otuz bir Ağustos bin beş yüz elli sekizde | aynı (rakamla yazdı) |
| 19:25 · c12s10 | 21 | yirmi bir | aynı (rakamla yazdı) |

Sözcükle yazılmış sayılar (yetmiş ile yüz bin, kırk altı yıl, doksan beş maddelik, iki milyon altın ekü, yirmi bin esir vb.) de Scribe'da aynen çıktı; yalnız c7s11 'yedi sekiz yüz' anlam belirsizliği taşıyor (yukarıda).

## 5. Ekranda yazılan ile kulağa gelenin ayrışabileceği yerler

Altyazı/ekran metni `disp`'ten, ses `speech`'ten üretildiği için bu farklar zaten tasarım gereği var; ama izleyicinin gördüğü ile duyduğu **birbirini tutmuyorsa** kafa karışıklığı yaratabilir:

| Ekran | Kulak (PRON / ASR) | Zaman | Yorum |
|---|---|---|---|
| Flandre | Flandra (Scribe iki geçişte; Whisper c6s5'te) | 00:52, 09:32 | Ekranı 'Flandra' yapmak (Türkçe yerleşik biçim) en kolay çözüm. |
| Jörg | Yörg (gönderilen) / Yörk-York (ASR) | 06:56 | Ekranda 'Jörg', kulakta 'Yörk': Almancaya uygun ama tuhaf görünebilir. |
| Lajos | Lajoş (gönderilen) / Layoş-Lajos (ASR) | 11:11 | Üçü de kabul edilebilir; tutarlı olsun. |
| Komünero | Komünero (gönderilen) / Cominero (ASR) | 04:30 | ü yerine i duyuluyorsa 'Komunero' yazıp gönderin. |
| Hıristiyan | Hristiyan (Scribe/Whisper) | 06:17, 13:08, 18:53, 20:01 | TDK yazımı 'Hristiyan'; ekranda 'Hıristiyan'. Ses hangisiyse ekran onunla eşleşsin (çok küçük sorun). |
| Kortesi (parlamento) / Cortés | Kortes (ikisi de) | 02:38; 13:49, 14:03, 14:13 | Eşsesli; bağlam ayırıyor ('Valladolid Kortesi' / 'Hernán Cortés'). |
| hikâyesi, hâlâ, ahlâkı, Resmî | şapkasız okunur | çeşitli | Şapkalı yazım yalnız ekranda; sorun değil. |
| ecü | ekü (gönderilen) / eki (Whisper) | 10:43 | Tek yerde; 'ekü' duyulduğundan emin olun. |

## 6. Dalga biçimi ölçümleri (kulaksız bulgular)

| Ölçüm | Bulgu |
|---|---|
| Seviye tutarlılığı | 14 bölümün aktif konuşma seviyesi −23,6 / −23,7 dB RMS (bölümler arası fark ≈0,1 dB); bölümlere uygulanan kazanç +10,8 ile +12,2 dB arası. Seviye dengesi tamam. |
| Kırpılma | Genel tepe 0,95 (c4'te); mutlak değeri 0,999'u aşan örnek sayısı 0. Kırpılma yok. |
| Bölüm başları | Çoğu bölümde konuşma bölüm başından ≈0,17-0,23 sn sonra başlıyor. **c12'de yalnız 0,05 sn:** giriş çok dar. Ham dosyada ilk ≈25 ms sessiz, sonra 'B' patlaması geliyor, yani kırpılma kanıtı yok; ama Whisper ilk sözcüğü 'Blüksel' yazdı (Scribe 'Brüksel'). Dinleyin (18:00). |
| Bölüm sonları | **c0'da (00:46,5)** ham dosya sıfır olmayan bir DC düzeyiyle bitiyor ve karışımda ani sıfıra düşüyor (son örnek ≈ −30 dBFS): bölüm kartına geçişte hafif 'tık' olabilir. Diğer bölümlerde son örnekler ≈ 0 (sorun yok). Ham dosyalardan c6, c9, c10 ve c13 ses tam sönmeden kesiliyor (son örnekler −47 ile −56 dB), ama karışımda son örnekler ≈0'a yakın olduğundan (c6 −87, c10 −37 int16) tık beklenmez. |
| Bölüm arası boşluk | Her bölümden sonra 3,0 sn dijital sessizlik (kart boşluğu); c13 sonunda yok. |
| Sessizlik | Cümle içi en uzun duraklama 0,94 sn (c12s1 'saat'ten sonra 'Öğleden'); sıkıştırma eşiği 0,85 sn olduğundan uzun boşluk yok. |

## 7. Hata bulunursa hangi bölüm yeniden üretilecek

Ses bölüm bölüm üretilmiş (`ses_ham/cN_v1.mp3`); tek cümle düzeltmek için bile **ilgili bölümün tamamı** yeniden üretilir. Süre/zaman bilgisi `out/voice_chapters.json` ve `out/timeline.json`'dan; karakter sayısı `script.chapter_text()` çıktısındandır (ElevenLabs'e giden metin, paragraflar boş satırla ayrılır).

| Bölüm | Cümle aralığı | Video aralığı | Süre (sn) | Karakter | Ham dosya | Whisper WER | Bu bölümde dinlenecek yüksek/orta riskli terimler |
|---|---|---|---:|---:|---|---:|---|
| c0 Brüksel, 25 Ekim 1555 | c0s1–c0s12 | 00:00–00:46 | 46,5 | 555 | ses_ham/c0_v1.mp3 | ölçülmedi | Şarlken |
| c1 Dört Tahtın Çocuğu | c1s1–c1s16 | 00:49–02:46 | 116,9 | 1454 | ses_ham/c1_v1.mp3 | ölçülmedi | Şarlken, Flandre, Habsburg, Mechelen, Tordesillas, Juana, Valladolid |
| c2 Taç Satılık | c2s1–c2s14 | 02:49–04:16 | 86,6 | 1151 | ses_ham/c2_v1.mp3 | 0,141 | Şarlken, Augsburglu, Fugger, Aachen |
| c3 Şehirlerin İsyanı | c3s1–c3s9 | 04:19–05:08 | 49,5 | 614 | ses_ham/c3_v1.mp3 | 0,193 | Komünero, Villalar, Padilla, María Pacheco, Germanía |
| c4 Worms'ta Bir Keşiş | c4s1–c4s16 | 05:11–07:05 | 113,8 | 1361 | ses_ham/c4_v1.mp3 | 0,130 | Jörg, Worms, Wartburg |
| c5 İmparator Hep Başka Yerde | c5s1–c5s15 | 07:08–08:52 | 104,4 | 1329 | ses_ham/c5_v1.mp3 | 0,214 | Şarlken, sedyeyle, Worms, Augsburg, Speyer, Mühlberg, Melanchthon, Moritz, Tiziano |
| c6 Kral, Esir, Düello | c6s1–c6s14 | 08:55–10:50 | 115,0 | 1411 | ses_ham/c6_v1.mp3 | 0,157 | Şarlken, Flandre, Habsburg, Cambrai, Castel Sant'Angelo |
| c7 Sultan: Hiç Karşılaşmadılar | c7s1–c7s15 | 10:53–12:38 | 105,1 | 1334 | ses_ham/c7_v1.mp3 | 0,113 | Şarlken, Lajos (II. Lajos), yedi sekiz yüz, Habsburg, Mohaç, Güns |
| c8 Akdeniz'de Barbaros | c8s1–c8s11 | 12:41–13:52 | 70,7 | 929 | ses_ham/c8_v1.mp3 | 0,147 | Şarlken, Halkulvadi, Cortés / Hernán, kaptan-ı derya |
| c9 Yeni Dünya: Altın, Gümüş ve Vicdan | c9s1–c9s14 | 13:55–15:43 | 108,3 | 1343 | ses_ham/c9_v1.mp3 | 0,178 | Şarlken, Tenochtitlan, Valladolid, Cortés / Hernán, Cajamarca, Atahualpa, Pizarro, Sepúlveda, Las Casas, Elcano, Primus circumdedisti me |
| c10 Faturayı Kim Ödedi? | c10s1–c10s9 | 15:46–16:50 | 63,9 | 868 | ses_ham/c10_v1.mp3 | 0,113 | Şarlken, Fugger, Potosí, Welser |
| c11 Adamın Kendisi | c11s1–c11s9 | 16:53–17:57 | 63,2 | 782 | ses_ham/c11_v1.mp3 | 0,086 | Şarlken, Habsburg |
| c12 Bırakmak | c12s1–c12s10 | 18:00–19:35 | 95,3 | 1197 | ses_ham/c12_v1.mp3 | 0,090 | Şarlken, Yuste, Juana, Orange, Willem |
| c13 Hesap | c13s1–c13s10 | 19:38–20:58 | 80,2 | 1026 | ses_ham/c13_v1.mp3 | 0,079 | Şarlken, Habsburg, Augsburg |

**Whisper WER'e göre dinleme sırası** (yüksekten düşüğe): c5 (0,214), c3 (0,193), c9 (0,178), c6 (0,157), c8 (0,147), c2 (0,141), c4 (0,130), c7/c10 (0,113), c12 (0,090), c11 (0,086), c13 (0,079). c0 ve c1 ölçülmedi (Scribe ile sözcük düzeyinde temiz).

**Yeniden üretim akışı** (mevcut betiklerle; ben çalıştırmadım): 1) `python3 -c "import script; print(script.chapter_text('cN'))"` çıktısını (yalnız bölüm metni) ElevenLabs'e verip `ses_ham/cN_v2.mp3` olarak kaydedin; 2) `python3 ses_birlestir.py cN=v2` (diğer bölümler v1 kalır; `out/voice.wav`, `out/voice_chapters.json`, `out/voice_for_scribe.mp3` yenilenir); 3) `out/voice_for_scribe.mp3`'ü Scribe ile yeniden dökün (`out/scribe_words.json`); 4) `python3 ses_hizala.py` (`out/timeline.json` yenilenir); 5) görüntüyü yeniden render edin: bölüm süresi değiştiği için **sonraki tüm bölümlerin zamanları kayar**. Başlamadan `out/` klasörünü yedekleyin.

### 7.1 Metin düzeltmesi yapılırsa hangi bölümler birlikte yeniden üretilmeli

`kaynaklar.md` §5'teki öneriler uygulanırsa her bölüm tek seferde yeniden üretilir (aşağıdaki sayılar o bölümde değişecek cümle sayısıdır):

| Bölüm | Değişecek cümleler | Zorunlu mu |
|---|---|---|
| c0 | YÜKSEK: c0s4; ORTA: c0s11; DÜŞÜK: c0s5 | önerilir (YÜKSEK) |
| c1 | ORTA: c1s4; DÜŞÜK: c1s12, c1s13 | isteğe bağlı |
| c2 | YÜKSEK: c2s9; DÜŞÜK: c2s7 | önerilir (YÜKSEK) |
| c3 | ORTA: c3s2 | isteğe bağlı |
| c5 | YÜKSEK: c5s12; ORTA: c5s10; DÜŞÜK: c5s3 | önerilir (YÜKSEK) |
| c6 | KRİTİK: c6s10; ORTA: c6s3, c6s4; DÜŞÜK: c6s1 | EVET (kesin hata c6s10) |
| c7 | ORTA: c7s11; DÜŞÜK: c7s7 | isteğe bağlı |
| c8 | ORTA: c8s5, c8s8; DÜŞÜK: c8s9, c8s11 | isteğe bağlı |
| c9 | DÜŞÜK: c9s10 | isteğe bağlı |
| c10 | DÜŞÜK: c10s3 | isteğe bağlı |
| c11 | ORTA: c11s7; DÜŞÜK: c11s5 | isteğe bağlı |
| c12 | DÜŞÜK: c12s1, c12s2 | isteğe bağlı |
| c13 | YÜKSEK: c13s5; ORTA: c13s3, c13s6 | önerilir (YÜKSEK) |

Not: c5'te 'sedyeyle' çıkarılırsa c5 yeniden üretilir (aynı turda 'Moritz'i 'Morits' yazmak ve 'Aogsburg'ü dinlemek mantıklı). c9 iki dinleme noktası (Tenoçtitlan; Valyadolid/Primus) içerdiğinden tek yeniden üretimle ikisi de düzelir.

### 7.2 PRON önerileri (yalnız yeniden üretim yapılırsa)

`script.py` değiştirilmedi. Bir bölüm zaten yeniden üretilecekse okunuş yazımları şöyle değiştirilebilir:

| Terim | Mevcut PRON | Öneri | Gerekçe |
|---|---|---|---|
| Jörg (c4s15) | Yörg | Yörk | Almancada sondaki g sertleşir; iki ASR de zaten 'Yörk' duydu. Ekran 'Jörg' kalabilir. |
| Flandre (c1s1, c6s5) | Flandre | Flandra (gösterim ve okunuş) | Türkçe yerleşik biçim; iki ASR 'Flandra' duyuyor. |
| Lajos (c7s3) | Lajoş | Layoş | Macarca j = y; Scribe zaten 'Layoş' çözdü. |
| Moritz (c5s11) | Moritz | Morits | 'tz' Türkçe okuyuşta belirsiz. |
| María Pacheco (c3s6) | Maria Pacheko | Maria Paçeko (isteğe bağlı) | Whisper 'Paçeko' yazdığına göre ch -> ç zaten doğru okunmuş; yalnız yeniden üretim yapılırsa güvene alınabilir. |
| Primus circumdedisti me (c9s14) | Primus sirkumdedisti me | Primus kirkumdedisti me | Latincede 'circum'daki ikinci c hep k; 's' neredeyse hiç doğru değil. |
| yedi sekiz yüz (c7s11) | yedi sekiz yüz | yedi yüz ile sekiz yüz arası | 7.800 yanlış anlaması riskini kaldırır (metin değişikliği). |
| sedyeyle (c5s12) | sedyeyle | (sözcüğü metinden çıkarın) | Kaynaksız ayrıntı + ASR'de 'Sedia'yla'. |
| Yuste (c12s8) | Yuste | Yuste (değiştirmeyin; dinleyin) | Whisper 'Yüste' yazdı; ses ü'ye kayıyorsa 'Yuuste' gibi uzatılmış yazım denenebilir. |

