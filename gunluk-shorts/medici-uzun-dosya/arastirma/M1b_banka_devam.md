# M1b — BANKA VE EKONOMİ · DEVAM DOSYASI
## Şap (alum) hattı [TR-BAĞ] · şube yılları · papalık depositario · "sanata harcama" · 1494 el koyma · Padgett–Ansell · Fugger/Rothschild · Monte delle doti

**Kapsam:** `M1_banka_ekonomi.md` §10 "Eksikler" listesi ve §1 DÜZELTME/NÜANS maddeleri.
**Hazırlayan:** M1b devam ajanı · 18 Ekim 2026 · Bu bir **senaryo değil**, senaryoyu yazacak kişi için olgu dosyasıdır · git işlemi yapılmadı.
**Kaynak kodları:** M1'deki `K..` kodları o dosyanın §11'indedir. Bu dosyada **yeni** kaynaklar `KB..` koduyla §8'de listelidir.
**Numaralama:** kronoloji `b1…`, canlı ayrıntı `bD1…`, mit/tartışma `bM1…`, TR-BAĞ `bT1…`, güncelleme `U1…`.

---

## 1. Başlık notu: araçlar, sınırlar, sınıf politikası

| Araç | Ne oldu |
|---|---|
| **WebSearch** | **60 başarılı çağrı** (37 `standard`, 23 `extended`). Bunlara ek **1 çağrı** (`theguardian.com` alan adı erişilemez olduğu için) API tarafından doğrulama aşamasında reddedildi; sonuç dönmedi, ama paylaşımlı bütçeden düşülmüş olabilir (düşüldüyse toplam 61). Görev tavanı ≤60 idi; fazlası bu tek reddedilen çağrıdan ibarettir. |
| **WebFetch** | **1 deneme** (`treccani.it`, Castro maddesi) → `getaddrinfo ENOTFOUND`. Görev talimatı gereği bırakıldı; **dolaşılmadı**. |
| **Bash** | Yalnız klasör listesi ile, dosya yazıldıktan sonra yerel betiklerle (`python3 -I`) satır sayımı, numara sıralama ve çapraz-referans denetimi için kullanıldı; internete erişilmedi. |
| **Sonuç** | **● (birincil metin gerçekten okundu) bu dosyada YOK.** Birincil metinlere (Lorenzo'nun *Ricordi*'si, Machiavelli, Treccani DBI maddeleri) ait her parça yalnız **arama özetinin aktardığı kadarıyla** görüldü. |

