# M2c — SİYASET DEVAM-2: Pazzi (c7) ve Aslanın İni (c8) · Kaynaklı olgu dosyası

> Hazırlayan: brif ajanı · 18 Ekim 2026 · Kapsam: **c7 "26 Nisan 1478"** ve **c8 "Aslanın İni" (1478–1481)**; M2'nin HAFIZA satırlarını güncelleyen/düzelten ek tur. **Senaryo değildir.**
> **DURUM: KISMEN DOĞRULANMIŞ, ● YOK.** Bu ortamda WebFetch çalışmıyor (DNS); hiçbir sayfa açılıp okunamadı. Tüm satırlar **WebSearch özetlerine** dayanır (özet modeli sayfayı derler; kesme/yanlış okuma payı vardır). Özetin tırnak içinde verdiği kısa parçalar "özet tırnağı" diye anılır; çeviri bize aittir.
> Kimlikler: `Yn` = yeni/güncellenen kronoloji satırı · `Tn` = kaynaklar-arası varyant tablosu · `Dn` = düzeltme/nüans (**M5'in D46'sının devamı: D47…**) · `Xn` = eksik/doğrulama kuyruğu · `Qn` = sorgu günlüğü · `Sn` = kaynak anahtarı (URL'ler §8'de). `M2:Kn`, `M2:C7.n`, `M2:§4.n`, `M5:Dn`, `M1b:bn`, `M3:Kn` önceki dosyalara atıftır.

---

## 0. Başlık notu — araç, bütçe, sınırlar

| Araç | Sonuç |
|---|---|
| **WebFetch** | Kullanılmadı (görev notu: DNS çalışmıyor; M2/M5 aynı hatayı bildirmişti). **Hiçbir olgu ● (birincil metin okundu) değildir.** |
| **WebSearch** | **45/45 sorgu kullanıldı** (44 `standard`, 1 `extended`; extended çıktıyı iyileştirmedi). Alan adı filtresi: yalnız `treccani.it` **13**; yalnız `wikisource.org` **2**; karışık liste **20** (içinde treccani ≥1: Q02, Q19, Q24, Q30, Q31, Q37, Q38, Q41, Q42; wikisource ≥1: Q01, Q03, Q04, Q07, Q19, Q23, Q24, Q25, Q41); filtresiz **10**. Bütçe tükendi; §9'daki boşluklar **yeni tur** ister. Arama aracı sayfa metnini değil **özet** döndürür: her satırın sınıfı buna göre verildi. |
| **Bash** | Yalnız yerel hesap (`python3 -I`): Jülyen hafta günü ve Paskalya (Meeus Jülyen algoritması), gün farkları. Web'e çıkılmadı. |

**Sınıf anahtarı (M2 ile aynı):** ◐ ≥2 bağımsız ikincil (arama özeti dahil; **Treccani'nin farklı eserleri aynı yayıncıdan sayıldı ve not edildi**) · ○ tek/çelişkili · ANEKDOT (kim anlattı yazılır) · YORUM · HAFIZA (araçla doğrulanmamış, metne GİRMEZ ya da "yayın öncesi teyit").
**Hesaplar bize aittir:** hafta günleri, gün farkları, yaşlar (Jülyen, Zeller/Meeus). Floransa yılı 25 Mart'ta başlar; **26 Nisan 1478 için iki üslup aynıdır** (25 Mart'tan sonra), ancak 22 Mart 1478 Paskalyası Floransa belgesinde "1477" görünür.

**Bu turda ne değişti (özet):**
1. **Kaynak ağı genişledi:** Treccani DBI'den Bandini, Carducci, Frescobaldi, Salviati, Montesecco, Jacopo ve Francesco de' Pazzi, Guglielmo/Cosimo de' Pazzi, Riario Sansoni, Lorenzo, Sisto IV, Ferdinando I, A. ve D. Carafa, Tomacelli; Wikisource'ta Machiavelli *Istorie* VIII ve Guicciardini *Storie fiorentine* IV/XIII (başlık-özet düzeyi); Gutenberg'te Reumont, Gardner, Staley (19.–20. yy. ikincil).
2. **Sinyal:** komünyon varyantı ≥3 yerde (DBI Jacopo + Guicciardini + Machiavelli çevirisi) ◐; "kaldırma" popüler anlatıda. Poliziano'nun cümlesi **hâlâ görülmedi** (T1).
3. **"Palle, palle" Guicciardini'den** (*Storie fiorentine* IV), Machiavelli'den değil (T5, D52).
4. **Bandini zinciri DBI ile kuruldu** (8 Mayıs 1479 mektup → 11/14 Temmuz Antonio de' Medici → 24 Aralık varış → 29 Aralık asılma); Lorenzo o sırada Napoli'deydi (T9, D62–D65).
5. **Napoli tarihleri DBI/EI ile netleşti** (6 Aralık ayrılış; 18 Aralık varış; 27 Şubat çıkış; dönüş 13/15 Mart); **"silahsız" için belge bulunamadı** (D61).
6. **Poggio Imperiale:** M2 yönü doğru (Napoli–Papalık galip), ama tarih tek kaynak (D59).
7. **Perde etiketi çatışması bulundu:** `compose.py` `PERDE_OF` = "II GÜZELLİK (c4–c10)", `YONETMENLIK_REHBERI.md` §5/§9 = "II BEDEL (c7–c11)" (D77).

### Q — sorgu günlüğü (45)

| Q | Konu | Alan adı filtresi | Sonuç (tek satır) |
|---|---|---|---|
| Q01 | sinyal varyantları, Poliziano/Machiavelli | dokumen, cambridge, gutenberg, wikisource, archive | "kaldırma" popüler; Poliziano metni yok; Perosa 1958 edisyonu anıldı |
| Q02 | Montesecco itirafı, Papa/Federico | dokumen, cambridge, treccani, jstor, academia | itiraf 4 Mayıs 1478; kilisede reddi; Excusatio; Papa sözü doğrulanmadı |
| Q03 | Lorenzo sakristi, tunç kapı, Nori, Ridolfi | dokumen, cambridge, gutenberg, wikisource, britannica | kuzey sakristi, Michelozzo/Luca della Robbia kapıları, Poliziano + Cavalcanti; Ridolfi tek eski kaynak |
| Q04 | Landucci 26 Nisan, palle | archive, gutenberg, dokumen, wikisource | Landucci metni çıkmadı; Strozzi görgü tanığı anıldı |
| Q05 | Salviati, Petrucci, Perugialılar, ısırma | gutenberg, dokumen, archive, britannica, cambridge | Salviati ~30 adamla; ısırma Poliziano'ya atfedilir (Savonarola biyografisi aracılığıyla) |
| Q06 | Giuliano kafatası/ekshümasyon 2007 | yok | 19 yara; ekshümasyon çalışması kendisi bulunamadı |
| Q07 | Machiavelli VIII metni (extended) | gutenberg, wikisource, archive, dokumen | metin açılmadı; "kaldırma" yeniden duyuldu |
| Q08 | ayin saati | yok | tek saat: History Today "11 çanı" (○) |
| Q09 | Papa "ölüm istemem" sözü | dokumen, cambridge, jstor, academia, archive | söz doğrulanamadı; Montesecco "Tanrı görür" reddi; "onurlu kafa kesme" sözü ○ |
| Q10 | DBI Bandini | treccani | 8 Mayıs 1479 → 24 Aralık → 29 Aralık zinciri |
| Q11 | Leonardo çizimi yazıtı | yok | Louvre: 29 Aralık 1479 Bargello; Richter 664 adı; 28 Aralık tek makale |
| Q12 | Lorenzo Napoli tarihleri | treccani | 6 Aralık / 18 Aralık / 27 Şubat / 13–15 Mart |
| Q13 | DBI Jacopo Pazzi (son) | treccani | cesedi sonraki pazar sürüklenir, Arno (ponte Rubaconte) |
| Q14 | DBI Salviati | treccani | Petrucci, Poliziano/Machiavelli, "cannibalism" (özet İngilizcesi), aynı gün ~30 idam |
| Q15 | DBI Montesecco | treccani | itiraf 4 Mayıs; reddi planın çökme nedenlerinden; yerine Maffei + Stefano |
| Q16 | Jacopo'nun sonu (ikinci deneme) | treccani | "ertesi gün" yakalanma (16. yy. vakayiname), tarih tutmuyor |
| Q17 | Sisto IV, Papa'nın sözü | treccani | EI: bilgisi var, öldürme belirsiz; DBI: onayıyla, modalite belirsiz |
| Q18 | DBI Lorenzo, Pazzi | treccani | "iki adam", Sagrestia Nuova, ~30 idam, Guglielmo sürgün |
| Q19 | "palle palle" | treccani, wikisource, archive | **Guicciardini IV**; Machiavelli'de Jacopo'ya "kimse cevap vermedi" |
| Q20 | Verrocchio mum heykeller | yok | Vasari (Isaacson): 3 boy mum; günümüze ulaşmadı |
| Q21 | Bertoldo Pazzi madalyası | yok | NGA: Lorenzo SALVS PVBLICA / Giuliano LVCTVS PVBLICVS, 6,6 cm |
| Q22 | Machiavelli VIII sinyal (it.wikisource) | wikisource | Giuliano evden alınır; sinyal cümlesi özette yok |
| Q23 | Landucci Pasqua | wikisource, archive, gutenberg | "Pasqua" görülmedi; Strozzi Pazar sabahı |
| Q24 | Francesco de' Pazzi sonu | treccani, wikisource | bacak yarası; Otto sorgusu; Salviati yanında asılır; ceset 23 gün sonra Arno |
| Q25 | Poliziano Latince, "Ite missa est" | wikisource, archive, dokumen, cambridge, academia | Celati 2019: 1478 yaz sonu sürüm; 1480 revize |
| Q26 | Pazzi Savaşı seyri | britannica, dokumen, cambridge, gutenberg, archive | Chianti, Colle, Poggio Imperiale, barış şartları (Reumont) |
| Q27 | DBI Riario Sansoni | treccani | 10 Aralık 1477; ayin onuruna; rehin; 12 Haziran serbest |
| Q28 | Poggio Imperiale yönü | yok | Siena freski "Sienalıların zaferi" (1480/79 başlığı) |
| Q29 | "silahsız" | yok | **kaynak yok**; yalnız dinî-kişisel bir blog; Britannica 1911 "yalnız" |
| Q30 | Savaş seyri (Collector) | thecollector, britannica, treccani, dokumen | Poggio Imperiale Napoli–Papalık galip (DBI Alfonso II) |
| Q31 | Otranto, Roma töreni | britannica, treccani, dokumen, cambridge, gutenberg | 28 Temmuz/11 Ağustos; Alfonso geri çağrılır; tören bulunamadı |
| Q32 | DBI Carducci | treccani | 8 Mayıs 1479 mektubu; Antonio de' Medici 11/14 Temmuz |
| Q33 | Bertoldo–Mehmed madalyası | dokumen, cambridge, jstor, academia | "scholars believed" teşekkür hediyesi; 1480/1481 |
| Q34 | Roma töreni (ikinci) | yok | **bulunamadı**; Becchi sinodu; ressam yolculuğu 27 Ekim 1480 |
| Q35 | Türkçe Bandini | yok | Türkçe kaynak çıkmadı; executedtoday/Italian Art Society |
| Q36 | Yetmişler Konseyi | treccani | Nisan 1480 Balìa; 5 yıl; Otto di Pratica; 1485/1490 yenileme |
| Q37 | Pazzi cezaları | britannica, treccani, dokumen | isim/arma silinir; Guglielmo sürgün; Volterra tutsakları 1480'de salıverilir |
| Q38 | aforoz/interdikt | treccani, britannica, dokumen, gutenberg | aforoz 1 Haziran 1478; interdikt 20/22 Haziran; Florentina Synodus Ağustos |
| Q39 | Lorenzo pencerede, Strozzi | gutenberg, archive, dokumen, britannica | pencerede göründü (Gardner, Reumont) |
| Q40 | DBI Ferdinando I | treccani | ayrı barış tarihleri; Otranto bağlamı; Sisto–Venedik ligi 17 Nisan 1480; absolüsyon 3 Aralık |
| Q41 | Machiavelli ilk plan (it.wikisource) | wikisource, treccani | **Pazar 26 Nisan, Fiesole ziyafeti**; Giuliano gelmeyince Duomo kararı |
| Q42 | Floransa–Osmanlı ticaret | dokumen, cambridge, jstor, academia, treccani | 1455 imtiyaz/bailo, 1469 ayrıcalık; Paolo da Colle |
| Q43 | Sistina tarihi | yok | "27 Ekim 1480" ↔ resmî 1481 |
| Q44 | DBI Ridolfi | treccani | zehir-emme anlatısı yok; madde Pazzi'yi yalnız andı |
| Q45 | Machiavelli/Guicciardini Napoli yolculuğu | wikisource | Guicciardini *Storie fiorentine* XIII "Viaggio a Napoli di Lorenzo (1479)" başlığı var |

---

## 1. c7 — 26 Nisan 1478: yeni/güncellenen kronoloji (Y01–Y42)

> **Okuma uyarısı:** Tüm anlatıların ortak zayıflığı: **Medici süzgeci.** Poliziano (görgü tanığı, 1478 yaz sonu, propaganda), Scala'nın *Excusatio*'su (Montesecco itirafını içerir), Machiavelli (≈1520–25, Medici siparişi), Guicciardini (Floransalı aristokrat, ≈1508–09), Montesecco ve Maffei'nin itirafları (Medici hapsinde yazıldı). **Pazzi tarafının kendi sesi yoktur** (Jacopo'nun meydandaki çağrısı dışında, onu da Machiavelli aktarır). Saat dilimleri kaynaklarda **yok** (T6).

| # | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|
| Y01 | Eki 1474 | Francesco Salviati Pisa başpiskoposu atanır; **Lorenzo girişini engeller, iki yıl şehre sokmaz**; Riario ve Pazzi'lerle bağı kini besler | ◐ | S23 (DBI Salviati); M2:K37 | DBI Salviati "ve iki yıl boyunca" der. Kaynak aynı yayıncı + M2 HAFIZA-O. |
| Y02 | 1474 | Sixtus IV Lorenzo ve Giuliano'yu papalık *depositario*'luğundan alır; görev Pazzi'ye (Imola krizi) | ◐ | M1b:b21, U14; EI Lorenzo | Tutar 30.000/40.000 (söylenmez). |
| Y03 | Haz 1476 | Şap tekeli Medici → Pazzi bankası | ○ | M1b:b23 (DBI G. de' Pazzi) | c9'da tek cümle; çift anlatılmaz (c9 brif tuzak #10). |
| Y04 | Mayıs–Haz 1477 | Montesecco, Girolamo Riario adına **gizlice Roma'ya** gider; plan temelleri | ◐ | S21 (DBI Montesecco) | |
| Y05 | 1477 | Girolamo Riario, Salviati ve **Franceschino (Francesco) Pazzi**, Montesecco'ya cinayeti örgütlettirmeyi kararlaştırır | ◐ | S14 (EdP Sisto IV) | "Napoli Kralı da destekledi" aynı özet; ○. |
| Y06 | 10 Ara 1477 | **Raffaele Riario 17 yaşında kardinal** (S. Giorgio al Velabro) | ◐ | S25 (DBI Riario Sansoni); M2:K41 | |
| Y07 | 14 Şub 1478 | Federico da Montefeltro'nun şifreli mektubu (Simonetta) | ◐ | M2:K42 | Alıcı çelişir; "abartılı olabilir". |
| Y08 | **Pazar 26 Nis 1478** | **Yüksek ayin**, Duomo (Santa Reparata/Santa Maria del Fiore); **genç Kardinal Riario'nun Floransa'ya gelişi onuruna** (Enc. machiavelliana + DBI) ↔ "ayini kardinal yönetti" (EI) | ◐ | S26, S25, S16 | Ayrışma T2'de. "Paskalya" **geçmiyor** (D47). |
| Y09 | 25/26 Nis | **İlk plan bir ziyafet**; Giuliano gelmez; saldırı Duomo'ya kayar. Machiavelli'ye göre ziyafet **Pazar 26 Nisan, Fiesole'de "villa loro"**; M2'de Cumartesi 25; DBI Lorenzo'da "ayinden önce sarayda, yanlış anlaşılma" | ◐ çekirdek, ○ ayrıntı | S34 (özet), M2:K43, S05 | **Gün/yer söylenmez** (D55). "villa loro" kimin villası belirsiz (Medici mi, Pazzi mi). |
| Y10 | 26 Nis, sabah öncesi | **Montesecco kilisede kan dökmeyi reddeder**; yerine **Antonio Maffei (apostolik vikar, Volterralı) ve Stefano da Bagnone**. DBI: aceleyle seçilen uygunsuz vekiller planın kısmi başarısızlığının nedenlerinden | ◐ | S21, S34 | Machiavelli: Stefano, Jacopo'nun kızına Latince öğreten papaz (özet). |
| Y11 | aynı sabah | **Ayin başlamış, Giuliano henüz kilisede değil**; Francesco ve Bandini evine gidip "dil dökerek/tuzakla" getirir | ◐ | S34 (özet) | Machiavelli: kilise "halkla dolu". |
| Y12 | aynı | Yolda şakalaşma; Francesco sarılır gibi yapıp **zırh olup olmadığını yoklar** | ◐ | M2:K45, C7.2 | Machiavelli'nin kendi yorum cümlesi ("bunca nefret, bu kadar sakin yürek") HAFIZA-O: metin aranacak. |
| Y13 | aynı, ayin | **Sinyal** (T1): komünyon (DBI Jacopo, Guicciardini, Machiavelli çevirisi) ↔ kaldırma (popüler) | ◐ ↔ ◐ | S19, S35, M2:K46, S44, S45 | Poliziano **görülmedi**. |
| Y14 | aynı | **Bandini kısa bir silahı Giuliano'nun göğsüne sapladı; Giuliano birkaç adım gidip düştü; Francesco üstüne atılıp defalarca vurdu** | ◐ | S34 (özet); M2:C7.3 | Guicciardini varyantı: **Franceschino, Giuliano ile kol kola yürürken** saldırır (özet) → T4. |
| Y15 | aynı | **Giuliano'ya ≈19 yara** diye sayılır | ◐ | S46 (Wikipedia), S37/S38 (Gardner/Staley), Magenta/Collector (M2:K47) | 18 bir kaynakta. DBI: "şiddetle". |
| Y16 | aynı | **Lorenzo'ya iki papaz saldırır** (DBI Lorenzo: "Jacopo'nun iki adamı"); **boynundan hafif yaralı, kendini savundu, "Sagrestia Nuova"ya (= kuzey sakristi) kaçtı** | ◐ | S05, S16, S37 | Kılıç çekme/pelerin ○ (T3). |
| Y17 | aynı | **Tunç kapılar** (Michelozzo/Luca della Robbia) **kapatıldı**; kapatanlar: **Poliziano ve Cavalcanti'ler** (Gardner); "Poliziano dahil yakınları" (M2:K48) | ◐ kapı, ○ adlar | S37, S47 (Britannica: Poliziano hayatını kurtardı), M2:K48 | Adlar kaynaklarda değişir. |
| Y18 | aynı | **Francesco Nori**, Lorenzo'yu korurken Bandini'nin hançerinden ölür | ◐ | S37, S38, M2:C7.6 | |
| Y19 | aynı | Giuliano'nun bedeni **katedral papazları toplayana dek yerde kaldı** | ◐ | S05 (DBI Lorenzo özeti) | |
| Y20 | aynı | **Kardinal Riario tutuklanır** (linçten kurtulur), **rehin tutulur; 12 Haziran 1478'de serbest**, Siena üzerinden Roma'ya | ◐ | S25, S26 | Tutulduğu yer belli değil (Palazzo Vecchio **doğrulanmadı**). |
| Y21 | aynı sabah | **Salviati, bir grup adamla** Signoria Sarayı'nı almaya ve gonfaloniere'yi öldürmeye gelir; **Cesare Petrucci** bahaneyi sezip saldırır/alarm verir; **Salviati'nin adamları sarayda bir odada tutulur** | ◐ | S23, S39 (Reumont), S37 (≈30 kişi) | Machiavelli: Petrucci'nin eline "şiş" geçti (DBI özeti) → kullanma. |
| Y22 | aynı | **Jacopo ≈yüz silahlı adamla meydana gelir, halkı ve özgürlüğü çağırır; karşılık yok.** Machiavelli (özet): halkı Medici'nin talihi/cömertliği sağır etmişti, özgürlük Floransa'da tanınmıyordu | ◐ | S34 (özet tırnak), S39 | Özet tırnağı İtalyanca verdi: *"l'uno era dalla fortuna e liberalità de' Medici fatto sordo, l'altra in Firenze non era cognosciuta, non gli fu risposto da alcuno"* (yayın öncesi teyit). |
| Y23 | aynı | **"Palle, palle"** sesleri; "ché tal segno ha l'arme de' Medici" | ◐ | S35 (Guicciardini IV, özet tırnağı) | Machiavelli'de görülmedi; Landucci açılmadı (D52). |
| Y24 | aynı gün | Lorenzo güçlü koruma altında **Medici Sarayı'na** götürülür, **pencerede göründü, alkışlandı** | ◐ | S37, S39 | 19. yy. ikincil; "sargılı boyun" Staley (mum heykel bağlamında). |
| Y25 | aynı gün | **Salviati**, başpiskoposluk giysileriyle **Palazzo Vecchio penceresinden asılır**; **Francesco de' Pazzi** yanına getirilip asılır (Otto sorgusundan sonra) | ◐ | S23, S20, M2:C7.10 | "Salviati'nin Francesco'ya diş geçirmesi": ANEKDOT (D51). |
| Y26 | aynı gün | **Salviati'nin kardeşi ve Franceschino (Francesco) ile birlikte ≈30 kişi daha idam edilir** (DBI Lorenzo, arama özetinin İngilizcesi: "along with about another thirty people"; İtalyanca metin görülmedi); kalabalık başkalarını öldürür (EI) | ◐ | S05 (DBI Lorenzo), S16 (EI) | Toplam "80'den fazla" (T5). "Daha" (≈30 + o ikisi) okuması özet düzeyidedir: yayın öncesi teyit. |
| Y27 | 27–29 Nis | **Jacopo** kaçar; **ertesi gün/birkaç gün içinde yakalanır, sorgulanır, asılır** | ◐ olgu / ○ gün | S19, S33 (16. yy. vakayiname: "ertesi gün"), S46 (28 Nis) | 27/28/29 çelişir (D53). |
| Y28 | sonraki pazar (3 Mayıs) | Jacopo'nun cesedi **bir çocuk çetesince çıkarılır, sürüklenir, Arno'ya (Ponte Rubaconte hizası) atılır** | ○ (tek DBI) | S19 | "Santa Croce'ye gömülmüş" özette **yok** (D52). |
| Y29 | ≈19 Mayıs (26 Nisan + 23 gün: hesap bize ait) | **Francesco'nun cesedi Arno'ya atılır (ölümünden 23 gün sonra)** | ○ | S20 | Tarih 26 Nisan'a göre hesap; Treccani özeti yalnız "23 gün sonra" der. |
| Y30 | 30 Nis | **Giuliano'nun cenazesi San Lorenzo'da** | ◐ | S29 + M5:K24 | |
| Y31 | 3 Mayıs → ≈13 Mayıs | **Maffei** Badia'da yakalanır, itiraf yazar, ≈10 gün sonra asılır (2023 belgesi) ↔ Machiavelli "hemen linç" | ◐ | M2:K53, C7.11–12 | Bu turda yeniden aranmadı. |
| Y32 | 4 Mayıs | **Montesecco itirafı** (Floransa'da, idam cezasından kısa süre önce); hazırlık aşamaları için "ayrıcalıklı kaynak" | ◐ | S21 (DBI Montesecco, A. Falcioni) | Floransa süzgeci. |
| Y33 | 17–19 Mayıs | **Renato (Piero'nun oğlu) ve Guglielmo (Antonio'nun oğlu) Pazzi** Stinche'ye, sonra Volterra Rocca'sına | ○ | Treccani DBI Pazzi maddeleri (S27/S28 ve Piero/Ranieri maddeleri; hangi maddenin söylediği özetten net değil) | Renato'nun akıbeti çelişir (Jacopo'yla birlikte pencereden asıldı ↔ "katılmak istemedi, yine de öldürüldü"). |
| Y34 | 26 Mayıs | **Giulio** (gelecek VII. Clemens) doğar | ◐ | M5:K24, P12; S29 | c11 brif "HAFIZA" demişti → artık ◐. |
| Y35 | 1 Haz 1478 | **Sixtus IV Lorenzo'yu (ve yandaşları/hükümeti) aforoz eder**; gerekçe: Salviati kilise mahkemesi dışında öldü | ◐ | S39, S47, S23 | "iniquitatis filius et perditionis alumnus" biçim kalıbı (Reumont, ○). |
| Y36 | 12 Haz | Riario serbest (Y20) | ◐ | S25 | |
| Y37 | 20 / 22 Haziran (bir kaynak: Roma'dan mektupta "ayın 4'ü") | **Floransa'ya (Floransa, Fiesole, Pistoia piskoposluklarına) interdikt** | ○ (üç değer) | S39, S47, S59 (Daniels) | "Haziran sonu / Temmuz başı". |
| Y38 | yaz sonu 1478 | **Poliziano *Commentarium*** ilk sürüm (yaz sonu); 1480'de revize sürüm; **Gentile Becchi *Florentina Synodus*** Ağustos 1478'de hazırlanıp basılır; **Scala *Excusatio Florentinorum*** | ◐ / ○ | S58 (Celati), S59 (Daniels özeti), M3b:b94 | 1480 revizesinde "Napoli ile ilişkiler nedeniyle" çıkarmalar (özet belirsiz). |
| Y39 | 21 Tem 1478 | Sekizler Konseyi Botticelli'ye "hainleri resmetmek" için 40 iri florin | ○ | M3:K30 | Yer: Vasari Palazzo del Podestà, Isaacson Palazzo Vecchio; bir kaynak "hata" der. |
| Y40 | 1478 | **Bertoldo'ya atfedilen Pazzi madalyası**: bir yüz Lorenzo (*LAVRENTIVS MEDICES · SALVS PVBLICA*), öteki Giuliano (*IVLIANVS MEDICES · LVCTVS PVBLICVS*); 6,6 cm; sahne: koro üstünde büstler | ◐ | S49 (NGA), S50 (V&A) | V&A ile NGA yüz etiketleri ters; sipariş: "Lorenzo" (Academia) ◐. |
| Y41 | sonraki | **Verrocchio'nun üç boy mum Lorenzo heykeli** (Vasari→Isaacson) ; "boynunda sargı" (Staley) | ANEKDOT/○ | S54, S38 | Hiçbiri günümüze ulaşmadı; yerleştirildiği kilise doğrulanmadı. |
| Y42 | sonraki | **Ceza:** Pazzi adı ve arması silinir; evlenme yasağı; Guglielmo (Lorenzo'nun eniştesi) 5–20 mil sürgün (16 yıl); sağ kalanlar 1494'e dek dönemez; **Volterra'daki Pazzi'ler 1480'de salıverilir**, evlilik yasağı kalkar | ◐ | S27, S28, S39 | |

---

## 2. c8 — Aslanın İni: yeni/güncellenen kronoloji (Y43–Y76)

| # | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|
| Y43 | yaz 1478→ | **Pazzi Savaşı:** Papa + Napoli (Alfonso, Calabria Dükü) + Urbino (Federico) ↔ Floransa + Milano | ◐ | S39, S48, S47 (Britannica "War of the Pazzi") | Başlangıç ayı ○ (M2:K57). |
| Y44 | 1478–79 | **Siena ordunun geçişine izin verir**; Alfonso Chianti'ye girer, Radda'yı alır, Castellina'yı kuşatır | ◐ | S39 (Reumont) | |
| Y45 | 7 Eyl 1479 | **Poggio Imperiale: Napoli–Papalık üstün; Floransa yenildi** | ◐ yön / ○ gün | S48; S65 (DBI Alfonso II özeti); S64 (Siena freski kaydı); S39 (7 Eylül) | Reumont ifadesi karışık ("check"); yön için D59. |
| Y46 | Kas 1479 | **Colle di Val d'Elsa uzun kuşatma sonunda düşer** (Reumont: 14 Kasım) | ◐ | S39, S48 | The Collector "Kasım'da iki aylık kuşatma başladı" der: çelişir. |
| Y47 | Kas–Ara 1479 | Askerî masraf hazineyi boşaltıyor; Lorenzo barış girişimi | ◐ | S48 | |
| Y48 | **6 Ara 1479** | **Lorenzo Floransa'dan Napoli'ye yola çıkar** | ◐ | S06 (EI), S08 (DS) | M2'nin "5–6" → 6. |
| Y49 | Pisa, Aralık | Lorenzo Signoria'ya yazıp gidiş nedenini bildirir; **Signoria ona sonradan elçilik ve tam yetki verir** | ○ | Q29 özeti ("bir anlatı" der; sonuçlar arasında Machiavelli'nin İngilizce çevirisi kopyası ve IntraText kitabı vardı; hangisi olduğu net değil) | "silahsız" **yok** (D61). Britannica 1911 "yalnız gitti". |
| Y50 | **18 Ara 1479 – 27 Şub 1480** | **Napoli'de kral Ferrante'nin "misafiri"** | ◐ | S05 (DBI Lorenzo), S48 | 18 Aralık tek DBI. |
| Y51 | **13 Mart ↔ 15 Mart 1480** | **Floransa'ya dönüş / barış** (DBI ve Tomacelli: 13; EI ve Treccani genel: 15) | ◐ çelişir | S05, S09, S06, S07 | Hesap: 6 Aralık → 13 Mart = **98 gün** ("yaklaşık üç ay"). |
| Y52 | 25 Mar 1480 | **Ayrı Napoli–Floransa barışı** (DBI A. Carafa) | ○ | S12 | EdP: Ferrante'nin Lorenzo ile ayrı anlaşması Aralık 1479 (ön anlaşma?) → çelişir. |
| Y53 | 1480 barış | Şartlar (Reumont): savaşta alınan yerler kralın takdirine; **Volterra kulesindeki Pazzi'ler serbest**; Alfonso'ya süreli para | ◐/○ | S39, S27 | DBI Lorenzo: barış "çok avantajlı değildi". |
| Y54 | Nis 1480 | **Balìa → Yetmişler Konseyi** (5 yıllığına; 1485 ve 1490'da yenilenir); Otto di Pratica dış politika, XII procuratori mali/iç işler | ◐ | S05, S63 (Enc. machiavelliana: Lorenzo) | DBI Bandini özetindeki "11 Temmuz 1479 Yetmişler" ifadesi tutarsız → kullanma (D69). |
| Y55 | 17 Nis 1480 | Sixtus IV–Venedik ligi | ◐ | S14 | |
| Y56 | Nisan 1478 | Bandini isyancı ilan (28 Nis 1478, DBI) | ○ | S01 | |
| Y57 | Bahar 1478 | **Bandini İstanbul'a kaçar** (akrabaları var) | ◐ | S01, S02, S51 | |
| Y58 | **8 May 1479** | Pera'daki Floransalı temsilci: **Sultan, Floransa'ya sevgisinden dolayı katili tutuklattı** | ◐ | S03 (DBI Carducci), S01 | Temsilcinin kimliği tartışmalı (Carducci / Frescobaldi / Carlo Baroncelli: Babinger) → ad verilmez (S04). |
| Y59 | **11 Tem 1479** | **Antonio di Bernardetto de' Medici elçi seçilir** ("ticaret işleri ve her şeyden önce Bandini'nin teslimi") | ◐ | S03, S01 | |
| Y60 | **14 Tem 1479** | Antonio aceleyle yola çıkar; Mehmed II katili **Ağustos ortasından fazla hapiste tutmayacaktı** | ◐ | S01, S03 | |
| Y61 | 18 Tem 1479 | Cumhuriyet Carducci'ye Sultan'a teşekkür ve "alçağı güvenli tut" talimatı | ◐ | S03 | |
| Y62 | **24 Ara 1479** | Heyet Floransa'ya varır (Italian Art Society: 23 Aralık) | ◐ / ○ | S01, S53 | |
| Y63 | **29 Ara 1479** | **Bandini, Capitano del Popolo Sarayı (Bargello) pencerelerinden asılır; üstünde hâlâ Doğu giysileri** | ◐ | S01, S51 (Louvre), S02 | 28 Aralık: bir makale ve Leonardo yazıtı için bir özet (D62). **Bu sırada Lorenzo Napoli'deydi** (Y50). |
| Y64 | Ara 1479 | **Leonardo'nun asılı Bandini çizimi** (Bayonne, Musée Bonnat; kurşun kalem + kahverengi mürekkep); yazıt: ad + giysi notları | ◐ | S51, S52 | UNESCO kataloğu ≈1503 der → kullanma. |
| Y65 | Aralık 1455; 1469 | **Floransa'ya Osmanlı ticaret ayrıcalıkları** (1455: bailo/konsolos hakkı + Venedik ile aynı gümrük; 1469: ayrıcalıklar) ; Pera, Edirne, Gelibolu, Bursa'da Floransalı tüccarlar | ○ | S56, S68 (Fleet, özet) | Tek makale özetleri. |
| Y66 | c. 1480–81 | **Bertoldo'nun II. Mehmed madalyası**: Gentile Bellini'ye dayanır; Lorenzo'nun teşekkür hediyesi olduğu **düşünülür (kesin belge yok)** | ◐ hedge'li | S55, M3:§5.18 (V&A, Frick, Met) | 1480 (müzeler) ↔ 1481 (altyazı). |
| Y67 | **28 Tem 1480** | **Gedik Ahmed Paşa Otranto yakınına çıkar** | ◐ | S43 (Historians' History), M2:K65 | |
| Y68 | **Ağustos 1480** | **Otranto düşer** (11 Ağustos: S43; 8 Ağustos: DBI D. Carafa; 14 Ağustos katliam: M2 HAFIZA-O) | ◐ çelişir | S43, S13 | Ölü sayıları **kullanılmaz** (D67). |
| Y69 | Ağu–Eki 1480 | **Ferrante Alfonso'yu ordusuyla Toskana'dan çağırır**; Ekim 1480'de Roma'da Toskana'dan çekilme kararı | ◐ / ○ | S43, S12 | |
| Y70 | **3 Ara 1480** | **Floransa–Papalık barışı, absolüsyonla mühürlenir** (EdP) ↔ **23 Aralık** (Reumont: Papa–Napoli–Floransa–Milano barışı, Venedik'in katılımına bağlı) | ◐ / ○ | S14, S39, S42 | Tören ayrıntısı **bulunamadı** (D68). DBI Lorenzo: Otranto Papa'yı yumuşattı. |
| Y71 | Ekim 1480 / 1481 | Floransalı ressamlar Sistina için Roma'ya: "27 Ekim 1480" (Wikipedia Rosselli, bible.gallery) ↔ işler 1481'de başlar (Vatikan Müzeleri) | ○ | S57 | D71. |
| Y72 | 3 May 1481 | II. Mehmed ölür | HAFIZA-Y | M2:K70 | Tool'la doğrulanmadı; bir özet: Medici ajanı Paolo da Colle ölümü Haziran 1481'de bildirdi (○, S56). |
| Y73 | 10 Eyl 1481 | **Otranto Napoli'ye geri döner** ("on bir aylık kuşatmadan sonra") | ◐ | S43, M2:K70 | |
| Y74 | — | DBI Ferdinando I: Mehmed'in kararı Ferrante'nin İtalyan düşmanlarınca kışkırtılmış gibi **görünmüyor**, İtalya'daki dağınıklık cesaretlendirdi | ○ | S11 | "Lorenzo Türkleri çağırdı" propagandasına karşı (D74). |
| Y75 | — | Ippolita Sforza'nın (Alfonso'nun eşi) imzası Medici adına barışı mühürledi (DBI özeti) | ○ | S10 | Tek özet; **kullanma**. |
| Y76 | 1481–82 | 1477'den 1481 sonuna: Medici şube kapanışları (Londra 1477–78, Milano 1478–79, Avignon 1479–80, Brugge 1480–81) c9'a kapı | ◐/○ | M1b:b51–b54 | c9 brif ile uyumlu. |

---

## 3. T — kaynaklar-arası varyant tabloları

### T1 · Sinyal (Pazzi, "ne zaman vurulacak?")
| Varyant | Kim söyler | Sınıf | Not |
|---|---|---|---|
| **Ayini yöneten papazın komünyon alması** | DBI Jacopo de' Pazzi (S19; arama özetinin İngilizcesi: "when the officiant took communion, the agreed signal to begin the action…"; İtalyanca metin görülmedi); Guicciardini *Storie fiorentine* IV (S35; özetleyicinin İtalyanca anlatımı, **birebir alıntı değil**: "appena il prete che cantava la messa si comunicò, al segnale stabilito, Franceschino de' Pazzi, a braccetto con Giuliano, lo assalì"); Machiavelli *Istorie* VIII, İngilizce çeviri özeti (M2:K46) | ◐ (≥3, hepsi Floransalı/Treccani) | İtalyanca Machiavelli sayfası (Q22) özette bu cümleyi vermedi: **yayın öncesi teyit.** |
| **Ekmeğin kaldırılması (elevation)** | History Today (S44: "11 çanı", ○); Brocku sergisi (S45: "büyük olasılıkla kaldırma anında"); Staley (S38); bir özet: "komplocuların ifadesine göre" | ◐ ama popüler/19. yy. | "Kaldırma anında herkes diz çöker" ayrıntısı bir özette; Poliziano'ya atfı **doğrulanmadı**. |
| Ekmeğin bölünmesi / "Ite, missa est" | M2:K46 (tek özet) | ○ | Kullanma. |
| Poliziano, Montesecco, Landucci | — | **görülmedi** | X01. |
**Davranış:** iki varyant tek cümlede ("bazı anlatılar… bazıları…"); ayinin hangi anı olduğu söylenmez. Liturji notu (hesap bize ait): komünyon, kaldırmadan sonra gelir; ikisi aynı dakikalarda değildir.

### T2 · Papa, Federico ve Napoli'nin rolü (taraflar ayrı)
| Taraf / kaynak | Ne söyler | Sınıf |
|---|---|---|
| **Floransa** (*Excusatio Florentinorum*, Scala; Montesecco itirafı 4 May 1478; Poliziano) | Papa'yı ve Riario'yu suçlar; itiraf metni *Excusatio*'ya girdi | ◐ (S21, M2:K54) — **propaganda süzgeci** |
| **Roma** | Sixtus IV, komploya karışmayı inkâr etti; Lorenzo'yu **Salviati kilise mahkemesi dışında öldü** diye aforoz etti | ◐ (S14 EdP; S23 DBI Salviati) |
| **EI Pazzi (1935)** | Papa komployu **biliyordu**, iki Medici'nin öldürülmesini bilip bilmediği **belirsiz**; Montesecco sorgusu onu **aklıyor gibi** ama Papa'nın Lorenzo'nun Floransa dışında olmasına dair bir sözü kayıtlı | ◐ |
| **DBI Sisto IV** | Komplo **kesinlikle Papa'nın onayıyla**, ayrıntılar belirsiz; Napoli Kralı ve Urbino ile **muhtemelen göz yumma** | ◐ |
| **Treccani "Eco" serisi** | Komplo Papa ve Federico'nun yardımıyla | ○ |
| **Simonetta 2004/2008** | Federico'nun 14 Şubat 1478 şifreli mektubu (alıcı çelişir); eleştirmenler "ilginç ama abartılı olabilir" | ◐ |
| **Simonetta 2014 / Maffei itirafı 2023** | "Sixtus IV Kilise devletinde yeni tiranlar"; Maffei: Papa, Napoli Kralı, Urbino Dükü kışkırtıcı; Riario habersiz | ○ / ◐ (zorla yazılmış olabilir) |
| Popüler | Montesecco, "onurlu kafa kesme" karşılığı itiraf yazdı; "Papa'yı da ele verdi" | ○ |
| Papa'nın **sözü** | "ölüm istemem" gibi söz bulunamadı; EI yalnız dolaylı anar | **YAZILMAZ** |

### T3 · Lorenzo'nun kaçışı
| Ayrıntı | Kaynak | Sınıf |
|---|---|---|
| Saldırganlar iki papaz (Maffei, Stefano) | S21, S34, M2:K44 | ◐ |
| "Jacopo'nun iki adamı" | S05 (DBI Lorenzo) | ◐ (aynı iki kişi olabilir) |
| Boynundan hafif yara; kendini savundu | S16 (EI), S05, S37, S47 | ◐ |
| Kılıcını çekip koroya sıçradı (Filippo Strozzi'ye atfedilen görgü tanığı özeti) | S40 | ○ (metin görülmedi) |
| **Kuzey sakristi, Michelozzo ve Luca della Robbia'nın tunç kapıları**; Poliziano + Cavalcanti'ler kapattı | S37; S05 ("Sagrestia Nuova") | ◐ / ○ adlar |
| Poliziano hayatını kurtardı | S47 (Britannica) | ◐ |
| Francesco Nori ölür | S37, S38, M2 | ◐ |
| Antonio Ridolfi yarayı zehir korkusuyla emer | S38 (tek, eski popüler); S31 (DBI Ridolfi) anmaz | ANEKDOT ○ |
| Kardinal altara sığınır | M2:P10 | HAFIZA-O |
| Eve dönüş: silahlı gençler; pencerede | S37, S39 | ◐ |

### T4 · Giuliano
| Ayrıntı | Kaynak | Sınıf |
|---|---|---|
| Evinden alınır (ayin başlamıştır) | S34 | ◐ |
| Bandini önce vurur (Machiavelli) ↔ **Franceschino kol kolayken** saldırır (Guicciardini) | S34, S35 | ◐ çelişir |
| ≈19 yara (18: bir kaynak) | S46, S37, S38 | ◐ |
| Yaş **24** | M5:D24 | ◐ |
| Cenaze 30 Nisan, San Lorenzo | S29 | ◐ |
| Gayrimeşru oğlu Giulio 26 Mayıs 1478 | M5:K24 | ◐ |
| 2007 ekshümasyon/kemik bulgusu | belgesel özeti ("kemiklerde görülür") | ○ — kullanma |

### T5 · Halkın tepkisi ve misilleme ölçeği
| Madde | Değer | Kaynak | Sınıf |
|---|---|---|---|
| "Palle, palle" | Guicciardini IV (Medici armasındaki toplar) | S35 | ◐ |
| Jacopo'ya cevap | "kimse cevap vermedi" (Machiavelli) | S34 | ◐ |
| Aynı gün idam | Salviati'nin kardeşi + Franceschino ile birlikte ≈30 kişi daha; kalabalık başkalarını öldürdü | S05, S16 | ◐ |
| Toplam | "80'den fazla" (Wikipedia, europeupclose); "yüz civarı" HAFIZA-D; "beş kişi pencerelerden asıldı" tek site | M2:§3 | ◐ / ○ |
| Pazzi aile cezası | isim/arma silinir, evlenme yasağı; Guglielmo sürgün; sağ kalanlar Volterra kalesinde, 1480'de salıverilir | S27, S28, S39 | ◐ |
| Maffei | 3 Mayıs yakalanma, ≈10 gün sonra asılma (2023) ↔ "hemen linç" (Machiavelli) | M2:K53 | ◐ |
| Montesecco | itiraf 4 Mayıs, sonra idam (kafa kesme: **doğrulanmadı**) | S21 | ◐ |

### T6 · Saat çıpaları: ne var, ne yok
| Çıpa | Kaynak | Sınıf | Kullanım |
|---|---|---|---|
| "Pazar sabahı" | Machiavelli, EI, Strozzi özeti | ◐ | söylenir |
| "Yüksek/solemn ayin", kardinal onuruna | EI, Enc. machiavelliana, DBI Riario | ◐ | söylenir |
| "Ayin başlamıştı, Giuliano yoktu" | Machiavelli | ◐ | söylenir |
| Sinyal anı = komünyon/kaldırma | T1 | ◐ | iki varyant |
| **"11 çanı"** | History Today | ○ | söylenmez (yayın öncesi teyit) |
| Salviati/Palazzo eşzamanlı | DBI Salviati ("seçilen günde, öteki komplocular kardeşlerle ilgilenirken") | ◐ | "aynı sırada" |
| Jacopo meydanda "öğleden sonra" | M2:P12 | HAFIZA | söylenmez |
| Asılmalar "aynı gün" | DBI Lorenzo | ◐ | "aynı gün" |
| "Akşam/gece" | — | **kaynak yok** | görsel dil (YORUM) |
| Ertesi pazar (3 Mayıs): Jacopo'nun cesedi | DBI Jacopo | ○ | "sonraki pazar" |

### T7 · Paskalya sorusu
- **Jülyen Paskalya 1478 = 22 Mart** (Meeus algoritması, yerel hesap; 1477→6 Nisan, 1479→11 Nisan, 1480→2 Nisan, 1481→22 Nisan). **26 Nisan 1478 = Paskalya + 35 gün = Paskalya'dan sonraki 5. Pazar** (hesap bize ait). 25 Nisan Cumartesi.
- Görülen Treccani/Wikisource/Gutenberg özetlerinin **hiçbirinde "Pasqua/Easter" yok**: "messa solenne/yüksek ayin" (◐ yokluk). "Easter Mass" yalnız popüler özetlerde.
- Landucci/Poliziano'da "Pasqua" geçip geçmediği **açılmadı** (X01).
- **Ayinin adı:** görülen özetlerde "messa solenne / yüksek ayin"; liturjik gün adı Paskalya sonrası 5. Pazar (Rogate / *Vocem iucunditatis* — **HAFIZA-O**, araçla doğrulanmadı) → metne girmez. "Sagrestia delle Messe" = kuzey sakristi eşitliği de HAFIZA-O (DBI Lorenzo "Sagrestia Nuova", Gardner "northern sacristy").

### T8 · Lorenzo'nun Napoli tarihleri
| Olay | Değer | Kaynak |
|---|---|---|
| Ayrılış | **6 Aralık 1479** | EI, DS (S06, S08) ◐; M2 "5–6" |
| Pisa mektubu | Aralık | Q29 özeti (kaynak adı net değil) ○ |
| Napoli'ye varış | **18 Aralık** | DBI Lorenzo ○ |
| Napoli'den çıkış | **27 Şubat 1480** | DBI ○ |
| Floransa'ya dönüş | **13 Mart** (DBI, Tomacelli) ↔ **15 Mart** (EI, Treccani genel) | ◐ çelişir |
| Ayrı barış | 25 Mart 1480 (DBI A. Carafa) | ○ |
| Toplam | 6 Aralık → 13 Mart = **98 gün**; 18 Aralık → 27 Şubat = 71 gün | hesap bize ait |

### T9 · Bandini zaman çizgisi (DBI Bandini + Carducci + Louvre)
28 Nis 1478 isyancı ilanı (○) → bahar sonu İstanbul → 8 Mayıs 1479 Pera mektubu → 11 Temmuz Antonio de' Medici seçilir → 14 Temmuz yola çıkar → (teslim: Ağustos?) → 24 Aralık Floransa → 29 Aralık asılma (Bargello) → Leonardo çizimi. **Yolculuk süresi ve rota belirsiz.**

---

## 4. TR-BAĞ güncellemesi (O ekseni)

| Soru | Bu turdan bulgu | Sınıf |
|---|---|---|
| **Bandini'yi kim yakalattı, kim getirdi?** | Sultan II. Mehmed tutuklattı (Floransalı temsilcinin 8 Mayıs 1479 mektubu: Floransa sevgisinden); **Antonio di Bernardetto de' Medici** elçi olarak alıp getirdi | ◐ (DBI Bandini + DBI Carducci + Louvre: "Sultan teslim etti") |
| **Pera temsilcisi kim?** | Carducci (DBI Carducci: "konsolosluğunu sayma nedeni yok"), Battista Frescobaldi (Capponi), Carlo Baroncelli (Babinger) | ○ tartışmalı → **ad verilmez** |
| **Mehmed neden?** | Floransalı temsilcinin yazdığına göre "sevgi"; Floransa–Osmanlı ilişkisi iyi (1455 ayrıcalık, 1469) | ○ (yorum) |
| **Osmanlı kaynaklarında kayıt?** | Aranmadı/bulunamadı | X |
| **Bertoldo madalyası** | "Lorenzo, Sultan'ın katili yakalatmasına teşekkür olarak ısmarlamış olabilir"; DBI Bandini/Carducci özeti "sundu" der (kip belirsiz) | ◐ hedge'li |
| **Madalya ters yüzü** | Mehmed zafer arabasında, üç taçlı kadın figürüne bağlı; arabada Napoli krallarının alevli sandalye amblemi (olası Napoli saldırısı imâsı) | ◐ (V&A, Met; M3) |
| **Floransa–Osmanlı ticaret** | Aralık 1455: Floransa'nın talebi kabul, bailo ve Venedik ile eşit gümrük; Pera/Edirne/Gelibolu/Bursa'da tüccarlar; 1469 ayrıcalıkları | ○ |
| **Otranto** | 28 Temmuz çıkarma, Ağustos düşüş; Napoli ordusu Toskana'dan çekilir; Papa Floransa'yla barışır | ◐ |
| **"Lorenzo Türkleri çağırdı"** | DBI Ferdinando I: Sultan'ın kararı Ferrante'nin düşmanlarınca kışkırtılmış gibi görünmüyor | ○ (propaganda iddiası) |
| **Bandini soyadı** | III. Murad'ın 1588 fermanındaki Orazio Bandini ile **bağ yok** (M3 §10) | uyarı |

---

## 5. Sanat ve propaganda (c7 sonu / c8 başı)

| Nesne | Ne | Sınıf | Not |
|---|---|---|---|
| **Botticelli — rezil edici resim (*pittura infamante*)** | 21 Tem 1478, 40 iri florin; yer Vasari: Palazzo del Podestà; Isaacson: Palazzo Vecchio | ○ | Kayıp; hepsini (80+) resmetmek akla yatkın değil (M3:K30). |
| **Verrocchio — mum heykeller** | Vasari: üç boy mum Lorenzo heykeli; "boynunda sargı" (Staley); günümüze ulaşmadı | ANEKDOT ◐ | Kilise adı doğrulanmadı. |
| **Bertoldo — Pazzi madalyası** | NGA 6,6 cm; iki yüz: *SALVS PVBLICA* / *LVCTVS PVBLICVS*; V&A'ya göre koro sahnesi | ◐ | Atıf: Bertoldo (NGA sanatçı sayfası; Academia: Lorenzo'dan sipariş). |
| **Poliziano — *Commentarium*** | İlk sürüm 1478 yaz sonu; Sallustius *Catilina* modeli; propaganda; 1480 revizesi | ◐ | Celati 2015/2019; Perosa 1958; Simonetta edisyonu. |
| **Scala — *Excusatio Florentinorum*; Becchi — *Florentina Synodus*** | Basılı bildiriler; Montesecco itirafı *Excusatio*'da | ◐ / ○ | "Afiş" yerine **bildiri/broşür** (matbaa). |
| **Leonardo — Bandini çizimi** | Bayonne; kurşun + mürekkep; Aralık 1479 | ◐ | UNESCO ≈1503 → kullanma. |
| **Sistina heyeti** | Ressamlar Roma'ya (27 Ekim 1480 ↔ 1481) | ○ | D71. |

---

## 6. Sayılar ve ölçüler (yeni/güncel)

| Konu | Değer(ler) | Sınıf | Not |
|---|---|---|---|
| Giuliano'nun yaşı | **24** | ◐ | 25/16 yanlış |
| Riario'nun yaşı | 17 (10 Aralık 1477'de) | ◐ | |
| Giuliano'ya yara | 19 (18) | ◐ | "diye sayılır" |
| Jacopo'nun adamları | ≈100 | ◐ | Machiavelli, Reumont |
| Salviati'nin adamları | ≈30 | ○ | Gardner |
| Aynı gün idam | Salviati'nin kardeşi + Franceschino ile birlikte ≈30 kişi daha | ◐ | DBI Lorenzo |
| Toplam | 80+ | ◐ | tek sayı verilmez |
| Francesco'nun cesedi Arno'ya | ölümünden 23 gün sonra | ○ | |
| Napoli kalışı | 98 gün (6 Ara→13 Mar) / 71 gün (18 Ara→27 Şub) | hesap | |
| Yetmişler | 5 yıl; 1485, 1490 yenileme | ◐ | |
| Botticelli | 40 iri florin | ○ | ekran kartı |
| Pazzi madalyası | 6,6 cm | ◐ | ekran dışı |

---

## 7. DÜZELTME / NÜANS (D47 → ; M5'in D46'sının devamı)

| Kod | Önceki ifade | Bulgu | Tür |
|---|---|---|---|
| **D47** | KAPSAM §5/§7, M2:D1 "Paskalya değil" | **Doğrulandı (hesap):** Jülyen Paskalya 22 Mart 1478; 26 Nisan = 5. Pazar. Görülen metinlerde "Pasqua/Easter" geçmiyor. Not: Floransa belgesinde 22 Mart 1478 "1477" yazılır. | DOĞRULAMA |
| **D48** | M2:K47 "uyluğunu yaraladı (blog)" | DBI Francesco: **ağır bacak yaralarıyla** amcasının evine gitti; kendi hançeriyle yaraladı ○ | NÜANS (↑) |
| **D49** | M2:K49 "Perugialılar kilitli odada (HAFIZA-O)" | DBI Salviati: **adamları sarayın bir odasında tutuldu, sonra asıldı**; Gardner: ≈30 adam | ◐ (↑) |
| **D50** | M2:K50 "Jacopo 'libertà' (○)" | Machiavelli (it.wikisource özet tırnağı) + Reumont (≈100 silahlı): **◐** | ◐ (↑) |
| **D51** | M2:§4.6 "Salviati ısırması bulunamadı" | **Poliziano'nun anlatısında** (DBI Salviati özeti: "a grisly scene of cannibalism"; Weinstein *Savonarola* özeti): Salviati asılırken Francesco'nun göğsüne dişlerini geçirir | ANEKDOT ◐ (kim: Poliziano) |
| **D52** | M2:§4.7 "Jacopo'nun cesedi HAFIZA-D"; M2 "palle HAFIZA-Y" | **DBI Jacopo:** sonraki pazar çocuk çetesi çıkarır, sürükler, **Arno'ya atar (Ponte Rubaconte)**; Santa Croce'ye gömülmesi özette **yok**. **"Palle" Guicciardini'den**, Machiavelli'de görülmedi | ○ / ◐ |
| **D53** | M2:K52 "28 (29) Nis" | Üç değer: **27** (16. yy. vakayiname "ertesi gün"), **28** (Wikipedia), **29** (HAFIZA-O) → "birkaç gün içinde" | ÇELİŞKİ |
| **D54** | M2:§4.3 Papa'nın rolü | EI: bilgisi var, öldürme belirsiz; DBI Sisto IV: onayıyla kesin, modalite belirsiz, Napoli/Urbino muhtemel; Sixtus inkâr etti (T2) | NÜANS (↑) |
| **D55** | M2:K43 ziyafet "Cumartesi 25" | Machiavelli: **Pazar 26 Nisan, Fiesole'de ziyafet**, Giuliano gelmeyince aynı gün Duomo; DBI Lorenzo: ayinden önce sarayda, yanlış anlaşılma | ÇELİŞKİ → gün/yer söylenmez |
| **D56** | M2:D2 "sinyal çözülemedi" | **Komünyon ≥3 yerde (DBI Jacopo, Guicciardini, Machiavelli çevirisi)**; kaldırma popüler (T1) | NÜANS (↑) |
| **D57** | M2:P10 "kardinal altara sığınır" HAFIZA-O | DBI Riario: **tutuklandı (linçten kurtuldu), rehin, 12 Haziran serbest**; ayin **onuruna** (Enc. machiavelliana) ↔ **yönetti** (EI) | ◐ (↑) |
| **D58** | M2:K56 "aforoz 1 Haz (HAFIZA-O)" | **◐ 1 Haziran 1478**; interdikt 20/22 Haziran (çelişir); gerekçe: Salviati'nin kilise mahkemesi dışında ölümü (DBI Salviati) | ◐ (↑) |
| **D59** | M2:K57 "Poggio Imperiale Floransa yenilgisi (HAFIZA-D)" | **Yön doğru:** DBI Alfonso II ve Collector: Alfonso Poggio Imperiale'de ve Colle kuşatmasında galip; Siena freski "Sienalıların Floransalılara zaferi". Gün 7 Eylül **tek kaynak** (Reumont ifadesi karışık). | ◐ (↑) |
| **D60** | M2:K61 "5–6 Aralık; varış 18 Aralık (HAFIZA-D)" | **6 Aralık (EI, DS)**; varış 18 Aralık (DBI); çıkış 27 Şubat; dönüş **13/15 Mart** | ◐ (↑) |
| **D61** | M2:D4 "silahsız" (NÜANS) | **Kaynak yok.** Yalnız dinî-kişisel bir blogda "silahsız ve yalnız" (kaynak sayılmaz). Britannica 1911 "yalnız". Machiavelli/Reumont çizgisinde Lorenzo Pisa'dan yazdı, **Signoria sonradan yetki verdi** (○). **"Silahsız" denmez.** | DÜZELTME |
| **D62** | M2:K62 "29 Aralık (○)" | **◐ 29 Aralık** (DBI Bandini + Louvre + Treccani kısa madde); 28 Aralık tek makale; Italian Art Society 23 Aralık (varış?) | ◐ (↑) |
| **D63** | M2:D7 "getirilişin kimler eliyle olduğu doğrulanamadı" | **Antonio di Bernardetto de' Medici** (DBI Bandini/Carducci) ; varış 24 Aralık | ◐ (↑) |
| **D64** | M2:§5.2 "yakalayan: görevliler mi tüccarlar mı?" | **Sultan'ın emriyle tutuklanma** (Pera mektubu); temsilcinin kimliği tartışmalı | ◐ (↑) |
| **D65** | M2:§5.2 "Mehmed neden?" | Floransalı temsilcinin aktarımı: "sevgi". Gerisi yorum | ○ |
| **D66** | M2:K69 Bertoldo "olası" | Kip korunur; "teşekkür hediyesi olduğu **düşünülür**"; tarih 1480/1481 | NÜANS |
| **D67** | M2:K65–66 Otranto | Düşüş **8/11 Ağustos** çelişir; katliam 14 Ağustos ve ölü sayıları HAFIZA → **söylenmez** | ÇELİŞKİ |
| **D68** | M2:K68 "af töreni (HAFIZA-D)" | **3 Aralık 1480 absolüsyon (EdP)**; tören ayrıntısı/15 kadırga **bulunamadı** (iki ek deneme) | NÜANS |
| **D69** | M2:K64 "Nis 1480 Yetmişler (HAFIZA-O)" | **◐ Nisan 1480 Balìa → Yetmişler** (DBI Lorenzo + Enc. machiavelliana). DBI Bandini özeti 11 Temmuz 1479'da "Yetmişler" der: **kullanma** | ◐ (↑) |
| **D70** | M2:C8.7 "Pazzi'ler Volterra kalesinde; ad-arma yasağı 1494'te kalkar" | İsim/arma silinir + evlenme yasağı (DBI Guglielmo/Cosimo); **Volterra tutsakları 1480'de salıverilir**; dönüş izni 1494 sonrası (Guglielmo ailesi) | NÜANS |
| **D71** | M2:K71 "Sistina 1481–82" | Ressamlar Roma'ya **27 Ekim 1480** (Wikipedia, bible.gallery) ↔ Vatikan: işler 1481–82. "Sözleşme 27 Ekim 1481" HAFIZA | ÇELİŞKİ |
| **D72** | M3 mum heykeller yok | Vasari→Isaacson: **üç boy mum Lorenzo**; ulaşmadı | ANEKDOT ◐ |
| **D73** | — | Florentina Synodus Ağustos 1478 (Daniels özeti ○); Poliziano ilk sürüm "yaz sonu" | ○ |
| **D74** | M2:§4.17 "Lorenzo Türkleri çağırdı" | DBI Ferdinando: kışkırtılmış görünmüyor | ○ (↑) |
| **D75** | M2:C7.11 Maffei "bir gün önce öğrendi" | Bu turda yeniden aranmadı; ◐ korunur | — |
| **D76** | M2:§3 "Giuliano 19" | ◐ | (↑) |
| **D77** | KAPSAM §3 / `compose.py` "Perde II GÜZELLİK" | `YONETMENLIK_REHBERI.md` §5/§9: **"PERDE II — BEDEL" (c7–c11)**, **Parça 2 c7 ile açılır (soğuk açılış)**; motor `PERDE_OF` hâlâ eski (c4–c10) | ÇATIŞMA → ana ajan kararı |
| **D78** | brif c11 "Giulio–Clemens HAFIZA" | **◐ (M5:K24,P12 + S29)**: c11 brif güncellenebilir | (↑) |

---

## 8. Kaynak anahtarı (URL'ler; hepsi arama sonuçlarında **görüldü**, **açılmadı**)

| S | Kaynak | URL |
|---|---|---|
| S01 | DBI Bandini dei Baroncelli, Bernardo (G. Pampaloni, c. 5, 1963) | https://www.treccani.it/enciclopedia/bandini-dei-baroncelli-bernardo_(Dizionario-Biografico)/ |
| S02 | Treccani kısa madde Bandini, Bernardo | https://www.treccani.it/enciclopedia/bernardo-bandini/ |
| S03 | DBI Carducci, Lorenzo | https://www.treccani.it/enciclopedia/lorenzo-carducci_(Dizionario-Biografico)/ |
| S04 | DBI Frescobaldi, Battista | https://www.treccani.it/enciclopedia/battista-frescobaldi_(Dizionario-Biografico)/ |
| S05 | DBI Medici, Lorenzo de' (c. 73, 2009) | https://www.treccani.it/enciclopedia/lorenzo-de-medici_(Dizionario-Biografico)/ |
| S06 | EI Medici, Lorenzo de', detto il Magnifico | https://www.treccani.it/enciclopedia/medici-lorenzo-de-detto-il-magnifico_(Enciclopedia-Italiana)/ |
| S07 | Treccani genel Lorenzo | https://www.treccani.it/enciclopedia/medici-lorenzo-de-detto-il-magnifico/ |
| S08 | Dizionario di Storia: Lorenzo | https://www.treccani.it/enciclopedia/lorenzo-de-detto-il-magnifico-medici_(Dizionario-di-Storia)/ |
| S09 | DBI Tomacelli, Marino | https://www.treccani.it/enciclopedia/marino-tomacelli_(Dizionario-Biografico)/ |
| S10 | DBI Sforza, Ippolita | https://www.treccani.it/enciclopedia/ippolita-sforza_(Dizionario-Biografico)/ |
| S11 | DBI Ferdinando I d'Aragona | https://www.treccani.it/enciclopedia/ferdinando-i-d-aragona-re-di-napoli_(Dizionario-Biografico)/ |
| S12 | DBI Carafa, Antonio | https://www.treccani.it/enciclopedia/antonio-carafa_res-edb58c36-87e9-11dc-8e9d-0016357eee51_(Dizionario-Biografico)/ |
| S13 | DBI Carafa, Diomede | https://www.treccani.it/enciclopedia/diomede-carafa_(Dizionario-Biografico)/ |
| S14 | Enciclopedia dei Papi: Sisto IV | https://www.treccani.it/enciclopedia/sisto-iv_(Enciclopedia-dei-Papi)/ |
| S15 | DBI Sisto IV | https://www.treccani.it/enciclopedia/papa-sisto-iv_(Dizionario-Biografico)/ |
| S16 | EI Pazzi | https://www.treccani.it/enciclopedia/pazzi_(Enciclopedia-Italiana)/ |
| S17 | Dizionario di Storia: Pazzi, congiura dei | https://www.treccani.it/enciclopedia/congiura-dei-pazzi_(Dizionario-di-Storia)/ |
| S18 | Treccani: Pazzi, congiura dei | https://www.treccani.it/enciclopedia/congiura-dei-pazzi/ |
| S19 | DBI Pazzi, Jacopo de' (vol. 82, 2015) | https://www.treccani.it/enciclopedia/jacopo-de-pazzi_(Dizionario-Biografico)/ |
| S20 | Treccani Pazzi, Francesco de' | https://www.treccani.it/enciclopedia/francesco-de-pazzi/ |
| S21 | DBI Montesecco (A. Falcioni) | https://www.treccani.it/enciclopedia/giovanni-battista-da-montesecco_(Dizionario-Biografico)/ |
| S22 | DBI Maffei, Antonio | https://www.treccani.it/enciclopedia/antonio-maffei_(Dizionario-Biografico)/ |
| S23 | DBI Salviati, Francesco | https://www.treccani.it/enciclopedia/francesco-salviati_(Dizionario-Biografico)/ |
| S24 | DBI Bracciolini, Iacopo | https://www.treccani.it/enciclopedia/iacopo-bracciolini_(Dizionario-Biografico)/ |
| S25 | DBI Riario Sansoni, Raffaele | https://www.treccani.it/enciclopedia/raffaele-riario-sansoni_(Dizionario-Biografico)/ |
| S26 | Enc. machiavelliana: Riario, Raffaello | https://www.treccani.it/enciclopedia/raffaello-riario_(Enciclopedia-machiavelliana)/ |
| S27 | DBI Pazzi, Guglielmo de' | https://www.treccani.it/enciclopedia/guglielmo-de-pazzi_(Dizionario-Biografico)/ |
| S28 | DBI Pazzi, Cosimo de' | https://www.treccani.it/enciclopedia/cosimo-de-pazzi_(Dizionario-Biografico)/ |
| S29 | DBI Medici, Giuliano de' | https://www.treccani.it/enciclopedia/giuliano-de-medici_res-f6ca07e6-dcde-11df-9ef0-d5ce3506d72e_(Dizionario-Biografico)/ |
| S30 | Enc. machiavelliana: Giuliano di Piero | https://www.treccani.it/enciclopedia/giuliano-di-piero-de-medici_(Enciclopedia-machiavelliana)/ |
| S31 | DBI Ridolfi, Antonio | https://www.treccani.it/enciclopedia/antonio-ridolfi_(Dizionario-Biografico)/ |
| S32 | Treccani Lingua italiana: "Le sorprese di Machiavelli: la Congiura dei Pazzi" | https://www.treccani.it/magazine/lingua_italiana/articoli/percorsi/percorsi_212.html |
| S33 | Treccani "Le signorie in Italia" (Eco serisi; 16. yy. vakayiname alıntısı) | https://www.treccani.it/enciclopedia/le-signorie-in-italia_(Storia-della-civilt%C3%A0-europea-a-cura-di-Umberto-Eco)/ |
| S34 | Machiavelli, *Istorie fiorentine* VIII (it.wikisource) | https://it.wikisource.org/wiki/Istorie_fiorentine/Libro_ottavo |
| S35 | Guicciardini, *Storie fiorentine* IV (it.wikisource) | https://it.wikisource.org/wiki/Storie_fiorentine_dal_1378_al_1509/IV |
| S36 | Guicciardini, *Storie fiorentine* XIII "Viaggio a Napoli" (it.wikisource) | https://it.wikisource.org/wiki/Storie_fiorentine_dal_1378_al_1509/XIII |
| S37 | Gardner, *The Story of Florence* (Gutenberg) | https://www.gutenberg.org/cache/epub/37793/pg37793-images.html |
| S38 | Staley, *The Tragedies of the Medici* (Gutenberg) | https://www.gutenberg.org/files/10877/10877-h/10877-h.htm |
| S39 | Reumont, *Lorenzo de' Medici* c. 1 ve 2 (Gutenberg) | https://www.gutenberg.org/cache/epub/50624/pg50624-images.html · https://www.gutenberg.org/cache/epub/50625/pg50625-images.html |
| S40 | *Florentine Palaces and Their Stories* (Gutenberg; F. Strozzi görgü tanığı alıntısı) | https://www.gutenberg.org/files/71464/71464-h/71464-h.htm |
| S41 | *Florentine Villas* (Gutenberg) | https://www.gutenberg.org/files/76926/76926-h/76926-h.htm |
| S42 | Lodge, *The Close of the Middle Ages* (Gutenberg) | https://www.gutenberg.org/files/62493/62493-h/62493-h.htm |
| S43 | *The Historians' History of the World* IX (Gutenberg) | https://www.gutenberg.org/files/71209/71209-h/71209-h.htm |
| S44 | History Today "The Pazzi Conspiracy" | https://www.historytoday.com/archive/months-past/pazzi-conspiracy |
| S45 | Brocku sergisi "The Pazzi Conspiracy" | https://exhibits.library.brocku.ca/s/botticelli-savonarola-and-the-politics-of-late-quattrocento-florence/page/the-pazzi-conspiracy |
| S46 | Wikipedia "Pazzi conspiracy" | https://en.wikipedia.org/wiki/Pazzi_conspiracy |
| S47 | Britannica: Pazzi conspiracy / Pazzi family / War of the Pazzi / Lorenzo / Sixtus IV | https://www.britannica.com/event/Pazzi-conspiracy · https://www.britannica.com/topic/Pazzi-family · https://www.britannica.com/topic/War-of-the-Pazzi |
| S48 | The Collector "A Pope's Revenge: The Bloody War That Followed the Pazzi Conspiracy" | https://www.thecollector.com/war-pazzi/ |
| S49 | NGA Pazzi Conspiracy Medal (ön/arka) | https://www.nga.gov/collection/art-object-page.70392.html · https://www.nga.gov/collection/art-object-page.70393.html |
| S50 | V&A Pazzi conspiracy medal | https://collections.vam.ac.uk/item/O349106/pazzi-conspiracy-medal-unknown/ |
| S51 | Louvre mini-site (Leonardo; Bayonne çizimi) | https://mini-site.louvre.fr/trimestriel/2019/l%C3%A9onard_de_vinciGB/32/ |
| S52 | Richter no. 664 | https://www.fromoldbooks.org/R.bak/section-10/item-664.html · https://interconnected.org/more/davinci/664.html |
| S53 | Italian Art Society "On this day 23 December 1479…" | https://www.italianartsociety.org/2019/12/on-this-day-23-december-in-1479-bernardo-bandini-baroncelli-one-of-the-assassins-involved-in-the-pazzi-conspiracy-a-plot-to-murder-lorenzo-and-giuliano-de-medici-was-captured-in-constan/ |
| S54 | Isaacson *Leonardo da Vinci* (erenow kopyası; Vasari–Verrocchio mum heykeller) | https://erenow.org/biographies/leonardo-da-vinci-the-flights-of-the-mind/22.php |
| S55 | Academia "Three Italian Portraits of the Ottoman Sultan" | https://www.academia.edu/31775805/Three_Italian_Portraits_of_the_Ottoman_Sultan |
| S56 | Academia "Florence and the Ottoman empire in the second half of the fifteenth century" | https://www.academia.edu/44074434/Florence_and_the_Ottoman_empire_in_the_second_half_of_the_fifteenth_century |
| S57 | Wikipedia "Last Supper (Rosselli)"; Vatikan Müzeleri Sistina | https://en.wikipedia.org/wiki/Last_Supper_(Rosselli) · https://www.museivaticani.va/content/museivaticani/en/collezioni/musei/cappella-sistina/storia-cappella-sistina.html |
| S58 | Celati, "The conflict after the Pazzi conspiracy and Poliziano's *Coniurationis commentarium*" (2019) | https://www.academia.edu/42766825/_The_conflict_after_the_Pazzi_conspiracy_and_Poliziano_s_Coniurationis_commentarium_Literature_Law_and_Politics_in_Forum_Italicum_53_2_2019_pp_327_349 |
| S59 | Daniels (Almanca, *Das Interdikt in der europäischen Vormoderne*) — *Florentina Synodus* | https://dokumen.pub/das-interdikt-in-der-europischen-vormoderne-1nbsped-9783428582211-9783428182213.html |
| S60 | Weinstein, *Savonarola* (dokumen.pub kopyası; Poliziano'dan Salviati sahnesi) · *Conspiracy Literature in Early Renaissance Italy* | https://dokumen.pub/savonarola-9780300178487.html · https://dokumen.pub/conspiracy-literature-in-early-renaissance-italy-historiography-and-princely-ideology-2020947374-9780198863625-9780192608963.html |
| S61 | Simonetta 2014 "L'enigma Montesecco…" | https://www.academia.edu/11085605/_L_enigma_Montesecco_una_nuova_scoperta_sulla_congiura_dei_Pazzi_Sisto_IV_e_i_novi_tyranni_Roma_nel_Rinascimento_2014_279_298 |
| S62 | executedtoday (Bandini) | https://www.executedtoday.com/tag/mehmet-ii/ |
| S63 | Enc. machiavelliana: Medici, Lorenzo de', detto il Magnifico | https://www.treccani.it/enciclopedia/medici-lorenzo-de-detto-il-magnifico_(Enciclopedia-machiavelliana)/ |
| S64 | Bridgeman kaydı: Siena fresk "Sienalıların Floransalılara zaferi, Poggio Imperiale" (başlıkta 1480) | https://bridgemanimages.com/de/noartistknown/victory-of-the-sienese-over-the-florentines-at-the-battle-of-poggio-imperiale-1480-by-giovanni-di/nomedium/asset/757128 |
| S65 | DBI Alfonso II d'Aragona | https://www.treccani.it/enciclopedia/alfonso-ii-d-aragona-re-di-napoli_(Dizionario-Biografico)/ |
| S66 | Wikipedia "Gentile de' Becchi" (interdikt/sinod) | https://en.wikipedia.org/wiki/Gentile_de%27_Becchi |
| S67 | bible.gallery (Cosimo Rosselli; "27 Ekim 1480" Roma yolculuğu) | https://www.bible.gallery/art/cosimo/moses-and-the-tables-of-the-law/605 |
| S68 | Fleet, *European and Islamic Trade in the Early Ottoman State* (dokumen.pub kopyası; 1469 ayrıcalığı) | https://dokumen.pub/european-and-islamic-trade-in-the-early-ottoman-state-the-merchants-of-genoa-and-turkey-0521028450-9780521028455.html |

---

## 9. X — EKSİK / doğrulama kuyruğu (yeni tur ister)

**c7**
- X01 **Poliziano *Coniurationis commentarium*** (Latince; Perosa 1958 / Celati 2015 / Simonetta): sinyal cümlesi, sakristi kapısını kapatanların adları, Salviati ısırması, kayıp listesi. **Montesecco *Confessione*** metni (Excusatio) ve **Papa'nın dolaylı sözü**. **Landucci** *Diario* (Del Badia 1883; Jervis 1927) 26 Nisan–Mayıs girişleri ("Pasqua" var mı, "palle", ölü sayısı). **Filippo Strozzi** görgü tanığı metni.
- X02 Machiavelli VIII'in **sinyal cümlesi** ve "bunca nefret, bu kadar sakin yürek" yorumu (it.wikisource'ta aramak).
- X03 **Ayin saati** (hiçbir kaynakta kesin yok; "11 çanı" tek popüler).
- X04 **Maffei 2023 itirafı** içerik doğrulaması (NYU/La Nazione/Simonetta); Maffei'nin son günleri.
- X05 Renato Pazzi'nin akıbeti (asıldı mı, öldürüldü mü?); Jacopo'nun ölüm günü; Francesco'nun cesedinin 23. günü.
- X06 Duomo'nun kan döküldükten sonra yeniden kutsanması/kapanışı (aranmadı).
- X07 Giuliano ekshümasyonu (Lippi *Illacrimate sepolture*, 2007) ve kemik bulgusu.
- X08 Verrocchio/Orsini mum heykellerinin yerleştirildiği kiliseler; Botticelli freskinin yeri.
- X09 Interdikt tarihi (20/22 Haziran/4 Temmuz?), *Florentina Synodus* toplantısı (Reumont şüpheli).

**c8**
- X10 **Guicciardini *Storie fiorentine* XIII "Viaggio a Napoli"** ve Machiavelli *Istorie* VIII Napoli bölümü (Lorenzo'nun gerekçesi, Pisa mektubu, "silahsız"?). **Lorenzo *Lettere*** (Rubinstein).
- X11 **Ferrante'nin tavrı** ve Napoli sarayı (Commynes; anekdotlar: "mumya salonu" efsanesi HAFIZA/ANEKDOT).
- X12 **Roma absolüsyon töreni** (3 Aralık 1480; 15 kadırga; Pazzi tutuklularının serbestliği) — iki arama başarısız.
- X13 **Bandini'nin iadesi:** teslim tarihi/limanı, gemi, rota (14 Temmuz → 24 Aralık neden 5 ay?), Mehmed'in yazısı; Osmanlı kaynakları (Tursun Bey, Neşri, Aşıkpaşazade, Kemalpaşazade, Topkapı arşivi); Babinger.
- X14 **Floransa–Osmanlı ahidnamesi** (1455/1469) metin ve tarih; Pera temsilcisinin kimliği.
- X15 **Bertoldo madalyası:** kesin sipariş belgesi, Mehmed'e gönderildi mi, tarih (1480/1481).
- X16 **Otranto:** düşüş günü (8/11/14), ölü sayıları, Gedik Ahmed Paşa'nın rolü; Osmanlı "Pulya seferi" kaynakları.
- X17 Sistina heyeti: Ekim 1480 mi 1481 mi (sözleşme belgesi).
- X18 Poggio Imperiale günü ve komutanlar (Costanzo Sforza? Malatesta?); Colle teslim günü (14 Kasım ↔ iki aylık kuşatma).
- X19 Yetmişler Konseyi: DBI Lorenzo tam metin.
- X20 Kardinal Riario'nun tutulduğu yer; serbest bırakılma koşulu.
- X21 **Lorenzo'nun Otranto sırasındaki kendi diplomatik adımları** (elçi, mektup, Ferrante/Papa ile yazışma, 1480): kaynakta bulunamadı; Papa'nın yumuşaması ◐ (DBI Lorenzo, Lodge), ama bunun Lorenzo'nun eylemi olduğu **gösterilmedi**. DBI Lorenzo tam metin + *Lettere* (Rubinstein) gerekir.

---

## 10. Güvenilirlik özeti (yazar için)

- **En sağlam (◐):** Pazar sabahı yüksek ayin; Giuliano'nun öldürülüşü (Bandini + Francesco); Lorenzo'nun hafif yaralı sakristiye kaçışı; Nori'nin ölümü; Salviati'nin Palazzo Vecchio'da yakalanıp asılması; Francesco'nun Salviati yanında asılması; aynı gün ≈30 idam; Montesecco'nun kilisede reddi ve yerine iki papaz; 4 Mayıs itirafı; 1 Haziran aforoz; Bandini zinciri (8 Mayıs 1479 → Antonio de' Medici → 24/29 Aralık); Lorenzo'nun 6 Aralık 1479'da yola çıkıp 18 Aralık'ta Napoli'ye varışı (DBI + EI); Yetmişler Konseyi Nisan 1480; Otranto'nun Ağustos 1480'de düşüşü ve Napoli ordusunun geri çağrılışı; Bertoldo madalyası (hedge'li).
- **En zayıf:** sinyalin tam niteliği (T1); Poliziano/Montesecco/Landucci metinleri (hiç okunmadı); ayin saati; Papa'nın kişisel sözü; Jacopo'nun ölüm günü ve ceset anlatısı (tek DBI); Ridolfi'nin yara emmesi; mum heykellerin yeri; Roma'daki af töreni; Ferrante'nin kişisel tavrı; Otranto ayrıntıları; Mehmed'in neden iade ettiği.
