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