**Hangi `allowed_domains` işe yaradı (sıralı):**
1. `treccani.it` — **en verimli kapı**: DBI/Enciclopedia dei Papi/Enciclopedia Italiana maddelerinden İtalyanca tırnaklı cümleler getirdi (Castro, Paolo II, Piero, Sassetti, T. Portinari, Canigiani, Pazzi, Benci, Volterra maddeleri, Lorenzo).
2. `ezrapoundcantos.org` — Lorenzo'nun *Ricordi*'sinin İtalyanca+İngilizce transkripsiyonundan **663.755 florin** pasajı (Canto XXI kaynakları); ayrıca el yazması/Fabroni sayı notu.
3. `dokumen.pub` — de Roover/Goldthwaite/Fleet/*Bank Failures* kitap özetleri (şube listesi, şap, Edward IV).
4. `en.wikipedia.org` — Londra tasfiyesi (1478; 51.533 fl), Pisa, Milano, Lyon; Giovanni/Cossa dizisi.
5. `cambridge.org` — Holmes'un Londra şubesi bölümü özeti; de Roover makale başlıkları (Sassetti, "Decline"); Cohn'un giriş bölümü.
6. `gutenberg.org` — Machiavelli'nin Volterra ve Lorenzo-ticaret pasajları (özet düzeyi).
7. Alan adı filtresiz `extended` sorgular — Günster & Martin (2015) şap kartel makalesi, Postrel (Reason), "Flesh Eating Stone" makalesi, TDV İA/Küre (Şebinkarahisar).
8. `archive.spectator.co.uk` (1949 kitap incelemesi; zayıf), `novelinvestor.com`/`nybooks.com` (Parks özeti ve 1474–76 aralığı).
**İşe yaramayan/denenmeyen:** `wikisource.org`, `museodeimedici.it` denenmedi; `britannica.com` yalnız tek satır verdi; `theflorentine.net` sonuç listeledi ama katkı sağlamadı.

**Sınıf ölçeği (M1 ile aynı):** **●** yok · **◐** ≥2 *bağımsız* ikincil kaynakta uyumlu (arama özeti dahil; Treccani'nin farklı yazarlı maddeleri — DBI/EdP/EI — bağımsız sayıldı, ama aynı yayıncıdan olduğu **not edildi**; Wikipedia ve kopyaları tek kaynak; yapay zekâ destekli içerik çiftlikleri sayılmadı) · **○** tek ya da doğrulanamayan · **ANEKDOT** · **HAFIZA**.
**Birebir alıntı kuralı:** Tırnak içindeki metinler arama özetinde *tırnaklı göründüğü kadarıyla* verilmiştir; orijinal sayfa açılıp kontrol edilmedi. **Türkçe çeviriler bize aittir.**

**Bu turda yakalanan özet/kaynak tuzakları (senaryocu bilmeli):**
1. Wikipedia "Tolfa": *"II. Pius dağıtımı yalnız Medici'ye verdi"*. Treccani DBI Piero + EdP Paolo II + akademik makale: sözleşme **1466**, **II. Paulus** dönemi, **Piero**. II. Pius 1464'te öldü (HAFIZA; M1 NÜANS #6 ile aynı).
2. Spectator 1949 ve Parks özeti *"Lorenzo 1466'da imzaladı"* diyor; DBI'nin Piero maddesinde "il M." Piero'dur; Lorenzo o yıl 17 yaşındaydı (doğum 1449; HAFIZA).
3. **"Usta kalfa ücreti 16,84 soldi (1391–95)" Floransa değildir:** Munro'nun tablosunda bu değer **Flaman groatı (Bruges)** cinsinden bir seridir. Bu dosyada Floransa ücreti **bulunamadı** (bkz. §5D).
4. Bir özet DBI Piero'ya *"Depositeria 1465'te verildi"* cümlesini atfetti; ikinci aramada **doğrulanamadı** (b10'da ○).
5. Foça için bir kaynak *"Cenevizliler Osmanlı döneminde de kira ile elinde tuttu"* diyordu; 1455 fethiyle çeliştiği için **hata sayıldı**.

### Hızlı özet

- **Sayılar:** Kronoloji **83 satır** (`b1…b83`), canlı ayrıntı **18**, mit/tartışma **17**, TR-BAĞ **11**, M1/M2 güncelleme satırı **40**. Sınıf dağılımı: **◐ 39**, **○ 43**, HAFIZA 1, ● 0 (kronoloji satırlarında ilk sınıfa göre).
- **En sağlam üç malzeme:** (1) **663.755 florin** = Lorenzo'nun *Ricordi*'sinde 1434–1471 *sadaka + yapı + vergi* toplamı (iki bağımsız okuma; DÜZELTME #4'ü kapatır). (2) **Şap zinciri:** Foça 1455 → Tolfa 1460–62 → **Piero'nun 1466 sözleşmesi** (II. Paulus dönemi; "9 yıl, 30. ayda fesih" ayrıntısı tek kökten, ○) → 11 Haz 1470 Napoli kartel → 1474 *depositeria* / Haz 1476 şap Pazzi'ye (birçok Treccani maddesi + Günster–Martin 2015). (3) **Depositario çelişkisi çözüldü:** 1410'lar Cossa'ya borç/bankacılık; resmî *depositario* (Bardi) **1420/1422**'den, ≈22 yıl.
- **En riskli üç iddia:** (1) **Medici'nin şaptan kazancı** — hiçbir kaynakta rakam yok; elimizdeki tek ipucu Mart 1475'te zarar (Parks özeti, ○). (2) **Tek kaynaklı canlı sahneler** — Martinus V'in teminat mitrası için aforoz tehdidi (DBI özeti, ikinci aramada doğrulanamadı); Castro'nun "Türk'e karşı zafer" sözü (kaynak belirsiz) — birebir kullanma. (3) **Londra şubesi:** kapanış 1472/1477/1478, Canigiani'nin rolü (tek direktör / hiç ortak değil) ve Edward IV borcu (ödendi ↔ temerrüt) birbirini tutmuyor; 51.533 fl tek köken.
- **Eksik kalan:** Floransa ücretleri, Palazzo Medici gerçek maliyeti, Giovanni'nin 1427 beyanı, Medici'nin şap kârı, 1494 envanteri/alacaklılar, Fugger "halefliği" için bilimsel kaynak (§7).

---

## 2. Güncelleme tablosu (M1 ve M2 satırlarının doğrulanması/çürütülmesi)

> Sütunlar: `M1 satırı (#, bölüm) | eski sınıf | yeni sınıf | not`. "Kron." = M1 §2A/2B numarası. "M2" ile başlayanlar **çapraz kontrol** (M2'deki HAFIZA-O/D kayıtlarının bu turda gelen kaynağı). **Dikkat:** M2 dosyası bu tur içinde güncellendi; buradaki M2 numaraları güncel sürüme göredir (K36 = Volterra, K37 = Imola/Pazzi, K44 = Maffei, §4.11, §5.3). M3 #35–36 (Medici kütüphanesi) ve M4 #5 (1512 dönüş) yalnız çapraz kontrol için okundu.

| M1 satırı (#, bölüm) | eski sınıf | yeni sınıf | not |
|---|---|---|---|
| **U1** · §1 DÜZELTME #4 · M6 · D36 · D54 (c4/c16, "Cosimo sanata 600 bin florin harcadı") | ○ ("doğrulanana kadar rakam yok") | **◐** (663.755 rakamı ve kapsamı) · ○ (Wikipedia'nın "600 bin, sanat ve kültür" cümlesi) | Rakamın kaynağı bulundu: Lorenzo, *Ricordi*, **1434–1471**, kalemler **limosine, muraglie, gravezze** (sadaka, yapı, vergi), "diğer harcamalar hariç". Yani **Cosimo'nun sanatı değil**, hanenin (Cosimo + Piero + Lorenzo'nun ilk yılları) harcaması ve "sanat" değil "yapı/sadaka/vergi". Wikipedia cümlesinin bu kaydın yanlış okunmuş hâli olduğu **YORUM**. Bkz. b59, b61, bD3, §5D. |
| **U2** · §1 NÜANS #7 · Kron. #31 (c2, papalık depositario) | ○ (çelişki) | **◐** (iki aşamalı çözüm) | 1410–15: Cossa'ya borç ve bankacılık (Wikipedia, Italy On This Day); **resmî** *depositario*: Roma müdürü **Bartolomeo de' Bardi**, **1420** (bir Treccani maddesi) ya da **1422** (DBI; Britannica da 1422) — Spini'nin 1420 iflasından sonra. DBI: Medici bu arada Spini'nin "gerisine düşmüştü". "Medici 1410'dan beri papalık bankacısı" cümlesi hâlâ **kurulmaz**. b27–b34, §5C. |
| **U3** · Kron. #30 (1403 depositario Spini/Alberti/Ricci) | ○ | ○ | DBI: Cossa 1403'te Bologna'yı alınca Gozzadini'yi *depositarius Camere apostolice* görevinden uzaklaştırır; Medici adı geçmez. EdP Bonifacius IX: papa en çok Floransalılara (Giovanni di Bicci, Doffo degli Spini, Alberti) başvurur. M1 ile uyumlu (b27). |
| **U4** · Kron. #32 (Konstanz; Cossa'nın indirilişi) | HAFIZA | **◐** | "1415'te tahttan indirildi": Wikipedia + Italy On This Day (b29). Konsil yılları 1414–18 hâlâ yalnız HAFIZA. |
| **U5** · Kron. #34 (1420: Giovanni yönetimi oğullara bırakır) | ○ | **◐** | DBI: "ritirato dall'effettiva direzione del banco nel 1420"; 1421 gonfaloniere; 1422 Martinus V onu Monteverde kontu yapar (b33). |
| **U6** · D16 · E13 (Cossa'nın fidyesi) | ○ (tutar yok; HAFIZA 38.000 fl) | ○ (**38.000 dukat**, tek kaynak) | Italy On This Day: "stiff ransom of 38,000 ducats". HAFIZA'mla örtüşüyor ama **birim dukat** diyor. Bir başka kaynak: fidyeyi Floransa Cumhuriyeti 1419'da ödedi. Kardinallik makamı için 10.000 dukat borç (bir özet; ○). b30, bD13–14. |
| **U7** · §1 NÜANS #6 · Kron. #55 · T3 (Foça'nın Osmanlı'ya geçişi 1455) | HAFIZA | **◐** | Wikipedia Phocaea + Byzantine Legacy + Türk yüksek lisans/doktora tezi (1275'te Cenevizlilere verildi → şap ticaretiyle öne çıktı → 1455'te Osmanlı). Fetih sonrası komutanın adı **bulunamadı**. b1–b5. |
| **U8** · Kron. #55 (Tolfa'da şap, 1461, Giovanni da Castro) | HAFIZA | **◐** (aralık 1460–1462) | Treccani DBI Castro: 1461 (Nisan'da Corneto imtiyazı); DBI/EdP Pio II ve EI Allumiere: 1462 (Mayıs); Wikipedia: 1461; Günster–Martin: Mayıs 1462 en olası; bir Corneto metni: 1460'ta yola çıkış. b7–b9. |
| **U9** · Kron. #58 · T1 (1466 papalık şap şirketi) | ◐ | ◐ (sözleşmenin kendisi: **Piero**, 1466, **II. Paulus** dönemi) · ○ (**9 yıl, Papa 30. ayda feshedebilir; Camera madencilik ve pazarlamayı iki sözleşmeye bölmüş**: tek kök, Günster–Martin ve ona dayanan yazılar) + **DÜZELTME** | Sözleşme **Piero**'ya (Gottoso) verildi. "II. Pius verdi" ve "Lorenzo imzaladı" anlatımları yanlış (bM2, bM3). b11–b12. |
| **U10** · Kron. #62 · §4D (Haz 1470 Ischia 25 yıl) | ○ | **◐** | Günster–Martin özeti: **11 Haziran 1470**, Paulus II temsilcileri ↔ Napoli Kralı Ferrante, Tolfa + Ischia/Agnano; 25 yıl. Erken fesih tartışmalı. b15. |
| **U11** · T2 (şap = haçlı fonu) | ○ | **◐** | Pius II dönemi şap gelirleri haçlı için ayrılmış (Wikipedia Maona/Tolfa; *Renaissance Papacy* özeti); EdP Paolo II: Medici *Haçlı Depositeria'sı*nı da aldı. Uygulamada Paulus II gelirleri Skanderbeg/Macaristan için çekti (○). bM4. |
| **U12** · T4 (Osmanlı şapı: Şebinkarahisar, Kütahya) | HAFIZA | ◐ ("Şapkarahisar/Karahisar-ı Şarkî" adı) · ○ (1488 ferman; Gediz/Kütahya) · **HAFIZA** ("Şebin" ← "şeb" etimolojisi) | TDV İA + Küre Ansiklopedi: Osmanlılar şap madeni nedeniyle bu Karahisar'a "Şapkarahisar/Şarkîkarahisar" der; "Şebinkarahisar" biçimi 19. yy.'da çıkar. bT3–bT4. |
| **U13** · T5 · Kron. (Volterra 1472) · M2 K36 | HAFIZA | **◐** | Ayaklanma 26 Nis 1472 (DBI Ivani); Montefeltro; teslim 16 ya da 18 Haz; yağma 18 Haz (Wikipedia + DBI). Şap anlaşmazlığı Machiavelli + DBI Capacci. b17–b20. |
| **U14** · M2 K37 (papalık bankası Pazzi'ye "1473–75") | HAFIZA-O/D | ◐ (depositeria **1474**) · ○ (şap tekeli **Haz 1476**) | EI Lorenzo: "depositeria, tolta ai Medici (1474)"; DBI G. de' Pazzi: şap "giugno del 1476". NYRB özeti: "1474–76 arasında ikisini de kaybetti". b21, b23. |
| **U15** · M2 §5.3 (Foça–Tolfa–Medici–Volterra zinciri) | HAFIZA-O/D | **◐** | Yıllar için bkz. §6 "Şap hikâyesi". M2'nin "Pius II'nin birebir cümlesi doğrulanamadı → yazılmadı" kararı **doğru**: bu turda da doğrulanmadı (bD2). |
| **U16** · M2 §4.11 (Lorenzo'nun Volterra şap ortaklığı iddiası) | ○ | ○ | DBI Capacci: Capacci ve ortakları Floransalı seçkinlerin ve "belki Lorenzo'nun" desteğiyle imtiyaz ister; Lorenzo Capacci'nin haklarını geri vermek için araya girer. **Ortaklık/hisse kanıtı yok.** EI Volterra: Lorenzo'nun etkisi "yalnız olası". |
| **U17** · Kron. #48 (Canigiani: 1446 işe girer, 1465'te müdür) | ○ | ○ (**çelişkili**) | DBI Canigiani: 1446'dan faktör, **1472'de tek direktör**, Calais'te "kambiyo bekçisi". Cambridge/Holmes özeti: de Roover'a göre **hiç ortak alınmadı**; başka bir kaynak "müdür olmadı". b44, b50. |
| **U18** · Kron. #49 · #66 (Sassetti) | ○ | **◐** | DBI: "1463'te banka genel müdürü, ölümüne (**1490**) dek ≈30 yıl"; 1462'de Cenevre ve Avignon şirket paylarında serveti. Wikipedia: 1490 → "başka kaynak 1491" kuşkusu azaldı. b47, b56. |
| **U19** · Kron. #45 (Brugge 24 Mart 1439) | ○ | **◐** | Wikipedia (EN/IT) + dokumen özeti ("Bruges 1439"). Ajan/muhabir 1416'dan. b42. |
| **U20** · Kron. #59 (Cenevre→Lyon 1466) | ○ | **◐** | HLS + dokumen özeti: 1466; bazı siteler: 1464 (Lyon panayırlarının 1463 patent mektupları sonrası). b48. |
| **U21** · §5D (Pisa, Milano, Avignon, Venedik, Basel, Ancona, Napoli, Cenevre) | HAFIZA/○ | ○–◐ | Açılış yıllarının çoğu ◐; **kapanış yılları aralıklı/çelişkili** (§5B). |
| **U22** · Kron. #65 ("Londra 1478'de kapandı", desteksizdi) | ○ | **◐** (1477–78) | Wikipedia (EN/IT): tasfiye **1478**'de bitti, toplam zarar **51.533 altın florin**; DBI T. Portinari: Londra şubesi **1477**'de kapandı; bir çalışma notu 1472. **Güvenli:** "1477–78'de tasfiye edildi". b51. |
| **U23** · Kron. #60 · §4D (Edward IV kredileri) | ○ | ○ (**çelişkili**) | Wikipedia-it: Güller Savaşı yüzünden Edward IV ödeyemedi; DBI Canigiani: kral sonradan borçlarını Canigiani'ye ödedi. İki anlatım **yan yana** verilebilir. |
| **U24** · Kron. #63 · D41 (Portinari, 1471 kararı) | ○ | ○ | DBI T. Portinari: Medici 1478–80'de Brugge'yi tasfiyeye karar verir, Portinari'yi şubeyi üstlenmeye zorlar; Lorenzo'ya göre Londra+Brugge borçları **70.000 dukat**; de Roover Portinari'yi suçlar, başkaları "durum çok karmaşıktı" der. b52. |
| **U25** · Kron. #68 (Kas 1494, saray halk tarafından yağmalanır) | ◐ | ◐ + **NÜANS** | Palazzo Medici Riccardi müzesi: Cumhuriyet saraya ve öteki Medici konutlarına **el koydu**; kalabalık görevlilerin evlerini ve San Marco yanındaki **Heykel Bahçesi/Clarice Bahçesi**ni bastı; **Signoria temsilcileri halkı sarayın üst katlarına çıkarmadı**. "Saray yağmalandı" yerine "kısmen". b65–b66. |
| **U26** · Kron. #70 (1494–95 el koyma; HAFIZA/eksik) | HAFIZA/eksik | ◐ (el koyma + kayyum) · ○ (ayrıntı) | Wikipedia: tüm mülk "sequestrated" ve kayyumlara; dokumen özeti: *Tavola* dahil; bir alacaklı kayyumlardan **15.445 fl** istedi. Envanter/alacaklı listesi **yok**. b67. |
| **U27** · Kron. #37 (Monte delle doti 1425) | ○ | **◐** | Wikipedia + Kirshner–Molho (Academia) + Avvenire. b71. |
| **U28** · D46 · M10 (Lorenzo çeyiz fonundan çekti) | ○ zayıf | ○ zayıf (**kullanma**) | Wikipedia "Medici Bank": Lorenzo Monte'yi "defrauded", **53.643 altın florin** aldı, bir kısmını geri ödedi. Rakam **başka yerde bulunamadı**; popüler siteler aynı iddiayı atıfsız tekrarlıyor. b74. |
| **U29** · M15 (Padgett & Ansell, HAFIZA) | HAFIZA | ◐ (künye, çekirdek iddia) · ○ (veri ayrıntıları) | AJS 98(6) 1993: 1259–1319; 215 seçkin aileden 92'lik ağ; "robust action". Eleştiri: Cohn (süreklilik), Kent'in hizip anlatısı, yöntem eleştirileri. bM12. |
| **U30** · M14 (Medici→Fugger→Rothschild, HAFIZA) | HAFIZA | **◐** ("kurumsal süreklilik yok") | KB44: Wikipedia Fugger ("replaced the Medici", *citation needed*); Altoviti maddesi: Strozzi, Salviati, Altoviti papalık finansında Fugger ile yarıştı; EFW: Fugger–Rothschild arasında doğrudan bağ yok. bM11. |
| **U31** · M10 ("Lorenzo kötü bankacıydı") | ○ | ◐ (çok nedenli; tek kişiye bağlama) | Machiavelli (iki çeviri özeti uyumlu), DBI Sassetti ("yapısal sorunlar, verimsiz mali örgütlenme"), de Roover (aile-merkezli yapı, ajanlar, prenslere kredi), Goldthwaite (1500 öncesi Floransa'da banka krizi yok). bM8. |
| **U32** · M2 ("modern bankacılığın atası") | ◐ | ◐ + yeni satırlar | de Roover "holding" etiketi, Goldthwaite, Parks, Ferguson: bM17 ve §6 tarihyazımı tablosu. |
| **U33** · M17 ("banka 1494'te battı") | ◐ | ◐ + ayrıntı | 1494'e gelindiğinde Brugge/Londra/Milano şubeleri zaten yoktu; Lyon ya ≈1490'da sürüldü (dokumen) ya da 1494'te rakip firmaya devredildi (Wikipedia). b57–b58. |
| **U34** · Kron. #13–14 · M4 (Bardi/Peruzzi) | ◐ | ◐ + ○ | Geri ödeme oranları **Peruzzi %37, Bardi %48** (blog özeti, ○); Floransa'nın kendi 1343 temerrüdü **≈1,8 milyon fl** iki şirketi vurdu (○); Edward III "tek neden" görüşü "basit" (Wikipedia, ◐). b75. |
| **U35** · §4B (Floransa nüfusu 1427 ≈38.000) | ◐ | ◐ + not | CLARIAH veri hikâyesi şehir için **55 bin** tahmini kullanıyor ve catasto'nun şehir nüfusunu az saydığını söylüyor (kapsam farkı olabilir; ○). |
| **U36** · E1 (usta/işçi günlük ücretleri) | Bulunamadı | **Bulunamadı** (UYARI) | "16,84 soldi" değeri **Flaman groatı** serisinden; Floransa'ya uygulanmaz. İşaretçiler §5D. |
| **U37** · E2 (Palazzo Medici maliyeti) | Bulunamadı | ○ | Wikipedia (Hatfield 1970 atfıyla): Vespasiano yapının *tek başına* **60.000 dukat**a mal olduğunu tahmin etti; özet bozuk, **doğrulanamadı**. b62. |
| **U38** · E3 (Giovanni'nin 1427 beyanı) | Bulunamadı | **Bulunamadı** | Yalnız: Parks özeti "1427'de Giovanni iki yün imalathanesi beyan eder" (○); catasto Giovanni'nin desteğiyle yürürlüğe girdi (◐). b63. |
| **U39** · E4 (Tolfa 1461, Foça 1455, Volterra 1472, Pazzi 1473) | Eksik | **Büyük ölçüde kapandı** | b1–b26. Pazzi: depositeria 1474, şap Haz 1476. |
| **U40** · E5 (şube tarihleri) | Eksik | **Kısmen kapandı** | Açılışlar ◐, kapanışlar aralıklı: §5B. Cenevre'nin kesin açılışı ve Venedik/Pisa/Avignon kapanışı **açık**. |

---

## 3. Yeni kronoloji satırları

> Sütunlar: `# | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not`. Sıra, alt başlık içinde kabaca tarihe göredir (**b26 sıra dışıdır**, tarihi b9–b10 arasına düşer). "TR" = Türk izleyiciye özel çıpa. Sınıf hücresinde birden çok sınıf varsa ilki ana olguya, sonrakiler ayrıntıya/rakama aittir (M1 ile aynı kural).

### 3A. Şap (alum) hattı: Foça → Tolfa → Volterra → Pazzi

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---:|---|---|---|---|---|---|
| b1 | c1/TR | 1275 (bir kaynak: 1267) | Bizans İmparatoru VIII. Mikhael Palaiologos, **Foça**'yı (Phocaea) ve çevredeki **şap madenlerini işletme hakkını** Cenevizli **Zaccaria** ailesine verir; aile servetini büyük ölçüde bu şaptan kurar | ◐ | KB20, KB24 | Kişi: Benedetto ya da Manuele (Manuel) Zaccaria — kaynaklar ayrışıyor. Türk tezi: "1275'te Cenevizlilere verildi, şap ticaretiyle öne çıktı." |
| b2 | c1/TR | 1346 – 26 Şub 1347 | Simone Vignoso'nun Cenevizli filosu Sakız (Chios) ve Foça'yı alır; **Giustiniani** öncülüğünde **Maona** (hisseli ortaklık) 26 Şubat 1347'de kurulur ve Foça şap madenlerini işletir | ◐ | KB21, KB22, KB23 | Madenlerin yaklaşık on yılda bir **ihale**ye çıkarıldığı söyleniyor (KB22, KB23; ○). Maona = Cenova'nın sömürge işletme ortaklığı. |
| b3 | c1/TR | 1445 | Maona'nın Flaman limanlarına (Sluys, Bruges) **51.800 kantar ≈ 2.500 ton** şap sevk ettiği yazılır | ○ | KB21 | KB23'teki 1452 akti (yılda ≈15.800 kantar) ile **bağdaşmıyor**; aynı rakamın yazım hatası ya da çok yıllık toplam olabilir → kullanma (§5A). |
| b4 | TR | 1452 | Cenevizli bir noter belgesi, Foça'nın yıllık şap üretimini ≈**15.800 kantar** olarak verir | ○ | KB23 | Fleet'in kitabı (dokumen.pub özeti). |
| b5 | TR | 1453 → 1455 | **Foça (Eski/Yeni Foça) Osmanlı eline geçer (1455)**; Cenevizlilerin Foça şap kaynağı Osmanlı'ya geçer | ◐ | KB20, KB24 | M1 T3 HAFIZA → ◐. Bir seyahat sitesi (kupi.com) fethi Mehmed II'ye atfeder (○); komutan adı **bulunamadı** (HAFIZA'daki "Hamza Bey" kullanılmaz). |
| b6 | TR | 1453 sonrası | Avrupa'nın şapı büyük ölçüde Osmanlı elindeki Anadolu madenlerinden gelir; Batılı alıcılar Tolfa'ya yönelir | ○ | KB05, KB06 | Tolfa öncesi tek tedarik "Doğu'dan, Osmanlı denetimindeki kaynaklardan, Venedik üzerinden" (KB03; ○). Günster–Martin: Tolfa Osmanlı'yı Avrupa'dan elde ettiği şap gelirinden yoksun bıraktı (◐ KB03+KB04). |
| b7 | c3/TR | 1460–1462 (en çok 1461; "Mayıs 1462" en olası) | **Giovanni di Castro** (jurist Paolo di Castro ile Cornetolu Piera Cerrini'nin oğlu) **Tolfa** dağlarında (Papalık Devleti, Civitavecchia yakını) zengin şap yatağı bulur | ◐ | KB01 (1461), KB02 (1462), KB03 (1461), KB04 (Mayıs 1462), KB07 (1462; başka bir metin 1460) | Keşif anlatılarının çoğu **II. Pius'un kendi anılarına** dayanır (KB21 özeti); *Commentaries* öz-propaganda olarak okunur (KB49). |
| b8 | c3/TR | Nisan–Ağu 1461 (DBI bağlamı) | Castro, Corneto Komünü'nden **25 yıllık** imtiyaz alır (Nisan); Camera Temmuzda onaylar; Ağustosta II. Pius bulla ile hakkı **üretilen kantar başına 2 dukat** karşılığında tanır | ○ | KB01 | DBI Pio II maddesi 1462 dediği için yıl bağlamı b7'ye göre belirsiz. |
| b9 | c3/TR | 1462 | Castro iki kuria mensubuyla maden/ticaret **şirketi** kurar. II. Pius başta **heyecan göstermez**; Cenevizli bir uzman cevheri inceleyince ikna olur | ○ | KB01, KB02 | ANEKDOT niteliği: özet iki maddeyi ayırmadı. Bkz. bD2. |
| b10 | c3 | 1465 | Papalık *Depositeria*'sı ("Medici'lerin geçmişte neredeyse kesintisiz elinde tuttuğu") **Venedikli papa II. Paulus (Barbo)** tarafından 1465'te Medici'ye verilir | ○ | KB09 (özet), KB08 | İkinci aramada **doğrulanamadı**. 1455'te Callistus III'ün Martelli'yi görevden almasıyla (M1 #50) bir boşluğa işaret eder. Kullanma. |
| b11 | c3/TR | 1466 | **Piero de' Medici (Gottoso)**, Apostolik Camera'dan "yakın zamanda bulunmuş Tolfa şap madenlerinin işletilmesine katılmak ve bu değerli mineralin pazarlanması için" sözleşme alır | ◐ | KB09 (İt. alıntı), KB04, KB06 | **DÜZELTME:** sözleşme II. Pius dönemi değil; "Lorenzo imzaladı" anlatımı da yanlış (bM2, bM3). DBI cümlesi *"In compenso"* ile başlıyor — neyin karşılığı olduğu özetten **anlaşılmıyor**. EdP Paolo II: Tolfa yönetimi Medici Bankası'na verildi, *Haçlı Depositeria'sı* da (○). |
| b12 | c3/TR | 1466 | Pazarlama sözleşmesinin biçimi: **9 yıl**; Papa **30. aydan sonra** feshedebilir; Camera madencilik ve pazarlamayı iki ayrı sözleşmeye bölmüştür; Medici'ye bağlı bir grup alır | ○ (tek kök: Günster–Martin ve ona dayanan Reason/akademik özetler; sözleşmenin varlığı b11'de ◐) | KB04, KB05, KB06 | Medici'nin birim kazancı: **kantar başına 1 altın dukat** (KB06; ○, dönemi belirsiz). Camera payı: 2 dukat/kantar + ek kârın 2/3'ü (M1 #58 ◐). Fiyat, Camera'ya ödenen birim bedelin altına düşebiliyordu; Camera sonradan **daha azını kabul etti** (KB06; ○). |
| b13 | c3/TR | 1468 | Papalık elçisi Bruges'te **Cesur Charles** ile anlaşır: Dük papalık dışı şapı dışarıda tutar, karşılığında kâr payı; **Flaman dokumacılar öfkelenir**, anlaşma çöker, dük geri adım atar | ○ | KB05, KB06 | Başka özet: "1468'de on iki yıllık tekel Aşağı Ülkeler pazarı içindi." Süre/yıl tutarsız. |
| b14 | c3/TR | 1469 | Apostolik Camera Tolfa şehrini **17.300 altın dukaya** satın alır (Ferrante, Orsini desteğiyle teslimi 1469'a dek geciktirmişti); II. Paulus, krallıkla ilişkiyi bozmamak için Tolfa ve Agnano'nun **ortak işletilmesine** razı olur | ◐ | KB08 (EdP + DBI), KB02 (EI: ≈17.000 scudo) | Tutar 17.300 (EdP, DBI) / ≈17.000 (EI). |
| b15 | c9/TR | 11 Haz 1470 | Papalık (Paulus II) temsilcileri ile Napoli Kralı **Ferrante** arasında **şap kartel** anlaşması (Tolfa + Ischia/Agnano), **25 yıl**; satış/üretim yarı yarıya | ◐ (tarih/taraflar) · ○ (hükümler) | KB04, KB05, KB06, KB08 (EdP Paolo II: Napoli ile ortak şirket), K110, K111 (M1: "Haz 1470, 25 yıl") | Erken feshi tartışmalı: ≈1472 (soru işaretli) ↔ Mignanti'ye göre tam süre. M1 #62 ○ → ◐. |
| b16 | c9/TR | 1471 | Medici sözleşmesi **dört yıllık yenilenebilir** süreye indirilir | ○ | KB06 | Tek kaynak; aynı kaynak "1472'de Sixtus IV iptal etti" der — DBI Pazzi (Haz 1476) ile çelişir (b23). |
| b17 | c6 | erken 1470'ler | Volterra yurttaşları şap yatağını bulur, **Floransalı ortakları kâr paylaşımıyla** çağırır; Volterra konseyi **kamu arazisindeki servetin özel kişilere gitmemesi** gerektiğini savunur; Floransa danışmanları şirketten yana | ◐ | KB15, KB16 | DBI Capacci: Benuccio Capacci ve ortakları, Floransalı seçkinlerin ve "belki Lorenzo'nun" desteğiyle Volterra'da şap ocağı imtiyazı ister; özet yerel tüccarların çoğunun dışlandığını söylüyor (kimin dışladığı özetten net değil); Lorenzo Capacci'nin haklarını geri vermek için araya girer; grup yeniden kovulur. Spectator 1949 "Volterra'da keşif 1458" der (KB18; güvenilmez). |
| b18 | c6 | 26 Nis 1472 | Volterra'da **ayaklanma** | ○ | KB16 | Tek DBI girişi (Ivani). |
| b19 | c6 | 16–18 Haz 1472 | Federico da Montefeltro komutasında Floransa kuvvetleri Volterra'yı kuşatır; şehir teslim olur (16 ya da 18 Haz) ve **18 Haziran'da yağmalanır** | ◐ | KB16 (DBI Ivani: 18 Haz, ≈1 ay kuşatma), KB17 (Wikipedia: 25 gün kuşatma, 16 Haz teslim, 18 Haz yağma) | Lorenzo'nun payı: EI "yalnız olası"; 19. yy. bir görüş yağmayı savunma için tutulan **paralı askerlerin** başlattığını söyler (KB15 özeti; ○). DBI Maffei: Raffaele Maffei ve Fiumi çatışmayı Floransa'nın **şap tekeli** hedefine bağlar. **Çapraz ipucu (YORUM):** Pazzi suikastında Duomo'da Lorenzo'ya saldıracak iki papazdan biri **Antonio Maffei** Volterralıydı (M2 K44); Volterra 1472 ile Pazzi 1478 arasında bağ kurmak kaynak gerektirir, bu turda aranmadı. Mizah kapalı. |
| b20 | c6 | 1472–1474 | Floransa Volterra'da **kale** (Rocca Nuova) yapar; varlıklı ailelerin göçü ve mallara el koyma | ○ | KB17 | Yıl: 1472–74 / 1474 (Wikipedia ve seyahat sitesi özetleri; tek kök sayıldı). |
| b21 | c7 | Kas 1473 – 1474 | **Imola krizi:** Sixtus IV Imola'yı yeğeni için ister; Medici bankasından avans beklenir (**40.000 dukat**, DBI Lorenzo), Lorenzo reddeder; para büyük ölçüde **Pazzi**'den gelir. Sixtus **1474'te** Lorenzo ve Giuliano'yu papalık *depositario*'luktan alır; görev Pazzi'ye | ◐ (depositeria 1474) · ○ (tutar) | KB12, KB13, KB14, KB19, KB10 (DBI/EdP Sisto IV: Imola anlaşmazlığı Medici'yi papalık bankerliğinden ve Tolfa şap appaltosundan etti, Pazzi'ye verildi; tarih vermiyor) | Tutar 30.000 (Enciclopedia Machiavelliana) – 40.000 (DBI); Imola kimin için: yeğen Girolamo Riario (EI) ya da Kardinal Pietro Riario (Machiavelliana: Milano dükü Pietro'ya 30.000 dukata verdi; bulla Kas 1473'te Girolamo adına çıktı). M2'deki "1473" → **1474**. |
| b22 | c9 | Mart 1475 | Banka **şapta zarar** eder. Sebepler (Parks özeti): aforoz tehditlerine rağmen alıcılar daha ucuz **Türk şapına** geçti; Medici'nin fazla şapı fiyatları düşürdü; yabancı alıcılar dernek kurup pazarlıkta fiyatı indirdi; Volterra yatağı **kalitesiz** çıktı | ○ | KB19 (+ KB05: "Türk şapı Avrupa'ya girmeye devam etti" ◐) | Zarar **rakamı yok**. |
| b23 | c7 | Haz 1476 | Sixtus IV **şap tekelini** Medici bankasından **Pazzi bankasına** aktarır | ○ | KB11 (İt. alıntı), KB19 (NYRB: 1474–76), KB10 (Sisto IV maddeleri: şap appaltosu Pazzi'ye) | M2 K37 ve §5.3'teki "şap imtiyazının Pazzi'ye geçişi" (HAFIZA-D) bu satırla ○ düzeyine çıktı; "Pazzi'nin kini ekonomik bir kaynağa da dayanır" yorumu böylece kaynak kazandı (yorum olarak kalır). |
| b24 | c9 | 1490'lar | Medici'nin gerilemesiyle Tolfa işletmesi "pahalı yatırım" olur; Medici kira sözleşmesini bir sonraki bitişte bırakır; kira **Spannocchi**'ye, sonra **Chigi**'ye geçer | ○ | KB26, KB01 | Chigi: 1497 (DBI Castro: VI. Alexander Tolfa'yı Agostino Chigi'ye kiralar) ↔ 1501 (Cibona metni). |
| b25 | TR | 1488 | **II. Bayezid fermanı:** şap kaçakçılığına karşı (Gediz ve Şebinkarahisar şapı) | ○ | KB22 | Tek makale (özet). |
| b26 | c3/TR | Ağu 1464 (b9 ile b10 arasına denk gelir; sıra dışı konuldu) | **Cosimo (1 Ağu) ve II. Pius ölür**; yeni papa **II. Paulus (Pietro Barbo)** olur. Medici'nin Tolfa sözleşmesi bu pontifikaya aittir | HAFIZA (Pius'un ölümü ve Barbo'nun seçilişi) · ◐ (Cosimo'nun ölümü, M1 #56) | M1 NÜANS #6 (K110, K111) | Bu turda araçla doğrulanmadı; DÜZELTME bM2/bM3 buna dayanır. |

### 3B. Papalık *depositario* ve Cossa dizisi

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---:|---|---|---|---|---|---|
| b27 | c2 | 1403 | Cossa Bologna'yı papalığa geri alınca **Gozzadini**'yi *depositarius Camere apostolice* görevinden uzaklaştırır; Medici bu görevde adı geçmez | ○ | KB34 (DBI Giovanni di Bicci) | M1 #30 ile uyumlu. EdP Bonifacius IX: papa en çok Floransalılara (Giovanni di Bicci, Spini, Alberti) başvurur. |
| b28 | c2 | 1410 | Giovanni, Cossa'nın **kardinallik makamını "satın alması"** için borç verir; Cossa papa olunca Medici'yi papalık mali işlerinin başı yapar (Wikipedia'nın anlatımı) | ◐ (borç) · ○ ("başlık") | KB35 | Kardinallik parası: 10.000 dukat (bir özet; ○). DBI'de böyle bir "başlık" yok: Spini üstün (b31). |
| b29 | c2 | 1415 | Konstanz Konsili Cossa'yı tahttan indirir; Medici diğer bankalarla **rekabet etmek zorunda** kalır | ◐ | KB35 | M1 #32 HAFIZA → ◐. |
| b30 | c2 | 1418–1419 | Cossa Alman tutsaklığından Medici'nin fidyesiyle çıkar: **38.000 dukat** (tek kaynak); başka bir kaynak fidyeyi Floransa Cumhuriyeti'nin 1419'da ödediğini söyler. Cossa ölünce (22 Ara 1419, M1 #33) Giovanni anıt mezarını finanse eder | ○ | KB35 | Birim dukat; M1 HAFIZA 38.000 fl ile örtüşür. Mezar: M1 #36 (M1 S3: mezarı kimin ödediği belirsizdi; bu popüler site Medici'yi gösteriyor, ○). |
| b31 | c2 | 1420 | **Spini bankası batar;** Medici papalık bankacılığında önceliği yeniden kazanır | ◐ | KB34 (DBI), KB35 (Wikipedia) | DBI: Medici bir ara Spini'nin "gerisine düşmüştü" → 1410'lardaki üstünlük Konstanz sonrası kayboldu. |
| b32 | c2 | 1420 ya da 1422 | Roma müdürü **Bartolomeo de' Bardi**, Martinus V döneminde Curia'nın *depositario*'su olur; Medici görevi ≈**22 yıl** elinde tutar | ◐ | KB34 (DBI: 1422; ikinci Treccani maddesi: 1420), KB35 (Britannica: Giovanni 1422'de papalık bankacısı) | 22 yılın bitiş yılı verilmedi. |
| b33 | c2 | 1420–1422 | Giovanni bankanın fiilî yönetiminden çekilir (Cosimo ve Lorenzo'ya bırakır); **1421 gonfaloniere**; **1422** Martinus V onu **Monteverde kontu** yapar | ◐ (1420) · ○ (Monteverde) | KB34, K48 | |
| b34 | c2 | Martinus V döneminde, Cossa'nın ölümünden sonra | Martinus V, XXIII. Johannes'in bir borca **teminat bırakılmış mitrasını** geri almak için Giovanni Bicci'yi **aforozla tehdit** eder | ○ ANEKDOT | KB34 (DBI) | İkinci aramada doğrulanamadı; DBI maddesinde kontrol et. Bkz. bD1. |

### 3C. Şubeler (açılış–kapanış; ayrıntı ve çelişkiler için §5B)

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---:|---|---|---|---|---|---|
| b35 | c2 | 1385 | Vieri de' Medici'nin ortaklığı Venedik'te şube açmıştı | ○ | KB28 (DBI Vieri) | Banka öncesi. |
| b36 | c2 | 1402 | **Venedik ve Napoli** şubelerinin açılışı | ◐ | KB28, K58, K01 | Venedik 25 Mart 1402 (M1 #28). |
| b37 | c2 | 1409 | Giovanni Benci Roma şubesinde çalışmaya başlar (sonra Cenevre müdürü) | ○ | KB28 | |
| b38 | c3 | 1416 / 1425–26 | **Napoli** şubesi kapanır: 1416 (Treccani; temsilci 1426'ya dek) ↔ 1425 (Wikipedia-it); yerine **Cenevre ve Gaeta** | ○ | KB28, KB27 | Napoli sonradan Roma'ya bağlı alt şube, Tornabuoni denetiminde (dokumen özeti; ○). |
| b39 | c3 | 1420'ler (1426; 1429'da Benci tek müdür) | **Cenevre** şubesi | ○ | KB28 (1429), K115 (1426) | Kesin açılış yılı **bilinmiyor** (1424 HAFIZA'sı doğrulanmadı). |
| b40 | c3 | 1433 | **Basel** şubesi: Giovanni Benci, Konsil sırasında açmakla görevlendirilir | ◐ | KB28, K115 | Kapanış bilinmiyor. |
| b41 | c3 | 1436 | **Ancona** şubesi | ○ | K115 | |
| b42 | c3 | 24 Mart 1439 | **Brugge** resmî şube (ajan/muhabir 1416'dan) | ◐ | K01, KB27, K115 | M1 #45 ○ → ◐. |
| b43 | c3 | 1442 | **Pisa** şubesi ("Cosimo 1442'ye kadar bekledi") | ◐ | K115 (iki ayrı kitap özeti), K01 (yalnız kapanış) | Kapanış: **1443** (Wikipedia: ortak ölünce) ↔ **1489** (dokumen, "çoğu kaynak"). |
| b44 | c3 | 1446 | **Avignon**: sınırlı sorumlu ortaklık; iki yıl içinde tam ortaklığa dönüşür. **Londra**: Gherardo Canigiani 1446'dan faktör | ◐ | KB27, KB31, K115 | |
| b45 | c3 | 1452 (ya da erken 1453) | **Milano** şubesi, Francesco Sforza'nın talebiyle; **Pigello Portinari** açmakla görevlendirilir | ◐ | KB27, KB30, K115 | |
| b46 | c3 | 1462 | Sassetti'nin serveti **Cenevre ve Avignon** şirketlerindeki sermaye paylarında | ○ | KB29 | M1 #61 (gizli defter 1462–72) ile uyumlu. |
| b47 | c3 | 1463 | **Sassetti** Medici bankasının **genel müdürü** olur; **1490**'daki ölümüne dek ≈30 yıl | ◐ | KB29 (DBI), K71 | M1 #49/#66. |
| b48 | c3 | 1464–1466 | **Cenevre → Lyon**: 1466 (HLS, dokumen) ↔ 1464 (bazı siteler) | ◐ | K54, K115, KB32 | **Lionetto de' Rossi** Lyon müdürü; şube yolsuzluk yüzünden neredeyse batar, Sassetti kurtarır (Wikipedia; ○). |
| b49 | c3 | 1465 | Londra şubesi yeniden düzenlenir | ○ | K01 | |
| b50 | c9 | 1472 | Canigiani Londra'da **tek direktör** (DBI) | ○ (çelişkili) | KB31 ↔ K72 | Holmes özeti: de Roover'a göre **hiç ortak alınmadı**. DBI: Edward IV'e kredi vermeyi sürdürüp Calais'te "kambiyo bekçisi" oldu; kral sonradan borçlarını Canigiani'ye ödedi ↔ Wikipedia-it: Edward IV temerrüde düştü (U23). |
| b51 | c9 | 1472 / 1477 / 1478 | **Londra** kapanış/tasfiye: 1472 (bir çalışma notu) · **1477** (DBI T. Portinari; dokumen) · **1478** (Wikipedia: tasfiye bitti; **51.533 altın florin** zarar) | ◐ (1477–78) | KB30, K01, KB27, KB32 | Sebep: Güller Savaşı, Edward IV. Zarar rakamı tek köken (Wikipedia; de Roover'a dayanıyor olabilir) → ○. |
| b52 | c9 | 1478–1480 | Medici **Brugge**'yi tasfiyeye karar verir; **Portinari**'yi şubeyi üstlenmeye zorlar. Kapanış: 1480 ↔ 1481 | ◐ | KB30, K115 | Lorenzo'ya göre Londra+Brugge borçları **70.000 dukat**; Wikipedia >70.000 florin. Wikipedia (Sassetti): Sassetti, ortak **Angelo Tani**'nin karşı çıktığı Portinari projelerini onayladı (tek kaynak; ○; M1 #63 ile uyumlu). |
| b53 | c9 | 1478 / 1479 | **Milano** kapanır: 1478 (dokumen) ↔ **1479** (DBI T. Portinari); sebep: dükalara verilen krediler geri alınamadı | ◐ | KB30, K115 | |
| b54 | c9 | 1479 / 1480 | **Avignon** ("aile adını taşımayan şirket") kapanır | ○ | K115 | |
| b55 | c9 | 1481 | **Venedik** (tasfiye) | ○ | K115 | Tek özet; HAFIZA'daki "1470'ler sonu–80'ler" ile uyumlu. |
| b56 | c9 | 1490 | Sassetti ölür | ◐ | KB29, K71 | M1 "1491" şüphesi azaldı. |
| b57 | c9 | ≈1490 ya da 1494 | **Lyon** sonu: ≈1490'da Fransa–Floransa gerginliği yüzünden şube **Fransa'dan sürüldü** (dokumen) ↔ **1494'te rakip bir firmaya devredildi** (Wikipedia) | ○ (çelişkili) | K115, K01 | DBI Tornabuoni: Lyon'la ilgili bankayı kurtarmak için kurulan bir şirketten söz eder (ayrıntı yok). |
| b58 | c10 | 1494 | 1494'e gelindiğinde **Brugge, Londra, Milano şubeleri yoktu**; Lyon hâlâ anılıyor | ○ | K01 | Roma'nın 1494'teki durumu bu turda doğrulanmadı (HAFIZA). |

### 3D. Harcama, servet, catasto

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---:|---|---|---|---|---|---|
| b59 | c4/c16 | 1434–1471 (*Ricordi* ≈1472; yıl doğrulanmadı) | **Lorenzo il Magnifico**, *Ricordi*'sinde 1434–1471 arası hanenin **sadaka, yapı ve vergi** harcamasını **663.755 florin** olarak yazar ("diğer harcamalar hariç"); DBI baskısı **663.775½** | ◐ | KB36 (Cantos Project), KB13 (DBI) | El yazmasında sayının ardından bir **kesir işareti** var; Fabroni 663755 basar. Lorenzo toplamı "inanılmaz" bulur. DBI yorumu: Cosimo'nun prestij politikası ve buna bağlı yapı faaliyeti "muazzam meblağları yutmuştu". |
| b60 | c3 | 1434–1471 | Aynı *Ricordi*, Cosimo'nun defterlerinden **235.137 "scudi di suggello"**lık bir mirastan söz eder: Cosimo bunu **Pierfrancesco** ve oğulları reşit olana dek yönetmiştir | ○ | KB36 | Özet düzeyi; Lorenzo–Pierfrancesco miras davasına (1485) giden bağ için not. |
| b61 | c4/c16 | (Wikipedia'nın "600 bin") | Wikipedia: Cosimo "sanat ve kültüre 600.000+ altın florin (≈500 milyon $)" harcadı | ○ | K89 (M1) | b59'un yanlış okunmuş hâli olabilir (**YORUM**). |
| b62 | c4 | 1444–1460 (1484) | **Palazzo Medici** yapı maliyeti: Vespasiano'nun tahmini **60.000 dukat** (yalnız yapı) | ○ | KB37 | Wikipedia/Hatfield 1970 atfı; özet bozuk. Vespasiano tahmini **retorik** olabilir. |
| b63 | c2 | 1427 | Catasto: Parks özetine göre Giovanni **iki yün imalathanesi** beyan eder; toplam beyan edilen servet ≈**10.170.000 fl** | ○ | KB19, K42 | Giovanni'nin kendi toplam beyanı **bulunamadı**. Catasto Giovanni'nin desteğiyle yürürlüğe girdi (M1 #38). |

### 3E. 1494: sürgün, el koyma, kütüphane

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---:|---|---|---|---|---|---|
| b64 | c10 | 8–9 Kas 1494 | Piero kaçar; Signoria Medici'yi **sürgün** eder ve geri dönemeyeceklerini ilan eder | ◐ | KB40, K98 | Tarih: 8 Kas (storiadifirenze) ↔ 9 Kas (bir blog). |
| b65 | c10 | Kas 1494 | Cumhuriyet **Palazzo Medici'ye ve öteki Medici konutlarına resmen el koyar**; Donatello'nun **David ve Judith**'i ile iki **Marsyas** Palazzo Vecchio'ya taşınır | ◐ | KB39, KB40 | Beck: saray Fransız kralını ağırlamak için hazırlandı; Medici serveti müsadere edildi (○). |
| b66 | c10 | Kas 1494 | Kalabalık görevlilerin evlerini ve bazı Medici mekânlarını (**Heykel Bahçesi**, San Marco yakınındaki **Clarice Bahçesi**) basar; Signoria temsilcileri halkı **sarayın üst katlarına çıkarmaz** | ◐ (yağma) · ○ (üst kat ayrıntısı, tek müze sitesi) | KB39 | M1 #68'e **NÜANS** (U25). |
| b67 | c10 | 1494–95 | Medici'nin tüm mülkü (iş yatırımları, gayrimenkul, ***Tavola***) **kayyumlara** (receivers) verilir; bir alacaklı kayyumlardan **15.445 florin** talep eder | ◐ (el koyma) · ○ (15.445) | K01, K115 | Envanter/alacaklı listesi **bulunamadı**. |
| b68 | c10 | 1494 sonrası | Ödül: Piero'nun başına **4.000**, kardinal Giovanni'nin başına **2.000 florin** (Beck); başka bir site: asileri sağ getirene **5.000 dukat**; Piero için Floransa'dan ≥100 mil uzağa sürgün ("bir ay sonra" deniyor, neye göre olduğu özetten net değil) ve 25 Eylül 1495'te başına ayrı ödül | ○ | KB40 | Çelişkili. |
| b69 | c10/c11 | 1495 → 1508/1513 | Medici **kütüphanesi** Signoria tarafından **San Marco Dominiklerine satılır**; Giovanni (sonradan X. Leo) geri satın alır | ◐ | KB41, M3 #35–36 (M3'ün kendi K26 kodu: 1494 el koyma → San Marco; **1508** kardinal Giovanni geri alır, ◐) | BML sitesinin özeti "1513'te papa seçilen Giovanni…" diye okunabiliyor; M3'ün 1508'i ile çelişir ya da özet yanlış okunmuş olabilir. Bir M3 kaynağı: Vatikan parasıyla geri alındı. Satış bedeli bu turda bulunamadı. |
| b70 | c10 | 1512 | Medici Via Larga sarayına geri döner | ◐ | KB39, M4 #5 (Eylül 1512: Giuliano ve Kardinal Giovanni İspanyol desteğiyle Floransa'ya döner, ◐) | Gün çelişkisi M4'te. |

### 3F. Tarihyazımı, kurumlar, tartışma

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---:|---|---|---|---|---|---|
| b71 | c16 | 1425 | **Monte delle doti** kurulur (kısmen savaşlarla boşalmış hazineye para sokmak için) | ◐ | K97, KB46 | M1 #37 ○ → ◐. |
| b72 | c16 | 1440'lar–1450'ler | Fon çeyizleri vadesinde ödemez (1442 sonuna dek >1.800 mevduattan **373**'ü ödenmiş); 1450'lerden taksit; bir kaynağa göre 1425–1569 arası ≈**30.000 kız** kayıtlı | ○ | KB46 | Kirshner–Molho çizgisi; ikincil özet. |
| b73 | c16 | 1494 sonrası | Monte delle doti yükümlülüklerini karşılayamaz hale gelir | ○ | KB46 | Tek özet. |
| b74 | c9/c16 | (yıl yok) | Wikipedia: Lorenzo Monte delle doti'den **53.643 florin** aldı, bir kısmını iade etti | ○ (zayıf) | K01 | İkinci aramada başka yerde **bulunamadı**. |
| b75 | c16 | 1342–1346 | **Bardi/Peruzzi:** alacaklılara geri ödeme **Peruzzi %37, Bardi %48**; Floransa'nın kendi 1343 temerrüdü (≈1,8 milyon fl) iki şirketi de vurdu; "yalnız Edward III" görüşü "basit" | ○ (oranlar) · ◐ ("basit") | KB47 | Villani rakamları (900.000/600.000) için bkz. M1 #14. |
| b76 | c16 | 1943?–1946? | de Roover'ın **Sassetti** ("Francesco Sassetti and the Downfall of the Medici Banking House", BHR) ve **"The Decline of the Medici Bank"** (JEH) makaleleri | ◐ (başlıklar) · HAFIZA (yıl/yazar) | KB33 | |
| b77 | c16 | 1963 | de Roover'ın kitabına Cambridge incelemesi: de Roover **Machiavelli ve Guicciardini**'nin yargısını aktarır — Lorenzo'nun ticarette şansı yoktu, işi temsilcilerine bıraktı | ○ | KB33 | |
| b78 | c16 | 1978 | **Dale Kent**, *The Rise of the Medici: Faction in Florence, 1426–1434* — hizip/patronaj anlatısı; Padgett–Ansell'in veri kaynağı | ◐ | KB42, KB43 | |
| b79 | c16 | 1993 | **Padgett & Ansell**, AJS 98(6): 1259–1319 | ◐ | KB42 | |
| b80 | c16 | 1996 (HAFIZA) | **George Holmes**, "Lorenzo de' Medici's London Branch" (*Progress and Problems in Medieval England*, bölüm 13) | ○ | K72 | Yazar adı Cambridge sayfasının arama özetinden; yayın yılı (1996) HAFIZA. Belge dayanağı: *Mediceo avanti il Principato* + Public Record Office. |
| b81 | c16 | 1999 | **Samuel Cohn**, *Creating the Florentine State* girişi: Medici'nin yükselişi "değişimden çok süreklilik" olarak görülüyor | ○ | KB43 | |
| b82 | c16 | 2009 | **Goldthwaite**, *The Economy of Renaissance Florence*: 1500 öncesi Floransa'da banka krizi yok | ○ | K124 | Dokumen özeti; yalnız özet düzeyi. |
| b83 | c16 | 2015 | **Günster & Martin**, "A Holy Alliance: Collusion in the Renaissance Europe Alum Market", *Review of Industrial Organization* 47(1): 1–23 | ◐ | KB04 | |

---

## 4. Canlı ayrıntılar

> Sütunlar: `# | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı (orijinal dil + Türkçe çeviri; çeviri bize aittir)`.
> **Dürüst not:** Bu paketin ağırlığı sayısal/yapısal; duyusal ayrıntı azdır. Aşağıdakiler *arama özetinde tırnaklı göründüğü kadarıyla* alınmıştır; orijinal sayfalar açılmadı. "—" = doğrulanmış birebir cümle yok.

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| bD1 | c2 | **Teminat mitrası.** Cossa öldükten sonra Martinus V, XXIII. Johannes'in bir borç karşılığı teminat bıraktığı **mitrayı** geri almak için Giovanni Bicci'yi **aforozla tehdit eder**. | Treccani DBI, Giovanni di Bicci maddesi (Terenzi) — olaydan ≈500 yıl sonra yazılmış sözlük maddesi; dayandığı belge özette yok | ○ **ANEKDOT** (tek kaynak; ikinci aramada doğrulanamadı) | IT (özet tırnağı): "Dopo la morte del Cossa M. minacciò di scomunicare Giovanni Bicci per recuperare una mitria di Giovanni XXIII data in garanzia per un prestito di denari." → "Cossa'nın ölümünden sonra M[artinus], bir borca karşılık teminat olarak verilmiş XXIII. Johannes'in mitrasını geri almak için Giovanni Bicci'yi aforoz etmekle tehdit etti." |
| bD2 | c3/TR | **Castro'nun taşı.** Castro'nun Tolfa'da bulduğu kaya, İstanbul'da şap yapımında kullanılana benzer görünür; papaya "Türk'e karşı bir zafer" müjdelediği anlatılır (derleme anlatımları). DBI'ye göre ise II. Pius başta heyecan göstermez, Cenevizli bir uzman cevheri görene dek (b9). | Arama özetlerinde adı verilmeyen derleme/eski anlatımlar ve Wikipedia "Tolfa" türevleri; kaynak büyük olasılıkla II. Pius'un *Commentarii*'si (**HAFIZA**; keşif anlatılarının çoğunun II. Pius'un anılarına dayandığı KB21 özetinde var) | ○ **ANEKDOT** | EN (özet tırnağı; kaynak belirsiz): "I announce to you a victory over the Turk" → "Size Türk'e karşı bir zafer müjdeliyorum." **Birebir söyleme**; "…diye anlatılır" kipi. *Commentaries* öz-propaganda olarak okunur (KB49). |
| bD3 | c4/c9 | **Lorenzo defterlere bakar.** Lorenzo, 1434–1471 harcamalarını küçük bir **kuarto defterde** bulur; yazılı toplamlar ona "inanılmaz" gelir: sadaka, yapı, vergi — diğerleri hariç **663.755 florin**. | Lorenzo de' Medici, *Ricordi* (1471 sonrası; Lorenzo ≈23 yaşında, doğum 1449 HAFIZA; yazım yılı doğrulanmadı) — Cantos Project transkripsiyonu; Treccani DBI Lorenzo | ◐ | IT (DBI): "ascende a fiorini 663.775 e ½, tra limosine, muraglie e gravezze" → "[toplam] 663.775 buçuk florine çıkıyor; sadakalar, yapılar ve vergiler arasında." · EN (Cantos Project; özet aktarımı): "The sums written down are incredible. They amount to 663,755 florins for alms, buildings, and taxes, let alone other expenses." → "Yazılan toplamlar inanılmaz. Diğer harcamaları saymasak bile sadaka, yapı ve vergiye 663.755 florin tutuyor." · DBI yorumu: "La politica di prestigio di Cosimo e l'attività edilizia a essa connessa avevano inghiottito somme enormi" → "Cosimo'nun prestij politikası ve buna bağlı yapı faaliyeti muazzam meblağları yutmuştu." |
| bD4 | c9 | **Machiavelli'nin Lorenzo hükmü.** Lorenzo ticarette talihsizdi; ajanları işleri **prens gibi** yürüttü; servetin büyük kısmı eridi; ticareti bırakıp toprağa yöneldi (Prato, Pisa, Val di Pesa). | Machiavelli, *Istorie fiorentine* VIII (≈1520–25; Medici siparişi) — Gutenberg #2464 ve Fordham çevirilerinin özetleri | ◐ (iki çeviri özeti uyumlu); Medici siparişli tarih | EN (özet tırnakları; hangisi hangi çeviri belirsiz): "In his commercial affairs he was very unfortunate, from the improper conduct of his agents" → "Ticari işlerinde, ajanlarının uygunsuz davranışları yüzünden çok talihsizdi." · "the greater part of his private fortune was consumed" → "özel servetinin büyük kısmı tükendi." · "he gave up all commercial operations, and turned his attention to landed property" → "bütün ticari faaliyetleri bıraktı, ilgisini toprak mülkiyetine çevirdi." · "He acquired large possessions in the districts of Prato and Pisa, and in the Val di Pesa" → "Prato ve Pisa bölgelerinde ve Val di Pesa'da geniş mülkler edindi." |
| bD5 | c9 | **Lorenzo'nun sızlanması.** Lorenzo, Londra şubesinin zararının **üçte birinin** haksız yere kendi payına yazıldığından yakınır. | Treccani DBI Lorenzo (özet; olaydan sonra yazılmış sözlük maddesi) | ○ | — (birebir cümle özette yok) |
| bD6 | c9 | **Canigiani'nin Calais'si.** Edward IV'e kredi vermeyi sürdürür; karşılığında **Calais'te "kambiyo bekçisi"** görevi ve bir İngiliz kambiyo bürosu alır. Medici'yle bağı kopunca İngiliz bir kadınla evlenir, *denization* mektubu alır. | Treccani DBI Canigiani; Cambridge/Holmes özeti (M1 D44) | ○ (iki özet birbirini tamamlıyor; Edward IV'in ödeyip ödemediği çelişkili) | — |
| bD7 | c9 | **Portinari kardeşleri.** Pigello ve Acerrito Milano'yu yönetir; Tommaso Brugge'ye gönderilir. Medici 1478–80'de Brugge'yi tasfiyeye karar verince Tommaso'yu şubeyi üstlenmeye zorlar. | Treccani DBI T. Portinari ve P. Portinari | ◐ (DBI + Wikipedia) | — |
| bD8 | c7 | **Sixtus IV'ün tepkisi.** Lorenzo Imola avansını reddedince papa şiddetle protesto eder, misilleme olarak Lorenzo ve Giuliano'yu *depositario*'luktan alır. | Treccani DBI Lorenzo | ○ | IT: "Sisto IV protestò violentemente e tolse, come rappresaglia, al M. e a Giuliano la carica di depositario pontificio, recando un grave danno al banco." → "Sixtus IV şiddetle protesto etti ve misilleme olarak M.'den (Lorenzo) ve Giuliano'dan papalık depositario görevini aldı; bu bankaya ağır zarar verdi." |
| bD9 | c7 | **Şap Pazzi'ye geçer.** | Treccani DBI G. de' Pazzi | ○ | IT: "fu ancora Sisto IV, nel giugno del 1476, a trasferire dalla banca Medici a quella Pazzi, il monopolio dell'allume" → "Şap tekelini Medici bankasından Pazzi bankasına, 1476 Haziranında yine Sixtus IV aktardı." |
| bD10 | c3/TR | **Piero'nun sözleşmesi** (b11). | Treccani DBI Piero (I. Walter, c. 73, 2009) | ◐ | IT: "In compenso nel 1466 il M. ottenne dalla Camera apostolica un contratto per partecipare allo sfruttamento delle miniere di allume a Tolfa, recentemente scoperte, e per la commercializzazione di questo prezioso minerale." → "Karşılığında 1466'da M[edici], Apostolik Camera'dan, yakın zamanda bulunmuş Tolfa şap madenlerinin işletilmesine katılmak ve bu değerli mineralin pazarlanması için bir sözleşme aldı." |
| bD11 | c3 | **Sassetti'nin görevi.** | Treccani DBI Sassetti | ◐ | IT: "Nel 1463 divenne direttore generale del banco Medici, carica che tenne per quasi un trentennio fino alla morte, nel 1490." → "1463'te Medici bankasının genel müdürü oldu; bu görevi, 1490'daki ölümüne dek, yaklaşık otuz yıl sürdürdü." · "questioni strutturali (un'organizzazione finanziaria non efficiente)" → "yapısal sorunlar (verimsiz bir mali örgütlenme)." |
| bD12 | c10 | **1494: merdiven.** Kalabalık sokakları ve meydanları doldurur; görevlilerin evlerini ve Medici'nin bahçelerini basar. Ama sarayın **üst katlarına** çıkmaları engellenir. | Palazzo Medici Riccardi müzesi (kurumsal sayfa, EN arayüz) | ◐ (yağma) · ○ (üst kat) | EN (özet tırnağı): "…the Signoria's representatives prevented the rioters from climbing to the upper floors of Palazzo Medici, which had by then been requisitioned, thereby protecting its treasures." → "…Signoria temsilcileri, o zamana dek el konmuş olan Palazzo Medici'nin üst katlarına çıkmalarını engelleyerek hazineleri korudu." |
| bD13 | c2 | **Kardinallik parası.** Giovanni, Cossa'ya kardinal makamını "satın alması" için para verir; Cossa borcu, papa olunca Medici'yi papalık maliyesinin başı yaparak öder (Wikipedia'nın anlatımı). | Wikipedia (Giovanni di Bicci / Medici Bank) — modern özet; DBI'de "başlık" yok | ◐ (borç) · ○ (başlık) | EN (özet tırnağı): "In 1410, Giovanni lent John XXIII, then simply known as Baldassare Cossa, the money to buy himself the office of cardinal, which he repaid by making the Medici Bank head of all papal finances once he claimed the papacy." → "1410'da Giovanni, o sırada yalnızca Baldassare Cossa diye bilinen XXIII. Johannes'e kardinal makamını satın alması için para verdi; Cossa borcu, papalığı ele geçirince Medici Bankası'nı bütün papalık maliyesinin başına getirerek ödedi." |
| bD14 | c2 | **Fidye ve mezar.** | Italy On This Day (Baldassare Cossa) — popüler site | ○ | EN (özet tırnağı): "De Medici paid the stiff ransom of 38,000 ducats himself, and when the former pope died the following year in Florence, de Medici sponsored the construction of his magnificent tomb in the Baptistery." → "De Medici, 38.000 dukatlık ağır fidyeyi kendisi ödedi; eski papa ertesi yıl Floransa'da ölünce de Vaftizhane'deki görkemli mezarının yapımını üstlendi." |
| bD15 | c3/TR | **Aforoz tehdidi işe yaramadı.** Alıcılar daha ucuz Türk şapına geçer; Medici'nin fazla şapı fiyatı düşürür; yabancı alıcılar dernek kurup pazarlık eder. | Parks, *Medici Money* (2005) — NovelInvestor okuma notları; Postrel (Reason, 2019) | ○ (Parks) · ◐ ("Türk şapı girmeye devam etti") | — |
| bD16 | c16 | **Padgett–Ansell'in özeti.** | Padgett & Ansell (1993) — AcaWiki'de alıntılanan özet cümlesi | ◐ | EN (özet tırnağı): "…Medicean political control was produced by means of network disjunctures within the elite, which the Medici alone spanned." → "…Medici'nin siyasi denetimi, seçkinlerin içindeki ağ kopukluklarıyla üretildi; bu kopuklukları yalnız Medici aşıyordu." |
| bD17 | c16 | **de Roover'ın Lorenzo yargısı.** Lorenzo "parlak bir devlet adamı"; iş yeteneği edinmedi (yaklaşık). | de Roover (1963), dokumen.pub kopyasından alıntı özeti (kelimeler arama özetinde köşeli parantezli) | ○ | EN (**yaklaşık, birebir kullanma**): "a brilliant statesman … never acquired an aptitude for business" → "parlak bir devlet adamı… iş yeteneği hiç edinmedi." |
| bD18 | c1/TR | **Şap ve siyaset.** Spectator'ın 1949 incelemesi Tolfa sözleşmesini "Avrupa'nın genel siyasi tarihine dolanan olaylar zincirinin ilki" diye niteler. | Spectator, 27 Mayıs 1949, "Alum in History" (yazar belirsiz kitap incelemesi; Lorenzo'yu 1466'ya yanlış yerleştiriyor) | ○ (yorum cümlesi, kaynak değil) | EN (özet tırnağı): "the first of a series of incidents by which the alum trade became inter-woven with the general political history of Europe" → "şap ticaretinin Avrupa'nın genel siyasi tarihine dolanmasına yol açan olaylar zincirinin ilki." |

---

## 5. Sayılar ve ölçüler

> Çelişki olan yerde **her değer** yazıldı. "Hesap" = bana ait türetme.

### 5A. Şap (alum)

| Ölçü | Değer(ler) | Sınıf | Kaynak | Not |
|---|---|---|---|---|
| Tolfa keşif yılı | **1460 · 1461 · 1462** (Mayıs 1462 "en olası"; 1461'in Nisanı: Corneto imtiyazı) | ◐ | KB01, KB02, KB03, KB04, KB07 | Tek yıl verme; aralık ver. |
| Castro imtiyazı | **25 yıl** (Corneto Komünü); II. Pius bullası: üretilen **kantar başına 2 dukat** | ○ | KB01 | 1466 sözleşmesindeki "2 dukat/kantar" ile karışma riski var (aşağıda). |
| 1466 sözleşmesi | **9 yıl**; Papa **30 ay** sonra fesih hakkı (○, tek kök) · Camera'ya **2 dukat/kantar** + ek kârın **2/3'ü** (M1, ◐) · başka anlatım: Medici 1/3, "Camera ve haçlı fonu" 2/3 | ○ / ◐ | KB04, KB05, KB06, K110, K111 | Hangi kantar? (**doğrulanamadı**). |
| Medici'nin birim kazancı | **kantar başına 1 altın dukat** | ○ | KB06 | Dönem belirsiz ("sonraki sözleşme" olabilir). |
| 1470 kartel | **11 Haz 1470**; **25 yıl**; satış/üretim yarı yarıya; Tolfa + Ischia/Agnano | ◐ (tarih) · ○ (hüküm) | KB04, KB06 | |
| 1471 | **4 yıllık yenilenebilir** | ○ | KB06 | |
| Tolfa'nın satın alınması (1469) | **17.300 altın dukat** (EdP, DBI) · **≈17.000 altın scudo** (EI) | ◐ | KB08, KB02 | |
| Foça üretimi | **≈15.800 kantar/yıl** (1452 akti) · **51.800 kantar ≈ 2.500 ton** (1445, Flaman limanlarına) | ○ (**çelişkili**) | KB23, KB21 | 1 kantar ≈ 47,6 kg ise 51.800 kantar ≈ 2.470 ton (hesap; kantar ağırlığı **doğrulanmadı**, HAFIZA). Tek rakam kullanma. |
| Tolfa toplam üretim | 1462–1796 arası ≈ **17 milyon ton alunit** | ○ | KB04 (Delumeau'ya atıf) | Alunit cevheri, saf şap değil. |
| Imola (Sixtus IV) | **30.000 dukat** (Machiavelliana) · **40.000 dukat** (DBI Lorenzo) | ○ | KB14, KB13 | |
| Volterra | ayaklanma 26 Nis 1472 · kuşatma **25 gün** (Wikipedia) / **≈1 ay** (DBI) · teslim **16 ya da 18 Haz** · yağma **18 Haz** · bir kaynakta **7.000** Floransalı asker | ◐ / ○ | KB16, KB17 | |
| Medici'nin şaptan kârı | **Rakam yok.** Mart 1475'te zarar (Parks özeti) | ○ | KB19 | "Şapla zenginleşti" demek kaynaklı değil. |

### 5B. Şube takvimi (M1 §5D'nin güncellemesi)

| Şube | Açılış | Kapanış | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|
| Floransa (Tavola) | 1397 | 1494 (el koyma) | ◐ | M1, K01 | |
| Roma | ≈1385/86 (Vieri) · 1397 yeni ortaklık | 1494 (HAFIZA) | ◐ (açılış) | K50, KB28 | Giovanni Benci 1409'dan Roma'da. |
| Venedik | 1385 (Vieri'nin ortaklığı) · **25 Mart 1402** (Medici) | **1481** (tek özet) | ◐ / ○ | KB28, K58, K115 | |
| Napoli | **1402** | **1416** (DBI; temsilci 1426'ya dek) · **1425** (Wikipedia-it) | ○ | KB28, KB27 | Yerine Cenevre + Gaeta. |
| Cenevre | **1420'ler** (1426 dokumen; 1429'da Benci tek müdür DBI) | **1466'da Lyon'a taşındı** (1464 alt.) | ○ / ◐ | KB28, K115, K54 | Sassetti 1448–59 (M1); 1462'de şirket payları. |
| Basel | **1433** (Konsil) | ? | ◐ | KB28, K115 | |
| Ancona | **1436** | ? | ○ | K115 | |
| Brugge | **24 Mart 1439** | **1478–81**: karar 1478–80 (DBI) · kapanış 1480 ↔ 1481 | ◐ | K01, KB30, K115 | Portinari. |
| Pisa | **1442** | **1443** (Wikipedia) ↔ **1489** (dokumen) | ◐ / çelişki | K115, K01 | |
| Londra | **1446** (Canigiani faktör) | **1472 · 1477 · 1478** | ◐ (1477–78) | KB31, KB30, K01, KB27, KB32 | Zarar 51.533 fl. |
| Avignon | **1446** (sınırlı → 2 yılda tam ortaklık) | **1479 ↔ 1480** | ◐ / ○ | KB27, K115 | |
| Milano | **1452 / erken 1453** (Sforza'nın isteğiyle) | **1478 ↔ 1479** | ◐ | KB27, KB30, K115 | Pigello Portinari. |
| Lyon | **1466** (Cenevre'den; alt. 1464) | **≈1490** (sürüldü) ↔ **1494** (devredildi) | ○ | K54, K115, K01, KB32 | Lionetto de' Rossi. |

### 5C. Papalık *depositario* takvimi

| Dönem | Durum | Sınıf | Kaynak |
|---|---|---|---|
| ≈1389–1404 (Bonifacius IX) | Papa en çok Floransalılara başvurur (Giovanni di Bicci, Doffo degli Spini, Alberti) | ○ | KB34 |
| 1403 | Cossa Gozzadini'yi görevden uzaklaştırır; görev esas olarak Spini, Alberti, Ricci'de (M1) | ○ | KB34, K50 |
| 1410–1415 (Cossa/XXIII. Johannes) | Giovanni Cossa'ya borç verir; Wikipedia "Medici papalık maliyesinin başı" der ↔ DBI: Spini üstün | ◐ (borç) · ○ (başlık) | KB35, KB34 |
| 1415–1420 | Konstanz sonrası Medici rekabet eder; Spini üstün | ◐ | KB35, KB34 |
| 1420 | Spini batar; Medici önceliği geri alır | ◐ | KB34, KB35 |
| **1420 ya da 1422** | **Bartolomeo de' Bardi** Martinus V döneminde Curia *depositario*'su; ≈22 yıl | ◐ | KB34, KB35 |
| 1455 | Callistus III Roma müdürü Martelli'yi alır (M1 #50; bu turda yeniden doğrulanmadı) | ○ | K115, K82 |
| 1465 | II. Paulus *Depositeria*'yı verir ("Medici'lerin neredeyse kesintisiz elinde tuttuğu") | ○ | KB09 (özet) |
| 1466–1469 | Tolfa yönetimi + *Haçlı Depositeria'sı* Medici'de (EdP Paolo II) | ○ | KB08 |
| **1474** | Sixtus IV Lorenzo ve Giuliano'yu alır; Pazzi'ye | ◐ | KB12, KB13, KB19 |
| **Haz 1476** | Şap tekeli Pazzi'ye | ○ | KB11 |

**Güvenli cümle:** *"Medici, 1410'larda Cossa'nın bankacısıydı; Roma müdürleri 1420'lerin başından itibaren papalığın resmî depositario'su oldu — kesintilerle — ve Sixtus IV bu görevi 1474'te Pazzi'ye verdi."* (Kesintilerin yılları kesin değil.)

### 5D. Harcama, maliyet, servet, ücret

| Ölçü | Değer(ler) | Sınıf | Kaynak | Not |
|---|---|---|---|---|
| Lorenzo'nun *Ricordi* toplamı (1434–71) | **663.755** fl (sadaka + yapı + vergi, diğerleri hariç) · DBI baskısı **663.775½** · el yazmasında sayıdan sonra kesir işareti; Fabroni 663755 | ◐ | KB36, KB13 | **"Sanat" değil**, **Cosimo tek başına değil**. |
| Wikipedia "Cosimo" | ">600.000 altın florin, ≈500 milyon $, sanat ve kültüre" | ○ | K89 | Büyük olasılıkla yukarıdaki kaydın yanlış okunması (**YORUM**). |
| Palazzo Medici | yalnız yapı **60.000 dukat** (Vespasiano tahmini) | ○ | KB37 | Gerçek maliyet bulunamadı. |
| San Marco (çapraz: M3) | Papa önerisi **10.000 florin**; toplam **>40.000 florin** (Vespasiano'ya göre; birim dukat değil florin) | ◐ ANEKDOT (M3) · ○ (M1 #44: 10.000 taahhüdü) | M3 (M3'ün kendi K12 kodu), M1 K105 | Bu turda yeniden aranmadı; "Cosimo'nun sanatı" rakamları için doğru ölçek: tek proje >40.000 fl, hane toplamı (sadaka+yapı+vergi) 663.755 fl. |
| Cosimo'nun yönettiği miras | **235.137 scudi di suggello** (Pierfrancesco ve oğulları için) | ○ | KB36 | |
| Giovanni'nin ölümdeki serveti | ≈**180.000** fl ("Lorenzo'ya göre") · **179.221** | ○ | K48, K102, KB19 | "Lorenzo"nun kim olduğu hâlâ **doğrulanamadı**; Ricordi'de geçmesi olası ama HAFIZA. |
| 1427 toplam beyan | ≈**10.170.000** fl (bir kaynak) · M1 hesabı ≈**10,07 milyon** | ○ | K41, K42 | |
| Giovanni 1427 beyanı | **Bulunamadı**; Parks özeti: iki yün imalathanesi | ○ | KB19 | HAFIZA "net ≈79 bin": kullanma. |
| Floransa ücretleri | **Bulunamadı.** "16,84 / 16,908" = Bruges serisi (Flaman groatı), **kullanma** | — | KB38 | İşaretçiler: Tognetti (1995, *Archivio storico italiano*, Tablo A1, s. 317–18), Munro'nun Floransa fiyat-ücret dosyası, Ridolfi–Vasta (2025), Caferro (Yale). |
| Kur (popüler özet) | 1349: **1 fl = 64 soldi** · 15. yy ortası: **1 fl ≈ 90 soldi di piccioli** | ○ | KB38 | M1: 1324–25 66–67 soldi (K100); 1500: 1 fl = 7 lira. Tutarlılık kontrolü gerekir. |
| İşçi günlük ücreti (popüler) | 7–10 soldi (Goldthwaite'e atfen) ↔ ≈4,5 soldi | ○ (çelişkili) | KB38 | Kullanma. |

### 5E. Zarar, fidye, ödül, öteki

| Ölçü | Değer(ler) | Sınıf | Kaynak |
|---|---|---|---|
| Londra tasfiyesi | **51.533** altın florin (1478) | ○ (tek köken) | K01, KB27 |
| Londra + Brugge | **>70.000 florin** (Wikipedia) · **70.000 dukat** (Lorenzo'ya göre, DBI) | ◐ | K01, KB30 |
| Edward IV kredileri | **>£26.000** (1466–71; M1) | ○ | K72 |
| Cossa'nın kardinallik parası | **10.000 dukat** | ○ | KB35 |
| Cossa'nın fidyesi | **38.000 dukat** | ○ | KB35 |
| 1494 ödülleri | Piero **4.000**, Giovanni **2.000 florin** (Beck) · asi sağ yakalanırsa **5.000 dukat** | ○ | KB40 |
| 1494 alacak talebi | **15.445 florin** | ○ | K115 |
| Monte delle doti | 1442 sonu **373 / >1.800** mevduat ödenmiş · 1425–1569 ≈**30.000 kız** · Lorenzo iddiası **53.643 fl** | ○ | KB46, K01 |
| Bardi/Peruzzi | geri ödeme **%48 / %37** · Floransa'nın 1343 temerrüdü ≈**1,8 milyon fl** · Villani: Edward III borcu **900.000 / 600.000 fl** (M1) | ○ / ◐ | KB47 |
| Floransa nüfusu 1427 | şehir ≈**37–38 bin** (M1) · **55 bin** (CLARIAH veri hikâyesi, tahmin) | ◐ / ○ | K47 |
| Padgett–Ansell verisi | **215** seçkin aileden **92**'lik ağ; **33 blok** | ○ | KB42 |

---

## 6. Mit/tartışma ve TR-BAĞ

### 6A. Mit/tartışma (iddia → kim ne diyor → değerlendirme)

| # | İddia | Kim ne diyor | Değerlendirme | Sınıf |
|---|---|---|---|---|
| bM1 | **"Medici şap tekeli kurdu ve şaptan zenginleşti."** | 1466 pazarlama sözleşmesi (9 yıl/30 ay), 1470 Napoli kartel, 1474 depositeria kaybı, Mart 1475 zarar, Haz 1476 Pazzi, 1490'larda "pahalı yatırım". | **NÜANS:** Medici bir *halka*; kâr rakamı yok, ipuçları zarar yönünde. Tekel Türk şapı ve alıcı dernekleri karşısında erimiş. | ◐ (yapı) · ○ (zarar) |
| bM2 | **"II. Pius şap dağıtımını Medici'ye verdi."** | Wikipedia "Tolfa" böyle der; Treccani DBI Piero: sözleşme 1466 (Piero); EdP Paolo II: yönetim II. Paulus'un döneminde Medici Bankası'na; Günster–Martin: 1466. | **DÜZELTME:** II. Pius Castro'nun imtiyazını (2 dukat/kantar) tanıdı; Medici'nin sözleşmesi **II. Paulus** dönemi. | ◐ |
| bM3 | **"Lorenzo 1466'da şap sözleşmesini imzaladı."** | Spectator 1949 ve Parks özeti "Lorenzo" der; DBI Piero maddesi "il M." (Piero) der. | **DÜZELTME:** imza Piero'nundur; Lorenzo 17 yaşında. Lorenzo'nun şap işine sonradan girişi (Volterra) ayrı. | ○ |
| bM4 | **"Şap = haçlı parası."** | Pius II döneminde gelirler haçlı için ayrılır (Wikipedia, *Renaissance Papacy*); Medici *Haçlı Depositeria'sı*nı alır (EdP); 1466'da gelirin 2/3'ü "Camera ve haçlı fonu" (diğer anlatım); Paulus II Skanderbeg için para düşünürken "neredeyse umutsuz" olduğunu söyler (EN: "almost desperate"); şap geliri bir Macaristan hibesi için kullanılır (dokumen özeti; ○). | Söylem gerçek; **uygulama** karışık: gelir Camera'nın genel ihtiyacına gider. | ◐ |
| bM5 | **"Aforoz tehdidi Türk şapını durdurdu."** | Parks özeti: alıcılar yine de ucuz Türk şapına geçti. Postrel: Türk şapı Avrupa'ya girmeye devam etti, yeni kaynaklar bulundu. | **Hayır.** Tekel hiçbir zaman tam kapanmadı. | ◐ |
| bM6 | **"Volterra'nın yağması Lorenzo'nun emriydi."** | Genel suçlama; EI Volterra: Lorenzo'nun etkisi "yalnız olası"; 19. yy. özet: yağma savunma için tutulan paralı askerlerin eseri; DBI Capacci: Lorenzo imtiyazı geri vermek için araya girdi. | **Tartışmalı:** taraflar ayrı söylenir; Lorenzo'nun yağmadaki *kişisel emri* kaynaklı değil. Mizah kapalı. | ○ |
| bM7 | **"Volterra ayaklanması şap yüzündendi."** | Machiavelli (Gutenberg özeti): imtiyaz anlaşmazlığı; DBI Maffei: Raffaele Maffei ve Fiumi şap tekeli hedefini görür. | Şap, tetikleyici ve motiflerden biri; tek neden değil. | ◐ |
| bM8 | **"Lorenzo bankayı batırdı / banka 1494'te battı."** | Machiavelli+Guicciardini yargısı (de Roover aktarır): ticarette talihsiz, ajanlar prens gibi; DBI Sassetti: yapısal sorunlar, verimsiz mali örgütlenme; DBI T. Portinari: de Roover Portinari'yi suçlar, başkaları "karmaşık durum" der; Holmes: Edward IV'e bağımsız krediler; Goldthwaite: Floransa'da 1500 öncesi banka krizi yok. | **Çok nedenli**; tek kişiye bağlanmaz. | ◐ |
| bM9 | **"Londra şubesi 1478'de kapandı."** | Wikipedia: tasfiye 1478'de bitti (51.533 fl); DBI T. Portinari: 1477'de kapandı; bir çalışma notu: 1472. | **Çözüldü:** *"1477–78'de tasfiye edildi."* | ◐ |
| bM10 | **"Canigiani Londra müdürüydü / ortaktı."** | DBI: 1446 faktör, 1472 tek direktör; de Roover (Holmes özeti): hiç ortak alınmadı; başka kaynak: müdür olmadı. | **Çelişkili**; "Londra'daki Floransalı faktör" güvenli. | ○ |
| bM11 | **"Medici → Fugger → Rothschild zinciri."** | (KB44) Wikipedia Fugger: "replaced the Medici" (*citation needed*); Altoviti maddesi: Strozzi, Salviati, Altoviti papalık finansında Fugger ile yarıştı; EFW: Fugger–Rothschild arasında doğrudan bağ yok, Fugger'ler öncül olmuş olabilir; Fugger'in gücü madenler/emtia ve Habsburg kredisine dayanır; bir kaynak: bankacılık merkezi 1480–1520 arasında Floransa/Venedik'ten Augsburg'a kayar. Ferguson (PT baskısı özeti, K116): Medici bankası birden çok bağlı ortaklıktı; Rothschild'ler 1815–59 arasında ≈£43 milyon nominal 14 devlet tahvili çıkardı (süreklilik iddiası değil). | **Anlatısal benzetme**; **kurumsal süreklilik yok** (farklı şehir, kuşak, ortaklık biçimi). Ortak payda: papalık/kraliyet kredisi + poliçe ağı. Ferguson'un *kendi* ifadesi bu turda **doğrulanmadı** (HAFIZA). | ◐ |
| bM12 | **Padgett & Ansell: "Medici'nin yükselişi ağ pozisyonunun sonucuydu."** | Özet: Medici, birbirine bağlı olmayan seçkin grupları **yalnız kendisinin köprülediği** bir ağ konumundaydı; "robust action" = Cosimo'nun belirsiz, çok-sesli (*multivocal*) tarzı; Cosimo statü açısından orta zeminde durarak sınırları aşabildi. Evlilik bulgusu (özet, ○): Medici 1378–82'de Ricci ile isyana katılan eski zengin ailelerdendi; Ricci yok edildi, Medici yalnız dışlandı; 1420'ye gelindiğinde yine kabul edilir evlilik ortağı. **Eleştiri:** Cohn (1999) yükselişi süreklilik olarak görür; Dale Kent'in hizip/patronaj anlatısı (veriyi ilk Kent topladı, Padgett–Ansell kodladı); yöntem makalesi: öz-vektör merkeziliği seçimi tartışmalı ama Medici yönü yok sayılsa/ters çevrilse de aracılık sıralamasında zirvede kalıyor; bir Almanca inceleme ağ yaklaşımının bazı olguları yakalamakta yetersiz olduğunu savunur. | **Sağlam yapısal tez**, ama *neden-sonuç* ve *veri ölçeği* (215→92 aile) tartışmalı. Tarihçi eleştirisinin tam metni bu turda **okunmadı**. | ◐ (künye/çekirdek) · ○ (ayrıntı, eleştiri) |
| bM13 | **"Lorenzo çeyiz fonunu (Monte delle doti) yağmaladı."** | Wikipedia: 53.643 fl aldı, kısmen iade; Market Histories (M1 D46) ve bir popüler site atıfsız aynı iddia. | **Zayıf**; rakam ikinci aramada bulunamadı; bilimsel kaynak yok. **Kullanma** (gerekirse "anlatılır ki"). | ○ |
| bM14 | **"Cosimo sanata 600 bin florin harcadı."** | Wikipedia: ">600.000 sanat ve kültüre"; Lorenzo'nun *Ricordi*'si: 663.755, **sadaka+yapı+vergi, 1434–71**. | **Çözüldü:** rakam hane harcamasıdır, "sanat" değil. | ◐ |
| bM15 | **"Medici 1410'dan beri papalık bankacısı."** | Wikipedia: 1410'da Cossa; DBI: 1420/22'de Bardi, Spini'den sonra. | **İki aşama:** 1410'larda Cossa'nın bankacısı; resmî *depositario* 1420'lerin başında. | ◐ |
| bM16 | **"Saray 1494'te yağmalandı."** | Genel anlatım ↔ müze sitesi: üst katlar korundu, yağma bahçelerde ve bazı Medici mekânlarında. | **NÜANS:** "kısmen yağmalandı, resmen el konuldu". | ◐ |
| bM17 | **"Medici bankası modern bankacılığın atası."** | M1 M2'ye ek: **de Roover**: ortaklıklar ağı, "holding" etiketi (çağdaşlar *compagnia* der), düşüş = aile-merkezli yapı, ajanlar, prenslere kredi; **Goldthwaite**: Floransa bankacılığı 1494 sonrası bile krize girmedi, servetler miras bölüşümüyle sık el değiştirdi; **Parks**: faiz yasağı ve vicdan çerçevesi, bankacılara şüpheyle bakan hızlı bir anlatı (The Economist); **bir Almanca inceleme**: de Roover'ın "düşüş" varsayımı okumasını yönlendirdi. | **"İlk/icat" denmez**; Medici bir halka. | ◐ |

**Tarihyazımı: kimin sözü ne (özet tablo)**

| Yazar | Eser | Tez | Sınıf |
|---|---|---|---|
| **R. de Roover** | *The Medici Bank* (1948); *The Rise and Decline of the Medici Bank, 1397–1494* (1963); JEH makaleleri; Sassetti makalesi | Merkezsiz ortaklıklar ağı; düşüş = aile-merkezli yapı, kötü ajan politikaları, Edward IV ve Cesur Charles'a krediler, 1480–90 gerilemesinin 1494'te iflasa dönüşmesi; Lorenzo "parlak devlet adamı, iş adamı değil" (yaklaşık) | ○/◐ |
| **R. Goldthwaite** | *The Economy of Renaissance Florence* (2009) | 1500 öncesi Floransa'da banka krizi yok; Medici çöküşü sistemik değil; miras bölüşümü servetleri kırılgan kılar | ○ |
| **T. Parks** | *Medici Money* (2005) | Faiz yasağı/"metafizik"; şap macerası; 1475'te zarar; Pazzi'ye kayıp | ○ |
| **J. Padgett, C. Ansell** | AJS 98(6), 1993 | Ağ boşluğu + "robust action" | ◐ |
| **D. Kent** | *The Rise of the Medici* (1978) | Hizip ve patronaj anlatısı | ◐ |
| **S. Cohn** | *Creating the Florentine State* girişi (1999) | Süreklilik, kırılma değil | ○ |
| **G. Holmes** | Londra şubesi (1996) | Lorenzo'nun bağımsız kralı kredileri; belge: *Mediceo avanti il Principato* + PRO | ◐ |
| **A. Günster, S. Martin** | *Rev. Ind. Org.* 2015 | Şap kartel; Papalık–Napoli | ◐ |
| **V. Postrel** | Reason, 2019 | "Papa bile tekeli koruyamaz" | ○ |

### 6B. TR-BAĞ: ŞAP HİKÂYESİ (Foça → Tolfa → Medici → Volterra → Pazzi)

> M1 T1–T5'in bu turda doğrulanmış sürümü. **Hikâye akışı (10 halka):** her halkanın sınıfı yanındadır.

1. **Şap nedir:** kumaş boyamada **mordan** — boyanın liften akmamasını sağlar; "en yaygın mordan" (kökboya/madder boyası için) ◐ (KB26: *Madder Red*, *Soil to Foil*). Floransa'nın yün/boya sanayisi (c1) bu yüzden şapa muhtaçtı.
2. **Kaynak Doğu'dadır:** Foça (Cenevizli), Anadolu içi (Şebinkarahisar, Kütahya, Gediz) ◐/○; Venedik aracılığı ○ (KB03).
3. **1275 → 1346/47:** Zaccaria'dan **Maona**'ya; ihale usulü; 1445/1452 üretim rakamları (çelişkili) — b1–b4.
4. **1453–1455:** Fetih + Foça'nın Osmanlı'ya geçişi; Batılı alıcıların Tolfa'ya dönmesi — b5–b6.
5. **1460–62:** Tolfa'da **Giovanni di Castro**; II. Pius, "Türk'e karşı zafer" söylemi (ANEKDOT), Camera/haçlı fonu — b7–b9, bD2.
6. **1466:** **Piero** ve Medici grubunun **pazarlama sözleşmesi** (II. Paulus; 9 yıl/30 ay) — b11–b12.
7. **1468–1470:** Cesur Charles ve Flaman dokumacılar; **Napoli kartel** — b13, b15.
8. **1472:** **Volterra** — ikinci şap yatağı; ayaklanma ve yağma — b17–b19.
9. **1474–1476:** Sixtus IV Medici'yi *depositario*'luktan alır; şap Pazzi'ye — b21, b23. **Mart 1475:** zarar — b22.
10. **1488–1490'lar:** II. Bayezid'in kaçakçılık fermanı; Medici kirayı bırakır; Spannocchi, Chigi — b24–b25.

**Güvenli cümle önerileri (senaryo değil, olgu çıpası):** *"Foça 1455'te Osmanlı'ya geçince Batı, şapı kendi topraklarında aradı; Papalık Devleti'nde bulunan Tolfa şapının pazarlanması 1466'da Piero de' Medici'nin de içinde olduğu bir gruba verildi."* — b5, b7, b11 (◐). *"Medici bu işten ne kadar kazandı diye sorarsak elimizde rakam yok; 1475'te zarar yazılıyor."* — b22 (○).

| # | Konu | İçerik | Sınıf | Kaynak / Not |
|---|---|---|---|---|
| bT1 | **Foça (Phocaea) şapı** | 1275: Bizans → Cenevizli Zaccaria; 1346/47 → Giustiniani'nin **Maona**'sı; üretim 1445/1452 rakamları çelişkili | ◐ | KB20–KB23, KB24 |
| bT2 | **Foça'nın Osmanlı'ya geçişi (1455)** | Fetihten iki yıl sonra; Eski ve Yeni Foça birlikte | ◐ | KB20, KB24; komutan adı **bulunamadı** |
| bT3 | **Şebinkarahisar = "Şapkarahisar"** | Osmanlı döneminde şap madeni nedeniyle diğer Karahisarlardan ayırmak için **Şapkarahisar / Karahisar-ı Şarkî / Şarkîkarahisar**; bugünkü "Şebinkarahisar" biçimi 19. yy.; kaynaklara göre bu yolun batı kesimindeki pembe renkli kayalarda bulunan şap Eskiçağ'dan beri dünyanın en kaliteli şapı olarak bilinir ve Avrupa'ya ihraç edilirdi; 12. yy.'da Avrupa tekstilinin şap ihtiyacı büyük ölçüde Anadolu'dan ve özellikle Şebinkarahisar'dan karşılanır; şap ilaç, altın/gümüş parlatma, boyacılık ve deri işlemede kullanılır | ◐ (ad) · ○ (ihracat/kullanım) | KB25 (TDV İA + Küre) |
| bT4 | **"Şebin" ← "şeb" (Arapça şap)** | Etimoloji bu turda da **doğrulanamadı** | HAFIZA | Kullanma; sevimli çıpa ama kaynaksız |
| bT5 | **II. Bayezid fermanı (1488)** | Şap kaçakçılığına karşı; Gediz ve Şebinkarahisar şapı | ○ | KB22 |
| bT6 | **Kütahya şapı** | Bir tarihçi, fiyat-şişirme anılan bir göndermeyi Kütahya şapı diye okur (Fleet) | ○ | KB23 |
| bT7 | **Tolfa = "Türk'e karşı zafer"** | Pius II söylemi; keşif anlatıları II. Pius'un anılarına dayanır | ANEKDOT (○) | bD2, KB21, KB49 |
| bT8 | **Osmanlı'nın şap geliri** | Günster–Martin: Tolfa, Osmanlı'yı Avrupa'dan elde ettiği şap gelirinden yoksun bıraktı | ◐ | KB04, KB03 (iddia; rakam yok) |
| bT9 | **Aforoz tehdidi ve Türk şapı** | Tehdit alıcıyı durdurmadı; Türk şapı girmeye devam etti | ◐ | KB19, KB05 |
| bT10 | **Okunacak/yeni** | Günster & Martin (2015); Fleet, *European and Islamic Trade in the Early Ottoman State*; "The Flesh Eating Stone: Alum Mining and Trade in Asia Minor"; "Production et commerce de l'alun oriental en Méditerranée, XIe–XVe s." (ResearchGate); "The Margani and the alum mines in Tolfa"; Delumeau, *L'alun de Rome* (1962; M2'de de öneriliyor); Zippel'in Tolfa şapı çalışması (**HAFIZA**: yazar/yıl); Setton (M1 T6) | ○ | KB04, KB22, KB23 |
| bT11 | **Para: florin/dukat/akçe** | Hiç aranmadı (M1 T8) | HAFIZA | Devam sorgusu |

---

## 7. Hâlâ eksik kalanlar

| # | Eksik | Neden / ne bulundu | Önerilen yol |
|---|---|---|---|
| **X1** | **Medici'nin şaptan kazancı** | Hiçbir kaynakta rakam yok; yalnız "kantar başına 1 dukat" (○) ve Mart 1475 zararı (○) | Delumeau (1962); de Roover (1963) şap bölümleri; Günster–Martin tam metin (Springer) |
| **X2** | **Floransa ücretleri** (usta/işçi günlük) | Bulunamadı; "16,84 soldi" Flaman serisi | Tognetti 1995 (Tablo A1), Munro'nun `FlorencePricesWages.doc`, Ridolfi–Vasta WP 928 PDF, Goldthwaite *Building of Renaissance Florence* |
| **X3** | **Palazzo Medici gerçek maliyeti** | Yalnız Vespasiano'nun 60.000 dukat tahmini (○) | Ferretti (UniFi, M1 K106); Goldthwaite ve F. W. Kent (ikisi de HAFIZA önerisi) |
| **X4** | **Giovanni'nin 1427 beyanı, Cosimo 1457** | Bulunamadı | Brown Üniv. catasto veritabanı; Herlihy–Klapisch-Zuber |
| **X5** | **Şube kesin yılları** | Cenevre açılışı; Venedik, Pisa, Avignon, Lyon kapanışları; Basel/Ancona kapanışı | de Roover (1963) şube tabloları; DBI Tornabuoni, Benci |
| **X6** | **1494 envanteri, alacaklılar, defterlerin akıbeti** | El koyma ve kayyum kanıtlı; ayrıntı yok | *Kampf um Florenz. Die Medici im Exil (1494–1512)*; Cambridge *Piero di Lorenzo de' Medici and the Crisis of Renaissance Italy*; ASF *Mediceo avanti il Principato* |
| **X7** | **Kütüphane satış bedeli ve geri alım yılı** | M3 #36: 1508 (◐); BML özeti 1513 sonrası gibi okunuyor; satış bedeli ve alıcı Dominiklerle pazarlık yok | BML/Laurenziana tarihçesi; M3'ün K26'sı |
| **X8** | **Padgett–Ansell tam metni ve tarihçi eleştirileri** | Yalnız özetler; Kent/Cohn karşılaştırması okunmadı | AJS 98(6) PDF (Oxford `snijders/PadgettAnsell1993.pdf` bağlantısı sonuçlarda); Kent (1978); Cohn (1999) |
| **X9** | **Fugger "halefliği" için bilimsel kaynak** | Yalnız Wikipedia/EFW/Altoviti; Ferguson'un kendi cümlesi doğrulanmadı | Häberlein, Kellenbenz (HAFIZA); Ferguson, *Ascent of Money* (İngilizce baskı) |
| **X10** | **Lorenzo ve Monte delle doti** | 53.643 fl tek köken (Wikipedia) | Molho, *Marriage Alliance in Late Medieval Florence*; Kirshner–Molho (1978); Plebani (2023) |
| **X11** | **II. Pius'un birebir sözü; Castro'nun biyografisi** | Doğrulanamadı | I Tatti *Commentaries* (Latince/İngilizce); Treccani DBI Castro tam metin |
| **X12** | **Cossa fidyesi birimi (dukat/florin) ve ödeyen** | 38.000 dukat (tek kaynak) ↔ Floransa Cumhuriyeti ödedi (tek kaynak) | Cossa biyografileri; DBI Cossa |
| **X13** | **Martinus V–mitra anekdotu** | Tek DBI özeti | DBI Giovanni di Bicci tam metin |
| **X14** | **Imola tutarı ve kimin adına** | 30.000 ↔ 40.000 dukat; Girolamo ↔ Pietro | DBI Lorenzo, DBI Riario; M2 ile çapraz |
| **X15** | **Para: florin–dukat–akçe ilişkisi (T8)** | Hiç aranmadı | Spufford, *Handbook of Medieval Exchange* (M1 K100); Pamuk'un Osmanlı para tarihi çalışması (HAFIZA önerisi) |
| **X16** | **Florin altın içeriği / değeri** (görev §8) | Bu turda yeniden aranmadı; M1 §4A değerleri (3,53 g, .986; 1252–1533) geçerli | Bundesbank sayfası (M1 K05), Moruzzi (K06); bir numismatik güncel değer tablosu |
| **X17** | **14. yy. Floransa nüfusu aralığı** (görev §8) | Yalnız 1338 ≈90.000 (Villani, M1) ve 1427 şehir ≈37–38 bin / 55 bin tahmini; **1300 tahmini bulunamadı** | Herlihy–Klapisch-Zuber (*Tuscans and Their Families*, nüfus bölümü 1300–1550); Malanima (M1 K19) |
| **X18** | **Bardi/Peruzzi iflasının ölçüsü** (görev §8) | Kısmen: geri ödeme %37/%48 ve Floransa temerrüdü (○); Hunt'ın *Medieval Super-Companies* sermaye rakamları okunamadı | Hunt (1994, M1 K13); Villani |
| **X19** | **WebFetch** | `treccani.it` 1 denemede DNS hatası (`ENOTFOUND`) | Çalışan bir okuma aracı olmadan bu dosyadaki hiçbir madde ● olamaz |

---

## 8. Kaynak anahtarı (yeni: KB kodları)

> Hepsi **ikincil/aracılı** erişimdir (arama özeti). M1 `K..` kodları o dosyanın §11'indedir; burada yalnız yeni olanlar. Wikipedia ve kopyaları tek kaynak sayıldı.

| Kod | Kaynak | URL |
|---|---|---|
| KB01 | Treccani DBI — Castro, Giovanni di | https://www.treccani.it/enciclopedia/giovanni-di-castro_(Dizionario-Biografico)/ |
| KB02 | Treccani DBI/EdP — Pio II; EI — Allumiere; EI — Tolfa | https://www.treccani.it/enciclopedia/papa-pio-ii_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/pio-ii_(Enciclopedia-dei-Papi)/ · https://www.treccani.it/enciclopedia/allumiere_(Enciclopedia-Italiana)/ · https://www.treccani.it/enciclopedia/tolfa_(Enciclopedia-Italiana)/ |
| KB03 | Wikipedia — Tolfa | https://en.wikipedia.org/wiki/Tolfa |
| KB04 | Günster & Martin (2015), "A Holy Alliance…", *Rev. Ind. Org.* 47(1) | https://link.springer.com/article/10.1007/s11151-015-9465-0 · https://www.researchgate.net/publication/277881715_A_Holy_Alliance_Collusion_in_the_Renaissance_Europe_Alum_Market · https://econpapers.repec.org/article/kaprevind/v_3a47_3ay_3a2015_3ai_3a1_3ap_3a1-23.htm |
| KB05 | Reason (Postrel, 2019) — "Not Even the Pope Can Maintain a Monopoly" | https://reason.com/2019/03/23/not-even-the-pope-can-maintain/ |
| KB06 | "A Chemical Compound in a Capitalist Commodity Chain…" · "The discovery of the Tolfa mines and the reorganisation of territory and of the financial flows" | https://www.academia.edu/89977596/A_Chemical_Compound_in_a_Capitalist_Commodity_Chain_The_Production_Distribution_and_Industrial_Use_of_Alum_in_the_Mediterranean_and_the_Textile_Centers_of_the_Low_Countries_Thirteenth_Sixteenth_Centuries_ · https://www.researchgate.net/publication/378952986_THE_DISCOVERY_OF_THE_TOLFA_MINES_AND_THE_REORGANISATION_OF_TERRITORY_AND_OF_THE_FINANCIAL_FLOWS |
| KB07 | Daga — "Scoperta dell'allume" (Società Tarquiniense) | https://artestoriatarquinia.it/pubblicazione/scoperta-dellallume |
| KB08 | Treccani EdP/DBI — Paolo II | https://www.treccani.it/enciclopedia/paolo-ii_(Enciclopedia-dei-Papi)/ · https://www.treccani.it/enciclopedia/papa-paolo-ii_(Dizionario-Biografico)/ |
| KB09 | Treccani DBI — Medici, Piero de' (I. Walter, c. 73, 2009) | https://www.treccani.it/enciclopedia/piero-de-medici_(Dizionario-Biografico)/ |
| KB10 | Treccani EdP/DBI — Sisto IV | https://www.treccani.it/enciclopedia/sisto-iv_(Enciclopedia-dei-Papi)/ · https://www.treccani.it/enciclopedia/papa-sisto-iv_(Dizionario-Biografico)/ |
| KB11 | Treccani DBI — Pazzi, Guglielmo de' | https://www.treccani.it/enciclopedia/guglielmo-de-pazzi_(Dizionario-Biografico)/ |
| KB12 | Treccani EI — Medici, Lorenzo de', detto il Magnifico | https://www.treccani.it/enciclopedia/medici-lorenzo-de-detto-il-magnifico_(Enciclopedia-Italiana)/ |
| KB13 | Treccani DBI — Medici, Lorenzo de' | https://www.treccani.it/enciclopedia/lorenzo-de-medici_(Dizionario-Biografico)/ |
| KB14 | Treccani Enciclopedia Machiavelliana — Riario, Girolamo; Medici, Piero de' | https://www.treccani.it/enciclopedia/girolamo-riario_(Enciclopedia-machiavelliana)/ · https://www.treccani.it/enciclopedia/piero-de-medici_(Enciclopedia-machiavelliana)/ |
| KB15 | Machiavelli, *History of Florence* (Gutenberg #2464) · Fordham "Machiavelli on Lorenzo" · Reumont, *Lorenzo de' Medici* (Gutenberg #50624/#50625) | https://www.gutenberg.org/files/2464/2464-h/2464-h.htm · https://sourcebooks.web.fordham.edu/source/machiavelli-histflo-lorenzo.asp · https://www.gutenberg.org/files/50624/50624-h/50624-h.htm · https://www.gutenberg.org/files/50625/50625-h/50625-h.htm |
| KB16 | Treccani DBI — Capacci, Benuccio; Ivani, Antonio; Maffei, Antonio; Orsini d'Aragona; EI — Volterra | https://www.treccani.it/enciclopedia/benuccio-capacci_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/antonio-ivani_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/antonio-maffei_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/orsini-d-aragona-gentil-virginio_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/volterra_(Enciclopedia-Italiana)/ |
| KB17 | Wikipedia — Volterra; Fortezza Medicea (Volterra) | https://en.wikipedia.org/wiki/Volterra · https://en.wikipedia.org/wiki/Fortezza_Medicea_(Volterra) |
| KB18 | The Spectator, 27 Mayıs 1949, "Alum in History" | https://archive.spectator.co.uk/article/27th-may-1949/26/alum-in-history |
| KB19 | NovelInvestor — Parks, *Medici Money* okuma notları · NYRB (Mad at the Medicis; The Cosimos — özet hangisi olduğunu belirtmedi) | https://novelinvestor.com/notes/medici-money-by-tim-parks/ · https://www.nybooks.com/articles/2003/05/01/mad-at-the-medicis/ · https://www.nybooks.com/articles/2002/12/19/the-cosimos/ |
| KB20 | Wikipedia — Phocaea · The Byzantine Legacy — Phocaea · Enciclopédia Católica (PT) — Focéia · kupi.com — Foça tarihi | https://en.wikipedia.org/wiki/Phocaea · https://www.thebyzantinelegacy.com/phocaea · https://liriocatolico.com.br/enciclopedia/palavra/focea/ · https://kupi.com/en/explore/turkey/foca/history |
| KB21 | Wikipedia — Maona of Chios and Phocaea | https://en.wikipedia.org/wiki/Maona_of_Chios_and_Phocaea |
| KB22 | "The Flesh Eating Stone: Alum Mining and Trade in Asia Minor" | https://www.academia.edu/44266808/THE_FLESH_EATING_STONE_ALUM_MINING_AND_TRADE_IN_ASIA_MINOR_La_pietra_che_divora_la_carne_estrazione_e_commercio_di_allume_in_Asia_Minore |
| KB23 | dokumen.pub — Fleet, *European and Islamic Trade in the Early Ottoman State* | https://dokumen.pub/european-and-islamic-trade-in-the-early-ottoman-state-the-merchants-of-genoa-and-turkey-0521028450-9780521028455.html |
| KB24 | Türkçe tezler (İKÇÜ açık erişim; PAÜ GCRIS) — Foça tarihi | https://acikerisim.ikcu.edu.tr/yayin/1741931 · https://gcris.pau.edu.tr/handle/11499/49816 |
| KB25 | TDV İslâm Ansiklopedisi — Şebinkarahisar · Küre Ansiklopedi — Şebinkarahisar | https://cdn2.islamansiklopedisi.org.tr/dosya/38/C38012587.pdf · https://kureansiklopedi.com/tr/detay/sebinkarahisar-3 |
| KB26 | dokumen.pub — *Soil to Foil* · *Madder Red* · *The Renaissance Papacy 1400–1600* | https://dokumen.pub/soil-to-foil-aluminum-and-the-quest-for-industrial-sustainability-9780231204484-9780231555562-0231204485.html · https://dokumen.pub/madder-red-a-history-of-luxury-and-trade-1nbsped-0700712593-9780700712595-0203400437-0203400860.html · https://dokumen.pub/the-renaissance-papacy-1400-1600-9004449566-9789004449565.html |
| KB27 | Wikipedia (it) — Banco dei Medici | https://it.wikipedia.org/wiki/Banco_dei_Medici |
| KB28 | Treccani DBI — Benci, Giovanni; Medici, Vieri de'; Tornabuoni; Medici, Cambio de'; Medici, Cosimo de' | https://www.treccani.it/enciclopedia/giovanni-benci_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/vieri-de-medici_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/tornabuoni_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/cambio-de-medici_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/cosimo-de-medici_(Dizionario-Biografico)/ |
| KB29 | Treccani DBI — Sassetti, Francesco | https://www.treccani.it/enciclopedia/francesco-sassetti_(Dizionario-Biografico)/ |
| KB30 | Treccani DBI — Portinari, Tommaso; Portinari, Pigello | https://www.treccani.it/enciclopedia/tommaso-portinari_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/pigello-portinari_(Dizionario-Biografico)/ |
| KB31 | Treccani DBI — Canigiani, Gherardo | https://www.treccani.it/enciclopedia/gherardo-canigiani_(Dizionario-Biografico)/ |
| KB32 | Stella33 — Banco dei Medici notları · The Cecily Group · Zinio/*Medici* · themedicifamily.com | https://stella33.com/en/banco-dei-medici-notes-on-company-organization/ · https://thececilygroup.com/blog/a-case-study-the-medici-succession/ · https://www.zinio.com/publications/medici/35873/issues/461794/articles · https://themedicifamily.com/the-medici-bank |
| KB33 | Cambridge — de Roover: "Francesco Sassetti and the Downfall of the Medici Banking House" (BHR) · "The Decline of the Medici Bank" (JEH) · "The Medici Bank Organization and Management" (JEH) · *Renaissance News* incelemesi (1963) | https://www.cambridge.org/core/journals/business-history-review/article/francesco-sassetti-and-the-downfall-of-the-medici-banking-house/BE6B436969E9FEAD211E9370B813AAA2 · https://www.cambridge.org/core/journals/journal-of-economic-history/article/abs/the-decline-of-the-medici-bank/62FE8FE5810E09274AE0FBDD66E0F867 · https://www.cambridge.org/core/journals/journal-of-economic-history/article/abs/medici-bank-organization-and-management/C479683DE651459ABC23506617FA365E |
| KB34 | Treccani DBI — Giovanni di Bicci; Martino V (DBI/EdP); Bonifacio IX (EdP) | https://www.treccani.it/enciclopedia/giovanni-di-bicci-de-medici_res-0d7a7119-9b6c-11e6-9e53-00271042e8d9_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/papa-martino-v_(Dizionario-Biografico)/ · https://www.treccani.it/enciclopedia/martino-v_(Enciclopedia-dei-Papi)/ · https://www.treccani.it/enciclopedia/bonifacio-ix_(Enciclopedia-dei-Papi)/ |
| KB35 | Britannica — Giovanni di Bicci · Wikipedia — Giovanni di Bicci; Antipope John XXIII · Italy On This Day — Giovanni di Bicci; Baldassare Cossa | https://www.britannica.com/biography/Giovanni-di-Bicci · https://en.wikipedia.org/wiki/Giovanni_di_Bicci_de'_Medici · https://en.wikipedia.org/wiki/Antipope_John_XXIII · https://www.italyonthisday.com/2026/02/giovanni-di-bicci-de-medici-banker.html · https://www.italyonthisday.com/2025/05/baldassare-cossa-antipope.html |
| KB36 | The Cantos Project (Canto XXI kaynakları) — Lorenzo de' Medici, *Ricordi* | https://ezrapoundcantos.org/index.php/canto-17-27-overview/canto-xxi/xxi-sources/309-lorenzo-de-medici-ricordi |
| KB37 | Wikipedia — Palazzo Medici Riccardi | https://en.wikipedia.org/wiki/Palazzo_Medici_Riccardi |
| KB38 | Munro (Toronto) Floransa fiyat-ücret dosyası · Siena WP 928 (Ridolfi–Vasta) · Caferro (Yale), "Florentine Wages at the Time of the Black Death" | https://www.economics.utoronto.ca/munro5/FlorencePricesWages.doc · https://econpapers.repec.org/paper/usiwpaper/928.htm · https://economics.yale.edu/sites/default/files/florence_wages-caferro.pdf |
| KB39 | Palazzo Medici Riccardi mediateca — "La cacciata dei Medici da Firenze" | https://mediateca.palazzomediciriccardi.it/events-and-daily-life/la-cacciata-dei-medici-da-firenze/ |
| KB40 | S. Beck, "Florence, the Medici and Machiavelli" · Specchio dell'epoca (rivstoricavirt) · Storia di Firenze (8 Kas 1494) · Loyalty Binds Me (blog) · Treccani Enciclopedia Machiavelliana — Piero | https://san.beck.org/8-1b-Florence.html · https://www.rivstoricavirt.com/rivstoricavirt_sito/cacciata%20dei%20medici.htm · https://www.storiadifirenze.org/?p=1812 · http://loyaltybindsme.blogspot.com/2012/11/the-expulsion-of-medici.html |
| KB41 | Biblioteca Medicea Laurenziana — Fondi | https://www.bmlonline.it/en/la-biblioteca/fondi-principali/ · http://www.bml.firenze.sbn.it/it/fondi.htm |
| KB42 | Padgett & Ansell (1993) — AcaWiki özeti · Oxford PDF bağlantısı · Princeton bölüm · arXiv (yönlü ağlar) | https://acawiki.org/Robust_action_and_the_rise_of_the_Medici,_1400-1434 · https://www.stats.ox.ac.uk/~snijders/PadgettAnsell1993.pdf · http://assets.press.princeton.edu/chapters/s8767.pdf · https://arxiv.org/pdf/1612.08884 |
| KB43 | Cohn, *Creating the Florentine State* girişi (Cambridge) · Kent, *The Rise of the Medici* (kütüphane kaydı) | https://www.cambridge.org/core/books/abs/creating-the-florentine-state/introduction/D542D437B0C3FBB66216B59BC8D98D3B · https://nantilus.univ-nantes.fr/vufind/Record/PPN006525415 |
| KB44 | Wikipedia — Fugger family; Bindo Altoviti · Economic Forum of the World — Medici, Fugger, Rothschild | https://en.wikipedia.org/wiki/Fugger_family · https://en.wikipedia.org/wiki/Bindo_Altoviti · https://economicforumoftheworld.com/the-medici-fugger-and-rothschild-families/ |
| KB46 | Kirshner–Molho, "The Dowry Fund and the Marriage Market in Early Quattrocento Florence" (Academia) · Avvenire (L. Bruni) · HistoryPlus | https://www.academia.edu/81494869/The_Dowry_Fund_and_the_Marriage_Market_in_Early_Quattrocento_Florence · https://www.avvenire.it/idee-e-commenti/il-mercato-delle-donne-donate-tra-eredita-e-prezzo-sociale_49972 · https://historyplus.net/article/the-medici-how-one-banking-family-bought-the-renaissance/ |
| KB47 | The Timeless Investor (Substack) — Bardi/Peruzzi · Wikipedia — Compagnia dei Bardi | https://thetimelessinvestor.substack.com/p/the-bardi-and-peruzzi-banking-crisis · https://en.wikipedia.org/wiki/Compagnia_dei_Bardi |
| KB49 | O'Brien (2015), *The "Commentaries" of Pope Pius II* incelemeleri | https://www.sfu.ca/history/publications/2015-obrien-pius-II.html · https://49thshelf.com/content/view/full/10580214 |

**Not:** KB45 ve KB48 kullanılmadı (numaralar atlanmıştır: Ferguson için M1'deki **K116**, CLARIAH için **K47** kullanılmıştır). Okunacak ek kitaplar: *Kampf um Florenz. Die Medici im Exil (1494–1512)* (https://dokumen.pub/kampf-um-florenz-die-medici-im-exil-1494-1512-9783412213558-9783412206437.html) ve *Piero di Lorenzo de' Medici and the Crisis of Renaissance Italy* (https://dokumen.pub/piero-di-lorenzo-de-medici-and-the-crisis-of-renaissance-italy-9781108489461-9781108783798-2019038166-2019038167-9781108746571.html) — yalnız listelenmiştir, içerikleri okunmadı.
