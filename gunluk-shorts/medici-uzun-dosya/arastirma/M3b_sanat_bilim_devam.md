# M3b — SANAT, BİLİM, DÜŞÜNCE, KURUMLAR (DEVAM)

**Kapsadığı bölümler:** c14 (bilim, müzik) · c11 (Michelangelo–Medici, Machiavelli) · c16 (popüler kültür, "Medici etkisi", kurumların etkisi) · c12 (Accademia, Uffizi, Boboli) · c4–c7 (diğer patronlar, hümanistler, anekdot zincirleri)
**Hazırlayan:** araştırma ajanı M3b (M3'ün devamı) · **Tarih:** 18 Ekim 2026 · **Durum:** olgu dosyası (senaryo değil); git commit/push yapılmadı
**Okuma kuralı:** Bu dosyada **hiçbir satır "kesin" değildir**; ● sınıfı yoktur (bir sayfa bile açılıp okunamadı). Her satırın sınıfına bak. **HAFIZA** = araçla doğrulanmamış, senaryoya girmeden önce doğrulanmalı. Bu dosya M3'ün yerine geçmez, onu **tamamlar**: M3'ün satır numaraları `§2 #n` (kronoloji), `§3 #n` (canlı ayrıntı), `§5.n` (mit), `§9 #n`, `§10 #n` biçiminde anılır.

---

## 1. Başlık notu: araçlar, sınırlar, okuma kılavuzu

### 1.1 Hangi araçlar çalıştı?

- **WebSearch: çalıştı. 60 sorgu hakkının tamamı kullanıldı** (58'i sonuç döndürdü; 8'i `extended`, 50'si `standard`; 2'si `400` hatası verdi, kotadan düşüp düşmediğini bilemediğim için muhafazakâr davranıp hakka saydım). Dönenler **arama aracının ürettiği özetlerdir**; sayfa metni bana gelmedi. Özetler bazen kendi bilgisini ya da "bulamadım" notunu ekliyor; bunları olduğu gibi işaretledim. Bir özetin kendi yorumunu **yanlış bulduğum bir yer** var: Britannica'nın Uffizi'yi "Büyük Dük Leopold I" ile ilişkilendirmesine özet "hata" dedi; oysa Pietro Leopoldo Toskana Büyük Dükü olarak **I. Leopoldo** sayılır (sonradan imparator II. Leopold; HAFIZA, Y). Britannica doğru görünüyor.
- **WebFetch: tek deneme, başarısız.** `https://dhspriory.org/kenny/PhilTexts/Machiavelli/Letter%20to%20Vettori.htm` → `getaddrinfo ENOTFOUND dhspriory.org`. Görev kuralı gereği ikinci deneme yapılmadı. **Sonuç: ● yok.** Birincil metinler (Vettori mektubu, Condivi, Cellini, Vasari, Marriott çevirisi) yalnız **arama özetindeki alıntılar** olarak görüldü; özgün İtalyanca/Latince hiçbir yerde görülmedi.
- **`allowed_domains` uyarısı:** `eurogamer.net`, `ign.com`, `polygon.com` bu aracın kullanıcı ajanı için **erişilemez** (400 hatası, 2 sorgu boşa gitti). Oyun basını için `pcgamer.com`, `kotaku.com`, `gamesradar.com`, `gamespot.com` çalıştı.

### 1.2 Hangi `allowed_domains` işe yaradı?

| Alan adı | Sonuç |
|---|---|
| `treccani.it` | **En verimli:** Accademia di San Luca / Zuccari (DBI), Leopoldo ve Cimento (DBI). Kurumsal İtalyanca tanıklık |
| `uffizi.it` | Uffizi'nin kamusallaşması (24 Haz 1769) ve Boboli tarihi: resmî sayfa |
| `metmuseum.org` | Cristofori denemesi (1700 envanteri, Meccoli, Maffei, 3 hayatta kalan piyano) |
| `museogalileo.it`, `catalogue.museogalileo.it` (+ `brunelleschi.imss.fi.it` yansıma sayfaları) | Cimento, Vinta, Niccolini, pusula kitabı |
| `britannica.com` | Camerata, Yeni Sakristi, Euridice; kısa ama güvenilir |
| `plato.stanford.edu`, `iep.utm.edu` | Ficino ve "Akademi" sorusu: iki bağımsız ansiklopedi |
| `gutenberg.org`, `wikisource.org`, `archive.org` | **İngilizce çevrilmiş birincil metinlerin** (Symonds, Holroyd/Condivi, Cellini, Vasari-Fordham) özetlerini getirdi; tam sayfa değil |
| `palazzostrozzi.org` (+ Wikipedia, Britannica) | Palazzo Strozzi tarihi |
| `pcgamer.com`, `kotaku.com`, `gamesradar.com`, `gamespot.com` | *Assassin's Creed II* basın/röportaj özetleri (Désilets röportajı Kotaku'da) |
| `dokumen.pub` | Bu turda **işe yaramadı** (Johansson için denendi; alakasız kitaplar döndü) |
| `galileo.rice.edu` | Yalnız ana sayfa ve bir portre; ders verme ayrıntısı çıkmadı |
| `gamedeveloper.com`, `gamasutra.com` | Hiçbir doğrudan sonuç getirmedi |

### 1.3 Sınıf anahtarı (bu dosyada)

| Sınıf | Anlam |
|---|---|
| ● | **Hiç verilmedi** (WebFetch çalışmadı) |
| ◐ | Arama özetinde ≥2 bağımsız ikincil kaynak ya da kurumsal/müze/ansiklopedi sayfası uyumlu. Kaynakların bağımsızlığı sınırlıysa (Wikipedia türevleri) Not'ta yazıyor |
| ○ | Tek kaynak ya da doğrulanamayan |
| ANEKDOT | Sonradan yazılmış/anlatılmış hikâye; kim yazdı, ne zaman Not'ta |
| HAFIZA | Araçla doğrulanamadı; kendi bilgim (Y/O/D) |

**Kaynak notasyonu:** `S1…S44`, dosya sonundaki **Ek A**'ya gider (konu başına dönen sayfalar; M3'ün `K` etiketleriyle karışmaz). Ek B sorgu günlüğüdür.

