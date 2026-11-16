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
1. **Yaptıkların Bir Gün Sana Döner mi? | Kurosawa'nın Kral Lear'ı** (önerilen: kişisel soru önde, tanıdık kapı arkada)
2. Kral Lear Masum muydu? Kurosawa Ona Bir Geçmiş Verdi | Ran
3. Kurosawa Kral Lear'ı Japonya'ya Taşıdı: Ran (1985)
- "Ran (1985)" açıklamanın ilk satırında ve etiketlerde; başlıkta yer kalırsa sonda.

**Kapak adayları** (tek odak; tek vurgu rengi = ateş kırmızısı; Bebas ≥ 290 px; sağ alt boş):
- **A:** gece, mürekkep siyahı kale, pencerelerden ve çatıdan kırmızı ateş; önde, kapıdan yürüyerek çıkan küçük yaşlı figür (arkası ateşe dönük, ¾). Yazı: **"EKTİĞİNİ BİÇTİ"**. Filmin ilk karesi. Filmden ayrım: beyaz makyaj yok, askerler arasındaki merdiven kompozisyonu yok, kale tasarımı filmden değil dönem fotoğraflarından (Kumamoto/Himeji, 1870'ler).
- **B:** üç ok, biri kırık, kırmızı zemin üstünde mürekkep. Yazı: **"ÜÇ OK, ÜÇ OĞUL"**. Film ~4. saniyede okları gösterir.
- Hassasiyet notu (başkan): "EKTİĞİNİ BİÇTİ" bir hüküm; yorumu izleyiciye bırakmıyor ama kullanıcının okumasıyla ve Kurosawa'nın eklemesiyle uyumlu. Kalenin kadınlarının toplu ölümü, seppuku, kafa kesme sahneleri **çizilmez**. Amida resmi kutsal imge: figürü çizilmez, kapalı ya da yüzü görünmeyen kumaş olarak gösterilir.

## Kredi (tahmin)
~60 cümle × ~95 karakter ≈ 5.700 karakter × 2 çekim ≈ **11.400 karakter** (Kafka 10.832). Kesin sayı senaryo kesinleşince bildirilir.
