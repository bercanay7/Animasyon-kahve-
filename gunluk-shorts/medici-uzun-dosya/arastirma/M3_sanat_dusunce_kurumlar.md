# M3 — SANAT, DÜŞÜNCE, BİLİM, KURUMLAR

**Kapsadığı bölümler:** c4 (Kubbe ve Kefaret) · c5 (Konsil, Kitap, Platon) · c6 (Lorenzo, sanat/şiir yönü) · c10 ve c11 (Savonarola–sanat; Michelangelo/Clemens/Machiavelli, yalnız iskelet) · c12 ve c14 (kurum ve bilim yönü) · c16 (Hesap: "Medici ne yarattı?" tartışması)
**Hazırlayan:** araştırma ajanı M3 · **Tarih:** 18 Ekim 2026 · **Durum:** olgu dosyası (senaryo değil), ana ajan commit edecek
**Okuma kuralı:** Bu dosyada hiçbir satır "kesin" değildir. Her satırın sınıfına bak. Sınıfı **HAFIZA** olan her şey araçla doğrulanmamıştır ve senaryoya girmeden önce doğrulanmalıdır.

---

## 1. Başlık notu: araçlar, sınırlar, okuma kılavuzu

### 1.1 Hangi araçlar çalıştı?

- **WebSearch: çalıştı.** 50 başarılı sorgu (≈36 `standard`, ≈14 kritik konuda `extended`); ardından 4 sorgu kota reddi aldı. Dönenler **arama aracının ürettiği özetlerdir**; sayfa metni bana gelmedi. Özetler zaman zaman kendi içinde çelişiyor veya "bulamadım" diyor; bunları olduğu gibi not ettim.
- **WebFetch: hiç çalışmadı.** Denenen altı sunucunun hepsinde `getaddrinfo ENOTFOUND`: en.wikisource.org, www.gutenberg.org, en.wikipedia.org, archive.org, www.britannica.com, it.wikisource.org. (Ortam proxy belgesini okumaya çalışan bir Bash/curl girişimi güvenlik sınıflandırıcısınca reddedildi; aşılmaya çalışılmadı.)
- **Sonuç: hiçbir sayfa açılıp okunmadı, bu yüzden ● sınıfı kullanılmadı.** "Birincil metin" diye geçen her şey (Vespasiano, Condivi, Vasari, Cosimo'nun mektubu, Rucellai'nin Zibaldone'si…) **arama özetinde alıntılanmış çeviridir**; özgün İtalyanca/Latince çoğu yerde görülemedi. Alıntı sütunundaki "çeviri bize aittir" notu Türkçe karşılıklar içindir; İngilizce metinler başkalarının çevirisidir (çevirmen çoğu yerde doğrulanamadı).
- **WebSearch kotası bitti** (tur başına 200, tüm Medici ajanlarıyla paylaşımlı), Galileo sorgusunda. **Aramasız kalan başlıklar** (ayrıntı §11): Galileo/Sidereus Nuncius, Accademia del Cimento, Peri'nin *Euridice*'si, Cristofori ve piyano, Yeni Sakristi + 1529–30 + Laurenziana merdiveni, Machiavelli, *Assassin's Creed II*, "Medici" dizisi, "Medici etkisi", Boboli, Magi Şapeli, Plethon ayrıntısı, 1492 envanteri, Burckhardt/Kent/Welch'in kendi sözleri. Bunlar yalnızca **HAFIZA (§10)** olarak, güven derecesi ve doğrulama önerisiyle verildi.

### 1.2 Sınıf anahtarı

| Sınıf | Anlam (bu dosyada) |
|---|---|
| ● | Birincil metin gerçekten okundu. **Hiç verilmedi** (WebFetch çalışmadı). |
| ◐ | En az iki bağımsız ikincil kaynakta uyumlu (arama özeti dahil). Kaynak kalitesi düşükse Not sütununda yazıyor. |
| ○ | Tek kaynak ya da doğrulanamayan. |
| ANEKDOT | Sonradan yazılmış/anlatılmış hikâye. Kim yazdı, ne zaman, Not/Güvenilirlik sütununda. |
| HAFIZA | Araçla doğrulanamadı; kendi bilgim. Güven: Y (yüksek) / O (orta) / D (düşük). |

**Kaynak notasyonu:** `K12` gibi etiketler §12'deki **Kaynak anahtarı**na gider (arama sonuçlarında dönen sayfalar). Bir özet birden çok sayfaya dayandığından, hangi cümlenin hangi sayfadan geldiğini ayrıştıramadım; K etiketi "bu konuda dönen sayfalar" demektir.

**Sınıf dağılımı (bu dosya):**
- **Kronoloji (§2), 91 satır:** ◐ 61 (3'ü ANEKDOT, 1'i ◐/○ karma) · ○ 16 (2'si ANEKDOT) · HAFIZA 14 · ● 0.
- **Canlı ayrıntılar (§3), 71 satır:** ◐ 42 (6'sı ANEKDOT) · ◐/○ karma 8 · ○ 21 · ● 0. Bölümlere göre: c4 = 15, c5 = 10, c6 = 18, c10 = 5, c12 = 9 (3'ü c12/c14 ortak), c14 = 10 (3'ü ortak), c16 = 7.
- **§10'da 30 HAFIZA adayı** (hiçbiri doğrulanmadı), **§5'te 22 mit/tartışma girdisi**, **§9'da 15 sağlamlık satırı**.
- **Okuma ipucu:** ◐ burada "iki arama özeti uyumlu" demektir; kaynakların birçoğu Wikipedia, blog ve rehber düzeyinde. Bir olguyu senaryoya almadan önce en az K etiketindeki müze/üniversite/dergi sayfasından (aşağıda işaretli) doğrulamak gerekir.

### 1.3 DÜZELTME / NÜANS listesi (KAPSAM_VE_YAPI.md'ye karşı)

| # | Plandaki ifade | Bulgu | Etiket |
|---|---|---|---|
| D1 | "Kubbe Medici işi değil, Arte della Lana işi: doğrula" | Katedral yapımının Arte della Lana (yün loncası) denetiminde olduğu ve lonca mimari uzmanlığı olmadığı için başmimar aradığı iki özette uyumlu (K1, K3) → **DOĞRULANDI (◐)**. Medici'nin kubbe için karar/finans rolü hiçbir sonuçta çıkmadı (yokluk kanıtı değil, "aramada görülmedi"). Belgeli Medici–Brunelleschi bağı kubbede değil **San Lorenzo Eski Sakristi'sinde** (Giovanni di Bicci, K8). | DOĞRULANDI + sınır |
| D2 | "iskelesiz?" (kubbe) | Kaynaklar **"ahşap kalıpsız (centering yok)"** diyor, "iskelesiz" demiyor; kereste yetmediği için kalıp yapılamadığı bir blogda geçiyor (K5, K6; düşük kalite). "İskelesiz" demek yanlış olur. | DÜZELTME |
| D3 | "Palazzo Medici 1444–" | 1444 yaygın başlangıç yılı; Floransa Üniversitesi makalesi (Ferretti, K9) **1445 başı** ve Mart 1445 tarihli köşe arsayı temizleme mektubunu işaret ediyor. | NÜANS |
| D4 | "Lascaris'in Doğu seferi (1491–92)" | Speake (K25): **iki ayrı yolculuk, 1490 ve 1491**; Athos ziyareti ikincisinde (1491). Dönüş 1492 (Wikipedia özeti). Tek sefer gibi anlatılmaz. | NÜANS |
| D5 | "Medici Doğu Dilleri Matbaası (1584)" | **Roma'da** kuruldu (Floransa'da değil); XIII. Gregorius'un desteği, Kardinal Ferdinando'nun yönetimi (K46). "Floransa'nın matbaası" denmemeli. | NÜANS |
| D6 | "Donatello David'i, Medici avlusu" | Avluda **1469**'da anıldığı ◐; sipariş belgesi yok; tarih 1420'ler–1460'lar arası. Lorenzo–Clarice düğünü bağı **aramada çıkmadı**. | NÜANS |
| D7 | "Michelangelo, Lorenzo'nun sarayında büyüdü" | Anlatı **Condivi'ye (1553)** ait ve Michelangelo ≈15 yaşındayken hane içine alınma biçiminde; "büyüdü" değil. Condivi'de Bertoldo/antikalar geçmiyor, bu ayrıntılar Vasari'nin genişletilmiş baskısından (K36, tek özet). | NÜANS |
| D8 | "İtalyanca standardı Medici'den" | Yazı dili standardının kökeni **Bembo (*Prose*, 1525)** ve Salviati/Crusca (1583; *Vocabolario* 1612); Lorenzo/Poliziano'nun payı prestij (Raccolta Aragonese). | NÜANS |
| D9 | Medici Doğu Matbaası ve Osmanlı | III. Murad'ın Ekim 1588 fermanı bir **yasak değil, ticaret koruması** (K46). "Osmanlı matbaayı yasakladı"yı bu belgeyle desteklemek yanlış olur. | NÜANS |
| D10 | Bir özetin "Arapça İncil 1588'de Lübnan'a ithal edildi" cümlesi | Arapça İncil baskısı 1590–91; 1588 ithalatı başka bir kitap olmalı ya da özet hatalı. **Kullanma.** | UYARI |
| D11 | "Giostra" | **1475** Giostra'sı Giuliano'nun (kazanan). Lorenzo'nun kendi turnuvası 1469'dur (HAFIZA, Y); karıştırılmamalı. | NÜANS |
| D12 | Rucellai'nin "elli yıl kazandım, harcadım" sözü | Bir özet bunu Cosimo'ya atfetti, diğeri **Rucellai'ye (Zibaldone)**; Rucellai'ye ait kabul edilir (K14). Atıf karışıklığı tuzağı. | UYARI |

---

## 2. Kronoloji

Sınıf sütunu: ◐ / ○ / HAFIZA (+ ANEKDOT). K etiketleri §12'de.

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|---|
| 1 | c4 | (tarihsiz) | Katedralin yapım idaresi (Opera di Santa Maria del Fiore) Arte della Lana'nın denetiminde; lonca mimari uzmanlığı olmadığı için başmimar (capomaestro) atıyor | ◐ | K1, K3 | HAFIZA: devir 1331 (O); aramada tarih çıkmadı |
| 2 | c4 | 19 Ağu 1418 | Opera del Duomo kubbe için model/tasarım yarışması ilan etti; kullanılan model için 200 altın florin ödül; teslim Eylül sonuna | ◐ | K1, K3, K4 | Bir kaynak 18 Ağu diyor |
| 3 | c4 | 1418–1419 | Ghiberti ve yardımcıları model sundu; üç model yetkilileri ikna etmedi | ○ | K1 | Tek özet |
| 4 | c4 | Bahar 1420 | Brunelleschi'nin tasarımı seçildi; Brunelleschi ve Ghiberti birlikte denetçi; usta duvarcı Battista d'Antonio (belgeli 1420–39) | ◐ | K1, K3 | "Jüri berabere kaldı, kazanan Ghiberti" diyen blog güvenilmez bulundu (özet) |
| 5 | c4 | 1419–1428 | Giovanni di Bicci'nin parasıyla Brunelleschi'nin San Lorenzo Eski Sakristi'si; Giovanni ve eşi orada gömülü | ◐ | K8 | Başlangıç 1419 (bir kaynak); HAFIZA: 1421 (O). Patronaj sonra oğulları Cosimo ve Lorenzo'ya geçti |
| 6 | c4 | 1420–1436 | Kubbe: iç kabuk hafif tuğla, balıksırtı dizili; dış kabuk daha kalın, taş ve kiremit kaplı; **ahşap kalıp (centering) kullanılmadı** | ◐ | K5, K6 | Kaynaklar rehber/blog düzeyinde; bir özet kabukların malzemesinde çelişki gördü. "İskelesiz" denmez (D2) |
| 7 | c4 | 25 Mar 1436 | Eugenius IV katedrali kutsadı (Floransa takvimine göre yılbaşı); Dufay'ın *Nuper rosarum flores* motetinin bu tören için yazıldığı kabul edilir | ◐ | K7 | Wikipedia + DIAMM PDF + başka özetler |
| 8 | c4 | Ağu 1436 (≈5 ay sonra) | Kubbenin tamamlanışı ve ayrı bir kutsama (Benozzo Federighi, atanmış başpiskoposun yerine) | ○ | K7 | Tek özet |
| 9 | c4 | 1434–1436 (özet) | Cosimo, sürgünden dönünce San Marco'yu Fiesole Dominikenleri için yeniden yaptırdı; duvarlar için Fra Angelico | ○ | K11 | Özetin tarih dizilişi şüpheli; HAFIZA: Eugenius IV'ün devri 1436, inşaat 1437–52 (O). Doğrula |
| 10 | c4 | 1437 (HAFIZA) | Niccoli borçlu öldü; vasiyetinde kitaplık halkın kullanımına; 16 curator, Cosimo da biri; Cosimo borçları üstlenip 800 el yazmasının denetimini aldı (≈6.000 florin); kitaplar San Marco'ya | ◐ | K15 | Ölüm yılı HAFIZA (Y); içerik ◐ |
| 11 | c4 | c.1441–42 | San Marco hücre 39: *Magi'lerin Hayranlığı* freski; Fra Angelico mu Gozzoli mi tartışmalı | ◐ | K11 | Atıf: Angelico (Pope-Hennessy) / Gozzoli |
| 12 | c4 | 6 Oca 1443 | Eugenius IV yeni San Marco kilisesini kutsarken Cosimo'nun hücresinde geceledi | ○ | K11 | Tek özet (Wikipedia "Cosimo's cell") |
| 13 | c4 | 1444 (yaygın) / 1445 başı (belge) | Palazzo Medici (Michelozzo, Via Larga); belgelere göre kampanya 1445 başında, Mart 1445 mektubu köşe arsanın temizlenmesini anlatıyor | ◐ (1444 yaygın) / ○ (1445) | K9 | NÜANS (D3). Brunelleschi'nin daha görkemli modelinin reddi = Vasari'ye bağlanan, belgesiz gelenek |
| 14 | c4 | 1420'ler–1460'lar | Donatello'nun bronz *David*'i: çoğunluk 1440'lar; Smarthistory 1430'ların sonu–1440'lar, 1450'lerin başında tamam | ◐ | K10 | Sipariş belgesi yok; çoğunluk Cosimo, azınlık Piero (1460'lar) |
| 15 | c4 | 1469 | Bronz *David* Medici Sarayı avlusunda: ilk güvenli anılış | ◐ | K10 | Düğünle bağ aramada çıkmadı (D6) |
| 16 | c4 | 1436 (bir kaynak 1435) | Felice Brancacci Medici karşıtı olarak sürgüne; Brancacci Şapeli'nde aileyle ilişkili portreler Karmelitlerce silindi | ◐ | K20 | Masaccio 1427'de Roma'ya gitti, 1428'de öldü, döngü yarım kaldı |
| 17 | c4 | 1460; 1481–83 | Şapel "Halkın Meryemi"ne adandı; Filippino Lippi silinen yerleri onarıp döngüyü bitirdi | ◐ | K20 | |
| 18 | c4 | 1446–51 / 1453 | Palazzo Rucellai: Alberti tasarımı, Rossellino uygulaması ("büyük olasılıkla"); sekiz evin yerine tek saray | ◐ | K14 | Tarih ve atıf kesin değil |
| 19 | c4 | 1457'den | Giovanni Rucellai *Zibaldone*'sini yazmaya başladı (aile tarihi, sanat patronajı kaydı, ahlak) | ◐ | K14 | |
| 20 | c4 | 1 Eyl 1485 | Giovanni Tornabuoni–Ghirlandaio sözleşmesi (Santa Maria Novella ana şapeli); iş Mayıs 1486'da başlayıp 4 yılda bitecekti; şapel 22 Ara 1490'da yeniden açıldı | ◐ | K19 | Orcagna'nın eski fresklerinin hakkı Ricci'deydi, Tornabuoni onlardan aldı |
| 21 | c4 | 1480'ler | Sassetti Şapeli (Santa Trinita, Ghirlandaio): Sassetti'nin S. Maria Novella'daki hakkı kaybedilince iş Santa Trinita'ya taşındı | ◐ | K19 | Kesin yıllar HAFIZA (1483–85, O) |
| 22 | c5 | 1342 | Barlaam, Petrarca'ya Rumca temellerini öğretti | ○ | K27 | Tarih zayıf kaynakta (Scribd); Wikipedia listesi Barlaam'ı (c.1290–1348) anıyor |
| 23 | c5 | 1396/97 | Chrysoloras Floransa'da Rumca ders vermeye başladı (Salutati'nin daveti); *Erotemata* | ◐ | K27 | Yıl 1396 veya 1397 |
| 24 | c5 | Oca 1417 | Poggio Lucretius'u buldu (büyük olasılıkla Fulda); kopya Floransa'da Niccoli'ye gönderildi | ◐ | K28 | Yer "muhtemelen" |
| 25 | c5 | Şub–yaz 1439 | Konsil Ferrara'dan Floransa'ya taşındı: masraf yükü, veba korkusu, Cosimo'nun teşviki/Floransa'nın Rum heyeti masraflarını üstlenme teklifi | ◐ | K23 | Ay ve neden kaynaklar arasında ayrışıyor; Medici payı "tek neden" değil |
| 26 | c5 | 5/6 Tem 1439 | Birlik kararı (*Laetentur caeli*); ≈700 Doğu heyeti | ◐ | K23 | 5 veya 6 Temmuz |
| 27 | c5 | 1438–39 → 1492 | Plethon'un Platon üzerine söylevleri; Floransalılar ona "ikinci Platon" dedi; **Ficino'ya göre** Cosimo'nun "Akademi" fikri bu dinlemeden doğdu | ◐ ANEKDOT | K22 | Ficino'nun geriye dönük anlatımı (HAFIZA: 1492 Plotinos önsözü, O) |
| 28 | c5 | 1453 | İstanbul düştü; Konsil'de vaat edilen Batı yardımı gelmedi | ◐ | K23 | |
| 29 | c5 | 1470; 1484; 1492 | Ficino Platon çevirisini 1470'te bitirdi, 1484'te basıldı; Plotinos 1492 | ○ | K22 | Tek özet |
| 30 | c5 | 1462 (gelenek) / 1463 | Cosimo, Ficino'ya Platon el yazmaları ve Careggi civarında ev/mülk verdi: "Akademi"nin geleneksel merkezi | ◐ | K21, K22, K24 | Yıl 1462/1463; yer Careggi mi, Montevecchio mu ayrışıyor |
| 31 | c5 | 1463 civarı | Cosimo'dan Ficino'ya mektup: Careggi'ye gel, Platon'un "En Yüksek İyi" kitabını (*Philebus*) ve Orfik lirini getir | ◐ | K24 | Philebus teşhisi cilt editörünün notu; editör çeviri talebini 1463'e bağlıyor, mektubun kendi tarihi kesin değil; Latince metin görülmedi |
| 32 | c5 | 1490 ve 1491 | Lascaris iki Doğu yolculuğuna çıktı: el yazması toplamak ve II. Bayezid ile satın alma pazarlığı | ◐ | K25 | NÜANS (D4) |
| 33 | c5 | 1491 | Lascaris Athos'ta | ◐ | K25 | Cep defteri Vat. gr. 1412 |
| 34 | c5 | 1492 | Lascaris Floransa'ya ≈200 el yazmasıyla döndü; sonra Fransız krallara hizmet (Blois kütüphanesi 1496, Fontainebleau 1524) | ◐ | K25 | 200 sayısı: "Yunanistan'dan" (Lascaris, Speake) / "Athos'tan" (Wikipedia) |
| 35 | c5 | 1494 | Medici sürgünü: Cosimo'nun koleksiyonuna Signoria el koydu, San Marco kütüphanesine kattı | ◐ | K26 | |
| 36 | c5 | 1508 | Kardinal Giovanni (X. Leo) kitapları Dominikenlerden geri alıp Roma'ya, Palazzo Madama'ya götürdü | ◐ | K26 | Bir kaynak: Vatikan parasıyla geri alındı |
| 37 | c5 / c11 | 1523 veya 1524 | VII. Clemens Michelangelo'ya Laurenziana binasını ısmarladı | ◐ | K26 | 1523/1524 ayrışıyor |
| 38 | c5 / c11 | 1558; 1571 | Bina tamamlandı; kütüphane halka ilk kez açıldı | ◐ | K26 | Bir kaynak: 1571'de hâlâ eksikti |
| 39 | c6 | 1465–1472 | Verrocchio'nun San Lorenzo'daki Cosimo, Piero ve Giovanni mezarları | ◐ | K31 | |
| 40 | c6 | 1470'ler | Verrocchio atölyesi: Leonardo, Perugino, Botticelli, Ghirlandaio, Lorenzo di Credi vb. | ◐ | K31 | Atıflar zor |
| 41 | c6 | Oca 1475 | Giostra: Piazza Santa Croce; Giuliano kazandı, Simonetta Vespucci'yi güzellik kraliçesi ilan etti; Botticelli sancağı | ◐ | K39 | Floransa–Milano–Venedik ittifakı bağlamı |
| 42 | c6 | Nis 1476 | Simonetta Vespucci öldü (verem; doğum ≈1453) | ◐ | K39 | Giuliano'yla sevgili miydi: bilinmiyor |
| 43 | c6 | 1476–77 | Raccolta Aragonese: Lorenzo ve Poliziano'nun Toskana şiir antolojisi, Napoli'den Federico d'Aragona'ya | ◐ | K38 | Wikisource'un "1465"i hatalı görünüyor |
| 44 | c6 | c.1477–82 | *Primavera*; **1499 envanterinde** Lorenzo di Pierfrancesco'nun Floransa'daki şehir sarayında; Vasari ikisini Castello'da gördü | ◐ | K29 | Tarih 1481/82 de öneriliyor |
| 45 | c6 | 1482 | Lorenzo di Pierfrancesco–Semiramide Appiani evliliği; *Primavera* ile bağ **kesin değil** | ◐ | K29 | |
| 46 | c6 | 21 Tem 1478 | Sekizler Konseyi kaydı: Botticelli'ye "hainleri resmetmek" için 40 florin | ○ | K30 | Milanesi 1862'den aktarılmış; özgün görülmedi |
| 47 | c6 | 1480 | Lorenzo di Credi, annesi Lisa'nın vergi beyanına göre Verrocchio atölyesinde yılda 12 florin | ○ | K31 | Tek özet |
| 48 | c6 / c8 | c.1480–81 | Bertoldo'nun II. Mehmed madalyonu (tek imzalı madalyonu); Lorenzo'nun siparişi "olası" | ◐ | K47 | TR-BAĞ |
| 49 | c6 | c.1482 | Leonardo'nun Milano'ya gidişi; "Lorenzo gümüş lirle gönderdi" rivayeti | ○ ANEKDOT | K33 | Leonardo'nun Ludovico'ya mektubu (Codex Atlanticus) ağırlıkla askerî mühendislik |
| 50 | c6 | 1489–1492 (HAFIZA) | Michelangelo ≈15 yaşında San Marco bahçesinde/Medici hanesinde: Faun başı anekdotu | ◐ ANEKDOT | K34, K36 | Anlatan Condivi 1553; yıllar HAFIZA (O) |
| 51 | c6 | (tarihsiz) | Torrigiani'nin Michelangelo'nun burnunu kırması | ◐ ANEKDOT | K35 | Cellini (Torrigiani'den dinlediği) / Vasari farklı |
| 52 | c6 | 1490 | *Canzona di Bacco* (*Trionfo di Bacco e Arianna*): 1490 Karnavalı için | ◐ | K37 | "Genellikle 1490" |
| 53 | c10 | 7 Şub 1497 | Kibirlerin Yakılması, Piazza della Signoria | ◐ | K41 | |
| 54 | c10 | 1497 → | "Botticelli kendi resimlerini yaktı" iddiasının çağdaş kanıtı yok; Vasari bunu anlatmıyor; 1498 sonrası tarihli eserleri var | ◐ | K41 | |
| 55 | c12 | 1541 | Cosimo I Accademia Fiorentina'yı kararnameyle tanıdı, dilin kurallarını yazıya dökme görevini verdi | ○ | K45 | Tek özet; HAFIZA: Umidi 1540 (O) |
| 56 | c12 | 1560 | Cosimo I, Vasari'ye Floransa'nın dağınık 13 magistratura'sı için ofis binası (Uffizi) tasarlattı | ◐ | K42 | "Uffizi" = ofisler |
| 57 | c12 | 12–13 Oca 1563 | Accademia delle Arti del Disegno kuruldu (Cosimo I, Vasari, Borghini) | ◐ | K43 | Kuruluş metni 12 Oca'da Cosimo'ya sunuldu |
| 58 | c12 | 31 Oca 1563 | İlk oturum, Angeli manastırı toplantı salonu | ○ | K43 | Tek özet (Storia di Firenze) |
| 59 | c12 | 10 Mar 1564 | Michelangelo'nun cesedi Roma'dan Floransa'ya "mal gibi" gizlice getirildi rivayeti | ○ ANEKDOT | K44 | Popüler anlatım; arte.it sergisinin adı da bunu anıyor |
| 60 | c12 | 14 Tem 1564 | Michelangelo'nun görkemli cenaze töreni, San Lorenzo; Accademia düzenledi; Varchi orasyonu | ◐ | K44 | Basılı kapakta 28 Haziran yazmasına rağmen tören 14 Temmuz |
| 61 | c12 | 1565 | Vasari Koridoru (Palazzo Vecchio–Pitti) | ◐ | K42 | "5 ay" ve "düğün için" HAFIZA |
| 62 | c12 / c14 | 1570–75 | Francesco I'in studiolo'su (Palazzo Vecchio): Vasari, Borghini, Adriani | ◐ | K48 | Wikipedia 1570–72, çoğu kaynak 1575 |
| 63 | c12 / c14 | c.1575 | Medici porseleni: Francesco kimyagerlere formül buldurdu; Batı'nın ilk "vitreous paste" porselenleri | ○ | K48 | Tek özet; 1587 bitişi doğrulanamadı |
| 64 | c12 | 1580/81 | Uffizi'nin yapımı Buontalenti'ce bitirildi; 1581'de Francesco I Tribuna'da özel koleksiyon kurdu | ◐ | K42 | Bitiş 1580 veya 1581 |
| 65 | c12 | 1583 | Accademia della Crusca (Salviati); *Vocabolario* 1590'da başladı, 1612'de Venedik'te basıldı | ◐ | K45 | Bir kaynak 1582 |
| 66 | c14 | 1584 | Medici Doğu Matbaası, **Roma**; XIII. Gregorius; Kardinal Ferdinando; yönetici Giovanni Battista Raimondi; Arapça harfler Robert Granjon | ◐ | K46 | D5 |
| 67 | c14 | 1588 | Opificio delle Pietre Dure (Ferdinando I); ilk yerleşim Uffizi doğu kanadındaki Galleria dei Lavori | ◐ | K49 | |
| 68 | c14 | Eki 1588 | III. Murad'ın fermanı: Arapça/Farsça basılı kitap ithal eden iki Avrupalı tüccarı (Branton ve Orazio Bandini) korur; ferman 1594 Medici Öklid baskısının arkasında | ◐ | K46 | TR-BAĞ. Yasak değil, koruma |
| 69 | c14 | 1590–91; 1593; 1594 | Arapça-Latince İncil; İbn Sina *Kanun*; Öklid (Tusî çevirisi) | ◐ | K46 | |
| 70 | c14 | 1610'a dek | Raimondi, Granjon harfleriyle yalnızca 8 eser bastı | ○ | K46 | Açık artırma kaydı |
| 71 | c14 | 1808 | Napoléon matris ve zımbaların Paris'e getirilmesini emretti | ○ | K46 | |
| 72 | c16 | 1769 (bir kaynak 1765) | Uffizi resmen halka açıldı (Peter Leopold) | ◐ | K42 | Resmî Uffizi sitesi 1769 |
| 73 | c16 | 1920 | Studiolo'nun özgün düzene yakın yeniden kurulmasına karar | ○ | K48 | |
| 74 | c16 | 1975 | OPD, restorasyon laboratuvarıyla birleşti; bugün Kültür Bakanlığı'na bağlı özerk enstitü | ◐ | K49 | "Kurum bugüne uzanıyor" |
| 75 | c16 | 1960; 1993; 1998 | Tartışma çizgisi: Gombrich "Early Medici as Patrons" (1960); Goldthwaite (1993); Gombrich–Kempers NYRB tartışması (1993); *With and Without the Medici* (1998) | ◐ | K17, K18 | Yazarların kendi sözleri okunmadı |
| 76 | c16 | 1990; 1991; 2002 | Hankins: "Cosimo and the 'Platonic Academy'" (1990); "Myth of the Platonic Academy" (RQ 1991); "Invention of the Platonic Academy" (2002) | ◐ | K21 | 1991 makalesinin tezi ◐; 1990 yazısının özeti ◐; 2002 yazısının yalnız başlığı görüldü |
| 77 | c16 | 2000 | Barzman, Accademia del Disegno'nun pedagojik rolünü Pevsner'e karşı savunur | ◐ | K43 | CAA incelemesi |
| 78 | c11 | 1513 (Tem–Ara) | Machiavelli *Prens*'i yazar; 10 Ara 1513 tarihli Vettori mektubu | HAFIZA | — | Y. Doğrula |
| 79 | c11 | 1516 | *Prens*'in Lorenzo di Piero'ya (Urbino Dükü) ithafı (ilk niyet Giuliano) | HAFIZA | — | Y/O |
| 80 | c11 | 1519–1520 | Kardinal Giulio de' Medici Yeni Sakristi'yi ısmarlar; Michelangelo 1520'de başlar | HAFIZA | — | Y |
| 81 | c11 | 1520 (Kas) | Kardinal Giulio, Machiavelli'ye *Istorie fiorentine*'yi ısmarlar; 1525/26'da VII. Clemens'e sunulur | HAFIZA | — | Y/O |
| 82 | c11 | 6 Nis 1529 | Michelangelo Cumhuriyet'in istihkâm genel sorumlusu (San Miniato) | HAFIZA | — | Y/O |
| 83 | c11 | Eyl 1529 | Michelangelo Floransa'dan Venedik'e kaçar; Kasım'da döner | HAFIZA | — | O |
| 84 | c11 | 12 Ağu 1530 | Floransa teslim olur; Michelangelo saklanır, VII. Clemens affeder | HAFIZA | — | Y/O. 1975 gizli oda keşfi: O |
| 85 | c12 | 1549–50 | Eleonora di Toledo Pitti'yi satın alır; Boboli'nin yapımı (Tribolo) başlar; 1766'da halka açılır | HAFIZA | — | O |
| 86 | c14 | 6 Eki 1600 | Peri–Rinuccini *Euridice*, Pitti Sarayı; Maria de' Medici–IV. Henri evliliği | HAFIZA | — | Y |
| 87 | c14 | 7–13 Oca 1610; Mar 1610 | Galileo Jüpiter uydularını gözler; *Sidereus Nuncius* Cosimo II'ye ithaflı, "Medicea Sidera" | HAFIZA | — | Y |
| 88 | c14 | 1610 yazı | Galileo "Granduka'nın matematikçisi ve filozofu" unvanıyla Floransa'ya | HAFIZA | — | Y (maaş: D) |
| 89 | c14 | 1657–1667 | Prens Leopoldo'nun Accademia del Cimento'su; *Saggi di naturali esperienze* 1667 | HAFIZA | — | Y |
| 90 | c14 | 1700; 1711 | Prens Ferdinando'nun envanterinde Cristofori'nin "piano e forte" klavyesi; Maffei'nin 1711 makalesi | HAFIZA | — | Y/O |
| 91 | c16 | 2004; 2009; 2016–19 | Johansson *The Medici Effect*; *Assassin's Creed II*; "Medici: Masters of Florence" dizisi | HAFIZA | — | Y/O |

---

## 3. Canlı ayrıntılar

Tablo: `# | Bölüm | Ayrıntı | Kim yazdı / ne zaman (olaydan sonra mı?) | Güvenilirlik | Birebir alıntı`. Alıntıların **İngilizce kısmı arama özetinde başkasının çevirisi olarak göründü** (orijinal İtalyanca/Latince çoğu yerde görülmedi); Türkçe karşılıklar **bize aittir**. "Birebir yok" yazan yerde özet yalnızca dolaylı aktarım verdi, uydurma tırnak konmadı.

### 3.1 c4: Kubbe ve Kefaret

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| 1 | c4 | Cosimo, para yüzünden vicdanındaki yükü atmak için o sırada Floransa'da bulunan Papa Eugenius IV'e danışır. | Vespasiano da Bisticci, Cosimo'nun yaşamı (Bamberg çalışması ≈1495 diyor; Cosimo'nun 1464 ölümünden ≈30 yıl sonra). Övgücü, "çoğunluğun Cosimo'yu gördüğü gibi" çizen bir yazı. | ◐ ANEKDOT | EN (Vespasiano çevirisi, Uppsala sayfası, K12): "Wanting to lift this weight from his shoulders, he went to talk to Pope Eugenius who was then in Florence." / TR: "Bu yükü omuzlarından atmak isteyerek, o sırada Floransa'da bulunan Papa Eugenius'la konuşmaya gitti." |
| 2 | c4 | Papa, Observant Dominikenlerin San Marco'sunu yaptırmasını ve 10.000 florin harcamasını önerir; Cosimo işi bitirmek için toplamda 40.000'den fazla harcar. Sayılar **florin**, "duka" değil. | Aynı metin | ◐ ANEKDOT | EN: "Having spent ten thousand florins without completing what was necessary, Cosimo finished the job by spending in all more than forty thousand florins" / TR: "On bin florin harcanmıştı ama gereken iş bitmemişti; Cosimo işi tamamlamak için toplamda kırk bin florinden fazlasını harcadı." |
| 3 | c4 | Vespasiano'ya göre Cosimo, devlet yöneten çoğu insan gibi vicdanında epeyce şey biriktirmişti; kilise bağışları Tanrı'nın merhametini ummakla bağlantılıydı. | Vespasiano, Bamberg çalışmasının aktarımıyla | ○ | Birebir yok. Özette dolaylı: "accumulated quite a bit on his conscience, as most men do who govern states". Vespasiano'nun kendi kelimeleri görülmedi. |
| 4 | c4 | "Günah, faiz, bağış" zinciri: bir deneme ve bir akademik makale, Kilise doktrininde bankacının tefecilikle suçlu sayıldığını, bağışlanmanın yolunun hayır ve özellikle kiliseye patronaj olduğunu savunuyor ("magnificence" doktrini ayrıca aranmadı). | Modern yorum (italianrenaissanceresources denemesi; SciELO makalesi "God, Power and Money: Did Cosimo de' Medici Deceive Renaissance Florence?") | ◐ YORUM | Birebir yok (özet parafrazı). |
| 5 | c4 | San Marco'da Cosimo'nun iki hücresi var: özel inziva ve önemli konuklar için. Dominiken olmadığı hâlde bağışı nedeniyle hakkı oldu. Eugenius IV 6 Oca 1443'te yeni kiliseyi kutsarken orada geceledi. | Wikipedia "Cosimo de' Medici's cell" özeti | ◐ (hücre) / ○ (Papa'nın gecelemesi) | Birebir yok. |
| 6 | c4 | Hücre 39'daki Magi freskinde kralların taçlarını yemliğin önüne bırakışı; Cosimo bunu hükümdar olarak kendi yönlendirmesi için hep gözünün önünde istedi (1929 tarihli kaynak). Epifani Medici'nin sevdiği temaydı. | 1929 tarihli yayın (Heidelberg dijital: Singleton) | ○ | Birebir yok. |
| 7 | c4 | Niccoli'nin kitapları: 800 el yazması (kaynaklar "cilt" de diyor), ≈6.000 florin; vasiyette halkın kullanımı; 16 curator; Cosimo borçları üstlenmesi karşılığı koleksiyonun denetimini aldı. | Ullman & Stadter 1972'ye atıf yapan kataloglar; Chalmers biyografi sözlüğü | ◐ | Birebir yok. |
| 8 | c4 | **Yumurta anekdotu:** rakipler yumurtayı mermere dik duramaz; Filippo tabanını kırıp diker; "biz de yapardık" itirazına, planı görselerdi kubbeyi de yapmayı bilirlerdi diye karşılık verir. Çağdaş kayıt bulunamadı. | Vasari (1550/1568, olaydan ≈130 yıl sonra). Brunelleschi'nin çağdaşları kubbe biter bitmez onu efsaneleştirdi (The Critic, Trachtenberg incelemesi). | ANEKDOT ○ | Birebir yok (özet parafrazı). Vasari metni okunmadı. |
| 9 | c4 | Kutsama günü (25 Mart 1436, Floransa yılbaşı): Dufay'ın motetinin iki tenorunda kutsama introitinin ezgisi var; Papa'nın özel korosu söyledi; metinde "altın gül" geçer. | Dufay'ın müziği 1436 çağdaşı; DIAMM ve Wikipedia özetleri | ◐ | Latin (ezgi adı, özetten): "Terribilis est locus iste" / TR: "Ne heybetli bu yer." |
| 10 | c4 | **Rucellai'nin itirafı:** elli yıl hep kazanıp harcamış; harcamanın kazanmaktan daha tatlı olduğunu öğrenmiş. (Bir özet bunu yanlışlıkla Cosimo'ya atfetti, bkz. D12.) | Giovanni Rucellai, *Zibaldone* (1457'den, kendi eliyle, yaşarken yazıldı) | ◐ | EN: "For fifty years I have done nothing but earn money and spend it; in so doing I have learned that I enjoy spending money more than earning it." / TR: "Elli yıldır para kazanıp harcamaktan başka bir şey yapmadım; bu arada harcamaktan, kazanmaktan daha çok zevk aldığımı öğrendim." |
| 11 | c4 | Rucellai sarayı için: tek saray, sekiz evin yerine; sonradan yapılan keşif sekiz konutun varlığını doğruladı. | Rucellai'nin kendi tanıklığı (özet) | ○ | EN: "out of eight houses, I made one" / TR: "sekiz evden bir tane yaptım" |
| 12 | c4 | Brancacci'nin sürgünü (Medici karşıtlığı) sonrası Karmelit rahipler, şapeldeki ailesiyle ilişkili portreleri sildi; Filippino Lippi 1481–83'te silinen yerleri onardı. Siyaset freskin yüzünü kazıdı. | Şapel broşürü (Floransa Belediyesi), Finestre sull'Arte, The Florentine | ◐ | Birebir yok. |
| 13 | c4 | Tornabuoni şapeli: Vasari'ye göre fiyat 1.200 altın duka, iş beğenilirse 200 daha. Sözleşme tarihi (1 Eyl 1485) ve süre (4 yıl) British Museum'un notunda. | Vasari (1550/68, ≈65–80 yıl sonra); sözleşme bilgisi British Museum | ◐ | EN (Fordham Vasari özeti, K19): "the price to be twelve hundred ducats of gold, and if the work pleased him two hundred more" / TR: "fiyat bin iki yüz altın duka olacak, iş hoşuna giderse iki yüz daha." (Aramada "1.100 florin" doğrulanmadı.) |
| 14 | c4 | Fra Filippo Lippi'nin Prato'daki rahibe Lucrezia Buti'yi Sacra Cintola alayında kaçırması Vasari'nin hikâyesi; arşiv belgeleriyle doğrulanmış. Cosimo'nun müdahalesiyle evlilik izni alındı. "Cosimo Lippi'yi çalışsın diye odaya kilitledi, çarşafı ip yapıp kaçtı" hikâyesi kaynaksız bir Wikipedia türevinde geçiyor. | Vasari; modern arşiv doğrulaması (kaçırma) | ◐ (kaçırma, belgeli) / ○ ANEKDOT (kilitleme) | Birebir yok. |
| 15 | c4 | Giovanni di Bicci'nin ölüm sonrası "yatırımı": Eski Sakristi'ye eşiyle gömüldü; bir makale, böyle bir yerde gömülmenin ölünün ruhuna sağladığı faydaları inceliyor. | Modern makale (Artibus et Historiae no. 32 civarı, K8) | ◐ | Birebir yok. |

### 3.2 c5: Konsil, Kitap, Platon

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| 16 | c5 | **Cosimo'nun Careggi mektubu.** Bahçe işi için değil zihin işi için geldiğini yazar; Ficino'dan Platon'un "En Yüksek İyi" kitabını (*Philebus*) ve Orfik lirini getirmesini ister. | Cosimo → Ficino, 1463 civarı (cilt editörü, Philebus çevirisi talebini 1463'e bağlıyor; mektubun kendi tarihi kesin değil); Ficino'nun mektup derlemesinde, yani Ficino'nun elinden geçmiş. Cosimo 1464'te öldü, yaklaşık bir yıl önce. | ◐ | EN#1: "Yesterday I arrived at my Careggi estate, to cultivate not this place, but my mind." / TR: "Dün Careggi'deki mülküme geldim; burayı değil, zihnimi işlemek için." EN#2: "Join us, and bring your Orphic lyre" / TR: "Bize katıl ve Orfik lirini getir." EN#3: "Farewell, and come—and do not forget your Orphic lyre." / TR: "Hoşça kal; gel, ve Orfik lirini unutma." (Çevirmenler farklı; Latince görülmedi.) |
| 17 | c5 | Cosimo'nun Ficino'ya hediyesi: Platon'un tüm eserlerinin bir el yazması, Floransa'da bir ev ve Careggi'deki villasının yakınında bir ev/villa. | Hankins (1990) özetinin Wikipedia aktarımı; tarih 1462 (gelenek), başka bir kaynak 1463 diyor | ◐ | EN: "a manuscript of the complete works of Plato, a house in Florence, and a house (in some versions a villa) near his own villa at Careggi" / TR: "Platon'un bütün eserlerinin bir el yazması, Floransa'da bir ev ve kendi Careggi villasının yakınında bir ev (bazı anlatımlarda villa)." |
| 18 | c5 | "Akademi" tartışması: topluluğun tüzüğü ve üye kaydı yoktu; çağdaş kanıt "Platon Akademisi" adını göstermiyor; Hankins'e göre Ficino'nun "academy"si özel ders ortamıydı. | Hankins, *Renaissance Quarterly* 44/3 (1991), s. 429–475; özetler | ◐ | EN: "It was never a formal body – it had no statutes and kept no records of membership" (Wikipedia özeti) ve "a gymnasium for private tuition of arts students" (Hankins'in kendi özeti) / TR: "Hiçbir zaman resmî bir yapı olmadı; tüzüğü yoktu, üye kaydı tutmadı." ve "sanat öğrencilerine özel ders veren bir gymnasium." |
| 19 | c5 | Plethon: Floransa hümanistlerinin ona "ikinci Platon" dediği, Cosimo'nun Platon heyecanını Konsil sırasında Plethon'un söylevlerinin uyandırdığı hikâyesi **Ficino'dan** geliyor (geriye dönük). | Ficino, sonradan | ◐ ANEKDOT | EN: "...named him the second Plato" / TR: "ona 'ikinci Platon' adını verdiler"; EN: "According to Ficino, the academy was founded by Cosimo de' Medici because his enthusiasm for Plato had been aroused by the lectures of Gemistus Pletho at the time of the Council of Florence (1438)." / TR: "Ficino'ya göre akademi, Cosimo'nun Platon heyecanını Floransa Konsili sırasında Gemistos Plethon'un derslerinin uyandırması üzerine kuruldu." |
| 20 | c5 | Konsil'in maliyeti: yaklaşık 700 kişilik Doğu heyeti; Papa ödemelerde geride; Milano birliklerinin tehdidi; Cosimo'nun teklifi. | Modern anlatımlar (Wisconsin dijital "A History of the Crusades" sayfası, K23) | ○ | Birebir yok (özet parafrazı). |
| 21 | c5 | Vaat edilen yardım hiç gelmedi: Konsil Doğu için "Türk tehdidi" gerekçesiyle toplandı; 1453'te şehir düştü. | Modern tarih anlatımı | ◐ | EN: "Nor did any of the vaguely promised aid against the Turks ever arrive from Italy, and in 1453 Contantinople fell." (özetteki yazım) / TR: "İtalya'dan vaat edilen belirsiz yardımın hiçbiri gelmedi ve 1453'te Konstantiniyye düştü." |
| 22 | c5 | Poggio Lucretius'u bulur; Niccoli kendi güzel el yazısıyla kopyalar, bu nüsha 50'den fazla kopyanın modeli olur; Poggio orijinalin 14 yıl geri verilmediğinden yakınır. | Substack makalesi, Greenblatt *The Swerve* | ○ | Birebir yok. |
| 23 | c5 | Lascaris'in cep defteri (Vat. gr. 1412): Lorenzo'nun elde etmek istediği metinlerin (desiderata) listesi ve Medici kütüphanesinin o günkü içeriği. | Speake, Athos makalesi (GRBS) | ◐ | Birebir yok. |
| 24 | c5 | Lascaris kendisi İtalya'ya 200 el yazması getirdiğini söyler; defterdeki liste bunun neredeyse iki katı. | Speake (özet) | ◐ | Özet cümlesi: "Lascaris tells us elsewhere that he brought 200 manuscripts from Greece to Italy, and yet the notebook lists almost twice that number." Wikipedia ise 1492'de "Athos'tan ≈200" diyor. |
| 25 | c5 | Bruni'nin "yedi yüzyıl sonra Yunancayı İtalya'ya ben geri getirdim" iddiası abartı; Barlaam Petrarca'ya 1342'de, Chrysoloras 1396/97'de Floransa'da öğretmişti. | GreekReporter, Wikipedia listesi | ○ | Birebir yok. |

### 3.3 c6: Lorenzo (sanat, şiir, kişilik)

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| 26 | c6 | **Lorenzo'nun görünüşü.** Yakın dostu Niccolò Valori bile "doğa dış görünüşü bakımından ona üvey ana oldu" demek zorunda kaldı; iç insanda ise şefkatli ana gibiydi. | Valori, Lorenzo'nun yakınıydı; Unger'in *Magnifico*'sundaki aktarım (çeviri Unger'in). Özgün Latince/İtalyanca görülmedi. | ◐ | EN (Unger'den): "nature had been a step-mother to him with regard to his personal appearance" ... "when it came to the inner man she truly acted as a kindly mother…" / TR: "Doğa, kişisel görünüşü bakımından ona üvey ana olmuştu… ama iç insana gelince gerçekten şefkatli bir ana gibi davrandı…" |
| 27 | c6 | **Koku duyusu.** Valori'ye göre burnu basık, koku alma yok, görme zayıf. | Valori, FlorenceCity.it (İtalyanca) özetinden | ◐ | Birebir yok (özet). |
| 28 | c6 | **Ses.** Guicciardini: sanki burnundan konuşuyordu; bir Felemenkçe makale: keskin, tiz ses, ama belagatine engel olmadı. | Guicciardini (sonradan, 1500'ler); Felemenkçe makale ikincil | ○ | EN (FlorenceCity özeti): "it seemed he spoke through his nose" / TR: "burnundan konuşuyor gibiydi." |
| 29 | c6 | **Yüz.** Cerretani: koyu saç ve ten, yassı yanaklar, alışılmadık geniş ağız. Machiavelli, çirkin bir fahişeyi anlatırken Lorenzo'ya benzetmekten daha kötü hakaret bulamamış. | Cerretani (sonradan); Machiavelli'nin esprisini Unger aktarıyor (kaynağı belirtilmemiş) | ○ | Birebir yok. |
| 30 | c6 | Portre: Gozzoli'nin çocuk Lorenzo'su büyük olasılıkla gerçeğe yakın; beyaz atlı kral idealize. Verrocchio büstü tarifleri destekliyor. | Felemenkçe makale (FireFiandre) | ○ | Birebir yok. |
| 31 | c6 | **Faun anekdotu.** Michelangelo yaşlı bir faun başı yontar; Lorenzo şaka eder; Michelangelo gidince bir dişi çıkarıp diş etini oyar. Lorenzo etkilenip onu evine alır. | Ascanio Condivi, *Michelangelo'nun Yaşamı* (1553): Michelangelo'nun gözetiminde yazılmış "yetkili" biyografi; olaydan ≈60 yıl sonra. | ◐ ANEKDOT | EN (çeviri): "Lorenzo said to him jokingly that old people never have all their teeth and that they always miss one." / TR: "Lorenzo ona şakayla, yaşlı insanların dişlerinin hiçbir zaman tam olmadığını, hep birinin eksik olduğunu söyledi." (Aramada "5 dukat/ay" ve "mor pelerin" doğrulanmadı.) |
| 32 | c6 | Faun eseri kayıp; Bargello'da bulunmuş sanılan bir maske de kayıp. | Wikipedia "Head of a Faun", popüler sayfalar | ◐ | Birebir yok. |
| 33 | c6 | Bertoldo'nun bahçedeki rolü: NYRB incelemesine göre Condivi'de Bertoldo ve antikalar hiç geçmiyor; bunlar Vasari'nin genişletilmiş ikinci baskısında; Condivi bahçeye Granacci'nin götürdüğünü söylüyor. | NYRB 24 Haz 1999 "In Lorenzo's Garden" (Condivi/Vasari yayın incelemesi) | ○ | Birebir yok. |
| 34 | c6 | **Torrigiani'nin yumruğu.** Torrigiani, Cellini'ye gençken Carmine'de Masaccio'yu kopyalarken Michelangelo'nun alay ettiğini, öfkelenip yumruğunu vurduğunu, kemik ve kıkırdağın elinin altında çöktüğünü anlatır ve Michelangelo'nun bu izi ölene dek taşıyacağını söyler (özet parafrazı, tırnak yok). | Cellini'nin otobiyografisi (HAFIZA: 1550'lerin sonu–60'lar, O); Torrigiani'nin sözünün aktarımı, olaydan on yıllar sonra | ◐ ANEKDOT | Birebir yok. Chalmers biyografi sözlüğü: "as if they had been made of paste" / TR: "sanki hamurdan yapılmışlar gibi"; "biscuit" (bisküvi) ifadesi bazı çevirilerde geçer (özet). |
| 35 | c6 | Vasari başka bir güdü verir: Torrigiani'nin Michelangelo'ya kıskançlığı; olayın ardından Floransa'dan kaçmak zorunda kaldı. Lorenzo'nun öfkelendiği söylenir. Burnun bozukluğu Michelangelo'nun tüm portrelerinde belirgin. | Vasari (1550/68) | ◐ ANEKDOT | Birebir yok. Yaş: Michelangelo ≈15, Torrigiani ≈2,5 yaş büyük (özet, ○). |
| 36 | c6 | **Giostra sancağı** (Ocak 1475): Giuliano'nun sancağında Botticelli'nin Simonetta'yı miğferli Pallas olarak resmetmesi, "La Sans Pareille"; The Florentine ise Minerva'yı zeytin dalları ve alevler arasında, "La sans par" mottosuyla anlatıyor. Asıl sancak kayıp. | Wikipedia, Daily Art Magazine, The Florentine | ◐ (olay) / ○ (sancağın görünüşü) | Motto özetlerde "La Sans Pareille" ve "La sans par" diye iki yazımla geçiyor. |
| 37 | c6 | Giuliano ile Simonetta'nın sevgili olup olmadığı bilinmiyor; Simonetta Nisan 1476'da verem yüzünden öldü (≈22–23 yaş). | Wikipedia | ◐ | Birebir yok. |
| 38 | c6 | **Botticelli'ye ödeme:** Sekizler Konseyi 21 Tem 1478'de Botticelli'ye "hainleri resmetmek" emeği için 40 florin verilmesine karar verdi. Vasari yeri Palazzo del Podestà cephesi diyor; bir kaynak bunu hata sayıyor (Castagno 1457'de ölmüştü). En az 80 kişi idama mahkûm edilmişti; hepsini resmetmek akla yatkın değil. | Konsey kaydı çağdaş belge; bize ulaşan alıntı 19. yy. neşri (Milanesi 1862) | ○ | Latin (özette Milanesi'den): "deliberaverunt et santiaverunt Sandro Botticelli pro ejus labore in pingendo proditores flor. quadraginta largos" / TR: "Sandro Botticelli'ye, hainleri resmetme emeği için kırk iri florin verilmesine karar verip onayladılar." (Yazım özetteki gibi; özgün kayıt görülmedi.) |
| 39 | c6 | **Primavera nerede asılıydı?** 1499 envanteri Lorenzo di Pierfrancesco'nun Floransa'daki şehir sarayını anar. Bir özet tabloyu çiftin yatak odasında bir sedirin üstünde, diğeri yatak odasının ön odasında anıyor. Vasari tabloları Castello'da gördü. | 1499 envanteri çağdaş belge; modern aktarımlar | ◐ (envanter) / ○ (yatak odası mı, ön oda mı) | Birebir yok. |
| 40 | c6 | Leonardo Ludovico Sforza'ya yazdığı mektupta (Codex Atlanticus) sanatından çok askerî mühendislik becerilerini öne çıkarır. Lorenzo'nun onu gümüş lirle göndermesi (at kafatası biçimli lir) bir rivayet. | Leonardo'nun kendi mektubu, c.1482 çağdaş; lir hikâyesi sonradan | ◐ (mektup) / ○ ANEKDOT (lir) | Birebir yok. |
| 41 | c6 | Usta–çırak sisteminin fiyatı: Lorenzo di Credi'nin 1480 vergi beyanında (annesi Lisa) Verrocchio atölyesinde yılda 12 florin. Cennini 1390'larda çırağın "otoriteye saygıyla" bağlandığını yazar; HistoryRise'a göre çırağa çoğunlukla ücret ödenmez, eğitim ücret sayılırdı. | Vergi beyanı çağdaş (özet); Cennini 1390'lar | ○ | Birebir yok. |
| 42 | c6 | *Canzona di Bacco*: 1490 Karnavalı alayı için, sekizli (ottonari) ballata, yedi kıta ve nakarat; temel tema gençliğin kısalığı. Nakarat (kamu malı; HAFIZA, Y): "Quant'è bella giovinezza / che si fugge tuttavia! / chi vuol esser lieto, sia: / di doman non c'è certezza." | Lorenzo, 1490 | ◐ (tarih, biçim) / HAFIZA (nakarat) | Kritik baskıyla karşılaştırılmalı. TR (bize ait): "Ne güzel şey gençlik, ama kaçıp gidiyor! Neşeli olmak isteyen olsun: yarının güvencesi yok." |
| 43 | c6 | Raccolta Aragonese: Federico d'Aragona bir Toskana şiir derlemesi isteyince Lorenzo işi Poliziano'ya verdi (Oxford: Poliziano ve Lorenzo hazırladı, Lorenzo kendi şiirlerini ekledi); Federico onu en değerli mallarından biri saydı, kısmi kopyalar dolaşmaya başladı. Derleme Dante'nin *Vita nova*'sını ve Cino, Guittone, Cavalcanti gibi nadir şairleri içeriyor. | Oxford (Bodleian) açıklaması, Britannica, The Conversation | ◐ | Birebir yok. |

### 3.4 c10: Savonarola ve sanat

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| 44 | c10 | 7 Şubat 1497'de Piazza della Signoria'da lüks eşya ve sanat eseri yakıldı; Smithsonian'ın aktardığı David Reis'e göre dev bir yığın ve tepesinde Şeytan suretiyle; popüler bir sayfa yedi katlı piramit diyor (çelişen betimler). | Modern anlatımlar; Landucci günlüğü ve Burlamacchi'ye ulaşılamadı | ○ | Birebir yok. |
| 45 | c10 | Savonarola yandaşlarına "Piagnoni" (ağlayanlar) deniyordu. | History Today | ◐ | Birebir yok. |
| 46 | c10 | "Botticelli kendi resimlerini yaktı" iddiasına çağdaş kanıt yok; Vasari'nin Botticelli yaşamı bunu anlatmıyor; Botticelli'nin 1498'den sonra tarihlenen eserleri var, yani resmi bırakmadı. | Wikipedia "Bonfire of the vanities"; bir sanat tarihi yazısı (K41'deki Sotheby's sayfası olabilir); diğer sayfalar | ◐ | Birebir yok. |
| 47 | c10 | İddia popüler anlatımlarda yaygın ("Bonfire of the Botticellis" gibi başlıklar) ama hepsi geç ve kaynaksız. | Gadfly, Apollo, Substack (geç) | ◐ | Birebir yok. |
| 48 | c10 | Bir özet "Fra Bartolomeo ve Lorenzo di Credi kendi eserlerini yaktı" iddiasını doğrulamadı. | — | ○ | Aramada çıkmadı; HAFIZA: Vasari'de Fra Bartolomeo'nun çizimlerini yaktığı söylenir (O). |

### 3.5 c12: Dük (kurumlar)

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| 49 | c12 | Uffizi adı "ofisler": Cosimo I 1560'ta Vasari'ye Floransa'ya dağılmış 13 magistratura için yeni ofis binası tasarlattı. | Uffizi/IMSS özetleri | ◐ | EN: "In 1560, Cosimo I de' Medici, the Duke of Tuscany, ordered a design of new office buildings for the magistrates of Florence." ve "The building was meant to house 13 administrative authorities that were scattered about Florence." / TR: "1560'ta Toskana Dükü Cosimo I de' Medici, Floransa'nın yargıçları için yeni ofis binalarının tasarlanmasını emretti." ve "Bina, Floransa'ya dağılmış 13 idari makamı barındıracaktı." |
| 50 | c12 | Üst loggia 1565'te Palazzo Vecchio'yu Pitti'ye bağlayan koridorun parçası oldu; Tribuna (sekizgen) Buontalenti'ye atfedilir ve Atina'daki Rüzgârlar Kulesi'nden esinlendiği söylenir. | Uffizi/IMSS özetleri | ◐ (koridor) / ○ (Rüzgârlar Kulesi) | Birebir yok. |
| 51 | c12 | Accademia iki parçalı: "lonca" (tüm çalışan sanatçılar) ve seçkin "akademi" (Medici devletinin sanat üretimini denetleyen). 36 üye, Michelangelo kurumun "capo"larından biri, Borghini luogotenente. | Wikipedia; 2025 akademik makale; Storia di Firenze | ◐ | EN: "the company was a kind of guild for all working artists, while the academy was a more select group of artists responsible for supervision of artistic production in the Medici state" / TR: "şirket (compagnia) çalışan tüm sanatçılar için bir tür loncaydı; akademi ise Medici devletindeki sanat üretiminin denetiminden sorumlu daha seçkin bir sanatçı grubuydu." |
| 52 | c12 | Cenaze (14 Tem 1564, San Lorenzo): Varchi'nin orasyonu Borghini'ye ithaf edilmiş; basılı kapakta 28 Haziran yazıyor ama tören 14 Temmuz'da yapıldı. | Davis, *Fontes* 23 (Heidelberg) özeti; Penn Colenda kataloğu | ◐ (tören) / ○ (kapak tarihi) | Birebir yok. |
| 53 | c12 | Cesedin Roma'dan "mal gibi" kaçırıldığı hikâyesi (Roma yetkilileri boş mezarı Floransa topraklarına geçildikten sonra fark etmiş) popüler anlatımlarda; arte.it'in anma sergisi "Ad uso di mercanzia Michelangelo trafugato" adını taşıyor. Varış tarihi bu kaynakta 10 Mart. | Popüler anlatım, olaydan çok sonra | ○ ANEKDOT | Başlık (İtalyanca): "Ad uso di mercanzia" / TR: "Mal olarak (ticari eşya biçiminde)." |
| 54 | c12 | Crusca'nın *Vocabolario*'su Salviati'nin 14. yy. Floransa metin kanonuna dayandı, başka yazarları ancak "iyi Floransa lehçesi" kullandılarsa aldı; 1590'da başladı, 1612'de Venedik'te basıldı. | Modern dil tarihi özetleri | ◐ | EN: "based on Lionardo Salviati's canon of 14th-century Florentine texts, quoting other authors only if they used good Florentine" / TR: "Lionardo Salviati'nin 14. yüzyıl Floransa metinleri kanonuna dayanıyor; başka yazarlardan ancak iyi Floransa lehçesi kullandılarsa alıntı yapıyor." |
| 55 | c12 / c14 | **Studiolo:** "yarı ofis, yarı laboratuvar, yarı saklanma yeri, yarı merak kabini"; Borghini'nin programı odayı dört elemente böldü; Francesco dışında çok az kişi gördü; ölümünden sonra söküldü, 1920'de yeniden kurulması kararlaştırıldı. | Wikipedia, Oxford Cabinet, Rocaille | ◐ | EN: "part-office, part-laboratory, part-hiding place, and part-cabinet of curiosities" / TR: "yarı ofis, yarı laboratuvar, yarı saklanma yeri, yarı merak kabini." ve EN: "besides Francesco, very few persons ever saw the Studiolo" / TR: "Francesco dışında çok az kişi studiolo'yu gördü." |
| 56 | c12 / c14 | Medici porseleni: Francesco kimyagerlerden formül istedi; ≈1575'te Batı'nın ilk "vitreous paste" porselenleri. | Conceptual Fine Arts özeti | ○ | Birebir yok. |
| 57 | c12 / c14 | Opificio'nun ilk binası Uffizi'nin doğu kanadındaki Galleria dei Lavori; V&A: Avrupa'da sert taş (hardstone) üretiminde uzmanlaşan ilk saray manufakturası; ürünler saray döşemek ve hediye etmek içindi. | OPD resmî sitesi, V&A | ◐ | EN: "the first court manufacture in Europe to specialise in hardstones" / TR: "sert taşlarda uzmanlaşan Avrupa'nın ilk saray manufakturası." |

### 3.6 c14: Yıldızlar, Notalar, Taşlar (yalnız aramayla doğrulananlar)

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| 58 | c14 | Medici Doğu Matbaası'nın Arapça harfleri: Robert Granjon kesti; bir kütüphane tanımı "güzel akıcı Arapça harf" diyor. | Kütüphane/müzayede katalogları | ◐ | EN: "The beautiful cursive Arabic type, designed by Robert Granjon" / TR: "Robert Granjon'un tasarladığı güzel, akıcı Arapça harf." |
| 59 | c14 | **III. Murad'ın Ekim 1588 fermanı:** iki Avrupalı tüccarı (Branton ve Orazio Bandini) korur; sevkiyatlarını zorla açanlara karşı memurları uyarır. Ferman 1594 Medici Öklid baskısının arkasında günümüze kalmıştır. | Modern Osmanlı basım tarihi çalışmaları (Manchester, De Gruyter) | ◐ | EN (özet): "are opening up their shipments by force" / TR: "sevkiyatlarını zorla açanlar" (cümlenin öncesi özette yok). |
| 60 | c14 | İstanbul'da her iki basılı baskının satışı beklenenden düşük kaldı, oysa aynı metinlerin el yazması nüshalarına ciddi talep vardı. Typographia Medicea Arapça/Müslüman basımlarının %35'ini, Müteferrika kendi üretiminin yaklaşık %70'ini sattı (bir kaynağın karşılaştırması). | Modern çalışmalar | ○ | EN: "The sales of both printed editions in Istanbul, for instance, were lower than expected, despite the significant demand for manuscript copies of the same texts." / TR: "İstanbul'da her iki basılı baskının satışı, aynı metinlerin el yazması nüshalarına duyulan ciddi talebe rağmen beklenenin altındaydı." |
| 61 | c14 | 1610'a dek Raimondi, Granjon harfleriyle yalnızca 8 eser bastı. | Müzayede kaydı | ○ | Birebir yok. |
| 62 | c14 | Harfler sonunda Napoléon'un eline geçti: 1808'de zımba ve matrisler Paris'e getirilip Yakın Doğu'ya Arapça bildiriler basıldı. | Wikipedia/müzayede özeti | ○ | Birebir yok. |
| 63 | c14 | Arapça-Latince İncil'in 1590–91, İbn Sina *Kanun*'un 1593, Öklid'in (Tusî çevirisi) 1594'te basılması; bir özet "İncil 1588'de Lübnan'a ithal edildi" diyor ki tutarsız (D10). | Wikipedia, kütüphane katalogları | ◐ (baskılar) | Birebir yok. |
| 64 | c14 | Opificio'nun kuruluşu: 1588, Ferdinando I; "sert taş mozaik" (commesso) tekniğinin Cosimo I döneminde Floransa'ya getirildiği, ürünlere "opere di commessi Medici" denmesi. | OPD resmî sitesi, Wikipedia | ◐ | Birebir yok. |

### 3.7 c16: Hesap (tartışma ve miras)

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| 65 | c16 | Gombrich'in itirazı (NYRB 1993, Kempers'e yanıt): Medici gibi benzersiz konumdaki patronların daha geniş bir toplumsal grubun "tipik temsilcisi" sayılması. Gombrich yanıtında Kempers'in argümanının kendi eleştirisini karşılamadığını, eleştirisinin 15. yüzyılı işleyen üçüncü bölüme yönelik olduğunu söylüyor (özet "kitabının üçüncü bölümü" diyor; hangi kitap olduğu belirsiz, büyük olasılıkla Kempers'in). | Gombrich (1993 yanıtı) | ◐ | EN (özet): "patrons such as the Medici, whose situation was unique, are seen as typical representatives of a much larger social group" / TR: "durumu benzersiz olan Medici gibi patronlar, çok daha geniş bir toplumsal grubun tipik temsilcisi sayılıyor." |
| 66 | c16 | *With and Without the Medici* (1998), Medici faaliyetinin ne kadar "paradigmatik" sayılabileceğini farklı toplumsal gruplardan gelen siparişler üzerinden araştırıyor. | Kitap tanıtımı | ◐ | EN: "considers how far Medici activity as patrons can be considered paradigmatic" / TR: "Medici'nin patron olarak faaliyetinin ne ölçüde örnek (paradigmatik) sayılabileceğini ele alıyor." |
| 67 | c16 | Goldthwaite'in tezi: 1300–1600 arası kuzey İtalya'da sürekli zenginlik üretimi ve birikimi, tüketim artışının "izin verici nedeni"; merchant ve soylu aileler ile dinî kurumlar dahil. | Kitap tanıtımı, AHR ve BHR incelemeleri | ◐ | EN (kitap tanıtımı): "continual generation and accumulation of wealth in northern Italy between 1300 and 1600 was the permissive cause of high growth in consumption" / TR: "1300–1600 arası kuzey İtalya'da zenginliğin sürekli üretilip birikmesi, tüketimdeki yüksek büyümenin izin verici nedeniydi." |
| 68 | c16 | Cosimo'ya atfedilen söz: "Şehrimin mizacını bilirim; elli yıl geçmeden sürülürüz ama binalarım kalır." Kaynağı ve ilk geçtiği yer doğrulanamadı. | PBS *Medici: Godfathers of the Renaissance* eşlik sayfası | ○ | EN: "I know the humors of my city, before 50 years have passed we shall be expelled, but my buildings will remain." / TR: "Şehrimin mizacını bilirim; elli yıl geçmeden sürülürüz, ama binalarım kalır." (Atıf şüpheli; birebir kullanma, "diye aktarılır" de.) |
| 69 | c16 | Uffizi "halka açılış": resmî Uffizi sitesine göre Büyük Dük 1769'da galeriyi resmen halka açtı (bir kaynak 1765). | Uffizi resmî sitesi, diğer özetler | ◐ | EN: "the Grand Duke officially opened the Gallery to the public in 1769" / TR: "Büyük Dük galeriyi 1769'da resmen halka açtı." |
| 70 | c16 | OPD bugün de çalışıyor: 1975'te restorasyon laboratuvarıyla birleşti, Kültür Bakanlığı'na bağlı özerk enstitü. | OPD resmî sitesi, Wikipedia | ◐ | Birebir yok. |
| 71 | c16 | Pevsner'in (1940) "Accademia'nın öğretme niyeti" okuması ile Barzman'ın (2000) itirazı: Barzman, Pevsner'in Vasari'nin etkisini abarttığını ve kurumun pedagojik bağlılığını hafife aldığını söyler. | Barzman incelemesi (CAA Reviews) | ◐ | Birebir yok. |

