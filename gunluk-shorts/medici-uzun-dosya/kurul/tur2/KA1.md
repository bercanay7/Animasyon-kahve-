# KA1 — TUR 2 · Kaynak ve doğruluk (veto) · Mercek: KONU UZMANI (olgu ve sayı denetimi)
Medici Parça 1 v2 · **1. aşama: anlatım + kaynak + paket metni.** Ekran metni ve görseller 2. aşamada (v2 render çıkınca) ayrıca puanlanacak; ekran için veto hakkım açık.

## 1. Karar (şimdilik)
**ONAY — 9,0/10** (anlatım 9,5 · kaynak kapısı 9,5 · paket metni 8,5, aşağıdaki iki ücretsiz düzeltmeyle 9,5).
- Tur 1'deki üç anlatım hatası (Parks, Salvestro, veba) ve isteğe bağlı üç yama (c1s23, c1s24, c2s27) doğru biçimde kapanmış.
- Başkanın ek yamaları (c1s10, c2s20, c2s21) birincil ya da otoriter metinle birebir uyuşuyor.
- Söylenen metinde bilinen bir olgu hatası kalmadı.
- Paket metninde iki kaynak beyanı düzeltilmeden yayına çıkılmamalı (N1–N2). İkisi de yalnız metin düzeltmesi, render gerektirmez.

**Sınırlarım:** Sesi dinleyemedim, videoyu oynatamadım. "Söylenen = yazılan" kararı `script.py` çıktısına ve `out_p1/hizala_asr_kosular.txt` / `hizala_asr_rapor.json` (ASR) ölçümlerine dayanıyor. Bu turda birincil metinlere `curl` ile eriştim:
- KAY'ın indirdikleri: de Roover tam metni, DBI Giovanni di Bicci, Machiavelli III–IV İtalyanca, Stefani (*Delizie degli eruditi toscani* XIII), Cavalcanti.
- Benim indirdiklerim: DBI "Villani, Giovanni"; Casciu 2006 (storiadifirenze.org); Italia Nostra 2017 afişi; it.wikipedia "Anna Maria Luisa de' Medici" ve "Gian Gastone"; en.wikipedia "Palla Strozzi"; Brown Üniversitesi *Online Catasto of 1427*.
- Hepsi HTTP 200 döndü (scratch: `…/scratchpad/ka1t2/`, `…/scratchpad/kay/`).

## 2. Tur 1 maddelerimin durumu

### Anlatım yamaları (yeniden seslendirilen 12 cümle)
| Tur 1 | Durum | Kanıt |
|---|---|---|
| **K1** Tracy → Tim Parks (c2s7) | **KAPANDI** (anlatım, SRT, açıklama) | ASR 379,32 sn "Tim Parks'ın aktardığına göre"; SRT 6:19. İçerik ●: de Roover, "discrezione was a free gift and not a contractual obligation". Parks atfı ◐ (kitap okunmadı). Açık kalanlar: ekran plakası koddan "TİM PARKS" görünüyor, v2 karesiyle teyit edilecek; `YAYIN_TASLAK.md:38` hâlâ "Tracy Parks" (N10); açıklamadaki yeri yanlış (N1). |
| **K2** "…ve Salvestro çekildi" (c1s18) | **KAPANDI** | Cümle "…Michele di Lando, gonfaloniere oldu." ile bitiyor (ASR 234,91–244,01 sn). ● Machiavelli III: "i nuovi Signori … de' quali era gonfaloniere Luigi Guicciardini". DBI "Michele di Lando": "il 22 luglio … il palazzo fu invaso dalla folla che lo elesse a gonfaloniere". c1s16 de düzeldi (ASR 219,69–227,23 sn), bkz. alt tablo. "ÇEKİLDİ" plakası koddan kalkmış, v2'de teyit edilecek. |
| **K3** veba "Temmuz'a kadar" (c1s11) | **KAPANDI** | "yaz boyunca şehri bırakmadı" (ASR 181,38–186,35 sn). ● Stefani, Delizie XIII, Rub. 634: "Quella pistolenza cominciò di Marzo … e finì di Settembre". Boccaccio: "Mart–Temmuz". Yeni cümle iki kaynakla da doğru. Ekran "MART 1348 · YAZ BOYUNCA" (kodda), v2'de teyit edilecek. |
| **V4** "Medici adı … kademe altında" (c1s24) | **KAPANDI** | "Medici'nin bu kolu…" (ASR 277,80 sn). ● DBI Giovanni: "si collocavano, nel Trecento, al di sotto dell'élite cittadina, e vivevano delle rendite patrimoniali nel contado". |
| **V5** "en kanlı günlerinden biri" (c1s23) | **KAPANDI** | Yeni cümle "Yün işçilerinin kısa ömürlü loncası kaldırıldı; yönetimden de dışlandılar." (ASR 271,72–276,55 sn). ● Machiavelli III: "Annullorono ancora l'Arte del popolo minuto, e i subietti a quella … degli ufici privorono". |
| **V6** "büyük torunu" (c2s27) | **KAPANDI** | "torununun oğlu Lorenzo" (ASR 524,74 sn). ● DBI: "secondo il bisnipote Lorenzo il Magnifico lasciò un patrimonio di circa 180.000 fiorini". |
| **V3** "XXIII. Johannes … papa oldu" | **KISMEN** | Anlatım bilinçli olarak değişmedi; tur 1'de kabul edilebilir basitleştirme demiştim. Ekran plakası koddan "PİSA PAPASI · BUGÜN KARŞI PAPA SAYILIR" görünüyor, v2'de teyit edilecek. Pakette DBI maddesinin adına "karşı papa" eklenmesini öneririm (küçük, ücretsiz). |
| **S3** çeyiz sıralaması (c1s27) | **KABUL, açık-küçük** | DBI: çeyiz 1385'te ("ne divenne socio investendo i 1.500 fiorini avuti in dote"), devralma 1393. Anlatım tarih vermiyor ama sıra tersten okunabilir. Ses yaması gerekmez; ekranda "1385 · ÇEYİZ" gibi küçük bir etiket yeterli. |
| **S5** "Loren tarafı" | **KABUL** | Değişiklik gerekmez. |

