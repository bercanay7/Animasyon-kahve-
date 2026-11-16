# Kurosawa, *Ran* (1985): üretim planı (rev0, 16 Kasım 2026)

Durum: talep kontrolü yeniden ölçüldü; yorum kullanıcıyla kurulacak (sorular soruldu). Senaryo, iskelet ve paketleme taslağı sorulardan sonra.
Bölüm: Ekrandaki Felsefe (kanalın ilk film videosu).

## Talep kontrolü (a): tanınırlık
YouTube otomatik tamamlama (`suggestqueries-clients6.youtube.com`, hl=tr, gl=tr), 16 Kasım 2026:

| Arama | Otomatik tamamlama | Okuma |
|---|---|---|
| "ran filmi" | inceleme, 1985 | **Zayıf.** Tek başına "ran" konuya hiç ulaşmıyor (ranch simulator, randevu, range rover) |
| "ran kurosawa" | trailer, full movie, execution, battle scene, burning castle, analysis, soundtrack, reaction (hepsi İngilizce) | Uluslararası sinefil ilgisi var; Türkçe yok |
| "akira kurosawa" | **düşler**, dreams, filmleri, türkçe, düşler türkçe dublaj, ran, rashomon, oscar, seven samurai | **Orta.** Türk izleyicinin kapısı *Düşler* |
| "kurosawa" | filmleri, dreams, düşler, Ghost of Tsushima "kurosawa mode" | Oyun kitlesi de adı tanıyor |
| "yedi samuray" | fragman, inceleme | Orta-zayıf |
| "rashomon" | inceleme, akutagawa; anime karışıyor (BSD, Battle Cats) | Karışık |
| "kral lear" | sesli kitap, **Haluk Bilginer**, tirad, **Cüneyt Gökçer**, Edmund tirad, radyo tiyatrosu, özet, Goneril, film | **Güçlü.** Tiyatro ve sesli kitap kitlesi |
| "king lear" | summary, türkçe, Ian McKellen, analysis, Anthony Hopkins | |
| "nankör evlat" | sözler, Aykut Elmas | Lear'ın kendi sözü ("nankör bir evlat sahibi olmak yılan dişinden keskindir", I.iv; dize no. doğrulanacak) |
| "evlat" | ... **evlat ayrımı yapan anne baba**, evlat acısı | Kişisel damar |
| "miras kavgası" | Güldür Güldür, Gönül Dağı, kardeşlerim, rüyada | **Çok güçlü gündelik damar:** Türk dizilerinin ve hayatın konusu |
| "yaşlanınca" | "yaşlanınca görecem yanında kalanı" | Kişisel damar (şarkı/söz) |
| Kontrol: "dönüşüm kafka" | özet, analiz, animasyon, felsefesi | Kafka güçlüydü |
| Kontrol: "sisifos" | söyleni, felsefesi, hikayesi | |
| Kontrol: "milton" | futbolcu, Friedman, kasırga | Konuya ulaşmıyor (Milton zayıftı) |

**Sonuç (a):** "Ran" adı Milton düzeyinde zayıf; "Kurosawa" orta; "Kral Lear" güçlü. Tanıdık kapı **Kral Lear**; ikinci kapı Kurosawa (Düşler). "Ran" başlığın sonunda künye olarak durabilir, kapakta değil.

## Talep kontrolü (b): kişisel soru (sınanacak)
Arama damarları: miras kavgası, evlat ayrımı, nankör evlat, "yaşlanınca yanında kalan".