**Sınıf dağılımı (bu dosya):**
- **Güncelleme (§2), 38 satır** (M3 için 34, M4/M2 için 4): **28 satırda HAFIZA (Y/O/D) ya da "doğrulanmadı" → ◐** (çoğunda yıl/gün ayrıntısı HAFIZA kaldı, Not'ta yazılı); 10 satırda sınıf aynı kalıp nitelendi ya da bölündü.
- **Yeni kronoloji (§3), 106 satır (b1–b106):** ◐ 72 · ○ 22 · ◐/○ karma 12 · HAFIZA 0 · ● 0. Bunlardan **ANEKDOT 6** (b58, b102–b106), **YORUM 1** (b86).
- **Canlı ayrıntılar (§4), 34 satır (bd1–bd34):** ◐ 27 · ○ 7; ANEKDOT 5 (bd17, bd22, bd23, bd25, bd26).
- **Sayılar (§5.1), 42 satır (bs1–bs42):** ◐ 28 · ○ 3 · ◐/○ karma 11.
- **Mit/tartışma (§5.2):** 17 girdi (bm1–bm17). **TR-BAĞ (§5.3):** 3 satır (yeni doğrulanmış bağ yok; 2 HAFIZA/○ aday).
- **Sahne adayları (§6):** 3 ana + 5 kısa aday. **Okuma ipucu:** ◐ burada "arama özetinde ≥2 sayfa ya da kurum sayfası uyumlu" demektir; birçok kaynak Wikipedia, rehber, fan wiki düzeyinde. Bir olguyu senaryoya almadan önce Not'taki kurum/ansiklopedi sayfasından doğrulamak gerekir.

### 1.4 Çapraz kontrol (M1/M2/M4 ile)

| Konu | Sonuç |
|---|---|
| **Michelangelo 1529–30 ↔ M4 #30, #32, #41, §3 #14, #18** | **Çakışma yok, uyum var:** Ocak komite → Nisan "governatore e procuratore generale" (M4 ◐); Eylül 1529 kaçış (M4 ◐); bağışlanma "Yeni Sakristi'ye dönme şartıyla" (M4 ○ → bu turda ikinci kaynak: ◐). **Dikkat, iki ayrı çan kulesi:** **San Miniato al Monte** (savunma; M4 §3 #14: topçu, yün balyası) ile **San Niccolò oltr'Arno** (saklanma geleneği; arte.it, rehber). Karıştırılmamalı (b42) |
| **M4 #17, #22 (Yeni Sakristi 1519/20; Laurenziana 1524)** | Uyumlu (b32, b35) |
| **M4 #80 (Marie'nin vekâleten evliliği 5 Eki 1600)** | HAFIZA → **◐** (b4): Duomo, Kardinal Aldobrandini, Ferdinando I vekil; Lyon'da dinî tören 17 Ara 1600 |
| **M4 #105 (Patto, 3. madde: "devletin süsü, kamu yararı, yabancıların merakı")** | Uffizi resmî sayfası İngilizce "for the ornament of the State" ve "public use" ifadelerini veriyor (b77): üç öğenin ikisi için **resmî teyit**; "yabancıların merakı" hâlâ yalnız M4'ün ikincil sayfalarında |
| **M4 #95 (Cosimo II ölümü 1621)** | Yıl bu turda dolaylı göründü (○); gün hâlâ HAFIZA |
| **M1 #39 (Palla Strozzi 1427'de Floransa'nın en zengini)** | Uyumlu: Gentile da Fabriano siparişi (b83) bu servetin sanata dönüşmüş biçimi |
| **M2 K15 (Palla Strozzi 1434'te Padua'ya sürgün)** | Bu turda S33 sayfalarında **görülmedi**; M2'ye bırakıldı |
| **M2 K48 (Poliziano'nun Lorenzo'yla sakristide oluşu)** | Bu turda **bağımsız doğrulama yok**; yalnız Poliziano'nun *Commentarium*'u görgü tanığı anlatımı olarak teyit edildi (b94) |
| **M2 K92 (17 Kas 1494 Charles'ın girişi, HAFIZA-O)** | İki özet Pico'nun ölümünü **aynı güne** getirdi (b93): tarihe dolaylı destek ○ |
| **AC II fan kontrolü ("Baroncelli de Palazzo Vecchio'dan asıldı") ↔ M2 K62** | **Çelişki:** M2'ye göre Bernardo Bandini (Baroncelli) İstanbul'a kaçtı, 29 Ara 1479'da Floransa'da asıldı (◐). Kotaku'nun aktardığı fan kontrolünün bu cümlesi hatalı görünüyor; b67 (iii) o kısımda **kullanılmaz** |

### 1.5 Bu turun ana bulguları (kısa)

1. **c14'ün dört taşı HAFIZA'dan ◐'ye çıktı:** Galileo 1610, Accademia del Cimento, Peri'nin *Euridice*'si, Cristofori'nin piyanosu (b1–b31).
2. **Galileo'nun uydulara ad verme sahnesi çelişkili:** 13 Şubat 1610 mektubunda iki seçenek (*Cosmica* / *Medicea*) ◐; seçimi **kimin yaptığı** kaynaklara göre değişiyor (bm1). Kalıcı adlar Marius'un; Medici adı tutmadı.
3. **Machiavelli:** *Prens*, Lorenzo il Magnifico'ya değil **torunu Lorenzo di Piero'ya** ithaf (önce Giuliano niyeti); *Istorie fiorentine* siparişi 8 Kas 1520 (Najemy), sunum Mayıs 1526; *Prens* ilk basım 4 Oca 1532 (Blado, Folger kaydı).
4. **Michelangelo 1530'da nerede saklandı?** İki gelenek: Yeni Sakristi altı oda (2–3 ay) / San Niccolò kulesi tabanı (birkaç gün). Taraflar ayrı söylenmeli (bm8).
5. **Akademi zinciri:** Floransa 1563 → Roma ◐ ("Zuccari Floransa modelinde yeniden kurdu", Treccani); Roma → Paris ○; Paris/Roma → Londra için kanıt çıkmadı (bm11).
6. **Uffizi:** halka açılış **24 Haziran 1769** (resmî site); Capitoline 1471/1734 karşı örnek ◐. "İlk müze" denmez.
7. **Anekdotlar:** Lippi'nin çarşaf ipi **Vasari'de var** (artık kaynaklı ANEKDOT); Michelangelo'nun aylığı **5 dukat** ◐ (Condivi/Vasari çevirileri); yumurta anekdotunun **Vasari'den eski** yazılı kayıtları olabilir (Pacioli, Filicaia; ○); Leonardo'nun "at kafatası lir"i Vasari'ye ait, "Lorenzo gönderdi" bağı modern.
8. **"Platon Akademisi":** SEP ve IEP birlikte "resmî okul değil" diyor; ama Ficino'nun Eylül 1462 tarihli mektubunda "Akademi" kelimesi geçtiği aktarılıyor (○): gerilim bm10'da.
9. **Popüler kültür:** *Assassin's Creed II* sapma haritası basın/fan düzeyinde ○ (geliştirici belgesi: tek Kotaku röportajı); dizi için The Florentine'in somut hata listesi ◐; "Medici etkisi" için **tarihçi değerlendirmesi bulunamadı**.
10. **Medici-merkezli anlatıya karşı:** Palla Strozzi (1423, Gentile), Palazzo Strozzi (1489, Medici sarayını aşmak üzere), Pazzi Şapeli (1429) belgeli; aynı Brunelleschi hem Medici'nin hem Pazzi'nin şapelini tasarladı.

---

## 2. Güncelleme tablosu (M3 satırları → yeni sınıf)

Biçim: `M3 satırı (#, bölüm) | eski sınıf | yeni sınıf | not`. "Yeni olgu" için §3'e bak.

### 2.1 M3'ün kendi satırları

| M3 satırı (#, bölüm) | Eski sınıf | Yeni sınıf | Not |
|---|---|---|---|
| §2 #78 (c11) Machiavelli, *Prens*, 10 Ara 1513 Vettori mektubu | HAFIZA (Y) | **◐** | Mektup, "küçük eser" ve Giuliano'ya ithaf niyeti ≥3 çeviri/sayfada tutarlı (S15, b51). "Tem–Ara 1513 yazım" aralığı HAFIZA kaldı |
| §2 #79 (c11) *Prens*'in Lorenzo di Piero'ya ithafı, 1516 | HAFIZA (Y/O) | **◐** (Giuliano → Lorenzo geçişi) · **HAFIZA** (1516 yılı) | Basılı ithaf Lorenzo di Piero'ya (S19). Geçişin 1516'ya bağlanması hiçbir sonuçta yok; "sonraki üç yıl kadar" (S15). Lorenzo di Piero = Il Magnifico'nun **torunu**, Giuliano'nun yeğeni (bm6) |
| §2 #80 (c11) Yeni Sakristi, 1519/20 | HAFIZA (Y) | **◐** | Britannica: sipariş 1520, çalışma 1520–34; Met: inşaat 1519; Smarthistory (S11). **NÜANS:** 1520'de Giulio **kardinal**; papalığı 1523 (HAFIZA, M4 #21) → "VII. Clemens'in siparişi" kısaltması anakronik |
| §2 #81 (c11) *Istorie fiorentine* siparişi | HAFIZA (Y/O) | **◐** (8 Kas 1520 sipariş; Mayıs 1526 sunum) · **○** (maaş, Mar 1525) | Najemy: 8 Kas 1520, Studio yetkililerinin onayı, başkan Giulio. "1525/26'da VII. Clemens'e sunum"un 1525 Roma ayağı **doğrulanamadı**; kaynaklar Mayıs 1526 (S17) |
| §2 #82 (c11) Michelangelo istihkâm sorumlusu, 6 Nis 1529 | HAFIZA (Y/O) | **◐** (unvan, 1529) · **HAFIZA** (6 Nis günü) | "governatore e procuratore generale" unvanını Dokuzlar Milis Komitesi verdi (S12, S21). Özetlerde "gözetmen/supervisor" da geçer: İngilizce karşılık farkı. M4 #30 ile uyumlu |
| §2 #83 (c11) Eylül 1529 Venedik kaçışı, Kasım dönüş | HAFIZA (O) | **◐** (Eylül kaçışı) · **○** (21 Eyl, haydut ilanı, mal el koyma) | Kasım dönüşü bu turda çıkmadı (M4 #32 ○ kalır) |
| §2 #84 (c11) 1530 saklanma, VII. Clemens'in affı, 1975 keşfi | HAFIZA (Y/O; O) | **◐** (gelenek, af koşulu, 1975 keşfi) · **○** (yer, süre) | İki ayrı yer (b42). Af: "Yeni Sakristi'ye dönme şartıyla" (S12; M4 #41 ile uyumlu). 1975: restoratör Giovannoni, Dal Poggetto; bazı çizimler Michelangelo'ya ait değil. "12 Ağu 1530" günü M4 (10/12 Ağu) ile birlikte okunmalı |
| §2 #85 (c12) Boboli / Pitti | HAFIZA (O) | **◐** (başlangıç 1549/50, Tribolo → Ammannati → Buontalenti) · **HAFIZA** (1766 açılış) | Uffizi sitesi: Pitti'nin satın alınışı **1550** (M3'te 1549); 1766 halka açılış bu turda **çıkmadı** (S31) |
| §2 #86 ve §10 #4 (c14) *Euridice* 6 Eki 1600, Camerata | HAFIZA (Y) | **◐** | Wikipedia, Britannica, The Florentine, operascribe (S7, S9). "Dafne 1598" → **1597 ya da 1597–98** (iki biçim). "Bazı parçalar Caccini" ◐. Peri'nin 1598'i HAFIZA'dan düştü |
| §2 #87 ve §10 #1 (c14) Galileo, *Sidereus Nuncius* | HAFIZA (Y) | **◐** | 7 Oca 1610 ilk gözlem; **13 Mar 1610** yayın; "Medicea Sidera"; 13 Şub 1610 mektubu (S1, S3). "13 Oca dördüncü uydu" HAFIZA kaldı |
| §2 #88 ve §4 #42 (c14) Galileo'nun "matematikçi ve filozof" unvanı, maaş | HAFIZA (Y; maaş D) | **◐** (unvan) · **○** (tarih, maaş) | Padua kürsüsünden istifa 10 Haz 1610 (PMC) / atama Tem 1610 (Floransa Üniv. makalesi) / eski EB 1611: tarih **çelişkili**. "Yıllık 1.000 Floransa scudosu": tek makale, o makale Cosimo II'yi "III" diye yanlış adlandırıyor (S2) |
| §10 #1 (c14) "Cosimo II'ye 1605–08 yazlarında ders" | Y/O/D | **◐** (1605 yazı, 1606 ithaf) · **HAFIZA** ("1605–08" çoklu yaz) | Museo Galileo: 1606 pusula kitabı genç Prens Cosimo'ya ithaf, ona pusulayı "bizzat öğretti" (S4) |
| §2 #89 ve §10 #3 (c14) Accademia del Cimento | HAFIZA (Y) | **◐** | Museo Galileo + Treccani DBI (S5). **Resmî kapanış yok:** son toplantı 5 Mar 1667; "dağıldı" yerine "sönme" |
| §2 #90, §9 #7 ve §10 #5 (c14) Cristofori ve piyano | HAFIZA (Y/O) | **◐** (1688 işe alım, 1700 envanter, Meccoli notu, Maffei 1711, 3 piyano) · **○** (Ottoboni, "iki klavye/dört oktav") | Met denemesi + Cambridge bölümü + Wikipedia (S10). "1698 günlüğü" şüpheli |
| §10 #2 ve §9 #9 (c14) Medici koruması sınırı (1633) | O | **◐** | PBS + Museo Galileo (S6). Masraf konusunda iki kaynak **farklı şey söylüyor** (b19) |
| §2 #91 (c16) 2004 / 2009 / 2016–19 | HAFIZA (Y/O) | **◐** (2004 HBS Press; 17 Kas 2009) · **○** (dizi yılları) | Dizi tarihleri yalnız inceleme tarihlerinden dolaylı: The Florentine 6 Oca 2017 ve 7 Mar 2019 (S24–S26) |
| §10 #10 (c16) *Assassin's Creed II* | O | **◐** (yayın, kurgu çerçevesi) · **○** (sapma haritası) | Geliştirici kaynağı: Kotaku'da tek Désilets röportajı özeti (b65). Resmî Ubisoft metni **yok** |
| §10 #11 (c16) *Medici: Masters of Florence* | O | **◐** (eleştiri) · **○** (yapım künyesi) | The Florentine, Varsity, Television Heaven, Vodzilla (S25) |
| §10 #12 ve §9 #14 (c16) "Medici etkisi" | Y | **◐** | Kitap künyesi ◐; **tarihçi değerlendirmesi bulunamadı** (○ yokluk) |
| §2 #37–38 (c5/c11) Laurenziana 1523 mü 1524 mü | ◐ (ayrışıyor) | **◐** (1524 ağır basıyor) | İlk tasarım 1524; merdiven Ammannati'ce 1558–59; kütüphane en geç 1571'de açık (S14) |
| §10 #6 (c11) Strozzi dörtlüğü ve Michelangelo'nun yanıtı | Y (sipariş), O (dörtlük) | **◐** (varlık, ilk dizeler, c.1545–46) · **HAFIZA** (tam metin) | Şair adı kaynaklara göre "Giovanni Strozzi" / **Giovan Battista Strozzi (1504–71)** (S13). Metin satırları görülmedi (yalnız ilk dizeler) |
| §10 #8 (c11) Laurenziana merdiveni ve "rüya" sözü | O | **◐** (tasarım/uygulama zinciri) · **○** ("rüya" sözü, 1555 mektubu) | Bir rehber "rüyada gelmiş" der, tarih/kaynak yok (ANEKDOT ○); Vasari'ye 1555 mektubu **doğrulanamadı** (S14) |
| §10 #9 (c11) Machiavelli (hapis, *Prens*, *Istorie*, 1532) | Y/O | **◐** | b46–b59 |
| §10 #23 (c5) Pico ve Poliziano 1494 | D | **◐** (Pico 17 Kas 1494, aynı gün) · **○** (zehir söylentisi) · **HAFIZA D** (2007 arsenik, Poliziano'nun ölümü) | Bu turda aranmadı (S36) |
| §5.6 ve §9 #2 (c5) "Platon Akademisi" | ◐ | **◐** (genişletildi) | SEP: "resmî okul değil"; Cosimo 1463'te Careggi'de küçük mülk; **Eylül 1462 Ficino mektubunda "Akademi" sözü** (○); IEP: şüpheci okuma (S39) |
| §5.15 ve §9 #1 (c12/c16) Accademia "ilk" | ◐ | **◐** (zincir kısmen sağlam) | Floransa 1563 → Roma: Treccani "Floransa modelinde" (◐); San Luca **1577 breve** (XIII. Gregorius, Muziano) HAFIZA → ◐; Zuccari 1593 ◐; Paris/Londra bağı zayıf (S29, bm11) |
| §5.16 ve §9 #4 (c12/c16) Uffizi "ilk müze" | ◐; karşı örnekler HAFIZA (O) | **◐** (Capitoline karşı örnek) · **HAFIZA** (Ashmolean 1683) | Capitoline 1471 (Sixtus IV bronzları), kamuya açılış **1734**; Uffizi resmî: 24 Haz 1769 (S30, S32) |
| §9 #6 (c14) Opera | HAFIZA | **◐** | *Dafne* önce (kayıp); *Euridice* = tam günümüze ulaşan en eski opera (b3–b5) |
| §3 #8 ve §5.3 (c4) Yumurta anekdotu | ANEKDOT ○ | **ANEKDOT ○** (güncellendi) | En erken yazılı kayıt Vasari **olmayabilir**: Pacioli *De viribus quantitatis* (ms. 1496–1508) ve Piero da Filicaia ms. (16. yy başı) (Palmarini–Sosnowski özeti, ○). Vasari baskısı 1550 mi 1568 mi: **çözülmedi**. "≈130 yıl sonra" → belki ≈80–90 yıl (S43) |
| §3 #14 ve §5.22 (c4) Lippi'nin odaya kilitlenmesi | ○ ANEKDOT ("kaynaksız Wikipedia türevi") | **◐ ANEKDOT** | **Vasari'nin *Vite*'sinde var** (Fordham + Wikisource çevirileri); kaynaklı. Vasari'nin aynı bölümdeki korsan hikâyesini Konody "masal" sayar (S44) |
| §3 #31 ve §5.9 (c6) Faun | ◐ ANEKDOT | **◐ ANEKDOT** | Condivi–Vasari (+ Varchi) üçlüsü anlatıyor; Bargello'daki faun maskı anlatıya **uymuyor** (iki iri azı) (S40) |
| §5.9 "5 dukat/ay, mor pelerin doğrulanmadı" | doğrulanmadı | **◐** (5 dukat, oda, sofra) · **◐/○** (mor pelerin, babaya Gümrük görevi: Vasari) | Vasari: 5 dukat/ay **dört yıl** boyunca (Lorenzo'nun 1492 ölümüne dek) ↔ HAFIZA 1489–92 (3 yıl): gerilim (S40) |
| §3 #34–35 ve §5.10 (c6) Torrigiani | ◐ ANEKDOT | **◐ ANEKDOT** | Symonds çevirisi: "…like biscuit beneath my knuckles" ◐; mekân Carmine (Cellini). Bolton'daki "yalnız burnumu kıran adam olarak anılacaksın" sözü popüler/kaynaksız: kullanma (S41) |
| §3 #40 ve §5.11 (c6) Leonardo ve lir | ○ ANEKDOT | **○ ANEKDOT** (parçalandı) | **Lir = Vasari'nin hikâyesi** (◐); "Lorenzo gönderdi" bağı modern aktarım (2018 Pacioli makalesi, ○); Anonimo Gaddiano'nun lirden söz edip etmediği **doğrulanamadı** → HAFIZA-O kalır (S42) |

### 2.2 Diğer dosyalara çapraz güncelleme

| Dosya satırı | Eski sınıf | Yeni sınıf | Not |
|---|---|---|---|
| M4 #80 (c13) Marie'nin 5 Eki 1600 vekâlet evliliği, Aralık'ta Lyon | HAFIZA | **◐** | b4 (S8) |
| M4 #105 (c0/c16) Patto 3. madde lafzı | ◐ (içerik) / ○ (lafız) | ◐ (içerik) / **◐ (2/3 öğe, İngilizce, resmî)** | Uffizi: "for the ornament of the State", "public use" (b77) |
| M4 #95 (c15/c14) Cosimo II ölümü 1621, Galileo'nun "Mediceo yıldızları" 1610 | HAFIZA | ○ (1621 yılı; 1610 yıldızları ◐) | b17 |
| M2 K48 Poliziano'nun sakristide oluşu | ◐ | ◐ (bu turda bağımsız teyit yok) | b94 |

---

## 3. Yeni kronoloji satırları

Sınıf sütunu: ◐ / ○ / HAFIZA (+ ANEKDOT, YORUM). `S` etiketleri **Ek A**'ya gider. Numaralar `b1…b106`.

### 3.1 c14: Yıldızlar, Notalar, Taşlar (müzik ve bilim)

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| b1 | c14 | c.1573–1587 | Giovanni Bardi'nin Floransa **Camerata**'sı: antik Yunan müziğini ve dramını canlandırma amacı; Britannica c.1573–87 arasını (Bardi himayesi) verir; öne çıkan üyeler teorisyen **Vincenzo Galilei** ve besteci **Giulio Caccini**; Emilio de' Cavalieri de üye sayılır | ◐ | S9 | Vincenzo Galilei = astronom Galileo'nun **babası** (Britannica). Bardi'nin *Discorso*'su: tek, hafif eşlikli ses; konuşma ritmini izleyen şarkı → monodi → *stile rappresentativo* |
| b2 | c14 | 1573–1587 | Palisca'nın *The Florentine Camerata: Documentary Studies and Translations* (Yale, 1989) kitabının tanıtımı grubu **"gayriresmî, disiplinlerarası akademi"** diye tanımlar; ilk kayıtlı toplantı 14 Oca 1573, zirve 1577–82 | ○ | S9 | Kitap kaydı + Wikipedia; Palisca'nın kendi sözü görülmedi. "Camerata" adı Bardi çevresinin kendi ürettiği terim; Caccini'nin *Euridice* partisyonundaki ithafta geçer (Wikipedia, ○). Gevşek "akademi" etiketi → "Platon Akademisi" ile paralel (bm4, bm10) |
| b3 | c14 | 1597 ya da 1597–98 | Peri'nin **Dafne**'si (libretto Rinuccini), Jacopo Corsi'nin sarayında; müziği kayıp, yalnız 455 dizelik libretto kaldı | ◐ | S7 | Tarih iki biçimde: Carnaval 1597 / 1597–98 (bir özet "1594'te bestelendi"). M3 §10 #4'teki "1598" → "1597/98" |
| b4 | c14 | 5 Eki 1600 | **Marie (Maria) de' Medici ile IV. Henri'nin vekâleten evliliği** Floransa Katedrali'nde (Santa Maria del Fiore); nikâhı Kardinal Aldobrandini kıydı, damadın yerine Marie'nin amcası Büyük Dük Ferdinando I vekil oldu | ◐ | S8 | Dinî tören Lyon'da 17 Ara 1600. Şölen Palazzo Vecchio'da Sala dei Cinquecento (The Florentine). M4 #80 HAFIZA → ◐ |
| b5 | c14 | 6 Eki 1600 | Peri–Rinuccini **Euridice**, Pitti Sarayı'nda, bu düğün için ilk kez sahnelendi; **Peri Orfeo'yu kendisi söyledi**; günümüze **müziği ve librettosuyla tam ulaşan en eski opera** | ◐ | S7 | "İlk opera" denmez (*Dafne* önce, kayıp). "Vekâlet töreninin ertesi günü" (5 → 6 Eki) bizim hesabımız |
| b6 | c14 | 6 Eki 1600 | Euridice rolünde **Vittoria Archilei**; birçok rol Caccini çevresinden (kızı Francesca dahil); ilk uygulamada Peri'nin bazı parçaları **Caccini'nin müziğiyle** değiştirildi | ◐ | S7 | Wikipedia + Britannica. Hangi parçaların değiştiği özetlerde yok |
| b7 | c14 | 1600–1602 | Caccini kendi *Euridice* partisyonunu aceleyle bastırdı; **Peri'ninkinden altı hafta önce** çıktı; Caccini'nin kendi *Euridice*'si Pitti'de **5 Ara 1602**'de sahnelendi | ◐ | S7 | Basım yılı özetlerde yok; sahne tarihi Wikipedia (başka kaynak yalnız "1602") |
| b8 | c14 | (Peri önsözü) | Peri'nin basılı önsözü, sahnede bu tür müziği ilk dinleten olarak **Emilio de' Cavalieri**'yi anar | ○ | S7 | Wikipedia "Italian opera" aktarımı; önsözün metni görülmedi |
| b9 | c14 | 13 Mar 1610 | ***Sidereus Nuncius*** Venedik'te yayımlandı: Ay'ın dağlı yüzeyi, Samanyolu'ndaki yüzlerce yıldız ve Jüpiter'in dört uydusu; kapak sayfasında uydulara **"Medicea sidera"**; Cosimo II'ye ithaf | ◐ | S1 | Wikipedia + Museo Galileo katalog + Calisphere + Cambridge. "Teleskop gözlemine dayanan ilk yayımlanmış bilimsel eser": Wikipedia sıfatı (nitelikli) |
| b10 | c14 | 7 Oca 1610 | Galileo Jüpiter'in yanında **üç küçük "yıldız"** fark etti; Ocak içindeki gözlemlerle sayı **dörde** çıktı | ◐ | S1 | History Today + Wikipedia. "13 Oca dördüncü" günü HAFIZA kaldı |
| b11 | c14 | 13 Şub 1610 | Galileo Büyük Dük'ün sekreterine, uydulara yalnız Cosimo'nun adıyla ***Cosmica Sidera*** mı, dört kardeşin (Cosimo, Francesco, Carlo, Lorenzo) adıyla ***Medicea Sidera*** mı denmesi gerektiğini sordu; ilk keşfeden olarak ad verme hakkı olduğunu savundu; sekreter ikincisinin uygun olacağını bildirdi | ◐ | S3 | **Kimin seçtiği kaynaklarda çelişir (bm1).** Bu özette Vinta'nın adı geçmiyor |
| b12 | c14 | 10 Şub 1610 | Belisario Vinta'nın Galileo'ya mektubu: yeni gezegenlere Büyük Dük'ün adını verme fikrini "cömert ve kahramanca" bulur | ○ | S2 | Tek sayfa (Museo Galileo/IMSS Vinta biyografisi) çeviri aktarımı. **10 Şub (Vinta) ve 13 Şub (Galileo) sırası birlikte doğrulanmalı** |
| b13 | c14 | 19 Mar 1610 | Galileo, uyduları gördüğü **teleskopu** ve *Sidereus Nuncius*'un resmî bir nüshasını Büyük Dük'e gönderdi; nüshada uydular sekreterin tavsiyesine uyularak *Medicea Sidera* diye adlandırılmıştı | ○ | S3 | Wikipedia 'Galilean moons' özeti (tek zincir) |
| b14 | c14 | Haz–Tem 1610 | Galileo **10 Haz 1610**'da Padua kürsüsünden istifa etti (PMC); Cosimo II'nin Pisa ya da Floransa'da kürsü teklifini kabul etti; **"Pisa Üniversitesi'nin Birinci Matematikçisi ve Büyük Dük'ün Birinci Matematikçisi ve Filozofu"** unvanı, yüksek maaş, ders verme yükümlülüğü yok | ◐ | S2 | **Tarih çelişkisi:** PMC (10 Haz istifa) / başka kaynak Tem 1610 atama / eski EB 1611. Museo Galileo galeri sayfası unvanı "Chief Mathematician and Philosopher to the Grand Duke of Tuscany (1610–1611)" diye başlıklar (aralığın anlamı belirsiz, ○) |
| b15 | c14 | Tem 1610 | Yıllık **1.000 Floransa scudosu**, ders yükü yok | ○ | S2 | Floransa Üniv. yayını (FUP PDF); aynı makale Cosimo II'yi "Cosimo III" diye **yanlış** adlandırıyor. Padua'da yıllık 1.000 florin ("Venedik'ten") ○. M3 §4 #42 (HAFIZA D) → ○ |
| b16 | c14 | 1605–1606 | Galileo genç **Prens Cosimo**'ya (1590–1621) pusula kullanımını bizzat öğretti; **Haz 1606**'da Padua'da kendi evinde, matbaacı Pietro Marinelli'ye yaklaşık **60 nüsha** *Le operazioni del compasso geometrico e militare* bastırdı (her nüsha bir pusulayla birlikte satıldı), Cosimo'ya ithaflı | ◐ | S4 | "Önceki yaz" → 1605 yazı. "1605–08 çoklu yaz" doğrulanmadı. PMC: "Floransa'da öğretmen" (○) |
| b17 | c14 | 1621 | **Cosimo II ölür**, Ferdinando II naiplikle geçer | ○ | S6 | Yıl dolaylı; gün (28 Şub: M4 HAFIZA) çıkmadı |
| b18 | c14 | 1633 | Galileo'nun yargılanması: *Dialogo* **Ferdinando II**'ye ithaflıydı; Ferdinando Kutsal Makam'ın Galileo'yu aklamasını ve çalışmasına izin vermesini istedi; mahkûmiyetten sonra kararın iptali/hafifletilmesi için **temkinli** girişimde bulundu; Elçi Niccolini Galileo'nun Floransa'da ikamet izni için çabaladı | ◐ | S6 | Museo Galileo + PBS. PBS: desteğini sürdürürse Ferdinando'nun Toskana'daki hayatı "güçleşebilirdi" |
| b19 | c14 | 1633 | **Masraf konusunda iki anlatım:** PBS: Ferdinando yargılama sırasında Galileo'nun masraflarını **kesti** (hanedanın bekâsını bir adama verdiği sözün önüne koydu); Museo Galileo (Niccolini biyografisi): elçi, Büyük Dük **geri adım atarsa** masrafları kendisi üstlenmeyi teklif etti | ○ | S6 | Arama özeti ikisini "çelişki" saydı; ikisi bağdaşabilir (teklif koşullu). Yine de "koruma" cümlesi nitelikli kurulur (bm2) |
| b20 | c14 | 1657 | **Accademia del Cimento:** Prens Leopoldo (1617–75) ve Büyük Dük Ferdinando II (1610–70) kurdu; amaç Galileo'nun öğretisi doğrultusunda doğa olgularını **deneyle sınamak**; düstur *provando e riprovando* ("deneyip yeniden deneyerek") | ◐ | S5 | Museo Galileo |
| b21 | c14 | 1657–1667 | Düzenli katılanlar: Francesco Redi, Lorenzo Magalotti (sekreter), Vincenzo Viviani, Giovanni Alfonso Borelli, Carlo Renaldini | ◐ | S5 | İtalyanca Museo Galileo sayfası |
| b22 | c14 | 1667 | ***Saggi di naturali esperienze*** (Magalotti derledi): Cimento'nun çalışmalarının **yalnız küçük bir bölümünü** anlatır; Satürn'ün gerçek biçimi (Kopernik açısından hassas konu) kitaptan **çıkarıldı** | ◐ | S5 | Treccani DBI'de imprint bir yerde "Firenze 1666", başka yerde 1667; çoğu kaynak 1667 |
| b23 | c14 | 5 Mar 1667 | Cimento'nun **son toplantısı**; faaliyet, Leopoldo'nun kardinal oluşuyla (1667) sona erdi; resmî kapatma kararı yok; Leopoldo akademinin "sönmüş sayılmamasını" istedi | ◐ | S5 | Treccani DBI + "La rivoluzione scientifica" girdisi. Toplantılar 1662'den sonra seyrekleşti |
| b24 | c14 | 1688 (≈1690) | Prens **Ferdinando** (Gran Principe), Padovalı klavsen ustası **Bartolomeo Cristofori**'yi (1655–1731/32; ≈33 yaşında) saray enstrümanları bakıcısı olarak çağırdı; selefi yeni ölmüştü | ◐ | S10 | Britannica "yaklaşık 1690"; diğerleri 1688. Prens'in Venedik Karnavalı dönüşü Padua'dan geçip tanışmış olması muhtemel (○). Prens'in ≈40 klavsen/spineti olduğu (○) |
| b25 | c14 | 1688– | Cristofori'nin görevi: saray enstrümanlarının **bakım ve onarımı**, yeni enstrüman yapımı; Pratolino yazlık sarayında da çalıştı; ilk icatlar muhtemelen Prens'in Pratolino prodüksiyonlarında continuo çalması içindi | ○ | S10 | "Olasılıkla" dili |
| b26 | c14 | 1700 | **Medici envanterinde Cristofori'nin yeni icadı** "arpicembalo": çekiçler ve sönümleyiciler (◐); iki klavye, dört oktav (○); "Bartolomeo Cristofori tarafından yeni icat edilmiş" | ◐ | S10 | Envanterin İtalyanca metni görülmedi. Ripin (Met Journal 1978): kayıt eskiden daha geç sanılırdı; Mario Fabbri araştırması 1700 öncesine yerleştirdi. Envanter "piyanonun en eski kesin kanıtı" (Met/Cambridge özeti) |
| b27 | c14 | 1700 | Saray müzisyeni **Federigo Meccoli**'nin marjinal notu: *Arpicimbalo del piano e forte*'nin 1700'de Cristofori tarafından, Gran Principe hizmetindeyken icat edildiği | ◐ | S10 | Met denemesi + başka özet. 1698 tarihli günlük kaydı şüpheli sayılıyor (○) |
| b28 | c14 | 1711 | **Scipione Maffei**, *Giornale de' letterati d'Italia*'da aleti ***gravicembalo col piano, e forte*** diye tanıttı; ad bugünkü adın ilk biçimi sayılır | ◐ | S10 | Met + Cambridge. Bir özet: makale olmasa icat "saraylarda gizli kalabilirdi" (○, yorum). Aynı makaleye dayanan eski "1709" tarihlemesi terk edildi (Ripin) |
| b29 | c14 | 1711 | Maffei'ye göre Cristofori o güne dek **üç piyano** yapmıştı: biri **Kardinal Ottoboni**'ye (Roma), ikisi Floransa'da satıldı | ○ | S10 | Tek özet; Met denemesi özetinde **çıkmadı** |
| b30 | c14 | 1713–1716 | Ferdinando 1713'te öldü; 1716 tarihli enstrüman envanteri **"Bartolommeo Cristofori Custode"** imzalı (Cristofori "koruyucu/bakıcı" unvanıyla) | ○ | S10 | Tek özet |
| b31 | c14 | 1720; 1722; 1726 | **Hayatta kalan üç Cristofori piyanosu:** 1720 (Met, New York, 89.4.1219; en eskisi), 1722 (Roma, Museo degli Strumenti Musicali), 1726 (Leipzig Üniversitesi) | ◐ | S10 | Cristofori'nin ölümü: 27 Oca 1731 (Wikipedia) ya da 1732 (Britannica, NMC). Beş piyanonun İspanya Kraliçesi Maria Barbara'ya gittiği (Met; kimin yaptığı özette belli değil, ○) |

### 3.2 c11: Michelangelo ve Medici

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| b32 | c11 | 1519/1520–1534 | **Yeni Sakristi:** San Lorenzo'da Medici mezar şapeli; Britannica sipariş yılını **1520** (VII. Clemens, o tarihte Kardinal Giulio) ve çalışma süresini 1520–34 verir; Met inşaatın **1519**'da başladığını söyler; tasarım aslında **Leo X ve Clement VII**'nin mezarları içindi; heykeller Urbino Dükü Lorenzo ve Nemours Dükü Giuliano'nun mezarları için | ◐ | S11 | M4 #17 ile aynı çelişki. Giulio'nun papalığı 1523 (HAFIZA, M4 #21) |
| b33 | c11 | 1526–1533 | **Giuliano mezarı** 1526–33 (Smarthistory); ***Gece*** heykeli 1526–31 arasında oyuldu | ○ | S11, S13 | Tek tek özetler; kapsamları farklı |
| b34 | c11 | 1534 | Michelangelo Floransa'yı **kalıcı olarak terk etti**; sakristi ve kütüphane yarım kaldı; freskler hiç başlamadı | ◐ | S11 | M4 #45 notuyla uyumlu (Eylül 1534 HAFIZA) |
| b35 | c11 | 1524 | **Laurenziana'nın ilk tasarımı:** merdiven yan duvarlara yaslanan iki kol; sonra merkeze alındı | ◐ | S14 | M3 §2 #37 "1523/24" → 1524 ağır basıyor; M4 #22 ile uyumlu |
| b36 | c11 | 1550 | **Tribolo** merdiveni yapmaya çalıştı, yapılamadı | ○ | S14 | Tek özet |
| b37 | c11 | 1558/1559 | **Ammannati** merdiveni Michelangelo'nun gönderdiği **kil model**le (1558) / tasarımıyla (1559) uyguladı; Vasari de Michelangelo'nun planları ve sözlü talimatlarıyla çalıştı; Michelangelo uzaktan denetledi | ◐ | S14 | Tarih çelişkisi 1558/1559 |
| b38 | c11 | ≤1571 | Kütüphane Michelangelo'nun ölümünden sonra, **en geç 1571'de** açıktı | ◐ | S14 | M3 §2 #38 ile uyumlu |
| b39 | c11 | Nis 1526 | Floransa surların güçlendirilmesi için yeni bir **magistratura** kurdu; **Machiavelli** bunun sekreteri oldu ve on dört yıl sonra Palazzo Vecchio'ya döndü | ◐ | S21 | Başka kaynak: Clement VII, Machiavelli'ye surların yapım müdürlüğünü önerdi. 1526 planları "daha önce yarım kalmış Medici planlarının devamı" (○). **"Procuratore" unvanı Michelangelo'ya (1529) aittir, Machiavelli'ye değil** |
| b40 | c11 | 1529 | **Michelangelo**, Cumhuriyet'in "Dokuzlar Milis Komitesi" tarafından surların ***governatore e procuratore generale***'si atandı; VII. Clemens imparator ordusunun yardımıyla ailesini geri getirmeye hazırlanıyordu | ◐ | S12, S21 | M4 #30 ile uyumlu. Rehber (Reid's): "ömür boyu Medici patronajından Cumhuriyet patronajına geçmişti" |
| b41 | c11 | 21 Eyl 1529 | Michelangelo Floransa'dan **Venedik'e kaçtı** (nihai hedef Fransa, bir kaynak); Floransa hükümeti onu **haydut ilan edip mallarına el koydu**, dönerse affedileceğini bildirdi | ◐ (kaçış) / ○ (21 Eyl, haydut ilanı) | S12 | Kasım dönüşü bu turda çıkmadı (M4 #32) |
| b42 | c11 | 1530 (Ağu sonrası) | Cumhuriyet düştükten sonra Michelangelo'nun saklandığı yer **iki gelenekte**: (a) **Yeni Sakristi'nin altındaki dar oda** (bir kaynak "yedi metreye iki"; süre iki–üç ay; San Lorenzo Başrahibi **Giovan Battista Figiovanni** onu sakladı); (b) **San Niccolò oltr'Arno** çan kulesinin tabanındaki küçük oda ("birkaç gün") | ◐ (gelenek) / ○ (yer, süre) | S12 | **Çelişki bulgu.** Condivi/Vasari metni görülmedi. **San Niccolò kulesi ≠ San Miniato kulesi** (savunma, M4 §3 #14). Taraflar ayrı söylenmeli (bm8) |
| b43 | c11 | 1530 sonrası | VII. Clemens Michelangelo'yu **Yeni Sakristi işine dönme şartıyla** affetti | ◐ | S12 | Artnet + başka; M4 #41 ○ → ◐ |
| b44 | c11 | 1975 | Yeni Sakristi altında **"gizli oda"** bulundu: duvarlarda kömür ve sanguin çizimler; restoratör **Sabino Giovannoni** iki kat sıvayı kaldırırken fark etti (bir hesap Kas 1975, müze için yeni çıkış aranırken); **Dal Poggetto** çoğunu Michelangelo'ya atfetti; bazıları ona ait değil; ana teori tarih **1530** | ◐ | S12 | Çizimlerin atfı ve tarihi tartışmalı |
| b45 | c11 | c.1545–46 | Giovan Battista Strozzi'nin (1504–71) *Gece* heykeli üzerine dörtlüğü ("La Notte, che tu vedi…") ve Michelangelo'nun yanıtı ("Caro m'è 'l sonno…"); yanıt **Cosimo I dönemi siyasi iklimine, Medici yönetimine ima** olarak okunuyor (*Rime*'nin "siyasi bölümü") | ◐ | S13 | Metin satırları görülmedi (yalnız ilk dizeler). Standart baskı Girardi, Laterza 1960. Şair adı "Giovanni Strozzi" ya da "Giovan Battista Strozzi" |

### 3.3 c11: Machiavelli ve Medici

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| b46 | c11 | Kas 1512 | Machiavelli, Medici dönüşüyle **görevden alındı** | ◐ | S16 | M4 #4 (Soderini düşüşü 31 Ağu 1512) |
| b47 | c11 | 12 Şub 1513 | Boscoli komplosu ortaya çıkınca Machiavelli'nin adı **yaklaşık 20 kişilik listede** çıktı; tutuklandı (Bargello), **strappado** ile işkence gördü | ◐ (tutuklama, işkence) / ○ (12 Şub, gönüllü gidiş iddiası) | S16 | Bir hesap: Otto di Guardia'ya kendisi gitti. "Altı kez" ayrıntısı **çıkmadı** |
| b48 | c11 | 23 Şub 1513 | **Pietro Boscoli** ve **Agostino Capponi** başları kesilerek idam edildi; Machiavelli, muhtemelen delil zayıf olduğu için kurtuldu | ◐ | S16 | |
| b49 | c11 | Mar 1513 | Machiavelli, Giovanni de' Medici'nin **X. Leo** seçilmesinin ardından çıkan **af** kapsamında serbest kaldı (bir hesap: önce müebbet; Giuliano de' Medici'nin müdahalesiyle para cezası) | ◐ | S16 | Süre: tutuklamadan ≈3 ay ↔ Mart (çelişki) |
| b50 | c11 | 1513 | **Sant'Andrea in Percussina (Albergaccio)** çiftliğine çekildi; Vettori ile yazışma başladı | ◐ | S16 | |
| b51 | c11 | 10 Ara 1513 | **Vettori'ye mektup:** "küçük eser" *De Principatibus*; Giuliano de' Medici'ye ithaf edeceğini yazar; akşamları çamurlu giysilerini eşikte çıkarıp "saray ve divan giysileri" giyerek **eskilerin saraylarına** girdiğini anlatır | ◐ | S15 | Çeviri alıntıları §4 bd12–bd13. Özgün İtalyanca görülmedi |
| b52 | c11 | 1513–1516 (belirsiz) | İthaf **Giuliano'dan yeğeni Lorenzo di Piero'ya** (1492–1519, Lorenzo il Magnifico'nun **torunu**) çevrildi; geçişin yılı kaynaklarda yok ("sonraki üç yıl kadar"); iki ismin de eseri okuyup okumadığı **bilinmiyor** | ◐ | S15, S19 | 1516 (Giuliano'nun ölümü) HAFIZA. Basılı başlık: "To the Magnificent Lorenzo di Piero de' Medici" (Marriott) |
| b53 | c11 | (*Prens* ithafı) | İthaf mektubunda **hediye geleneği** (at, silah, altın işlemeli kumaş, değerli taş) ve **ressam benzetmesi**: ovadan dağları, dağdan ovayı seyreden peyzaj ressamı gibi, "düşük ve alçak mevkideki" bir yazarın prenslerin işlerini yazma hakkı; son cümlede talihin "haksız" kötülüğü | ◐ | S19 | Marriott çevirisi (çok sitede aynı çeviri: bağımsızlık sınırlı). §4 bd14–bd15 |
| b54 | c11 | 8 Kas 1520 | ***Istorie fiorentine*** siparişi kesinleşti: Floransa Üniversitesi (Studio) yetkilileri onayladı; başkanları **Kardinal Giulio**'ydu (Najemy); diğer kaynaklar "1520 sonu" | ◐ (Kas 1520) / ○ (gün) | S17 | Maaş **57 florinle** başlayıp **100'e** çıktı (birkaç kaynak) / "100 florin" (bir Almanca kaynak) |
| b55 | c11 | 1525–Mayıs 1526 | *Istorie*'nin büyük kısmı Mar 1525'te bitti (1492'ye dek; Almanca kaynak, ○); **Mayıs 1526**'da, artık papa olan Giulio'ya (VII. Clemens) resmen sunuldu; Papa eseri beğendi, ölçülü ödüllendirdi ve **ulusal ordu** konusunda yardım istedi | ◐ (Mayıs 1526) / ○ (Mar 1525, ödül) | S17 | "1525'te Roma'da sunum" **doğrulanamadı**. 1527 Roma yağması ve Floransa'da Medici'nin düşmesi umutları bitirdi |
| b56 | c11 | 4 Oca 1532 | ***Il Principe* ilk basım:** Roma, Antonio Blado d'Asola (Folger kaydı); Blado'ya Machiavelli'nin eserleri için on yıllık ayrıcalık (papalık himayesi); Floransa'da **Giunti** baskısı 8 Mayıs 1532 | ◐ | S18 | Machiavelli beş yıl önce ölmüştü. Folger'da Blado'nun *Istorie fiorentine* baskısı 25 Mar 1532 (ayrı). 1559 Yasaklı Kitaplar Dizini: bu turda **çıkmadı** |
| b57 | c11 | 1513→1532 | *Prens* elyazması olarak dolaştı; basılı yayın ölümünden sonra | ◐ | S18 | |
| b58 | c11 | (anlatı) | Vettori *Prens*'i Lorenzo'ya sunarken prens o gün **hediye edilen iki av köpeğiyle** ilgileniyormuş; kitabın sunumu köpeklerin gölgesinde kalmış | ○ ANEKDOT | S20 | Kaynağı belirtilmemiş bir İtalyan popüler makale (La Civiltà Cattolica); "Ridolfi" ya da birincil kaynak **doğrulanmadı**; "tazı" ayrıntısı yok |
| b59 | c11 | 20/21 Haz 1527 | Machiavelli'nin ölümü | ○ | S21 | Bir zaman çizelgesi 20 Haz; HAFIZA 21 Haz (Y). Medici'nin Mayıs 1527'de kovulması (M4 #26) ve Machiavelli'nin Cumhuriyet'te dışlanması: HAFIZA-O |

### 3.4 c16: Popüler kültür ve "Medici etkisi"

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| b60 | c16 | 2004 | **Frans Johansson**, *The Medici Effect* (Harvard Business School Press): yenilik, farklı alan ve kültürlerin **"kesişim"inde** doğar; başlık Rönesans Floransası'nın yaratıcılık patlamasına gönderme | ◐ | S26 | Amazon "Top 10 business book", 18 dile çeviri (○). Bir bibliyografya yayıncıyı "Harvard University Press" yazıyor (hata sayıldı) |
| b61 | c16 | 2004 | *Ubiquity* incelemesi (John Stuckey) kitabın tarihsel iddiasını şöyle özetler: Medici bankacıları ve benzerleri, çeşitli disiplinlerden özgün düşünürleri Floransa'ya ve birbirleriyle temasa getirdi, Rönesans'ı **tetiklemiş olabilir**; başka bir özet: Medici Rönesans'ı kasten planlamadı ama katkıda bulundu | ○ | S26 | Tarihçi değerlendirmesi **değil** |
| b62 | c16 | 1993 | **Padgett ve Ansell**, "Robust Action and the Rise of the Medici, 1400–1434", *AJS* 98(6): 1259–1319: evlilik, ekonomi ve patronaj ağlarında Medici ayrı yapıları birbirine bağlayan tek aktör; Cosimo'nun "çokseslilik (multivocality)" stratejisi | ◐ | S27 | "Medici etkisi"nin **akademik akrabası:** ağ analizi; sanat değil siyaset. AcaWiki özeti; makale metni görülmedi |
| b63 | c16 | 17 Kas 2009 | ***Assassin's Creed II*** PS3 ve Xbox 360 için çıktı; Windows 3 Mar 2010; Mac 1 Eki 2010 | ◐ | S24 | "Ubisoft Montréal" künyesi M3 HAFIZA'sında kaldı |
| b64 | c16 | 2009 (kurgu) | Oyun **1476 Floransa**'da başlar; kurgusal **Ezio Auditore**'nin babası darbe ortamında hainlikle suçlanır; **26 Nis 1478 Pazzi Komplosu** oyunda "Templar komplosu"dur; **Rodrigo Borgia** Templar Büyük Üstadı; müttefikler Machiavelli, Caterina Sforza, Leonardo da Vinci; mekânlar Floransa, San Gimignano, Forlì, Venedik | ◐ | S24 | Fan wiki + Wikipedia; Savonarola/*Bonfire of the Vanities* DLC bu turda çıkmadı (HAFIZA) |
| b65 | c16 | 2009 (röportaj tarihi özette yok) | Yaratıcı yönetmen **Patrice Désilets** (Kotaku röportajı): tarih serinin markası ama **"bazen baş belası"**; fikir verir, kısıt da getirir; sapmalara "bu bir his" der; oyundaki Machiavelli gerçek entelektüelden çok **dövüşçüye** yakındır | ○ | S23 | Tek röportajın özeti; tam metin görülmedi. Alıntılar §4 bd31 |
| b66 | c16 | 2009 (önizleme tarihi özette yok) | GamesRadar önizlemesi: oyun **gerçek bir komplo** (Medici–Pazzi, Papa'ya dek uzanan) çevresinde açılır; Ezio'nun ailesi uydurma, çevredeki olaylar ve kişiler gerçek; şehirler yıllar süren geliştirme, binlerce fotoğraf dokusu ve **tarihçi danışmanlığıyla** kuruldu | ○ | S23 | Danışman tarihçi adı yok |
| b67 | c16 | oyun ↔ tarih | **Sadakat:** Pazzi çekirdeği gerçek (Giuliano öldürülür, Lorenzo kurtulur, komplocular avlanır). **Sapmalar:** (i) Salviati'nin ölümü: oyunda Ezio öldürür (1479), gerçekte yakalanıp linç edilerek asıldı; (ii) Machiavelli 1488'de yüksek rütbeli Tarikat üyesi (gerçekte 19 yaşında); (iii) fan kontrolüne göre Francesco de' Pazzi, Salviati ve Baroncelli Palazzo Vecchio pencerelerinden asıldı, oyunda yalnız Francesco (**Baroncelli kısmı M2 K62 ile çelişir:** Bandini/Baroncelli İstanbul'a kaçtı, 29 Ara 1479'da Floransa'da asıldı, ◐; fan kontrolü orada hatalı görünüyor); (iv) Rodrigo Borgia gerçekte komplonun beyni değil; (v) Templar/Assassin kurgusu; (vi) 1499'da kubbeli Aziz Petrus (fan; anakronizm); (vii) saldırı yeri | ○ (çekirdek ◐) | S22, S23 | Hepsi basın/listicle/fan kontrolü; geliştirici belgesi **yok**. (vii) "saldırı Duomo'nun dışında değil içinde" bir fan kontrolü; oyundaki sahne yeri özetlerde net değil |
| b68 | c16 | 2016–2019 | ***Medici: Masters of Florence***: The Florentine'in (6 Oca 2017) ilk sezonun **somut hataları:** Donatello'nun çıplak bronz *David*'i Cosimo'nun 1433 yargılamasında henüz yoktu; Duomo'nun inşaatı Giovanni di Bicci'nin ölümünden neredeyse on yıl önce başlamıştı (alıntıdaki "Duomo" büyük olasılıkla kubbeyi kastediyor: 1420 ↔ 1429, bizim okumamız); **Giovanni di Bicci'nin ölümü cinayet gizemine çevrilmiş** (gerçekte nedeni bilinmiyor, doğal sanılıyor); eleştirmenler "pembe dizi" der; yapım değeri övülür | ◐ | S25 | The Florentine + Varsity + Television Heaven + Vodzilla. *David* tarihi M3 §2 #14–15 ile birlikte: 1430'ların sonu–1440'lar çoğunluğu 1433'ü dışarıda bırakır |
| b69 | c16 | 2019 | 2. sezon ***The Magnificent***: Sean Bean (Jacopo de' Pazzi), Daniel Sharman (Lorenzo); The Florentine "fact and fiction" yazısı 7 Mar 2019 | ◐ | S25 | Pazzi Komplosu doğruluk analizi özetlerde yok |
| b70 | c16 | (yapım) | Yaratıcı **Frank Spotnitz** diziyi "ya olsaydı" sorusuyla çerçeveler (The Florentine'e göre) | ○ | S25 | Spotnitz'in kendi sözü görülmedi |

### 3.5 c12 / c16: Kurumlar (Accademia, Uffizi, Boboli)

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| b71 | c12 | 1563 | Floransa **Accademia delle Arti del Disegno** (Vasari yönetiminde, Medici desteğiyle): kaynaklar "ilk sanat akademisi" der; Roma'nınkinin öncülü sayılır | ◐ | S29; M3 §2 #57 | "İlk" nitelikli (bm11). Kuruluş metni 12 Oca, kuruluş 13 Oca 1563 (M3) |
| b72 | c12 / c16 | 1577 | **XIII. Gregorius'un 1577 breve'i** Roma'daki ressam loncasını (*Università*) "Resim, Heykel ve Çizim Sanatları Akademisi"ne dönüştürdü (**Girolamo Muziano**'nun girişimi) | ◐ | S29 | Kurumun kendi sitesi + Wikipedia; Treccani başka bir girdide doğumu **1572**, başka kaynak 1583/1593 yazıyor |
| b73 | c12 / c16 | 1593 | **Federico Zuccari**, Accademia di San Luca'nın **principe**'si (Kardinal Federico Borromeo himayesi); yeniden kuruluş **Floransa'daki Accademia del Disegno modelinde** (Treccani) | ◐ | S29 | Bir Treccani girdisi "principe 1598". İlk statüler 1593 ya da **1607**. Britannica: 1593'ü eğitim programının yeniden etkinleşmesi sayar |
| b74 | c16 | 1648 | Paris'te **Académie royale de peinture et de sculpture** (Charles Le Brun'un öncülüğünde, XIV. Louis himayesinde); bir kaynak San Luca modelinden esinlendiğini söyler | ◐ (kuruluş) / ○ (model bağı) | S29 | Bir Baidu girdisi 1676'da San Luca'nın Fransız Akademisi'yle birleştiğini yazıyor, özet güvenilmez buldu; **HAFIZA-O:** 1676'da bir "birleşme/aggregation" gerçekten oldu: doğrulanmalı |
| b75 | c16 | 1768 | **Royal Academy of Arts** (Londra): III. George onayladı, ilk başkan **Joshua Reynolds** | ◐ | S29 | Önceki akademilere bağı özetlerde **yok** (HAFIZA-O: Fransız modeli) |
| b76 | c16 | ≈1581 | Uffizi'nin üst katında **Francesco I'in galerisi**; 17. yy'dan itibaren koleksiyon büyüdükçe galeri **seçilmiş dış ziyaretçilere** gittikçe açıldı | ◐ | S30 | M3 §2 #64 ile uyumlu |
| b77 | c16 | 31 Eki 1737 | **Anna Maria Luisa Paktı:** koleksiyon Floransa'ya "**Devletin süsü için**" ve kamu kullanımı için bağlandı (Uffizi İngilizcesi) | ◐ | S30; M4 #104–105 | "Yabancıların merakı" bu turda görülmedi. 31 Ekim tarihi M4'ten |
| b78 | c16 | 24 Haz 1769 | **Pietro Leopoldo** galeriyi Floransa'nın koruyucu azizi Aziz Yuhanna günü **halka açtı** | ◐ | S30 | Uffizi resmî. Uffizi kendini "dünyanın ilk modern müzelerinden biri" diye tanımlar (kurum öz tanımı, nitelikli). Britannica "Büyük Dük Leopold I" der (doğru: bkz. §1.1) |
| b79 | c16 | 1471; 1734 | **Capitoline:** 1471'de Sixtus IV bronz heykelleri (dişi kurt, Dikenli Çocuk, Camillus, Konstantin'in başı) Palazzo dei Conservatori'ye devretti (yazıt "restitution" der); **1734'te XII. Clemens müzeyi halka açtı**; birçok kaynak "dünyanın en eski halk müzesi" der | ◐ | S32 | Uffizi'nin "ilk" iddiasına karşı örnek (1769 > 1734). Ashmolean 1683 hâlâ HAFIZA |
| b80 | c12 | 1549–1550 | **Boboli:** Eleonora di Toledo'nun görevlendirmesiyle **Tribolo** başladı (Uffizi 1549; Britannica 1550); **Pitti Sarayı Cosimo I ve Eleonora tarafından 1550'de satın alındı** (Uffizi) | ◐ | S31 | M3 §10 #13 (1549 satın alma) ile **çelişki**: Uffizi 1550 |
| b81 | c12 | 1557–1593 | **Grotta Grande:** ilk işler 1557'de Davide Fortini (Tribolo'nun damadı) yönetiminde, aynı yıl görev **Vasari**'ye geçti; **Buontalenti** grotoyu 1583–93 arasında yaptı (ayrı Uffizi girdisi) | ◐ | S31 | Aralık: 1557–1587 / 1583–1593 |
| b82 | c12 | 18. yy | Pietro Leopoldo döneminde Boboli'de kapsamlı müdahaleler; **1766 halka açılış bu turda doğrulanmadı** | ○ | S31 | M3 §10 #13 |

### 3.6 c4: Medici dışı patronlar (Strozzi, Pazzi)

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| b83 | c4 | 1423 | **Gentile da Fabriano, *Magi'nin Tapınması***: bankacı **Palla Strozzi**'nin siparişi, Santa Trinita sakristisindeki aile mezar şapeli için; Palla, Magi'nin maiyetinde **şahin tutarken** resmedilmiş (*strozzieri* = şahinci, soyadı oyunu) | ◐ | S33 | Sipariş 1420 ya da 1423 öncesi (iki kaynak); Palla'nın toplam 300 florin ödediği (○). Tablo Uffizi'de |
| b84 | c4 | 1427 | Palla Strozzi **Floransa'nın en zengini** (Catasto) | ◐ | M1 #39; S33 | Çapraz; S33'te bir kaynak da "en zengin vatandaş" der |
| b85 | c4 | 1429 | **Andrea de' Pazzi**, Santa Croce'deki **Pazzi Şapeli**'ni (kapitül salonu) **Brunelleschi**'ye ısmarladı | ◐ | S34 | İnşaat başlangıcı 1440–43; tamamlanma 1461/1466/1469/1470'ler; Brunelleschi 1446'da öldü, ne kadarının yapıldığı belirsiz; mimar atfı **tartışmalı**; Michelozzo ve Giuliano da Maiano'nun bitirdiği (bir kaynak) |
| b86 | c4 / c7 | — | **Aynı mimar iki rakip ailenin şapelini tasarladı:** Medici'nin Eski Sakristi'si (M3 §2 #5) ve Pazzi Şapeli; Pazzi 1478'de ezildi | ◐ (iki olgu ayrı ayrı) · YORUM (yan yana koyma) | S34; M3 | Plutarkhos tipi karşılaştırma. "Pazzi Medici'ye gücünü göstermek için" yorumu bir seyahat blogunda (○): kullanma |
| b87 | c4 | 6 Ağu 1489 | **Palazzo Strozzi'nin yapımı başladı** (temel tarihini astrolog Benedetto Biliotti seçti); Filippo Strozzi (Yaşlı) Medici'nin sürgününden **1466**'da dönmüştü; arsayı toplamak 1473–1489 sürdü, çok bina yıktırdı | ◐ | S35 | |
| b88 | c4 | 1489– | Saray, **Medici sarayını aşmak** üzere tasarlandı (Britannica: ölçeği Medici Sarayı'nı bilerek geçti); Strozzi'nin kendi sitesi "özellikle Palazzo Medici" gibi önceki modelleri yeniden yorumladığını söyler | ◐ | S35 | "Medici'nin rakibi büyük patron" (bm15) |
| b89 | c4 | 1489– | **Mimar belirsiz:** Giuliano da Sangallo ve Benedetto da Maiano'nun birer modeli var, yalnız biri günümüze kalmış; Il Cronaca yapım şefi | ◐ | S35 | Il Cronaca zamanlaması çelişkili (1490–1504) |
| b90 | c4 | 1491; 1538 | Filippo 1491'de öldü, saray yarımdı (güney cephe ve korniş yarım); tamamlanma 1538 (Wikipedia); **Cosimo I** sonra sarayı müsadere edip ≈30 yıl sonra iade etti | ◐ (ölüm, yarım) / ○ (müsadere) | S35 | Özet "aynı yıl" der (anlaşılmaz); HAFIZA: Montemurlo 1537 sonrası (O) |

### 3.7 c5 / c7: Hümanistler

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| b91 | c5 | 1486–1488 | **Pico della Mirandola:** 900 tez (1486), Roma'da savunma önerisi; komisyon 7 tezi sapkın, 6'sını şüpheli buldu; Papa tamamını mahkûm etti (Pico itaat belgesi imzalamıştı); Fransa'ya kaçtı, **1488'de** papalık elçilerinin talebiyle tutuklandı; İtalyan prenslerin müdahalesiyle ve VIII. Charles'ın kararıyla serbest kaldı | ◐ | S36 | Sapkın sayısı 7+6=13 / "en az 13" |
| b92 | c5 | 1488 | Pico, papanın izniyle **Floransa'ya** yerleşti, **Lorenzo de' Medici'nin kişisel himayesinde** ("şartlı salıverme gibi"); bir kaynak: Toskana'ya dönüş yazı 1488 | ◐ | S36 | Fiesole bu turda çıkmadı. M2 K80: Pico, Savonarola'nın Floransa'ya çağrılışında rol oynadı (HAFIZA-O) |
| b93 | c5 / c10 | 17 Kas 1494 | **Pico öldü**; iki özete göre aynı gün **VIII. Charles Floransa'ya girdi**; zehir söylentileri | ◐ (ölüm tarihi, aynı gün) / ○ (zehir söylentisi, tek kaynak) | S36 | M2 K92 (17 Kas 1494 giriş: HAFIZA-O) ile eşleşir. 2007 arsenik çalışması aranmadı |
| b94 | c7 | 1478 | **Poliziano**, *Pactianae coniurationis commentarium*: Pazzi saldırısının **ilk anlatımı, görgü tanığı**; Sallustius'un *Catilina*'sından yararlanan **siyasi propaganda** ("Stanze'nin karanlık karşı noktası"); Celati'nin 2015 yayını | ◐ | S37 | Poliziano'nun sakristide oluşu M2 K48; bu turda bağımsız teyit yok. Lorenzo'nun oğullarına hocalığı çıkmadı |
| b95 | c4 / c5 | 1427–1444 | **Leonardo Bruni** Floransa şansölyesi (ayrıca 1410–11); Albizzi ve Medici karşısında siyasi gücü sınırlı; Cosimo 1434'te iktidarı alınca cezalandırılmadı, ölümüne (1444) dek şansölye kaldı | ◐ | S38 | Catholic Encyclopedia "1427'de Medici'nin kayırmasıyla" der: **anakronik** (Medici iktidarı 1434; HAFIZA Y): kullanma |
| b96 | c5 | 1437 | **Arthur Field**, Bruni'yi Cosimo'ya karşı 1437 komplosunun olası parçası olarak saptar | ○ | S38 | Field'in teşhisi; kabul görmüş olgu değil |
| b97 | c5 | 1439 | Bruni'nin *Historiae Florentini Populi*'si çıktı; Bruni "resmî tarihçi" sayıldı | ◐ | S38 | |
| b98 | c5 | Eyl 1462; 1463 | Ficino'nun **Eylül 1462** tarihli mektubu "Careggi'deki mülkte bizim için düzenlediğin **Akademi**"den söz eder (SEP); Cosimo **1463**'te Ficino'ya Careggi'de küçük mülk verdi | ◐ (1463 mülk) / ○ (mektup alıntısı) | S39 | Mektubun alıcısı özette yok; Latince görülmedi. Hankins'in "metafor" okumasıyla gerilim (bm10) |
| b99 | c5 | — | **SEP:** kaynaklar "Platon Akademisi"ni düzenli toplantılı resmî okul olarak anlamamıza izin vermez; Ficino seçkin Floransalı gençleri öğretmeyi yeğledi (Hankins, Celenza'ya atıf). **IEP:** Ficino'nun akademi göndermeleri Platon el yazmasının Floransa'da bulunuşunu ve kendi çevirilerini kastediyor olabilir; "akademi başkanı olsun olmasın Platonculuğun savunucusuydu". İkisi de Field 1988, Kristeller 1943, Hankins 1989'a atıf yapar | ◐ | S39 | İki bağımsız ansiklopedi uyumlu |

### 3.8 c4 / c6: Anekdot zincirleri (birincil kaynak çevirileri)

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| b100 | c6 | 16 Tem 1553 | Condivi'nin ***Vita di Michelagnolo*** kitabı çıktı | ○ | S40 | Tarih tek özette (Gutenberg/Holroyd çevresi). Holroyd önsözü: Vasari'nin hayatı birkaç kez çevrildi, Condivi'ninki "hiç tam olarak" çevrilmedi (○) |
| b101 | c6 | (≈1489–1492) | **Hane içi koşullar:** Condivi (Gutenberg çevirisi): Lorenzo Michelangelo'ya sarayda **oda** verdi, onu **çocukları gibi sofrasına** oturttu, ayda **5 dukat harçlık** ve statüsüne uygun giysi verdi. Vasari: aynı **5 dukat/ay**, **dört yıl** boyunca (Lorenzo'nun 1492 ölümüne dek), **mor pelerin**, babası Lodovico'ya **Gümrük'te görev** | ◐ (5 dukat, oda, sofra) · ◐/○ (pelerin, görev: Vasari) | S40 | M3 §5.9 "doğrulanmadı" → ◐. "Dört yıl" ile HAFIZA 1489–92 (≈3 yıl) arasında gerilim |
| b102 | c6 | (≈1489–1492) | **Faun başı:** Condivi ve Vasari aynı hikâyeyi anlatır; Symonds: antik bir faundan **kopya** Lorenzo'nun dikkatini çekti; Lorenzo yaşlıların dişlerinin eksik olduğunu söyledi; Michelangelo bir dişi kırıp diş etini oydu; Lorenzo onu hanesine almaya karar verdi (Condivi) | ◐ ANEKDOT | S40 | **Bargello'daki faun maskı anlatıya uymuyor** (yalnız iki iri azı). Anlatan: Condivi 1553 (Michelangelo'nun gözetiminde), Vasari 1550/68 |
| b103 | c6 | — | **Torrigiani:** Cellini'nin aktardığı, Torrigiani'nin kendi böbürlenmesi: Carmine'de Masaccio şapelinde çizim öğrenirken Michelangelo'nun burnuna yumruk atar; **"kemik ve kıkırdak parmak eklemlerimin altında bisküvi gibi çöktü"**; izi ölene dek taşıyacak | ◐ ANEKDOT | S41 | Symonds çevirisi. Vasari: dostluk sonrası alay, kırık burun. Torrigiani'nin sonu çelişir ("İspanyol Engizisyonu'nda öldü" sonradan eklenmiş görünüyor) |
| b104 | c6 | ≈1482 | **Leonardo ve lir:** Vasari (1550/68): Leonardo Milano'ya kendi yaptığı, çoğunlukla gümüşten, **at kafatası biçimli** lirle gitti; Anonimo Gaddiano ve Vasari Leonardo'nun Milano sarayına **müzisyen olarak** sunulduğunu söyler; "Lorenzo onu lirle **gönderdi**" bağı 2018 tarihli bir Pacioli makalesine bağlanır; bir başka kaynak Leonardo'nun Atalante Migliorotti ile "Lorenzo'nun sanatsal elçisi" olarak gitmiş olabileceğini söyler | ◐ (lir, müzisyen olarak sunulma) / ○ ANEKDOT (Lorenzo'nun göndermesi) | S42 | Anonimo Gaddiano ≈1530'lar–40'lar, yazarı bilinmiyor. Anonimo'nun lirden söz edip etmediği **doğrulanamadı**. Leonardo'nun lire dair hiçbir çizim/yazısı günümüze kalmamış (○) |
| b105 | c4 | 1418–1420 | **Yumurta:** Benzoni (1565) hikâyeyi **Kolomb'a** bağlar; **Vasari** Brunelleschi'ye bağlar ve Benzoni'den 15 yıl önce (≈1550; Grokipedia özeti, düşük güven); **Pacioli** *De viribus quantitatis* (ms. Bologna, 1496–1508; bir kaynak 1509) ve **Piero da Filicaia** elyazması (16. yy başı) Brunelleschi'yle bağlar (Palmarini–Sosnowski makalesi) | ○ ANEKDOT | S43 | Makalenin metni görülmedi, yalnız özet/anahtar sözcükler. Manetti'nin yumurtayı **anıp anmadığı** doğrulanmadı. Vasari'de 1550 mi 1568 mi: çözülmedi |
| b106 | c4 | — | **Lippi'nin kilitlenmesi:** Vasari: Cosimo Lippi'yi evinde çalışırken **kilitletti**; Lippi yatak çarşaflarını makasla kesip **ip yaptı**, pencereden indi; Cosimo pişman olup ona serbestlik tanıdı; aynı pasajda "dâhiler göksel varlıktır, yük hayvanı değil" fikri (kimin ağzından olduğu özette karışık) | ◐ ANEKDOT | S44 | Fordham + Wikisource çevirileri. Vasari'nin aynı hayattaki **korsan hikâyesi** Konody ve Catholic Encyclopedia tarafından "masal/romans" sayılır: Vasari'nin Lippi bölümü güvenilirlik açısından karışık |

---

## 4. Canlı ayrıntılar

Tablo: `# | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı`. **Alıntıların İngilizce kısmı arama özetinde başkasının çevirisi olarak göründü** (özgün İtalyanca/Latince hiçbir yerde görülmedi, çevirmenler çoğunlukla doğrulanamadı). **Türkçe karşılıklar bize aittir.** "Birebir yok" yazan yerde özet yalnız dolaylı aktarım verdi; uydurma tırnak konmadı. Doğrulanamayan söz senaryoda "…diye aktarılır" çerçevesiyle kullanılır.

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| bd1 | c14 | Galileo, uyduları adlandırmak için Büyük Dük'ün sekreterine **iki seçenek** sunar: yalnız Cosimo'nun adı mı, dört kardeşin adı mı; ilk keşfeden olarak ad verme hakkını savunur | Galileo, 13 Şub 1610 mektubu (Wikipedia *Galilean moons* özeti; mektubun kendisi görülmedi) | ◐ | Latin adlar (özetten): *Cosmica Sidera* ↔ *Medicea Sidera* / TR: "Cosimo'nun yıldızları" ↔ "Medici yıldızları". Mektup cümlesi **birebir kullanılmaz** |
| bd2 | c14 | Vinta'nın yanıtı övgü doludur | Belisario Vinta → Galileo, 10 Şub 1610 (Museo Galileo/IMSS Vinta biyografi sayfası özeti) | ○ | EN (çeviri, çevirmen yok): "[...] Your idea of naming the new planets you have discovered after His Highness is generous and heroic" / TR: "[…] Keşfettiğiniz yeni gezegenlere Hazretlerinin adını verme düşünceniz cömert ve kahramanca." Senaryoda "diye aktarılır" |
| bd3 | c14 | Kapak sayfasında dört uydunun adı | *Sidereus Nuncius* kapağı, Venedik, Mar 1610 (Calisphere, Museo Galileo) | ◐ | Latin (özetten): *Medicea sidera* / TR: "Medici yıldızları". Kapak metninin tamamı görülmedi |
| bd4 | c14 | Bir kitap, bir **aletle birlikte teslim**: pusula kitabının her nüshası bir pusulayla satıldı; ithaf genç Prens Cosimo'ya | Museo Galileo, *Le operazioni del compasso geometrico e militare* (1606) | ◐ | Birebir yok. (Kurye çerçevesine uygun görsel: kitap + alet paketi) |
| bd5 | c14 | 1633: elçi Niccolini, Büyük Dük caymayı düşünürse Galileo'nun geçimini kendi cebinden karşılamayı teklif eder | Museo Galileo, Niccolini biyografisi | ○ | Birebir yok (özet). PBS'in "masrafı kesti" anlatısıyla gerilimli ama bağdaşabilir (teklif koşullu; bm2) |
| bd6 | c14 | *Euridice*'de Peri **Orfeo'yu kendisi söyledi**; Euridice'yi Vittoria Archilei | Wikipedia | ◐ | Birebir yok |
| bd7 | c14 | Caccini'nin acelesi: partisyonu Peri'ninkinden **altı hafta önce** bastırdı | Wikipedia | ◐ | Birebir yok. (Kibre/rekabete yönelik hafif mizah malzemesi; kurbana değil) |
| bd8 | c14 | 1700 envanterindeki satır | Medici envanteri, 1700 (Met denemesi özeti) | ◐ | EN (çeviri): "newly invented by Bartolomeo Cristofori" / TR: "Bartolomeo Cristofori tarafından yeni icat edilmiş." İtalyanca özgün görülmedi |
| bd9 | c14 | Saray müzisyeninin kenar notu | Federigo Meccoli, 1700 (Met denemesi özeti) | ◐ | IT (özetten): *Arpicimbalo del piano e forte* / TR: "pianolu ve forteli arpicembalo". Notun devamı özette İngilizce paraphrase |
| bd10 | c14 | Aletin ilk basılı adı | Scipione Maffei, *Giornale de' letterati d'Italia*, 1711 | ◐ | IT (özetten): *gravicembalo col piano, e forte* / TR: "piano ve forte'li klavsen" |
| bd11 | c14 | 1716 envanterinde imza | 1716 envanteri (Wikipedia özeti) | ○ | IT (özetten): *Bartolommeo Cristofori Custode* / TR: "Bakıcı (koruyucu) Bartolommeo Cristofori" |
| bd12 | c11 | **Machiavelli'nin akşam ritüeli** | Machiavelli → Vettori, 10 Ara 1513; çeviriler (S15, S17) | ◐ | EN (arama özetindeki bir çeviri; çevirmen doğrulanamadı): "When evening comes, I return home and enter my study; on the threshold I take off my workday clothes, covered with mud and dirt, and put on the garments of court and palace. Fitted out appropriately, I step inside the venerable courts of the ancients" / TR: "Akşam olunca eve dönüp çalışma odama giriyorum; eşikte çamura ve toza bulanmış gündelik giysilerimi çıkarıp saray ve divan giysilerimi giyiyorum. Yakışır biçimde donanmış olarak eskilerin saygıdeğer saraylarına giriyorum." (Başka çevirilerde "regal and courtly garments") |
| bd13 | c11 | "Küçük eser" ve ithaf niyeti | aynı mektup (Spartacus Educational çevirisi) | ◐ | EN: "I have composed a little work On Principalities; there I plunge as deeply as I can into consideration of this subject" ve "so I dedicate it to his Magnificence Giuliano" / TR: "*Prensliklere Dair* küçük bir eser yazdım; bu konunun içine elimden geldiğince derin dalıyorum" ve "bu yüzden onu Muhteşem Giuliano'ya ithaf ediyorum." (İkinci cümlenin öncesi özette yok: bağlam eksik) |
| bd14 | c11 | İthaf mektubu: hediye geleneği | *Prens* ithafı (Marriott çevirisi; çok sitede aynı metin) | ◐ | EN (özetteki Marriott): "whence one often sees horses, arms, cloth of gold, precious stones, and similar ornaments presented to princes" / TR: "bu yüzden prenslere sık sık at, silah, altın işlemeli kumaş, değerli taş ve benzeri süslerin sunulduğu görülür." |
| bd15 | c11 | İthaf mektubu: son cümle | idem | ◐ | EN: "you will see how unmeritedly I suffer a great and continued malignity of fortune" / TR: "talihin büyük ve sürekli kötülüğüne ne denli haksız yere katlandığımı göreceksiniz." |
| bd16 | c11 | İthaf mektubu: **ressam benzetmesi** | idem | ◐ | Birebir yok (özet parafrazı): ovadan dağları, yüksekten ovayı seyreden peyzaj ressamı gibi, düşük mevkideki yazar da prenslerin işlerini yazabilir |
| bd17 | c11 | **Av köpekleri:** Vettori el yazmasını Lorenzo'ya sunduğu gün prens iki av köpeği hediye almıştı; kitabın sunumu köpeklerin gölgesinde kaldı | La Civiltà Cattolica, "Il Principe di Machiavelli" (tarihi ve yazarı doğrulanamadı) | ○ ANEKDOT | Birebir yok (özet parafrazı). Ridolfi/birincil kaynak doğrulanmadı |
| bd18 | c11 | **Gizli oda:** Yeni Sakristi altında duvarlarda kömür ve sanguin çizimler; 1975'te restoratör iki kat sıvayı kaldırırken fark etti | The Florentine, Atlas Obscura, Geographical Cure, Destination Florence (S12) | ◐ | Birebir yok. Bazı çizimler Michelangelo'ya ait değil |
| bd19 | c11 | **San Niccolò kulesi:** kuşatma sırasında cumhuriyetçi komutanlar bu kilisede sadakat yemini etmişti; Michelangelo kulenin tabanındaki küçük odada sığındı | arte.it; Facaros & Pauls rehberi (S12) | ◐ (gelenek) | EN (özet): "sheltered for several days in a small room at the base of the bell tower" / TR: "çan kulesinin dibindeki küçük bir odada birkaç gün sığındı." Kaynak "geleneksel olarak" der |
| bd20 | c11 | ***Gece*** ve yanıt: Strozzi'nin dörtlüğü izleyicinin heykeli uyandırıp canlı olup olmadığını sınamasını söyler | G. B. Strozzi ve Michelangelo, c.1545–46 (Ekphrastic Review, Freiburg, rivista-incontri özetleri) | ◐ | IT (yalnız ilk dizeler, özetten): *La Notte, che tu vedi…* ve *Caro m'è 'l sonno…*. **Satırların kalanı görülmedi: birebir yazılmadı** |
| bd21 | c4 | Palla Strozzi'nin **şahini:** bankacı kendi soyadının oyununu (*strozzieri* = şahinci) siparişini verdiği resme işletti | Gentile da Fabriano, 1423 (Wikipedia, Christian Century özetleri) | ◐ | Birebir yok |
| bd22 | c4 | **Lippi'nin çarşaf ipi** | Vasari, *Vite* (Fordham çevirisi; olaydan yüz yıl kadar sonra) | ◐ ANEKDOT | EN: "Cosimo therefore, when he was working for him in his house, caused him to be shut in, so that he could not go out and waste his time; but he, cutting up the sheets of the bed with a pair of scissors, made a rope and let himself down by the window." / TR: "Bu yüzden Cosimo, Lippi kendi evinde çalışırken onu içeri kilitletti ki dışarı çıkıp vaktini boşa harcamasın; o ise yatağın çarşaflarını makasla kesip bir ip yaptı ve kendini pencereden aşağı bıraktı." |
| bd23 | c6 | **Faun:** Lorenzo'nun dişe dair şakası | Condivi 1553, Vasari (Symonds, Finestre sull'Arte özetleri) | ◐ ANEKDOT | Birebir yok (özet parafrazı): Lorenzo yaşlıların dişlerinin tam olmayacağını söyledi; Michelangelo bir dişi kırıp diş etini oydu. (M3 §3 #31'deki Condivi çeviri cümlesi korunur) |
| bd24 | c6 | **Hane içi:** oda, sofra, 5 dukat; Vasari'de mor harman | Condivi (Gutenberg çevirisi), Vasari | ◐ | Birebir yok (özet parafrazı). EN (Vasari, başka çeviri): "violet-coloured mantle" / TR: "mor renkli harmani" |
| bd25 | c6 | **Torrigiani'nin böbürlenmesi** | Cellini, *Vita*, Symonds çevirisi (Cellini 1558–66'da yazdı; olaydan on yıllar sonra) | ◐ ANEKDOT | EN: "…bone and cartilage go down like biscuit beneath my knuckles" / TR: "…kemik ve kıkırdağın parmak eklemlerimin altında bisküvi gibi çöktüğünü [hissettim]." |
| bd26 | c6 | **Leonardo'nun lir:** kendi yaptığı, gümüş, at kafatası biçimli | erenow.org'daki bir Leonardo biyografisi (URL yolu: *leonardo-da-vinci-the-flights-of-the-mind*; yazar adı özette yok); Vasari'ye dayanır | ○ ANEKDOT | EN (modern biyografi parafrazı, **Vasari'nin sözü değil**): "a lyre that he had made himself, mostly of silver, in the shape of a horse's skull" / TR: "kendi yaptığı, çoğunlukla gümüşten, at kafatası biçiminde bir lir". Vasari'nin kendi cümlesi görülmedi |
| bd27 | c5 | **Pico'nun ölüm günü** Charles VIII'in giriş günüyle çakışır | S36 sayfalarından ikisi (özet "aynı gün Floransa Fransız ordusuna düştü" der; hangileri olduğu ayrışmıyor) | ◐ | EN (özet): "on the very day (November 17) on which Charles VIII made his entry into Florence" / TR: "Charles VIII'in Floransa'ya girdiği günün ta kendisinde, 17 Kasım." |
| bd28 | c5 | Ficino'nun 1462 mektubu | Ficino, Eylül 1462 (SEP özeti) | ○ | EN: "the Academy you arranged for us on the estate in Careggi" / TR: "Careggi'deki mülkte bizim için düzenlediğin Akademi." Alıcı belirsiz, Latince görülmedi |
| bd29 | c12 | San Luca'nın kendi tarihi | Accademia di San Luca resmî sitesi | ◐ | IT (özetten): "Il passaggio da Universitas in Accademia delle Arti della Pittura, della Scultura e del Disegno, per iniziativa del pittore Girolamo Muziano, venne ufficialmente sancito da un Breve emanato da Gregorio XIII nel 1577." / TR: "Universitas'tan Resim, Heykel ve Çizim Sanatları Akademisi'ne geçiş, ressam Girolamo Muziano'nun girişimiyle, 1577'de XIII. Gregorius'un çıkardığı bir breve ile resmen onaylandı." |
| bd30 | c16 | Uffizi'nin **yavaş açılışı** | Uffizi resmî sayfaları | ◐ | EN: "gradually opened to a select number of visitors from outside the court" ve "for the ornament of the State" / TR: "saray dışından seçilmiş bir ziyaretçi kitlesine kademeli olarak açıldı" ve "Devletin süsü için." Özetin alıntıları. 24 Haz 1769: Aziz Yuhanna günü |
| bd31 | c16 | **Désilets** *AC II* ve tarih üzerine | Kotaku, "Assassin's Creed II Spoiler Talk With Patrice Desilets" (yıl özette yok) | ○ | EN (özetteki alıntılar): "a pain in the ass sometimes" ve "It's a feeling" / TR: "bazen baş belası" ve "Bu bir his meselesi." Tam metin görülmedi |
| bd32 | c16 | The Florentine'in dizi eleştirisi | The Florentine, 6 Oca 2017 | ◐ | EN: "The Duomo's construction began almost a decade before Giovanni di Bicci's death. Donatello's stunning nude bronze David had not yet been created during the trial that led to Cosimo's exile." / TR: "Duomo'nun inşaatı Giovanni di Bicci'nin ölümünden neredeyse on yıl önce başlamıştı. Donatello'nun çarpıcı çıplak bronz David'i, Cosimo'yu sürgüne götüren yargılama sırasında henüz yaratılmamıştı." |
| bd33 | c4 / c5 | Bruni'nin gücü | Wikipedia "Leonardo Bruni" | ◐ | EN: "Though he occupied one of the highest political offices, Bruni was relatively powerless compared to the Albizzi and Medici families." / TR: "Floransa'nın en yüksek makamlarından birini işgal etse de Bruni, Albizzi ve Medici ailelerine kıyasla görece güçsüzdü." |
| bd34 | c7 | Poliziano'nun *Commentarium*'u | Celati yayını incelemesi (Erudit) | ◐ | EN (özet): "an act of political propaganda" ve "dark counterpoint to Poliziano's Stanze" / TR: "bir siyasi propaganda eylemi" ve "Poliziano'nun *Stanze*'sinin karanlık karşı noktası." |

---

## 5. Sayılar ve ölçüler; mit/tartışma; TR-BAĞ

### 5.1 Sayılar ve ölçüler

Aralık veya çelişki varsa hepsi yazıldı.

| # | Bölüm | Ölçü | Değer(ler) | Çelişki / aralık | Sınıf | Kaynak |
|---|---|---|---|---|---|---|
| bs1 | c14 | *Sidereus Nuncius* yayını | 13 Mar 1610, Venedik | — | ◐ | S1 |
| bs2 | c14 | İlk gözlem | 7 Oca 1610 (3 "yıldız"); Ocak içinde 4 | 13 Oca "dördüncü" HAFIZA | ◐ | S1 |
| bs3 | c14 | Mektup dizisi | 10 Şub (Vinta→Galileo) · 13 Şub (Galileo→sekreter) · 19 Mar (teleskop + nüsha) | sıra ve kimlik karışık | ◐ / ○ | S2, S3 |
| bs4 | c14 | Dört kardeş | Cosimo, Francesco, Carlo, Lorenzo | — | ◐ | S3 |
| bs5 | c14 | Padua → Floransa | 10 Haz 1610 istifa · Tem 1610 atama (· eski EB 1611) | çelişki | ◐ / ○ | S2 |
| bs6 | c14 | Galileo'nun maaşı | 1.000 Floransa scudosu/yıl (Floransa); 1.000 florin/yıl (Padua, "Venedik'ten") | tek makale; makale Cosimo II'yi "III" yazıyor | ○ | S2 |
| bs7 | c14 | Pusula kitabı | 1606; ≈60 nüsha; Padua; Marinelli; her nüsha bir pusulayla | — | ◐ | S4 |
| bs8 | c14 | Cosimo II ömrü | 1590–1621 | gün/ay HAFIZA | ◐ | S4, S2 |
| bs9 | c14 | Cimento | 1657–1667 (10 yıl); son toplantı 5 Mar 1667; 5 üye adı; *Saggi* 1667 | Treccani'de "1666" yazımı | ◐ | S5 |
| bs10 | c14 | Kurucu ömürleri | Leopoldo 1617–75; Ferdinando II 1610–70 | — | ◐ | S5 |
| bs11 | c14 | Camerata | c.1573–87 (Britannica); ilk kayıtlı toplantı 14 Oca 1573; zirve 1577–82 | — | ◐ / ○ | S9 |
| bs12 | c14 | *Dafne* | 1597 Carnaval ya da 1597–98; 455 dizelik libretto | — | ◐ | S7 |
| bs13 | c14 | Düğün günleri | 5 Eki 1600 vekâlet · 6 Eki *Euridice* · 17 Ara 1600 Lyon | — | ◐ | S7, S8 |
| bs14 | c14 | Caccini'nin *Euridice*'si | basım: Peri'den 6 hafta önce; sahne 5 Ara 1602 | — | ◐ | S7 |
| bs15 | c14 | Cristofori ömrü | 1655–1731/32 | 27 Oca 1731 ↔ 1732 | ◐ | S10 |
| bs16 | c14 | İşe alım | 1688 (≈33 yaşında) / ≈1690 | — | ◐ | S10 |
| bs17 | c14 | Prens'in klavyeleri | ≈40 klavsen + spinet | tek özet | ○ | S10 |
| bs18 | c14 | 1700 envanteri | çekiç, sönümleyici (◐); 2 klavye, 4 oktav (○) | — | ◐ / ○ | S10 |
| bs19 | c14 | Maffei | 1711; 3 piyano (biri Ottoboni'ye) | Ottoboni tek özet | ◐ / ○ | S10 |
| bs20 | c14 | Hayatta kalan piyanolar | 1720 (Met), 1722 (Roma), 1726 (Leipzig) | — | ◐ | S10 |
| bs21 | c11 | Yeni Sakristi | 1519/1520–1534; Giuliano mezarı 1526–33; *Gece* 1526–31 | 1519 mu 1520 mi | ◐ / ○ | S11, S13 |
| bs22 | c11 | Laurenziana | tasarım 1524; Tribolo 1550; Ammannati 1558/1559; açılış ≤1571 | 1558/59 | ◐ | S14 |
| bs23 | c11 | 1529–30 | unvan 1529; kaçış 21 Eyl 1529; gizli oda ≈7 m × 2 m, 2–3 ay ↔ San Niccolò "birkaç gün"; keşif 1975 | yer ve süre çelişkisi | ○ / ◐ | S12 |
| bs24 | c11 | Machiavelli 1513 | adı ≈20 kişilik listede; 12 Şub tutuklama (○); 23 Şub Boscoli–Capponi idamı; Mart af; ≈3 ay | süre | ◐ / ○ | S16 |
| bs25 | c11 | *Prens* mektubu | 10 Ara 1513 | — | ◐ | S15 |
| bs26 | c11 | *Istorie* | 8 Kas 1520 sipariş; 57 → 100 florin; Mayıs 1526 sunum | "100 florin" bir kaynakta doğrudan | ◐ / ○ | S17 |
| bs27 | c11 | *Prens* basımı | 4 Oca 1532 (Blado); 8 May 1532 (Giunti); 10 yıl ayrıcalık; ölümden 5 yıl sonra | — | ◐ | S18 |
| bs28 | c11 | Surlar | Nis 1526 magistratura; 14 yıllık aradan sonra Palazzo Vecchio | — | ◐ | S21 |
| bs29 | c16 | *AC II* | 17 Kas 2009 (PS3/X360); 3 Mar 2010 (Win); 1 Eki 2010 (Mac); hikâye 1476'da başlar | — | ◐ | S24 |
| bs30 | c16 | Johansson | 2004; 18 dil (○) | yayıncı hatası | ◐ / ○ | S26 |
| bs31 | c16 | Padgett–Ansell | 1993; *AJS* 98(6): 1259–1319 | — | ◐ | S27 |
| bs32 | c12 | Akademiler | 1563 Floransa · 1577 breve · 1593 Zuccari · 1607 (ya da 1593) statüler · 1648 Paris · 1768 Londra | San Luca doğumu 1572 / 1577 / 1583 / 1593; principe 1593 / 1598 | ◐ | S29 |
| bs33 | c16 | Uffizi | ≈1581 galeri · 17. yy seçilmiş ziyaretçi · 1737 pakt · 24 Haz 1769 | M3: "1765" diyen bir kaynak | ◐ | S30 |
| bs34 | c12 | Boboli | 1549/1550 başlangıç; Pitti 1550; Grotta 1557–93 (Buontalenti 1583–93) | 1549 ↔ 1550 | ◐ | S31 |
| bs35 | c16 | Capitoline | 1471; 1734 | — | ◐ | S32 |
| bs36 | c4 | Gentile / Palla Strozzi | 1423; 300 florin (○) | sipariş 1420 / "1423 öncesi" | ◐ / ○ | S33 |
| bs37 | c4 | Pazzi Şapeli | 1429 sipariş; başlangıç 1440–43; bitiş 1461 / 1466 / 1469 / 1470'ler | geniş aralık | ◐ | S34 |
| bs38 | c4 | Palazzo Strozzi | 6 Ağu 1489; arsa 1473–89; Filippo 1466'da döndü, 1491'de öldü; bitiş 1538 | Il Cronaca 1490–1504 | ◐ | S35 |
| bs39 | c5 | Pico | 1486 (900 tez); 7 + 6 tez; 1488 tutuklama; 17 Kas 1494 ölüm | — | ◐ | S36 |
| bs40 | c4 / c5 | Bruni | şansölye 1410–11 ve 1427–44; *Historiae* 1439 | — | ◐ | S38 |
| bs41 | c6 | Michelangelo'nun aylığı | 5 dukat/ay; "dört yıl" (Vasari) | HAFIZA 1489–92 | ◐ | S40 |
| bs42 | c4 | Yumurta anekdotunun yaşı | Pacioli ms. 1496–1508 (veya 1509); Benzoni 1565; Vasari ≈1550 (?) | 1550 ↔ 1568 | ○ | S43 |

### 5.2 Mit/efsane ve tarihçi tartışmaları

Biçim: **iddia → kim ne diyor → değerlendirme → video davranışı önerisi.**

**bm1. Uydulara Medici adını kim verdi?**
- **Kim ne diyor:** Wikipedia (*Galilean moons*): Galileo 13 Şub 1610'da sekretere **iki seçenek** sundu; sekreter ikincisini önerdi. Museo Galileo (katalog): Büyük Dük'ün **kendisi**, sansasyonel keşfi kişisel adı yerine aile adına bağlamayı yeğledi. Sky & Telescope (2020): öneriyi Cosimo'ya atfeder. Biagioli'nin kitabının Academia.edu özeti: adı seçmenin **Vinta**'ya ait olduğu (◐/○). Hepsi iki seçeneğin sunulduğunda birleşir.
- **Değerlendirme:** seçenekler ◐; **seçimi yapanın kimliği açık** (dört ayrı atıf).
- **Video:** "Galileo iki ad önerdi; saray ikincisini seçti." Kişi atfı yapılmaz. **İroni:** kalıcı adlar Medici'nin değil, **Marius'un** (Wikipedia/NWE ◐; adların kendisi HAFIZA-Y).

**bm2. "Medici Galileo'yu korudu"**
- **Kim ne diyor:** 1610'da unvan, maaş, ders yükü yok ◐ (b14). 1633: *Dialogo* Ferdinando II'ye ithaflı; PBS: desteği sürerse Ferdinando'nun Toskana'daki hayatı güçleşirdi, yargılama sırasında masrafları kesti; Museo Galileo: Ferdinando aklanma için girişti, mahkûmiyet sonrası temkinli iptal/hafifletme denedi, elçi Niccolini masrafı üstlenmeyi teklif etti ve ikamet izni aldı; bir başka kaynak: Ferdinando yaşlı adamı ziyaret edip teselli etti (○).
- **Değerlendirme:** "sınırlı koruyucu" ◐; masraf konusunda iki kaynak farklı şey söylüyor (PBS "kesti"; Niccolini biyografisi "cayarsa ben üstlenirim"): ikisi bağdaşabilir, tek başına çelişki sayılmaz ○.
- **Video:** "Medici Galileo'yu kollayabildiği yere kadar kolladı"; masraf ayrıntısı söylenmez ya da iki taraf ayrı söylenir. **Ağır sahne: mizah kapalı.**

**bm3. "Opera Medici'nin icadı / ilk opera *Euridice*"**
- **Kim ne diyor:** *Dafne* önce (Corsi sarayı, 1597/98), müziği kayıp ◐; *Euridice* tam ulaşan en eski opera ◐; Medici düğünü için sahnelendi ◐; Rinuccini–Peri–Caccini–Corsi–Bardi–Cavalieri çevresi.
- **Değerlendirme:** "Medici sahneyi ve bahaneyi verdi; icat soylu salon çevrelerinin" ◐.
- **Video:** "Günümüze ulaşan en eski opera, bir Medici düğünü için." "İlk" ve "icat etti" denmez.

**bm4. "Camerata bir kurumdu"**
- **Kim ne diyor:** Wikipedia: ad Bardi çevresinin kendi ürettiği terim, Caccini ithafında geçer; Palisca kitabının tanıtımı: "gayriresmî disiplinlerarası akademi"; ilk kayıtlı toplantı 14 Oca 1573 (○).
- **Değerlendirme:** gevşek salon çevresi ○/◐; **"Platon Akademisi" ile aynı tuzak** (bm10).
- **Video:** "Kont Bardi'nin salonu"; "Camerata" tırnaklı.

**bm5. "Piyanoyu Medici icat etti"**
- **Kim ne diyor:** Cristofori icat etti ◐; Medici'nin payı **istihdam ve koleksiyon:** 1688 işe alım, ≈40 klavyeli prens (○), 1700 envanter kaydı; adı Maffei koydu (1711). Alet 1700'de "arpicembalo" olarak kayda geçti.
- **Video:** "Prens Ferdinando'nun ustası Cristofori." "Medici icat etti" denmez.

**bm6. *Prens* üzerine üç karışıklık**
- (a) **"Lorenzo il Magnifico'ya ithaf"** → yanlış; ithaf **Lorenzo di Piero'ya** (1492–1519), Il Magnifico'nun **torununa** ◐ (S15, S19). Önce niyet Giuliano ◐.
- (b) **Geçiş yılı:** 1516 (HAFIZA) ↔ "1513" (Marriott sayfa metaverisi, La Civiltà Cattolica) ↔ "sonraki üç yıl kadar" (S15): **açık**.
- (c) **Okudular mı?** "Bilinmiyor" ◐; av köpekleri anekdotu ○ ANEKDOT.
- (d) **Amaç:** Medici'nin gözüne girip yönetime dönmek ("Floransa yönetimine yeniden giriş", bir kaynak) ◐.
- **Video:** "Prens'i Lorenzo di Piero'ya sundu; Il Magnifico'nun torunuydu." Köpek anekdotu "diye anlatılır" + ○.

**bm7. "Machiavelli Medici'nin düşmanıydı"**
- **Kim ne diyor:** 1512 görevden alma ◐; 1513 komplo listesinde adı, işkence, af ◐ (komploda rolü için delil zayıf); Medici'ye *Prens* ithafı ◐; Giulio'nun *Istorie* siparişi ◐; 1526'da Medici papasının surlar işi ◐ (b39). Cumhuriyet'in 1527'de dışlaması HAFIZA-O.
- **Değerlendirme:** Medici'nin hem **kurbanı** hem **işvereni**; "düşman" etiketi aşırı basit ◐.
- **Video:** "Medici'nin hapsinden çıktı, sonra Medici'ye kitap yazdı." İşkence ayrıntısında mizah kapalı.

**bm8. Michelangelo 1530'da nerede saklandı?**
- **Kim ne diyor:** İki gelenek (b42). San Niccolò: arte.it + rehber (◐ gelenek). Yeni Sakristi altı: Artnet + The Florentine + Geographical Cure (2–3 ay; Figiovanni). Bir kaynak "üç yıl gizli oda" iddiasını sorgular (○). Condivi/Vasari metni görülmedi.
- **Video:** "Birinci anlatıya göre …, ikincisine göre …". **San Miniato kulesi (savunma) ile San Niccolò kulesi (saklanma) karıştırılmaz.**

**bm9. Yumurta anekdotu (güncel)**
- **Kim ne diyor:** Vasari ≈1550 (Benzoni'den 15 yıl önce; düşük güvenli özet) · Pacioli (ms. 1496–1508) · Filicaia (16. yy başı) (Palmarini–Sosnowski özeti, ○) · Manetti'de yok/var: doğrulanamadı. M3'ün "≈130 yıl" hesabı belki ≈80–90 yıl.
- **Video:** "Yarışmadan on yıllar sonra yazıya geçen bir hikâye" (nitelikli). Brunelleschi'nin iç dünyasına girilmez.

**bm10. "Platon Akademisi"**
- **Kim ne diyor:** SEP: resmî okul değil; Cosimo 1463'te küçük Careggi mülkü verdi; **Eylül 1462 mektubunda "Akademi" sözü** (○). IEP: Ficino'nun akademi göndermeleri Platon el yazması ve çeviriler olabilir; "başkanı olsun olmasın savunucuydu". M3: Hankins 1991 *Myth*, 2002 *Invention*.
- **Değerlendirme:** "Akademi" kelimesi **Ficino'nun kendi dilinde var**; kurum olarak var olduğu **kanıtlanmıyor**: ikisi birlikte söylenir.
- **Video:** "Ficino'nun 'Akademi' dediği, Careggi'deki dostlar çevresi"; tırnak.

**bm11. Akademi zinciri ve "ilk"**
- **Kim ne diyor:** Floransa 1563 → Roma: kurumun kendi sitesi 1577 breve + Zuccari 1593; Treccani "Floransa modelinde" ◐. Roma → Paris 1648: "San Luca'dan esinlendi" ○ (tek kaynak). Londra 1768: Paris/Roma ile bağ **özetlerde yok**. HAFIZA-O: 1676 San Luca–Fransız Akademisi birleşmesi.
- **Değerlendirme:** zincirin **ilk halkası ◐**, sonrası ○/kanıtsız. "İlk" için "ilk büyük, devlet destekli" nitelikli.
- **Video:** "Roma, Floransa'nın modelini aldığını söyler" (Treccani'ye dayanır); Paris ve Londra için zincir kurma.

**bm12. "Uffizi ilk modern müze"**
- **Kim ne diyor:** Uffizi resmî: 24 Haz 1769; kendini "ilk modern müzelerden biri" diye tanımlar. Capitoline: 1471 bronzlar, 1734 halka açılış ("dünyanın en eski halk müzesi" iddiası) ◐. Ashmolean 1683 HAFIZA.
- **Video:** "İlk" denmez; "halka açılışı 1769".

**bm13. "Medici etkisi" (Johansson) ve tarihçiler**
- **Johansson:** farklı alanların kesişimi yenilik üretir; Medici başlığa isim verir ◐ (S26). Ubiquity incelemesi tarihsel iddiayı "Medici'nin çok disiplinli düşünürleri bir araya getirmesi" diye özetler (○). **Tarihçi değerlendirmesi bulunamadı** (aramada yok).
- **Tarihçilerin ilgili görüşleri (bu tur ve M3):** Gombrich–Kempers–Goldthwaite (M3 §5.1 ◐): Medici'yi "tipik patron" saymaya itiraz; Goldthwaite talebi zenginlik birikimine bağlar. Hankins: Ficino'nun "Akademi"si özel ders ortamı (M3; S39). Kent (bir öğrenci çalışmasının aktarımıyla, ○, S28): San Lorenzo programı iktidar ifadesi; Cosimo hümanistleri sarayına çekerek onları ailenin siyasi kaderine bağlamayı umdu. Padgett–Ansell (◐, S27): Cosimo'nun gücü ağdaki köprü konumundan. Bir ders kitabı sayfası: Rönesans Medici iktidarından önce başlamıştı (○, S28).
- **Değerlendirme:** "Medici etkisi" bir **iş literatürü metaforu**; tarihçiler Medici'yi "kesişim mimarı" olarak değil, **görünür patron ve siyasi ağ düğümü** olarak okur ◐/○.
- **Video:** Kullanılırsa: "modern bir iş kitabı, Medici adını 'farklı alanların kesişimi' metaforu için kullandı"; tarihsel iddia olarak sunulmaz.

**bm14. *AC II* ve dizi: sapma haritası (b63–b70)**
- **Kim ne diyor:** *AC II*: çekirdek gerçek, Templar/Assassin kurgusu; sapmalar b67. Geliştirici: Désilets "his" (○). Dizi: The Florentine hata listesi (◐): *David* ve kubbe zamanlaması, Giovanni'nin "cinayeti".
- **Video:** "Oyun/dizi şunu böyle gösterdi, tarih şöyle" biçimi; yalnız ◐ olanlar; fan listeleri kullanılmaz.

**bm15. "Medici-merkezli anlatıya karşı"**
- **Kim ne diyor:** Palla Strozzi (1427'de en zengin, 1423 Gentile) ◐; Palazzo Strozzi (1489, Medici sarayını aşmak üzere) ◐; Pazzi Şapeli (1429) ◐; Rucellai–Tornabuoni–Sassetti–Brancacci (M3 ◐). Cosimo I'in sonradan Palazzo Strozzi'ye el koyması ○.
- **Değerlendirme:** Medici'nin **rakipleri de büyük patrondu**; ölçek ve siyasi görünürlük Medici'yi ayırır (M3 §9 #3).
- **Video:** "Strozzi'ler de saray yaptırdı; Medici sarayından büyük olsun diye."

**bm16. Leonardo'nun lirle gönderilişi**
- **Kim ne diyor:** Lir = Vasari (◐); Anonimo'da var mı: doğrulanamadı; "Lorenzo gönderdi" = modern (○).
- **Video:** "Vasari'ye göre Leonardo lirle gitti"; Lorenzo'nun göndermesi "diye anlatılır".

**bm17. Pico'nun ölümü ve "zehir"**
- **Kim ne diyor:** 17 Kas 1494 ◐; zehir söylentileri ○ (tek kaynak, "bazıları zehirlendi dedi" düzeyinde); 2007 arsenik çalışması aranmadı (HAFIZA D).
- **Video:** "Ölümü zehir söylentisiyle anılır"; kesinlik yok.

### 5.3 TR-BAĞ: Osmanlı / Türkiye ile ilgili

| # | Bölüm | Bağ | Olgu | Sınıf | Kaynak | Kullanım notu |
|---|---|---|---|---|---|---|
| bt1 | c11 | *Prens*'te Türk (Osmanlı) örneği | *Il Principe*'nin IV. bölümünde "Türk" monarşisi (tek hükümdar, diğerleri onun kulları) ile Fransa krallığı karşılaştırılır | HAFIZA (Y) | — | Marriott çevirisinin IV. bölümünden doğrula. Türk izleyiciye doğal çıpa; bu turda aranmadı |
| bt2 | c5 / c10 | Pico'nun ölüm günü ↔ Charles VIII'in girişi ↔ Cem Sultan | Pico 17 Kas 1494'te öldü, bir kaynağa göre aynı gün Charles Floransa'ya girdi (b93); Charles'ın Napoli seferinde Cem Sultan'ı yanında taşıdığı HAFIZA | ○ / HAFIZA | S36; M2 K92, K98 | Cem Sultan M2 kapsamında (HAFIZA-O); burada yalnız tarih örtüşmesi |
| bt3 | c14, c16 | Galileo, Cimento, *Euridice*, Camerata, Cristofori, Uffizi, Accademia | **Bu turda doğrulanmış Osmanlı/Türkiye bağı çıkmadı** | — | — | c14'te TR çıpası yalnız M3'ün Doğu Matbaası/ferman malzemesi (§6 #4) ve M4'ün Livorno–Santo Stefano malzemesi |

---

## 6. Sahne adayları ("yıldız an")

Her adayda: belgelenmiş çekirdek, duyusal malzeme (**yalnız belgeli olan**), belirsiz noktalar, çerçeve önerisi, mizah ve iç dünya sınırı. **Kural: iç dünya yalnız kaynaktan** ("Ne düşündüğünü bilmiyoruz, ama ne yaptığını biliyoruz").

### Aday 1: Galileo'nun uyduları, 7 Ocak – Haziran 1610 (c14)

- **Belgelenmiş çekirdek:** 7 Oca 1610'da Jüpiter'in yanında üç küçük "yıldız", Ocak içinde dört (◐, b10) → Şubat'ta isimlendirme: Vinta'nın "cömert ve kahramanca"sı (10 Şub, ○, bd2) ve Galileo'nun iki seçenekli sorusu (13 Şub, ◐, bd1) → 13 Mar 1610'da Venedik'te kitap, kapakta *Medicea sidera* (◐, bd3) → 19 Mar'da teleskop ve nüsha Büyük Dük'e (○) → 10 Haz 1610'da Padua'dan istifa ve Floransa'da "Büyük Dük'ün Birinci Matematikçisi ve Filozofu" unvanı (◐; tarih çelişkili, b14).
- **Duyu (belgeli):** teleskop, nesne olarak Büyük Dük'e gönderildi (○); kitap kapağındaki Latince ad (◐); 1606'dan "kitap + alet" paketi (◐, bd4). Gecenin havası, sesi, ışığı özetlerde **yok**: uydurulmaz.
- **Belirsiz:** adı **kimin** seçtiği (bm1: dört atıf); istifa/atama günü; maaş (tek makale, ○); Galileo'nun iç dünyası (mektup dışında kaynak yok).
- **Çerçeve:** *"Dört yıldız, dört kardeş."* Kapı cümlesi: **adlar tutmadı** (kalıcı adlar Marius'un) ama Galileo Floransa'ya döndü; ve 1633'te aynı sarayın onu yalnız kısmen koruyabildiği (bm2) sahneye kapı. "O gece kimse bilmiyordu ki…" kalıbı bölümde **bir kez** ve yalnız belgeli sona (dört uydu, Medici adı) dayanarak.
- **Mizah (kuruma/kibre):** bir gök cismine hangi aile adı yakışır pazarlığı; "yıldızlar aileye zimmetlendi, kayıtlar tutmadı". **1633 sahnesinde mizah kapalı.**
- **Okunuş adayları (okunus.md):** Galileo Galilei, *Sidereus Nuncius*, *Medicea Sidera*, *Cosmica Sidera*, Belisario Vinta, Padua, Simon Marius.

### Aday 2: *Euridice*, 5–6 Ekim 1600 (c14 / c13)

- **Belgelenmiş çekirdek:** 5 Eki'de Duomo'da **vekâlet töreni** (Kardinal Aldobrandini; Ferdinando I damat yerine; şölen Palazzo Vecchio'da, Sala dei Cinquecento) (◐, b4) → 6 Eki'de Pitti'de ***Euridice***: Peri Orfeo'yu söyledi, Vittoria Archilei Euridice'ydi, Caccini çevresinden şarkıcılar, Peri'nin bazı parçaları Caccini'ninkiyle değiştirildi (◐, b5–b6) → en eski tam opera; *Dafne* kayıp (◐) → Caccini kendi nüshasını **altı hafta önce** bastırdı (◐, bd7); kendi *Euridice*'si 5 Ara 1602'de (◐) → dinî tören Lyon'da 17 Ara 1600 (◐).
- **Duyu (belgeli):** müziğin türü: "konuşmanın yükseltilmiş biçimi, yaylı çalgılarla desteklenen dramatik recitativo" (Wikipedia özeti, ◐). **Salonun ışığı, kalabalığı, alkış, kokular özetlerde yok.**
- **Belirsiz:** izleyici tepkisi, salondakiler, hangi parçaların Caccini'ye ait olduğu, sonun mutlu olup olmadığı, Marie'nin salonda olup olmadığı (HAFIZA).
- **Çerçeve:** *"Bir kız, bir krala vekâleten verildi; ertesi gün bir sanat türü sahnelendi."* Plutarkhos dokunuşu: Camerata'nın teorisyeni **Vincenzo Galilei**, astronom **Galileo**'nun babasıdır (◐, Britannica): "konuşur gibi şarkı söylemek" fikri ve "gökyüzüne bakan oğul" aynı hanenin işi. Kapı: Marie ileride Fransa'nın naibi ve Rubens'in müşterisi olacak (M4 #81, #84; HAFIZA).
- **Mizah (kuruma/kibre):** antik Yunan dramını diriltme iddiasıyla sonuç (opera) arasındaki mesafe; Caccini'nin matbaa acelesi. Kurbana (kişinin acısına) yönelmez.
- **Okunuş adayları:** *Euridice*, Jacopo Peri, Ottavio Rinuccini, Giulio Caccini, Vittoria Archilei, Jacopo Corsi, Giovanni Bardi, Emilio de' Cavalieri, Aldobrandini, Pitti, *Dafne*, Orfeo.

### Aday 3: Piyano / Cristofori, 1688–1711 (c14)

- **Belgelenmiş çekirdek:** 1688 (≈1690) Prens Ferdinando, Padua'dan Cristofori'yi saray enstrümanları bakıcısı olarak alır (◐, b24) → Pratolino (○) → **1700 envanteri**: "Cristofori tarafından yeni icat edilmiş" arpicembalo; çekiçler, sönümleyiciler (◐, b26, bd8) → Meccoli'nin kenar notu (◐, bd9) → **1711**: Maffei'nin makalesi, ad *gravicembalo col piano, e forte* (◐, bd10) → 1716 "Custode" imzası (○) → üç piyano bugüne kalmış (◐, b31).
- **Duyu (belgeli):** yalnız nesne: çekiç, sönümleyici (◐); iki klavye, dört oktav (○); Prens'in ≈40 klavsen/spineti (○). Atölye, ses, koku **yok**.
- **Belirsiz:** Cristofori'nin kişiliği ve mektupları; icat "anı" (1698 günlük kaydı şüpheli); Ottoboni (○).
- **İç dünya sınırı:** Cristofori'nin ne düşündüğü bilinmiyor; yalnız **ne yaptığı** belgeli: alet yapmak, saray envanterini tutmak.
- **Çerçeve:** *"Büyük icatlar bazen envanterde tek bir satır olarak doğar."* Kapı: aleti dünyaya duyuran saray değil, bir gazete makalesiydi (Maffei ◐; "makale olmasa icat saraylarda kalırdı" yorumu ○, **yorum olarak** söylenir).
- **Mizah (kuruma):** envanter dili ("yeni icat") ve bürokratik ad: önce "arpicembalo", sonra "piano e forte". Cristofori'ye değil, sisteme.
- **Okunuş adayları:** Bartolomeo Cristofori, Ferdinando de' Medici (Gran Principe), Pratolino, Federigo Meccoli, Scipione Maffei, Ottoboni, *arpicembalo*, *gravicembalo col piano e forte*, *Giornale de' letterati d'Italia*.

### Ek adaylar (kısa)

1. **Machiavelli'nin akşam giysisi (10 Ara 1513, c11):** Plutarkhos portresi; işkenceden sonra çiftlikte; çamurlu gündelik giysi → "saray giysisi" (◐, bd12); ithafın ressam benzetmesi (bd16); sonra av köpekleri ANEKDOT (○, bd17). Mizah: kuruma/kibre (saray giysisi giyen işsiz memur); **işkence anlatımında mizah kapalı.**
2. **Michelangelo'nun gizli odası (1530/1975, c11):** iki gelenek (bm8); duvarda kömür çizimler (◐, bd18). Mizah kapalı. Zweig yavaşlatması: "1975'te iki kat sıva".
3. **Lippi'nin çarşaf ipi (c4):** ANEKDOT ◐ (bd22); mizah serbest (kimse zarar görmüyor; hedef: Cosimo'nun "çalıştırma" planı, kuruma/kibre); kaynak çerçevesi "Vasari yüz yıl sonra".
4. **Palla Strozzi'nin şahini (1423, c4):** Medici'nin sonradan sürgün ettiği zenginin sanat siparişi; soyadı oyunu (◐, bd21).
5. **Poliziano'nun *Commentarium*'u (1478, c7):** ağır sahne öncesi **kaynak uyarısı**: Pazzi'nin ilk anlatımı Medici çevresinden ve propaganda niteliğinde (◐, bd34). Pazzi anlatımında tarafları ayrı söyleme kuralıyla birlikte.

---

## 7. Hâlâ eksik kalanlar

### 7.1 Sınırlar

- **WebFetch yok, ● yok.** En değerli birincil/ikincil metinlerin URL'leri aramada döndü ve bir sonraki turda WebFetch çalışırsa doğrudan açılabilir: Vettori mektubu (`dhspriory.org`, `ianchadwick.com`), *Prens* ithafı (`standardebooks.org`), Condivi/Holroyd (`gutenberg.org/cache/epub/19332`), Symonds (`…/11242`), Cellini (`…/4028`), Vasari-Lippi (`sourcebooks.fordham.edu/basis/vasari/vasari9.asp`), Met Cristofori denemesi, Galileo mektupları (`it.wikisource.org/wiki/Lettere_(Galileo)/I`).
- 2 sorgu `allowed_domains` hatasıyla (eurogamer, ign, polygon) boşa gitti.

### 7.2 Başlık başlık

- **(1) Bilim ve müzik:** *Sidereus Nuncius*'un ithaf metni (Van Helden çevirisi); Vinta mektuplarının metni; Galileo'nun 7 Mayıs 1610 mektubundaki unvan isteği (`it.wikisource` sayfası sonuçta var ama okunmadı); **maaş ve atama tarihi çelişkili**; "1605–08 yazları" doğrulanmadı. *Euridice*: Peri'nin önsözü, izleyici/mekân, final; **Camerata "efsanesi"nin akademik tartışması** (Palisca'nın kendi argümanı) görülmedi. Cristofori: Maffei'nin makalesinin kendisi (Ottoboni), envanterin İtalyanca metni, "iki klavye/dört oktav" ayrıntısı.
- **(2) Michelangelo:** Condivi/Vasari'nin 1529–30 anlatımı; "6 Nisan 1529" günü; Kasım 1529 dönüşü; Ferrara durağı; Strozzi dörtlüğü ve yanıtın **tam metni**; Vasari'ye 1555 mektubu ("rüya"); Laurenziana'nın sipariş belgeleri.
- **(3) Machiavelli:** *Prens* ithafının **yılı** (1516?) ve Giuliano'nun ölümü (Mar 1516: HAFIZA); 1559 Dizin; *Discursus*, *Mandragola*; 1527 sonrası Cumhuriyet'in dışlaması; av köpekleri anekdotunun **kaynağı**; strappado "altı çekiş" ayrıntısı; *Istorie*'nin sunum yeri ve günü.
- **(4) Popüler kültür:** Ubisoft'un **resmî** açıklamaları, danışman tarihçilerin adları, "çok kültürlü ekip" uyarı cümlesi, *Bonfire of the Vanities* DLC'si; dizinin yapım künyesi (Rai/Lux Vide, sezon tarihleri); **"Medici etkisi" için tarihçi değerlendirmesi**; Johansson'un kendi cümleleri.
- **(5) Kurumlar:** Accademia'nın 1563 *Capitoli*'si ve öğretim içeriği; Pevsner'in zincir iddiası; **Paris–Roma–Londra bağının kanıtı** (özellikle Londra); 1676 birleşme; Patto'nun üçüncü öğesi ("yabancıların merakı") birincil metin; Boboli'nin 1766'da halka açılışı; Vasari Koridoru; Ashmolean 1683.
- **(6) Diğer patronlar:** Rucellai/Tornabuoni/Sassetti bu turda yeniden aranmadı (M3 ◐); Palla Strozzi'nin 1434 sürgünü bu turda görülmedi (M2 K15); Strozzi Şapeli (Santa Maria Novella, Filippino Lippi); Cosimo I'in Palazzo Strozzi müsaderesinin yılı; Pazzi Şapeli'nin tamamlanma tarihi ve mimarı; Medici'nin sipariş payına dair nicel veri (Goldthwaite).
- **(7) Hümanistler:** Poliziano'nun Lorenzo'nun oğullarına hocalığı; sakristide oluşuna bağımsız kanıt; Pico: Fiesole, 2007 arsenik çalışması; Bruni: Hans Baron'un tezi, Rossellino mezarı, Cosimo ile ilişkisi; Hankins 2002 makalesinin içeriği; Kristeller'in konumu.
- **(8) Anekdotlar:** Condivi'nin İtalyanca metni; Cellini'nin özgün metni; Anonimo Gaddiano'nun Leonardo pasajı; Pacioli'nin yumurta pasajı; Vasari'nin 1550 ve 1568 baskılarındaki farklar.

### 7.3 M3 §11.2'deki 18 sorgunun durumu

| M3 §11.2 | Durum | Bu turda |
|---|---|---|
| 1. *Sidereus Nuncius* ithaf (ext) | **Yapıldı** (Q1, Q3, Q50) | ◐; ithaf metni yok |
| 2. Galileo unvan/maaş | **Yapıldı** (Q2) | ◐ unvan, ○ maaş |
| 3. Peri *Euridice* | **Yapıldı** (Q5, Q55) | ◐ |
| 4. Cristofori | **Yapıldı** (Q6, Q7, Q51) | ◐; Ottoboni ○ |
| 5. Cimento | **Yapıldı** (Q29) | ◐ |
| 6. Michelangelo 1529 (ext) | **Yapıldı** (Q10, Q11, Q56) | ◐/○ |
| 7. Yeni Sakristi, Strozzi dörtlüğü | **Yapıldı** (Q9, Q12, Q13) | ◐; tam metin yok |
| 8. *AC II* (ext) | **Yapıldı** (Q21–Q25, Q52) | ○ (sapma haritası) |
| 9. Medici dizisi | **Yapıldı** (Q24) | ◐ |
| 10. Machiavelli | **Yapıldı** (Q15–Q20, Q56, Q57) | ◐ |
| 11. Vasari-Botticelli/Lippi | **Yarım:** Lippi yapıldı (Q53) | Botticelli yapılmadı |
| 12. Burckhardt/Kent/Welch | **Yarım** (Q59) | Kent yalnız öğrenci çalışması aktarımıyla (○) |
| 13. Lascaris 1492 | **Yapılmadı** | — |
| 14. *Ricordi* 663.755 florin | **Yapılmadı** | — |
| 15. Magi Şapeli / Gozzoli | **Yapılmadı** | — |
| 16. Boboli, Vasari Koridoru | **Yarım:** Boboli yapıldı (Q34) | Koridor yapılmadı |
| 17. Capitoline / Uffizi "ilk müze" | **Yapıldı** (Q32, Q35) | ◐; Ashmolean yok |
| 18. WebFetch ile birincil metinler | **Yapılamadı** (DNS) | — |

### 7.4 Sonraki tur için önerilen sorgular/kaynaklar (öncelik sırasıyla)

1. WebFetch/başka araç düzelirse: **Vettori mektubu**, ***Prens* ithafı**, **Condivi/Holroyd**, **Cellini**, **Vasari-Lippi**, **Met Cristofori denemesi**, **Galileo'nun 7 Mayıs 1610 mektubu** (→ ● için tek yol).
2. `Maffei 1711 "Nuova invenzione d'un gravecembalo col piano e forte" Giornale de' letterati d'Italia Ottoboni tre` (Ottoboni ve "üç piyano").
3. `Palmarini Sosnowski "Was it really Columbus' egg" Pacioli De viribus quantitatis Brunelleschi uovo` (revistas.ucm.es CFIT 60872): yumurtanın en eski kayıtları.
4. `Hankins "Invention of the Platonic Academy of Florence" 2002 Rinascimento`, `Kristeller Ficino Academy` (Platon Akademisi'nin güncel akademik konumu).
5. `Najemy Machiavelli Istorie fiorentine commission Studio 1520 Giulio` ve `Machiavelli Principe dedica Lorenzo 1516 Giuliano morte` (ithaf yılı).
6. `Pevsner Academies of Art Past and Present Florence Rome Paris London chain` ve `Accademia di San Luca 1676 Académie de France union Colbert` (zincirin ikinci ve üçüncü halkası).
7. `Biagioli Galileo Courtier Medicean Stars naming Vinta` (isimlendirme kararının yazarı).
8. `Ubisoft Assassin's Creed II historians consulted Animus database Pazzi` ve Kotaku Désilets röportajının tamamı.
9. `Uffizi Boboli 1766 apertura al pubblico`, `Vasari Corridor 1565 five months` (Uffizi resmî).
10. `Poliziano tutor Lorenzo's children Clarice dismissed 1479`, `Pico della Mirandola 2007 arsenic exhumation study` (yalnız ciddi bilimsel yayın bulunursa).

---

## Ek A. Kaynak anahtarı (S etiketleri)

> **Not:** Bunlar arama aracının döndürdüğü sayfalardır; **hiçbiri açılıp okunmadı** (özetler arama aracı tarafından üretildi). Bir konudaki S etiketi, o konu sorgularında dönen sayfaları ifade eder; hangi cümlenin hangi sayfadan geldiğini ayrıştıramadım. Kalite notları: blog/rehber/listicle/forum = düşük; Wikipedia, fan wiki = orta (özet düzeyi, türev zinciri); müze/üniversite/ansiklopedi/kurum sitesi = yüksek.

- **S1** (*Sidereus Nuncius*): https://en.wikipedia.org/wiki/Sidereus_Nuncius · https://calisphere.org/item/095f5e8a945aea90a6e5636b14f72790/ · https://catalogue.museogalileo.it/object/GalileoGalileiSidereusNunciusFacsimile.html · https://www.historytoday.com/archive/galileo-observes-satellites-jupiter · https://www.sites.hps.cam.ac.uk/starry/galileo.html · https://www.lindahall.org/about/news/scientist-of-the-day/galileo-galilei-2/ · https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5871402/ · https://www.chronicle.com/article/galileo-said-to-present-his-discoveries-to-favor-medicis/
- **S2** (Galileo unvan, maaş, Vinta): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5871402/ · https://media.fupress.com/files/pdf/16/3105/3105_11853 · https://www.unipd.it/en/galileo-anni-padovani · https://www.Britannica.Com/biography/Cosimo-II · https://www.palazzo-pitti.net/cosimo-ii-biography.html · https://brunelleschi.imss.fi.it/itineraries/biography/BelisarioVinta.html · https://brunelleschi.imss.fi.it/itineraries/gallery/ChiefMathematicianAndPhilosopherToTheGrandDukeOfTuscany_34491.html · https://www.academia.edu/111271101/Galileo_s_Secrets · https://it.wikisource.org/wiki/Lettere_(Galileo)/I · https://jimclifford.ca/britannica-articles-1/a/EB.4/144850376/39.html
- **S3** (*Cosmica*/*Medicea*): https://en.wikipedia.org/wiki/Galilean_moons · https://www.newworldencyclopedia.org/entry/Galilean_moons · https://catalogue.museogalileo.it/indepth/JupitersMoonsSatellites.html · https://www.sites.hps.cam.ac.uk/starry/galsidnun.html · https://epizodyspace.ru/bibl/inostr-yazyki/sky-and-teleskope/2020/5/Witkoski_Finding_Jupiter's_Moons_Sky_and_Telescope_139_no_05_(2020)-1.pdf
- **S4** (pusula kitabı, Cosimo'ya ders): https://www.museogalileo.it/en/museum/explore/meet-galileo/38-works/462-le-operazioni-del-compasso-geometrico-e-militare-1606.html · https://galileo.ou.edu/node/1791.html · https://maremagnum.com/en/libri-moderni/la-operazione-del-compasso-geometrico-et-militare-di-galileo-galilei-nobil-fiorentino-lettor-delle-matematiche-nello-studio-di-/164964996
- **S5** (Cimento): https://catalogue.museogalileo.it/indepth/Academies.html · https://catalogo.museogalileo.it/multimedia/AccademiaCimentoBis.html · https://catalogue.museogalileo.it/multimedia/SaggiNaturaliEsperienzeBis.html · https://www.treccani.it/enciclopedia/leopoldo-de-medici_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/la-rivoluzione-scientifica-luoghi-e-forme-della-conoscenza-le-accademie_(Storia-della-Scienza)/ · https://www2.museogalileo.it/it/biblioteca-e-istituto-di-ricerca/progetti/esposizioni-temporanee/296-scienziati-a-corte-l-arte-della-sperimentazione-nell-accademia-galileiana-del-cimento-1657-1667-it.html
- **S6** (Galileo 1633 ve Medici): https://www.pbs.org/empires/medici/renaissance/galileo.html · https://brunelleschi.imss.fi.it/itineraries/itinerary/TheTrial.html · https://brunelleschi.imss.fi.it/itineraries/biography/FrancescoNiccolini.html · https://brunelleschi.imss.fi.it/pencil/eng/html/People/05%20Ferdinando2.htm · https://oajournals.fupress.net/index.php/cdg/article/download/8619/8617/8496
- **S7** (*Euridice*, *Dafne*, Caccini): https://en.wikipedia.org/wiki/Euridice_(Peri) · https://en.wikipedia.org/wiki/Jacopo_Peri · https://en.wikipedia.org/wiki/Italian_opera · https://en.wikipedia.org/wiki/Euridice_(Caccini) · https://en.wikipedia.org/wiki/Dafne · https://www.britannica.com/topic/LEuridice · https://www.britannica.com/biography/Jacopo-Peri · https://www.theflorentine.net/2007/01/25/renaissance-florentine-opera/ · https://operascribe.com/2018/12/26/102-euridice-jacopo-peri/
- **S8** (Marie'nin vekâlet düğünü): https://unofficialroyalty.com/marie-de-medici-queen-of-france · https://content.www.wellcomecollection.org/works/zkge44hj · https://melvillesprintcollection.org/exhibits/show/ch4/marie-medici-series/cat191 · https://www.theflorentine.net/2015/03/05/ephemeral-renaissance/ · https://roderickconwaymorris.com/Articles/76.html
- **S9** (Camerata): https://www.britannica.com/topic/Florentine-Camerata · https://www.britannica.com/biography/Giovanni-Bardi-conte-di-Vernio · https://www.britannica.com/art/monody · https://www.britannica.com/biography/Emilio-de-Cavalieri · https://en.wikipedia.org/wiki/Florentine_Camerata · https://www.abaa.org/book/800661473 · https://wikimili.com/en/Florentine_Camerata
- **S10** (Cristofori ve piyano): https://www.metmuseum.org/essays/the-piano-the-pianofortes-of-bartolomeo-cristofori-1655-1731 · https://www.metmuseum.org/toah/hd/cris/hd_cris.htm · https://www.metmuseum.org/art/collection/search/501788 · https://www.metmuseum.org/perspectives/national-piano-month-3 · https://resources.metmuseum.org/resources/metpublications/pdf/En_Route_to_the_Piano_A_Converted_Virginal_The_Metropolitan_Museum_Journal_v_13_1978.pdf · https://www.cambridge.org/core/books/abs/history-of-stringed-keyboard-instruments/invention-of-the-piano/EF896FE4B4182F58C6C0375D072AC350 · https://en.wikipedia.org/wiki/Bartolomeo_Cristofori · https://www.britannica.com/print/article/143328 · https://www.ebsco.com/research-starters/history/invention-piano/ · https://www.palazzo-pitti.net/gran-principe-biography.html · https://collections.nmc.ca/people/365/bartolomeo-cristofori
- **S11** (Yeni Sakristi): https://www.britannica.com/topic/Medici-Chapel · https://www.britannica.com/topic/San-Lorenzo-church-Florence-Italy · https://smarthistory.org/new-sacristy/ · https://www.metmuseum.org/exhibitions/listings/2017/michelangelo/exhibition-galleries
- **S12** (Michelangelo 1529–30, gizli oda, San Niccolò): https://news.artnet.com/art-world/art-bites-michelangelo-hide-from-pope-2669396 · http://www.thehistoryblog.com/archives/25920 · https://www.thegeographicalcure.com/post/michelangelo-secret-drawings-florence · https://aleteia.org/2022/02/02/this-church-in-florence-has-a-secret-room-with-michelangelos-sketches/ · https://www.theflorentine.net/2023/10/31/michelangelos-secret-room-medici-chapels-museum/ · https://www.atlasobscura.com/places/michelangelos-hidden-drawings · https://en.wikipedia.org/wiki/Sagrestia_Nuova · https://fondazione.destinationflorence.it/en/df-mag/uncovering-michelangelos-secret-room/ · https://conoscifirenze.it/history/377-michelangelo-and-the-secret-room.html · https://www.arte.it/luogo/chiesa-di-san-niccolò-oltr-arno-1875 · https://www.facarospauls.com/apps/florence-art-and-culture/325/san-niccolo-oltarno · https://www.reidsguides.com/italy/destinations/tuscany/florence/sights/s-miniato-al-monte.html · https://news.artnet.com/art-world/art-bites-michelangelo-military-fortifications-2709244?amp=1
- **S13** (Strozzi dörtlüğü, *Gece*): https://www.ekphrastic.net/the-ekphrastic-review/two-epigrams-on-michelangelos-night-translated-and-answered-by-julie-steiner · https://uni-freiburg.de/kunstgeschichte/kwg-vortrag-vom-stein-zur-stimme-poetisierungen-von-michelangelos-skulpturen-in-der-europaeischen-lyrik/ · https://rivista-incontri.nl/article/download/8789/9408/13655 · https://it.wikisource.org/wiki/Rime_(Michelangelo) · https://storgy.com/poems/from-the-italian-of-giovanni-strozzi-algernon-charles-swinburne/ · https://franco.wiki/fr/La_Nuit_(Michel-Ange).html
- **S14** (Laurenziana): https://en.wikipedia.org/wiki/Laurentian_Library · https://www.studiomatrx.org/architecture-canon/laurentian-library · https://www.thegeographicalcure.com/post/guide-to-the-laurentian-library · https://buffaloah.com/a/virtual/italy/flor/lorenzo/lib.html · https://www.cambridge.org/core/journals/architectural-history/article/abs/michelangelos-laurentian-library-drawings-and-design-process/9CF8C0223BC94B01D64C6995DA3C9D0D · https://www.palazzo-pitti.net/bartolomeo-ammannati.html
- **S15** (Vettori mektubu, 10 Ara 1513): https://iep.utm.edu/machiave/ · http://dt.pepperdine.edu/courses/greatbooks_ii/gbii20/Machiavelli's%20letter%20to%20Francesco%20Vettori%20of%2010%20December%201513.pdf · https://courses.washington.edu/hsteu401/Letter%20%20to%20Vettori.pdf · https://qcurtius.com/2017/01/03/a-retreat-can-spur-creative-energy-machiavellis-letter-to-francesco-vettori/ · https://ianchadwick.com/machiavelli/miscellanea/letter-to-francesco-vettori/ · https://dhspriory.org/kenny/PhilTexts/Machiavelli/Letter%20to%20Vettori.htm (WebFetch: ENOTFOUND) · https://spartacus-educational.com/Quotations_Machiavelli.htm · https://harpers.org/2008/05/machiavelli-on-communing-with-greatness · https://www.soa.org/news-and-publications/newsletters/innovators-and-entrepreneurs/2017/may/ei-2017-iss58/timeless-thinking-machiavellis-letter-to-francesco-vettori/ · https://www.theflorentine.net/2013/12/12/out-of-exile/ · https://en.wikipedia.org/wiki/Francesco_Vettori
- **S16** (Machiavelli 1513 tutuklama): https://itatti.harvard.edu/news/banishment-and-arrest-niccol%C3%B2-machiavelli · https://www.executedtoday.com/?p=24150 · https://www.florencewithguide.com/?p=5233
- **S17** (*Istorie fiorentine*): https://military-history.fandom.com/wiki/Florentine_Histories · https://www.cambridge.org/core/product/identifier/CBO9780511780691A012/type/BOOK_PART
- **S18** (*Prens* basımı): https://catalog.folger.edu/record/75484 · https://www.sothebys.com/en/buy/auction/2021/antiquarian-books-and-manuscripts/machiavelli-il-principe-florence-1532-later-danish · https://ilovetypography.com/2019/06/16/machiavelli-typographic-prince/ · https://www.britannica.com/print/article/476608 · https://it.wikisource.org/wiki/Opera:Il_Principe
- **S19** (*Prens* ithafı): https://www.marxists.org/reference/archive/machiavelli/works/prince · https://standardebooks.org/ebooks/niccolo-machiavelli/the-prince/w-k-marriott/text/dedication · https://pressbooks.library.torontomu.ca/theprince/chapter/dedication/ · https://www.universalfreemasonry.org/en/library/the-prince/dedication
- **S20** (av köpekleri anekdotu): https://laciviltacattolica.it/articolo/il-principe-di-machiavelli
- **S21** (1526 surlar, Machiavelli; Michelangelo unvanı): https://www.latoscanadileonardo.it/en/itineraries/florentine-area/masters-companions-friends-and-disciples/machiavelli-niccolo.html · https://core-prod.cambridgecore.org/core/books/american-machiavelli/from-fortune-into-providence/661F94544F4931B85C688C3CE23B07E6 · https://www.timetoast.com/timelines/niccolo-machiavelli--2 · https://www.openculture.com/2025/09/michelangelo-fort-designs.html · https://casabuonarroti.it/?p=2894
- **S22** (*AC II* doğruluk): https://www.thegamer.com/assassins-creed-historical-accuracy-failures/ · https://en.wikipedia.org/wiki/Francesco_Salviati_(bishop) · https://en.wikipedia.org/wiki/Girolamo_Riario · https://en.wikipedia.org/wiki/Giuliano_de%27_Medici · https://gamefaqs.gamespot.com/boards/956858-assassins-creed-ii/54752225
- **S23** (*AC II* basın ve geliştirici): https://www.pcgamer.com/revisiting-the-renaissance-with-assassins-creed-2/ · https://kotaku.com/a-fan-is-fact-checking-the-assassins-creed-games-1828909197 · https://kotaku.com/assassins-creed-ii-spoiler-talk-with-patrice-desilets-5432096 · https://www.gamesradar.com/assassins-creed-ii-hands-on/2/ · https://www.pcgamer.com/games/assassins-creed/the-5-most-historically-inaccurate-moments-in-the-assassins-creed-series/ · https://www.gamespot.com/articles/assassins-creed-2-first-impressions/1100-6210843/ · https://gamefaqs.gamespot.com/boards/956858-assassins-creed-ii/54370400
- **S24** (*AC II* künye ve olay örgüsü): https://en.wikipedia.org/wiki/Ezio_Auditore_da_Firenze · https://assassinscreed.fandom.com/wiki/Pazzi_conspiracy · https://assassinscreed.fandom.com/wiki/Assassin's_Creed_II · https://assassinscreed.fandom.com/wiki/Rodrigo_Borgia
- **S25** (*Medici: Masters of Florence*): https://www.theflorentine.net/2017/01/06/masters-florence-gets-wrong/ · https://www.theflorentine.net/2019/03/07/medici-masters-florence-season-2-fact-fiction/ · https://varsity.co.uk/reviews/11703 · https://televisionheaven.co.uk/reviews/medici-masters-of-florence · https://vodzilla.co/?p=39125
- **S26** (*The Medici Effect*): https://en.wikipedia.org/wiki/The_Medici_Effect · https://en.wikipedia.org/wiki/Frans_Johansson · https://ubiquity.acm.org/article.cfm?id=1041060 · https://store.hbr.org/product/the-medici-effect-with-a-new-preface-and-discussion-guide-what-elephants-and-epidemics-can-teach-us-about-innovation/10129 · https://www.librarything.com/work/226262
- **S27** (Padgett–Ansell): https://acawiki.org/Robust_action_and_the_rise_of_the_Medici,_1400-1434 · https://data.gesis.org/gesiskg/resource/gesis-bib-32311
- **S28** ("Medici Rönesans'ı yarattı mı" popüler/öğrenci düzeyi): https://commons.emich.edu/cgi/viewcontent.cgi?article=1102&context=honors · https://historum.com/t/why-were-the-medicis-so-important-to-the-renaissance-in-italy.38408/ · https://www.atlantis-press.com/article/125984501.pdf · https://belleten.gov.tr/tam-metin/3645/eng · https://courses.lumenlearning.com/suny-fmcc-worldhistory/chapter/art-and-patronage/
- **S29** (akademi zinciri): https://en.wikipedia.org/wiki/Accademia_di_San_Luca · https://www.treccani.it/enciclopedia/federico-zuccari_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/federico-zuccari/ · https://www.accademiasanluca.eu/it/accademia/storia · https://www.britannica.com/art/academy-of-art · https://www.britannica.com/place/Accademia-di-San-Luca · https://www.treccani.it/enciclopedia/il-paragone-fra-le-arti_(Storia-della-civilt%C3%A0-europea-a-cura-di-Umberto-Eco)/ · https://www.treccani.it/enciclopedia/potere-e-declino-delle-accademie_(Storia-della-civilt%C3%A0-europea-a-cura-di-Umberto-Eco)/ · https://www.dailyartmagazine.com/famous-art-academies/ · https://www.theartstory.org/definition/the-academy-of-art/ · https://en.wikipedia.org/wiki/Accademia_di_Belle_Arti_di_Roma · https://www.accademiasanluca.eu/it/news/id/3246/colloquio-internazionale-strong-br-storie-e-controstorie-delle-accademie-del-disegno-tra-firenze-bologna-roma-strong-
- **S30** (Uffizi'nin kamusallaşması): https://www.uffizi.it/en/pages/about-us · https://www.uffizi.it/en/artworks/i-corridoi-di-galleria · https://www.uffizi.it/en/magazine-imagines/imagines-1-english · https://www.britannica.com/topic/Uffizi-Gallery · https://brunelleschi.imss.fi.it/pencil/eng/html/Space/09%20Uffizi.htm
- **S31** (Boboli): https://www.uffizi.it/en/boboli-garden/history · https://www.uffizi.it/en/artworks/grotta-del-buontalenti · https://www.britannica.com/place/Boboli-Gardens · https://www.britannica.com/biography/Tribolo
- **S32** (Capitoline): https://en.wikipedia.org/wiki/Capitoline_Museums · https://www.historyofinformation.com/detail.php?id=4351 · https://theviewfromadrawbridge.com/2026/01/29/romes-capitoline-museums-the-oldest-public-museums-in-the-world/
- **S33** (Gentile da Fabriano, Palla Strozzi): https://en.wikipedia.org/wiki/Adoration_of_the_Magi_(Gentile_da_Fabriano) · https://uen.pressbooks.pub/arth2720/?p=397 · https://www.christiancentury.org/artsculture/on-art/adoration-magi-gentile-da-fabriano-ca-1423 · https://quattrocentoitalia.artinterp.org/omeka/items/show/78
- **S34** (Pazzi Şapeli): https://en.wikipedia.org/wiki/Pazzi_Chapel · https://en.wikipedia.org/wiki/Santa_Croce,_Florence · https://smarthistory.org/?p=4211 · https://blog.fua.it/?p=694
- **S35** (Palazzo Strozzi): https://en.wikipedia.org/wiki/Palazzo_Strozzi · https://www.palazzostrozzi.org/en/history-palazzo-strozzi/ · https://www.palazzostrozzi.org/en/a-great-house-palazzo-strozzi/ · https://www.britannica.com/place/Palazzo-Strozzi · https://www.britannica.com/biography/Filippo-Strozzi · https://www.britannica.com/biography/Il-Cronaca · https://en.wikipedia.org/wiki/Benedetto_da_Majano
- **S36** (Pico): https://www.catholic.org/encyclopedia/view.php?id=8022 · https://www.encyclopedia.com/humanities/encyclopedias-almanacs-transcripts-and-maps/pico-della-mirandola-count-giovanni-1463-1494 · https://plato.stanford.edu/Entries/pico-della-mirandola/ · https://unibo.it/en/university/who-we-are/our-history/famous-people-and-students/giovanni-pico-della-mirandola-1
- **S37** (Poliziano, *Commentarium*): https://books.fupress.com/catalogue/coniurationis-commentarium--commentario-della-congiura-dei-pazzi/2298 · https://sourcelibrary.org/book/pactianae-conjurationis-commentarium-poliziano · https://warwick.ac.uk/fac/arts/ren/ugstudy/2019-20/term2/wk9-political_and_social_upheavals-celati.docx · https://www.erudit.org/en/journals/renref/2016-v39-n2-renref06782/1086569ar.pdf
- **S38** (Bruni): https://en.wikipedia.org/wiki/Leonardo_Bruni · https://www.proquest.com/docview/203375470 · https://catholic.com/encyclopedia/leonardo-bruni
- **S39** (Ficino ve "Akademi"): https://plato.stanford.edu/entries/ficino/ · https://iep.utm.edu/ficino/
- **S40** (Faun; Condivi; Michelangelo'nun hane içi koşulları): https://www.finestresullarte.info/en/works-and-artists/michelangelo-s-early-masterpieces-the-madonna-della-scala-and-the-battle-of-the-centaurs · https://www.gutenberg.org/cache/epub/19332/pg19332-images.html · https://www.gutenberg.org/files/19332/19332-h/19332-h.html · https://www.gutenberg.org/cache/epub/11242/pg11242-images.html · https://www.gutenberg.org/cache/epub/32362/pg32362-images.html · https://dev.bookbrowse.com/excerpts/index.cfm/book_number/3095/page_number/10/michelangelo · https://www.galleriabazzanti.it/en/?p=15431 · https://en.wikisource.org/wiki/The_Life_of_Michael_Angelo/Strength
- **S41** (Torrigiani; Cellini): https://en.wikisource.org/wiki/Torrigiano,_Pietro_(DNB00) · https://www.gutenberg.org/cache/epub/4028/pg4028-images.html · https://ia801308.us.archive.org/13/items/autobiographyofb04028gut/7clln10h.htm · https://www.gutenberg.org/cache/epub/11242/pg11242-images.html · https://www.gutenberg.org/files/39380/39380-h/39380-h.htm
- **S42** (Leonardo, lir, Anonimo Gaddiano): https://en.wikipedia.org/wiki/Anonimo_Gaddiano · https://erenow.org/biographies/leonardo-da-vinci-the-flights-of-the-mind/26.php · https://discoveringdavinci.com/notebooks/biography/03-florentine-independence-and-the-first-silent-career.html · https://re.public.polimi.it/handle/11311/1058770
- **S43** (yumurta): https://en.wikipedia.org/wiki/Egg_of_Columbus · https://thecritic.co.uk/brunelleschis-egg/ · https://revistas.ucm.es/index.php/CFIT/en/article/view/60872 · https://go.gale.com/ps/i.do?id=GALE%7CA615692090&issn=19882394&it=r&linkaccess=abs&p=IFME&sid=googleScholar&sw=w&userGroupName=anon%7Eaa74557c&v=2.1 · https://grokipedia.com/page/Egg_of_Columbus · https://en.wikipedia.org/wiki/Luca_Pacioli · https://www.origamiheaven.com/historydeviribusquantitatis.htm
- **S44** (Vasari, Lippi): https://sourcebooks.fordham.edu/basis/vasari/vasari9.asp · https://en.wikisource.org/wiki/Lives_of_the_Most_Excellent_Painters,_Sculptors,_and_Architects/Fra_Filippo_Lippi · https://www.gutenberg.org/ebooks/41887.html.images · https://en.wikisource.org/wiki/Catholic_Encyclopedia_(1913)/Filippo_Lippi

---

## Ek B. Sorgu günlüğü (60 sorgu hakkı)

`std` = standard, `ext` = extended. "Sonuç": ✔ işe yaradı · ◐ kısmen · ✘ boşa.

| Q | Mod | `allowed_domains` | Konu | Sonuç |
|---|---|---|---|---|
| 1 | ext | — | *Sidereus Nuncius*, Medicea Sidera | ✔ |
| 2 | std | — | Galileo 1610 unvan, maaş, Vinta | ✔ (maaş tek makale) |
| 3 | std | — | *Cosmica*/*Medicea* adlandırma | ✔ |
| 4 | std | galileo.rice.edu | Cosimo II'nin hocası | ◐ (PMC ve ana sayfa) |
| 5 | std | — | Peri *Euridice*, *Dafne* | ✔ |
| 6 | std | — | Cristofori 1700 envanter, Maffei | ✔ |
| 7 | std | metmuseum.org | Met Cristofori denemesi | ✔ |
| 8 | std | britannica.com | Camerata | ✔ |
| 9 | std | britannica, smarthistory, metmuseum | Yeni Sakristi | ✔ |
| 10 | ext | — | Michelangelo 1529, gizli oda | ✔ |
| 11 | std | — | San Niccolò kulesi, Condivi/Vasari | ◐ (Condivi/Vasari metni yok) |
| 12 | std | — | Strozzi dörtlüğü | ✔ |
| 13 | std | — | "Caro m'è 'l sonno" metni | ◐ (metin yok) |
| 14 | std | — | Laurenziana merdiveni, 1555 mektubu | ◐ (mektup yok) |
| 15 | ext | — | Vettori mektubu, ithaf | ✔ |
| 16 | std | — | Machiavelli 1513 işkence/af | ✔ |
| 17 | std | — | Vettori mektubu alıntıları | ✔ |
| 18 | std | — | *Istorie fiorentine* siparişi | ✔ |
| 19 | std | — | *Prens* 1532 basımı | ✔ |
| 20 | std | — | *Prens* ithaf mektubu | ✔ |
| 21 | ext | — | *AC II* tarihsel doğruluk | ◐ (geliştirici yok) |
| 22 | std | gamedeveloper, gamasutra, ign, eurogamer, pcgamer, gamespot | *AC II* geliştirici | ✘ (400: ign, eurogamer) |
| 23 | std | gamedeveloper, pcgamer, gamespot, gamesradar, polygon, kotaku | *AC II* geliştirici | ✘ (400: polygon) |
| 24 | std | — | *Medici* dizisi doğruluk | ✔ |
| 25 | std | gamedeveloper, pcgamer, gamespot, gamesradar, kotaku | *AC II* geliştirici | ✔ (Kotaku, GamesRadar, PC Gamer) |
| 26 | std | — | *The Medici Effect* | ✔ (tarihçi yok) |
| 27 | std | dokumen.pub, wikipedia, hbr.org, hbsp.harvard.edu | *Medici Effect* giriş | ◐ |
| 28 | std | — | Padgett–Ansell | ✔ |
| 29 | std | britannica, museogalileo ×2, treccani | Cimento | ✔ |
| 30 | std | — | Galileo 1633 ve Medici | ✔ |
| 31 | ext | — | Akademi zinciri | ◐ |
| 32 | std | uffizi.it, britannica, imss | Uffizi kamusallaşma | ✔ |
| 33 | std | treccani, accademiasanluca.eu, britannica | San Luca, Zuccari | ✔ |
| 34 | std | uffizi.it, britannica, unesco ×2 | Boboli | ◐ (1766 yok) |
| 35 | std | — | Capitoline 1471/1734 | ✔ |
| 36 | std | — | Palla Strozzi, Gentile | ◐ (yalnız tablo) |
| 37 | std | — | Pazzi Şapeli | ✔ |
| 38 | std | britannica, wikipedia, palazzostrozzi.org | Palazzo Strozzi | ✔ |
| 39 | std | — | Pico | ✔ |
| 40 | std | — | Poliziano, Pazzi *Commentarium* | ✔ |
| 41 | std | — | Bruni | ◐ |
| 42 | ext | plato.stanford, britannica, iep, scholar/dash.harvard | Platon Akademisi | ✔ |
| 43 | std | — | Condivi, Faun | ✔ |
| 44 | std | gutenberg ×4 | Condivi diş şakası | ✔ |
| 45 | std | gutenberg, wikisource ×2, archive.org | Cellini–Torrigiani | ✔ |
| 46 | std | — | Anonimo Gaddiano, lir | ◐ |
| 47 | std | — | Yumurta, Vasari baskıları | ◐ |
| 48 | ext | — | Pacioli, Filicaia, yumurta | ◐ |
| 49 | std | — | Marie'nin vekâlet düğünü | ✔ (*Euridice* anılmıyor) |
| 50 | std | — | Galileo 7 Mayıs 1610 mektubu | ◐ (mektup metni yok) |
| 51 | std | — | Cristofori'nin işe alınışı | ✔ |
| 52 | std | wikipedia, ubisoft.com, fandom | *AC II* künye | ✔ |
| 53 | std | gutenberg, wikisource ×2, fordham | Vasari–Lippi | ✔ |
| 54 | std | gutenberg, wikisource ×2, archive.org | Condivi 5 dukat | ✔ |
| 55 | std | wikipedia, britannica, theflorentine, operascribe, metmuseum | *Euridice* ayrıntı | ✔ |
| 56 | std | — | Machiavelli 1526 surlar | ✔ |
| 57 | std | — | *Prens* av köpekleri | ◐ (tek popüler makale) |
| 58 | std | — | Galileo'nun Cosimo'ya dersi | ✔ |
| 59 | ext | — | "Medici Rönesans'ı yarattı mı" tarihçi tartışması | ◐ (akademik kaynak yok) |
| 60 | std | — | Palisca, Camerata | ✔ |

*Dosya sonu. Hazırlayan: M3b. Git commit/push yapılmadı (ana ajan yapacak).*
