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

---

## 2. aşama — ekran metinleri ve görsel olgular (v2, 598,5 sn)

### 2.1 Karar (SON PUAN)
**v2 için: RED, 8,5/10 (VETO: E1).** Alt puanlar: anlatım 9,5 · kaynak kapısı 9,5 · paket metni 9,5 · ekran 7,5.
- **Tek engelleyici E1:** "aforoz tehdidi" çekiminde Papa V. Martinus hançer kaldırıyor. Kaynak (de Roover, dipnot 45) yalnız aforoz tehdidinden söz ediyor; görüntü belgesiz bir şiddet olgusu ekliyor.
- **v3'te E1 ile birlikte Ö1–Ö4 de düzelirse: ONAY, 9,5.** Hepsi ücretsiz, aynı yeniden render partisine girer (≈8 çekim).
- **Yalnız E1 düzelir, Ö1–Ö4 kalırsa: 8,8 (eşiğin altı).** Dördü de küçük ama gerçek tarih ya da olgu hatası.
- v3 sonrası gerileme kontrolünü tek üye olarak ben yaparım (kare listesi §2.8).

**Sınırlarım:** Videoyu oynatamadım, sesi dinleyemedim. v2'den ffmpeg ile ≈90 tam çözünürlüklü kare çıkardım (2–595 sn; sayaç ve geçiş anları dahil) ve `out_p1/kurul/genel_01–04` kontak sayfalarına baktım.

Kaynakları curl ile açtım (hepsi HTTP 200):
- it.wikipedia: "Loggia della Signoria", "Stemma dei Medici", "Catasto fiorentino", "Istorie fiorentine", "Paradiso (Divina Commedia)", "Fiorino d'oro";
- en.wikipedia: "Tomb of Antipope John XXIII";
- DBI (Treccani biyografi sözlüğü): "Medici, Giovanni di Bicci de'" ve "Villani, Giovanni";
- de Roover 1963, tam metin.

Wikipedia ikincil bir kaynaktır. Her maddede güven düzeyini yazdım: ● = metin okundu ve iddiayı taşıyor; ◐ = nitelikli; "bilgim" = kaynağı bu turda açılmadı, kendi bilgimdir.

Bu turda başka üyelerin tur 2 raporlarını da okudum (SA2, AN1, AN2).

