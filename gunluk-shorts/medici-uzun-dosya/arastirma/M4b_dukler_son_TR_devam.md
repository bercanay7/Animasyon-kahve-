# M4b — M4'ün devamı: Cosimo I'den son Medici'ye zincir, iki kraliçe, Patto, dönem TR-BAĞ'ı

**Bölümler:** c0, c11 (kapanış), c12, c13, c15, c16 · **Hazırlayan:** M4b devam ajanı · **Tarih:** 18 Ekim 2026 · **Durum:** M4'ün sekiz maddelik devam paketi **büyük ölçüde sınandı** (60 sorgu); **yine hiçbir satıra ● verilmedi** (tek WebFetch denemesi DNS hatası verdi, hiçbir sayfa açılıp okunmadı).

> Bu dosya senaryo değildir; M4 ile birlikte okunur. `#` = M4 satırı, `b…` = bu dosyanın yeni satırı. Tırnak içindeki her İtalyanca/İngilizce parça **arama özetinde tırnak içinde görünen biçimdir**; çeviri bize aittir; sayfa açılıp doğrulanmamıştır. Sınıf en çok ◐'dir ve ◐ burada "arama özeti dahil ≥2 bağımsız ikincil kaynakta uyumlu" demektir (aynı ansiklopedinin iki girişi, yazarları farklıysa iki kaynak sayıldı; Wikipedia aynaları tek kaynak sayıldı).

---

## 1. Başlık notu

### 1.1 Araçlar ne yaptı?

| Araç | Sonuç |
|---|---|
| **WebSearch** | **60 sorgu** (12 `extended`, 48 `standard`); bütçeye (≤60) tam uyuldu; ret/hata yok. |
| **WebFetch** | **1 deneme** (`treccani.it`, Anna Maria Luisa DBI maddesi): `getaddrinfo ENOTFOUND www.treccani.it`. Talimata uyularak **tekrarlanmadı**. ● imkânsız. |
| **Bash** | Yalnız yerel iş: klasör, parça birleştirme, sınıf sayımı. Web'e Bash'ten çıkılmadı. |

**`allowed_domains` karnesi:**
- `treccani.it` (3 sorgu): **çok verimli.** DBI/Enciclopedia Italiana/Dizionario di Storia girişlerinden tırnaklı İtalyanca pasajlar özetlere düştü (Cosimo I'in seçilişi, Gian Gastone'nin "ruspanti"leri, 1932 değerlendirmesi). Sayfa açılamadığı için yine ◐.
- `storiadifirenze.org` + `cultura.comune.fi.it` + `italianostra.org` + `uffizi.it` (2 sorgu): **verimli.** Patto: 13 madde, Fransızca özgün, Casciu'nun makalesi, Comune/Uffizi'nin lafız sürümü.
- `cambridge.org, jstor.org, tandfonline.com, oup.com, historytoday.com, britannica.com` (1 sorgu): **kısmen.** Knecht (History Today, EHR incelemesi), Jouanna (French History), Britannica geldi; Holt/Frieda/Crouzet gelmedi.
- Kısıtsız sorgular: en iyi bulguların bir kısmı buradan geldi (Italian Art Society/Eleonora, Yale UP alıntısı/Lorenzino 1548, Mercan çalışmaları/TR-BAĞ, Uffizi/Garzia).
- `dokumen.pub`, `wikisource.org`, `theflorentine.net`, `museodeimedici.it` ile **hedefli sorgu yapılmadı** (bütçe).

### 1.2 Sınıf dağılımı (otomatik sayım, satırın ilk sınıfına göre)

