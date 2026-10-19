# Medici c6–c16 — bağımsız olgu / ton / seslendirilebilirlik incelemesi (19 Ekim 2026)

> Kapsam: `scr_c6.py … scr_c16.py` (c0–c5 ses üretildiği için dışarıda; yalnız c5 → c6 kapısına bakıldı). **scr dosyalarına dokunulmadı.** Öneriler `cNsM` kimliğiyle ve TAM yedek cümleyle verilir; cümle SAYISI değişmesin diye çoğu yerinde (in-place) değişikliktir. Tek silme: c7s19 (kimlikler kayar; ses henüz yok, sorun değil).
>
> **Kanıt gücü dürüstlüğü:** Bu ortamda ● düzeyinde teyit yapılamadı (birincil metin açılmıyor). Karşılaştırma: `arastirma/M1…M5`, `brif/*`, `kaynaklar_P3…P7.md` + 27 adet WebSearch (hepsi "standard"; arama özetleri ◐/○ düzeyidir, makale/kitap metni açılmadı). Aşağıda "◐" = birden çok ikincil/ansiklopedik özet uyumlu, "○" = tek özet/zayıf.

## 1. Özet tablo

| Bölüm | K1 | K2 | K3 | K4 |
|---|---:|---:|---:|---:|
| c6  | 0 | 2 | 1 | 0 |
| c7  | 1 | 1 | 2 | 1 |
| c8  | 0 | 1 | 1 | 1 |
| c9  | 0 | 2 | 3 | 1 |
| c10 | 0 | 0 | 2 | 0 |
| c11 | 0 | 1 | 3 | 1 |
| c12 | 0 | 3 | 2 | 1 |
| c13 | 0 | 0 | 4 | 1 |
| c14 | 0 | 0 | 2 | 1 |
| c15 | 1 | 3 | 0 | 0 |
| c16 | 0 | 3 | 1 | 0 |
| **Toplam** | **2** | **16** | **21** | **7** |

K1 = kesin hata / yanıltıcı, yayını engeller · K2 = olası hata / zayıf dayanak · K3 = ton / üslup / akış (parça açılışı-kancası dahil) · K4 = okunuş.
Önerilen yedek cümle sayısı ≈ 42 (+1 silme).

**Genel sonuç:** Olgu katmanı beklenenden sağlam; iki gerçek sorun var: (1) c15s13 araştırma sınırımızı "literatür böyle" diye söylüyor, (2) c7s46 "o sabah bronza döküldü" yanlış okunuyor. Asıl işin çoğu parça açılış/kapı akışında (c6, c8, c10, c12, c14 bağlamı; c13→c14 kancası uyuşmuyor) ve okunuş (Bargello, Mugello, Scipione, "Henri IV" vb.).

---

## 2. Bulgular (bölüm bölüm)

### c6 — Lorenzo (P3 açılışı)

**[K3] c6s1–s2 · P3 açılışı kim/kimin torunu/nerede kurmuyor.** İlk iki cümlede "Lorenzo" soyadsız, Floransa/Cosimo geçmiyor; P2'yi görmemiş izleyici kaybolur (c5 kapısındaki "tahtsız efendi" burada yok). Ayrıca "en iyi dostu" abartı (kaynak "yakın dost"). En küçük düzeltme: aynı iki cümleyi yerinde değiştir (dönem HUD'daki YIL 1449 ile gelir). Kanıt: kendi okumam + M5:K16.
```
("Cosimo'nun torunu Lorenzo de' Medici'yi yakın dostu Niccolò Valori anlatır: doğa, görünüşü konusunda ona üvey ana gibi davranmış; ama zihne gelince şefkatli bir ana olmuş.", None, "◐ M5:K16; M3:C26 (özgün görülmedi → \"Valori'ye atfedilir\"); P3 açılışı: kimin torunu")
("Valori'ye göre Floransa'nın bu tahtsız efendisinin yüzü güzel sayılmazdı, ama saygı uyandıracak kadar vakarlıydı.", None, "◐ M5:K16")
```

**[K2] c6s4 · koku.** Dayanak M5:K19'a göre "◐ zayıf" (iki ikincil: öğrenci-notu sitesi + Unger/FlorenceCity); "Valori'ye göre" kesin atıf özgün metin görülmeden veriliyor. "bile" sözcüğü, docstring'in yasakladığı "görünüş/koku alayı"na kayıyor (s3–s4 art arda kusur listesi). Kanıt ◐ zayıf.
```
("Valori'ye atfedilen tarife göre koku duyusu da neredeyse yoktu.", None, "◐ zayıf M5:K19; M3:C27 (iki ikincil; \"atfedilen\"; yayın öncesi teyit; \"bile\" kalktı — alaysı okunmasın)")
```

**[K2] c6s22 · Botticelli sancağı.** Etiket "○ … (anlatılır)" ama cümle düz kesin kipte. Sancak kayıp, Simonetta'nın model olduğu gelenek (Poliziano/Vasari türevi).
```
("Botticelli'nin sancağa Simonetta'yı miğferli bir Pallas olarak resmettiği anlatılır; asıl sancak kayıp.", None, "○ olay / ○ görünüş M3:C36 (\"anlatılır\")")
```

*Not (düzeltme gerektirmeyen):* Giuliano doğumu Ekim 1453 → 24 yaş (24 y 5–6 ay; M5:D24, DBI/Enc. machiavelliana ◐) tutarlı; "üç yıl üç ay" 3 y 2 a 28 g, kabul edilebilir yuvarlama. Machiavelli ithafı: Vettori mektubu (10 Ara 1513) "Muhteşem Giuliano'ya ithaf ediyorum" der, basılı ithaf Lorenzo di Piero'ya (M3b:b51–b52) → c6s17 destekli (yalnız "ithaf etmeyi düşündü" daha kesin; küçük zevk, öneri yok). **c5 → c6 kapısı uyumlu** ("listenin sahibine, Lorenzo'ya bakalım" → "Lorenzo'yu … anlatır"); yukarıdaki düzeltme bunu bozmaz.

---

### c7 — 26 Nisan 1478