### 2.2 Tur 1 ekran maddelerim ve 1. aşama N3–N5: durum
| Madde | Durum | v2 kanıtı |
|---|---|---|
| **G1** Duomo kubbesi yanlış yıllarda | **KAPANDI** | 1338 (141, 143 sn), 1348 (183, 187 sn) ve 1378 (236, 243, 249 sn) karelerinde kubbe yok. 1429/1433 kapanış kulesinde (587 sn) kubbe yarım, fenersiz ve tepesinde vinç var; 1420–36 inşaatıyla uyumlu. |
| **G2** 1465 sonrası arma erken bağlamlarda | **KAPANDI** (ama yeni bir gerileme var: Ö3) | 1378'de (282 sn) ve Bölüm II kartında (340 sn) 8 kırmızı top var, mavi top yok. Peruzzi ağı ile çifte kayıt çekimlerinden arma kalkmış. Mavi zambaklı arma yalnız şu yerlerde: 1743 bağlamı (8–12 sn), başlık kartı (103 sn), bitiş kartı (595 sn). Son ikisini marka işareti olarak kabul ediyorum. |
| **V1** boncuklu abaküs | **KAPANDI** | 151 sn: Hint-Arap rakamları (1…0), yazılı toplama 347+125=472 ve sayma bezi. |
| **V2** 1737–43 kostüm ve oda | **KISMEN (kabul)** | 1737 koridorunda (60–64 sn) figürler artık silüet. 1743 yatak odası (5–12 sn) Quattrocento kitiyle kalıyor; tur 1'de "temsilî oda" kararını başkana bırakmıştım. |
| **V3** XXIII. Johannes "papa" | **KAPANDI** | 438,6 sn: "COSSA = XXIII. JOHANNES · PİSA PAPASI · BUGÜN KARŞI PAPA SAYILIR". |
| **V7** 152.820 | **KAPANDI** | 516,5 sn: "150.000+ FLORİN KÂR"; defter satırında "1397–1420 KÂR 150.000+". |
| **V8** "VENEDİK 1407" | **KAPANDI** | 418 ve 422 sn: eksende yalnız "1340 CENOVA" var; "MEDİCİ İCADI" çarpılı. |
| **V9** uydurma portre madalyaları | **KAPANDI** | Lorenzo (530 sn) ve Cosimo (582 sn) madalyalarında "TEMSİLÎ" damgası var. Cosimo yazıtı "COSMVS · MEDICES"; PATER PATRIAE yok, doğru (unvan ≥1464). |
| **S1** HUD 1378'de takılı | **KISMEN → Ö4a** | 300 sn'ye 1390 adımı eklendi. 285–297 sn hâlâ 1378; "VIERI DI CAMBIO · GIOVANNI'NİN PATRONU" levhası bu yılın altında (296 sn). |
| **S2** Bardi/Peruzzi düğüm sayısı | **KAPANDI** | 163,5 sn: iki ağda ≈15'er düğüm ve "ŞUBE SAYILARI TEMSİLÎ". |
| **S3** çeyiz sırası | **AÇIK, kötüleşti → Ö4a** | Bkz. §2.4. |
| **S4** Ciompi sahnesinde palle bayrakları | **KAPANDI** | 217–221 ve 236 sn: beyaz zeminde kırmızı haçlı Popolo/Adalet sancağı, kırmızı zambaklı komün bayrağı; palle yok. Machiavelli III ile uyumlu: Michele di Lando'nun elinde "la insegna del gonfaloniere di giustizia" ● (sancağın kırmızı haçlı olması: bilgim ◐). |
| **S6** 21 lonca kalkanı | **KAPANDI** | 231–240 sn: 3×7 = 21 kalkan ve "ARMALAR TEMSİLÎ". |
| **K1/K2/K3**'ün ekran yanları (Parks, ÇEKİLDİ, veba) | **KAPANDI** | 382 sn "TİM PARKS · AKTARDIĞINA GÖRE"; 249 sn "MICHELE DI LANDO · YÜN TARAYICISI → GONFALONIERE" ("ÇEKİLDİ" yok); 183 sn "MART 1348 · YAZ BOYUNCA". |
| **N3** Strozzi rakamı | **KAPANDI** | 501–502 sn: "PALLA STROZZI · 1427'NİN EN ZENGİNİ · 163.000 FLORİN · YAKLAŞIK". Online Catasto (162.906) ve Wikipedia (162.925) rakamlarının doğru yuvarlaması. "İkinci en zengin" ifadesi ne karelerde ne kodda var. |
| **N4** Villani levhası | **KISMEN → Ö2** | 175 sn: "1300'DE PERUZZİ ORTAĞI · ŞİRKETİ 1341'DE BATTI". |
| **N5** Cavalcanti levhası | **KAPANDI** | 556–562 sn: "HAPİSTE · 1430'LAR · OLAYA DAHA YAKIN" ve "1430'LAR · HAPİSTE". Yeni c2s30 anlatımıyla aynı (DBI ●). |

Yamalı cümlelerin ekran karşılıkları da doğru:
- **c2s10:** 402 sn "SERMAYE · 1426'DA ÇEKİLDİ · DE ROOVER'A GÖRE". de Roover: "the capital had already been withdrawn in 1426" ●.
- **c2s20:** 466,5 sn "DE ROOVER · ANDIĞI ARŞİV BELGELERİ", "BELGE · DE ROOVER" ve "AFOROZ TEHDİDİ"; "TRECCANI" ve "ANEKDOT" kalkmış ●.
- **c2s21:** 484 sn "22 YIL KESİNTİSİZ + 18 YIL ARALIKLI · 1422" (DBI ●).
- **c1s16:** 221 sn "MAYIS 1378 · KURAYLA · SALVESTRO DE' MEDICI · MEDİCİ AİLESİNİN BAŞKA BİR KOLU"; ekranda torbadan kura çekiliyor (Machiavelli "Fu tratto…" ●).