### Başkanın ek yamaları ve sınaması
| Cümle | Sonuç | Kanıt |
|---|---|---|
| **c1s10** Villani Peruzzi ortağı | **● doğru; nüans var** | DBI "Villani, Giovanni" (Zabbia): "collaborava con la compagnia dei Peruzzi della quale divenne socio dal maggio 1300". Ortaklığı Roma 1300–01, Brugge/Gent 1302–07 dönemini kapsıyor; 1308'de Floransa'ya döndü. 1322'den itibaren Buonaccorsi ortağı; bu şirket 1341'de battı, Villani 1346'da hapse girdi. "Kaybedenlerin içindendi" sonucu doğru (1340'lar çöküşünün iflasçılarından). "Yani" ile Peruzzi ortaklığına bağlanması ise gevşek: 1343'te Peruzzi ortağı değildi. Ses yaması gerekmez; ekranda düzeltme önerisi N4'te. |
| **c2s20** aforoz tehdidi (de Roover n. 45) | **● doğru; KAY'ın "aforoz yok" hükmünün düzeltilmesi yerinde** | de Roover metni: "Giovanni di Bicci held as security a rich bejeweled miter belonging to Pope John XXIII (Baldassare Cossa) and later claimed by the latter's successor, Martin V." Dipnot 45: "Pope Martin V had to threaten Giovanni di Bicci with excommunication if he failed to obey and restore the pledge. Giulia Camerani Marri … (1951), p. 32, Nos. 48-49". DBI: "custodì gli oggetti preziosi (fra cui due mitre) posti a garanzia". "De Roover'ın andığı belgelere göre … zorunda kalmıştı" kipi birebir ("had to"); belgeler okunmadığı için "andığı" ifadesi tam doğru çerçeve. |
| **c2s21** kasa memurluğu | **● doğru** | DBI Giovanni: "con la nomina di Bartolomeo Bardi a depositario della Camera apostolica (1422). Da allora, i Medici mantennero la carica per 22 anni consecutivi e per altri 18 a intermittenza". |
| **c1s16** Mayıs, kura | **● / ◐** | Machiavelli III: "Correva allora lo anno 1378, ed era il mese di aprile … potendo nella seguente Signoria essere facilmente Salvestro de' Medici gonfaloniere" ve "Fu tratto per tanto gonfaloniere Salvestro di messer Alamanno de' Medici". "Mayıs", nisandan sonraki Signoria'dan (1 Mayıs–30 Haziran) türetilmiş; Guicciardini'nin 1 Temmuz'da göreve başlamasıyla tutarlı. |
| **c1s26** "Roma'da" ve **c2s1** "Çözüm," | **KAPANDI** | ASR'de var: 291,91–292,46 sn "Roma'da"; 342,91–343,39 sn "Çözüm". |