**[K1] c7s46 · "O sabah bir de bronza döküldü".** Madalya (Bertoldo'ya atfedilen, 1478) o sabah değil, sonradan yapıldı; cümle düz okununca "o sabah döküldü" der. Bölüm kapısı da "o sabah"a yaslandığı için yanlış anlam sonda pekişiyor. Kanıt: M2c:Y40 (NGA, V&A: "1478"); ◐.
```
("Aynı yıl bu olay bronza da döküldü: Bertoldo'ya atfedilen bir madalyanın bir yüzünde Lorenzo, ötekinde Giuliano var; yazılar “Halkın Esenliği” ve “Halkın Yası”.", None, "◐ NGA + V&A M2c:Y40 (atıf ○; çeviri bize ait; \"o sabah\" YANLIŞ okunuyordu)")
```
(c7s47 "…o sabah ölmüştü" aynen kalabilir; istenirse "26 Nisan sabahı".)

**[K2] c7s3 · Riario'nun yaşı.** "17 yaşındaki": EN Wikipedia + italyonthisday doğumu 3 Mayıs 1461 verir → 26 Nisan 1478'de 16 y 11 ay (10 Ara 1477'de kardinal olduğunda 16). Treccani DBI özeti "17" der (araştırma Y06). Kaynaklar ayrışıyor (○/◐). Güvenli kip:
```
("Ayin, şehre yeni gelmiş genç bir konuğun onuruna yapılıyordu: 16 ya da 17 yaşındaki Kardinal Raffaele Riario, Papa'nın akrabası.", None, "◐ doğum 3 Mayıs 1461 (EN Wikipedia; italyonthisday) → 16 y 11 ay; DBI \"17\" ayrışır; \"onuruna\" Enc. machiavelliana; akrabalık M2:K41 ○ (\"kardinal yönetti\" söylenmez)")
```

**[K4] c7s22 · tunç kapı cümlesi yanlış duyulur.** "Dostlarının, Michelozzo ve Luca della Robbia'nın tunç kapısını …" sözdizimi sesle dostların adı gibi okunuyor (Michelozzo 1472'de ölmüştü). Kapının ustaları ekranda kalsın.
```
("Dostlarının, sakristinin ağır tunç kapısını arkasından kapattığı anlatılır; aralarında şair Poliziano da vardı.", None, "◐ Gardner + Britannica; adlar ÇELİŞİR M2c:T3 (\"anlatılır\"; kapıyı yapanlar — Luca della Robbia/Michelozzo — ekranda, seste değil)")
```
PRON (düşük öncelik): `(r"\bMaffei\b", "Maffey")` — şimdi kimlik eşlemesi; Türkçe okuyucu "Maffei"yi üç hece okuyabilir.

**[K3] c7s19 · "Giuliano 24 yaşındaydı." cümlesi c6s27 ile aynı parçada tekrar** (P3: 5 dk arayla "yirmi dört" iki kez); c6 kapısındaki dramatik ironi bunu zaten taşıyor. **Öneri: c7s19'u sil** (yaş c6s27'de kalır). Ek kazanç: 24/25 tartışması bir yerde kalır.

**[K3] c7s10 · "Treccani" cold-open'da tanıtılmıyor.** Seride yalnız c2'de anılmıştı; her parçada ilk geçişte kısa tanım şart. Aynı kalıp: c9s17 (aşağıda), c11s35, c12s4, c15s15 ilk geçişlerinde de "İtalyan Ansiklopedisi Treccani" demek yeter (mekanik).
```
("Yerine aceleyle iki papaz seçildi: Antonio Maffei ve Stefano da Bagnone; İtalyan Ansiklopedisi Treccani bu değişikliği planın kısmen çökmesinin nedenlerinden sayar.", None, "◐ DBI Montesecco özet tırnağı (\"Treccani'ye göre\")")
```

*Sorun çıkmayanlar:* 19 yara, 26 Mayıs Giulio, 30 Nisan cenaze, Salviati'nin asılması, Montesecco itirafı, Papa'nın payı (taraflar ayrı), "Pazzi'lerin sesi yok" uyarısı, ağır sahnede mizahın kapalı olması (s14 "şakalaştıkları" aktarılan olgu, alay değil). **Maffei itirafı (s42):** Simonetta'nın Mayıs 2023'te Archivio di Stato'da bulduğu belge doğrulandı (NYU/Syracuse haberleri ◐; işkence/zorla yazma çerçevesi de uyumlu) — "anlatılan" sözcüğü kalkabilir ama içerik ayrıntısı (Papa/Napoli/Urbino) bu turda ○.

---

### c8 — Aslanın İni (P4 açılışı)

**[K2/K3] c8s1 · parça açılışı bağlamsız + aforoz günü.** "Aforoz kararı 1 Haziran 1478'de çıktı" — kim, neden? P4'e c7'den gelmeyen izleyici için boşlukta. Ayrıca gün: bazı kaynaklar 1 Haziran'ı **ihtar/bülten** (aforoz + interdikt tehdidi), kesin aforozu/interdikti sonraya yazar (Brocku sergisi: "1 Haziran'da tehdit"; başka katalog 1 Temmuz; ben Haziran sonu hatırlıyorum ama arama doğrulamadı → ○). Gün söylenmezse risk de, bağlam da çözülür.
```
("Pazzi suikastının ve başpiskopos Salviati'nin asılmasının ardından, Haziran 1478'de Papa IV. Sixtus Lorenzo'yu aforoz etti; çok geçmeden Floransa'nın kendisine de yasak, yani interdikt kondu.", None, "◐ M2c:Y35,Y37 (gün söylenmez: 1 Haziran ihtar mı kesin karar mı ○ — Reumont/EdP/DBI Lorenzo teyit); P4 açılışı: kim/neden")
```

**[K4] c8 · PRON.** `Bargello` şimdi kimlik eşlemesi; İtalyanca "Bar-CEL-lo" (g+e yumuşak). `Poggio Imperiale` → "Poççio" (ç = tʃ) yerine "gg" = dʒdʒ.
```python
(r"\bBargello\b", "Barcello"), (r"\bPoggio Imperiale\b", "Pocco İmperyale"),
```

*Kontrol edilen, sorun çıkmayan:* Napoli tarihleri (6 Ara/18 Ara/27 Şub) tek DBI ama "DBI'ye göre" kipinde; Bandini zinciri (Louvre + haber özetleri: Sultan'dan teslim, 24 Ara varış, 29 Ara Bargello, Leonardo çizimi) uyumlu ◐; Otranto 28 Temmuz; Aralık 1480 bağışlanma; **Mehmed II'nin ölümü 3 Mayıs 1481 ve Otranto'nun Eylül 1481'de dönüşü (HAFIZA-Y) benim bilgimle de doğru** (yayın öncesi Türkçe kaynakla teyit yine de listede). Madalya tarifi hedge'li, "tuhaf hediye" mizahı kuruma yönelik. Mizah kapalı sahnelerde (Bandini, Otranto) yok. "Silahsız" geçmiyor (doğru).

---

### c9 — Defter Kapanıyor

**[K2] c9s11–s12 · Londra: toplam kredi ≠ kalan borç.** M1 #60 / Cambridge: 1466–71 arası **toplam krediler >£26.000, bir kısmı geri ödendi**; popüler "kralın borcu £10.500". Script "yirmi altı bin sterlin borç verdi … kralın ödeyemediği yazılır" diyerek 26.000'in tamamını ödenmemiş gösteriyor. Web özeti de aynı: ">£26.000 (1466–71), bir kısım ödendi; başka kaynak £10.500". Kanıt ○ (Holmes özeti).
```
("Londra şubesi, 1466 ile 1471 arasında Kral IV. Edward'a toplam yirmi altı bin sterlinden fazla kredi verdi.", None, "○ M1:#60,D44 (Holmes/Cambridge: toplam kredi, kalan borç DEĞİL; popüler £10.500 SÖYLENMEZ)")
("Bir kısmı geri ödendi; kalanı için Güller Savaşı suçlanır, ama rakamlar kaynaktan kaynağa değişir.", None, "○ çelişkili M1b:U23,b50")
```

**[K2][K4] c9s18 · "Tarihçi de Roover'a göre" ve Goldthwaite.** (a) Yazıda ve seste "Tarihçi de Roover'a göre" ifadesindeki "de" bağlaç ("tarihçi de, ayrıca") gibi okunabiliyor (c2'de cümle başında "De Roover'a göre" olduğundan sorun yoktu). (b) "Goldthwaite … banka krizi görmez" yalnız dokumen özetine (○, M1b:b82) dayanıyor; "genel" eklemek iddiayı güvenli kılar.
```
("Tarihçi Raymond de Roover'a göre Lorenzo parlak bir devlet adamıydı, iş adamı değil; Goldthwaite ise 1500 öncesi Floransa'da genel bir banka krizi görmez.", None, "○ yaklaşık M1b:bD17,b82 (birebir tırnak yok; \"genel\" eklendi; Goldthwaite özeti ○)")
```
PRON (c9'a): `(r"\bRaymond\b", "Reymond")` — "de Roover"→"de Rover" c2'deki seslendirilmiş okunuşla tutarlı kalsın.

**[K3] c9s7 · "genel müdür" iki anlamlı.** Portinari = yalnız Brugge şube müdürü; iki cümle sonra "Genel müdür Sassetti" (banka). Dinleyici Portinari'yi bankanın genel müdürü sanar. Kanıt: M1 #57/D40 (Wikipedia+Cambridge ◐: "yıllarca yardımcı/faktör").
```
("Brugge'de yıllarca yardımcı olarak çalışan Tommaso Portinari'ye Cosimo'nun pek güvenmediği anlatılır; ama Cosimo ölünce Portinari şubenin müdürü ve ortağı oldu.", None, "◐ \"anlatılır\" M1:#57,D40 (yıl ≈1465–68 belirsiz; \"genel müdür\" = yalnız Brugge)")
```

**[K3] c9s21 · iki Piero.** s4'te "Piero de' Medici" (Cosimo'nun oğlu, 1466), s21'de "Piero kaçtı" (Lorenzo'nun oğlu, 1494) aynı bölümde tanıtılmadan. 
```
("Kasım 1494'te Lorenzo'nun oğlu Piero kaçtı; Signoria Medici'yi sürgün etti.", None, "◐ M1b:b64; M2:K91 (8↔9 Kasım söylenmez; öyküsü c10)")
```

**[K3] c9s28 · kapıdaki "o güne" bağlayacak gün yok** (önceki cümleler "Banka öldü, güzellik kaldı"). 
```
("Peki Medici'yi sürgüne gönderen o güne nasıl gelindi? Bir kralın Alpler'i aşmasıyla, bir rahibin vaazlarıyla.", None, "YORUM (c10 kapısı; \"o gün\" = Kasım 1494)")
```

*Not (öneri yok):* Sassetti "1463'ten 1490'a, yaklaşık otuz yıl" DBI'nin kendi sözü ("quasi un trentennio") ama aritmetik 27 yıl ve başka kaynaklar 1458/59'u verir → yayın öncesi teyit listesinde. Foça 1455 / Tolfa, Brugge/Londra kapanış aralıkları, 1494 el koyma, Donatello bronzları sağlam.

---

### c10 — Rahip ve Kral (P5 açılışı)

**[K3] c10s1 · P5 açılışı kim/nerede kurmuyor.** "Lorenzo, 43 yaşında … Careggi villasında öldü" — soyad ve şehir yok; c9 kapısı "kral + rahip" derken bölüm ölüm odasıyla açılıyor (rahip s4'te geliyor, kral çok sonra).
```
("Nisan 1492'de Floransa'nın efendisi Lorenzo de' Medici, 43 yaşında, rahatlama umuduyla taşındığı Careggi villasında öldü.", None, "◐ M4c:A02,D47; \"43\" = M5 hesap (gün söylenmez: 8 ↔ 9 Nisan); P5 açılışı: kim/nerede/ne zaman")
```

**[K3] c10s12 · Charles VIII bölümde hiç tanıtılmıyor.** "Fransız kampı", "krala" derken kral kim? s21'de adı "Charles" soyut geliyor; c9 kapısının vaat ettiği "Alpler'i aşan kral" burada görünmüyor. Yerinde değişiklikle (22 söz) çözülür:
```
("Piero görüşmeyi kendi eliyle yürütmek istedi; ekimin sonunda, Sarzana'daki kampta, Alpler'i aşıp gelen Fransa Kralı VIII. Charles'a şehrin kalelerini Signoria'ya sormadan bıraktı.", None, "◐ Treccani/Cambridge M4c:A13,D55 (kale sayısı, gün söylenmez; \"beceriksiz\" DENMEZ); c9 kapısının \"kral\"ını burada adlandırır")
```
(Romen "VIII." → "Sekizinci Şarl" mevcut regex/PRON ile doğru çıkar.)

*Kontrol edilen, sorun çıkmayan:* **c10s34 "şafağında"** — benim ilk şüphem yersiz: DBI Savonarola "üç Dominiken şafakta ayine katılır" der (M4c:C14) → şafak ayine bağlı, idama değil; sorun yok. Poliziano mektubunda Savonarola'nın bulunuşu (üç özet) ve "üç şart/duvar"ın olmayışı (D48) tutarlı; 9 Kasım 1494 Pazar; Capponi/Corsini/Charles 17 Kasım; Büyük Konsey; 7 Şubat 1497 ateşi; 7-8 Nisan 1498; 23 Mayıs. Botticelli mizahı kaynak yokluğuna yönelik (gerçek başlık: "Bonfire of the Botticellis"). Zweig kapı (K1) bölümde tek.
*Ritim notu (yedeksiz):* s15 ("anlatılır"), s17 ("yazılır"), s18 ("yazıldığına göre") — yıldız anın tam ortasında üç hedge art arda; kaynak disiplini gereği doğru ama anlatıyı yavaşlatıyor. İsterseniz tek şemsiye ifade ("Bu günü çoğunlukla Landucci'nin günlüğünden ve ona dayanan anlatılardan biliyoruz") + s18'de hedge'i düşürmek mümkün; kimlik kaymaması için yazmadım.

---

### c11 — Papa Oğulları

**[K2] c11s6 · Alfonso d'Este atı.** Etiket "○ anlatılır" ama cümle düz kesin kip; dayanak yalnız Schaff (Pastor'a atıf) ✓ var ama tek eski ikincil (arama: iki turda aynı kaynak).
```
("Papa'nın beyaz atını, aforozlu Alfonso d'Este'nin yedekten yürüttüğü anlatılır.", None, "○ Schaff→Pastor IV (tek eski ikincil); M4:3B#3; mizah a")
```

**[K3] c11s14 · Giulio = Clemens bağı hiç kurulmuyor.** c7s45 "Giulio doğdu" (Clemens adı c11'e bırakılmıştı) ama c11'de VII. Clemens tanıtımsız geliyor; hem c7'nin vaadi boşa gidiyor hem P5'e yeni gelen izleyici Clemens'in kim olduğunu bilmiyor. Tek Şarlken cümlesi korunur (26 söz).
```
("X. Leo'nun papalığında Luther itiraz etmişti; Giuliano'nun ölümünden bir ay sonra doğan oğlu Giulio'nun, yani VII. Clemens'in papalığında ise Roma'ya Şarlken'in, yani V. Karl'ın ordusu girdi.", None, "◐+◐ M4:#16,#25; M5:K24,P12 (c7s45 sonucu: Giulio = Clemens; ŞARLKEN CÜMLESİ, tek)")
```

**[K3] c11s22 · aynı "Ne düşündüğünü bilmiyoruz; ama ne yaptığını biliyoruz" kalıbı bu serinin 4. tekrarı** (c8s11, c10s17, c11s22, c13s29; c12s25 varyant; c0/c1 varyantları da var). Aynı kelime kelime kalıp P4–P6'da dört kez duyulur → tik. c8s11 ve c10s17'de kalsın (en güçlü), c11 ve c13'te düz anlatım:
```
("Papa aralıkta kılık değiştirip kaçtı; kılığı bir kaynakta seyyar satıcı, bir başkasında tüccar olarak anlatılır.", None, "◐ M4:#28,3B#13 (kalıp c8/c10'da kaldı; üçüncü tekrar düz anlatıma çevrildi)")
```

**[K3] c11s30–s31 · kuşatmanın sonu söylenmiyor + 1975 odası havada.** Gavinana'dan sonra "Papa Michelangelo'yu bağışladı" geliyor ama cumhuriyetin teslim olduğu hiç anlatılmıyor; sonra "1975'te … bir oda çıktı ortaya" ile Michelangelo arasındaki bağ (saklanma geleneği) kurulmadığından dinleyici için non sequitur. İki cümle yerinde değişir:
```
("Cumhuriyet teslim olunca Michelangelo bir süre saklandı; saklandığı yerin Yeni Sakristi'nin altındaki bir oda olduğu da söylenir. Papa onu bağışladı, ama bir şartla: Yeni Sakristi'ye dönecekti.", None, "◐ M3b:b42,b43,bm8 (iki gelenek: Yeni Sakristi altı ↔ San Niccolò; \"söylenir\")")
("1975'te, Yeni Sakristi'nin altındaki iki kat sıva kalkınca, duvarları kömür çizimlerle dolu bir oda çıktı ortaya; çizimleri Michelangelo'ya bağlamak tartışmalıdır.", None, "◐ M3b:b44,bd18 (restoratör iki kat sıva; atıf tartışmalı; Zweig yavaşlatması)")
```

**[K4] c11 · PRON paketi.** `Mainz` (→ "Mayns"), `Luther` (→ "Lüter"), `Fabrizio` ("-z-" = ts), `Ferruccio` ("Ferruççio" fazladan hece), `Castel` (c11s21 "Castel'de": C = /dʒ/ okunur), `d'Este`:
```python
(r"\bMainz\b", "Mayns"), (r"\bLuther\b", "Lüter"), (r"\bFabrizio\b", "Fabritsyo"),
(r"\bFerruccio\b", "Ferruçço"),        # mevcut "Ferruççio"nun yerine
(r"\bCastel\b", "Kastel"),             # "Castel Sant'Angelo" satırından SONRA
(r"\bd'Este\b", "deste"),
```

*Kontrol edilen, sorun çıkmayan:* Leo'nun yazıtı **Leo'nun kendisi tarafından** yazıldı (Wikipedia/THE ◐) ve Hanno 8 Haziran 1516'da öldü; X. Leo "iki oylama" (1513 conclave, Wikipedia ◐); 189/147/42 İsviçre Muhafızı; Orange'ın iki kurşunu; Maramaldo; Alessandro/Lorenzino; 9 Ocak Cosimo. Ağır sahnelerde mizah yok; mizah yalnız Hanno/Albrecht (kurum). Not: sayı yoğunluğu (22 rakam öbeği) s17'de "189 kişisinden 147'si" dil olarak kaba: "yüz seksen dokuz kişilik İsviçre Muhafızı'ndan yüz kırk yedi kişi öldü" daha doğal (K3 küçük zevk, kimlik tahsis edilmedi).

---

### c12 — Dük (P6 açılışı)

**[K3] c12s1 · P6 açılışı yer/aile belirsiz.** "bir dükü kuzeni öldürmüş … 17 yaşında Cosimo" — hangi şehir, hangi dük, hangi Cosimo (Cosimo il Vecchio ile karışır)? Yerinde:
```
("Ocak 1537'de Floransa Dükü Alessandro'yu kuzeni öldürmüş, Senato da yerine Medici'nin yan kolundan 17 yaşındaki Cosimo'yu seçmişti.", None, "◐ M4b:b5 (P6 açılışı: kim/nerede; Cosimo I = Popolani kolu, Giovanni dalle Bande Nere'nin oğlu — M4b/M5)")
```
(Aynı olgunun c11s36–37'deki tekrarı, parçalar ayrı izlendiği için bilinçli; tam filmde fazlalık hissi küçük.)

**[K2] c12s14 · Vasari Koridoru yanlış tarif.** "Üst galerisi … koridora dönüştü": koridor Uffizi'nin galerisinin kendisi değil, onu Pitti'ye uzatan **ayrı yapı** (Arno'yu aşar). Uffizi resmî sayfası "1565 / düğün için" der (M3:cd50).
```
("1565'te Uffizi'nin üst katı, Arno'yu aşarak Palazzo Vecchio'yu Pitti Sarayı'na bağlayan bir koridorla uzatıldı: iktidarın ofisinden evine kapalı bir yol.", None, "◐ koridor; \"iktidarın ofisinden evine\" YORUM M3:cd50 (Vasari Koridoru ayrı yapı; \"galeri koridora dönüştü\" yanlış okunuyordu)")
```

**[K2] c12s23–s24 · "ilk yazanı bilinmiyor" ve 1857 sonucu.** (a) "Rivayetin ilk yazanı bilinmiyor" bizim **araştırma sınırımız** ("bulunamadı", M4b:bM1; Pieraccini anısı sınanmadı), literatür iddiası değil. (b) "1857'de … sıtmadan olduğu sonucuna varıldı" yalnız Wikipedia hattı (M4b:b24); Uffizi sayfası yalnız giysiyi anlatır. (c) **Bu turda doğrulandı:** 2010 kemik-bağışıklık çalışması (Trans R Soc Trop Med Hyg 104:583) Eleonora, Giovanni, Garzia ve Francesco'da *P. falciparum* proteinleri buldu (özet ◐); **2026 iScience DNA çalışması kardinal Giovanni'nin (ö. 1562) kaburgasını da içeriyor** (Pisa Üniv. basın açıklaması + CNN/archaeologymag ◐ — c12 docstring'inin "D16 belirsiz Giovanni" notu çözüldü: 1562'deki kardinal Giovanni). Böylece c12, c15 için tohum atar ve "1857" kırılgan dayanağının yerini alır.
```
("Sonra bir hikâye doğdu: Garzia kardeşini, Cosimo da Garzia'yı öldürmüş. Rivayet ölümlerden çok sonra ortaya çıktı; ilk yazanını gösteremiyoruz.", None, "ANEKDOT/◐ mit M4b:bM1 (\"rivayete göre\"; belge yok; \"bilinmiyor\" = araştırma sınırı)")
("Garzia'nın mezarı 1857'de açıldığında iskeletinde kırmızı atlas bir ceket vardı, şiddet izi görülmedi; sonraki kemik incelemeleri, 2026'daki DNA çalışması dahil, ölümlerin sıtmayla uyumlu olduğunu gösterdi.", None, "◐ M4b:b24,bD8,bM1 + 2010 TRSTMH + 2026 iScience (Giovanni; basın özeti ○ — makale açılmadı; yayın öncesi teyit)")
```

**[K3] c12s35 · kapı: ölümden sonra "kuruyordu".** s34 Cosimo'nun 1574 ölümü; s35 "Cosimo Floransa'da bir devlet kuruyordu" zaman geri sarıyor. Aynı tuple, tek cümle:
```
("Cosimo Floransa'da bir devlet kurarken, aynı yıllarda Paris'te, Floransa doğumlu bir Medici kızı, adı 24 Ağustos 1572 ile anılacak bir krizin ortasındaydı.", None, "◐ tarih; sorumluluk tartışmalı → c13 M4b:b32–b35,bM7 (K1)")
```

**[K4] c12 · PRON.** `(r"\bMugello\b", "Mucello")` (İtalyanca g+e; şimdi "Mugello" sert g okunur).

*Kontrol edilen, sorun çıkmayan:* **"üç ayrı 29"** — IAS/Reiss (29 Mart Napoli sözleşme+vekâlet; 29 Haziran ikisi ayrı girişle Floransa; **29 Temmuz resmî düğün**) ile destekli ◐/○; Wikipedia yalnız "29 Mart 1539" verir (kimse çelişmez ama hızlı kontrol eden 29 Haziran'ı "düğün" bulabilir → teyit listesinde). Lorenzino 1548 (Dall'Aglio: emir Cosimo'dan değil, V. Karl hattı — cümle hedge'li ✓). Siena 15 ay/1557; Uffizi 13 makam; 1769 açılış; Santo Stefano 1561/1562; Büyük Dük 1569/1570; İnebahtı: Toskana'dan 12 gemi iki anlatım (hedge'li ✓), Osmanlı yenilgisi nötr.
*Çerçeve notu (opsiyonel, HAFIZA — Türk izleyici dengesi):* s18 yalnız "Hristiyan esirleri kurtarmak"tan söz ediyor; Santo Stefano gemileri Müslüman esir de alıp Livorno'da satıyordu (araştırmada yok; genel bilgi ○). Eklenirse:
`("Kaynaklara göre amaç, Osmanlı ve korsan gemileriyle savaşmak ve Hristiyan esirleri kurtarmaktı; aynı savaşlarda Müslüman esirler de alınır, ganimet ve esir satışının Livorno'yu zenginleştirdiği yazılır.", None, "○/H M4b:b21,b22,bM6 + genel bilgi (teyit)")`

---

### c13 — İki Kraliçe

**[K4] c13s28 · "Henri IV" sayı olarak okunmaz.** Romen regex yalnız "IV." + büyük harf kalıbını yakalıyor; "Henri IV öldürüldü"de "IV" ham kalır, TTS "I-V" ya da Latince okuyabilir (çıktıda "Anri IV" doğrulandı). Satır içi değişken:
```
("13 Mayıs 1610'da taç giydi; ertesi gün {Henri IV|Dördüncü Henri} öldürüldü, Marie naip oldu.", None, "◐ Gutenberg Pardoe + Louvre başlıkları M4c:B19–B20")
```
(PRON "Henri → Anri" sonradan çalışır: "Dördüncü Anri".)

**[K3] c13s4 · "Marsilya, 14 yaşında bir gelin."** Yer adı özne gibi okunur ("Marsilya … gelin"). 
```
("Düğün Marsilya'daydı; gelin 14 yaşındaydı.", None, "◐ 14 = hesap bize ait (çeyiz \"yüz bin altın\" ekran kartı)")
```

**[K3] c13s17 · "faturalar kesilmeye başladı"** bu parçada hemen önce c12s31'de ("Viyana fatura kesti") kullanıldı; aynı metafor art arda iki bölümde (P6).
```
("Sonra her şey onun hanesine yazılmaya başladı: çatalı o getirmiş, dondurmayı o getirmiş, topuklu ayakkabıyı da, parfümü de… ve tabii zehri.", None, "◐ M4b:bM9 + M4c:D77 (hepsi \"anlatılır\" düzeyi; mizah a+c)")
```

**[K3] c13s29 · aynı "Ne düşündüğünü bilmiyoruz…" kalıbı** (bkz. c11s22).
```
("Favorisi Concini 1617'de öldürülünce Marie, Blois Şatosu'na gönderildi; 1619'da bir gece oradan kaçtı.", None, "◐ yıllar; Louvre başlığı \"nuit du 21 au 22 février 1619\" M4c:B21–B23 (kalıp tekrarı kaldırıldı; ip/merdiven H söylenmez)")
```

**[K3] c13s38 · P6 → P7 kancası uyuşmuyor.** Kapı "adını gökyüzüne yazdırıyordu" (Galileo 1610) diyor ama c14 Roma'daki Arapça matbaayla (1584) açılıyor; gökyüzü bölümün 12. cümlesinde geliyor. Ayrıca "yazdırıyordu" zamanı Marie'nin 1622+ sahnesinin ardından geriye gidiyor. En küçük düzeltme: kapı c14'ün üç vuruşunu sırayla duyursun (gökyüzü sonda kalır, hâlâ en güçlü görüntü):
```
("İki kraliçe Fransa'da imgesini savunurken, ailenin Floransa'daki kolu Arapça harf kestiriyor, opera sahneletiyor, gökyüzüne de adını yazdırıyordu.", None, "YORUM + ◐ c14 (K3 uyarlaması: c14'ün üç vuruşunu sırayla önceden duyurur — matbaa 1584, Euridice 1600, Galileo 1610)")
```

*Kontrol edilen, sorun çıkmayan:* Catherine/Marie tarihleri (13 Nisan 1519, 1533, 1559, 1572, 1581, 1589, 1600, 1610, 1617/1619, 1630/1631, 1642); Britannica kalıbı (liderlerin öldürülmesi onaylandı, katliam büyük olasılıkla değil) hedge'li; çatal/dondurma/ayakkabı/parfüm "anlatılır" düzeyinde ve mit çürütülüyor ✓; Balet comique 15 Ekim 1581 ✓; çeyiz 600.000 écu "borçtan düşüldüğü yazılır" ✓; Rubens/Siegen, Louvre galerisi ✓; 1572 ve Marie'nin yoksulluğunda mizah yok ✓. (s20 "Bir ülke inceliğini de günahını da tek bir yabancıya yazmış" bir ulus hakkında genelleme — K3 küçük, kimlik tahsis edilmedi; istenirse "Hem inceliği hem günahı tek bir yabancıya yazmak, pratik bir düzendi.")

---

### c14 — Yıldızlar, Notalar, Taşlar (P7 açılışı)

**[K3] c14s1 · "Cosimo'nun oğlu Kardinal Ferdinando" — hangi Cosimo?** P7'ye c12'yi görmeden gelen izleyici Cosimo il Vecchio sanar; ayrıca yeni kuşakta üç Ferdinando var (kardinal/I; II; prens).
```
("16. yüzyılın sonunda Roma'da, Papa XIII. Gregorius'un desteğiyle ve Büyük Dük Cosimo'nun oğlu Kardinal Ferdinando'nun himayesinde, bir Medici Doğu Dilleri Matbaası kuruldu.", None, "◐ M3:K66,D5 (Roma'da, Floransa'da DEĞİL; yıl 1584 HUD'da); P7 açılışı: hangi Cosimo")
```

**[K3] c14s3 · "Sonra İstanbul'dan bir ferman çıktı" kronolojiyi bozar.** Ferman **Ekim 1588** (M3 #68), Arapça İncil 1590–91, Kanun 1593, Öklid 1594; "Sonra" fermanı baskılardan sonraya koyuyor. (Ferman Branton ve Orazio Bandini'yi korur ✓ M3 #59; web'de ferman 1587/1588 ayrışır ○.)
```
("Daha bu baskılar çıkmadan, İstanbul'dan bir ferman çıkmıştı: III. Murad, Arapça ve Farsça kitap getiren iki Avrupalı tüccarı koruma altına alıyordu; yasak değil, koruma.", None, "◐ M3:K68,C59,D9 (Ekim 1588; Arapça İncil 1590–91; \"Sonra\" yanıltıyordu)")
```

**[K4] c14s22 · `Scipione` → "Şipyone"** (İtalyanca "sci" = ş; şimdi okunuşu "Sipione/Skipione" riskli).
```python
(r"\bScipione\b", "Şipyone"),
```

*Kontrol edilen, sorun çıkmayan:* Matbaa 1584 Roma/Gregorius XIII/Granjon; Opificio (1588, Uffizi); Euridice 6 Ekim 1600, Peri/Archilei, "günümüze tam ulaşan en eski opera", Caccini altı hafta; Galileo 7 Ocak–13 Mart 1610, Sidereus Nuncius, Marius adları; 1633 Dialogo II. Ferdinando'ya ithaf; Cristofori 1700 envanteri, 1711 Maffei, üç piyano. Piyano mizahı kuruma dönük. 1633 sahnesi süssüz ✓. Bandini göz kırpması (s4) P4'ten haftalar sonra izleyen için zayıf kalır ("Giuliano'nun katili"); isteğe bağlı "1478'de Giuliano'yu vuranla".

---

### c15 — Son Medici'ler

**[K1] c15s13 · "bu anlatı tek bir kaynak hattına dayanıyor".** Bu ifade Medici literatürü hakkında bir **iddia**; araştırmadaki dayanak (M4b:bM12) yalnızca *bizim* kaynak hattımızın (EN Wikipedia + aynaları) tek olduğunu söylüyor — "çöküş" tezi Acton'dan Galluzzi'ye uzanan geniş bir literatürde işlenir. Araştırma sınırı seste literatür bilgisi gibi çıkıyor; yayını engeller. Dayanak olan tek sektörel nüans (yün geriler, ipek gelişir; M4b:b64 akademik özet ○) korunarak:
```
("III. Cosimo elli üç yıl hüküm sürdü; dönemi çoğu anlatıda gerileme diye geçer, ama bu tablo her sektör için aynı değildi: yün geriledi, ipek gelişti diye yazılır.", None, "◐/○ M4b:b63,b64,bM12 (bir akademik özet; \"tek kaynak hattı\" iddiası KALKTI — o, araştırma sınırımızdı, literatür bilgisi değil)")
```

**[K2] c15s2 · "birkaç gün arayla".** Francesco **19 Ekim**, Bianca **20 Ekim 1587** (EN Wikipedia, italyonthisday ◐) → bir gün arayla. Araştırma "bir gün arayla"yı HAFIZA'da tutup hedge için "birkaç gün"e çevirmişti; hedge yanlış yöne gidiyor.
```
("Ekim 1587'de Francesco, eşi Bianca Cappello'yla bir gün arayla öldü.", None, "◐ Francesco 19 Ekim, Bianca 20 Ekim (EN Wikipedia; italyonthisday) M4b:b50 — \"birkaç gün\" yanlıştı")
```

**[K2] c15s3 · "ilk anlatıcısı bilinmez"** (c12s23'teki aynı sorun: araştırma sınırı literatür gibi).
```
("Zehir söylentisinin o günlerde dolaştığı söylenir; zehirli turta hikâyesi ise sonradan anlatılmıştır, ilk anlatıcısını gösteremiyoruz.", None, "H / ANEKDOT M4:3E#3,§5.15 (\"ilk anlatıcısı bilinmez\" = araştırma sınırı)")
```

**[K2] c15s19 · "Erkek hat kapanmıştı".** Docstring'e göre "Son Medici" yalnız Toskana'yı yöneten hat; Ottajano kolu ayrı ○. Cümle bunu söylemiyor; c16 docstring'i "Tüm Medici'ler bitti DENMEZ" der. 
```
("Toskana'yı yöneten erkek hat kapanmıştı; geriye bir kadın ve imzalanacak bir sözleşme kalmıştı.", None, "◐ M4b:b68,b73 (K1 → c16; Ottajano kolu ○ — \"tüm Medici'ler bitti\" çağrışımı kaçınılır)")
```

*Kontrol edilen, sorun çıkmayan (özellikle sorulanlar):* **2026 DNA çalışması doğrulandı** — iScience, Pisa Üniv. + Yale; Francesco'nun **üç kaburgası**, kardinal Giovanni'nin bir kaburgası; Francesco'da *P. falciparum* + *P. malariae* (iki tür) ✓, "iki sıtma parazitinin DNA'sı" doğru; 2004'te mezar açılırken ayrılan örnekler; 2006 arsenik (Mari ve ark.) ve 2010 antijen (Fornaciari/Giuffra) künyeleri uyumlu. CNN manşeti "may be solved" gerçek ("çözülmüş olabilir"). **Livornina 1593, Mustafa Ağa 1598** (Mercan 2023: Mehmed III ve Halil Paşa mektupları, müzakere başarısız ✓), **Fahreddin 1608 anlaşma / 1613 geliş** ✓, Gian Gastone 1723/1737, **Francis Stephen yalnız bir kez (Ocak–Nisan 1739)** ✓. Mizah ölüm sahnelerinde yok; "iki ayrı kesinlik" (s6) kusurlu sözcük (biri hedge'li) — "kesinlik düzeyi" daha doğru (küçük).
*Ritim notu:* ortalama 18,5 söz/cümle (üst bant), s8–s10 (25-24-20) Ferdinando bloğu isim yoğun; "yorgun" ruh haline uyuyor, ama P7 sonunda dinleyici yorgunluğu için c15s9–s10 bölünebilir (öneri yazılmadı).

---

### c16 — Hesap

**[K2] c16s2 · "bedeni açılmasın istemiş; istediği yerine gelmemiş".** Dayanak blog zinciri (○, M4b:b79); "istediği yerine gelmemiş" ise mezarda iç organların ayrı kapta bulunmasından **bizim çıkarımımız** (embalmlama âdeti de bunu verir). Sahnenin en kırılgan satırı. Hedge ve çıkarım düşürülmüş sürüm (ya da tümüyle sil, opsiyonel zaten):
```
("Bir anlatıya göre, bedeninin açılmamasını ve yüzüyle ellerinin yalnız nedimelerince yıkanmasını istemiş.", None, "○ M4b:b79,bD26 (blog zinciri; birincil görülmedi; \"istediği yerine gelmemiş\" ÇIKARILDI — kaynağı yok)")
```

**[K3] c16s3 · sözleşmenin tarihi söylenmiyor.** c15 "imzalanacak bir sözleşme" der, c16 1743'te açılıp "Sözleşmeye …" diyor; altı yıllık sıçrama ve (P7'ye c0'ı görmeden gelen için) hangi sözleşme belirsiz. 26 söz:
```
("31 Ekim 1737'de imzalanan sözleşmeye çoğu zaman bağış denir; bir akademik yoruma göre ise o bir devir koşuluydu: Lorraine mülkiyeti alırken eserlerin Floransa'dan çıkarılamayacağını kabul ediyordu.", None, "◐ \"devredilemezlik\" / ○ akademik yorum tek özet M4b:b75,bM13,D11 (\"bir yoruma göre\"; \"bağışladı\" DENMEZ; tarih c0 ile tutarlı)")
```

**[K2] c16s9 · "Primavera … siparişiydi".** Primavera'nın Lorenzo di Pierfrancesco için yapıldığı **büyük olasılıkla** doğru (1499 envanteri dayanaklı çıkarım); sipariş belgesi yok.
```
("Kubbeyi yün loncası yaptırdı; Strozzi, Rucellai, Tornabuoni da sipariş verdi; Primavera bile büyük olasılıkla ailenin başka bir kolunun siparişiydi.", None, "◐ M3:D1,K18,K20,K44,§5.13; M3b:b83,b87 (Primavera: 1499 envanteri → \"büyük olasılıkla\")")
```

**[K2] c16s19 · Harvard'daki defterler.** Baker Library'nin Medici malzemesi Selfridge Koleksiyonu: "ailenin **bir kolunun** altı kuşaklık hesap defterleri" (1918 Christie's, 1927 Harvard); "bankanın defterleri" denirse hata olur.
```
("Medici defterlerinin bir kısmı bugün Floransa Devlet Arşivi'nde, bir kısmı Harvard'da.", None, "◐ M1:D50 (Baker Library, Selfridge Koleksiyonu = ailenin bir kolunun hesap defterleri; \"banka defteri\" DENMEZ)")
```

*Kontrol edilen, sorun çıkmayan:* 18 Şubat alayı + belediye müzeleri ücretsiz (Comune/Finestre sull'Arte ◐); Pact'ın 31 Ekim 1737'si; Pact'in uygulanışı için "bilmiyoruz" dürüst (arama: Lorraine'in Viyana'ya taşıma kanıtı bulunamadı). "Çifte kayıt/ilk müze/Fugger–Rothschild" mit düzeltmeleri doğru yönde. **1737/1743:** tutarlı (c0: 31 Ekim 1737; 18 Şubat 1743).
*Küçük (yedeksiz):* s8'de “…” tırnakları kaynak alıntısı gibi okunur (USLUP §3: tırnak içi kaynaklıdır) — "Kaynaklar onu tek yaratıcı değil, en görünür patronlardan biri olarak anlatıyor." biçimi tırnaksız daha tutarlı; s21 "çürüttüğümüz" fazla zafer dili ("ayıkladığımız"); s16 "Capitoline ondan önce açılmıştı" belirsiz (halka açılış 1734 ↔ Uffizi 1769 kastediliyor: "ondan önce halka açılmıştı").

---

## 3. Parça sınırı kancaları ve parça açılışları

| Sınır | Durum | Düzeltme |
|---|---|---|
| **P2→P3** (c5s21 "Şimdi listenin sahibine, Lorenzo'ya bakalım." → c6s1) | Ardışık akıyor; P3 tek başına açılıyorsa Lorenzo/Floransa belirsiz | c6s1–s2 (yukarıda) |
| **P3→P4** (c7s47 "…barışı o sabah ölmüştü." → c8s1 aforoz) | Ardışık çok güçlü; c8 tek başına: kim/neden belirsiz, gün riski | c8s1 (yukarıda); c7s46 "o sabah" düzeltilince kapı da temizlenir |
| **P4→P5** (c9s28 "kralın Alpler'i aşması, rahibin vaazları" → c10s1) | Ardışık akıyor (rahip s4'te geliyor); kral c10'da hiç adlandırılmıyor; c10s1 soyadsız | c9s28, c10s1, c10s12 |
| **P5→P6** (c11s37-38 "otuz yedi yıl hüküm sürecekti. Nasıl?" → c12s1) | Çalışıyor ama c12s1 aynı olguyu bağlamsız tekrar ediyor (bilinçli); "Nasıl?"ya cevap s2–s4'te örtük | c12s1 (yer/aile eklendi) |
| **P6→P7** (c13s38 "gökyüzüne yazdırıyordu" → c14s1 Roma matbaası) | **Uyuşmuyor**: kapı gökyüzü vaat ediyor, bölüm matbaayla açılıyor | c13s38 (üç vuruşu sırayla duyurur) + c14s1 (hangi Cosimo) |
| **P7 sonu** (c16s25) | Güçlü, kapanış sessiz; mezar/alay tutarlı | — |

---

## 4. Okunuş (PRON) — toplu liste

```python
# scr_c8.py    (Bargello kimlik eşlemesi VAR → değiştir)
(r"\bBargello\b", "Barcello"), (r"\bPoggio Imperiale\b", "Pocco İmperyale"),
# scr_c9.py
(r"\bRaymond\b", "Reymond"),            # "de Roover"→"de Rover" c2 ile tutarlı kalsın
# scr_c11.py
(r"\bMainz\b", "Mayns"), (r"\bLuther\b", "Lüter"), (r"\bFabrizio\b", "Fabritsyo"),
(r"\bFerruccio\b", "Ferruçço"),         # mevcut "Ferruççio"nun yerine
(r"\bCastel\b", "Kastel"),              # "Castel Sant'Angelo" girdisinden SONRA
(r"\bd'Este\b", "deste"),
# scr_c12.py
(r"\bMugello\b", "Mucello"),
# scr_c14.py
(r"\bScipione\b", "Şipyone"),
# scr_c7.py (düşük öncelik; mevcut kimlik eşlemesi "Maffei"nin yerine)
(r"\bMaffei\b", "Maffey"),
```
Ayrıca: **c13s28** "Henri IV" satır içi `{Henri IV|Dördüncü Henri}` (Romen regex'i yakalamıyor). Doğrulanan, sorunsuz olanlar: sayı→söz dönüşümü ve ünsüz uyumu (bin dört yüz altmış dokuzda / yetmiş beşte / seksen birde / iki bin yirmi üçte), Romen sıra sayıları (II. Pius, XIII. Gregorius vb.), "19. yüzyıl", `de' `→"de ", Giostra→Costra, Culyano, Politsyano, Lorentso. Düşük riskli, öneri yok: Opificio ("Opifiçyo" fazladan y), "gonfaloniere" (isteğe bağlı "gonfalonyere").

---

## 5. Ton / üslup / kaynak sınıfı — kısa notlar (yedeksiz)

- **Mizah kapalı sahneler:** ihlal bulunmadı (c7 tüm bölüm; c8 Bandini/Otranto; c10 V1/V4/V7; c11 V1/V4–V8; c12 1562/Lepanto/ölüm; c13 1572/Köln; c14 1633; c15 Francesco-Bianca/Gian Gastone). Sınır vakalar: c7s14 "şakalaştıkları" (aktarılan olgu), c14s4 Bandini göz kırpması (katil soyadı üzerinden — katille ilgili, kurbanla değil), c15s6 iki manşet (basına yönelik).
- **Uydurma iç dünya / diyalog:** yok. Tırnaklar kaynaklı (Machiavelli, Guicciardini "palle", papalık bülteni Latince çevirisi "aktarıldığına göre"). Kalıp ("Ne düşündüğünü…") yalnız kaynaksız iç dünyayı reddetmek için kullanılıyor ✓.
- **Kalıp tekrarı:** bkz. c11s22/c13s29 (kalıp 4 bölümde kelimesi kelimesine). "…'e göre" atıfları da yığılıyor: "Britannica'ya göre" ×3 (c10s29, c11s15, c13s13; ayrıca "Louvre'a göre" c13s33), "Treccani" ×7 — ansiklopedi sesi "uzak profesör"e yaklaşabilir; bazılarını "kaynaklara göre"ye çevirmek serbest zevk.
- **Sayı yoğunluğu:** USLUP "bölüm başına söylenen ≤6" fiilen aşılmış (rakam öbeği: c12 31, c13 30, c11 22, c8/c10 18, c15 18). Tarihler harfle okunduğu için kulakta ağır; c12s6'daki "üç 29" bilinçli ve işe yarıyor; c12s32 (27 söz, 4 sayı) en yoğun cümle.
- **Ritim:** hiçbir cümle 28'i aşmıyor (azami 28: c6s16). Ortalamalar: c15 18,5 üst bant; c11 16,1; c6/c12 15,6. Uzun cümle yığılması: c15s8–s10, c11s1/s4/s5.
- **Kaynak etiketi–metin uyumsuzlukları:** c6s22 (○ "anlatılır" ama düz), c11s6 (○ "anlatılır" ama düz); c8s9 mizahı ○ olgu üzerine kurulu (kabul, etiket belirtiyor). ● hiçbirinde yok (beklenen).
- **Bakım:** `scr_c7.py` docstring "Parça 2'nin soğuk açılışı" → P3'ün 2. bölümü; `scr_c12.py` "Parça 3'ün soğuk açılışı" → P6; `script.py` başlık "P1 = c0–c6 …" eski bölümleme; c12 docstring'indeki "2026 DNA GİRMEZ" artık güncel değil (yukarıdaki c12s24).

---

## 6. Doğrulanan / sorun çıkmayan kilit olgular (WebSearch, ◐/○)

2026 iScience sıtma DNA'sı (Francesco 3 kaburga + Giovanni 1; *P. falciparum* + *P. malariae*) · 2010 antijen çalışması (Eleonora, Giovanni, Garzia, Francesco) · Francesco 19 / Bianca 20 Ekim 1587 · Mustafa Ağa 1598 (Mercan 2023; müzakere başarısız) · Hanno yazıtı Leo'nundur; Hanno 8 Haziran 1516 · 1513 conclave iki oylama · Alfonso d'Este Leo'nun atını yedekten yürüttü (Schaff/Pastor) · Eleonora: 29 Mart sözleşme+vekâlet, 29 Haziran giriş, 29 Temmuz düğün (Reiss) · Maffei itirafı 2023 (Simonetta, ASF, 3 Mayıs 2023) · Bandini 29 Aralık 1479 Bargello (Louvre) · Londra >£26.000 toplam / £10.500 (Cambridge/popüler) · Dall'Aglio (Lorenzino 1548) · Francis Stephen 1739 tek ziyaret · 18 Şubat alayı ve ücretsiz müzeler · Harvard Selfridge Koleksiyonu · Machiavelli ithafı: Vettori mektubu Giuliano'ya, basılı ithaf Lorenzo di Piero'ya.

---

## 7. Kullanıcıya YAYIN ÖNCESİ TEYİT listesi (sayfa düzeyinde, 15 kalem)

1. **Raffaele Riario'nun yaşı** (3 Mayıs 1461 doğum → 16; Treccani "17") — DBI Riario Sansoni (c7s3).
2. **Aforoz ve interdikt günleri** (1 Haziran bülten mi, kesin karar mı; interdikt günü) — Sixtus IV'ün üç bülteni (kritik baskı), Reumont, EdP Sisto IV, DBI Lorenzo (c8s1).
3. **Giuliano'nun doğum günü/yaşı** (25 ya da 28 Ekim 1453 → ölürken 24) — DBI Giuliano, Enc. machiavelliana (c6s27).
4. **Londra şubesinin Edward IV kredileri** (>£26.000 toplam ↔ £10.500 kalan) — Holmes, "Lorenzo de' Medici's London Branch"; de Roover 1963 (c9s11).
5. **Sassetti'nin genel müdürlük başlangıcı** (1463 DBI ↔ 1458/59) ve **Goldthwaite**'in banka krizi yargısı — DBI Sassetti; Goldthwaite 2009 (c9s17–s18).
6. **Valori'nin Vita'sı** (üvey ana, ten, koku) — özgün metin/1991 baskısı (c6s1–s4).
7. **Bandini zinciri** (8 Mayıs 1479 mektup, 14 Temmuz, 24 ve 29 Aralık) — DBI Bandini + DBI Carducci + Louvre (c8s14–s18).
8. **Mehmed II 3 Mayıs 1481, Otranto 10 Eylül 1481** (HAFIZA-Y) — Osmanlı/Türk kaynağı (c8s32).
9. **Alfonso d'Este ve Leo X'in possesso'su** — Pastor, *History of the Popes* IV (Schaff'ın atıf yeri) (c11s6).
10. **Eleonora–Cosimo tarihleri** (29 Mart / 29 Haziran / 29 Temmuz) — Reiss (Italian Art Society), Uffizi/Comune; Wikipedia yalnız 29 Mart (c12s6–s7, punchline'ın dayanağı).
11. **Garzia/Giovanni sıtma kanıtı** — Trans R Soc Trop Med Hyg 104:583–587 (2010) ve iScience 2026 makale metni (kaç kaburga, hangi örnek, Garzia dahil mi) (c12s24, c15s4–s5).
12. **Francesco I / Bianca ölüm günleri** (19/20 Ekim 1587) — DBI Francesco I, Bianca Cappello (c15s2).
13. **Mustafa Ağa 1598 elçiliği** (başarısızlığın gerekçesi) ve **Orazio Bandini/Branton 1588 fermanı** (ferman yılı 1587/1588) — Mercan 2023 (Annali ISIG Trento); Osmanlı basım tarihi çalışması (c14s3, c15s10).
14. **Vasari Koridoru/Uffizi 1565, Uffizi'nin 1769 halka açılışı** — Uffizi resmî sayfası (c12s14–s15, c16s20).
15. **Lepanto'da Toskana'dan 12 gemi** (papalık hizmeti/kiralık iki anlatım) ve **Santo Stefano'nun amacı** — M4b:b28,T17; Türk/Venedik kaynağı (c12s32).