| Aday | Not |
|---|---|
| "Yaptıkların bir gün sana döner mi?" | Ran'ı Lear'dan ayıran şey tam bu: Kurosawa yaşlı kralı masum bırakmaz, ona kanlı bir geçmiş verir (DOĞRULANACAK: Kurosawa'nın kendi sözü). Kafka'nın "koşullu sevgi"sinden ayrı damar |
| "Kardeşleri miras neden düşman eder?" | Gündelik damar en güçlüsü; ama Ran'ın derin sorusu değil, yüzeyi |
| "Elinden güç gidince seni kim sever?" | Kafka'ya çok yakın (koşullu sevgi); elenmeye aday |
| "Çocuklarına ne bırakırsın?" | Yumuşak; tetikleyici değil |

## Açık işler
- Yorum (kullanıcıyla), iskelet seçimi (Kafka = Kişōtenketsu; tekrar edilmeyecek), başlık + kapak ilk taslağı, kaynak klasörü (`kaynak/`: Kral Lear İngilizce özgün metin satır numaralı; Kurosawa kaynak notları).
- Üslup kapısı: cinecode `ukiyoe` ve `ink-wash` tarifleri; LemoLab demo motorları (MIT, commit d33bdea) indirilip tek betiğe paketlenecek.

## Gerçek görseller (kullanıcının isteği, 16 Kasım: "yer yer, hepsi değil")
Kural: yalnız **kamu malı (PD) ve CC0**; CC BY künyeyle. **Kullanılmaz:** CC BY-SA ve BY-NC (para kazanan kanal), Ran'dan kare, afiş, fragman ve 1985 çekim fotoğrafı, Kurosawa'nın resimleri ve storyboard'ları (Japonya'da ölümden sonra 70 yıl telifli: 1998 + 70 → 2068), eşi Yōko'nun ve ailesinin fotoğrafları. Her varlık `kaynak/GORSELLER.md`'ye (kaynak URL, envanter no, lisans, erişim tarihi) ve `araclar/ASSETS.md`'ye işlenir; künye `youtube.md`'de. Gerçek kişiye söz uydurulmaz; fotoğrafın altına yalnız kaynakta yazan bilgi.

İlk yoklama (16 Kasım, API ile):
| Malzeme | Kaynak | Lisans | Ne için |
|---|---|---|---|
| David Garrick Kral Lear rolünde (James McArdell, 1761; Met 707787, 707788) | Met Open Access | CC0 (`isPublicDomain: true`) | Lear'ın 400 yıllık sahne geçmişi |
| Lear ve Cordelia (Bartolozzi ~1783, Met 713083; Heath 1825–40, Met 739728); "King Lear" (William Sharp 1783, Met 707789) | Met Open Access | CC0 | IV.7 barışma sahnesi |
| Nō maskesi, 1336–1573 (Met 60220); "Kojo" yaşlı adam maskesi, 19. yy (Met 45140) | Met Open Access | CC0 | Kurosawa'nın Nō'dan aldığı (kendi sözüyle DOĞRULANACAK). Filmdeki makyaj çizilmez, gerçek tarihî maske gösterilir |
| Sesshū Tōyō okulu resimleri (Met 45649, 54576; tarihleri 17.–19. yy kopyaları: "Sesshū'ya göre" diye yazılır) | Met Open Access | CC0 | Üslubun geleneği (suiboku) |
| Kurosawa ve Mikio Naruse, *Nadare* çekimi, 1937 (P.C.L.) | Wikimedia Commons | PD-Japan-oldphoto | Genç asistan Kurosawa |
| Kurosawa, *Yedi Samuray* setinde, 1953 (dergi taraması) | Wikimedia Commons | PD-Japan-oldphoto | Ustalık dönemi |
| Mōri Motonari portresi; First Folio (1623) Lear sayfası; 1870'ler Kumamoto/Himeji kale fotoğrafları | Commons / müzeler | yoklanacak (PD-Art; Folger CC BY-SA ve Bodleian BY-NC **elenir**) | Üç ok efsanesi; Lear'ın ilk baskısı; dönem kalesi |

ABD durumu: PD-Japan-oldphoto, 1956 sonundan önce çekilmiş fotoğraflar 1970'te Japonya'da kamu malı olduğundan URAA ile ABD'de yeniden telife girmez (Commons'un kabul ölçütü). Senaryo aşamasında her dosyanın sayfası ayrıca okunur.