**ASR (söylenen = yazılan):** üç bölümde de "eksik_sozcuk" boş, yani seste bulunmayan sözcük 0. Jeton eşleşmesi c0 %98,3, c1 %97,4, c2 %96,6. Yamalı 12 cümlenin hepsi tam kanıtla eşleşiyor. Eşleşmeyen dört bölge orijinal kayıtta; ASR yanlış duymuş olabilir. Kulak listesi için bkz. N7.

### Ekran / görsel maddelerim (G1, G2, V1, V2, V7, V8, V9, S1, S2, S4, S6)
**v2 render bekleniyor, 2. aşamada kare kare bakılacak.** Kodda görülenler, teyit değildir:
- dönem katmanı (`donem.py`);
- "ŞUBE SAYILARI TEMSİLÎ", "ARMALAR TEMSİLÎ";
- "150.000+ fl.";
- 1407 VENEDİK kalkmış;
- abaküs yerine yazılı rakam;
- 1737 koridor figürleri silüet.

Paketteki kapak K2'de keseye asılı palle mavi topsuz, yani Giovanni dönemine uygun. G2'nin paket tarafı bu nedenle temiz.

### Tur 1'de "erişilemedi" kalan olgular, bu turda kapandı
| Cümle | Önce | Şimdi | Kanıt |
|---|---|---|---|
| **c0s8** "13 madde, Fransızca" | erişilemedi | **●** | Casciu 2006 (*La Principessa saggia*, Palazzo Pitti kataloğu, s. 30–57): "Nei suoi tredici articoli redatti nell'originale in francese e quindi tradotti in italiano e ratificati" (art. I–XIII tek tek sayılıyor). Italia Nostra 2017 afişi: "Articolo III – Traduzione in italiano dell'originale in francese". |
| **c0s11** "üçüncü madde" | erişilemedi | **●** | Casciu 2006: "il celebre articolo iii" |
| **c0s4** "yabancı birliklerin elindeyken" | ◐ (1737 için yok) | **● / ◐** | it.wikipedia AML: "nel gennaio del 1737 le truppe spagnole … furono sostituite da 6.000 soldati austriaci". Casciu 2006: "generale Wachtendonk, comandante delle truppe austriache in Toscana, del luglio 1737". |
| **c1s19** "kamu borcunun azaltılması" | ○ (okunan metinde yok) | **◐ / ●** | Machiavelli III, Ciompi talepleri: "che il Monte fermasse gli interessi, e solo i capitali si restituissero" (yeni loncalar ve küçük borçlara erteleme de sayılıyor). "Vergide adalet" ◐ kalır; "yazıldığına göre" kipi doğru. |
| **c2s23** "137 hane ≈ %30; en zengin Strozzi" | ○ | **●** | Bkz. §3 Catasto. |

## 3. Catasto rakamları (başkanın ek sorusu)
Kaynak: **Brown Üniversitesi, *Online Catasto of 1427*** (yay. Herlihy, Klapisch-Zuber, Litchfield, Molho). Bu, 1427 kadastro kayıtlarının akademik veri tabanı; tam metin ve liste okundu.

| Rakam | Karar | Not |
|---|---|---|
| **9.780 hane** | **●** | "the total 9,780 households assessed" |
| **137 hane / %29,8** (anlatım: "bir hesaba göre … yaklaşık yüzde otuzunu"; ekran: "%29,8") | **●** | "These are the 137 households in Florence (1.4%) with 10,000 florins or more of total assessment in 1427 … had 3,000,672 florins of total assessment (29.8% of the total 10,081,080 florins assessed in the city)". "Kayıtlı servet" = "total assessment", doğru karşılık. "Bir hesaba göre" kipi artık gereğinden ihtiyatlı ama zararsız. |
| **En zengini Palla Strozzi** | **●** | Aynı veri tabanında zenginlik sırası: 1. Palla di Nofri Strozzi **162.906**; 2. Francesco di Simone Tornabuoni 109.333; 3. Giovanni di Bicci Medici 91.089. |
| **Strozzi "162.925 FLORİN · BRÜT"** (ekran) | **◐ — küçük tutarsızlık** | en.wikipedia "Palla Strozzi": "gross taxable assets of 162,925 florins in 1427", dipnot Crabb 2000, okunmadı. 137/%29,8 Online Catasto'dan alındığı için ekran da aynı tablodan **162.906** göstermeli ya da "≈163 BİN" yazmalı; iki ayrı kaynaktan iki kesin sayı karıştırılmasın. Ücretsiz; 2. aşamada karede bakılacak. |
| **Uyarı (2. aşama)** | — | Ekranda Giovanni için "ikinci en zengin" yazılırsa yanlış olur: Online Catasto toplam değerlendirmesinde **üçüncü**. DBI ve de Roover'ın "ikinci" dediği **vergi yükü** ("secondo cittadino più tassato"). Gerekirse "EN ÇOK VERGİ ÖDEYEN İKİNCİ" yazılmalı. Anlatım böyle bir iddia taşımıyor. |