### 2.3 Başkanın ilettiği bulgular: doğrulamam
| Bulgu | Sonuç | Kanıt ve güven | Önem ve düzeltme |
|---|---|---|---|
| **AN2-E1** papa hançerle | **DOĞRULANDI → E1, ENGELLEYİCİ (veto)** | 471,9 sn: hançer sağ elde, bel hizasında (x≈1280–1330, y≈350–520). 472,7 sn: hançer başın üstünde (x≈1235–1275, y≈150–300). Kodda `scenes_c2.py:186` `kind="papa", action="threat"`. Kaynak yalnız aforoz tehdidi diyor: de Roover n. 45 "Pope Martin V had to threaten Giovanni di Bicci with excommunication" ●. Görüntü belgesiz bir fiziksel tehdit ekliyor: gerçek bir papa bankacıya bıçak kaldırıyor. Hassasiyet yönüyle KA2'nin de alanı. | **ENGELLEYİCİ** · ücretsiz: `action="point"` ya da `"talk"`; elde bulla (`c2_bulla` simgesi motorda var) ya da boş kalkık el. "AFOROZ TEHDİDİ" damgası kalır. 1 çekim. |
| **SA2-Y2** Loggia dei Lanzi | **DOĞRULANDI → Ö1** | 139,5–142,6 sn, sağ kenar (x≈1700–1920, y≈435–930): üç geniş kemer, çeyrek yonca frizli teras ve korkuluk. Bu `cilt_sehir.loggia()` ("Loggia dei Lanzi"). 236–239,8 sn'de (22 Temmuz 1378) bitmiş hâliyle duruyor (x≈1770–1920, y≈505–945). it.wikipedia: "L'edificazione risale al periodo tra il 1376 e il 1382" ● (ikincil, yaygın). 1338'de yoktu, Temmuz 1378'de inşaattaydı. | **önemli** · `donem.loggia_stage(y)`: 1376'dan önce yok (sıradan cephe), 1376–82 arası ayaklar ve iskele, 1382'den sonra tam yapı. 2 çekim. |
| **SA2-Y4** 1520 mührü 8 toplu | **DOĞRULANDI → Ö3** | 577,5 sn: balmumu mühürde kenar boyunca 8 top (x≈1250–1470, y≈330–560). Siparişin tarihi 1520: it.wikipedia "Istorie fiorentine": "Alla fine dell'anno il cardinale Giulio de' Medici… gli fece offrire l'incarico di stendere un'opera sulla storia di Firenze (1520)" ●; DBI (teyit_P1): "L'8 novembre [1520] fu «condotto» dallo Studio" ●. Arma: it.wikipedia "Stemma dei Medici": XI. Louis'in Mayıs 1465 tarihli Montluçon kararnamesi tepedeki topa Fransa zambaklarını verir; 16. yüzyılda (X. Leo, VII. Clemens) toplar kenar boyunca ("in cinta") dizilir ●. | **önemli** · 1520 mührü 6 toplu olmalı, en üstteki top üç zambak kabartmalı (balmumu tek renk, zambak kabartmayla seçilir). Nesneye kendi yılı verilmeli (`year=1520`). 1 çekim. |
| **SA2-Y5** Villani levhası | **DOĞRULANDI → Ö2** | Peruzzi 1343'te battı: de Roover "when the Peruzzi company failed in 1343" ●. 1341'de batan, Villani'nin yönettiği Buonaccorsi: DBI "Dal 1322 … tra i soci della compagnia Buonaccorsi di cui, dopo la riorganizzazione del 1324, prese la direzione …" ve "precipitò nel 1341 quando la compagnia fallì" ●. Peruzzi ortaklığı: "socio dal maggio 1300" ●. Levha, Peruzzi 1341'de batmış izlenimi veriyor; anlatım hemen önce "1340'larda battı" dediği için bu okuma kolaylaşıyor. | **önemli** · **tam metin:** "GIOVANNI VILLANI" / rol: "1300'DE PERUZZİ ORTAĞI · YÖNETTİĞİ BUONACCORSİ 1341'DE BATTI". Sığmazsa iki satır: "1300'DE PERUZZİ ORTAĞI" + "YÖNETTİĞİ BUONACCORSİ ŞİRKETİ 1341'DE BATTI". 1 çekim. |
| **SA2-Y3** HUD 1252'de Dante ve Villani; "BUGÜN" + HUD 1737 | **DOĞRULANDI → Ö4b; "BUGÜN" küçük** | 124 sn: "DANTE" ve HUD 1252. 133 sn: "GIOVANNI VILLANI · KRONİKÇİ · ESKİ DARPHANE YÖNETİCİSİ" ve HUD 1252. 82 sn: "BUGÜN" ve HUD 1737. Dante 1265'te doğdu (bilgim; yaygın olgu). Paradiso ≈1321'de tamamlandı: it.wikipedia "1ª ed. originale 1321 ca." ●; yazımın ≈1316'da başlaması bilgim ◐. Villani ≈1280 doğumlu (bilgim ◐). DBI: "ufficiale della Moneta nel 1317"; "sovrintendente alla moneta d'oro e d'argento … nel 1327-28" ●. | **önemli** (Dante, Villani), **küçük** ("BUGÜN"). **Önerim SA2'ninkinden biraz farklı:** c1s3 Dante çekiminde HUD gizlensin ya da "≈1320" yazsın; **c1s4–c1s5 → 1338.** Gerekçe: darphane çekimi Villani'nin 1338 rakamına dayanıyor ("yılda 350–400 bin florin", VIL XII.94 ●), levhadaki "ESKİ DARPHANE YÖNETİCİSİ" de 1338'e göre doğru. 1317 seçilirse "eski" sözcüğüyle çelişir. "BUGÜN" çekiminde HUD gizlensin ya da "BUGÜN" yazsın. |
| **SA2-Y6** catasto kapı kapı | **DOĞRULANDI → K1** | it.wikipedia "Catasto fiorentino": 22 Mayıs 1427 yasası "ogni cittadino dovesse dichiarare sotto il suo Gonfalone il proprio nome … i beni"; beyannameler (portate) "ufficiali del Catasto"ya teslim edilir ●. Ekranda memurlar kapı kapı dolaşıyor; bu yöntemi yanlış gösteriyor. Anlatım ("yazdırdı") doğru. | **küçük** · sahne: beyanname getiren hane reisleri ve masa başında ufficiali. |
| **SA2-Y8** mezar yazıtı Türkçe | **DOĞRULANDI → K2** | en.wikipedia "Tomb of Antipope John XXIII": yazıt "IOANnES QVOnDAM PAPA [XXIII]". Martinus'un itirazı, "quondam"ın hem "eski" hem "merhum" anlamına gelmesinden ● (dipnotlu ikincil; c2s19'u da destekler). Taştaki Türkçe "ESKİ PAPA" bir çeviri, olgu hatası değil. | **küçük** · taşa "IOANNES QVONDAM PAPA XXIII", altına Türkçe "eski papa" etiketi. |