## Üslup adayları (cinecode, konuya göre)
| Tarif | Rol | Not |
|---|---|---|
| `ukiyoe` | Ana anlatım adayı 1 | Edo savaşçı baskıları (musha-e) Sengoku'yu anlatır; LemoLab demo motoru var (`print.js`, `nature.js`, `traveler.js`). Risk: düz renk bloklarıyla filmin renk kodlu ordularına kayma; renkler filmden uzak seçilir |
| `ink-wash` | Ana anlatım adayı 2 | Tarif Çin xieyi; Japon suiboku'ya (Sesshū, Muromachi = Ran'ın dönemi) çevrilir: Çin hattatlığı, Çin mührü ve guqin yok. Tek renk + bir kırmızı: filmin renklerinden en uzak |
| `archive-lighttable` | **Gerçek görsel araları** | Kuryenin masası: gerçek nesneler (Met baskıları, Nō maskesi, 1937/1953 fotoğrafları, First Folio) ışıklı masada, büyüteçle içine girilir; tek sinyal rengi. Canvas 2D'ye uyarlanır (demo three.js/WebGL) |
| Elenenler | `shadow-puppet`, `paper-lantern`, `papercut-red` | Çin geleneği; Japon konusunda kültür karışması (hassasiyet). `woodcut` Kafka'da kullanıldı |

## Kurul (kullanıcının kararı, 16 Kasım): bu turda kurul yok
Kapılar başkan denetimiyle geçer, `KURUL.md`'ye "kurulsuz" diye açıkça yazılır. Hassasiyet ve telif bakışı üslup kapısında başkanca yapılır.

## Yorum (kullanıcıyla birlikte, 16 Kasım)
- **Kullanıcı:** Ran'ı ~1 yıl önce izledi, çok etkilendi. Aklında kalan: **kale yanarken kralın yürüyerek çıktığı sahne.** Kral Lear'ı okudu, izlemedi. Çıkış noktası: Kurosawa'nın filmi yıllarca resim olarak önceden çizmesi ve gözleri zayıflamışken bu resimlerin çekilmesi.
  - Başkanın düzeltmesi: "kör" denmez. Kaynaklar "neredeyse kör" (TCM) ve "gözleri zayıflıyordu" diyor (K4); anlatımda "gözleri iyice zayıflamışken".
- **Kullanıcının önceki değerlendirmesi (geçmiş sohbetten):**
  1. *Oyunculuk ve kopuş:* Nō'yu andıran abartılı oyunculuk zaman zaman filmden koparıyor; savaş sahneleri ve geçmişle yüzleşme anları geri çekiyor. → Videoda dürüst bir an olur: "Bu oyunculuk bazen izleyiciyi iter; bu bir kaza değil" + gerçek Nō maskesi (Met CC0). Kurosawa'nın kendi sözü bulunamazsa "Nō geleneğini andırır" diye anlatılır (K9).
  2. *Gerçek trajedi:* Hidetora'nın asıl yıkımı oğulların ihaneti değil, kendi zalim geçmişiyle girdiği iç savaş. → **Omurga.** Kaynakla uyumlu: Kurosawa Lear'a geçmiş verdi (K1); Shakespeare'in Lear'ı "günah işlediğinden çok kendisine günah işlenmiş" (L5), Hidetora değil.
  3. *Kaede:* intikamın saf hâli, Hidetora'nın yarattığı canavar; ama aynı travmayı yaşayan Sue ve Tsurumaru gibi affetmeyi değil yıkımı seçtiği için masum değil. → **İksir.** Üç kişi aynı acı: biri yakıp yıkar (Kaede), biri affeder (Sue), biri karanlıkta kalır (Tsurumaru).