---

## 4. Sayılar ve ölçüler

Aralık veya çelişki varsa hepsi yazıldı. "HAFIZA" satırları doğrulanmamıştır.

| # | Bölüm | Ölçü | Değer(ler) | Çelişki / aralık | Sınıf | Kaynak |
|---|---|---|---|---|---|---|
| 1 | c4 | Kubbe yarışması ödülü | 200 altın florin ("kullanılan model için") | — | ◐ | K1, K3 |
| 2 | c4 | Yarışma ilan günü | 19 Ağu 1418; teslim Eylül sonu | Bir kaynak 18 Ağu | ◐ | K1, K3 |
| 3 | c4 | Brunelleschi–Ghiberti ortak denetim | 1420 baharı; Battista d'Antonio belgeli 1420–39 | Bir blog "berabere, Ghiberti kazandı" diyor (güvenilmez) | ◐ | K1 |
| 4 | c4 | Kubbe inşa süresi | 1420–1436 (≈16 yıl) | "Fener 1471'e dek bitmedi" (blog); HAFIZA: fener 1446–61, top 1468–71 (O) | ◐ | K6 |
| 5 | c4 | Kutsama | 25 Mar 1436 (Eugenius IV) | Kubbe kabuğunun kapanışı ≈5 ay sonra, ayrı kutsama (tek özet) | ◐ / ○ | K7 |
| 6 | c4 | Eski Sakristi inşaatı | 1419–1428 | HAFIZA: 1421 başlangıç (O) | ◐ | K8 |
| 7 | c4 | Palazzo Medici başlangıcı | 1444 | Belgeli saha çalışması 1445 başı; bir kaynak "1444–1484" inşa süresi | ◐ / ○ | K9 |
| 8 | c4 | Donatello *David* tarihi | 1420'ler–1460'lar; çoğunluk 1440'lar | Smarthistory: 1430'lar sonu–1440'lar, 1450'ler başında tamam; azınlık 1460'lar (Piero) | ◐ | K10 |
| 9 | c4 | San Marco harcaması | Papa önerisi 10.000 florin; toplam >40.000 florin | "Duka" değil florin | ◐ | K12 |
| 10 | c4 | Aynı yazarın başka bir bağlamı | Kâhya dolandırıcılığı ≈10.000 florin | Aynı çalışmada İtalyanca metin "harcama"yı ≈100.000 florin olarak veriyor (neyin harcaması olduğu özette belirsiz). **M1 bankacılık eksenine not.** | ○ | K12 |
| 11 | c4 | Niccoli kitaplığı | 800 el yazması/cilt, ≈6.000 florin; 16 curator | "Cilt" mi "el yazması" mı kaynaklar arasında | ◐ | K15 |
| 12 | c4 | Tornabuoni şapeli | 1.200 duka + 200 (memnunsa), Vasari; sözleşme 1 Eyl 1485; süre 4 yıl; açılış 22 Ara 1490 | "1.100 florin" iddiası aramada doğrulanmadı | ◐ | K19 |
| 13 | c4 | Rucellai | "50 yıl kazandım/harcadım"; "8 evden 1 saray" | Saray: 1446–51 (Alberti) veya 1453 | ◐ / ○ | K14 |
| 14 | c5 | Konsil heyeti | ≈700 Doğu delegesi | — | ◐ | K23 |
| 15 | c5 | Birlik kararı | 5 veya 6 Temmuz 1439 | Taşınma ayı: Şubat veya yaz 1439 | ◐ | K23 |
| 16 | c5 | Lascaris el yazması | 200 ("Yunanistan'dan", kendi beyanı); defterde ≈2 katı | Wikipedia: 1492'de "Athos'tan ≈200"; "80 yeni" iddiası **bulunamadı** | ◐ | K25 |
| 17 | c5 | Lascaris yolculukları | 2 (1490, 1491); Athos 1491; dönüş 1492 | Tek sefer 1491–92 anlatısı | ◐ | K25 |
| 18 | c5 | Ficino çevirileri | Platon: bitiş 1470, basım 1484; Plotinos 1492 | — | ○ | K22 |
| 19 | c5 | Ficino'ya hediye | 1462 (gelenek) veya 1463; Careggi mi Montevecchio mu | Kaynaklar ayrışıyor | ◐ | K21, K22, K24 |
| 20 | c5 | Medici kütüphanesi | 1494 el koyma; 1508 Roma; 1523/24 sipariş; 1558 bina; 1571 halka açılış | 1523 mü 1524 mü | ◐ | K26 |
| 21 | c6 | Raccolta Aragonese | 1476–77 | Wikisource baskısı 1465 (hatalı görünüyor); Macar makale 1476 | ◐ | K38 |
| 22 | c6 | Giostra | Ocak 1475, Santa Croce | — | ◐ | K39 |
| 23 | c6 | Simonetta | doğum ≈1453, ölüm Nisan 1476 | Ölüm günü ayrışıyor | ◐ | K39 |
| 24 | c6 | Botticelli'nin 1478 ücreti | 40 florin ("iri florin"); ≥80 idam | Tek özet | ○ | K30 |
| 25 | c6 | Lorenzo di Credi'nin ücreti | 12 florin/yıl (1480 vergi beyanı) | Tek özet | ○ | K31 |
| 26 | c6 | Cennini | Agnolo Gaddi atölyesinde ≈10 yıl; kitap 1390'lar | Doğum 1360/1370; ölüm 1427/1440 | ○ | K32 |
| 27 | c6 | *Primavera* tarihi | 1470'lerin sonu–1480'lerin başı; 1481/82; envanter 1499 | — | ◐ | K29 |
| 28 | c6 | Bertoldo medalyonu | c.1480–81 | Müzeler 1480 veya 1480–81 | ◐ | K47 |
| 29 | c6 | Canzona | 1490; 7 kıta + ritornello; sekizli | — | ◐ | K37 |
| 30 | c12 | Uffizi | 1560 başlangıç; 13 magistratura; bitiş 1580 veya 1581; Tribuna 1581; halka açılış 1769 | 1765 diyen bir kaynak | ◐ | K42 |
| 31 | c12 | Vasari Koridoru | 1565 | Süre ("5 ay") HAFIZA (O) | ◐ | K42 |
| 32 | c12 | Accademia del Disegno | 13 Oca 1563 (kuruluş metni 12 Oca); ilk oturum 31 Oca; 36 üye | Bir kaynak "1561, Avrupa'nın ilk resmî çizim okulu" (aykırı) | ◐ | K43 |
| 33 | c12 | Michelangelo cenazesi | 14 Tem 1564 | Basılı kapak 28 Haz; ceset varışı 10 Mar (popüler kaynak) | ◐ / ○ | K44 |
| 34 | c12 | Crusca | 1583 (Salviati); *Vocabolario* 1590'da başladı, 1612'de basıldı | Bir kaynak 1582 | ◐ | K45 |
| 35 | c12 | Accademia Fiorentina | 1541 (tanınma) | HAFIZA: Umidi 1540 (O) | ○ | K45 |
| 36 | c12 / c14 | Studiolo | 1570–72 (Wikipedia) veya 1570–75; yeniden kurma kararı 1920 | Program/komisyon başlangıcı 1564/1569/1570 | ◐ | K48 |
| 37 | c14 | Medici Doğu Matbaası | 1584; Arapça İncil 1590–91; *Kanun* 1593; Öklid 1594; 1610'a dek 8 eser | Katalog adreslerinde 1591 de görülüyor | ◐ | K46 |
| 38 | c14 | Ferman | Ekim 1588 | — | ◐ | K46 |
| 39 | c14 | Satış oranı | Medici %35; Müteferrika ≈%70 | Tek karşılaştırma | ○ | K46 |
| 40 | c14 | OPD | 1588; 1975 birleşme | — | ◐ | K49 |
| 41 | c4 (HAFIZA) | Kubbe boyutları | ≈4 milyon tuğla; haçla birlikte ≈114,5 m; iç çap ≈45 m | Kaynaklar arasında değişir (41–45 m) | HAFIZA O | — |
| 42 | c14 (HAFIZA) | Galileo'nun maaşı | ≈1.000 scudo/yıl (Büyük Dük'ün hizmetinde) | Birim ve tutar doğrulanmadı | HAFIZA D | — |