**Çapraz not (SA2 §5, kapak K2 arması):** SA2, kapaktaki 6 kırmızı toplu kalkan için "kaynağı yok" diyor. it.wikipedia "Stemma dei Medici" (dipnot 4) şunu yazıyor: "In origine, l'arma della famiglia de' Medici mostrava sei palle rosse in campo oro (anche se, almeno fino a tutto il XV secolo, vennero realizzate varianti dello scudo che presentavano fino a undici palle…)" ◐ (dipnotlu ikincil). Yani 6 kırmızı top belgeli bir erken biçim; 8 top da belgeli bir varyant. Olgu açısından kapakta değişiklik gerekmiyor; videoyla tutarlılık sanat kararıdır.

### 2.4 Kendi yeni bulgularım (v2 ekran)
| # | Yer | Bulgu | Ne yapılmalı | Önem |
|---|---|---|---|---|
| **Ö4a** | 302,4–313,1 sn (c1s27). 304 sn: "PICCARDA BUERI'NİN ÇEYİZİ · 1.500 FLORİN"; 306–310 sn: "EVLİLİK SÖZLEŞMESİ · İLK SERMAYE". HUD (sağ üst) **1390**. | Evlilik ve çeyiz 1385 tarihli. DBI: "Piccarda Bueri (sposata nel 1385)" ve "già da un anno era direttore della filiale … e ne divenne socio investendo i 1.500 fiorini". de Roover: "brought him in October 1385" ●. Ekran evlilik sözleşmesini 1390'a tarihliyor ve anlatımdaki gevşek sırayı (tur 1 S3) sabitliyor. Ayrıca 285–297 sn'de "VIERI DI CAMBIO · GIOVANNI'NİN PATRONU" levhası HUD 1378 altında duruyor (tur 1 S1). | **İkisini tek düzeltme kapatır:** c1s26'daki "Roma'da" sözcüğünde (291,9 sn) HUD → **1385**; c1s27 bitene kadar 1385 kalsın. 300 sn'deki "1390'LARIN BAŞI" levhası olduğu gibi kalır; c1s28'de 1397. HUD hep ileri gider, geri sıçrama olmaz. 3 çekim. | **önemli** |
| **K3** | 445–452 sn (c2s17, kefalet/fidye), HUD 1415 | DBI: kurtuluş 1418, fidye 1419 ("organizzare la liberazione (1418) e a pagare il riscatto (1419)") ● | HUD c2s17'de 1418 olsun ya da levhaya "1418–19" eklensin | küçük |
| **K4** | 143 sn: "≈90.000 KİŞİ" kartı, "VILLANI'YE GÖRE · TAHMİN" damgasının ilk yarısını örtüyor (x≈990–1400, y≈225–315) | Kaynak niteliğini taşıyan damga tam okunmalı | damgayı kartın üstüne ya da yanına al | küçük |
| **K5** | 129–137 sn, darphane | Sikke boynuzlu bir demirci örsünde dövülüyor. Ortaçağda alt kalıp (pila) kütüğe gömülür, üst kalıp (torsello) çekiçle vurulurdu (bilgim ◐). | isteğe bağlı: kütükte kalıp ve zımba | küçük, isteğe bağlı |