- **Kurosawa'nın hayatı:** (b) kısa çerçeve (kullanıcının seçimi): 75 yaş, on yıla yakın para arama, resimlerle çekilen film, eşinin ölümü ve bir günlük ara. Heigo ve 1971 **girmez**.
- **Başkanın kararı: kişisel soru** iki katlı. Kanca ve başlık: **"Yaptıkların bir gün sana döner mi?"** (Hidetora; Kurosawa'nın Lear'a eklediği). Kapanış: **"Peki sana yapılanla ne yaparsın?"** (Kaede ile Sue). Kafka'nın "koşullu sevgi"sinden ayrı damar: orada sevilenin koşulu, burada eylemin sorumluluğu.

## Hikâye iskeleti: Harmon çemberi (seçildi)
- **Neden:** Hidetora tam bir çember çizer: tahtından iner, yabancı dünyaya (kendi oğullarının kapısına, kendi yıktığı kalelerin harabesine) düşer, bedeli öder, Saburo'ya döner ve ölür. 6. adım (bedel) kanalın "yolculuk nerede kırıldı?" imzası ve kullanıcının sahnesi: yanan kale. Önceki video Kafka = Kişōtenketsu, ondan önce İkaros = Harmon; art arda değil. Süsü değiştirildi: İkaros'ta kahraman Daidalos'tu, çember baba-oğuldu; burada çember **geçmişin geri dönüşü** ve Kurosawa çerçevesi.
- **Kahraman:** Hidetora. İkinci eksen Kurosawa (75 yaş, kendi "son büyük filmi"); üçüncü eksen izleyici (iksir).
- **Açılış (kanca):** olayın ortası: yanan kale, yaşlı adam yürüyerek çıkıyor (kullanıcının sahnesi; kapak A). İlk cümlede soru.