---

## 5. Mit/efsane ve tarihçi tartışmaları

Biçim: **iddia → kim ne diyor → kaynaklı değerlendirmem → video davranışı önerisi.**

### 5.1 "Medici Rönesans'ı yarattı / başlattı"

- **İddia:** popüler anlatının omurgası; plan §4'te "aşırı basit".
- **Kim ne diyor:**
  - **Gombrich**, "The Early Medici as Patrons of Art: A Survey of Primary Sources" (1960): birincil kaynak taraması (◐, K17). 1993 NYRB yanıtında Medici gibi "benzersiz" konumdaki patronların daha geniş bir toplumsal grubun "tipik temsilcisi" sayılmasını eleştirir; Kempers'in karşı argümanı: Medici'nin öne çıkışı çoğunlukla geriye dönük, Cosimo I patronajı üzerinden (özet, ○).
  - **Goldthwaite**, *Wealth and the Demand for Art in Italy, 1300–1600* (1993): zenginlik birikimi ve yeni tüketici grupları (tüccar, soylu, dinî kurumlar) sanat talebinin itici gücü (◐, K18). Medici'ye ilişkin kendi cümleleri aramada görülmedi.
  - ***With and Without the Medici* (1998):** Medici faaliyetinin ne kadar "paradigmatik" sayılabileceğini farklı toplumsal grupların siparişleri üzerinden sorar (◐, K17).
  - **Burckhardt (1860), Hans Baron, Roscoe (1796), Dale Kent (2000), Evelyn Welch (1997):** bu aramada sözleri doğrulanamadı, HAFIZA. Kısa hatırlayışım: Burckhardt ve Roscoe Medici merkezli anlatıyı yaygınlaştırdı; Baron Rönesans'ı Medici'den önce Floransa'nın Milano karşıtı savaşına bağladı; Kent Cosimo'nun patronajını kişisel/dinî/dostluk bağlamında okur; Welch sanatı geniş bir toplumsal bağlamda ele alır. **Bunları kaynak sayfa görülene kadar senaryoya alma.**