### 2.5 Ekranda sınadığım ve doğru bulduğum olgular (özet)
**c0 (0–103 sn):**
- "18 ŞUBAT 1743";
- takvim "9 TEMMUZ 1737 → 31 EKİM 1737" ve 114 gün;
- belgede I–XIII madde numaraları, "FRANSIZCA" ve "ITALIANO" (Casciu 2006 ●);
- "3. MADDE · ÖZET" kartı, tırnaksız;
- "SINIR YAKLAŞIKTIR";
- "DEVLETİN SÜSÜ · HALKIN YARARI · YABANCILARIN MERAKI" ve "ÇEVİRİ";
- galerideki beş kalem;
- Uffizi'deki "BUGÜN" (HUD sorunu dışında).

**c1:**
- "3,5 GRAM · 2 CM" (it.wikipedia "Fiorino d'oro": 3,5 g, 20 mm ●);
- florinin "FLORENTIA" zambak yüzü ve "S · IOHANNES · B" yüzü;
- "≈90.000 KİŞİ · VILLANI'YE GÖRE · TAHMİN";
- 1338: Palazzo dei Priori ve kırmızı zambaklı beyaz komün bayrakları (1251 sonrası Guelf bayrağı; bilgim ◐);
- 1348 nehir panoramasında üç kemerli Ponte Vecchio (1345 yeniden yapımı; bilgim ◐);
- "12 YAŞINDA" ve "KATMAN KATMAN";
- "CIOMPI'NİN TALEPLERİ … YAZILDIĞINA GÖRE" (Monte faizi: Machiavelli III ●);
- "KURGU · KONUŞMA TARİHÇİNİN";
- "AĞUSTOS SONU";
- "ORSANMICHELE · VIA PORTA ROSSA";
- sermaye sayacı "10.000 FLORİN".

**c2:**
- "KLASİK BİR ÖRNEK";
- "BORÇ ✗ FAİZ ✗";
- "VİCDAN KOMİTESİ" (mizah);
- "MÜŞTERİ: KİLİSE";
- "25 MART 1402 · YILBAŞI";
- "COSSA = XXIII. JOHANNES" (HUD 1402'den 1410'a geçiyor: kardinallik 1402, papalık seçimi 1410 ●);
- "KONSTANZ KONSİLİ · 1415";
- "VAFTİZHANE · COSSA'NIN MEZARI" (HUD 1419; ölüm Aralık 1419);
- "V. MARTINUS · İTİRAZ";
- "%29,8 · 137 HANE · BİR HESABA GÖRE" (Online Catasto ●);
- "GIOVANNI · CATASTO'YU DESTEKLEDİ";
- "1420 · YÖNETİM OĞULLARINA";
- "20 ŞUBAT 1429 → 1428 · YILBAŞI 25 MART";
- "LORENZO · TORUNUNUN OĞLU · İLERİDE MUHTEŞEM · 180.000 FLORİN · LORENZO'NUN KAYDINA GÖRE · TEMSİLÎ";
- "MACHIAVELLİ · BİR ASRA YAKIN SONRA";
- "MACHIAVELLİ'NİN ÇİZDİĞİ · KİMSE İSTEMEDEN DE";
- "COSIMO · GIOVANNI'NİN OĞLU · 39 YAŞINDAYDI · 1389 DOĞUMLU · TEMSİLÎ";
- kapanış kulesi.