## 4. Yeni sorunlar (bu turda)
| # | Yer | Bulgu | Ne yapılmalı | Önem |
|---|---|---|---|---|
| **N1** | `studio_paketi_P1/02_aciklama.txt`, KAYNAKLAR | Başlık "(bu parçada gerçekten okunanlar)", ama altında **Tim Parks, Medici Money** var. Kitap okunmadı; KAY §5 "açıklamaya yazılmasın" demişti. Kaynak beyanı olarak yanlış. | Başlığı "KAYNAKLAR" yap ya da Parks'ı ayrı satıra al: "Anlatımda anılan (kitap okunmadı; aynı bilgi de Roover'da doğrulandı): Tim Parks, *Medici Money* (2005)". | **önemli: yayından önce, ücretsiz** |
| **N2** | aynı liste + `03_sabit_yorum.txt` | Sabit yorum "Rakamlar ve tarihler açıklamadaki kaynaklara dayanır" diyor. Ama "13 madde / Fransızca" ve "137 hane / %30" listedeki hiçbir kaynakta yok; bu turda başka iki kaynakta bulundu. | Listeye ekle: **Stefano Casciu, "Principessa di gran saviezza"…, *La Principessa saggia* (Livorno 2006), s. 30–57** ve ***Online Catasto of 1427*, Brown University (Herlihy–Klapisch-Zuber verisi)**. Eklenince sabit yorumdaki cümle doğru olur. | **önemli: yayından önce, ücretsiz** |
| **N3** | Ekran (2. aşama) | Strozzi 162.925 ↔ 162.906; Giovanni'nin sırası | §3'e bak | küçük |
| **N4** | Ekran c1s10 plakası (koddan "GIOVANNI VILLANI · PERUZZİ ORTAĞI (1300'DEN)") | "1300'DEN" ortaklığın iflasa kadar sürdüğü izlenimini veriyor. DBI yalnız 1300–1307/08 dönemini belgeliyor; iflasa uğrayan kendi şirketi Buonaccorsi (1341). | "1300'DE PERUZZİ ORTAĞI · KENDİ ŞİRKETİ BUONACCORSİ 1341'DE BATTI". Böylece anlatımdaki "kaybedenlerin içindendi" çıkarımı belgeye bağlanır. | küçük–önemli (ücretsiz) |
| **N5** | Ekran c2s30 plakası (koddan "CAVALCANTI · 1440'LARDA") | DBI "Cavalcanti, Giovanni": *Istorie*'yi hapiste (1420'lerin sonu–1439/40) yazdı, olaylar 1440'a kadar. Anlatımdaki "1440'larda" sınırda (1440 dahil) ◐. | Plaka "HAPİSTE · ≈1440" olsun. Anlatımla çelişmez, daha doğru. | küçük |
| **N6** | Anlatım (kesinleşti; kayıt için) | Ses yaması gerektirmeyen ◐ nüanslar: c1s10'da "yani" bağı (N4); c2s30 "1440'larda"; c1s27 çeyiz sırası; c1s18 "Palazzo Vecchio" adı (1378'de Palazzo dei Priori; anakronik ama zararsız, okuru yönlendiriyor); c2s15 Cossa'ya papalıktan önceki borç, Konstanz'daki suçlama düzeyinde (DBI: "10.000 ducati forniti dai Medici"). | Hiçbiri olgu hatası değil; yalnız kayıt. | — |
| **N7** | `yayin/KULAK_KONTROL_P1.md` | ASR'nin eşleştiremediği orijinal kayıt bölgeleri listede yok: **c2s8 "Faiz değil, hediye."** (389,35–390,85 sn; ASR "FISD / Hediy", espri cümlesi) ve **c1s6 "ona göre"** (140,42–141,02 sn; ASR "O ne gül?"). Ayrıca c1s16'nın taşıdığı tek yeni olgu ay adı; ASR "Mayıs'ında"yı "naysinde" duydu (listede var). | İkisini listeye ekle; c1s16 için kullanıcının kulak onayı şart. | önemli (kulak), olgu iletimi açısından |
| **N8** | 02_aciklama, Stefani satırı | "Rubrica 634" okunan *Delizie* XIII baskısına göre doğru (metinde "Rub. 634"). Rodolico/RIS baskısı ve yaygın İngilizce çeviri (Fordham) "643" numaralar; okur "yanlış numara" sanabilir. | "(Delizie degli eruditi toscani XIII baskısı; RIS baskısında rub. 643)" ekle. | küçük |
| **N9** | 02_aciklama, 2. satır | "5:39'de" | "5:39'da" (otuz dokuz → -da) | küçük (dil) |
| **N10** | `yayin/YAYIN_TASLAK.md:38` | Eski 7 parçalık taslakta hâlâ "Tracy Parks" var; okunmamış Goldthwaite ve Padgett–Ansell da listede. | P2–P7 açıklamalarına kopyalanmadan düzelt. | küçük |
| **N11** | `kaynaklar_P1.md`, `kurul/teyit_P1.md` | Bu turda kapanan maddelerin etiketleri eski. | c0s4, c0s8, c0s11 → ●; c1s19 ○ → ◐/●; c2s23 ○ → ●; c2s30 "○ İngilizce çeviriden dolaylı" → içerik ● (Cavalcanti İtalyanca, Polidori 1838), tarih ◐; c2s10 ○ → ◐ (de Roover "no capital … after 1426"). §4 "erişilemedi" listesinden c0s8, c0s11 ve 137/%29,8 düşülsün. | küçük (belge) |