Yeni kronoloji **84 satır (b1–b84)**: ◐ 61 · ○ 23 (19 satır karma sınıflı, örn. "◐ olgu / ○ gün"). Canlı ayrıntı **31 satır**: ◐ 21 · ○ 10. Mit/tartışma **17 girdi** (bM1–bM17): ◐ 9 · ○ 7 · — 1. TR-BAĞ **15 satır (T14–T28)**: ◐ 8 · ○ 6 · — 1. Sınıf sayımı satırın **ilk** sınıfına göredir; ● hiç yoktur. HAFIZA satırı yeni kronolojide yoktur (M4'ten kalanlar §2'deki güncelleme tablosunda ve §7'de anılır).

### 1.3 Okuma uyarısı

Arama özetleri bir modelin birden çok sayfadan yaptığı derlemedir; **iç çelişkiler** gördüm (örn. aynı özetin bir yerinde "Wikipedia" dediği şeyin başka yerde farklı gün vermesi). Çelişkili günler tabloda **olduğu gibi** bırakıldı. Kritik her tarih/sayı için `kaynaklar.md` aşamasında sayfa açılarak teyit gerekir. Bu dosyadaki **HAFIZA** satırları yalnız "M4'ten kalan ve bu turda sınanamayan" olarak anılır; yeni HAFIZA satırı eklenmemiştir (yalnız birkaç açık işaretli çıkarım).

### 1.4 Yeni DÜZELTME / NOT kutusu (M4 §1.4'ün devamı; D9'dan başlar)

1. **DÜZELTME D9 — Eleonora ile evlilik "29 Haziran" değil.** M4 #52 "29 Haziran 1539" demişti. Dört ayrı tarih var (◐, Italian Art Society/S. Reiss, palazzo-pitti.net, Wikipedia): **29 Mart 1539** Napoli'de sözleşme ve **vekâleten evlilik**; **22 Haziran** Livorno'ya varış; **29 Haziran** Cosimo ve Eleonora'nın **ayrı ayrı Floransa'ya girişleri**; **29 Temmuz 1539** resmî düğün. Senaryo "Haziran sonunda geldi, Temmuz sonunda evlendiler" diyebilir. (b10–b12)
2. **DÜZELTME D10 — Patto "üç madde" değil, 13 madde; özgünü Fransızca.** Casciu (Storia di Firenze) ve aynı ifadeyi yineleyen ikinci bir sayfa (muhtemelen Floransa Belediyesi'nin kültür sitesi; özetten kesinleşmedi): **13 madde**, özgün metin **Fransızca**, sonra İtalyancaya çevrilip onaylanmış. Ünlü olan **3. madde**dir. Italia Nostra afişinin başlığı: "Convenzione di Famiglia (Vienna 1737) – Articolo III – Traduzione in italiano dell'originale in francese". Yani sık alıntılanan İtalyanca cümle **bir çeviridir**. "Vienna" ibaresinin anlamı bilinmiyor (b73). Görevdeki "üç madde" büyük olasılıkla "3. madde"nin yanlış okunuşudur (**YORUM**).
3. **DÜZELTME D6'ya ek — İtalyanca lafız.** M4'ün tahmin ettiği "per" edatları **doğrulandı** (sorgu özetleri; sonuçlar arasında La Nazione, arte.it, finestresullarte vardı, hangisinin hangi varyantı taşıdığı özetten kesinleşmedi): *"per ornamento dello Stato, per utilità del Pubblico e per attirare la curiosità dei Forestieri"*. Floransa Belediyesi/Uffizi sürümü araya "e" koyar (*"…dello Stato, e per utilità del Pubblico, e per attirare…"*). Kullanıcı notundaki biçim bu cümlenin "per"siz kısaltmasıdır. Lafız ◐ (çeviri olarak), Fransızca özgün **görülmedi**. (b74, bD23)
4. **NOT D11 — Patto "bağış" mı?** Comune/Uffizi dili "Medici mallarının devlete devri" der; bir akademik özet (storiadifirenze.org, yazarı Casciu/Verga/Menicucci'den hangisi olduğu özetten çıkarılamadı) 3. maddenin koleksiyonu Floransa'ya **bağışlamadığını**, Francis Stephen ve ardıllarına geçişin **koşulu olarak devredilemezlik** koyduğunu söyler. USLUP §5-A örneği ("Floransa'da kalacak") doğru; "bağışladı/miras bıraktı" dilinden kaçınılmalı (○). (b75, bM13)
5. **DÜZELTME D12 — Ferdinando I'in ölüm günü.** M4 #95 "7 Şubat 1609" demişti; arama özeti hükümdarlığı "19 Ekim 1587 – **17 Şubat 1609**" verir (○, tek özet). Doğrulanmalı. (b51)
6. **NOT D13 — Marie ve "Rubens'in evi".** Bazı özetler "Rubens'in ödünç verdiği ev" der. Rubens 1640'ta ölmüştür (HAFIZA; yaygın bilinen bir olgu, bu turda aranmadı), Marie 1642'de. Wikipedia özeti: ev, **Rubens ailesinin 50+ yıl önce oturduğu** evdir (Sternengasse 10). M4'ün "Rubens ailesinin eski evi" ifadesi doğru; "Rubens'in kendi evinde öldü" denmemeli. (b48)
7. **NOT D14 — Cosimo 1537'de "dük" değildi.** Treccani DBI: **10 Ocak 1537**'de Senato, seçim koşullarını resmîleştirerek Cosimo'nun **dük unvanı taşımamasına**, yalnız *"capo e primario della città"* denmesine karar verdi. Dük unvanını Eylül 1537'de, Karl V'in onayıyla almaya başladığı yazılır (○). "17 yaşında dük oldu" demek yanlış olur; "kentin başı" demek doğru. (b5, b7)
8. **NOT D15 — Ottajano kolu.** M4 §5.22 doğru yöndeydi; ama "kol söndü" demek için dayanak **yok**: Wikipedia, Ottajano Prensleri'ni 19. yy'a dek sıralar ve kolu "sürmekte olan iki Medici kolundan biri" sayar (○). Bir soy ağacı kataloğu, bu kolun **1737'de Büyük Dukalık talebinde bulunduğunu (başarısız)** söyler (○). "Medici'nin son üyesi" ifadesi yalnız **Toskana'yı yöneten hat** için doğrudur. (b84)
9. **NOT D16 — 2026 DNA çalışmasındaki "Giovanni".** Arama özetleri "iki kardeş" der ve çalışmayı Francesco I (ö. 1587) ile kardeşi Giovanni'ye bağlar; **Giovanni = Kardinal Giovanni (ö. 20 Kasım 1562)** olması olası (○; bu bizim çıkarımımız, makale açılmadı). 1562 ölümleriyle 1587 ölümü aynı "sıtma" hikâyesinde buluşur.
10. **NOT D17 — Alessandro'nun annesi "köle" mi?** Simonetta da Collevecchio belgelerde Alfonsina Orsini'nin **hizmetçisi**dir; köylü kökenli, serbest hizmetçi; Afrika kökenine kanıt yok. "Moorish slave" hikâyesi Fransız yazar Jean Nestor'un 1560 tarihli kitabına gider; Giorgio Spini bu söylentiyi temelsiz bulmuştur (Wikipedia özeti, ○). DNA çalışması yine bulunamadı (D8 sürer). (bM4)
11. **NOT D18 — Rubens döngüsü: "24 tablo = 21 sahne + 3 portre".** Louvre/Pinakothek/Morgan Library özetleriyle ◐. (b43)
12. **NOT D19 — "Uçan mum"?** Görev metnindeki "zehir/uçan mum" ifadesi anlaşılamadı. En yakın tarihî karşılık **"escadron volant"** ("uçan filo": Catherine'in nedimeleri). Terim ilk kez **1695**'te anonim *Les amours de Henri IV*'de görülür; Una McIlvenna'nın çalışması bunu büyük ölçüde **mit** sayar (◐; bM9). Başka bir şey kastediliyorsa (örn. "zehirli mum") bu turda ayrıca aranmadı.
13. **NOT D20 — Marie'nin doğum yılı.** Çoğu kaynak 1575, Britannica 1573 (b39). Gün (26 Nisan) HAFIZA'da kalır.

### 1.5 Hızlı kullanım (senaryocu için)

- **En sağlam malzeme (◐):** Patto'nun künyesi (31 Ekim 1737; 13 madde; Fransızca özgün; Craon; 3. madde ve gerekçe cümlesi); 1562 sonbaharı (Giovanni 20 Kasım, Eleonora 17 Aralık, Uffizi'nin "sıtma" dili, 1857 incelemesi); Eleonora'nın yolculuğu (11–29 Haziran) ve 29 Temmuz düğünü; 9–10 Ocak 1537'de Senato'nun "capo e primario" şartı; Lepanto'da **12** Toskana kadırgası; Livornina'nın iki tarihi (1591, 1593); Rubens'in 26 Şubat 1622 sözleşmesi ve 24 = 21+3; Marie'nin 3 Temmuz 1642'de Köln'de ölümü; Anna Maria Luisa'nın mezar açımı (2012/13: frengi izi yok); Treccani'nin Gian Gastone değerlendirmesi.
- **Kesin kipte kullanılmayacaklar:** "Cosimo oğlunu öldürdü" (mit; bM1); Charles IX'un "hepsini öldürün" sözü (ANEKDOT); parmak ısırma sahnesi (ANEKDOT); "Alessandro'nun annesi köle" (bM4); "Lorenzino'yu Cosimo öldürttü" (tartışmalı; bM3); Patto "bağıştır" (bM13); Bianchi'nin zehirciliği (bM9); Ferdinando I'in ölüm günü (○); Gianfigliazzi'nin 1578 İstanbul elçiliği (○); Bona/Sakız rakamları (○).
- **Mizah kapalı sahneler** (USLUP §2-6): Alessandro'nun öldürülmesi, 1562 ölümleri, Lorenzino'nun Venedik'te öldürülmesi, 24 Ağustos 1572, Marie'nin Köln'deki sonu, Anna Maria Luisa'nın ölüm odası, Bona. **Mizah adayları (kuruma/kibre):** Rubens'in "imge siyaseti" siparişi; *Balet comique*'in 5 saatlik gösterişi; imparatorun tanıması için ödenen 100.000 duka; Livornina'nın "Türkler, Moorlar, Ermeniler, Persler…" hitap listesi (yalnız bir müzayede betimine dayanıyor: ○, önce teyit); "yabancıların merakı" cümlesi ile Uffizi'nin ücretsiz giriş günü.

---

## 2. Güncelleme tablosu (M4 satırı → yeni sınıf)

> Biçim: **M4 satırı (#, bölüm) | eski sınıf | yeni sınıf | not**. "→ bN" ilgili yeni satır. Değişmeyen satırlar listelenmedi.

### 2.A Kronoloji (M4 §2)

| M4 satırı (#, bölüm) | Eski | Yeni | Not |
|---|---|---|---|
| #48 (c11) Alessandro öldürülür, 6 Ocak 1537 | HAFIZA | **◐** | Gece 5–6 Ocak; akış iskeleti ◐, saat akışı yok → b1–b4 |
| #49 (c11) Cosimo seçilir, 9 Ocak 1537 | HAFIZA | **◐** | 9 Ocak seçim; 10 Ocak Senato şartları; bir kaynak 8 Ocak → b5–b6; D14 |
| #50 (c12) Montemurlo, 1 Ağustos 1537 | HAFIZA | **◐** olgu / ○ gün | 31 Temmuz–2 Ağustos çelişir → b8 |
| #50 notu: Strozzi 1538'de hapiste ölür | HAFIZA | **◐** | 18 Aralık 1538, Fortezza da Basso; neden ○ → b9 |
| #51 (c12) Otoriter devlet | HAFIZA | **○** (kısmen) | "pratica segreta" ○; Magistrato Supremo/casus ağı HAFIZA'da kaldı → b30 |
| #52 (c12) Evlilik, 29 Haziran 1539 | HAFIZA | **◐ DÜZELTME** | 29 Mart vekâlet / 29 Haziran giriş / 29 Temmuz düğün → b10–b12; D9 |
| #54 (c12) Lorenzino Venedik'te öldürülür, Şubat 1548 | HAFIZA | **◐** | **26 Şubat 1548**; "Cosimo'nun emri" tartışmalı → b15; bM3 |
| #55 (c12) Magistrato Supremo; Pitti 1549 | HAFIZA | **◐** (Pitti) / HAFIZA (Magistrato) | → b16, b30 |
| #57 (c12) Marciano, 2 Ağustos 1554 | HAFIZA | **◐** | → b19 |
| #58 (c12) Siena teslim, 17 Nisan 1555 | HAFIZA | **◐** ay / ○ gün | "Nisan 1555"; bir kaynak 21 Nisan işgal → b18 |
| #59 (c12) II. Felipe devri, 1557 | HAFIZA | **◐** yıl / ○ gün | 3 ve 19 Temmuz 1557 tek kaynakta → b20 |
| #60 (c12) Cerbe 1560, Toskana kadırgaları | HAFIZA | HAFIZA | Aramada çıkmadı (sınanmadı) |
| #61 (c12) Santo Stefano, 1561/62 | HAFIZA | **◐** | Onay 1 Ekim 1561; tören 15 Mart 1562 → b21 |
| #62 (c12) Kasım–Aralık 1562 üç ölüm | HAFIZA | **◐** | 20 Kasım / 6 (12) Aralık / 17 Aralık → b23 |
| #63 (c12) 1564 | HAFIZA | **◐** | Treccani → b25 |
| #64 (c12) Büyük Dük, 27 Ağustos 1569 / 5 Mart 1570 | HAFIZA | **◐** | Bulla 27 Ağustos 1569; taç 5 Mart 1570 (bir kaynak Ocak) → b26–b27 |
| #65 (c12) Lepanto, Toskana kadırgaları | HAFIZA | **◐** | **12** kadırga → b28 |
| #66 (c12) Cosimo I ölür, 21 Nisan 1574 | HAFIZA | **◐** yıl-yer / HAFIZA gün | Villa di Castello → b29 |
| #76 (c13) 18–24 Ağustos 1572 | HAFIZA | **◐** | 22 Ağustos girişim, 23 Ağustos konsey, 24 Ağustos katliam → b32–b35 |
| #77 (c13) *Balet comique*, 15 Ekim 1581 | HAFIZA | **◐** | Mekân çelişkisi → b38 |
| #79 (c13) Marie doğar, 26 Nisan 1575 | HAFIZA | **◐** yıl (1575) / ○ (Britannica 1573) | Gün HAFIZA → b39; D20 |
| #80 (c13) Vekâleten evlilik 5 Ekim 1600; Lyon | HAFIZA | **◐** (5 Ekim; çeyiz–borç mahsubu) / ○ (Lyon günü) | → b40–b42 |
| #84 (c13) Rubens döngüsü, 1622–1625 | HAFIZA | **◐** | **26 Şubat 1622** sözleşme; 1625 → b43–b45 |
| #85 (c13) "Aldatılmışlar Günü", 10–11 Kasım 1630 | HAFIZA | **◐** | 10, 11 veya 12 Kasım → b46 |
| #86 (c13) 1631–1642, 3 Temmuz 1642 | HAFIZA | **◐** | Sternengasse 10, plörezi → b47–b49; D13 |
| #93 (c15) Ferdinando I, kardinallikten dönüş | HAFIZA | **◐** (kısmen) | 1562 kardinal (13 yaş); 19 Ekim 1587 başlangıç; 1589 evlilik HAFIZA → b50 |
| #94 (c15) Livornina 1591–93 | HAFIZA | **◐** | 1 Temmuz 1591 taslak; 10 Haziran 1593 → b53 |
| #95 (c15/c14) Ferdinando I ölümü (7 Şubat 1609) | HAFIZA | **○ DÜZELTME** | 17 Şubat 1609 → b51; D12. Cosimo II (28 Şubat 1621) sınanmadı |
| #96 (c15) Cosimo III–Marguerite Louise | HAFIZA | **◐** | Aralık 1674 / Haziran 1675 → b62 |
| #97 (c15) Cosimo III hükümdarlığı | HAFIZA | **○** | 53 yıl, vergi, takas → b63–b65; 1716 bando sınanmadı |
| #98 (c15) Veraset | HAFIZA | **◐** (kısmen) | 1738 Viyana; Craon → b69–b70; 1713/1718 sınanmadı |
| #99 / #103 Gian Gastone, 9 Temmuz 1737 | ◐ ölüm / HAFIZA yaşam | **◐ / ◐** | Treccani (DBI + EI + DS) → b66–b68 |
| #102 (c16) 1717 dönüş | HAFIZA | **◐** yıl | Casciu → b72; 1716 (Johann Wilhelm) sınanmadı |
| #104 (c0/c16) Patto, 31 Ekim 1737 | ◐ | **◐ güçlendi** | 13 madde, Fransızca, Craon → b73; D10 |
| #105 (c0/c16) 3. madde | ◐ içerik / ○ lafız | **◐ içerik / ◐ İtalyanca çeviri lafzı / ○ Fransızca özgün** | → b74, bD23–bD24; D6'ya ek |
| #106 (c0/c16) 1739 vasiyeti | ○ | **○** (ilerleme) | ≈1739 + kodisiller; metin görülmedi → b77 |
| #107 (c0) 18 Şubat 1743 | ◐ (yer doğrulanamadı) | **◐** + Palazzo Pitti **◐ zayıf** | Saat/tanık yok → b78–b79 |
| #108 (c16) San Lorenzo'ya gömülme | HAFIZA | **◐** | → b80–b81 |
| #110 (c16) 1737–1860 Lorraine | HAFIZA | **◐** (kısmen) | Craon 1737–48; 1739; 1765; 1786 → b69–b71; 1860 sınanmadı |
| #111 (c16) Modern hatırlama | ○ | **◐** | 18 Şubat alayı; 31 Ekim → b82–b83 |

### 2.B Canlı ayrıntı (M4 §3)

| M4 satırı | Eski | Yeni | Not |
|---|---|---|---|
| §3.A #2 Patto'nun amacı/lafzı | ◐ içerik / ○ lafız | **◐ / ◐ (çeviri)** | bD23; D6'ya ek |
| §3.A #5 madde sayısı | doğrulanamadı | **◐ (13)** | bD24; D10 |
| §3.A #6 ölüm yeri bulunamadı | ◐ / ○ | **◐ zayıf (Pitti)** | b78 |
| §3.C #2 seçilişin psikolojisi | HAFIZA YORUM | **◐ iskelet** + YORUM | Guicciardini çevresi → bD4; "yönetilebilir sanıldı" hâlâ YORUM |
| §3.C #3 Eleonora portresi/elbise | HAFIZA | **○** | Portre ◐; "1857'de bulunan elbise" doğrulanmadı; portredeki elbise gömü elbisesi **değil** (○) → bD7 |
| §3.C #4 1562 | HAFIZA | **◐** | Uffizi dili → bD8 |
| §3.C #6 Siena kuşatması | HAFIZA | **◐ (kısmen)** | 15 ay, açlık; Monluc adı → b18 |
| §3.C #7 Büyük Dük tacı | HAFIZA | **◐** | → b26–b27 |
| §3.D #8 24 Ağustos şafağı / "hepsini öldürün" | HAFIZA ANEKDOT | **○ ANEKDOT** | Zincir kurulamadı → bM8 |
| §3.D #9 Marie çeyizi-borç | HAFIZA | **◐** | → b41 |
| §3.D #11 Rubens döngüsü | HAFIZA | **◐** | → bD14–bD16 |
| §3.D #12 Köln'de son | HAFIZA | **◐** | → b48; D13 |
| §3.E #6 Livornina | HAFIZA | **◐** | → b53 |
| §3.E #7 Cosimo III'ün iki yüzü | HAFIZA | **○** | 1678/1691 reformlar; 1716 bando sınanmadı |
| §3.E #8 Gian Gastone anekdotları | HAFIZA ANEKDOT | **◐** (Treccani) / ANEKDOT (yatak vb.) | → bD19–bD22; bM11 |
| §3.E #9 Mirasın pazarlığı | HAFIZA | **◐** | → b69–b70 |
| §3.F #6 Soy sonu | HAFIZA | **○** | D15 → b84 |

### 2.C Mit/tartışma (M4 §5)

| M4 satırı | Eski | Yeni | Not |
|---|---|---|---|
| §5.1 X. Leo "papalığı verdi" | ○ ANEKDOT | **○ ANEKDOT** | İkinci aramada da Giorgi metni **çıkmadı** → bM16 |
| §5.11 Alessandro'nun babası/annesi | HAFIZA | **○** | İki baba hipotezi; Simonetta hizmetçi; Nestor 1560 → bM4; D17 |
| §5.12 Cosimo–Garzia | HAFIZA ANEKDOT | **◐ olgu (sıtma) / ANEKDOT (efsane)** | Uffizi, 1857 → bM1 |
| §5.13 Lorenzino | HAFIZA | **◐** | Apologia/Brutus ◐; Dall'Aglio'nun 1548 yorumu → bM3 |
| §5.14 Catherine ve 1572 | HAFIZA | **◐ (kısmen)** | Britannica, Knecht, Jouanna; Holt/Frieda/Crouzet/Sutherland doğrulanamadı → bM7 |
| §5.17 çatal | HAFIZA | **○** | → bM9 |
| §5.17 dondurma | HAFIZA | **◐ mit** | → bM9 |
| §5.17 parfüm | HAFIZA | **○** | → bM9 |
| §5.17 zehir | HAFIZA | **◐ mit** | → bM9 |
| §5.17 gerçek katkılar (balet) | HAFIZA | **◐** | → b38 |
| §5.18 Gian Gastone anekdotları | HAFIZA ANEKDOT | **◐** | → bM11 |
| §5.19 Patto lafzı | ○ | **◐ (çeviri lafzı)** | → bM14; D10 |
| §5.20 AML doğum/ölüm | ◐ | **◐** | Ölüm yeri eklendi (b78) |
| §5.22 Yan kollar | HAFIZA | **○** | D15 → bM17 |

### 2.D Sayılar (M4 §4) ve TR-BAĞ (M4 §6)

| M4 satırı | Eski | Yeni | Not |
|---|---|---|---|
| §4 Marie'nin çeyizi ≈600.000 écu | HAFIZA | **◐** | → b41 |
| §4 Rubens 24 tablo (21+3) | HAFIZA | **◐** | → b43 |
| §4 Lepanto'da ≈12 Toskana kadırgası | HAFIZA (düşük) | **◐** | → b28 |
| §4 Cosimo III hükümdarlığı 53 yıl | HAFIZA | **○** | Wikipedia: "Toskana tarihinin en uzunu"; tek kaynak hattı (1670–1723 aritmetiği tutarlı) → b63 |
| §4 Catherine'in 10 çocuğu; Aziz Bartolomeo ölü sayısı | HAFIZA | HAFIZA | Aranmadı |
| §6 T3 Tunus 1535 | HAFIZA | HAFIZA | Aranmadı |
| §6 T4 Fransız–Osmanlı Tirren 1552–55 | HAFIZA | **○** (1553'e çekildi) | → b17, T15 |
| §6 T5 Cerbe 1560 | HAFIZA | HAFIZA | Toskana payı çıkmadı |
| §6 T6 Santo Stefano | HAFIZA | **◐** | → b21–b22, T16 |
| §6 T7 Lepanto | HAFIZA | **◐** | → b28, T17 |
| §6 T8 Livorno'nun dönüşümü | HAFIZA | **◐ (kısmen)** | Cosimo: Livorno limanı; asıl büyüme Ferdinando I → b31, b52 |
| §6 T9 Livornina | HAFIZA | **◐** | → b53, T20 |
| §6 T10 Fahreddin II | HAFIZA | **◐ + DÜZELTME** | 1608 antlaşma Ferdinando I; sürgün 1613 **Cosimo II** döneminde → b58–b59, T25 |
| §6 T12 Bâb-ı Âli ile resmî ilişkiler | HAFIZA (düşük) | **◐** | Var: 1574–78 ve 1598 → T19, T21 |
| §6 T13 Uzun Savaş'ta Toskana | HAFIZA (düşük) | **○** | Wikipedia özeti → T27 |

---

## 3. Yeni kronoloji satırları

> Okuma: **Kaynak** sütunu, arama sonucunda görülen sayfaların adıdır (URL'ler §8); içerikleri **açılıp okunmadı**. "Bölüm" sütunu plan bölümünü (c0…c16) gösterir. Tarih çelişkileri **Not** sütunundadır.

### 3.A c11–c12 — Alessandro'nun sonu, Cosimo'nun gelişi (1537–1539)

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| b1 | c11 | 5–6 Ocak 1537 (akşam/gece) | **Lorenzino de' Medici, kuzeni Alessandro'yu kendi dairesinde öldürür.** Alessandro'ya cinsel bir buluşma vaat edilmiştir; Lorenzino bir bahaneyle odadan çıkar; adamlarını önceden göndermiş olan Alessandro uyuyakalır; Lorenzino hizmetkârı "Scoronconcolo" ile döner, ikisi kılıç ve hançerle öldürür, Alessandro şiddetle direnir | ◐ | EN Wikipedia "Alessandro de' Medici, Duke of Florence" ve "Lorenzino de' Medici"; Britannica "Lorenzino" (5–6 Ocak akşamı); *Italies* (Kasım 2025, G. Marrone: 5'ten 6'ya gece) | Bir sayfa 7 Ocak der (hata sayılır). Warburg Enstitüsü belgesi ("Truths and Lies of a Renaissance Murder"; yazar özetten alınamadı): Varchi anlatısının "birçok yönü kesin yanlış" (○). **Saat akışı hâlâ yok.** |
| b2 | c11 | 5–6 Ocak 1537 | Tuzaktaki kadının kimliği: çoğu tarihçi **Caterina Soderini** (Leonardo Ginori'nin karısı) der; bazıları Lorenzino'nun kız kardeşi **Laudomia**. Tetikçinin adı kaynakta değişir: Piero di Giovannabate (Wikipedia), Baccio del Tavolaccino (Treccani EI), Michele del Tavolaccino (M4 hafızası) | ◐ (Soderini, çoğunluk) / ○ (diğerleri) | EN Wikipedia "Lorenzino de' Medici"; Treccani EI "Lorenzino de' Medici" | Senaryoda "bir kadın" ya da "Caterina Soderini Ginori olduğu söylenir"; tetikçi için lakap "Scoronconcolo" yeter. |
| b3 | c11 | 6 Ocak 1537 | Alessandro'nun boğuşmada Lorenzino'nun bir parmağından parça ısırdığı anlatılır | ○ ANEKDOT | EN Wikipedia ("one source says") | Kim yazdı belirsiz (Varchi hattı: HAFIZA). Kesin kipte verilmez. |
| b4 | c11 | Ocak–Şubat 1537 | Lorenzino *Apologia*'sında eylemini siyasi (Floransa'yı, çoğunun "tiran" saydığı birinden kurtarmak) ve Brutus'a benzer sunar; Varchi de davasını Brutus'la kıyaslar; Treccani eylemi siyasi değil **özel intikam** sayar; Wikipedia kişisel kıskançlık ve miras kavgası gibi birçok hipotezi anar | ◐ (Apologia, Brutus kıyası) / ○ (yazarlık, motif) | EN Wikipedia "Lorenzino de' Medici"; Treccani EI "Lorenzino"; ellopos.net "Against despots" | *Apologia*'nın yazarı bir özette "belirsiz; büyük olasılıkla kendisi" diye geçer (○). Michelangelo'nun bu anmaya katılmak isteyenler arasında olduğu söylenir (○). bM3. |
| b5 | c12 | 8 / 9 / 10 Ocak 1537 | **Cosimo'nun seçilişi.** Senato (Kırk Sekizler) 9 Ocak'ta genç Cosimo'yu Floransa devletinin başına getirir; **10 Ocak'ta** Senato, seçim anında konan koşulları resmîleştirir: **dük unvanı yok**, yalnız *capo e primario della città*; yardımcısını Senato üyeleri arasından seçecektir. Bir kaynak seçimi 8 Ocak verir | ◐ | Treccani DBI "COSIMO I"; Treccani DBI "MEDICI, Raffaello de'"; Treccani DBI "VITELLI, Alessandro"; EN Wikipedia "Cosimo I" | M4 #49 (9 Ocak) ◐. Alıntılar bD3–bD4. D14. Kardinal Cibo ayrıntısı aramada **çıkmadı** (HAFIZA). |
| b6 | c12 | Ocak 1537 | Seçimin arkasında **Francesco Guicciardini** çevresinde toplanan, Kırk Sekizler Senatosu'ndan sekiz "optimat" (aralarında Raffaello de' Medici) vardır; Fortezza da Basso komutanı **Alessandro Vitelli** Guicciardini ve diğerlerince ikna edilip 9 Ocak'taki seçimi destekler; Francesco Vettori, Cosimo'nun 1537'deki özel danışmanları arasındadır | ◐ | Treccani DBI "MEDICI, Raffaello de'"; "VITELLI, Alessandro"; "CORSI, Giovanni" | Cosimo'nun "yönetilebilir sanılması" (M4 §3.C #2) hâlâ **YORUM**. |
| b7 | c12 | Haziran–Eylül 1537 | V. Karl, Haziran 1537'de Cosimo'yu Floransa devletinin başı olarak tanır (Fransa'ya karşı yardım karşılığı); Eylül 1537'de Cosimo kendini "dük" olarak anmaya başlar. Cosimo, imzaladığı "yetkiyi Kırk Sekizler'e devreden" maddeyi kısa sürede reddeder | ○ | EN Wikipedia "Duchy of Florence", "Cosimo I" (arama özeti) | D14. Tek kaynak hattı. |
| b8 | c12 | 31 Temmuz / 1–2 Ağustos 1537 | **Montemurlo.** Cosimo'nun kuvvetleri (Alessandro Vitelli) aceleyle toplanmış sürgün ordusunu yener. Treccani sürgünlerin başında **Filippo Strozzi**'yi anar; Wikipedia komutan olarak Piero Strozzi ve Bernardo Salviati'yi; Filippo Strozzi yakalanır | ◐ (olgu) / ○ (gün) | EN Wikipedia "Battle of Montemurlo" (1 veya 2 Ağustos); EBSCO (31 Temmuz); Treccani Dizionario di Storia | Treccani: zafer cumhuriyetçi restorasyon tehdidini bitirdi; Cosimo "Toskana devletinin kurucusu" sayılır. Baccio Valori adı aramada **çıkmadı**. |
| b9 | c12 | 18 Aralık 1538 | **Filippo Strozzi** (d. 4 Ocak 1489) Fortezza da Basso'da (Vitelli'nin gözetiminde) ölür: intihar mı, Cosimo'nun emriyle öldürülme mi, kaynaklar ayrışır | ◐ (tarih, yer) / ○ (neden) | Find a Grave "Filippo Strozzi the Younger"; EN Wikipedia (çeviri aynası); Treccani DBI "COSIMO I" | İşkence iddiası yalnız bir özette (○). |
| b10 | c12 | 29 Mart 1539 | Napoli'de **Cosimo–Eleonora di Toledo** evlilik sözleşmesi imzalanır ve **vekâleten evlilik** kutlanır | ◐ | Italian Art Society (S. Reiss); palazzo-pitti.net "Eleonora of Toledo"; EN Wikipedia infobox | **D9**: M4 #52 düzeltildi. |
| b11 | c12 | 11–29 Haziran 1539 | Eleonora, kardeşi Garcia ve yedi kadırgayla 11 Haziran'da Napoli'den denize açılır; 22 Haziran sabahı Livorno'ya varır; Pisa yolunda Cosimo ile buluşur (22 veya 23 Haziran); Poggio a Caiano'da birkaç gün kalırlar; **29 Haziran'da ayrı ayrı Floransa'ya girerler** | ◐ | Italian Art Society; EN Wikipedia "Eleanor of Toledo" | "29 Haziran" = **giriş günü**, düğün değil. |
| b12 | c12 | 29 Temmuz 1539 | **Resmî düğün.** Palazzo Medici'nin ikinci (bahçe) avlusunda şenlikler; dekor Niccolò Tribolo; resimler arasında Bronzino, Francesco Salviati, Battista Franco, Bachiacca; Pierfrancesco Giambullari'nin 1539 tarihli basılı anlatımı vardır | ◐ | Italian Art Society; palazzo-pitti.net | Eleonora 17 yaşında. |

### 3.B c12 — Cosimo I'in devleti, savaşları, ölümler (1544–1574)

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| b13 | c12 | 1544 | Barbaros'un filosu doğuya dönüşte Toskana kıyılarını vurur: Porto Ercole, Giglio, Talamone, Lipari yağmalanır, ≈6.000 esir (bir anlatım); Lipari saldırısı Temmuz 1544 (başka kaynak) | ○ | Arama özeti; kaynak sayfası belirtilmedi (sonuçlar arasında EN Wikipedia "Ottoman wintering in Toulon" ve National Geographic "Barbarossa" vardı) | TR-BAĞ bağlamı. Piombino/Elba'ya 1544 saldırısı **doğrulanamadı** (bir İtalyan kaynak Türk filosunu Piombino/Elba'da 1543'e koyar). Hangi kentin kimin toprağı olduğu özetlerde belirtilmedi. |
| b14 | c12 | 1548 | Cosimo Elba'da **Cosmopoli**'yi (Portoferraio) kurar; üç kale (Forte Stella, Falcone, Inglese) | ◐ | EN Wikipedia "Portoferraio"; visittuscany.com | Mimarlar Bellucci ve Caterini, sonra Buontalenti (bir kaynak). 1553'te Dragut'a dayanır (b17). |
| b15 | c12 | 26 Şubat 1548 | **Lorenzino Venedik'te öldürülür**: San Polo/San Tomà köprüsü yakınında iki tetikçi, Lorenzino ve amcasına saldırır; amca kaçar; tetikçiler yakalanmaz | ◐ | Yale UP (Dall'Aglio, *The Duke's Assassin*, alıntı sayfası); History Today "Solving a Renaissance Murder Mystery" | **Geleneksel görüş: emri Cosimo verdi.** Dall'Aglio, Floransa Devlet Arşivi'ndeki şifreli mektuplar nedeniyle "Cosimo'nun Venedik'teki adamlarının işin içinde olduğundan" kuşku duyar (Yale özeti; ○). bM3. M4 #54 ◐. |
| b16 | c12 | 1549 | Eleonora **Palazzo Pitti'yi satın alır**; yenileme yaklaşık on yıl sürer, aile yine de taşınır | ◐ | EN Wikipedia "Eleanor of Toledo"; Apollo Magazine | Boboli/mimar: M3. |
| b17 | c12 | 1553 | Fransız–Osmanlı seferi: Osmanlı filosu, Fransız birliklerini (Maréchal de Thermes) Sienalı Maremma'dan Korsika'ya taşır; Dragut aynı sezon Elba'yı yağmalar ama Portoferraio surları dayanır | ○ | EN Wikipedia "Italian War of 1551–1559"; worldhistoryedu.com "Invasion of Corsica (1553)"; visittuscany.com | Yıl **1553** (M4 T4 "1552–55"; "1555'te Elba" kaynaksız). TR-BAĞ T15. |
| b18 | c12 | Ocak 1554 – Nisan 1555 | **Siena kuşatması**: ≈15 ay; açlık teslimi zorlar; Siena Medici işgaline Nisan 1555'te girer (bir kaynak 21 Nisan); Montalcino'daki Fransız yanlısı direniş 1557'ye (M4: 1559) sürer | ◐ | historyofwar.org "Siege of Siena"; flore.unifi.it "Guerra e conquista di Siena"; EN Wikipedia "Fortezza Medicea (Siena)" | Başlangıç yılı 1553/1554 çelişir. M4 #58 (17 Nisan) doğrulanmadı. Fransız komutan Monluc'un *Commentaires*'i anılır. |
| b19 | c12 | 2 Ağustos 1554 | **Marciano (Scannagallo).** Gian Giacomo de' Medici, Marignano Markisi ("Medeghino") komutasındaki Floransa–İmparatorluk ordusu, Piero Strozzi'nin Fransız–Sienalı ordusunu yener; Siena'nın saha ordusu biter | ◐ | EN Wikipedia "Battle of Marciano"; historyofwar.org; vive.cultura.gov.it | Marignano Markisi Floransalı Medici'lerle akraba değildir (HAFIZA; karışıklık riski için not). |
| b20 | c12 | 1557 | II. Felipe Siena'yı Cosimo'ya devreder: "fetih iki yıl sonra Felipe II tarafından yasallaştırıldı" (Treccani); bir kaynakta fiefin tevdii **3 Temmuz 1557**, Chiappino Vitelli'nin şehri Cosimo adına teslim alışı **19 Temmuz 1557** | ◐ (yıl) / ○ (gün) | Treccani Enciclopedia on line "Cosimo I"; tek gün kaynağı (özet) | |
| b21 | c12 | 1 Ekim 1561 / 15 Mart 1562 | **Santo Stefano Tarikatı.** IV. Pius'un onayı 1 Ekim 1561; 15 Mart 1562'de Pisa'da başpiskopos Giorgio Cornaro papa adına Cosimo'yu Büyük Usta olarak giydirir | ◐ | EN Wikipedia "Order of Saint Stephen"; finestresullarte.info; piazzadeicavalieri.sns.it | M4 #61 (1561/62) çözüldü. Amaç: Osmanlı ve korsan deniz taşımacılığıyla savaşmak, Hristiyan esirleri kurtarmak; Cosimo'nun farklı kentlerin soylularını birleştirecek sembolik bir davaya ihtiyacı olduğu (bir kaynak; ○). |
| b22 | c12 | 1563–1564 | Tarikatın ilk deniz işleri: 1563'te İspanya'nın Oran'ı kurtarma harekâtına destek; 1564'te Müslüman ticaretine ve limanlarına ilk saldırı; üs Livorno; ganimet satışı Livorno'yu zenginleştirir, kuzey Avrupa tüccar ve korsanlarını çeker | ○ | EN Wikipedia "Order of Saint Stephen"; finestresullarte.info | Kadırga *Lupa*'nın Müslüman kadırgalarıyla çatışmada kaybı (○). Livorno'daki esir bagno'su aramada **çıkmadı**. TR-BAĞ T16. |
| b23 | c12 | 20 Kasım – 17 Aralık 1562 | Aile Maremma/Tirren kıyısı gezisinde sıtmaya yakalanır. Kardinal **Giovanni** 20 Kasım'da Livorno'da (19 yaşında); **Garzia** 6 Aralık'ta (bir yerde 12 Aralık); **Eleonora** yaklaşık bir aylık hastalıktan sonra 17 Aralık'ta Pisa'da ölür; Ferdinando dışında herkes birkaç haftada gider | ◐ | EN Wikipedia "Giovanni de' Medici (cardinal)", "Garzia de' Medici", "Eleanor of Toledo"; Uffizi "Burial clothes of Don Garzia de' Medici"; historyofroyalwomen.com | Garzia günü 6/12 Aralık çelişkili. Garzia 15–16 yaşında (popüler anlatımda 16; doğum yılı 1547: HAFIZA). |
| b24 | c12 | 1857 | Medici mezarları ilk kez incelenir: Garzia "kırmızı atlas ceket giymiş bir iskelet" olarak tanımlanır; şiddet izi bulunmaz, ikisinin de sıtmadan öldüğü sonucuna varılır | ◐ | Uffizi (Garzia'nın gömü giysisi sayfası); EN Wikipedia "Garzia de' Medici" | Efsane: bM1. Popüler bir kitapta (Bob Brier) 2004'te Giovanni'nin kalıntılarının şiddet izi için incelendiği anlatılır (○). |
| b25 | c12 | 1564 | Cosimo yönetimi büyük oğlu Francesco'ya bırakır; dük unvanını korur ve dış politikayla ilgilenmeyi sürdürür | ◐ | Treccani DBI "COSIMO I"; Dizionario di Storia | M4 #63. |
| b26 | c12 | 27 Ağustos 1569 | V. Pius, uzun müzakerelerden sonra Cosimo'ya **Büyük Dük** unvanını bulla ile verir (daha önce IV. Pius döneminde İspanya ve İmparatorluk muhalefeti kral/arşidük unvanını engellemişti) | ◐ | Treccani DBI "COSIMO I" (1569); EN Wikipedia "Grand Duchy of Tuscany", "List of grand dukes of Tuscany" (27 Ağustos); 1570 Almanca baskı (müzayede) | |
| b27 | c12 | 5 Mart 1570 → 1575/76 | Roma'da V. Pius'un elinden taç (5 Mart 1570; bir kaynak Ocak 1570). İmparator II. Maximilian'ın tanıması **2 Kasım 1575** diplomasıyla, Francesco I lehine (başka kaynak 1576); Francesco imparatorluk Hofkammer'ine **100.000 duka** tazminat ödemek zorunda kalır | ◐ (Mart 1570) / ○ (1575 diploması, 100.000) | EN Wikipedia "Grand Duchy of Tuscany", "Grand Ducal Crown of Tuscany"; Treccani | Maximilian II 1576 Ekim'de öldü (HAFIZA); "ölümünden sonra" diyen kaynak çelişir. M4 #64. |
| b28 | c12 | 7 Ekim 1571 | **Lepanto.** Toskana devleti ≈200 kadırgadan **12**'sini gönderir; gemilerde 100'den fazla Santo Stefano şövalyesi (bir anlatım). Başka bir kaynak: "papalık tarafından kiralanmış 12 Toskana kadırgası" | ◐ (12 kadırga) / ○ (şövalye sayısı, komuta) | finestresullarte.info ve Wikipedia "Order of Saint Stephen" özetleri; EN Wikipedia "Battle of Lepanto" (Toskana ve tarikat Kutsal Birlik tarafları arasında); Britannica Kids | Toskana komutanı doğrulanamadı (Tommaso de' Medici adı HAFIZA, **sınanmadı**). Kutsal Birlik toplamı 206–207 kadırga (+6 galeas) kaynaklara göre. TR-BAĞ T17. |
| b29 | c12 | 21 Nisan 1574 | **Cosimo I Villa di Castello'da ölür** | ◐ (yıl+yer) / HAFIZA (gün) | Treccani Dizionario di Storia (arama özeti) | |
| b30 | c12 | 1537–1574 | Devlet aygıtı: Cosimo, Alessandro'nun magistralarını korur ama doğrudan dükün yönettiği gizli **"pratica segreta"**ya tabi kılar. *Otto di Guardia e Balìa* arşivi: Principato'nun kuruluşundan 1777'ye dek ağırlıkla ceza işleri; Floransa Yahudi cemaati üzerinde de yetkisi vardır | ○ | Treccani Dizionario di Storia; Otto di guardia e balìa arşiv kaydı (projetos.dhlab.fcsh.unl.pt) | **Magistrato Supremo (1549), casus ağı, sansür aramada çıkmadı** (HAFIZA). Grokipedia'nın "Otto'yu casusluk aracına çevirdi" iddiası düşük kaynak, kullanılmadı. |
| b31 | c12 | 1540'lar–1560'lar | Cosimo'nun ekonomisi: Livorno'yu, denizden uzaklaşan Pisa limanının yerine geliştirir; Portoferraio; arazi ıslahı ve Elba demir madenleri (öğrenci notu; ○); 1540'lar–50'lerde İberya Yahudi tüccarlarını Floransa ve Pisa'ya çağırır, sonra politikayı tersine çevirir | ○ | EBSCO research starter "Cosimo I"; skuola.net (düşük); Jewish Virtual Library | Livorno'nun asıl büyümesi Ferdinando I döneminde (b52–b53). Livorno Fortezza Vecchia'nın Alessandro döneminde (1518–1533) bittiği (○). |

### 3.C c13 — Catherine ve Marie (1572–1642)

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| b32 | c13 | 22 Ağustos 1572 | **Coligny'ye suikast girişimi** (Maurevert). Azmettirici tartışmalı: Guise ailesi (özetlere göre "daha olası ama kanıtlanamaz"), Alba ya da Catherine | ◐ (olay) / ○ (azmettirici) | Britannica "Massacre of Saint Bartholomew's Day"; EN Wikipedia "Assassination of Admiral Coligny"; Catholic Encyclopedia | |
| b33 | c13 | 23 Ağustos 1572 | **Acil konsey**: kral, kardeşi Anjou Dükü Henri, Catherine ve danışmanlar Huguenot liderlerinin öldürülmesine karar verir | ◐ | Britannica; EN Wikipedia "St. Bartholomew's Day massacre" | Britannica: Catherine "Coligny ve başlıca yandaşlarının öldürülmesini onaylamış görünüyor, ama büyük olasılıkla sonrasındaki katliamı değil". bM7. |
| b34 | c13 | 24 Ağustos 1572 | **Katliam.** Birincil sorumluluk kraliyet muhafızına ve Anjou'nun askerlerine (Guise ve Aumale komutasında) yüklenir | ◐ | Britannica; EBSCO research starter | |
| b35 | c13 | 26 Ağustos 1572 | IX. Charles kamuya açık bir beyanla sorumluluğu üstlenir; "kraliyet" ifadesi sıkça "Catherine" diye okunmuştur | ○ | arama özeti (tek kaynak) | |
| b36 | c13 | Haziran 1572 | Jeanne d'Albret ölür; doktorlar akciğer hastalığı teşhis eder; bir kaynağa göre otopsi zehir bulmaz | ○ | atlasobscura.com; EN Wikipedia "René Bianchi (perfumer)" (özet) | Zehirli eldiven efsanesi bM9. |
| b37 | c13 | ≥1547 → 1578 | **René Bianchi** (Renato Bianco, "René le Florentin"), kraliçenin resmî parfümcüsü (en az 1547'den; ö. 1578); tarihte "Catherine'in zehircisi" diye ünlüdür | ○ | EN Wikipedia "René Bianchi (perfumer)" | Tek kaynak. |
| b38 | c13 | 15 Ekim 1581 | ***Balet comique de la reine***: Joyeuse Dükü ile Marguerite de Lorraine-Vaudémont'un düğün şenlikleri kapsamında, Catherine'in himayesinde; koreografi Balthasar de Beaujoyeulx; dekor ve kostüm Jacques Patin; Circe konusu; 5 saati aşan gösteri; 1582'de basılı metin (basılı libretosu olan ilk balet) | ◐ | EN Wikipedia "Ballet Comique de la Reine", "Ballet de cour"; Britannica; EBSCO research starter | **Mekân çelişkisi:** Hôtel de Bourbon büyük salonu (Louvre bitişiği) / Louvre Grand Salle. "İlk balet de cour" sıfatı kaynaklarda "genellikle" diye geçer: nitelikli. |
| b39 | c13 | 1575 (1573) | Marie doğar: çoğu kaynak 1575; Britannica 1573 | ◐ (1575) / ○ (1573) | Britannica; EN Wikipedia | M4 #79 gün (26 Nisan) hâlâ HAFIZA. D20. |
| b40 | c13 | 5 Ekim 1600 | Marie–IV. Henri **vekâleten evliliği** Floransa'da (Santa Maria del Fiore; Kardinal Aldobrandini). Vekil kişi çelişir (Ferdinando I mi, Bellegarde mi) | ◐ (5 Ekim) / ○ (vekil) | roderickconwaymorris.com; Hertziana "Proxy Wooings and Weddings"; unofficialroyalty.com; herodote.net | herodote.net **"5 Mayıs 1600"** yazar (çelişki; ○). |
| b41 | c13 | 1600 | **Çeyiz 600.000 écu** ("scudi" bir kaynakta), **Fransa'nın Ferdinando I'e olan borcundan düşülür** (*"déduit sur la dette"*); borç "bir milyon écu'ya yakın" (bir Fransızca kaynak); Britannica: evlilik, borçları ödemeye yarayacak çeyiz için yapıldı; ek yıllık 20.000 (tek kaynak) | ◐ (mahsup, 600.000) / ○ (borç tutarı, yıllık 20.000) | herodote.net; sept.info ("Dumas, Henri IV"); Britannica | Sorguda hafızadan denenen "1.174.000 écu" (borç/çeyiz hesabı) aramada **görülmedi**; kullanılmasın. |
| b42 | c13 | 12–17 Aralık 1600 | Lyon: Henri gelini ilk kez 12 Aralık'ta görür (bir kaynak); dinî tören 17 Aralık (herodote.net: 16 Aralık) | ○ | roderickconwaymorris.com; herodote.net | Günler çelişir. |
| b43 | c13 | 26 Şubat 1622 | **Rubens, Louvre'da iki sözleşme imzalar**: biri Marie'nin yaşamını anlatan 24 tablo, öteki IV. Henri için eşlik eden seri; "her figürü kendi eliyle yapıp boyamayı" taahhüt eder; Rubens'in aldığı en büyük sipariş | ◐ | EN Wikipedia "Luxembourg Palace", "Marie de' Medici cycle"; melvillesprintcollection.org; Corpus Rubenianum XIV tanıtımları | 24 = **21 yaşam sahnesi + 3 portre** (Louvre notu; Morgan Library). D18. |
| b44 | c13 | 1625 | Marie döngüsü Luxembourg Sarayı'nın batı galerisinde tamamlanıp asılır; Rubens 1625 başında Paris'e dönüp son rötuşları yapar | ◐ | EN Wikipedia "Luxembourg Palace"; artprice haberi | Louvre'a kalıcı yerleşim 1816; "Galerie Médicis" olarak toplanması 1993 (◐). |
| b45 | c13 | 1630–1631 | IV. Henri serisi 1630'da askıya alınır, 1631'de kesin terk edilir (bitmedi); Richelieu'nun komisyonu başka sanatçılara verme girişimi (bir kaynak; ○) | ◐ | EN Wikipedia "Luxembourg Palace"; Corpus Rubenianum XIV.2 (Merle du Bourg) tanıtımı | |
| b46 | c13 | 10 / 11 / 12 Kasım 1630 | **"Aldatılmışlar Günü."** Marie Richelieu'nun azlini ister, kral Richelieu'yu seçer; olay günü kaynaklarda 10, 11 veya 12 Kasım | ◐ | EN Wikipedia "Day of the Dupes" | M4 #85 (10–11 Kasım). |
| b47 | c13 | Şubat 1631 → 1641 | Marie Compiègne'e gönderilir (Şubat 1631; bir kaynak 1630); Temmuz 1631'de krallıktan kaçar (İspanyol Hollandası/Brüksel, Amsterdam); İngiltere'de damadı Charles I'in sarayında 1638–Yaz 1641; sonra Köln | ◐ | Springer "A Queen Mother in Exile: Marie De Médicis in the Spanish Netherlands and England, 1631–41"; EN Wikipedia "Marie de' Medici"; EBSCO | Amsterdam'da görkemli karşılama (bir kaynak; ○). |
| b48 | c13 | 3 Temmuz 1642 | **Marie Köln'de Sternengasse 10'da plörezi ve yoksulluk içinde ölür**; ev Rubens ailesinin 50+ yıl önce oturduğu evdir | ◐ | EN Wikipedia "Marie de' Medici"; EBSCO; encyclopedia.com | **D13**: "Rubens'in verdiği ev" anlatımı, Rubens'in 1640'ta ölmüş olması nedeniyle şüpheli. Hastalık Haziran 1642'de başlar (bir kaynak). |
| b49 | c13 | 1642–1643 | Kalıntılar borçlar ödenene dek bir yıl tutulur (bir kaynak); gövde Saint-Denis'e gömülür; kalbin yeri çelişir (bir kaynak "Köln Katedrali") | ○ | h2g2; EN Wikipedia (çelişkili özetler) | Doğrulanmadı. |

### 3.D c15 — Ferdinando I'den Gian Gastone'ye (1562–1765)

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| b50 | c15 | 1562 → 19 Ekim 1587 | Ferdinando 13 yaşında kardinal yapılır (1562), hiçbir zaman rahip takdis edilmez; 19 Ekim 1587'de kardeşi Francesco I'in ölümüyle hükümdar olur | ◐ | EN Wikipedia "Ferdinando I de' Medici"; britishinstitute.it | "Kardinallikten dönüş 1587/88" ve evlilik (1589, Christine de Lorraine) tarihleri **sınanamadı**. |
| b51 | c15 | 17 Şubat 1609 | Ferdinando I ölür (hükümdarlık 19 Ekim 1587 – 17 Şubat 1609) | ○ | EN Wikipedia özeti (tek kaynak) | **D12**: M4 #95 "7 Şubat". |
| b52 | c15 | 1587–1609 | Ferdinando I'in ekonomisi: Val di Chiana sulama/ıslahı (Pisa, Fucecchio ve Val di Nievole düzlükleri tarıma açılır), bataklık kurutma, güney Toskana'da yol ağı, Livorno ticareti; Usimbardi 1593'te Val di Chiana ıslahını teşvik eder; Livorno nüfusu 10.000'i aşar (bir kaynak) | ◐ (ıslah, yol, Livorno) / ○ (nüfus) | EN Wikipedia "Ferdinando I", "Pietro Usimbardi"; piazzadeicavalieri.sns.it | Halep ile ticaret bağı arayışı Wikipedia özetinde (○). |
| b53 | c15 | 1 Temmuz 1591 / 10 Haziran 1593 | **Livornina.** 1591 taslağı (1 Temmuz 1591 tarihli) ve **1593 *Constitutio*** (Floransa, 10 Haziran 1593): tam dinî özgürlük, af, Toskana vatandaşlığı, özel mahkemeler, sarı rozet muafiyeti, mülk ve ticaret hakkı; topluluk 1593'te beş kişilik konsey kurar | ◐ (iki tarih, şartlar) / ○ (konsey) | EN Wikipedia "History of the Jews in Livorno"; sephardicgenealogy.com; moked.it; upenn.edu | Hitap listesi bD29. Doğu ticareti beklentisi T20. |
| b54 | c15 | 1598 | Ferdinando I, **Neri Giraldi**'yi Sultan'a elçi gönderir; aynı yıl Osmanlı elçisi **Mustafa Ağa** Floransa'da ağırlanır (III. Mehmed ve Kaptan-ı Derya Halil Paşa'nın dostluk ve imtiyaz talebine ilişkin mektuplarıyla); müzakere başarısızlıkla biter | ◐ | Mercan, *Annali dell'Istituto storico italo-germanico in Trento* 49/1 (2023), 97–123 (özet); iris.uniroma1.it kaydı (Giraldi görevi) | Giraldi çalışması: Ferdinando'nun kendini Katolikliğin savunucusu sunup İspanya'ya bağımlılığı azaltma amacı (özet). T21. |
| b55 | c15 | 1599 | **Sakız (Chios) seferi**: 2.000 kişi ve beş gemi; başarısız; Osmanlı tarafı ≈10.000, Floransa kaybı ≈400 | ○ | EN Wikipedia "Chios expedition (1599)" | Tek kaynak; tarikat şövalyeleri merkezde. T22. |
| b56 | c15 | 1605–1609 | Santo Stefano şövalyeleri Ion ve Ege'de Osmanlı'ya karşı başarı kazanır (1605–09). **Bona (Annaba) 1607**: amiral Jacopo Inghirami; tarikatın en büyük amfibi harekâtı; şehir yakılır, 470 ölü, 1.500 esir (bir anlatım). Bernardino Poccetti'nin **Sala di Bona** freskleri (Palazzo Pitti, 1607–1609) Bona ve Prevesa'yı anlatır | ◐ (Bona 1607, Sala di Bona) / ○ (rakamlar) | EN Wikipedia "Order of Saint Stephen"; finestresullarte.info; Royal Collection harita kaydı | Prevesa'nın 1605 tarihi HAFIZA, sınanamadı. T24. |
| b57 | c15 | 1607 | Ferdinando I, Halep'te isyancı paşa ile antlaşma yapar; Osmanlı kuvvetleri isyanı yaklaşık yirmi gün sonra ezer; mühendis Giovanni Altoni'nin "Suriye gezisi" | ○ | rime.cnr.it makalesi (özet) | İsyancı paşanın adı özetten alınamadı (Canpulatoğlu Ali Paşa HAFIZA). T23. |
| b58 | c15 | 1608 | **Ferdinando I–Fahreddin II** (Maanoğlu, Dürzi Emiri) antlaşması: açık ticari bölüm + gizli askerî bölüm; Osmanlı baskı yaparsa Medici toprağında sığınma maddesi | ◐ | Aramco World (Temmuz/Ağustos 2014); journals.ku.edu "The Druze Emir in Renaissance Europe" | M4 T10. T25. |
| b59 | c15 | 1613 → 1618 → 1635 | Fahreddin 1613'te yaklaşık yüz kişiyle üç gemide (biri Hollanda, ikisi Fransız) Toskana'ya sürgüne gider; Ferdinando 1609'da ölmüş olduğundan sürgün **Cosimo II** döneminde (1609–21) geçer; 1618'de Şam valisi Muhammed Paşa ile dostluk sonrası döner; IV. Murad 1635'te tutuklanıp İstanbul'da idam edilmesini emreder | ◐ (1613, 1618) / ○ (gemi sayısı, 1635) | Aramco World; journals.ku.edu | 1613'te padişah I. Ahmed (HAFIZA). |
| b60 | c15 | 1621 | Ferdinando II, 10 yaşında Cosimo II'nin yerine geçer; naiplik: büyükannesi Christine de Lorraine ve annesi Maria Maddalena d'Austria | ◐ | EN Wikipedia "Ferdinando II de' Medici" | Cosimo II'nin ölümü (28 Şubat 1621) ve nedeni (verem iddiası) **sınanamadı**. |
| b61 | c15 | 1630 / 1633 / 1657 | Floransa'da veba (1630); Galileo Roma'ya çağrılır ve vazgeçirilir (1633), Ferdinando II davada Galileo'yu kayırır; Accademia del Cimento (1657; Ferdinando II ve kardeşi Leopoldo) | ◐ | PBS "Medici" zaman çizelgesi; Museo Galileo; EN Wikipedia "Accademia del Cimento" | M3 alanı; çapraz referans. |
| b62 | c15 | Aralık 1674 – Haziran 1675 | **Cosimo III–Marguerite Louise d'Orléans.** Cosimo, karısının Montmartre manastırına gitmesine razı olur (Aralık 1674); 80.000 livre pension; Haziran 1675'te ayrılır, Poggio a Caiano'daki değerli ne varsa söker | ◐ | EN Wikipedia "Cosimo III", "Marguerite Louise d'Orléans"; historyofroyalwomen.com | M4 #96. Evlilik yılı (1661) sınanmadı. Özetlerde Marguerite bir yerde XIII. Louis'nin yeğeni, başka yerde XIV. Louis'nin kuzeni diye geçer (çelişki değil: aynı akrabalığın iki yönü; HAFIZA ile uyumlu). |
| b63 | c15 | 1670–1723 | Cosimo III **53 yıl** hüküm sürer (Toskana tarihinin en uzunu); fuhuş ve Mayıs şenliklerini düzenleyen yasalar; "Public Decency" bürosu; eğitim üzerinde yeniden denetim; vergi artışı | ○ | EN Wikipedia "Cosimo III de' Medici" ve aynaları | Hepsi tek (Wikipedia) hattı. |
| b64 | c15 | 17. yy sonu – 18. yy başı | Hazine tahvil faizini ödeyemez, faiz 0,75 puan indirilir; kırsal pazarlarda takas yayılır; Ferdinando II'nin ölümünde (1670) nüfus 720.594, Siena "neredeyse terk edilmiş"; yün sanayii geriler, ipek gelişir (bir akademik özet) | ○ | EN Wikipedia "Ferdinando II", "Cosimo III", "Grand Duchy of Tuscany"; Cambridge (Altopascio, sonuç bölümü) | Floransa şehir nüfusu bulunamadı. Gerilemenin başlangıcı Ferdinando II'ye çekiliyor. bM12. |
| b65 | c15 | 1678, 1691 | Cosimo III'ün adli "reformları" (Treccani DBI anar); sonuçları doğrulanamadı | ○ | Treccani DBI "COSIMO III" (arama özeti) | |
| b66 | c15 | 1723 – 9 Temmuz 1737 | **Gian Gastone: 379 "ruspanti"** (adını, kendilerine verdiği altın sikke "ruspo"dan alırlar); gözde **Giuliano Dami** (çocukken gübre topladığı, 1721'de Duecento Meclisi'ne girdiği) | ◐ | Treccani DBI "GIAN GASTONE I de' Medici" (M. P. Paoli, c. 54, 2000) | Bir LiveJournal ≈370 der (düşük). bD19. |
| b67 | c15 | 1723–1737 | Değerlendirme: Treccani EI (1932) devlet işlerine "kayıtsız" der, ama kısa saltanatı babanın "gevşek ve yıkıcı politikası"ndan sonra bir **onarım** sayar; ekonomi ve kilise politikasındaki önlemler ilk Lorraine reformlarını önceler. Dizionario di Storia (2010) tek reformu üniversite öğretimini Aristotelesçilikten kurtarmak sayar. Wikipedia: yoksullara vergi indirimi, Yahudileri kısıtlayan cezai yasaların kaldırılması (bir blog: kamuya açık idamların sonu) | ◐ (EI + DS) / ○ (vergi, idam) | Treccani EI "GIANGASTONE"; Treccani Dizionario di Storia; EN Wikipedia "Gian Gastone"; Britannica | Britannica: "ne hırsı ne yeteneği vardı". bD20–bD21; bM11. |
| b68 | c15 | 9 Temmuz 1737 | **Gian Gastone ölür**; Treccani: "artık kendi devletinin hükümdarı değildi, devlet Lorraine Dükü Francis Stephen'ın birlikleri tarafından işgal edilmişti" | ◐ | Treccani (Gian Gastone girişleri) | Ölüm yeri/anı bulunamadı. Bir sayfa (Giuliano Dami) "29 Temmuz 1737" yazar: açıklanamadı. Habsburg kaynağı Francis Stephen'ın hükümdarlığını 12 Temmuz 1737'den başlatır (○). |
| b69 | c15/c16 | 1737–1748 | Craon Prensi Marc de Beauvau, Naiplik Konseyi başkanı olarak devleti fiilen yönetir (1737–1748), sonra Richecourt; Francis Stephen Toskana'yı Viyana'dan yönetir, Floransa'ya **yalnızca bir kez**, 1739 başında gelir | ◐ | EN Wikipedia "Marc de Beauvau, 1st Prince of Craon"; habsburger.net "Tuscany as a Habsburg secundogeniture"; Storia di Firenze kronolojisi | |
| b70 | c16 | 1738 | Viyana Antlaşması'yla (1738) Francis Stephen Toskana'nın varisi belirlenir; Britannica 1735 ön düzenlemeyi anar | ◐ | habsburger.net; Britannica "Gian Gastone" | |
| b71 | c16 | 1765, 1786 | Peter Leopold babasının ani ölümüyle (1765) geçer; 1786'da ölüm cezasının kaldırılması, ceza kanunu reformları arasındadır | ◐ | EN Wikipedia "Francis I, Holy Roman Emperor"; unofficialroyalty.com | **Uffizi'nin 1769'da açılması bu aramada doğrulanamadı** (M3 ◐). |

### 3.E c0/c16 — Anna Maria Luisa, Patto, kapanış (1717–bugün)

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| b72 | c16 | 1717 | Anna Maria Luisa dul kalınca Floransa'ya döner; Casciu'ya göre evlilikteki resmî hak feragati iptal edilir, tüm saray ayrıcalıklarına ve muamelesine kavuşur | ◐ | Casciu, "Principessa di gran saviezza" (storiadifirenze.org; arama özeti) | M4 #102. |
| b73 | c0/c16 | Ağustos – 31 Ekim 1737 | Sözleşme taslağı Lorraine'in tam yetkilisi **Craon**'a Ağustos başında Marchese Rinuccini tarafından teslim edilir. **31 Ekim 1737: *Convenzione di famiglia*** imzalanır: **13 madde**, özgünü **Fransızca**, sonra İtalyancaya çevrilip onaylanmış; Elettrice ile yeni büyük dük Francis Stephen arasında; önsöz asıl amacı Toskana'nın yararı olarak gösterir | ◐ | Casciu (storiadifirenze.org); cultura.comune.fi.it "Anna Maria Luisa de' Medici e il Patto di famiglia"; Storia di Firenze kronolojisi; Italia Nostra afişi | **D10.** Italia Nostra afişinde başlık "Convenzione di Famiglia (Vienna 1737)": "Vienna"nın anlamı bilinmiyor. İmzacıların adları (Craon dışında) doğrulanamadı. |
| b74 | c0/c16 | 31 Ekim 1737 | **3. madde:** koleksiyonlar "ebediyen" Floransa kentine ve Toskana Devleti'ne bağlı kalır; gerekçe: devletin süsü, kamunun yararı, yabancıların merakı. İtalyanca çeviri lafzı bD23'te | ◐ | La Nazione; arte.it; finestresullarte.info; Comune di Firenze/Uffizi; Italia Nostra afişi | Uffizi: madde Habsburg–Lorraine'li hükümdarların kentin hazinelerini yağmalamasını hukuken önlemeyi amaçlıyor. |
| b75 | c0/c16 | 31 Ekim 1737 | **Hukukî nitelik tartışması.** Bir akademik özet (storiadifirenze.org; yazarı özetten çıkarılamadı): sözleşme "Lorraine ile Medici arasında quasi-özel bir akit", 3. madde koleksiyonu Floransa'ya/Toskana'ya **bağışlamaz**; Francis Stephen ve ardıllarına mülkiyet geçişinin koşulu olarak devredilemezlik koyar. Comune/Uffizi dili ise "Medici mallarının devlete devri" der | ◐ ("devredilemezlik") / ○ (akademik yorum, tek özet) | storiadifirenze.org (özet); cultura.comune.fi.it; Uffizi | bM13; D11. |
| b76 | c16 | 1738–1743 | Anna Maria Luisa bu yıllarda San Lorenzo kompleksinde geniş mimari ve dekoratif müdahaleler yapar; kubbe ve çan kulesi başlıca projeler | ○ | rivista-incontri.nl makalesi (özet) | Cephe/Cappella dei Principi ayrıntısı bulunamadı. |
| b77 | c0 | ≈1739 → 1743 | Vasiyet ≈1739'da yazılır ve ölümüne dek kodisillerle değiştirilir; mirasçılar akrabalar, hayır ve dinî kurumlar, yoksullar, nedimeler | ○ | il Giornale (kendini varis sayan bir kişiyle ilgili haber; yıl "iki yıl sonra" = 1739) | **Vasiyet metni görülmedi.** Modern talep: "vasiyet bağlayıcı bir uluslararası antlaşmadır" diyen bir "varis" (○). |
| b78 | c0 | 18 Şubat 1743 | **Ölüm: Palazzo Pitti'de, Karnaval döneminde, sabah** ("ruhunu Tanrı'ya teslim etti": İngilizce bir anlatım); 75 yaşında | ◐ (tarih, 75 yaş) / ◐ zayıf (Pitti) | EN Wikipedia "Anna Maria Luisa de' Medici" (infobox: Palazzo Pitti); madamegilflurt.com (soy kaydı tarzı blog); La Nazione, arte.it (tarih) | M4 #107: yer artık ◐ zayıf. **Saat ve tanıklar bulunamadı.** Bir kaynak 17 Şubat (M4). Bir kaynağa göre ölümü Karnaval döneminde Floransa'ya "derin bir karanlık/yas gölgesi" düşürdü (○; ne olduğu ayrıntılandırılmamış). |
| b79 | c0 | Şubat 1743 | Ölümünden kısa süre önce bedeninin ele alınışını yazar: yüzünü ve ellerini yalnız nedimeleri yıkasın, beden açılmasın, hemen gömülsün; "bu olmadı", Medici geleneğiyle organlar çıkarılır | ○ | madamegilflurt.com; thehistoryblog.com | Blog zinciri; birincil metin görülmedi. |
| b80 | c16 | 1743 | San Lorenzo Medici kriptasına (Medici Şapelleri) gömülür | ◐ | EN Wikipedia; Archaeology (2013); La Nazione | M4 #108. |
| b81 | c16 | Aralık 2012 – Şubat 2013 | Medici mezarlarında Anna Maria Luisa'nın kalıntıları açılır (ortak bir proje; Pisa Üniversitesi kaydı arama sonuçlarında): **iç organlar ve ciğerler ayrı bir kapta**; iskelette **frengi izi yok** (söylentiye karşı); 1966 selinde zarar görmüş; ölüm nedeni belirsiz kalır | ◐ | Archaeology (14 Şubat 2013); *Nature* 495:46 (2013); thehistoryblog.com; theflorentine.net; arpi.unipi.it kaydı | Açılış tarihi kaynaklara göre "2012 sonu" / "Şubat 2013". Fornaciari adı özetlerde doğrulanmadı. |
| b82 | c16 | 18 Şubat (her yıl) | Floransa'nın "Elettrice Palatina günü": Palazzo Vecchio'da anma töreni, Floransa Cumhuriyeti Tarihî Alayı kentte yürüyüp Medici Şapelleri'ndeki mezara varır; belediye müzeleri ve Şapeller ücretsiz | ◐ | cultura.comune.fi.it; La Nazione; arte.it; finestresullarte.info | M4 #111'in genişletmesi. |
| b83 | c16 | 31 Ekim (2017 ve sonrası) | Patto yıldönümünde Uffizi'de ücretsiz giriş ve konser; Uffizi'nin "L'eredità di Anna Maria Luisa de' Medici per Firenze" videosu | ○ | finestresullarte.info; libreriamo.it; uffizi.it | Kapanış görseli için. |
| b84 | c16 | 1559 → bugün | **Ottajano (Ottaiano) kolu:** Floransa'dan Napoli'ye geçen Bernardetto de' Medici'nin kolu (soy ağacı kataloğu: "1559'da Napoli'ye aktarılan dal"); Wikipedia prens listesi 19. yy'a (Giuseppe 1843–1894; ardılı Angelica, 11. Prenses) uzanır; "sürmekte olan iki Medici kolundan biri" (diğeri Verona/Caprara–Gavardo) | ○ | EN Wikipedia "Princes of Ottajano", "Bernadetto de' Medici"; maremagnum/inlibris soy ağacı kataloğu | Katalog: kol 1737'de Büyük Dukalık talebinde bulundu, başarısız (○). **D15**: "1920'lerde söndü" iddiasına dayanak yok. |

---

## 4. Canlı ayrıntılar

> **Dürüstlük notu:** Hiçbir birincil metin açılmadı; "kim yazdı / ne zaman" sütunu modern özetin kimliğini ve (biliniyorsa) altındaki çağdaş kaynağı verir. Tırnak içindeki parçalar **arama özetinde tırnak içinde verilen biçimidir** (sayfa açılmadı); **çeviri bize aittir**. Özetleyenin kendi cümlesi olan satırlarda "birebir alıntı" sütunu boş bırakıldı.

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman (olaydan sonra mı?) | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| bD1 | c11 | **Alessandro'nun son gecesi:** vaat edilen buluşma, Lorenzino'nun bahaneyle çıkışı, adamlarını göndermiş Alessandro'nun uykuya dalışı, hizmetkârla dönüş. Kadının kimliği (Soderini Ginori mi, Laudomia mı) ve tetikçinin adı kaynağa göre değişir | Modern özet (Wikipedia, Britannica); altta Varchi (yazım tarihi 1540'lar–1565: HAFIZA) ve *Apologia* | ◐ | — |
| bD2 | c11 | **Parmak ısırma:** Alessandro boğuşmada Lorenzino'nun parmağından bir parça kopardı | Tek özet ("one source says"); ilk anlatıcı belirsiz | ○ ANEKDOT | — |
| bD3 | c12 | **9–10 Ocak 1537, Senato'nun şartı:** Cosimo'ya dük unvanı verilmez | Treccani DBI "COSIMO I" (modern ansiklopedi; arama özeti) | ◐ | IT: *"Il 10 gennaio, dando forma ufficiale alle condizioni poste a C. all'atto dell'elezione, il Senato deliberava che egli non avesse il titolo di duca, ma solo quello di «capo e primario della città»."* → TR: "10 Ocak'ta, seçim anında C.'ye konan koşulları resmî biçime sokarak, Senato onun dük unvanı taşımamasına, yalnızca 'kentin başı ve birincisi' unvanını almasına karar verdi." |
| bD4 | c12 | **Cosimo'yu kimler çağırdı:** Guicciardini çevresindeki optimatlar | Treccani DBI "MEDICI, Raffaello de'" (arama özeti) | ◐ | IT: *"…il M. fu tra gli otto ottimati membri del Senato dei Quarantotto, riuniti intorno a Francesco Guicciardini, che chiamarono a Firenze il giovane Cosimo."* → TR: "…M., Francesco Guicciardini çevresinde toplanan, genç Cosimo'yu Floransa'ya çağıran Kırk Sekizler Senatosu'nun sekiz optimatından biriydi." |
| bD5 | c12 | **Filippo Strozzi'nin sonu:** Montemurlo'da yakalanan Strozzi, Vitelli'nin tuttuğu Fortezza da Basso'da öldü (18 Aralık 1538); intihar mı, öldürülme mi belirsiz | Treccani DBI; Find a Grave; Wikipedia (çeviri aynası) | ◐ (olgu) / ○ (neden) | — |
| bD6 | c12 | **Eleonora'nın gelişi:** denizden, kardeşi Garcia'nın kadırgalarıyla; Livorno'dan Pisa'ya yürürken yolun yarısında Cosimo'yla karşılaşma | Wikipedia "Eleanor of Toledo" ve Italian Art Society (modern; Giambullari'nin 1539 anlatımına dayanması olası: HAFIZA) | ◐ | EN (özet): *"…set sail from Naples, 11 June, accompanied by her brother Garcia with seven galleys following. They arrived at Livorno… on the morning of June 22. That same morning Eleonora left for Pisa and halfway there met Cosimo."* → TR: "…11 Haziran'da Napoli'den denize açıldı; kardeşi Garcia ve yedi kadırga onu izledi. 22 Haziran sabahı Livorno'ya vardılar. Aynı sabah Eleonora Pisa'ya yola çıktı ve yarı yolda Cosimo'yla karşılaştı." |
| bD7 | c12 | **Bronzino portresi:** oğlu Giovanni'yle Eleonora; "hanedanı güvenceye alan" rolü kutlayan, aşırı idealize bir resim. Resimdeki elbise gömü elbisesi **değil** | Smarthistory (modern); gömü elbisesi: bir blog | ◐ (portre) / ○ (elbise) | EN (Smarthistory özeti): *"much-idealized Eleonora in an elaborately decorated and bejeweled dress"* → TR: "büyük ölçüde idealize edilmiş, ayrıntılı işlemeli ve mücevherli bir elbise içindeki Eleonora" |
| bD8 | c12 | **1857 ve Garzia'nın giysisi:** Medici mezarları ilk kez incelendiğinde Garzia kırmızı atlas cekete sarılı bir iskelettir; giysi bugün Uffizi/Pitti koleksiyonundadır | Uffizi koleksiyon sayfası (resmî kurum; 19. yy incelemesinin modern aktarımı) | ◐ | — (Özetleyenin cümlesi: "uno scheletro vestito con un farsetto di raso rosso"; sayfanın birebir cümlesi değil) |
| bD9 | c12 | **Venedik, 26 Şubat 1548:** iki tetikçi Lorenzino'yu amcasıyla yürürken San Polo yakınında pusuya düşürür; amca kaçar, Lorenzino ölür | Dall'Aglio, *The Duke's Assassin* (Yale UP) alıntı sayfası ve History Today (modern akademik) | ◐ | — |
| bD10 | c12 | **Santo Stefano'nun gerekçesi:** Cosimo'nun, yeni devletinin farklı kentlerinin soylularını birleştirecek sembolik bir davaya ihtiyacı vardı | Tek özet | ○ | — |
| bD11 | c13 | **26 Ağustos 1572:** Charles'ın kamu beyanı; "kraliyet" = Catherine okuması | Tek özet | ○ | — |
| bD12 | c13 | **Balet'in uzunluğu:** 5 saati aşan gösteri; Circe temalı; 1582 baskı | Wikipedia; Britannica | ◐ | — |
| bD13 | c13 | **Jeanne d'Albret'in ölümü:** doktorlar akciğer hastalığı teşhis eder; bir kaynak otopsi yapıldığını ve zehir bulunmadığını söyler | Atlas Obscura; Wikipedia (özet) | ○ | — |
| bD14 | c13 | **Rubens'in şartı:** her figürü kendi eliyle yapacak | Wikipedia "Luxembourg Palace" (sözleşmenin İngilizce çevirisi; çevirmen belirsiz) | ○ | EN: *"to make and paint with his own hand each and every one of the figures"* → TR: "(tablolardaki) her bir figürü kendi eliyle yapmak ve boyamak" |
| bD15 | c13 | **Marie'nin Minerva portresi** ve mottosu | Pinakothek/Louvre özetleri (modern) | ◐ | LA: *"Pax optima rerum"* → TR: "Barış, her şeyin en iyisidir" |
| bD16 | c13 | **Reddedilen sahne:** Marie'nin sürgününü yalan bir suçlamanın sonucu gösteren, Calumnia (İftira) ve meşalesiyle simgelenen bir sahne döngüye alınmadı | Pinakothek özeti | ○ | — |
| bD17 | c13 | **Köln'de son:** Haziran 1642'de hastalanır, 3 Temmuz'da plörezi ve yoksulluk içinde ölür; kalıntılar borç yüzünden bir yıl bekletilir (bir kaynak) | Wikipedia; EBSCO; h2g2 (modern) | ◐ (ölüm) / ○ (bekletme) | — |
| bD18 | c15 | **Marguerite Louise'in ayrılışı:** Poggio a Caiano'yu değerli eşyadan soyar | historyofroyalwomen.com (modern) | ○ | — |
| bD19 | c15 | **Ruspanti ve Dami** | Treccani DBI (M. P. Paoli, 2000) | ◐ | IT: *"i suoi 379 «ruspanti», cosiddetti dalle monete d'oro, i «ruspi»"* → TR: "379 'ruspanti'si; adlarını altın sikkeler olan 'ruspi'den alırlardı". IT: *"da ragazzo raccoglieva letame e, divenuto cittadino fiorentino, nel 1721 era entrato nel Consiglio dei duecento"* → TR: "çocukken gübre toplardı; Floransa vatandaşı olunca 1721'de İki Yüzler Meclisi'ne girmişti". |
| bD20 | c15 | **1932'nin hükmü:** Gian Gastone devlete kayıtsız ama saltanatı bir onarım | Treccani EI "Giangastone" (1932) | ◐ | IT: *"…apatico e indifferente alle cure dello stato."* → TR: "devlet işlerine kayıtsız ve ilgisiz". IT: *"…i pochi anni del suo granducato rappresentano, sotto certi aspetti, un restauramento seguito alla fiacca e rovinosa politica paterna. Molti provvedimenti di pubblica economia e politica ecclesiastica preannunziano il grande movimento riformatore dei primi sovrani lorenesi."* → TR: "…kısa büyük dukalığı, bazı bakımlardan babasının gevşek ve yıkıcı politikasının ardından bir onarım dönemidir. Ekonomi ve kilise politikasına ilişkin birçok önlem, ilk Lorraine hükümdarlarının büyük reform hareketini önceden haber verir." |
| bD21 | c15 | **2010'un hükmü:** tek reformu üniversite | Treccani Dizionario di Storia (2010) | ◐ | IT: *"unica sua riforma, l'aver liberato l'insegnamento universitario toscano dai lacci dell'aristotelismo"* → TR: "tek reformu, Toskana üniversite öğretimini Aristotelesçiliğin bağlarından kurtarmasıdır" |
| bD22 | c15 | **Ölürken egemen değildi** | Treccani (Gian Gastone girişi; hangisi olduğu özetten kesin değil) | ◐ | IT: *"G. moriva il 9 luglio 1737; ma non era già più sovrano del suo stato, occupato dalle milizie di Francesco Stefano, duca di Lorena."* → TR: "G. 9 Temmuz 1737'de öldü; ama artık kendi devletinin hükümdarı değildi; devlet, Lorraine Dükü Francis Stephen'ın birliklerince işgal edilmişti." |
| bD23 | c0/c16 | **Patto, 3. madde lafzı** (İtalyanca çeviri biçimi) | Aktaran: La Nazione, arte.it, finestresullarte, Comune di Firenze/Uffizi (2017–2024 modern sayfalar; hangisinin hangi varyantı taşıdığı özetten kesinleşmedi); özgün 1737 Fransızca, görülmedi | ◐ (çeviri lafzı) / ○ (noktalama, büyük harf, "Gioje/Gioie") | IT (1): *"per ornamento dello Stato, per utilità del Pubblico e per attirare la curiosità dei Forestieri"* → TR: "devletin süsü için, kamunun yararı için ve yabancıların merakını çekmek için". IT (2, Comune/Uffizi): *"…per ornamento dello Stato, e per utilità del Pubblico, e per attirare la curiosità dei Forestieri"*. IT (kapsam): *"o levare fuori della Capitale e dello Stato del Granducato, Gallerie, Quadri, Statue, Biblioteche, Gioje ed altre cose preziose"* → TR: "…başkentin ve Büyük Dukalık Devleti'nin dışına çıkarmak: Galeriler, Tablolar, Heykeller, Kütüphaneler, Mücevherler ve diğer kıymetli şeyler" (başka bir aktarım "siccome le Sante Reliquie e Reliquiari" ekler: "Kutsal Emanetler ve Emanet Kutuları gibi") |
| bD24 | c0/c16 | **Patto'nun dili ve künyesi** | Italia Nostra afişi (2017); Comune di Firenze/Casciu | ◐ | IT: *"Convenzione di Famiglia (Vienna 1737) - Articolo III - Traduzione in italiano dell'originale in francese."* → TR: "Aile Sözleşmesi (Viyana 1737) – Madde III – Fransızca özgününden İtalyanca çeviri." IT: *"Nei suoi tredici articoli redatti nell'originale in francese"* → TR: "Fransızca özgün olarak kaleme alınmış on üç maddesinde" |
| bD25 | c16 | **1717 dönüşü ve hakların iadesi:** evlilikteki resmî feragat iptal edilir | Casciu (storiadifirenze.org; arama özeti) | ◐ | — |
| bD26 | c0 | **Ölüm sabahı ve talimat:** Karnaval günlerinde, sabah; yüzünü ve ellerini yalnız nedimeleri yıkasın, beden açılmasın | madamegilflurt.com; thehistoryblog.com (modern bloglar; birincil kaynak belirtilmemiş) | ○ | EN (özet): *"rendered her soul to God"* → TR: "ruhunu Tanrı'ya teslim etti" |
| bD27 | c16 | **2012/13 mezar açımı:** iç organlar ve ciğerler ayrı kapta; frengi izi yok | Archaeology (2013), *Nature* 495:46 (2013) haberleri (modern, olaydan 270 yıl sonra) | ◐ | — |
| bD28 | c15 | **Mustafa Ağa'nın Floransa'sı (1598)** | Mercan 2023 (*Annali ISIG Trento*; özet) | ◐ | EN: *"Besides delivering the official letters of Sultan Mehmed III and Grand Admiral Halil Pasha concerning Grand Duke Ferdinando I de' Medici's request for friendship and privileges, Mustafa Agha also conducted diplomatic negotiations with the Grand Duke and attended some courtly ceremonies in the Medici palaces."* → TR: "Mustafa Ağa, Sultan III. Mehmed'in ve Kaptan-ı Derya Halil Paşa'nın, Büyük Dük I. Ferdinando'nun dostluk ve imtiyaz talebine ilişkin resmî mektuplarını teslim etmenin yanı sıra Büyük Dük'le diplomatik müzakereler yürüttü ve Medici saraylarındaki bazı saray törenlerine katıldı." |
| bD29 | c15 | **Livornina'nın hitap listesi** | Christie's müzayede kaydı (satıcı betimi; metnin kendisi değil) | ○ | EN: *"Addressed to 'Levantines', Spaniards, Portuguese, Greeks, Germans, Italians, 'Hebrews', Turks, Moors, Armenians, Persians and others"* → TR: "'Levantenler', İspanyollar, Portekizliler, Rumlar, Almanlar, İtalyanlar, 'İbraniler', Türkler, Moorlar, Ermeniler, Persler ve diğerlerine hitaben" |
| bD30 | c15 | **Fahreddin'e sığınma güvencesi (1608)** | Aramco World (2014; modern) | ◐ | EN (makale ifadesi, özet): *"it included a provision assuring Fakhr al-Din asylum at the house of de' Medici should Istanbul come to object too strongly"* → TR: "İstanbul fazla itiraz ederse Fahreddin'e Medici'nin evinde sığınma güvencesi veren bir madde içeriyordu" |
| bD31 | c13 | **Catherine'in "nedimeleri"ne hiciv (1584):** en eski düşmanca betimleme | ANU (McIlvenna) bölümünün başlığı ve özeti | ○ | EN (başlık): *"A Stable of Whores?"* → senaryoda **birebir kullanılmaz** (USLUP §2-7); dolaylı: "düşmanları sarayını bir tür ahır gibi hicvetti" |

---

## 5. Sayılar ve ölçüler, mit/tartışma, TR-BAĞ

### 5.1 Sayılar ve ölçüler

> Aralık ve çelişki varsa **hepsi** yazıldı. "Hesap bize ait" = tarihlerden bizim çıkardığımız sayı.

| Konu | Değer(ler) | Kaynak / çelişki | Sınıf |
|---|---|---|---|
| Cosimo'nun seçildiği yaş | 17 | Wikipedia (M4: 17 yıl 6 ay 27 gün, hesap; doğum tarihi HAFIZA) | ◐ |
| Cosimo'nun egemenlik süresi | 1537–1574 ≈ 37 yıl (hesap) | b5, b29 | ◐ |
| Montemurlo | 31 Temmuz / 1 / 2 Ağustos 1537 | Kaynaklar çelişir | ◐ / ○ |
| Eleonora'nın evlilik yaşı | 17 | Italian Art Society | ◐ |
| Eleonora'nın yolculuğu | 11 → 22 Haziran 1539 = 11 gün (hesap); yedi kadırga | Italian Art Society; Wikipedia | ◐ |
| Evlilik takvimi | 29 Mart (vekâlet) → 29 Haziran (giriş) → 29 Temmuz (düğün) | b10–b12 | ◐ |
| Siena kuşatması | ≈15 ay (Ocak 1554 – Nisan 1555) | historyofwar.org; başlangıç 1553/1554 çelişir | ◐ |
| Siena'nın devri | 3 Temmuz (fief), 19 Temmuz 1557 (teslim) | Tek özet | ○ |
| 1562 ölümleri | Giovanni 19 yaşında (20 Kasım), Garzia 15–16 yaşında (6 veya 12 Aralık), Eleonora (17 Aralık); ilk ölümden sonuncuya 27 gün (hesap bize ait) | Wikipedia; Uffizi | ◐ |
| Büyük Dük: bulla → taç | 27 Ağustos 1569 → 5 Mart 1570 ≈ 6 ay 6 gün (hesap) | Treccani; Wikipedia | ◐ |
| İmparatorluk tanıması | 2 Kasım 1575 (veya 1576); 100.000 duka tazminat | Çelişir; tek özet | ○ |
| Lepanto | 12 Toskana kadırgası / ≈200; 100+ Santo Stefano şövalyesi | finestresullarte/Wikipedia özetleri | ◐ (12) / ○ (100+) |
| Kutsal Birlik filosu | 206–207 kadırga (+6 galeas) | Kaynaklara göre değişir | ◐ |
| Barbaros 1544 | ≈6.000 esir | Tek özet | ○ |
| Bona 1607 | 470 ölü, 1.500 esir | Bir anlatım | ○ |
| Sakız 1599 | 2.000 kişi, 5 gemi; Floransa kaybı ≈400; Osmanlı ≈10.000 | Wikipedia (tek) | ○ |
| Marie'nin çeyizi | 600.000 écu (scudo); ek yıllık 20.000; borç "bir milyona yakın" | herodote.net; Britannica; tek kaynaklar | ◐ (600.000) / ○ |
| Marie'nin ömrü | 1575 → 3 Temmuz 1642 ≈ 67 yaş (hesap; 1573 doğumla 69) | Kaynaklar çelişir | ◐ |
| Rubens döngüsü | 2 sözleşme (26 Şubat 1622); 24 = 21 + 3; 1625; Louvre'a 1816; Galerie Médicis 1993 | Wikipedia; Louvre; Morgan | ◐ |
| Ferdinando I | 13 yaşında kardinal (1562); hükümdarlık 19 Ekim 1587 – 17 Şubat 1609 ≈ 21 yıl 4 ay (hesap) | Tek özet (bitiş) | ◐ / ○ |
| Livornina | 1 Temmuz 1591 (taslak) → 10 Haziran 1593; beş kişilik topluluk konseyi | Wikipedia; sephardicgenealogy | ◐ / ○ |
| Fahreddin | 1608 antlaşma → 1613 sürgün → 1618 dönüş (5 yıl) → 1635; ≈100 kişi, 3 gemi | Aramco; journals.ku.edu | ◐ / ○ |
| Cosimo III | 53 yıl; Aralık 1674 / Haziran 1675; 80.000 livre; faiz −0,75 puan | Wikipedia hattı | ○ |
| Toskana nüfusu | 720.594 (1670) | Wikipedia (tek) | ○ |
| Gian Gastone | 379 ruspanti (DBI); ≈370 (LiveJournal) | Çelişir | ◐ / ○ |
| Patto | 13 madde; 3. madde; 31 Ekim 1737; Craon 1737–48; Francis Stephen Floransa'ya 1 kez (1739) | Casciu; Comune; habsburger.net | ◐ |
| Anna Maria Luisa | 1717 dönüş; 1738–43 San Lorenzo işleri; ≈1739 vasiyet; ölümden 270 yıl sonra mezar açımı (2012/13) | Çeşitli | ◐ / ○ |
| Hanedan sonu | 9 Temmuz 1737 (Gian Gastone) → 18 Şubat 1743 (AML) = 5 yıl 7 ay (M4) | Treccani; Wikipedia | ◐ |
| **HAFIZA'da kalanlar** | Catherine'in 10 çocuğu; Aziz Bartolomeo ölü sayıları; Cosimo II'nin ölüm nedeni; Floransa şehir nüfusu | Aranmadı / bulunamadı | HAFIZA |

### 5.2 Mit/tartışma (İddia → Kim ne diyor → Değerlendirme)

#### bM1 — "Cosimo oğlunu öldürdü" (Garzia, Giovanni, 1562)  **[◐ mit; olgu ◐ sıtma]**
- **İddia:** Garzia (15–16) avda kardeşi Giovanni'yi (19) bıçakladı; babası Cosimo, Garzia'yı kılıçla deldi; Eleonora yasa dayanamadı.
- **Kim ne diyor:** Efsanenin bu "aile" biçimi Bob Brier'in popüler kitabında aktarılır (özet). Wikipedia: efsane ölümlerden **yüzyıllar sonra** doğdu; 1857'de cesetler ilk kez incelendiğinde şiddet izi bulunmadı, ikisinin de sıtmadan öldüğü sonucuna varıldı. **Uffizi (resmî site):** Garzia 1562'de ailesiyle yaptığı kıyı gezisinde sıtmaya yakalanıp öldü. 2026'da Yale–Pisa ekibi (basın: archaeologymag, Yale, CNN, Science) "iki kardeş"in kaburgalarından *Plasmodium* DNA'sı bildirdi (D16). **Efsanenin ilk yazanı bulunamadı** (M4'ün Pieraccini 1924–25 anısı sınanmadı).
- **Değerlendirme:** Olgu: üç kişi birkaç hafta içinde, aynı seyahatin ardından, sıtma tablosuyla öldü (◐). "Cosimo katildi" yalnız "rivayet; ilk kaynak bilinmiyor; belge yok" kipinde. Mizah kapalı.

#### bM2 — Eleonora ve "portredeki elbisesiyle gömülmesi"  **[○]**
- Bronzino portresindeki elbise bir dönem Eleonora'nın gömü elbisesi sanıldı; yeni araştırmalar gömü elbisesinin **başka bir elbise** olduğunu, Pitti'de korunduğunu söyler (özet). Bir blog, ölüm anında elbiseyi giydirenlerin bulaş korkusuyla düzgün bağlamadığını yazar (○). M4 §3.C #3'teki "1857'de bulunan elbise" iddiası doğrulanmadı; 1857 tarihi yalnız Garzia'nın giysisi için görüldü (b24).
- **Değerlendirme:** "Gömü elbisesi bugün Pitti'de" demek için sayfa açılmalı.

#### bM3 — Lorenzino: Brutus mu, intikam mı? Ve 1548'de emri Cosimo mu verdi?  **[◐ çatışan okumalar]**
- **Eylem:** *Apologia* siyasi gerekçe ve Brutus; Varchi de Brutus benzetmesini yapar; Treccani EI "özel intikam"; Wikipedia kıskançlık/miras gibi hipotezleri sayar; Warburg belgesi Varchi anlatısının birçok noktada kesin yanlış olduğunu söyler.
- **1548:** Geleneksel görüş: emri Cosimo verdi. Dall'Aglio (Yale UP): Floransa Devlet Arşivi'ndeki şifreli mektuplar, Cosimo'nun Venedik'teki adamlarının işin içinde olduğundan kuşku doğurdu; tetikçiler yakalanmadı.
- **Değerlendirme:** Senaryo "Cosimo'nun emriyle öldürüldüğü uzun süre kabul edildi; yeni bir çalışma buna kuşku düşürüyor" diyebilir. M4'ün "Cosimo'nun menzili" yorumu bu nedenle **kesin kipten çıkarıldı**.

#### bM4 — Alessandro'nun babası ve annesi  **[○]**
- **Kim ne diyor:** Resmen Lorenzo di Piero (Urbino Dükü); popüler baba Giulio (VII. Clemens). Wikipedia "Simonetta": doğrulanmadı, "modern tarihçiler çoğunlukla ilk teoriyi tercih eder" (özet); History.co.uk: "birçok tarihçi Giulio'nun oğlu olduğuna inanır"; V&A katalog kaydı Giulio'yu kesin yazar (müze kaydı, akademik değil). Anne: Simonetta belgelerde Alfonsina Orsini'nin hizmetçisi; serbest, köylü kökenli; Afrika kökenine kanıt yok; "Moorish slave" hikâyesi Jean Nestor (1560) → Spini: temelsiz. Popüler yazılar köle/Afrikalı iddiasını tekrarlar. Catherine Fletcher'ın *The Black Prince of Florence* (2016) ve Literary Hub yazısı tartışmanın başvuru noktalarıdır (**içerikleri okunmadı**). DNA çalışması yok.
- **Değerlendirme:** "Kökeni tartışmalı; iki baba hipotezi; annenin statüsü kaynaklarda farklı" yeter. Ten rengi/köken üzerinden alay yok.

#### bM5 — Cosimo'nun unvanları  **[◐]**
- 10 Ocak 1537 "kentin başı ve birincisi" → Eylül 1537 "dük" olarak anılma (○) → 27 Ağustos 1569 Büyük Dük bullası → 5 Mart 1570 Roma'da taç → 2 Kasım 1575 imparatorluk diploması (○) ve 100.000 duka (○). **YORUM:** "kentin birincisi" → Roma'nın verdiği taç → Viyana'nın pahalı onayı: M4 §3.C #7'deki ironi artık kaynaklı.

#### bM6 — Santo Stefano: haçlı tarikatı mı, ganimet şirketi mi?  **[○ / YORUM]**
- Kaynaklar: amaç Osmanlı/korsan ticaretini vurmak ve esirleri kurtarmak; ganimet satışı Livorno'yu zenginleştirdi. Wikipedia (Sakız maddesi): tarikat Osmanlı korsanlarını izleme görevini "kötüye kullandı" (tek, taraflı ifade; ○). Küre Ansiklopedi (Türkçe): tarikat Osmanlı'yla sorun çıkardı ama siyasi krize dönüşmedi, ticaret sürdü (○). **YORUM:** "dinî çerçeve + ticari ganimet" birlikte okunabilir.

#### bM7 — Catherine ve 1572: sorumluluk  **[◐ kısmen]**
- **Geleneksel görüş:** Britannica (olay maddesi) Catherine'in planladığını yazar. **Daha nüanslı:** Britannica (biyografi maddesi): Coligny'nin ve başlıca yandaşlarının öldürülmesini onayladı, büyük olasılıkla sonrasındaki **katliamı** değil. **Knecht:** EHR incelemesine göre Catherine'i aklamaya daha az yatkın; History Today'de "son dönem aklama çabası suçlu kanı örtmeye yetmedi" diye özetlenen bir tez (özet, paraphrase). **Jouanna** (*French History* incelemesi): "Catherine azmettirdi" varsayımını reddeder, sorumluluğu kralın konseyine yükler. **Hollingsworth** (History Today incelemesi): Catherine hoşgörü ve uzlaşma arayan kurnaz bir figür. Coligny girişimi: Guise (en olası ama kanıtlanamaz), Alba ya da Catherine; 23 Ağustos konseyi; 26 Ağustos kral beyanı (○).
- **Doğrulanamayanlar:** Holt, Frieda, Sutherland, Crouzet, Diefendorf (HAFIZA'da kalır).
- **Değerlendirme:** "Tarihçiler Catherine'in Coligny'nin öldürülmesini onayladığında hemfikir sayılabilir; sonrasındaki katliamdan ne ölçüde sorumlu olduğunda ayrılırlar" kalıbı (◐). Tek bir tarihçi adı kesin tutum olarak verilmeden önce kitap açılmalı.

#### bM8 — IX. Charles'ın "hepsini öldürün" sözü  **[○ ANEKDOT]**
- Fransız basınında "Tuez-les tous…" kalıbı dolaşır (kaynaksız); İngilizce yazında "eski bir gelenek Charles'ın 'Kill them all' dediğini söyler"; Wikipedia: 23 Ağustos'ta böyle dediği "söylenir". Birincil zincir **kurulamadı**; Tavannes'ın *Mémoires*'ı (oğul tarafından yazılıp yayımlanmış: HAFIZA) güvenilirlik sorunuyla anılır (J.-L. Bourgeon, *BSHPF* 1996: "Les 'Mémoires' de Tavannes et la Saint-Barthélemy : mode d'emploi"; başlığı bile bir kullanım uyarısıdır).
- **Değerlendirme:** "Charles'a şu söz atfedilir" + tırnaksız; birebir söz yazılmaz (USLUP §2-3).

#### bM9 — Catherine mitleri  **[tablo]**

| Mit | Anlatı | Değerlendirme | Sınıf |
|---|---|---|---|
| Çatal | Catherine çatalı Fransa'ya getirdi | Çatal İtalya'da zaten kullanılıyordu; Catherine'in kullanımı çevresinde yayılmasını teşvik etmiş olabilir (Cooks Info). Çağdaş kanıt görülmedi | ○ (büyük olasılıkla abartı) |
| Dondurma/sorbe | Floransalı aşçılar 1533'te dondurmayı getirdi | Liddell–Weir: hikâyeleri destekleyen tarihsel kanıt yok; hikâyeler 19. yy dondurmacı ve satıcılarının icadı. Colonial Williamsburg: 1533'te İtalyan aşçılar sıvıları yapay dondurmayı henüz bilmiyordu; bilinen en eski Fransızca dondurma tarifinden 150 yıldan fazla önce. Cooks Info: Catherine'e atfetme 1800'lerin ortasında başlar. Elizabeth David (alıntı; ○): Catherine Floransa'dan ayrılırken tüm hanesi Fransızdı | ◐ **mit** |
| Parfüm | René le Florentin ile Fransız parfümcülüğü başladı | Bianchi gerçek ve resmî parfümcü (≥1547; b37); "Fransa'ya parfüm getirdi" iddiası blog düzeyinde | ○ |
| Zehir | Zehirli eldivenler (Jeanne d'Albret, 1572) | 16.–17. yy anlatılarında geçer ama kanıt yok; Jeanne ≈10 hafta önce, akciğer hastalığından öldü; otopsi bulgusu tek kaynakta; mezhepsel anlatı; "İtalyan" kimliği suçlamayı kolaylaştırdı | ◐ **mit** |
| Escadron volant | Nedimeleriyle casusluk/baştan çıkarma | Terim 1695 anonim *Les amours de Henri IV*'de (Brantôme'a atfı yanlış: bir Fransız kaynak; başka bir kaynak Brantôme'da kökleri görür, çelişir). McIlvenna (Routledge 2016) bunun indirgemeci ve kadın düşmanı bir fantezi olduğunu savunur (özetin ifadesi). Belgeli örnekler: Charlotte de Sauve–Navarre'lı Henri (1572); Isabelle de Limeuil–Condé (1562). 1577 Chenonceau balosu tek anlatıya dayanır | ◐ **mit** |
| Gerçek katkılar | *Balet comique de la reine* (1581), saray şenlik kültürü | b38 | ◐ |

#### bM10 — Rubens döngüsü bir "aklama" mı?  **[◐ / YORUM]**
- Pinakothek/Louvre/Morgan özetleri: amaç Marie'nin geçmişini aklamak ve itibarını geri kazanmak; Rubens'ten tartışmalı siyasi etkisini olumlu göstermesi istendi; yoğun klasik alegori güvenlik gereğiydi (özetin yorumu). Bir tez özeti döngünün "kasıtlı belirsiz" olduğunu savunur; Büttner'in Corpus Rubenianum XIV cildi alegorinin işleyişini merkeze alır.
- **YORUM:** Sipariş sahibi 1631'den sonra kaçarken tabloların Luxembourg'da asılı kalması ve bugün Louvre'da ayrı bir galeride toplanması, "imge siyaseti"nin ömrünün siyasetten uzun olduğunu gösterir.

#### bM11 — Gian Gastone anekdotlarının güvenilirliği  **[◐ / ANEKDOT]**
- Treccani DBI (2000) ruspanti/Dami'yi (379) anlatır (modern, ansiklopedik); EI (1932) "kayıtsız ama onarıcı"; DS (2010) "tek reform: üniversite"; Britannica "ne hırsı ne yeteneği vardı". LiveJournal (≈370 ruspanti, pis yatak odası, mesane taşı): düşük, kaynak zinciri yok. Acton (1932) bu turda görülmedi.
- **Değerlendirme:** ruspanti/Dami ◐; yatak/pis oda/hastalık ayrıntıları ANEKDOT; mizah kapalı.

#### bM12 — "Cosimo III batırdı" anlatısı tek yönlü mü?  **[○ / YORUM]**
- Wikipedia: gerileme Ferdinando II'de başlar, Cosimo III kötüleştirir (hazine, takas); bir akademik özet: yün geriler, ipek gelişir; Altopascio çalışması: kriz Floransa'da hoşnutsuzluk yarattı ama hükümdara ciddi meydan okumadı. "Çöküş" dili tek bir kaynak hattına dayanıyor; nüans: sektörel ayrışma. Nüfus rakamı tek (1670).

#### bM13 — Patto bağış mı, şartlı devir mi?  **[◐ / ○]**
- Comune/Uffizi: "Medici mallarının devlete devri" ve "ebediyen bağlı"; akademik özet (storiadifirenze.org): 3. madde bağışlamaz, mülkiyeti Francis Stephen ve ardıllarına geçirirken devredilemezlik koşulu koyar, sözleşme "quasi-özel"; bir başka kaynak: "gerçek bir unvan devri olmadan" Toskana'ya bağladı, çünkü koleksiyon Devlet'in elinde kaldı.
- **Değerlendirme:** Senaryo "Floransa'da kalacak/dışarı çıkarılamayacak" (◐) der, "bağışladı" demez.

#### bM14 — Patto'nun lafzı  **[◐ çeviri; ○ Fransızca]**
- bD23–bD24. Özgün Fransızca; "Vienna 1737" etiketi; İtalyanca çevirinin tarihi/çevirmeni bilinmiyor. Tırnakla verilecekse "İtalyanca çevirisinden" kaydı ve "çeviri bize aittir"; en güvenlisi sözü dolaylı vermek (USLUP §5-A kalıbı).

#### bM15 — Anna Maria Luisa'nın ölümü ve "frengi" söylentisi  **[◐]**
- Mezar açımı (2012/13): frengi izi yok; ölüm nedeni belirsiz (Archaeology, *Nature*, History Blog); organlar ayrı kapta; talimatın "ihlali" (blog; ○). Senaryo: "ölüm nedeni bugün de bilinmiyor" (◐); "yaşlılıktan" demek kaynaksız.

#### bM16 — X. Leo'nun "papalığı verdi" sözü (güncelleme)  **[○ ANEKDOT]**
- İkinci aramada Giorgi'nin *relazione*si de, Alberi'nin derlemesi de **çıkmadı**. Çıkanlar: IT Wikiquote (yanlış atıf kategorisi; Bembo mektubu ve Bale'e gönderme: M4 §5.1–5.2'de uyarıldığı gibi iki sözün karışması olası); Jimmy Akin: "seçilişinde söylendiği söylenir (kanıtlanmış değil)"; HSP dijital kütüphane kaydı (içerik okunmadı). Sonuç: ○ bırakıldı; senaryoya girmez ya da "…diye aktarılır" + "kaynağı bir Venedik elçisi raporu ama bu raporun metni bu turda görülmedi" kipinde. Giorgi'nin metninin olası yeri (HAFIZA): Alberi'nin Venedik elçileri raporları derlemesi.

#### bM17 — Gerçekten "son" mu?  **[○]**
- D15. Toskana'yı yöneten hat 1737'de (erkek) / 1743'te (son üye) bitti (◐); Ottajano kolu sürer (Wikipedia, ○); 1737'de Büyük Dukalık talep etti, başarısız (katalog, ○). "Son Medici" ifadesi dar anlamda doğru.

### 5.3 TR-BAĞ (dönem: Cosimo I → Cosimo II; M4 §6'nın devamı)

> M4 T1–T13 satırlarının durumu §2.D'de. Aşağıdaki T14–T28 yeni ya da genişletilmiş satırlardır. **Cosimo I'in Osmanlı ile doğrudan diplomasisine kaynak bulunamadı (T18).**

| # | Bölüm | Olgu | Sınıf | Not / doğrulama |
|---|---|---|---|---|
| T14 | c12 | **Barbaros'un 1544 Toskana kıyı baskını:** Porto Ercole, Giglio, Talamone, Lipari; ≈6.000 esir | ○ | b13. Cosimo'nun toprağı mıydı? Özetlerde belirtilmedi. |
| T15 | c12 | **1548 Cosmopoli; 1553 Fransız–Osmanlı seferi:** Osmanlı filosu Fransız birliklerini Sienalı Maremma'dan Korsika'ya taşır; Dragut Elba'yı yağmalar, Portoferraio surları dayanır | ○ | b14, b17. M4 T4 "1552–55" → **1553**. Siena'nın 1552 ayaklanması/Fransız himayesi bu turda sınanmadı. |
| T16 | c12 | **Santo Stefano Şövalyeleri:** onay 1 Ekim 1561, tören 15 Mart 1562; amaç Osmanlı ve korsan deniz taşımacılığı; üs Livorno; 1563 Oran, 1564 ilk saldırı | ◐ | b21–b22. Küre Ansiklopedi (Türkçe): Osmanlı'yla sorun çıkardı ama siyasi krize dönüşmedi, ticaret sürdü (○). Esir bagno'su aramada çıkmadı. |
| T17 | c12 | **Lepanto 1571:** 12 Toskana kadırgası (≈200 içinde); papalık hizmetinde sayılır; 100+ Santo Stefano şövalyesi (○) | ◐ | b28. Komutan ve gemi adları sınanmadı. Osmanlı tarafı için Türkçe kaynak ayrı aranmalı. |
| T18 | c12 | **Cosimo I–Osmanlı doğrudan diplomasisi: kaynak bulunamadı.** Mercan'a göre Floransa'nın Porte'ye iki diplomatik girişimi 16. yy'ın ikinci yarısında vardır (1574–78, 1598); ticaret ayrıcalıkları Mehmed II'den başlar ve II. Bayezid (1488, 1499), I. Selim (1513), I. Süleyman (1527) ile yenilenir | ○ | **YORUM:** Cosimo dönemi için resmî heyet kanıtı yok. Ayrıcalık yenilemeleri tek bölüm özetinde (○). |
| T19 | c12/c15 | **1574–78 (Francesco I):** Florentine tekstil üreticileri/tüccarlar Porte ile teması yeniden kurmak için ısrar eder (yün sanayii durgun); **Venedik** başlıca engeldir (Floransalıların Venedik yünlüsünü taklit etmesine karşı); Francesco, yurtdışına yazdığı mektuplarda Osmanlı hükümdarlarıyla ilişkisi olmadığını yinelemiştir (özetin ifadesi); elçi **Bongianni Gianfigliazzi** (bir özet) | ◐ (genel) / ○ (Gianfigliazzi) | Mercan 2016 (MAP cilt 3, Brepols, s. 19–31) ve *Mediterranean Historical Review* 2020 ("A diplomacy woven with textiles"). Gianfigliazzi ikinci aramada **doğrulanamadı**. |
| T20 | c15 | **Livornina 1591/1593 ve Doğu ticareti:** Sefarad tüccarlardan Osmanlı Levant'ına erişim beklentisi; Yunanistan ve Osmanlı topraklarından yerleşimci devşirme; hitap listesi (Türkler, Rumlar, Ermeniler, Persler) | ◐ / ○ | b53, bD29. Rum/Ermeni tüccarların Livorno'daki fiilî rolü bulunamadı. Kaborycha ve Tazzara çalışmaları ipucu. |
| T21 | c15 | **1598:** Neri Giraldi'nin Sultan'a elçiliği; Osmanlı elçisi Mustafa Ağa'nın Floransa'da ağırlanması (III. Mehmed ve Kaptan-ı Derya Halil Paşa'nın mektuplarıyla); müzakere başarısızlıkla biter | ◐ | b54, bD28. Başarısızlığın nedeni özetlerde yok. |
| T22 | c15 | **1599 Sakız seferi** | ○ | b55. |
| T23 | c15 | **1607 Halep isyancısıyla antlaşma;** Altoni'nin Suriye gezisi | ○ | b57. İsyancının adı (Canpulatoğlu Ali Paşa: HAFIZA) doğrulanmalı. |
| T24 | c15 | **Bona 1607; Prevesa; Sala di Bona** (Pitti, 1607–09) | ◐ / ○ | b56. Pitti'deki fresk, Türk izleyici için ziyaret edilebilir bir "Osmanlı–Medici" kanıtı: görsel kaynak adayı. |
| T25 | c15 | **Fahreddin II:** 1608 antlaşma (Ferdinando I), 1613 sürgün (Cosimo II dönemi), 1618 dönüş, 1635 idam (IV. Murad) | ◐ | b58–b59. Osmanlı kaynakları (Maanoğulları) ile birlikte okunmalı. |
| T26 | c15 | **Ferdinando I'in genel Osmanlı siyaseti:** "ikircikli" (Mercan 2025, *The Mediterranean in Florence*, Giunti, bölüm başlığı: "An Ambivalent Attitude Towards the East"); Kıbrıs'ı geri alma ve Kutsal Topraklar tasarıları; Rudolf II'ye destek; Halep ile ticaret | ◐ (başlık) / ○ (içerik, Wikipedia özeti) | Mercan bölümü okunmadı. |
| T27 | c15 | **Uzun Savaş (1593–1606):** Toskana birlikleri Habsburglara yardım eder; Macaristan'ın savunması Livorno–Pisa ticaret çıkarlarına bağlanır | ○ | Wikipedia özeti; M4 T13 "HAFIZA (düşük)" → ○. |
| T28 | — | **Türkçe/akademik başlangıç noktaları:** Küre Ansiklopedi "Toskana"; Özden Mercan (Hacettepe) yayınları; *Tarih Araştırmaları Dergisi* 35/59 (2016): "Osmanlıya karşı İranla ittifak: 16. yüzyılın siyasi ve iktisadi rekabet ortamında Avrupa'nın müttefik arayışları"; Joseph M. Silva (Santo Stefano) ve Corey Tazzara (Livorno 1676 serbest liman) | — | Hiçbiri açılmadı; okuma listesi. |

---

## 6. Sahne adayları

> **Ortak uyarı:** Üç sahne için de **saat saat birincil akış çıkarılamadı.** "Çerçeve" yalnız ◐/○ düzeyindeki olguları taşır. Mizah A ve B'de **kapalıdır**; C'de yalnız kuruma/kibre.

### Sahne A — Alessandro'nun öldürülmesi (5–6 Ocak 1537) ve Cosimo'nun gelişi

- **Çerçeve (◐):** Gece 5–6 Ocak 1537 (Britannica: akşam). Lorenzino, kuzenini kendi dairesine bir buluşma vaadiyle çeker (kadın: çoğunluğa göre Caterina Soderini Ginori; bazılarına göre Laudomia); bahaneyle odadan çıkar; adamlarını göndermiş Alessandro uyuyakalır; Lorenzino hizmetkâr "Scoronconcolo" ile döner; kılıç ve hançerle öldürürler; Alessandro direnir (parmak ısırma: ANEKDOT ○). Lorenzino *Apologia*'sında Brutus'a başvurur; Treccani bunu özel intikam sayar. 9 Ocak'ta Kırk Sekizler Senatosu, Guicciardini çevresinin çağırdığı Cosimo'yu (17) seçer; 10 Ocak'ta şart: dük değil, "kentin başı ve birincisi". Vitelli (Fortezza da Basso) destekler.
- **Saat akışı:** **Yok.** Varchi'nin anlatısı bir Warburg belgesinde "birçok yönüyle kesin yanlış" bulunur (○). "Şafak", "mum", "perde" gibi sözcükler doğrulanana dek kullanılmamalı (M4 sahne C'deki "perdeye sarılıp saklanan ceset" HAFIZA'dır, bu turda çıkmadı).
- **Kişiler:** Alessandro, Lorenzino, "Scoronconcolo", kadın (isimsiz kullan), Francesco Guicciardini, Alessandro Vitelli, Cosimo (Mugello'da yetişmiş, Floransa'da pek tanınmayan biri: Wikipedia özeti), Kardinal Cibo (rolü bulunamadı).
- **Belgelenmiş sözler:** Tırnaklık söz **yok**.
- **Belirsiz noktalar:** Kadının kimliği; tetikçinin adı; motif (Brutus mu, kıskançlık/miras mı); ölümün kaç gün gizlendiği; Floransa'nın neden ayaklanmadığı.
- **Zweig'ci iskelet:** tuzak (vaat) → bekleyiş → uyku → dönüş → kısa cümlelerle olay → sessizlik → bir sonraki sabahın boşluğu → 9–10 Ocak: Senato, genç Cosimo'ya dük unvanı vermemeyi kararlaştırır (bD3). **Dramatik ironi:** "kentin başı ve birincisi"nin 33 yıl sonra Roma'da tacı giyecek olması (b26–b27; hesap bize ait).
- **Ton:** mizah kapalı; kurbana alay yok; kökeni/ten rengi üzerinden kaba söz yok (bM4).

### Sahne B — Kapanış: 18 Şubat 1743 (ve aynalı sahne 31 Ekim 1737)

- **Çerçeve (◐):** 9 Temmuz 1737 Gian Gastone ölür (devlet zaten Francis Stephen'ın birliklerinin elindedir); Ağustos başında taslak Craon'a teslim edilir; **31 Ekim 1737** 13 maddelik, Fransızca yazılmış sözleşme imzalanır; 3. madde: koleksiyonlar "ebediyen" Floransa'ya ve Toskana Devleti'ne bağlı; gerekçe devletin süsü, kamunun yararı, yabancıların merakı (IT çeviri lafzı bD23). Anna Maria Luisa 1717'den beri Floransa'dadır; 1738–43 San Lorenzo'da kubbe ve çan kulesiyle uğraşır; ≈1739'da vasiyet yazar, kodisillerle değiştirir. **18 Şubat 1743**, Karnaval günlerinde, sabah, Palazzo Pitti'de (◐ zayıf) 75 yaşında ölür; bir kaynağa göre ölümü Floransa'ya yas gölgesi düşürür (○); talimatı (yüz ve eller; açılmasın) yerine getirilmez (○). San Lorenzo kriptasına gömülür. 270 yıl sonra mezar açılır: iç organlar ayrı kapta, **frengi izi yok**, ölüm nedeni hâlâ belirsiz. Her 18 Şubat'ta Floransa tarihî alayla mezara yürür; 31 Ekim'de Uffizi ücretsizdir.
- **Saat akışı:** **Yok** (saat, tanık, son söz bulunamadı).
- **Kişiler:** Anna Maria Luisa; Craon; Francis Stephen (Floransa'ya yalnız 1739 başında gelir); Gian Gastone (ölü).
- **Belgelenmiş sözler:** Patto metni (Fransızca) **görülmedi**; İtalyanca çeviri lafzı bD23. USLUP §5-A "aktarıldığına göre" kalıbı korunur. D2: "beş buçuk yıl önce".
- **Belirsiz noktalar:** Ölüm saati/tanıklar; vasiyet metni; imza töreninin yeri/kişileri; "Vienna 1737" etiketi.
- **Ayna yapısı:** 31 Ekim 1737 imza masası ↔ 18 Şubat 1743 ölüm odası ↔ 2013 mezar açımı ↔ bugünün Uffizi kuyruğu. **Ek ironi (◐):** "yabancıların merakı" cümlesi ile "ücretsiz giriş günü" aynı takvimde buluşur; **bir de hukuk ironisi:** akademik özete göre madde bir bağış değil, Lorraine'in mülkiyet alırken kabul ettiği bir şarttır (bM13).
- **Ton:** ölüm odasında mizah kapalı; kapanışta bugünle çarpıştırma ≤2.

### Sahne C — Rubens döngüsü (26 Şubat 1622 – 3 Temmuz 1642)

- **Çerçeve (◐):** 26 Şubat 1622 Louvre'da iki sözleşme: 24 tablo (21 sahne + 3 portre) ve IV. Henri serisi. Amaç: geçmişi aklamak, itibarı geri kazanmak; alegori güvenlikti (özet). Minerva portresi, "Pax optima rerum". Reddedilen sahne: Calumnia. 1625'te batı galeri tamamlanır; Henri IV serisi 1630'da durur, 1631'de terk edilir. 10–12 Kasım 1630 "Aldatılmışlar Günü"; Şubat 1631 Compiègne; Temmuz 1631 kaçış; 1638–41 İngiltere; 1641 Köln; **3 Temmuz 1642** Sternengasse 10'da plörezi ve yoksulluk. Tablolar 1816'da Louvre'a, 1993'ten beri "Galerie Médicis"e.
- **Saat akışı:** Gerekmez (galeri sahnesi); Köln odası için kaynak yok.
- **Belgelenmiş sözler:** Sözleşme parçası bD14 (EN çeviri, ○).
- **Belirsiz noktalar:** Peiresc'in rolü (aramada çıkmadı); ücret ve teslim takvimi; Concini'nin neden gösterilmediği; Marie'nin Köln'deki son günleri.
- **Ton:** mizah **kuruma/kibre** (imge siyaseti: tarihi yeniden yazdırma siparişi) açık olabilir; Marie'nin yoksulluğuna ve ölümüne kapalı. **YORUM:** Louvre'daki 24 tablo, sipariş sahibinin Köln'de borçlu ölmesinden sonra da asılı kalır.

### Ek sahne adayları (kısa)

| Sahne | Gün | Durum |
|---|---|---|
| Eleonora'nın gelişi: Napoli'den kadırgalarla, Pisa yolunda Cosimo'yla buluşma; 29 Haziran'da ayrı girişler | 11–29 Haziran 1539 | ◐ |
| Eleonora'nın düğünü: Tribolo, Bronzino, Salviati'nin bahçe avlusu | 29 Temmuz 1539 | ◐ |
| 1562 sonbaharı: Maremma gezisi, üç ölüm, 1857'de kırmızı atlas ceketli iskelet (mizah kapalı) | 20 Kasım–17 Aralık 1562 | ◐ |
| Lorenzino'nun Venedik'te pusuya düşürülmesi (Dall'Aglio: Cosimo'nun işi mi?) | 26 Şubat 1548 | ◐ |
| Siena'nın açlıkla teslimi (15 ay) | Nisan 1555 | ◐ |
| Lepanto'da 12 Toskana kadırgası | 7 Ekim 1571 | ◐ |
| *Balet comique*: 5 saatlik gösteri (mizah açık: kurum/gösteriş) | 15 Ekim 1581 | ◐ |
| Marie'nin vekâleten düğünü ve çeyiz-borç mahsubu (mizah açık: ticari evlilik) | 5 Ekim 1600 | ◐ |
| Fahreddin'in üç gemiyle Toskana'ya gelişi (TR-BAĞ) | 1613 | ◐ |
| Mustafa Ağa'nın Floransa'da ağırlanması (TR-BAĞ) | 1598 | ◐ |
| Bona'nın alınışı ve Sala di Bona freskleri (mizah kapalı) | 1607–1609 | ◐/○ |
| 18 Şubat alayı: Palazzo Vecchio'dan San Lorenzo'ya | her yıl | ◐ |

---

## 7. Hâlâ eksik kalanlar

**Kesin boşluklar (aranıp bulunamadı):**
1. **Varchi *Storia fiorentina* XV ve *Apologia* metni:** hâlâ açılmadı; 5–6 Ocak 1537 için saat akışı yok; Kardinal Cibo'nun rolü, ölümün gizlenmesi, cesedin yeri.
2. **Cosimo I'in "Magistrato Supremo (1549)", casus ağı, sansür:** bulunamadı. Yalnız "pratica segreta" ○.
3. **Catherine tarihyazımı:** Holt, Frieda, Sutherland, Crouzet, Diefendorf'un tutumları doğrulanamadı (Knecht, Jouanna, Britannica ◐).
4. **"Tuez-les tous" zinciri** (Tavannes *Mémoires*, Bourgeon 1996) açılmadı.
5. **Patto'nun Fransızca özgünü**, imzacıları (Craon dışında), 13 maddenin tamamı (yalnız 3. madde), "Vienna 1737" etiketinin anlamı; Casciu/Verga/Menicucci makaleleri ve Valentini'nin (Italia Nostra) çevirisi açılmadı. **Hukukî nitelik tartışmasının yazarı** (b75) belirsiz.
6. **Anna Maria Luisa:** vasiyet metni; ölüm saati/tanıklar/son sözler; cenaze töreni; 1691 evliliği ve 1716 (Johann Wilhelm'in ölümü) tarihleri; Fornaciari adının doğrulanması.
7. **Gian Gastone:** ölüm yeri ve koşulları; Acton'ın hükmü; Dami sayfasındaki "29 Temmuz 1737" çelişkisi.
8. **Cosimo II:** ölüm nedeni (verem iddiası) ve günü; Ferdinando I'in evlilik (1589) ve kardinallikten ayrılış tarihleri; Ferdinando I'in ölüm günü (17 mi, 7 mi).
9. **Cosimo III:** dindarlığı, vergiler, Floransa şehir nüfusu, 1716 bando'su; Marguerite Louise'in evlilik yılı (1661).
10. **Lepanto:** Toskana komutanı, gemi adları, kayıplar; **Cerbe 1560** (Toskana payı); **Tunus 1535**; **Leo X–Selim haçlı planı** (T1) aranmadı.
11. **Santo Stefano:** Livorno bagno'su ve Osmanlı esirleri; Prevesa'nın tarihi; tarikatın Levant seferleri takvimi.
12. **Medici–Osmanlı:** 1574–78 neden başarısız oldu; Gianfigliazzi 1578; Sultan'ın yanıtları; Cosimo I döneminde herhangi bir resmî temas var mıydı?
13. **Uffizi'nin 1769'da açılışı** bu turda doğrulanamadı (M3 ◐).
14. **Marie ve Rubens:** döngünün ücreti, teslim takvimi, Peiresc, Concini; Marie'nin kalbinin yeri (Köln mü, başka yer mi); **1610 tacı ve naiplik (1610–17), 1617'de Concini'nin öldürülmesi, 1619 Blois'dan kaçış** (M4 #81–#83, §3.D #10) bu turda **aranmadı**.
15. **Alessandro'nun kökeni:** Fletcher'ın kitabı ve Literary Hub yazısının içeriği; DNA iddiası hâlâ kanıtsız.
16. **2026 iScience makalesi** (künye, yöntem, "Giovanni"nin kimliği) açılmadı.

**Sonraki tur için sorgu önerileri (yapıştırılabilir):**
- `Convention de famille 1737 Florence texte article III Anne-Marie-Louise Électrice Palatine Craon Rinuccini` (Fransızca özgün)
- `Menicucci "Le trattative per il patto di famiglia" Gian Gastone Craon Rinuccini 1737 articoli` (storiadifirenze.org)
- `Mercan "Medici-Ottoman diplomatic relations" 1574 1578 Gianfigliazzi Istanbul Murad III` (Brepols cilt 3)
- `Varchi Storia fiorentina libro XV Lorenzino Alessandro "Scoronconcolo" "Cibo" trattenere la morte due giorni`
- `Knecht Catherine de' Medici Saint Bartholomew 1572 "Catherine" responsibility Holt "French Wars of Religion" Crouzet`
- `Cosimo II de' Medici death 28 February 1621 tuberculosis; Ferdinando I death 17 February 1609 Pisa`
- `Lepanto 1571 Tommaso de' Medici galere toscane capitana "Santo Stefano" Pisa Carovana`

---

## 8. Kaynak URL listesi (arama sonuçlarında görülen sayfalar; **içerikleri açılmadı**)

- **Cosimo I, 1537:** treccani.it/enciclopedia/cosimo-i-de-medici-duca-di-firenze-granduca-di-toscana_(Dizionario-Biografico)/ · treccani.it/enciclopedia/cosimo-i_(Dizionario-di-Storia)/ · treccani.it/enciclopedia/raffaello-de-medici_res-1b10ae76-dcdf-11df-9ef0-d5ce3506d72e_(Dizionario-Biografico)/ · treccani.it/enciclopedia/alessandro-vitelli_(Dizionario-Biografico)/ · treccani.it/enciclopedia/giovanni-corsi_(Dizionario-Biografico)/ · en.wikipedia.org/wiki/Battle_of_Montemurlo · en.wikipedia.org/wiki/Cosimo_I_de'_Medici · en.wikipedia.org/wiki/Duchy_of_Florence · findagrave.com/memorial/194287824/filippo-strozzi_the_younger · ebsco.com/research-starters/history/cosimo-i-de-medici
- **Alessandro / Lorenzino:** en.wikipedia.org/wiki/Alessandro_de'_Medici,_Duke_of_Florence · en.wikipedia.org/wiki/Lorenzino_de'_Medici · treccani.it/enciclopedia/lorenzino-de-medici_(Enciclopedia-Italiana)/ · yalebooks.yale.edu/?p=4973 · academic.oup.com/yale-scholarship-online/book/29793 · historytoday.com/archive/feature/solving-renaissance-murder-mystery · britannica.com/print/article/372330 · doaj.org/article/ca455e01aa4c4e6ebf9e680cc69dd21b · commons.warburg.sas.ac.uk/downloads/j3860693n · ellopos.net/politics/renaissance/1-against-despots.asp · en.wikipedia.org/wiki/Simonetta_da_Collevecchio · history.co.uk/articles/the-life-of-alessandro-de-medici-the-black-duke-of-florence · lithub.com/the-forgotten-history-of-florences-mixed-race-medici/
- **Eleonora / 1562:** italianartsociety.org (2015/06, "On 29 July 1539…") · palazzo-pitti.net/eleonora-of-toledo.html · palazzo-pitti.net/garzia-demedici-biography.html · en.wikipedia.org/wiki/Eleanor_of_Toledo · en.wikipedia.org/wiki/Garzia_de'_Medici · en.wikipedia.org/wiki/Giovanni_de'_Medici_(cardinal) · uffizi.it/en/artworks/burial-clothes-of-don-garzia-de-medici-doublet-with-breeches-surcoat · historyofroyalwomen.com/eleanor-of-toledo/eleanor-toledo-murder-malaria/ · pieceworkmagazine.com/the-eleonora-project-part-7-the-death-of-eleonora-as-told-by-her-gown/ · smarthistory.org/?p=1603 · archaeologymag.com/2026/07/malaria-killed-the-medici-brothers-not-poison/
- **Siena, unvan, tarikat:** en.wikipedia.org/wiki/Battle_of_Marciano · historyofwar.org/articles/siege_siena_1553_5.html · historyofwar.org/articles/battles_marciano.html · flore.unifi.it (Guerra e conquista di Siena) · vive.cultura.gov.it/en/event-battle-marciano · en.wikipedia.org/wiki/Grand_Duchy_of_Tuscany · en.wikipedia.org/wiki/List_of_grand_dukes_of_Tuscany · en.wikipedia.org/wiki/Order_of_Saint_Stephen · finestresullarte.info/en/works-and-artists/defending-the-faith-and-protecting-the-mediterranean-history-of-the-knights-of-st-stephen · piazzadeicavalieri.sns.it (Order of Saint Stephen) · en.wikipedia.org/wiki/Battle_of_Lepanto · kureansiklopedi.com/tr/detay/toskana-2 · en.wikipedia.org/wiki/Portoferraio · en.wikipedia.org/wiki/Ottoman_wintering_in_Toulon
- **Catherine:** britannica.com/biography/Catherine-de-Medici/The-Massacre-of-St-Bartholomews-Day · britannica.com/event/Massacre-of-Saint-Bartholomews-Day · en.wikipedia.org/wiki/St._Bartholomew's_Day_massacre · en.wikipedia.org/wiki/Assassination_of_Admiral_Coligny · historytoday.com/rj-knecht/catherine-de-medici-saint-or-sinner · academic.oup.com/ehr/article-abstract/CXXII/497/813/391181 · academic.oup.com/fh/article-abstract/28/4/563/586603 · historytoday.com/archive/review/catherine-de-medici-mary-hollingsworth-review · katalog.dhi-paris.fr/vufind/Record/1637760108 (Bourgeon/Tavannes) · en.wikipedia.org/wiki/Ballet_Comique_de_la_Reine · en.wikipedia.org/wiki/René_Bianchi_(perfumer) · atlasobscura.com/articles/5032 · research.colonialwilliamsburg.org/Foundation/journal/Spring10/icecream.cfm · cooksinfo.com/catherine-de-medici · thenewgastronome.com/caterina-de-medici-a-gastronomic-myth/ · en.wikipedia.org/wiki/Escadron_volant · openresearch-repository.anu.edu.au (McIlvenna, "A Stable of Whores?")
- **Marie / Rubens:** en.wikipedia.org/wiki/Marie_de'_Medici · ebsco.com/research-starters/history/marie-de-medicis · link.springer.com/chapter/10.1057/9780230321793_2 · en.wikipedia.org/wiki/Day_of_the_Dupes · en.wikipedia.org/wiki/Luxembourg_Palace · en.wikipedia.org/wiki/Marie_de'_Medici_cycle · herodote.net/16_decembre_1600-evenement-16001216.php · roderickconwaymorris.com/Articles/76.html · hnanews.org (Corpus Rubenianum XIV incelemesi) · themorgan.org/blog/peter-paul-rubens-receives-commission-lifetime · louvre.fr/oeuvre-notices (L'Apothéose de Henri IV…) · sammlung.pinakothek.de (Medici-Zyklus)
- **Ferdinando I → Gian Gastone:** en.wikipedia.org/wiki/Ferdinando_I_de'_Medici · britishinstitute.it/en/the-medici-grand-dukes/ferdinando-I-de-medici · en.wikipedia.org/wiki/Ferdinando_II_de'_Medici · en.wikipedia.org/wiki/Cosimo_III_de'_Medici,_Grand_Duke_of_Tuscany · historyofroyalwomen.com/the-royal-women/marguerite-louise-dorleans-end-medici-dynasty/ · treccani.it/enciclopedia/gian-gastone-i-de-medici-granduca-di-toscana_(Dizionario-Biografico)/ · treccani.it/enciclopedia/giangastone-de-medici-granduca-di-toscana_(Enciclopedia-Italiana)/ · treccani.it/enciclopedia/gian-gastone-de-medici_(Dizionario-di-Storia)/ · treccani.it/enciclopedia/cosimo-iii-de-medici-granduca-di-toscana_(Dizionario-Biografico)/ · britannica.com/biography/Gian-Gastone · en.wikipedia.org/wiki/Gian_Gastone_de'_Medici · en.wikipedia.org/wiki/Princes_of_Ottajano · en.wikipedia.org/wiki/Marc_de_Beauvau,_1st_Prince_of_Craon · habsburger.net/en/chapter/tuscany-habsburg-secundogeniture · cambridge.org/core/books/abs/altopascio/conclusion/48B709D6952491D8E2CA300656E80FF0
- **Patto / Anna Maria Luisa:** italianostra.org/wp-content/uploads/AML-MEDICI_LOCANDINA_31-10-17_def.pdf · storiadifirenze.org/pdf_ex_eprints/56-Casciu.pdf · storiadifirenze.org/pdf_ex_eprints/14-Verga_Pitti.pdf · storiadifirenze.org/wp-content/uploads/2018/03/254-Menicucci.pdf · cultura.comune.fi.it/dalle-redazioni/anna-maria-luisa-de-medici-e-il-patto-di-famiglia · uffizi.it/video/l-eredita-di-anna-maria-luisa-de-medici-per-firenze · lanazione.it/firenze/cronaca/18-febbraio-firenze-celebra-lelettrice-palatina-musei-gratis-e-iniziative-59137846 · arte.it/notizie/firenze (musei comunali, Elettrice) · finestresullarte.info/eventi/patto-di-famiglia-anna-maria-luisa-uffizi-31-ottobre · en.wikipedia.org/wiki/Anna_Maria_Luisa_de'_Medici · madamegilflurt.com/2015/02/the-death-of-anna-maria-de-medici.html · thehistoryblog.com/archives/69476 · archaeology.org/news/2013/02/14/130214-medici-anna-maria-cause-of-death/ · nature.com/articles/495046a.pdf · arpi.unipi.it/handle/11568/825609 · theflorentine.net/?p=5010 · conoscifirenze.it/history/1142-anna-maria-luisa-and-the-family-pact.html · ilgiornale.it (Io erede dei Medici…) · rivista-incontri.nl/article/download/14249/20940/43054
- **TR-BAĞ:** tandfonline.com/doi/full/10.1080/09518967.2020.1820696 · cadmus.eui.eu/handle/1814/46687 · brepols.net/products/IS-9781909400368-1 · rivisteweb.it/doi/10.7387/107764 · iris.uniroma1.it/handle/11573/1099914 · avesis.hacettepe.edu.tr (Mercan yayınları) · archive.aramcoworld.com/issue/201404/lebanon.s.renaissance.prince.htm · journals.ku.edu/druze/article/view/24764 · en.wikipedia.org/wiki/Chios_expedition_(1599) · rime.cnr.it/index.php/rime/article/view/474 · en.wikipedia.org/wiki/History_of_the_Jews_in_Livorno · christies.com.cn/lot/lot-1794989 · newhaven.academia.edu/LisaKaborycha · jewishvirtuallibrary.org/the-jews-and-the-medici

---

*Dosya sonu. Ana ajan: git commit/push yapılmadı.*