- **Aramada görülen karşı veriler:** kubbe Opera/Arte della Lana işi (◐, D1); Rucellai sarayı ve itirafı (◐); Tornabuoni–Ghirlandaio sözleşmesi (◐); Sassetti (◐); Brancacci: Medici'nin düşmanı bir patron ve siyasetle silinen portre (◐); *Primavera*/*Venüs*: ana Medici kolu değil, kuzen kolu (Lorenzo di Pierfrancesco) çevresi (◐/○).
- **Medici lehine belgeli veri:** Giovanni di Bicci–Eski Sakristi (◐); Cosimo–San Marco–Niccoli kitaplığı (◐); Ficino'ya Careggi (◐); Verrocchio'nun Medici mezarları (◐); Laurenziana (◐).
- **Değerlendirme:** "tek yaratıcı" tezi **desteklenmiyor**; "en iyi belgelenmiş ve en görünür patronlardan biri" destekleniyor. Görünürlüğün bir kısmı kaynakların doğasından geliyor (Vespasiano'nun Cosimo'yu övmesi, Vasari'nin Floransa/Medici merkezli anlatısı: HAFIZA, doğrulanmadı).
- **Video davranışı:** "Medici Rönesans'ı yarattı" denmez. "Rönesans'ın en görünür patronlarından biri oldular; başkaları da harcadı, bazıları Medici'ye rağmen" çizgisi.

### 5.2 "Kubbeyi Medici yaptırdı"

- **Kim ne diyor:** Katedral yapımı Arte della Lana (yün loncası) denetimindeki Opera'da (◐, K1, K3). Medici'nin kubbe için karar veya finans rolü hiçbir sonuçta çıkmadı (yokluk kanıtı değildir). Brunelleschi–Medici bağı kubbede değil San Lorenzo Eski Sakristi'sinde belgeli (◐, K8).
- **Değerlendirme:** "Kubbe Medici işi değil" **DOĞRULANDI (◐)** ama "hiçbir bağ yok" denemez. Brunelleschi Medici'nin de mimarıydı (San Lorenzo), HAFIZA: Cosimo'nun 1440'ların başında San Lorenzo'nun yeniden inşasını üstlenmesi (O).
- **Video:** "Kubbe yün tüccarlarının, hemen yanındaki kilise Medici'nin" gibi iki ayrı cümle.

### 5.3 Yumurta anekdotu

- **İddia:** Brunelleschi yumurtayı kırıp dik durdurarak yarışmayı kazandı.
- **Kim ne diyor:** Vasari anlatır (◐ ANEKDOT); The Critic, çağdaşların kubbe biter bitmez onu efsaneleştirdiğini söylüyor; çağdaş kayıt bulunamadı (K2). Bir blog yarışmanın kazananı hakkında aykırı anlatım veriyor (güvenilmez).
- **Değerlendirme:** ANEKDOT. Belgeli olan: 1418 yarışma, 200 florin, 1420 seçim.
- **Video:** "Vasari yüz yıl sonra şöyle anlatıyor…" çerçevesiyle; Brunelleschi'nin iç dünyasına girilmez (kaynak yok).

### 5.4 "İskelesiz kubbe"

- **Kim ne diyor:** Kaynaklar "ahşap kalıp (centering) kullanılmadı"; balıksırtı dizilim kendi kendini taşır; Toskana'da kalıp için yeterli kereste yoktu (K5, K6; blog/rehber düzeyi). Wikipedia özeti: "ahşap destek çerçevesiz yapılan ilk sekizgen kubbe" (K7).
- **Değerlendirme:** **"İskelesiz" yanlış (D2)**; kalıpsız (centering'siz). HAFIZA: çalışma platformları ve vinçler (Brunelleschi'nin makineleri) vardı (O).

### 5.5 Sipariş kefaret mi, yatırım mı, siyasi görünürlük mü?

- **Belgeli:**
  - **Vicdan:** Vespasiano: Cosimo vicdanını Papa'ya danıştı; 10.000 florin önerildi; >40.000 harcandı (◐ ANEKDOT, K12). Bu, Cosimo'nun ölümünden ≈30 yıl sonra yazan, övgücü bir kaynaktan: "Cosimo böyle yaşadı" değil, "çağdaşlar Cosimo'yu böyle anlattı".
  - **Doktrin:** bankacı = tefeci günahkâr; çıkış hayır/patronaj (◐ YORUM, K12).
  - **Onur ve hatıra:** Rucellai'nin itirafı (◐, K14).
  - **Ölüm sonrası yatırım:** Giovanni di Bicci'nin Eski Sakristi'ye gömülmesi (◐, K8).
- **HAFIZA ("magnificence"):** Aristoteles'in *Nikomakhos'a Etik*'inde "magnificence" erdemi, Aquinas ve Bruni'nin Ethica çevirisi; Pontano *De magnificentia* (1498). **Aramada doğrulanamadı.**
- **"Yatırım" motifi:** bu aramada kaynak çıkmadı.
- **Değerlendirme:** tek motif yok. Üç motif belgeli (vicdan, onur/hatıra, ölüm sonrası); "siyasi görünürlük" ve "yatırım" HAFIZA.
- **Video:** "kefaret mi, yatırım mı" sorusu **açık bırakılabilir**; Vespasiano alıntısı ve Rucellai itirafı yan yana konabilir.

### 5.6 "Platon Akademisi"

- **Kim ne diyor:** Hankins, "The Myth of the Platonic Academy of Florence", *RQ* 44/3 (1991): tüzük ve üye kaydı yok; "Academia" Ficino'da metafor, özel ders ortamı; çağdaş kanıtta "Platon Akademisi" adı geçmiyor (◐, K21). Hankins'in 1990 yazısının özeti, Ficino'nun belgelerinin Cosimo'nun bir akademi kurduğu fikrini desteklemediğini söylüyor (◐); 2002 tarihli "The Invention of the Platonic Academy of Florence" yazısının yalnız başlığı görüldü (içeriği bilinmiyor, ○). **Field** (1988, *Origins of the Platonic Academy*) bibliyografide; **Kristeller**'in pozisyonu aramada görülmedi (HAFIZA: Kristeller gevşek ama gerçek bir çevre görür, O).
- **Geleneksel anlatı:** 1462'de Cosimo Ficino'ya Platon el yazmaları ve Careggi civarında mülk verdi (◐); Wikipedia ve ansiklopediler "Akademi"yi bu tarihe oturtur ve organizasyonsuz olduğunu da belirtir (K22).
- **Değerlendirme:** "Akademi" **tırnaklı**. Belgeli: Cosimo'nun Ficino'ya desteği, Careggi mektubu (◐), Ficino'nun dersleri/çevresi.
- **Video:** "Careggi'de Ficino'nun çevresi, sonradan 'Platon Akademisi' diye anılacak bir toplulukluk" çizgisi.

### 5.7 Konsil → Plethon → Cosimo → Akademi zinciri

- **Kim ne diyor:** Zincirin Plethon–Cosimo halkası Ficino'nun **geriye dönük** anlatımı (◐ ANEKDOT, K22); Hankins bu anlatıyı eleştirel okur (K21). Konsil'in Floransa'ya taşınmasında Cosimo'nun teşvikinin payı kaynaklarda var ama taşınma nedenleri çoklu (masraf, veba, Cosimo'nun teklifi) (◐, K23).
- **Değerlendirme:** Medici'nin Konsil'i "şehre çekmedeki payı" **gerçek ama tek neden değil**; Plethon–Cosimo–Akademi bağı ANEKDOT.

### 5.8 "1453'te kaçan Rum bilginler Rönesans'ı başlattı"

- **Kim ne diyor:** Rumca öğretimi 1453'ten önce İtalya'da: Barlaam–Petrarca (1342, ○), Chrysoloras Floransa'da 1396/97 (◐); Bruni'nin "yedi yüzyıl sonra ilk ben" abartısı (○); Argyropoulos (c.1415–1487), Chalcondyles (1423–1511), Bessarion 1453 öncesi ve sonrası gelenler (◐ liste, K27).
- **Değerlendirme:** göç **kademeli** ve 1453 öncesine uzanır; "1453 → Rönesans" mit. Lascaris ayrıca **Doğu'dan getiren** biri (Floransa'ya gelen değil, Lorenzo'nun gönderdiği), TR-BAĞ.

### 5.9 Michelangelo, "Medici okulu" ve Faun

- **Kim ne diyor:** Condivi (1553): Faun hikâyesi ve hane içine alınma (◐ ANEKDOT, K34). NYRB incelemesi: Condivi'de Bertoldo ve antikalar yok, bunlar Vasari'nin genişletilmiş ikinci baskısında; bahçeye Granacci götürdü (○, K36). Vasari ikinci baskı bahçeyi "okul ve akademi" olarak betimler (K36). Elam (1992) bahçenin rolünü gösteren makale diye anılıyor; 2024 bir makale Elam'ın 20. yy. şüphelerine karşı bahçenin işlevini gösterdiğini söylüyor (○, K36); Elam'ın kendi sözü görülmedi.
- **Değerlendirme:** Faun = Michelangelo'nun gözetiminde yazılmış (Condivi) bir **ANEKDOT**. "Resmî heykel okulu/akademisi" iddiası zayıf destekli; bahçe ve Lorenzo'nun antikaları gerçek olabilir (◐/○). "Büyüdü" değil, ≈15 yaşında hane içine alındı (HAFIZA: 1489–92, O). Aramada "5 dukat/ay, mor pelerin" doğrulanmadı.
- **Video:** "Michelangelo'nun anlattığına göre / Condivi'ye göre…" çerçevesi.

### 5.10 Torrigiani ve kırık burun

- **Kim ne diyor:** Cellini Torrigiani'nin kendi böbürlenmesini aktarır: Carmine'de Masaccio kopyalarken, Michelangelo'nun alayı üzerine; kemik-kıkırdak çöktü. Vasari kıskançlık der ve Torrigiani'nin Floransa'dan kaçmak zorunda kaldığını ekler; Lorenzo'nun öfkesi. Burnun izi tüm portrelerde belirgin (◐, K35).
- **Değerlendirme:** olay **iki farklı çerçevede** anlatılıyor: Cellini'de mekân Carmine, güdü alay; Vasari'de Medici çevresi, güdü kıskançlık. İkisi de olaydan on yıllar sonra.
- **Video:** "Aynı burun, iki hikâye" kaynak çatışması olarak.

### 5.11 Leonardo ve lir

- **Kim ne diyor:** Lorenzo'nun Leonardo'yu ≈1482'de gümüş lirle Ludovico Sforza'ya gönderdiği rivayet; bir kaynak "efsane" diyor, bir diğeri Lorenzo'nun lirin sipariş vericisi olabileceğini söylüyor; Lorenzo'nun Sforza at projesini tanıttığı iddiası "belirsiz" (K33). Leonardo'nun Ludovico'ya mektubu ağırlıkla askerî mühendislik (◐).
- **Değerlendirme:** ANEKDOT ○. Kaynakları (Anonimo Gaddiano, Vasari) aramada **görülmedi**; HAFIZA: Anonimo Gaddiano ≈1540 civarı, Lorenzo'nun gönderdiğini söyler (O). Lorenzo'nun Leonardo'ya büyük sipariş vermediği HAFIZA (O).
- **Video:** "diye anlatılır" çerçevesi; Leonardo'nun kendi mektubu daha sağlam.

### 5.12 Botticelli kendi resimlerini yaktı mı?

- **Kim ne diyor:** Çağdaş kanıt yok; Vasari anlatmıyor; 1498 sonrası tarihli eserleri var (◐, K41). Bir sanat tarihi yazısı da aynı sonuca varıyor (muhtemelen Sotheby's sayfası). Popüler anlatımlar geç ve kaynaksız.
- **Değerlendirme:** **mit** (◐). "Vasari'ye dayanır mı?" sorusunun yanıtı: **özetlere göre hayır**. HAFIZA: Vasari, Botticelli'nin Savonarola yanlısı olduğunu yazar ve onu mali sıkıntıya sokar (O); bu satır kaynakla doğrulanmadı.
- **Video:** "söylenir ama kanıtı yok" çerçevesi.

### 5.13 *Primavera* ve *Venüs'ün Doğuşu*'nu kim ısmarladı?

- **Kim ne diyor:** 1499 envanteri *Primavera*'yı Lorenzo di Pierfrancesco'nun şehir sarayında anar (◐); 1482 evlilik bağı "olası, kesin değil" (◐); *Venüs*'ün patronu "olasılıkla" aynı kişi (○); Vasari ikisini Castello'da gördü (◐). Akrabalık derecesi özetlerde "cousin twice removed" diyor (HAFIZA: ikinci kuzen, O).
- **Değerlendirme:** Lorenzo il Magnifico'nun siparişi değil; kuzen kolundan bir patron. Webster Smith (1975) atfı aramada doğrulanmadı.
- **Video:** "Medici'nin bir koluna ait" doğru; "Lorenzo'nun sipariş ettiği" yanlış.

### 5.14 "Lorenzo Toskana'yı yazı dili yaptı"

- **Kim ne diyor:** Raccolta Aragonese (1476–77): Lorenzo ve Poliziano'nun Dante merkezli Toskana şiir derlemesi, Floransa vernaküler edebiyatının prestijini yükseltti (◐, K38). Standardın çerçevesi: Bembo *Prose della volgar lingua* (1525) 14. yy. Floransa modeli (◐, K45), Cosimo I'in Accademia Fiorentina'yı tanıması (○), Crusca (1583) ve *Vocabolario* (1612) (◐).
- **Değerlendirme:** Lorenzo **prestij** sağladı; standardı Bembo (Venedikli) ve Salviati/Crusca oturttu. HAFIZA: konuşulan İtalyanca'nın birliği 19.–20. yy. (O).
- **Video:** "Lorenzo Toskana'yı yazı dilinin saygın bir seçeneği yaptı" ölçüsünde; "yarattı" denmez.

### 5.15 "Accademia delle Arti del Disegno ilk sanat akademisi"

- **Kim ne diyor:** "Resmî ilk sanat akademisi" diyen kaynaklar var (K43); Pevsner (1940) statüde "yeni başlayanları öğretmek" niyetini okur; Barzman (2000) Pevsner'in Vasari'nin payını abarttığını ve kurumun pedagojik bağlılığını hafife aldığını savunur (◐, K43). Carracci Akademisi ≈1580 Bologna (○, K43). San Luca (1577) aramada görülmedi (HAFIZA).
- **Değerlendirme:** kurum gerçek ve erken (◐, 1563); "ilk" **nitelikli**: yarı lonca (compagnia), yarı seçkin akademi; öğretme işlevi tartışmalı.
- **Video:** "ilk" denmez; "ilk büyük, devlet destekli sanatçı akademilerinden biri; yarı lonca, yarı akademi" biçimi.

### 5.16 "Uffizi ilk modern müze"

- **Kim ne diyor:** Uffizi'nin kronolojisi: 1560 ofis → 1581 Tribuna'da Francesco I'in özel koleksiyonu → 1769 resmen halka açılış (◐, K42).
- **Değerlendirme:** "Ofis"ten "müze"ye uzun yol; "ilk" sıfatı kanıtsız. HAFIZA: Capitoline bronzları 1471, Ashmolean 1683 gibi karşı örnekler (O).
- **Video:** "ilk" denmez.

### 5.17 Medici Doğu Matbaası ve Osmanlı

- **Kim ne diyor:** Matbaa Roma'da 1584; III. Murad'ın Ekim 1588 fermanı **yasak değil, tüccar koruması** (◐); İstanbul satışları beklenenin altında (○); "Osmanlı matbaayı yasakladı" anlatısı tartışmalı: bir kaynak Medici yayınlarının yalnız Osmanlı'ca değil, İslam dünyasındaki yöneticilerce engellendiğini söylüyor, bir diğeri "yasak olduğu için basmadılar" görüşüne itiraz ediyor (○, K46).
- **Değerlendirme:** ticari başarısızlık ve ferman birlikte anlatılabilir; "yasak" ya da "yasak değil" tarafında net hüküm bu aramadan çıkmaz.
- **Video:** dikkatli; ferman ◐, satış ○.

### 5.18 Bertoldo'nun II. Mehmed madalyonu

- **Kim ne diyor:** V&A: Bertoldo'nun tek imzalı madalyonu; Lorenzo, Sultan'ın Pazzi katilini yakalatmasına karşılık olarak ısmarlamış olabilir. Frick: "Lorenzo'nun Sultan'a hediye olarak ısmarladığı olası". Met: "muhtemelen Lorenzo'nun siparişi" (◐, hepsi hedge'li). Bertoldo İstanbul'a gitmedi, Gentile Bellini'nin madalyonundan türetti; ters yüzdeki zafer arabası Napoli'ye olası saldırıya imalı (V&A, Met).
- **Değerlendirme:** madalyon ◐; **kimin için** ve **neden** sorusu kaynaklarda hedge'li: "olası".
- **Video:** "sipariş edilmiş olabilir" dili.

### 5.19 Lorenzo'nun görünüşü ve kişiliği

- **Kim ne diyor:** Valori (yakın dost): dış görünüşte "üvey ana", iç insanda "şefkatli ana"; burun basık, koku yok, görme zayıf (◐, K40). Guicciardini: burnundan konuşur gibi (○). Cerretani: koyu ten, geniş ağız (○). Gozzoli'nin çocuk Lorenzo'su gerçeğe yakın, kral Lorenzo idealize (○).
- **Değerlendirme:** Valori Lorenzo'ya yakın biriydi, yani övgüye eğilimli bir tanık; yine de dış görünüş gibi hoş olmayan bir ayrıntıyı vermesi onu inandırıcı kılıyor. Guicciardini ve Cerretani Lorenzo'dan sonra yazdı (HAFIZA: Guicciardini Lorenzo öldüğünde 9 yaşındaydı, Y); yani bunlar ikinci el betimler. Üçünün özgün metni görülmedi; aktarımlar modern kitap ve makalelerden.
- **Video:** Valori'den doğrudan ("diye aktarılır" çerçevesiyle); "koku alamıyordu" iki ikincil kaynakta uyumlu (◐), "sesi tizdi/burnundan konuşuyordu" zayıf (○). Hiçbiri özgün metinden doğrulanmadı.

### 5.20 Cosimo'nun "binalarım kalır" sözü

- **Kim ne diyor:** PBS eşlik sayfasında Cosimo'ya atfedilen söz (○, K13). Kaynağı belirtilmemiş.
- **Değerlendirme:** PBS dışında bir sayfa görülmedi; ilk geçtiği metin doğrulanamadı. **Birebir yazma**, "diye aktarılır" de. (Not: söz doğruysa bile kaynağı Cosimo'nun kendisi olmayabilir; bir derleme veya yorum olabilir.)

### 5.21 Brunelleschi'nin reddedilen Palazzo Medici modeli

- **Kim ne diyor:** Vasari'ye bağlanan anlatıma göre Cosimo Brunelleschi'nin fazla gösterişli modelini reddedip Michelozzo'nun daha ölçülü tasarımını seçti (○, K9). Vasari metni görülmedi.
- **Değerlendirme:** ANEKDOT ○, belgesiz gelenek.

### 5.22 Lippi'nin odaya kilitlenmesi

- **Kim ne diyor:** Kaynaksız Wikipedia türevi: Cosimo onu çalışsın diye hapsetti, çarşaftan ip yaptı (○, K16). HAFIZA: Vasari'de Cosimo'nun sonra "seçkin kişileri baskıyla yönetmenin yanlış olduğunu" anladığı söylenir (O). Kaçırma olayı ise belgeli (◐).
- **Değerlendirme:** ANEKDOT ○.

---

## 6. TR-BAĞ: Osmanlı / Türkiye ile ilgili her şey

| # | Bölüm | Bağ | Olgu | Sınıf | Kaynak | Kullanım notu |
|---|---|---|---|---|---|---|
| 1 | c5 | **Lascaris'in Doğu seferleri** | Lorenzo, Janus Lascaris'i el yazması toplamak ve II. Bayezid ile satın alma pazarlığı yapmak üzere iki kez gönderdi (1490, 1491); Athos ziyareti 1491; cep defteri Vat. gr. 1412 (aranacaklar listesi + kütüphanenin içeriği); ≈200 el yazması | ◐ | K25 | NÜANS: tek sefer değil. "80 yeni metin" iddiası bulunamadı. Lorenzo'nun ölümü (8 Nis 1492, HAFIZA Y) sırasında Lascaris'in nerede olduğu kaynakta yok |
| 2 | c6 / c8 | **Bertoldo'nun II. Mehmed madalyonu** | c.1480–81, Bertoldo'nun tek imzalı madalyonu; Lorenzo'nun siparişi "olası/muhtemel"; Bertoldo İstanbul'a gitmedi, portreyi Gentile Bellini'nin madalyonundan türetti; ters yüzde Mehmed zafer arabasında, üç taçlı kadın figürüne bağlı iple; zafer arabasında Napoli krallarının alevli sandalye impresası (Napoli'ye saldırı ima edilmiş olabilir) | ◐ | K47 | Hedge'li dil kullan: "ısmarlanmış olabilir". V&A'ya göre Lorenzo, Sultan'ın Lorenzo'nun kardeşi Giuliano'nun katilini yakalatmasına minnetle bu madalyonu ısmarlamış olabilir (bu yorum tek müze sayfasında) |
| 3 | c6 / c8 | Mehmed'in Floransalı sanatçı isteği | Bir müze sayfası, Mehmed'in Floransalı sanatçılar istemiş olduğunu söylüyor | ○ | K47 | Tek özet; ayrıntı doğrulanmadı |
| 4 | c14 | **Medici Doğu Matbaası ve III. Murad'ın fermanı** | Matbaa Roma'da 1584; ferman Ekim 1588, Arapça/Farsça basılı kitap ithal eden iki Avrupalı tüccarı (Branton ve Orazio Bandini) korur ve memurlara sevkiyatları zorla açmamalarını emreder; ferman 1594 Öklid baskısının arkasında | ◐ | K46 | **Yasak değil, koruma.** "Bandini" soyadı Pazzi katili Bernardo Bandini(/Baroncelli) ile aynı; akrabalık veya bağ **kaynakta yok**, ad benzerliğinden bağ kurulmaz |
| 5 | c14 | İstanbul satışları | Beklenenin altında; Medici %35, Müteferrika ≈%70 satış oranı (bir kaynağın karşılaştırması) | ○ | K46 | Tek karşılaştırma. Müteferrika 1727 HAFIZA (Y) |
| 6 | c5 | **Konsil'in "Türk tehdidi" gerekçesi** | Bizans İmparatoru VIII. Ioannes birlik teklif etti çünkü Osmanlı tehdidi vardı; vaat edilen yardım gelmedi; 1453'te İstanbul düştü | ◐ | K23 | Medici'nin Konsil'i Floransa'ya çekmesinin arka planı |
| 7 | c5 | 1453 sonrası Rum bilginler | Bessarion, Argyropoulos, Chalcondyles İtalya'da; göç 1453 öncesine uzanır | ◐ | K27 | Mit düzeltmesi (§5.8) |
| 8 | c6 / c8 | Gentile Bellini | Venedik'in ressamı Bellini Mehmed sarayında madalyon yaptı; Bertoldo'nun kaynağı | ◐ | K47 | Yıllar (1479–81) HAFIZA (Y) |
| 9 | c14 | Mısır Memlük hediyesi (zürafa 1487) | Lorenzo'ya Memlük sultanı Kayıtbay'ın zürafa göndermesi | HAFIZA O | — | Osmanlı değil, Doğu rengi. Doğrula |
| 10 | c12 / c14 | Santo Stefano Şövalyeleri, Lepanto, Livorno/Livornina, Cem Sultan, Bandini'nin iadesi | Bu paket dışı; M1/M2/M4 | — | — | Çapraz referans için burada anıldı |

---

## 7. Sahne adayları ("yıldız an")

Her adayda: belgelenmiş çekirdek, duyusal malzeme (yalnız belgeli olan), belirsiz noktalar, kullanım uyarısı. **Kural: iç dünya yalnız kaynaktan.**

### Aday 1: Kubbe, 19 Ağustos 1418 – 25 Mart 1436 (c4)

- **Belgelenmiş çekirdek:** Opera del Duomo yarışmayı 19 Ağustos 1418'de ilan etti, ödül 200 altın florin, teslim Eylül sonu (◐); 1420 baharı Brunelleschi'nin tasarımı seçildi, Ghiberti ortak denetçi, Battista d'Antonio usta (◐); kubbe ahşap kalıpsız yapıldı (◐); 25 Mart 1436'da Eugenius IV katedrali kutsadı (◐).
- **Ses/duyu:** Dufay'ın *Nuper rosarum flores* motetinin iki tenorunda *Terribilis est locus iste* ezgisi; Papa'nın özel korosu; Floransa'da o gün yılbaşı (◐).
- **Belirsiz:** yumurta (ANEKDOT, Vasari); jüri ve Ghiberti'nin gerçek payı; Medici'nin kubbede payı (bulunamadı); kubbenin kapanış/ikinci kutsama tarihi (tek özet).
- **Çerçeve önerisi:** "Vasari yüz yıl sonra yumurtayı anlatacak" tipi mesafe. Yün loncasının bürokrasisi mizah malzemesi olabilir (kuruma yönelik).

### Aday 2: Cosimo ve Papa, "on bin florin" (c4)

- **Belgelenmiş çekirdek:** Vespasiano: Cosimo vicdanındaki yükü atmak için Papa Eugenius'a danıştı; öneri San Marco'ya 10.000 florin; Cosimo toplamda 40.000'den fazla harcadı (◐ ANEKDOT). San Marco'da Cosimo'nun iki hücresi; Magi freski; Niccoli'nin kitaplarının San Marco'ya girişi (◐).
- **Ses/duyu:** Vespasiano çevirisinden doğrudan alıntılar (§3, #1–2); hücrenin freski (taçlarını yemliğe bırakan krallar) (○).
- **Belirsiz:** Vespasiano'nun övgücü tonu; "papalık bulla" yorumu (NYRB, tek özet); gerçek "vicdan" mı "siyaset" mi sorusu; Papa'nın hücrede gecelemesi (○).
- **Çerçeve önerisi:** "Çağdaşlar Cosimo'yu şöyle anlattı…"; kefaret/yatırım sorusunu açık bırak. Mizah: bankacı vicdanı ile defter benzetmesi **yazar sesinin** yorumu olarak, Cosimo'nun sözü gibi sunulmadan.

### Aday 3: Faun'un dişi ve iki burun hikâyesi (c6)

- **Belgelenmiş çekirdek (Condivi 1553):** yaşlı faun başı; Lorenzo'nun diş şakası; Michelangelo'nun dişi çıkarışı; Lorenzo'nun onu evine alması (◐ ANEKDOT). İkinci anlatım (Cellini/Vasari): Torrigiani'nin yumruğu (◐ ANEKDOT).
- **Ses/duyu:** Lorenzo'nun şaka cümlesi (EN çeviri alıntısı, §3 #31); "kemik ve kıkırdak çöktü… hamurdan yapılmış gibi" (§3 #34).
- **Belirsiz:** yıl ve yaş; bahçe "okul" mu; Bertoldo (Condivi'de yok); 5 dukat/mor pelerin (doğrulanmadı); Torrigiani olayının mekânı (Carmine mi Medici çevresi mi).
- **Çerçeve önerisi:** "Michelangelo'nun kendi anlattığı gibi…" + ikinci hikâyeyle çatışma; Lorenzo'nun esprisine yaslanan sıcak sahne.

### Aday 4: Lascaris'in cep defteri, Athos 1491 (c5)

- **Belgelenmiş çekirdek:** Lorenzo Lascaris'i el yazması toplamaya ve II. Bayezid ile pazarlığa gönderdi; Athos ziyareti 1491; cep defteri Vat. gr. 1412'de hem Lorenzo'nun aradığı metinler hem kütüphanenin içeriği; Lascaris 200 el yazması getirdiğini söylüyor, defter bunun neredeyse iki katını listeliyor (◐).
- **Ses/duyu:** cep defterinin kendisi (iki liste: "elimizde olanlar", "aranacaklar"); Athos manastırları (yer isimleri HAFIZA).
- **Belirsiz:** Lorenzo'nun ölümü haberini nerede aldığı; pazarlığın ayrıntısı; "80 yeni metin" iddiası.
- **Çerçeve önerisi:** Türk izleyiciye çıpa: Bir Rum bilgin, Osmanlı topraklarında Floransa'nın kütüphanesini tamamlıyor; mizah kütüphane hırsına/liste tutkusuna yönelir.

### Ek adaylar (kısa)

- **Cosimo'nun Careggi mektubu, 1463 (c5):** "Zihnimi işlemek için"; Ficino'dan Orfik lir; ◐; kısa, sıcak, belgeli (§3 #16).
- **7 Şubat 1497 yığını ve Botticelli miti (c10):** yığın görüntüsü ○, mitin kanıtsızlığı ◐ (§5.12).
- **14 Temmuz 1564: Michelangelo'nun cenazesi (c12):** San Lorenzo, Accademia, Varchi ◐; kapakta 28 Haziran yazmasına rağmen tören 14 Temmuz ○; "mal gibi kaçırılan ceset" ANEKDOT ○.
- **HAFIZA adayları (kaynak doğrulaması bekliyor):** 6 Ekim 1600 *Euridice*; Ocak–Mart 1610 Galileo ve *Medicea Sidera*; 1529–30 Michelangelo'nun hem istihkâmcı hem saklanan (§10).

---

## 8. Okunacak kaynaklar

### 8.1 Künyesi arama sonuçlarında görülenler (içerikleri okunmadı)

| # | Kaynak | Not |
|---|---|---|
| 1 | Ullman, B. L. & Stadter, P. A., *The Public Library of Renaissance Florence: Niccolò Niccoli, Cosimo de' Medici and the Library of San Marco* (1972) | Niccoli vasiyeti, San Marco kitaplığı (K15) |
| 2 | Hankins, J., "The Myth of the Platonic Academy of Florence," *Renaissance Quarterly* 44/3 (Güz 1991), 429–475, doi:10.2307/2862593 | K21 |
| 3 | Hankins, J., "Cosimo de' Medici and the 'Platonic Academy'" (1990) | Dergi adı aramada görülmedi (HAFIZA: *JWCI* 53, O) |
| 4 | Hankins, J., "The Invention of the Platonic Academy of Florence," *Rinascimento* n.s. 42 (2002), 1–39 | K21 |
| 5 | Field, A., *The Origins of the Platonic Academy of Florence* (1988) | Bibliyografide görüldü; yayıncı HAFIZA |
| 6 | Gombrich, E. H., "The Early Medici as Patrons of Art: A Survey of Primary Sources," in *Italian Renaissance Studies*, ed. E. F. Jacob (London: Faber, 1960) | K17 |
| 7 | Gombrich–Kempers yazışması, *New York Review of Books*, 24 Haz 1993, "Painting and Patronage" | K17 |
| 8 | *With and Without the Medici: Studies in Tuscan Art and Patronage 1434–1530* (1998) | Editörler HAFIZA (E. Marchand, A. Wright, O) |
| 9 | Goldthwaite, R. A., *Wealth and the Demand for Art in Italy, 1300–1600* (Johns Hopkins UP, 1993) | K18 |
| 10 | Barzman, K., *The Florentine Academy and the Early Modern State: The Discipline of Disegno* (CUP, 2000) | CAA Reviews #181 (K43). Tam ad HAFIZA: Karen-edis Barzman |
| 11 | Pevsner, N., *Academies of Art, Past and Present* (Cambridge, 1940) | K43 |
| 12 | Sealy, J., "Anatomy and academies of art I: founding academies of art," *Journal of Anatomy* (2020), doi:10.1111/joa.13131 | Anatomi ve akademiler (K43) |
| 13 | Davis, C. (yay.), Benedetto Varchi'nin Michelangelo cenaze orasyonu, *Fontes* 23 (Heidelberg, artdok 643) | Cenaze (K44) |
| 14 | Speake, G., "Janus Lascaris' Visit to Mount Athos in 1491," *Greek, Roman, and Byzantine Studies* | Cilt/yıl görülmedi (K25) |
| 15 | Leuschner, E. & Wolf, G. (yay.), *The Medici Oriental Press: Knowledge and Cultural Transfer around 1600* (Florence: Olschki) | K46 |
| 16 | Condivi, A., *The Life of Michelangelo* (Penn State UP İngilizce baskısı; HAFIZA: ed. H. Wohl, çev. A. S. Wohl, 1999) ve NYRB, 24 Haz 1999, "In Lorenzo's Garden" | K36 |
| 17 | Vespasiano da Bisticci, *The Vespasiano Memoirs: Lives of Illustrious Men of the XVth Century* (İngilizce çeviri; HAFIZA: W. George & E. Waters, 1926) ve Uppsala sayfasındaki Cosimo bölümü | K12 |
| 18 | *The Letters of Marsilio Ficino*, cilt 1 (London: Shepheard-Walwyn; ISBN 9780856835162) | Cosimo'nun Careggi mektubu (K24) |
| 19 | Ferretti, E., Palazzo Medici üzerine Floransa Üniversitesi PDF'i | 1445 belgeleri (K9) |
| 20 | Frommel, C. L., "Palazzo Rucellai" (2006), Heidelberg artdok | K14 |
| 21 | Greenblatt, S., *The Swerve: How the World Became Modern* (2011) | Poggio–Lucretius (K28) |
| 22 | Unger, M. J., *Magnifico: The Brilliant Life and Violent Times of Lorenzo de' Medici* | Valori aktarımı (K40); yıl HAFIZA (2008) |
| 23 | Ross, J., *Lives of the Early Medici as Told in Their Correspondence* (Gutenberg #74973) | Başlık görüldü; yazar HAFIZA. Mektup kaynağı olarak yararlı olabilir |
| 24 | "A Florentine Poetic Anthology (MS Can. Ital. 99)," Bodleian/Oxford | Raccolta Aragonese (K38) |

### 8.2 HAFIZA önerileri (künye doğrulanmadı, yalnız okuma önerisi)

Burckhardt, *Die Cultur der Renaissance in Italien* (1860); Roscoe, *Life of Lorenzo de' Medici* (1796); Baron, *The Crisis of the Early Italian Renaissance* (1955); Kent, *Cosimo de' Medici and the Florentine Renaissance* (2000); Welch, *Art and Society in Italy 1350–1500* (1997); Goldthwaite, *The Building of Renaissance Florence* (1980); Elam, "Lorenzo de' Medici's Sculpture Garden," *MKIF* 36 (1992); Pollens, *The Early Pianoforte* (1995); Van Helden (çev.), *Sidereus Nuncius* (1989); Johansson, *The Medici Effect* (2004); Kristeller'in Ficino çalışmaları.

---

## 9. "Dünyaya etki" iddialarının sağlamlık değerlendirmesi (c16 için)

Her satır: **kanıt ne, abartı nerede, videoda nasıl denir.** Sınıf, "kurum/olgu var mı" sorusunun sınıfıdır; "Medici icat etti/ilk" iddiaları ayrıca değerlendirilir.

| # | İddia | Kanıt (sınıf) | Abartı nerede | Önerilen ifade | Bölüm |
|---|---|---|---|---|---|
| 1 | **Akademi modeli** (Accademia delle Arti del Disegno, 1563) | Kurum var: 13 Oca 1563, Cosimo I, Vasari, Borghini; iki parçalı yapı (compagnia + seçkin akademi); 36 üye; Michelangelo capo; Michelangelo cenazesini düzenledi (◐, K43, K44) | "İlk resmî sanat akademisi" kaynaklarda geçiyor ama Pevsner–Barzman tartışmalı (öğretim işlevi hafife mi alındı?); Carracci ≈1580 (○); San Luca 1577 (HAFIZA); yarı lonca niteliği | "İlk büyük, devlet destekli sanatçı akademilerinden biri; yarı lonca, yarı akademi." "İlk" denmez | c12, c16 |
| 2 | **"Platon Akademisi"** | Cosimo–Ficino desteği, Careggi mektubu (◐); kurum belgesi yok, tüzük/üye kaydı yok (◐, Hankins) | Resmî kurum olarak anlatılması | "Akademi" tırnaklı; "Careggi'de Ficino'nun çevresi" | c5 |
| 3 | **Patronaj modeli** | Medici belgeli büyük patron (Eski Sakristi, San Marco, Niccoli kitaplığı, Ficino, Verrocchio mezarları) (◐); Rucellai, Tornabuoni, Sassetti, Brancacci başka patronlar (◐) | "Medici icat etti / tek patron"; Gombrich'in eleştirisi: Medici'yi tipik saymak (◐) | "En görünür patronlardan biri; ölçek ve siyasi görünürlüğü onları ayırır" (ikinci kısım HAFIZA, kaynakla doğrulanmalı) | c4, c16 |
| 4 | **Müze fikri** (Uffizi) | 1560 ofis → 1581 Tribuna'da özel koleksiyon → 1769 halka açık (◐) | "İlk modern müze" sıfatı kanıtsız; karşı örnekler HAFIZA (Capitoline 1471, Ashmolean 1683, O) | "Ofislerden galeriye, galeriden müzeye: üç basamak." "İlk" denmez | c12, c16 |
| 5 | **Kamu kütüphanesi** | San Marco: Niccoli vasiyeti + Cosimo; Ullman–Stadter başlığı "Rönesans Floransası'nın halk kütüphanesi" (◐); Laurenziana 1571 halka açık (◐) | "İlk halk kütüphanesi" (HAFIZA: Cesena Malatestiana 1454 karşı örnek, O) | "Rönesans Floransası'nın halka açık kitaplığı" | c4, c5 |
| 6 | **Opera** | HAFIZA: *Euridice* 6 Ekim 1600, Pitti, Medici düğünü (Y); Corsi/Bardi/Peri/Rinuccini çevresi (Y) | "Medici icat etti" (icat soylu salon çevresinden, Medici sahne ve düğün) | Doğrulanınca: "Medici düğününde sahnelenen, günümüze ulaşan en eski operalardan biri" | c14 |
| 7 | **Piyano** | HAFIZA: Cristofori, Prens Ferdinando hizmetinde, 1700 envanteri (Y/O) | "Medici icat etti" (icat eden Cristofori; Medici'nin payı iş ve himaye) | Doğrulanınca: "Prens Ferdinando'nun ustası Cristofori" | c14 |
| 8 | **İtalyanca standardı** | Raccolta Aragonese (Lorenzo/Poliziano) prestij (◐); Bembo 1525, Crusca 1583, *Vocabolario* 1612 (◐); Accademia Fiorentina tanınması (○) | "Lorenzo Toskana'yı yazı dili yaptı"; konuşulan birlik çok sonra (HAFIZA) | "Medici, Floransa lehçesinin itibarını ve kurumlarını verdi; standardı Bembo ve Crusca oturttu" | c6, c12 |
| 9 | **Bilim himayesi** | HAFIZA: Galileo 1610 + Cimento 1657 (Y/O) | "Medici bilimi korudu" (1633'te koruma sınırı, HAFIZA); "ilk bilim akademisi" değil (HAFIZA: Lincei 1603, O) | Doğrulanınca: "unvan, maaş, yıldızlara aile adı" üçlüsü | c14 |
| 10 | **Atölye = okul** | Verrocchio atölyesi: Leonardo, Perugino, Botticelli (atıf) (◐); çıraklık ücreti verileri (○) | "Medici sanat okulu" (Faun bahçesi) zayıf (○) | "Okul değil atölyeler; Lorenzo'nun bahçesi antik heykel koleksiyonu" | c6 |
| 11 | **Doğu Dilleri Matbaası** | Roma 1584, Granjon harfleri, Arapça İncil/Kanun/Öklid (◐); 1610'a dek 8 eser (○); satış düşük (○) | "Doğu ile bilgi köprüsü" büyük söz, çıktı sınırlı | "İddialı ama sınırlı bir girişim" | c14 |
| 12 | **Sanat = diplomasi** | Bertoldo–Mehmed madalyonu "olası" (◐); HAFIZA: 1481–82 Sistina ressam heyeti (Y/O) | Madalyonun amacı kesin değil | "Olası bir diplomatik jest" | c6, c8 |
| 13 | **Kurumların sürekliliği** | OPD 1975'ten beri bugün (◐); Uffizi bugün (◐); Studiolo 1920'de yeniden kuruldu (○) | — | "Banka öldü, kurumlar ve nesneler kaldı" (tez cümlesiyle uyumlu) | c16 |
| 14 | **"Medici etkisi"** (Johansson) | HAFIZA: 2004 iş kitabı, metafor (Y) | Tarihsel iddia değil, işletme metaforu | Kullanılırsa "modern bir iş literatürü metaforu" olarak | c16 |
| 15 | **Hümanizm ve kitap** | Niccoli, Poggio, Cosimo'nun borç üstlenmesi, Lascaris'in Doğu seferi (◐); Medici kütüphanesinin 1494–1571 yolculuğu (◐) | "1453'te Rum bilginler geldi" mitini Medici'ye bağlamak (◐ mit) | "Kitaba paranın gittiği, kitabın kapısında Medici'nin durduğu bir şehir" | c5 |

---

## 10. HAFIZA adayları (araçla doğrulanmadı; doğrulama önerisiyle)

> **Uyarı:** Bu bölümdeki her şey benim hafızamdır. Güven: Y = yüksek, O = orta, D = düşük. Hiçbiri senaryoya "doğrulanmış" diye girmemeli. Birebir alıntı **yazılmadı**.

| # | Bölüm | Konu | Hatırladığım çekirdek | Güven | Doğrulama önerisi |
|---|---|---|---|---|---|
| 1 | c14 | Galileo ve *Sidereus Nuncius* | Jüpiter'in uydularını Ocak 1610'da gözledi (7 Ocak ilk, 13 Ocak dördüncü); *Sidereus Nuncius* Mart 1610'da Venedik'te çıktı, Cosimo II'ye ithaflı; uydulara "Medicea Sidera" dedi; yaz 1610'da Büyük Dük'ün "matematikçisi ve filozofu" unvanıyla Pisa/Floransa'ya geçti; Cosimo II'ye 1605–08 yazlarında ders verdiği söylenir | Y (olgu), O (ad tartışması), D (maaş) | Galileo, *Opere*; Van Helden çevirisi; Vinta mektupları |
| 2 | c14 | Medici koruması sınırı | Cosimo II 1621'de öldü; 1633 yargılanmasında Medici koruması yetmedi | O | Galileo biyografileri |
| 3 | c14 | Accademia del Cimento | 1657, Prens Leopoldo ve Ferdinando II; Viviani, Borelli, Redi, Magalotti; *Saggi di naturali esperienze* 1667; Leopoldo kardinal olunca dağıldı | Y/O | Magalotti'nin *Saggi* önsözü; modern özet |
| 4 | c14 | *Euridice* ve opera | 6 Ekim 1600, Pitti Sarayı; libretto Rinuccini; müzik Peri (bazı parçalar Caccini); Maria de' Medici–IV. Henri vekâleten evlilik 5 Ekim 1600; Peri'nin *Dafne*'si 1598, Corsi sarayı, müziği büyük ölçüde kayıp; Camerata de' Bardi (Vincenzo Galilei dahil) | Y | Grove/New Grove; Peri'nin 1600 basımının önsözü |
| 5 | c14 | Cristofori ve piyano | Padovalı (1655–1731); Prens Ferdinando (1663–1713) hizmetinde ≈1688'den; 1700 envanterinde "yeni icat… piano ve forte yapan arpicembalo" kaydı; Scipione Maffei'nin 1711 makalesi (*Giornale de' letterati d'Italia*); hayatta kalan üç piyano: 1720 (Metropolitan, New York), 1722 (Roma), 1726 (Leipzig) | Y/O | Pollens; Met kataloğu |
| 6 | c11 | Yeni Sakristi | Kardinal Giulio de' Medici siparişi (1519/20) Giuliano (Nemours) ve Lorenzo (Urbino) mezarları için; Gece/Gündüz, Şafak/Alacakaranlık; Michelangelo 1520–1534. Giovanni Strozzi'nin Gece heykeli üzerine dörtlüğü ve Michelangelo'nun cevabı (Floransa'nın özgürlüğü üzerine). Metin doğrulanmadı | Y (sipariş), O (dörtlük) | Michelangelo, *Rime*; Vasari |
| 7 | c11 | 1529–30 | 6 Nis 1529 istihkâm genel sorumlusu; San Miniato; Eyl 1529'da Venedik'e kaçış, Cumhuriyet'in onu isyancı ilan etmesi, Kasım'da dönüş; 12 Ağu 1530 teslim; Condivi'ye göre San Niccolò çan kulesinde saklanma; VII. Clemens'in affı; 1975'te Yeni Sakristi altında kömür çizimli gizli oda keşfi (tarihlendirme ve Michelangelo'ya atıf tartışmalı) | O | Condivi; Dal Poggetto yayınları |
| 8 | c11 | Laurenziana merdiveni | Michelangelo'nun tasarımı Roma'dan modellerle; Ammannati uyguladı (1559); Michelangelo'nun merdiveni "bir rüya gibi" hatırladığını söyleyen mektup (Vasari aktarır). Metin doğrulanmadı | O | Vasari, *Vite* |
| 9 | c11 | Machiavelli | Şubat 1513 hapis ve işkence; *Prens* 1513 (10 Ara 1513 tarihli Vettori mektubu); 1516'da ithaf Lorenzo di Piero'ya (ilk niyet Giuliano); *Istorie fiorentine*: Kardinal Giulio'nun siparişi (1520), VII. Clemens'e sunum (1525/26); *Prens* 1532'de Blado'dan, papalık imtiyazıyla | Y/O | Machiavelli, *Lettere*; ithaf metni |
| 10 | c16 | *Assassin's Creed II* | Ubisoft Montréal, Kasım 2009; kurgusal Ezio Auditore; Pazzi komplosu Templar çerçevesine oturtulmuş; Rodrigo Borgia Templar lideri; Leonardo müttefik/mucit; DLC *Bonfire of the Vanities* (2010, Savonarola); seride açılışta "çok kültürlü bir ekip" uyarı cümlesi. **Oyunun tarihe sadakat/sapma haritası bu aramada çıkarılamadı.** Resmî açıklama/röportaj öncelikli | O | Ubisoft basın bültenleri; *The Art of Assassin's Creed II*; geliştirici röportajları; Animus Database girdileri |
| 11 | c16 | "Medici: Masters of Florence" | Rai ve Lux Vide ortak yapımı; 2016–2019, 3 sezon; yaratıcılar Frank Spotnitz ve Nicholas Meyer; Cosimo (Richard Madden), Giovanni di Bicci (Dustin Hoffman), Lorenzo (Daniel Sharman) | O | Yapımcı açıklamaları; tarihçi eleştirileri |
| 12 | c16 | "Medici etkisi" | Frans Johansson, *The Medici Effect* (2004): farklı alanların kesişiminde yenilik; Medici'yi metafor kullanır | Y | Kitabın girişi |
| 13 | c12 | Boboli ve Pitti | 1549 Eleonora di Toledo Pitti'yi satın aldı; Tribolo (1550); Ammannati, Buontalenti (Grotta Grande ≈1583–93); 1766'da halka açık; Marie de' Medici'nin Luxembourg Sarayı Pitti'den esinlenir (Salomon de Brosse) | O | Pitti/Boboli resmî siteleri |
| 14 | c12 | Vasari Koridoru | 1565'te ≈5 ayda, Francesco ve Johanna'nın düğünü için; ≈760 m | O | Uffizi resmî sayfası |
| 15 | c4 | Magi Şapeli | Benozzo Gozzoli, 1459–61, Palazzo Medici şapelinde; Konsil'in Bizanslı heyetinin yüzleri (VIII. Ioannes, Patrik Ioseph) Medici portreleriyle iç içe; yüz kimlikleri tartışmalı | Y/O | Palazzo Medici Riccardi sitesi |
| 16 | c4 | "Magnificence" doktrini | Aristoteles *Nikomakhos'a Etik* IV ("megaloprepeia"); Aquinas; Bruni'nin Etik çevirisi (1416/17); Pontano *De magnificentia* (1498); Medici patronajı bu okumayla savunulabilir | Y (genel), O (ayrıntı) | Welch, Goldthwaite, Kent |
| 17 | c4 | Lorenzo'nun harcama özeti | Medici'nin 1434–1471 arası ≈663.755 florini "hayır, bina ve vergi"ye harcadığı, Lorenzo'nun *Ricordi*'sinde paranın iyi harcandığı duygusuyla yazıldığı söylenir | O | Lorenzo, *Ricordi*; de Roover, *Rise and Decline of the Medici Bank* |
| 18 | c4 | Michelozzo ve Venedik | Cosimo'nun 1433–34 Venedik sürgününde Michelozzo yanındaydı; San Giorgio Maggiore'de bir kütüphane yaptı | O | Michelozzo monografileri |
| 19 | c4 | San Lorenzo | Cosimo'nun 1440'ların başında yeniden inşayı üstlenmesi; Brunelleschi 1446'da öldü; Cosimo'nun mezarı yüksek sunak önünde | O | Kent; San Lorenzo resmî sitesi |
| 20 | c4 | Kubbe boyutları | ≈4 milyon tuğla; haçla ≈114,5 m; iç çap ≈45 m (kaynaklar 41–45 m arası); fener ≈1446–61; top (Verrocchio) 1468–71; çalışma platformları ve vinçler vardı | O | Ross King, *Brunelleschi's Dome*; Opera del Duomo |
| 21 | c5 | Plethon | Georgios Gemistos Plethon; Floransa'da 1438–39; Platon ile Aristoteles'in farkı üzerine yazı; "Plethon" adının "Platon" ile söz oyunu olduğu söylenir | O | Hankins, *Plato in the Italian Renaissance* |
| 22 | c5 | Argyropoulos ve Chalcondyles | Argyropoulos Floransa Studio'sunda 1456'dan itibaren; Chalcondyles 1475–91 | O | Wilson, *From Byzantium to Italy* |
| 23 | c5 | Pico ve Poliziano 1494 | İkisi de 1494'te öldü; 2007'de mezar incelemesinde arsenik tartışması basına yansıdı | D | Yalnızca ciddi bilimsel yayın bulunursa |
| 24 | c6 | Lorenzo'nun 1492 envanteri | Ölümünden sonra *Libro d'inventario* (Müntz 1888 yayını); mücevher, vazo, heykel; değerli kalemler | O | Spallanti yayını |
| 25 | c6 / c8 | Sistina misyonu 1481–82 | Sixtus IV ile barış sonrası Lorenzo, Botticelli, Ghirlandaio, Perugino, Cosimo Rosselli'yi Roma'ya gönderdi; diplomatik hediye olarak okunur | Y/O | Sistina Şapeli kataloğu |
| 26 | c6 | Lorenzo'nun 1469 turnuvası | Şubat 1469 Santa Croce; Luigi Pulci'nin *Giostra*'sı; Clarice Orsini nişanı bağlamı | Y/O | Pulci |
| 27 | c12 | Vasari ve "Floransa'nın önceliği" | *Vite* (1550, 1568) Floransa merkezli yeniden doğuş anlatısı, Cosimo I sarayında yazıldı; "Medici Rönesans'ı yarattı" tezinin tarih-yazımsal köklerinden biri | Y (olgu), yorum | Vasari'ye ilişkin eleştirel yayınlar |
| 28 | c12 | Cellini'nin *Perseus*'u | 1545–54, Cosimo I için; Piazza della Signoria | Y | — |
| 29 | c4 | Lippi–Cosimo | Vasari'de Cosimo'nun Lippi'yi kilitlemekten vazgeçip "seçkin kişilerin baskıyla yönetilemeyeceğini" anlaması | O | Vasari, *Vita di Fra Filippo Lippi* |
| 30 | c5 | Malatestiana | Cesena 1454, "ilk belediye kütüphanesi" iddiası; San Marco'ya karşı örnek | O | Kütüphane resmî sitesi |

---

## 11. Eksik kalan başlıklar ve takip listesi

**Neden eksik:** (1) WebFetch hiç çalışmadı → birincil metin yok; (2) WebSearch kotası (200/tur, ajanlar arası paylaşımlı) Galileo sorgusunda bitti.

### 11.1 Aramasız kalan başlıklar (görev listesindeki madde numaralarıyla)

- **(6) Bilim ve müzik:** Galileo/Cosimo II/*Sidereus Nuncius* ve "Medici yıldızları"; Accademia del Cimento; Peri'nin *Euridice*'si; Cristofori ve piyano → **hepsi yalnızca HAFIZA (§10 #1–5)**.
- **(7) Mimari/Medici Şapeli:** Yeni Sakristi, Laurenziana merdiveni (kütüphane tarihi ◐ hariç), 1529–30 → **yalnız HAFIZA (§10 #6–8)**.
- **(8) "Medici'nin ilham kaynağı olduğu şeyler":** Machiavelli, "Medici etkisi", *Assassin's Creed II* ve dizi → **yalnız HAFIZA (§10 #9–12)**; oyun için resmî açıklama/röportaj aranmadı.
- **(1) Kubbe/patronaj:** San Marco'da Michelozzo kütüphanesi (aramada çıkmadı), "papalık bulla" iddiası, "magnificence" doktrini (HAFIZA); **Strozzi (saray, şapel) ve Pazzi Şapeli (Santa Croce) patronajı**: sorguda yer aldı ama sonuç çıkmadı; Burckhardt'tan Kent ve Welch'e tarihçi tartışmasının kendi cümleleri; kubbe boyutları ve inşa teknolojisi için ciddi kaynak (Opera del Duomo, King, Saalman vb.).
- **(2) Hümanizm:** Plethon'un Floransa söylevleri ayrıntısı; Pico ve Poliziano; Bruni; Medici'nin Konsil'i çekmedeki payının **birincil kanıtı** (Cosimo'nun teklifi hangi belgede).
- **(3) Lorenzo:** Leonardo lir rivayetinin ilk kaynakları (Anonimo Gaddiano, Vasari); Michelangelo'nun hane içindeki yılları ve ücreti; Verrocchio'nun Lorenzo ile ilişkisi; Lorenzo'nun karakteri için Poliziano/Pico çevresi tanıklıkları.
- **(4) Savonarola ve sanat:** Landucci günlüğü ve Burlamacchi metinleri; Vasari'nin Botticelli yaşamının gerçek metni.
- **(5) Kurumlar:** Accademia'nın öğretim içeriği (anatomi, geometri dersleri; Sealy 2020 makalesi bulundu ama içeriği okunmadı) ve 1563 *Capitoli*; **sonraki akademilere (Roma San Luca, Paris Académie royale vb.) etkisi** hiç aranmadı; Boboli (yalnız HAFIZA).
- **(9) Sağlamlık:** Burckhardt, Kent, Welch'in kendi sözleri; "ilk müze/ilk akademi" için karşı örneklerin kaynakları.

### 11.2 Kota açılırsa önerilen takip sorguları (öncelik sırasıyla)

1. `Sidereus Nuncius 1610 dedication Cosimo II Medicean Stars Galileo letter Vinta Cosmica Medicea` (extended)
2. `Galileo appointed philosopher mathematician Grand Duke 1610 salary scudi`
3. `Peri Euridice 6 October 1600 Pitti wedding Maria de' Medici Rinuccini Dafne 1598`
4. `Cristofori 1700 Medici inventory piano e forte Maffei 1711 Ferdinando`
5. `Accademia del Cimento 1657 members Saggi 1667 dissolved Leopoldo cardinal`
6. `Michelangelo 1529 fortifications siege fled Venice hidden room New Sacristy 1975` (extended)
7. `Michelangelo New Sacristy Giulio de' Medici 1519 Night Strozzi quatrain Caro m'è 'l sonno`
8. `Assassin's Creed II Pazzi conspiracy historical accuracy Ubisoft historian interview` (extended)
9. `Medici Masters of Florence historical accuracy historians Spotnitz` 
10. `Machiavelli Prince dedication Lorenzo di Piero Vettori letter 10 December 1513; Istorie fiorentine commission Giulio`
11. `Vasari Life of Botticelli Savonarola piagnone text` ve `Vasari Life of Filippo Lippi Cosimo locked celestial forms`
12. `Burckhardt Medici patronage; Kent Cosimo de' Medici and the Florentine Renaissance review; Welch Art and Society in Italy patronage`
13. `Lascaris 1492 return after Lorenzo's death; Lascaris "eighty" manuscripts unknown`
14. `Lorenzo de' Medici Ricordi 663,755 florins`
15. `Benozzo Gozzoli Magi Chapel Council of Florence portraits`
16. `Boboli Gardens history Tribolo 1550 public 1766; Vasari Corridor five months 1565`
17. `Capitoline Museums first public museum 1471; Uffizi first museum claim`
18. Birincil metinler için WebFetch çalışırsa: Vespasiano (Cosimo ve Eugenius), Condivi (Faun), Cellini (Torrigiani), Vasari (Brunelleschi, Botticelli, Lippi), Lorenzo'nun *Canzona*'sı, Cosimo'nun Careggi mektubu (Latince) → **● sınıfı için tek yol**.

### 11.3 Senaryo yazarı için doğrulama önceliği

1. Vespasiano'nun Cosimo/Eugenius pasajı (c4'ün ana sahnesi).
2. Condivi (Faun) ve Cellini/Vasari (Torrigiani), kaynak çatışması sahnesi için.
3. Speake'in Lascaris makalesi (TR-BAĞ çıpası).
4. Galileo, *Euridice*, Cristofori (c14'ün üç ana taşı, şu an HAFIZA).
5. Hankins 1991 (c5 "Akademi" tırnak mantığı).

---

## 12. Kaynak anahtarı (K etiketleri)

> **Not:** Bunlar arama aracının döndürdüğü sayfalardır; **hiçbiri açılıp okunmadı**. Özetler arama aracı tarafından üretildi. Bir konudaki K etiketi, o konu sorgusunda dönen sayfaları ifade eder; hangi cümlenin hangi sayfadan geldiğini ayrıştıramadım. Kalite notları: blog/rehber = düşük; Wikipedia = orta (özet düzeyi); müze/üniversite/dergi = yüksek.

- **K1** (kubbe yarışması; blog düzeyi): https://www.odysseytraveller.com/articles/brunelleschis-dome-renaissance-genius/ · https://coloradobiz.com/?p=14797 · https://areademo.beculture.it/en/?p=25049
- **K2** (yumurta; The Critic, Trachtenberg incelemesi): https://thecritic.co.uk/brunelleschis-egg/
- **K3** (kubbe/lonca): https://www.italianartsociety.org/2017/06/florence-is-dominated-by-the-silhouette-of-its-cathedral-dome/ · https://www.worldhistory.org/audioplayer/en/1-19124/ · https://www.nationalgeographic.com/magazine/article/Il-Duomo
- **K4** (Museo Galileo/IMSS): https://brunelleschi.imss.fi.it/itineraries/multimedia/FilippoBrunelleschi.html
- **K5** (rehber): https://www.headout.com/blog/duomo-florence-history/ · https://www.headout.com/blog/wp-json/wp/v2/posts/173846
- **K6** (blog): https://www.mencher.blog/2026/02/15th-century-art-brunelleschi.html · https://internal-mongodb.champds.com/archive-ga-23-10/brunelleschi-s-dome.pdf · https://www.studiomatrx.org/architecture-canon/florence-cathedral-dome
- **K7** (kutsama, Dufay): https://en.wikipedia.org/wiki/Florence_Cathedral · https://en.wikipedia.org/wiki/Nuper_rosarum_flores · https://www.diamm.ac.uk/documents/175/09_Du_Fay_Nuper_rosarum_flores.pdf · https://interlude.hk/reverberating-devotionthe-basilica-di-santa-maria-del-fiore-and-guillaume-dufay/ · https://www.fhs-sw1.org.uk/news/fhs-musical-moment-nuper-rosarum-flores-by-guillaume-dufay
- **K8** (Eski Sakristi): https://smarthistory.org/brunelleschi-old-sacristy-san-lorenzo-florence/ · https://www.medievalists.net/2011/04/the-ornamentation-of-brunelleschis-old-sacristy-of-san-lorenzo-in-florence/ · https://repository.lsu.edu/gradschool_theses/610 · https://centaur.reading.ac.uk/73388 · https://artibusethistoriae.org/chapter304.html · https://hiddenflorence.org/stories/cosimo/3-microcosm-of-community/
- **K9** (Palazzo Medici): https://flore.unifi.it/retrieve/handle/2158/1039731/131850/Ferretti%20palazzo%20medici.pdf · https://www.studiomatrx.org/architecture-canon/palazzo-medici-riccardi · https://www.visittuscany.com/fr/attractions/palazzo-medici-riccardi/ · https://www.italyonthisday.com/search/label/Michelozzo · https://www.studentessamatta.com/medici-palace-florence-michelozzo-lorenzo-magnifico-history-fun-facts/
- **K10** (Donatello *David*): https://en.wikipedia.org/wiki/David_(Donatello,_bronze) · https://smarthistory.org/?p=1524 · https://www.sav.sk/journals/uploads/12201424ars2022-2_Mrazova_web.pdf · https://quattrocentoitalia.artinterp.org/omeka/items/show/108 · https://m.caareviews.org/reviews/39
- **K11** (San Marco hücresi): https://en.wikipedia.org/wiki/Cosimo_de%27_Medici%27s_cell · https://en.wikipedia.org/wiki/Adoration_of_the_Magi_(San_Marco) · https://digi.ub.uni-heidelberg.de/diglit/singleton1929/0063 · https://brunelleschi.imss.fi.it/itineraries/gallery/MuseoSanMarco_32084.html · https://professor-moriarty.com/info/node/1552
- **K12** (Vespasiano, Cosimo, kefaret): http://www2.idehist.uu.se/distans/ilmh/Ren/flor-medici-vesp.htm · https://brewminate.com/god-power-and-money-did-cosimo-demedici-deceive-renaissance-florence/ · https://www.scielo.sa.cr/scielo.php?script=sci_arttext&pid=S2215-24582013000300012 · https://www.nybooks.com/articles/2002/12/19/the-cosimos/ · https://fis.uni-bamberg.de/bitstreams/a8bd97b4-c1b1-4986-b040-917f923f4ab5/download · https://www.italianrenaissanceresources.com/units/unit-5/essays/the-special-case-of-the-medici-experts-in-self-promotion/ · https://dc.etsu.edu/cgi/viewcontent.cgi?article=5386&context=etd · https://en.wikipedia.org/wiki/Vespasiano_da_Bisticci
- **K13** (Cosimo'ya atfedilen söz; PBS): https://www.pbs.org/empires/medici/show/prog1.html
- **K14** (Rucellai): https://en.wikipedia.org/wiki/Giovanni_di_Paolo_Rucellai · https://en.wikipedia.org/wiki/Palazzo_Rucellai · https://archiv.ub.uni-heidelberg.de/artdok/8358/1/Frommel_Palazzo_Rucellai_2006.pdf · https://www.italianrenaissanceresources.com/?p=2156
- **K15** (Niccoli): https://www.ellopos.net/politics/renaissance/3-classics.asp?pg=3 · https://words.fromoldbooks.org/Chalmers-Biography/n/niccoli-niccolo-lat-nicolaus.html · https://search.ub.tum.de/vufind/Record/DE-604.BV002479932 · https://catalog.folger.edu/record/55109 · https://works.wellcomecollection.org/works/zesaw8e8
- **K16** (Lippi): https://en.wikipedia.org/wiki/Lucrezia_Buti · https://pratoturismo.it/en/what/itineraries/discovering-the-lippi · https://museicapitolini.org/en/node/1013669
- **K17** (Gombrich, patronaj tartışması): https://www.erudit.org/fr/revue/racar/2003/v28/n/1069792ar.pdf · https://www.nybooks.com/articles/1993/06/24/painting-and-patronage/ · https://www.crcpress.com/cpd/cpd-form/9781859284230 · https://cour-de-france.fr/article4317.html
- **K18** (Goldthwaite): https://www.amazon.co.uk/Wealth-Demand-Art-Italy-1300-1600/dp/0801852358 · https://academic.oup.com/ahr/article-abstract/99/1/174/74212 · https://www.tandfonline.com/doi/abs/10.1080/03612759.1995.9951018 · https://www.semanticscholar.org/paper/Wealth-and-the-demand-for-art-in-Italy,-1300-1600-Goldthwaite/ab5016b6e490cea59cf5db18ec2f59e120985283
- **K19** (Tornabuoni, Sassetti): https://en.wikipedia.org/wiki/Giovanni_Tornabuoni · https://en.wikipedia.org/wiki/Tornabuoni_Chapel · https://www.fordham.edu/Halsall/basis/vasari/vasari11.asp · https://www.britishmuseum.org/collection/object/P_1866-0714-9 · https://archiv.ub.uni-heidelberg.de/artdok/8208/1/Pfisterer_Florence_1485_2018.pdf
- **K20** (Brancacci): https://cultura.comune.firenze.it/system/files/2022-01/CB_Depliant_eng-LR.pdf · https://www.finestresullarte.info/en/ancient-art/florence-brancacci-chapel-undergoes-monitoring-work · https://www.finestresullarte.info/en/works-and-artists/the-brancacci-chapel-the-new-look-at-painting · https://www.theflorentine.net/2021/11/25/restoration-to-begin-on-the-brancacci-chapel/ · https://www.ancient-history-sites.com/sites/brancacci-chapel/
- **K21** (Hankins): https://www.cambridge.org/core/journals/renaissance-quarterly/article/abs/myth-of-the-platonic-academy-of-florence/779C22CBAFFC0835B8E13539239FFCBC · https://scholar.harvard.edu/jameshankins/publications/myth-platonic-academy-florence · https://www.semanticscholar.org/paper/Cosimo-de'-Medici-and-the-'Platonic-Academy'-Hankins/057ff82362950aa283b5074ef6292d9883137769 · https://dash.harvard.edu/server/api/core/bitstreams/7312037c-58f5-6bd4-e053-0100007fdf3b/content · https://www.researchgate.net/publication/296630392_The_invention_of_the_Platonic_Academy_of_Florence · https://en.wikipedia.org/wiki/Platonic_Academy_(Florence)
- **K22** (Ficino, Plethon): https://www.encyclopedia.com/humanities/encyclopedias-almanacs-transcripts-and-maps/florentine-academy · https://www.newworldencyclopedia.org/entry/Marsilio_Ficino · https://Www.Wikipedia.org/wiki/Ficino
- **K23** (Konsil): https://en.wikipedia.org/wiki/Council_of_Florence · https://en.wikipedia.org/wiki/Bull_of_Union_with_the_Greeks · https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/florence-council · https://orthodoxwiki.org/Council_of_Florence · https://search.library.wisc.edu/digital/AXM6SCNSNSQBQB85/text/AWG5MMHPR2TLVR8N
- **K24** (Cosimo'nun Careggi mektubu): https://sourcelibrary.org/book/epistolae-ficinus/page/69dbc9f71040d1d5e20a8138 · https://www.akademika.no/letters-marsilio-ficino/9780856835162 · https://plato.stanford.edu/archives/sum2025/entries/ficino/ · https://jonwilson9.substack.com/p/the-magic-of-the-orphic-hymns
- **K25** (Lascaris): https://grbs.library.duke.edu/index.php/grbs/article/download/3411/5739/0 · https://www.semanticscholar.org/paper/Janus-Lascaris%E2%80%99-Visit-to-Mount-Athos-in-1491-Speake/90047471561b87cad032d2a5800362efa76904ce · https://en.wikipedia.org/wiki/Janus_Lascaris · https://www.britannica.com/biography/John-Lascaris-Greek-scholar · https://www.catholicity.com/encyclopedia/l/lascaris,janus.html
- **K26** (Medici kütüphanesi, Laurenziana): https://britannica.com/topic/Medicean-Laurentian-Library · https://flore.unifi.it/retrieve/e398c378-f0aa-179a-e053-3705fe0a4cff/17.pdf · https://blog.fua.it/?p=619 · https://www.latoscanadileonardo.it/en/places/metropolitan-city-of-florence/municipality-of-florence/biblioteca-mediceo-laurenziana-en.html · https://brunelleschi.imss.fi.it/itineraries/place/BibliotecaMediceaLaurenziana.html
- **K27** (Rum bilginler): https://en.wikipedia.org/wiki/Greek_scholars_in_the_Renaissance · https://greekreporter.com/2024/04/01/greatest-byzantine-greek-scholars-renaissance/ · https://www.ellopos.net/politics/european-history/22-renaissance.asp?pg=7
- **K28** (Poggio): https://kathleenmccook.substack.com/p/poggio-finds-a-manuscript · https://www.librarything.com/work/455583 · https://shelf-awareness.com/readers/2011-09-30/the_swerve:_how_the_world_became_modern.html
- **K29** (*Primavera*, *Venüs*): https://digitalcommons.lindenwood.edu/cgi/viewcontent.cgi?article=1057&context=theses · https://en.wikipedia.org/wiki/Pallas_and_the_Centaur · https://www.medievalists.net/2012/10/botticellis-primavera-and-the-poetic-imagination-of-italian-renaissance-art/ · https://en.wikipedia.org/wiki/Lorenzo_di_Pierfrancesco_de%27_Medici · https://en.wikipedia.org/wiki/Villa_di_Castello · https://www.sandro-botticelli.com/primavera.jsp
- **K30** (Botticelli 1478, Pazzi cezası): https://www.thesmartset.com/?p=1260 · https://ebsco.com/research-starters/politics-and-government/pazzi-conspiracy · https://www.finestresullarte.info/en/works-and-artists/the-pazzi-conspiracy-the-event-that-forever-changed-the-face-of-florence-and-italy-history-through-art · https://sacred-texts.com/aor/dv/0664.htm · https://www.fromoldbooks.org/R.bak/section-10/item-664.html (Leonardo'nun Baroncelli çizimi notu; içeriği okunmadı)
- **K31** (Verrocchio atölyesi, Lorenzo di Credi): https://eclecticlight.co/2019/03/17/leonardo-the-apprentice-verrocchios-pupils/ · https://prestelpublishing.penguinrandomhouse.de/leseprobe/Leonardo-da-Vinci/leseprobe_9783791384979.pdf · https://gardnermuseum.emuseum.com/people/1050/lorenzo-di-credi · https://www.electrummagazine.com/?p=1710
- **K32** (Cennini, çıraklık): https://www.nationalgallery.org.uk/paintings/glossary/cennino-cennini · https://www.shafe.co.uk/essay_panel_painters_workshop/ · https://www.britishinstitute.it/en/history-of-art/trecento-cennino · https://historyrise.com/article/the-impact-of-apprenticeship-on-craftsmanship-in-renaissance-italy/
- **K33** (Leonardo, lir, mektup): https://catchlight.blog/2019/02/22/leonardos-horse-head-lyre/ · https://www.discoveringdavinci.com/learn/cast/cast/lorenzo-medici.html · https://en.wikipedia.org/wiki/Letter_from_Leonardo_da_Vinci_to_Ludovico_Sforza · https://www.italianrenaissanceresources.com/units/unit-8/essays/milan/
- **K34** (Faun): https://en.wikipedia.org/wiki/Head_of_a_Faun · https://arte2000.it/en/blog-en/marble-faun-head-michelangelo-genius/ · https://www.pbs.org/empires/medici/renaissance/michelangelo.html · https://baffledtimetravel.com/head-of-a-faun-michelangelo/ · https://www.rightattitudes.com/2025/02/17/michelangelo-won-lorenzo-de-medici-patronage/
- **K35** (Torrigiani): https://en.wikipedia.org/wiki/Pietro_Torrigiano · https://en.wikisource.org/wiki/1911_Encyclop%C3%A6dia_Britannica/Torrigiano,_Pietro · https://words.fromoldbooks.org/Chalmers-Biography/t/torrigiano-peter.html · https://itatti.harvard.edu/node/8646
- **K36** (bahçe, Elam, Bertoldo): https://www.nybooks.com/articles/1999/06/24/in-lorenzos-garden/ · https://www.tandfonline.com/doi/full/10.1080/14601176.2024.2327947 · https://en.wikipedia.org/wiki/Bertoldo_di_Giovanni · https://ericwedwards.wordpress.com/2013/12/14/michelangelo-sculpture-and-architecture-for-the-medici/ · https://getbacklauretta.com/2018/06/08/lorenzo-de-medicis-sculpture-garden/
- **K37** (*Canzona di Bacco*): https://libreriamo.it/poesie/canzona-di-bacco-lorenzo-de-medici-giovinezza/ · https://laspada.altervista.org/wp-content/uploads/2016/05/trionfo_di_bacco_e_arianna.pdf · https://sololibri.net/Trionfo-di-Bacco-e-Arianna-Lorenzo-De-Medici-testo-analisi-parafrasi.html · https://www.studenti.it/la-canzona-di-bacco-lorenzo-de-medici-commento.html
- **K38** (Raccolta Aragonese): https://www.cabinet.ox.ac.uk/node/10033 · https://www.britannica.com/biography/Politian · https://theconversation.com/how-a-lost-manuscript-revealed-the-first-poets-of-italian-literature-150777 · https://ojs.ppke.hu/verbum/article/download/587/606/825 · https://it.wikisource.org/wiki/Pagina:Lorenzo_de%27_Medici_-_Opere,_vol.2,_Laterza,_1914.djvu/359
- **K39** (Giostra, Simonetta): https://en.wikipedia.org/wiki/Simonetta_Vespucci · https://www.theflorentine.net/?p=5363 · https://dailyartmagazine.com/?p=113178 · https://eclecticlight.co/2017/11/08/faces-of-the-distant-past-botticelli-the-medicis-and-ephemeral-beauty/ · https://diariodiunfiorentino.altervista.org/la-bella-simonetta-vespucci/
- **K40** (Lorenzo'nun görünüşü): https://en.wikipedia.org/wiki/Lorenzo_de'_Medici · https://www.florencecity.it/il-magnifico-lorenzo-e-il-suo-matrimonio/ · https://www.firefiandre.be/artikels/hoe-zag-lorenzo-il-magnifico-er-werkelijk-uit · https://www.goodreads.com/book/show/2715456-magnifico · https://www.amazon.com/Magnifico-Brilliant-Violent-Lorenzo-Medici-ebook/dp/B000SIQMNS
- **K41** (Kibirlerin Yakılması, Botticelli): https://en.wikipedia.org/wiki/Bonfire_of_the_vanities · https://www.sothebys.com/en/articles/reflections-of-a-world-in-crisis-art-in-florence-circa-1492-1512 · https://www.smithsonianmag.com/smart-news/when-fanatical-monk-took-over-florence-and-burned-bunch-vanities-180962005/ · https://www.historytoday.com/node/56978 · https://www.thegadflymagazine.org/home-1/bonfire-of-the-botticellis · https://apollo-magazine.com/botticelli-in-the-fire-hampstead-theatre/
- **K42** (Uffizi, Vasari Koridoru): https://brunelleschi.imss.fi.it/itineraries/place/GalleriaUffizi.html · https://uffizi.it/en/artworks/i-corridoi-di-galleria · https://simple.wikipedia.com/wiki/Uffizi · https://dome.mit.edu/handle/1721.3/123340?show=full
- **K43** (Accademia del Disegno): https://www.storiadifirenze.org/?temadelmese=gennaio-1563-nasce-laccademia-delle-arti-del-disegno · https://www.academia.edu/127549633/The_Institution_of_the_Accademia_delle_Arti_del_Disegno_in_Medici_Florence_Protagonists_Locations_and_Controversies · https://www.academia.edu/40745130/Cosimo_I_de_Medici_and_the_Formation_of_the_Accademia_delle_Arti_del_Disegno_Florence_1563_ · https://en.wikipedia.org/wiki/Accademia_delle_Arti_del_Disegno · https://en.wikipedia.org/wiki/Accademia_di_Belle_Arti_di_Firenze · http://www.caareviews.org/reviews/181 · https://onlinelibrary.wiley.com/doi/10.1111/joa.13131 · http://www.visual-arts-cork.com/history-of-art/academy-of-art-florence.htm
- **K44** (Michelangelo'nun cenazesi): https://archiv.ub.uni-heidelberg.de/artdok/643/1/Davis_Fontes23.pdf · https://arte.it/calendario-arte/firenze/mostra-ad-uso-di-mercanzia-michelangelo-trafugato-rievocazione-delle-onoranze-funerali-in-gloria-di-michelangelo-buonarroti-9448 · https://www.arte.it/notizie/firenze/450-di-michelangelo-oggi-a-firenze-una-notte-per-lui-9595 · https://colenda.library.upenn.edu/catalog/81431-p3rj4918w · https://www.dailyartmagazine.com/?p=254051
- **K45** (Crusca, Bembo, Fiorentina): https://en.wikipedia.org/wiki/Questione_della_lingua · https://moodle2.units.it/pluginfile.php/497124/mod_resource/content/1/lezione%2012%20-%2010.11.2022.pdf · https://www.diacronia.ro/indexing/details/A12912/pdf · https://wydawnictwo.pan.pl/index.php/kn/article/download/1180/932/4500 · https://periodicos.fclar.unesp.br/letras/article/download/13794/10771/48737
- **K46** (Medici Doğu Matbaası, Osmanlı): https://en.wikipedia.org/wiki/Medici_Oriental_Press · https://www.historyofinformation.com/detail.php?id=361 · https://borderlines-cssaame.org/posts/2023/8/9/whats-in-a-font-pathways-of-the-medici-oriental-press-arabic-typeface · https://www.jhiblog.org/2018/11/02/from-the-archive-the-early-history-of-arabic-printing-in-europe/ · https://inlibris.com/item/bn57189/ · https://www.invaluable.com/auction-lot/four-publications-of-the-first-printing-press-in--1211-c-04b49b89c8 · https://en.olschki.it/libro/9788822267924 · https://pure.manchester.ac.uk/ws/portalfiles/portal/188475254/5000140104_5000223054_1_SM.pdf · https://www.degruyterbrill.com/document/doi/10.1515/9783111386621-003/pdf?licenseType=open-access · https://www.ageofinvention.xyz/p/age-of-invention-did-the-ottomans · https://religionculturesociety.com/wp-content/uploads/2019/05/s1__schwartz_did-ottoman-sultans-ban-print.pdf · https://www.ebsco.com/research-starters/language-and-linguistics/first-arabic-printing-press/
- **K47** (Bertoldo, Mehmed madalyonu): https://collections.vam.ac.uk/item/O134080/mehmed-ii-medal-di-giovanni-bertoldo · https://www.metmuseum.org/art/collection/search/460839 · https://www.metmuseum.org/art/collection/search/461519 · https://frick.org/exhibitions/bertoldo/15b · https://www.frick.org/exhibitions/bertoldo/15a · https://www.artfund.org/our-purpose/art-funded-by-you/mehmed-ii-sultan-of-turkey · https://www.nga.gov/collection/artist-info.2027.html
- **K48** (Studiolo, Medici porseleni): https://en.wikipedia.org/wiki/Studiolo_of_Francesco_I · https://www.cabinet.ox.ac.uk/studiolo-francesco-i-de-medici-introduction · https://www.rocaille.it/studiolo-francesco-i-de-medici/ · https://museionline.info/firenze-musei-e-monumenti/studiolo-di-francesco-i · https://www.palazzo-pitti.net/the-studiolo-of-francesco-i.html · https://www.conceptualfinearts.com/cfa/?p=4919
- **K49** (Opificio delle Pietre Dure): https://opificiodellepietredure.cultura.gov.it/en/museum/the-opificio-delle-pietre-dure-museum-history/ · https://opificiodellepietredure.cultura.gov.it/en/the-institute/ · https://collections.vam.ac.uk/item/O61542/ · https://en.wikipedia.org/wiki/Opificio_delle_pietre_dure · https://dgeric.cultura.gov.it/en/?p=122 · https://www.visittuscany.com/en/attractions/opificio-delle-pietre-dure-museum/
- **K50** (Medici mektupları, kaynak olarak): https://www.gutenberg.org/files/74973/74973-h/74973-h.htm (başlık: *Lives of the Early Medici*; içeriği okunmadı)

---

*Dosya sonu. Hazırlayan: M3. Git commit/push yapılmadı (ana ajan yapacak).*