**Diğer:**
- Sayaçların ara değerleri (501,6 sn "162.993", 498 sn "68.798+", 306 sn "1.478") yalnız birkaç karelik geçişler; olgu iddiası değil.
- Paket (PK1-Y1 sonrası): açıklamanın 2. satırı doğru; kaynak listesi N1, N2 ve N8 ile uyumlu.
- SRT yeni c2s10 ve c2s30 cümleleriyle birebir: "De Roover'a göre Roma şubesi zamanla / sermayesiz çalışır hale geldi;" ve "Cavalcanti ise 1430'larda, hapisteyken,".
- Bölüm zaman damgaları v2 zamanlarıyla uyumlu: 6:52 = c2s12 (412,9 sn); 7:11 = c2s15 (431,7 sn); 8:06 = c2s22 (486,6 sn).

### 2.6 Kullanıcının sorusu, kendi alanımdan: "Çizim tarzı ucuz mu, yapay zekâyla üretilmiş gibi mi?"
**YZ izlenimi:** Olgu ve dönem gözüyle yok. Yapay zekâ görsellerinin tipik izleri hiçbir karede yok: bozuk harf, anlamsız arma, tutarsız el ya da yazı görmedim. Latin yazıtlar, tarihler, rakamlar ve kaynak damgaları ("BİR HESABA GÖRE", "TEMSİLÎ", "KURGU", "BELGE · DE ROOVER") doğru ve birbiriyle tutarlı; bu, elle kurulmuş bir titizlik olarak okunuyor.

**Ucuz ve şablon okunan şey dönemsizlik.** Aynı oda kiti (ağaçlı duvar halısı, kafes pencere, kırmızı perdeli taht) beş farklı yer ve tarihte tekrar ediyor: 1378 Signoria salonu (221 sn), 1397 bankası (347 sn), 1415 Konstanz (442 sn), 1419 papalık salonu (462 sn) ve 1743 yatak odası (9 sn). 14. yüzyıl ile 18. yüzyıl aynı mobilyayla duruyor. Bu, bilgili izleyicide "hazır set" izlenimi yaratıyor.

Aynı kit bu turdaki dönem hatalarının da kaynağı: 1338'deki Loggia, 1520 mührünün 1429 arması ve papanın elindeki hançer kitten geliyor.

**Çare:** Dönem katmanını yapılardan kostüme, odaya ve figür eylemlerine genişletmek:
- 14. yüzyıl gotik, 15. yüzyıl erken Rönesans ve 18. yüzyıl barok için ayrı oda ön ayarları;
- "şiddet" eylemlerini yalnız gerçek şiddet sahnelerine kilitleyen bir kapı.

### 2.7 En emin olmadığım nokta (2. aşama)
- **E1:** Hareket hâlinde göremedim. Ama iki karede bıçak, balçak ve topuz açıkça seçiliyor; kod da eylemi doğruluyor.
- **Ö1:** Loggia'nın Temmuz 1378'deki inşaat düzeyini bilmiyorum (yapı 1376'da başladı). "Ayaklar ve iskele" önerisi genel bir öneri.
- **Ö4:** HUD'daki yılı bir tarih iddiası sayıyorum. Ekip onu yalnız bir "bölüm imleci" sayıyorsa Ö4'ün ağırlığı düşer; ama izleyici sağ üstteki yılı tarih olarak okur.
- **Kapak arması:** Dayanağım it.wikipedia; dipnotlu ama ikincil. İlk kaynağı (Ceramelli Papiani) görmedim.

### 2.8 v3 için tek üye gerileme kontrolü: bakacağım kareler
- **E1:** 471,4–474,0 sn, 0,1 sn adımla.
- **Ö1:** 139,5, 141,8, 142,6, 236,0 ve 238,5 sn.
- **Ö2:** 175 sn.
- **Ö3:** 577,5 sn.
- **Ö4:** 124, 133 ve 82 sn; 291,9–313 sn arası.
- **K maddeleri uygulanırsa:** 143, 450, 459,5 ve 489,5 sn.

**Kabul ölçütü:**
- Papanın elinde silah yok.
- 1338 karesinde Loggia yok; 1378 karesinde inşaat hâlinde.
- Villani levhası yukarıdaki tam metinle.
- 1520 mührü 6 toplu, tepedeki top zambaklı.
- c1s26–c1s27 boyunca HUD 1385.
- Dante çekiminde HUD gizli ya da "≈1320"; Villani çekiminde 1338.