| Adım | İçerik | Cümleler (taslak) |
|---|---|---|
| 0. Kanca | Yanan kale; "Bu adam elli yılda kurduğu her şeyi kendi elleriyle verdi. Yaptıkların bir gün sana döner mi?" L1 açılır | A01–A04 |
| Çerçeve | Kurosawa 75 yaşında; bu sahneyi on yıl önce resim olarak çizmişti; para yok; gözleri zayıflıyor (K3–K5). Kral Lear'ın Japonya'ya taşınmışı; L2 açılır: "Shakespeare'in unuttuğu tek şeyi ekledi" | A05–A10 |
| 1. Konfor | Hidetora, 70 yaşında; elli yılda kurduğu ülke; av | B01–B03 |
| 2. İhtiyaç | Dinlenmek ama unvanı korumak; ülkeyi üç oğluna bölmek; üç ok (Mōri, K2); Saburo okları kırar, sürülür. Lear'la eşleme: üç kız → üç oğul (L2, L3) | B04–B10 |
| 3. Yabancı dünya | Taro, sonra Jiro kapıyı kapar; Kaede'nin geçmişi: ailesini Hidetora öldürmüştü (L2 kapanır: geçmiş) | C01–C07 |
| 4. Uyum | Kendi yıktığı kalelerin arasında dolaşır; Sue ve kör Tsurumaru (Hidetora'nın kör ettirdiği): affeden ve affedemeyen (L3 açılır) | C08–C14 |
| 5. "Ödül" | İstediği oldu: artık hükmetmiyor. Ama bu bir ödül değil | D01–D02 |
| 6. Bedel (kırılma) | **Yanan kale** (kancaya dönüş, L1 kapanır): adamları ölür, kılıcı kırık; yürüyerek çıkar, deliliğe. Lear'ın fırtınası (L4, L5): "Lear masumdu; Hidetora değil". Nō anı: abartılı oyunculuk (kullanıcının notu) + gerçek maske. Kurosawa: kale gerçekten yakıldı, tek çekim (K7); eşinin ölümü, bir gün ara (K6) | D03–D14 |
| 7. Dönüş | Saburo onu bulur; barışma (Lear-Cordelia IV.7, L7; Met CC0 gravürü); Saburo vurulur, Hidetora ölür (görsel olarak işlenmez) | E01–E06 |
| 8. Değişim / iksir | Kaede'nin sonu; Tsurumaru uçurum kenarında, Sue'nün verdiği resim düşer. Üç kişi aynı acı, üç seçim (L3 kapanır). "Yaptıkların sana döner. Ama sana yapılanla ne yapacağın senin." Abone çağrısı doruk anında; bitiş ekranı: Prometheus ya da Sisifos | E07–E14 |

Toplam ~58–62 cümle; hedef **8 dk** (başkan kararı).

### Merak döngüleri
- **L1 (A01 → D05):** "Bu yaşlı adam kendi kalesinden neden tek başına, kılıçsız çıkıyor?"
- **L2 (A09 → C06):** "Kurosawa, Shakespeare'in unuttuğu tek şeyi ekledi." → geçmiş.
- **L3 (C12 → E12):** "Aynı acıyı yaşayan üç kişi var; biri canavara dönüşecek."
- **ABT:** her bölümde bir AMA ("ama okları kıran oğul sürüldü", "ama kapıyı kapatan kadının bir geçmişi vardı", "ama Hidetora Lear değildi").

## Paketleme taslağı (senaryodan önce)
**Başlık adayları** (<60 karakter; "NEDEN …?" ve Kafka'nın "X'in Y'si: soru" kalıbından kaçınılır):
1. **Yaptıkların Sana Döner mi? | Kurosawa'nın Kral Lear'ı** (52 karakter) (önerilen: kişisel soru önde, tanıdık kapı arkada)
2. Kral Lear Masum muydu? Kurosawa Ona Bir Geçmiş Verdi | Ran
3. Kurosawa Kral Lear'ı Japonya'ya Taşıdı: Ran (1985)
- "Ran (1985)" açıklamanın ilk satırında ve etiketlerde; başlıkta yer kalırsa sonda.

**Kapak adayları** (tek odak; tek vurgu rengi = ateş kırmızısı; Bebas ≥ 290 px; sağ alt boş):
- **A:** gece, mürekkep siyahı kale, pencerelerden ve çatıdan kırmızı ateş; önde, kapıdan yürüyerek çıkan küçük yaşlı figür (arkası ateşe dönük, ¾). Yazı: **"EKTİĞİNİ BİÇTİ"**. Filmin ilk karesi. Filmden ayrım: beyaz makyaj yok, askerler arasındaki merdiven kompozisyonu yok, kale tasarımı filmden değil dönem fotoğraflarından (Kumamoto/Himeji, 1870'ler).
- **B:** üç ok, biri kırık, kırmızı zemin üstünde mürekkep. Yazı: **"ÜÇ OK, ÜÇ OĞUL"**. Film ~4. saniyede okları gösterir.
- Hassasiyet notu (başkan): "EKTİĞİNİ BİÇTİ" bir hüküm; yorumu izleyiciye bırakmıyor ama kullanıcının okumasıyla ve Kurosawa'nın eklemesiyle uyumlu. Kalenin kadınlarının toplu ölümü, seppuku, kafa kesme sahneleri **çizilmez**. Amida resmi kutsal imge: figürü çizilmez, kapalı ya da yüzü görünmeyen kumaş olarak gösterilir.

## Kredi (tahmin)
~60 cümle × ~95 karakter ≈ 5.700 karakter × 2 çekim ≈ **11.400 karakter** (Kafka 10.832). Kesin sayı senaryo kesinleşince bildirilir.

## Ek (16 Kasım): kullanıcının ikinci sahnesi: kör Tsurumaru ve flüt
Kullanıcı: "Sondaki kör flüt sahnesi de çok etkileyiciydi." Kaynaklardaki sıra (Wikipedia olay örgüsü; moviemistakes "ending"; DBU makalesi; bağımsız iki özet aynı):
1. **Kulübe:** Hidetora sığındığı kulübede, ailesini öldürüp kör ettirdiği Tsurumaru'yla karşılaşır. Tsurumaru ona flüt çalar; Hidetora bu ezgiyle sarsılır (kullanıcının 1. notundaki "geçmişiyle yüzleştiği an").
2. **Flüt Sue'nün hediyesi:** sürgüne giderken vermiştir. Harabeye kaçarken flüt kulübede unutulur; Sue ona yoldaş olsun diye Amida resmini bırakıp flütü almaya döner ve **geri gelmez** (Jiro'nun adamlarınca öldürülür; görsel olarak işlenmez).
3. **Son:** Tsurumaru harabe kalenin surunda yapayalnız; **flütü yok**, ablası yok, elinden Amida resmi de düşer.
- Kesinlik notu: son sahnede flüt çalınmıyor (kaynaklara göre flüt kaybolmuştur). Kullanıcının hatırladığı ezgi büyük olasılıkla kulübe sahnesi ya da müzik. Anlatımda "son sahnede flüt çalar" denmez.

**Senaryoya etkisi (başkan kararı):**
- **Flüt filmin ses motifi olur:** mürekkep dünyasında tek "ses nesnesi". Kulübede çalar (adım 4), Sue onun için geri döner (adım 7), sonda yoktur (adım 8): sessizlik. İksirin karşılığı: Sue'nün affı bir ezgi kadar küçük ve kırılgan; Kaede'nin intikamı bütün bir hanedanı yakar.
- **Yeni döngü L4 (C10 → E10):** "Sue o gece neden geri döndü?" → bir flüt için.
- **Müzik:** flüt ezgisi özgün sentez (`audio/score.py`; shakuhachi/nōkan benzeri nefesli). **Tōru Takemitsu'nun Ran müziği telifli: ne ezgi ne motif taklit edilir.**
- **Hassasiyet:** Tsurumaru onurlu çizilir; göz yarası, kan yok; "kör" bir hakaret sıfatı gibi değil, Hidetora'nın yaptığının sonucu olarak söylenir ("Hidetora'nın kör ettirdiği çocuk"). Amida resmi kutsal imge: figür çizilmez, sarılı kumaş.
- **Kapanış planı:** son geniş plan: surda tek, küçük figür, gün batımı boşluğu; flüt sesi yok; tek kırmızı nokta (düşen resmin şeridi). **Shorts adayı** bu an + kanca "Bir flüt için geri döndü".
- **Kapak B alternatifi:** surda yalnız kör figür, yazı "FLÜTÜ GERİDE KALDI" (üç ok ile karşılaştırılacak; ilk saniyelerde karşılanması için açılış montajına bir an konur).

## Senaryo rev0 (16 Kasım; başkan taslağı, kurul yok): iskelet → cümle
66 cümle, 771 kelime (Kafka 708 kelime = 6:39) → tahmini **~7:15–7:45**. Kral Lear dizeleri `KL1–KL8`, Kurosawa bilgileri `K1–K10` (`kaynak/KAYNAKLAR.md`). Film diyaloğu alıntılanmadı. Olay örgüsü sırası filme göre düzeltildi: yanan kale, harabe ve flütten **önce** gelir.

| Harmon adımı | Cümleler |
|---|---|
| 0. Kanca (yanan kale, soru) | A01–A05 |
| Çerçeve: Kurosawa'nın resimleri, Lear | B01–B07 |
| 1. Konfor | C01 |
| 2. İhtiyaç: bölüşme, üç ok, Saburo'nun sürgünü | C02–C09 |
| 3. Yabancı dünya: kapılar, Kaede'nin geçmişi (L2 kapanır) | D01–D09 |
| 4–5. Uyum ve ters ödül: Saburo'nun boş kalesi | E01–E02 |
| 6. Bedel: yanan kale (L1 kapanır), Lear'ın fırtınası, Nō anı | E03–E11 |
| 6b. Yüzleşme: flüt, Sue, Kaede | F01–F07 |
| 7. Dönüş: Saburo, Cordelia, ölümler, Sue'nün dönüşü (L4) | G01–G07 |
| 8. Değişim / iksir: surdaki adam, üç seçim (L3), Kurosawa, iki soru, abone, bitiş ekranı | H01–H11 |

Değişiklikler (doğrulanamayan için): "yetmiş yaşında" ve "elli yıl" çıkarıldı (kaynakta bulunmadı; "bütün ömrünü"); "kale Kaede'nin ailesinindi" çıkarıldı (yalnız "ailesini kılıçtan geçirmişti" doğrulandı); Saburo okları dizinde kırar (doğrulandı); Sue Hidetora'yı affetti (B güven). Japonca adlar: `tts`'te Mōri → Mori, Yōko → Yoko.

## Üslup kararı (başkan, 16 Kasım; üslup kapısı karesi henüz yok)
İki LemoLab demo motoru (MIT, commit d33bdea) indirildi ve başsız Chromium'da çalıştırıldı; kareler `uslup/lemo_demo_karsilastir.jpg` (üst sıra ukiyoe, alt sıra ink-wash). Ağ çağrısı yok (yalnız kendi `lines.json`, `voices/dur.json`, `fonts.css`).

**Seçilen: `ink-wash` motoru, Japon suiboku'ya (Sesshū, Muromachi) çevrilerek + gerçek görsel araları.**
- Neden: Ran bir çöküş trajedisi; boş kâğıt (留白) = harabe, sis, duman ve filmin sonundaki sessizlik (H03 "Hiçbir ses yok"). Tek kırmızı = **ateş** (yanan kale, kapak A) ve sonda düşen resmin şeridi. Tek renk, filmin renk kodlu ordularını ve Emi Wada kostümlerini kopyalama riskini sıfırlar. Xieyi figür (soluk kütle + iki yüklü fırça darbesi, yüz 3–5 darbe) oyuncuya benzemeyi ve beyaz makyajı kendiliğinden dışarıda bırakır. Kodla çizimin zayıf yanı (yüz, el) bu üslupta zaten gösterilmez.
- `ukiyoe` elendi: demo neşeli bir seyahat afişi (Fuji, pirinç tarlası, *Büyük Dalga*'yı andıran dalga: tarif de bunu yasaklar); trajediye ters; renk blokları filmin sancak renklerine kayar. Dönem de geç (Edo).
- **Japonlaştırma (hassasiyet, kültür karışmasın):** Çin hattatlığı (`glyph.js`) kullanılmaz; ekran yazısı Türkçe; mühür Çince karakter değil kanalın kendi işareti (ör. kırmızı kare içinde "ZK" ya da boş mühür); guqin yerine özgün shakuhachi/nōkan benzeri nefesli + taiko (`audio/score.py`, Takemitsu taklidi yok); manzara Japon: kale (1870'ler fotoğraflarına göre, filmin kalesi değil), volkanik ova, sur. Japon kültürü klişe değil: geyşa, katana pozu, kiraz çiçeği süsü yok.
- **Gerçek görsel araları:** `archive-lighttable` demosu depoda yok (404); tarif okunup kendi Canvas 2D sürümümüz kurulur: koyu masa üstünde pirinç kâğıdına tutturulmuş gerçek nesne (Met CC0 Lear baskıları, Nō maskesi, Kurosawa 1937/1953 fotoğrafları), büyüteçle yaklaşma, künye kartı. Mürekkep dünyasıyla aynı kâğıt tonu: kopuk durmasın.
- Paketleme: `kafka/tools/bundle_woodcut.py` gibi `tools/bundle_ink.py` → `lib/ink.bundle.js`; `Math.random` varsa tohumlanır.
- Sonraki adım: üslup kapısı (manzara: yanan kale gece + orta plan: kulübede Hidetora ve Tsurumaru + yakın plan: flüt tutan eller ya da yüzü görünmeyen baş + 15 sn hareket: kaleden inen figür) + bir arşiv arası karesi. Kurul yok; hassasiyet ve telif bakışı başkanca.