**Paket metninde doğruladıklarım:**
- Başlık "Faiz Yasakken Nasıl Zengin Oldular?" videonun söyledikleriyle karşılanıyor: kanon hukukunda faiz yasağı (de Roover); 1427'de Giovanni ilk üçte (Online Catasto).
- Açıklamanın ilk paragrafı doğru ve Casciu'nun nüansına uyuyor: III. madde bağış değil, "çıkarılamazlık" şartı.
- "Fransızca özgün metne erişemedik" notu dürüst.
- Bölüm başlıkları olgu olarak doğru. Zaman damgaları yeni ASR zamanlarıyla uyumlu (3:01 veba, 3:34 Ciompi, 6:51 çifte kayıt, 7:09 Cossa, 8:04 catasto); v2 videoyla yeniden bakılmalı.
- Etiketlerden P1'de olmayan adlar çıkmış.
- Kapak metinleri doğru: "SON MEDİCİ / MİRASI KİLİTLEDİ" yaygın kısaltma ve III. madde ile uyumlu; "FAİZ YASAKTI" doğru.
- SRT, yamalı 12 cümleyle birebir uyumlu ve olgu hatası taşımıyor. Alan dışı not: 2:46–2:49 replikleri "III." / "Edward'ın" diye bölünüyor, nokta cümle sonu gibi okunabilir; altyazı üyesine.

## 5. En emin olmadığım nokta
- **Duyamadığım iki ses yeri.** c1s16'da "Mayıs'ında" (ASR "naysinde") ve c2s8'de "Faiz değil" (ASR "FISD"). İkisinde de metin doğru; sorun sesin bunu iletip iletmediği, bunu yalnız kulak doğrular.
- **Strozzi'nin kesin rakamı.** 162.925 (Crabb 2000, Wikipedia) ile 162.906 (Online Catasto) arasında hangisinin "brüt" olduğunu birincil kayıtla ayırt edemedim. Bu yüzden ekranda yuvarlama ya da tek kaynak öneriyorum.
- **c2s20.** Camerani Marri belgelerini (no. 48–49) okumadım. Anlatımın "De Roover'ın andığı belgelere göre" çerçevesi tam olarak bu sınırı söylüyor.

Kullanıcının "çizim tarzı ucuz mu, YZ gibi mi?" sorusunu ve ekran/görsel maddelerimi v2 render çıkınca karelerle yanıtlayacağım (2. aşama).
