# MEDICI — Yayın Taslağı (7 parça × ≈10 dk + isteğe bağlı Tam Film)

Durum: **metin taslağı** (19 Ekim 2026; yapı kullanıcı önerisiyle 3 parçadan 7 parçaya çevrildi). Zaman damgaları, kapaklar, SRT ve dosya adları **gerçek anlatım + render bitince** `yayin/paket_kur.py` ile üretilecek; bu dosya başlık/açıklama/yorum/etiket metinlerinin kaynağıdır.
Yayın ritmi önerisi: **Pazar 20:00 (+03)**, parçalar arası **+7 gün** (7 hafta) — kanal verisi hızlı sarıyorsa hafta başı 2 parça (Pazar + Çarşamba); tek oynatma listesi **"Medici (7 parça)"**; yedi parça da yayınlandıktan sonra isteğe bağlı **Tam Film** (≈68 dk). İlk tarih, parçaların hazır olmasına göre sabitlenir (Şarlken 18 Ekim'de yayında).

## 1. Parça haritası

| Parça | Bölümler | ≈dk | Konu |
|---|---|---:|---|
| 1/7 | c0–c2 | 9,9 | 1743 odası → florin şehri → kambiyo, defter, "vicdan komitesi", Giovanni |
| 2/7 | c3–c5 | 10,6 | Cosimo'nun hücresi, sürgün ve dönüş → kubbe ve kefaret → konsil, kitap, Platon |
| 3/7 | c6–c7 | 9,2 | Lorenzo "Muhteşem" → 26 Nisan 1478, Pazzi suikastı |
| 4/7 | c8–c9 | 7,3 | Aforoz, savaş, Napoli yolculuğu, Osmanlı → bankanın şube şube kapanışı |
| 5/7 | c10–c11 | 9,8 | Lorenzo'nun ölümü, Savonarola, Fransa Kralı → papa oğulları, Roma 1527, kuşatma |
| 6/7 | c12–c13 | 9,2 | Dükler ve Uffizi → iki Medici kraliçesi, çatal/dondurma/zehir mitleri |
| 7/7 | c14–c16 | 9,3 | Galileo, matbaa, opera, taşlar → son Medici'ler → 1743 odasına dönüş ve hesap |

## 2. Başlıklar (≤60 karakter; aranan ad başta, vaat/merak sonda)

| Parça | Önerilen | Alternatifler |
|---|---|---|
| 1/7 | `Medici (1/7): Bankacı Aile Nasıl Doğdu? Florin ve Defter` (55) | `Medici Ailesi (1/7): Altın Florinden Çifte Deftere` · `Medici (1/7): 1743'te Bir Oda, Bir Sözleşme` |
| 2/7 | `Medici (2/7): Cosimo'nun Sürgünü, Kubbe ve Kitaplar` (50) | `Medici (2/7): Bir Hücreden Floransa'nın Başına` · `Medici (2/7): Tahtsız Kral Cosimo` |
| 3/7 | `Medici (3/7): Muhteşem Lorenzo ve Katedralde Suikast` (52) | `Medici (3/7): Pazzi Suikastı, 26 Nisan 1478` · `Medici (3/7): Bir Pazar Sabahı, Bir Katedral` |
| 4/7 | `Medici (4/7): Aforoz, Osmanlı ve Bankanın Kapanışı` (50) | `Medici (4/7): Papa'ya Karşı Savaş, Napoli, İstanbul` · `Medici (4/7): Defter Neden Kapandı?` |
| 5/7 | `Medici (5/7): Savonarola, Fransa Kralı ve Papa Oğulları` (55) | `Medici (5/7): Rahip, Kral ve Roma 1527` · `Medici (5/7): Sürgünden Dönüş, Kuşatma, Bir Çocuk` |
| 6/7 | `Medici (6/7): Büyük Dük ve İki Medici Kraliçesi` (47) | `Medici (6/7): Uffizi, Catherine, Marie` · `Medici (6/7): Çatal, Dondurma, Zehir: Mit mi?` |
| 7/7 | `Medici (7/7): Yıldızlar, Notalar ve Son Medici'nin Hesabı` (56) | `Medici (7/7): Galileo'dan Son Medici'ye` · `Medici (7/7): Rönesans'ı Gerçekten Onlar mı Yarattı?` |
| Tam Film | `Medici Ailesi: Tam Film (7 Parça · 68 dk)` | `Medici: Floransa'nın Bankacıları, Dükleri ve Kraliçeleri (Tam Film)` |

Not: Başlıkta "satın aldı/ele geçirdi" gibi aşırı iddia kullanılmadı (Anayasa: dürüst vaat). 7/7 için alternatifteki soru formu, "Medici Rönesans'ı yarattı" tezini desteklemediğimiz için yalnızca soru olarak kullanılabilir.

## 3. Açıklamalar (yapıştır; `[BÖLÜMLER]` yerine `bolumler_P*.txt` içeriği)

Ortak blok (her açıklamanın sonuna): kaynaklar + ses/telif notu + etiketler.

```
BAŞLICA KAYNAKLAR (seçme): Treccani (Dizionario Biografico, Enciclopedia Italiana), Britannica, Raymond de Roover, Tracy Parks, Goldthwaite, Padgett–Ansell, Uffizi/V&A/Met kurum sayfaları. Tam liste ve teyit notları: sabit yorumda.

Ses: yapay anlatıcı (ElevenLabs). Çizim, harita ve animasyonların tamamı kodla üretilmiştir; müzik ve ses efektleri sentezdir. Haritalardaki sınırlar yaklaşıktır.
```

### Parça 1/7
```
18 Şubat 1743, Floransa. Yetmiş beş yaşında bir kadın ölüyor; geride, bir şehrin hazinesini "buradan çıkarılamaz" diye bağlayan bir sözleşme bırakıyor. Peki bir bankacı ailesi, mirasını bir şehre bağlayacak noktaya nasıl geldi?

Medici'nin hikâyesi yedi parçada. Bu ilk parçada o odadan geriye, florin şehrine gidiyoruz: altın florinin doğuşu, kambiyo ve "vicdan komitesi", çifte kayıt defteri ve Giovanni'nin köşesi.

Kaynakları açıkça ayırıyoruz: rivayetler "rivayet" diye, tartışmalı yerler "tartışmalı" diye, çevirileri bize ait olan satırlar "çeviri bize ait" diye anılır.

[BÖLÜMLER]

Sıradaki: 2/7 — Cosimo, kule, sürgün ve dönüş.
#Medici #Floransa #Rönesans #TarihBelgeseli
```

### Parça 2/7
```
Eylül 1433'te Cosimo, Palazzo Vecchio'ya çağrıldı ve tutuklandı. Kapatıldığı hücrenin adı Alberghettino'ydu: Küçük Han.

İkinci parçada Cosimo'nun sürgünü ve dönüşü, tahtsız iktidar, Brunelleschi'nin kubbesi ve "kefaret" yatırımı, Ferrara–Floransa Konsili, Rum bilginler, kitaplar ve Platon.

[BÖLÜMLER]

Önceki: 1/7 — Bankacı Aile Nasıl Doğdu? · Sıradaki: 3/7 — Muhteşem Lorenzo ve Pazzi suikastı.
#Medici #CosimoDeMedici #Rönesans #TarihBelgeseli
```

### Parça 3/7
```
26 Nisan 1478, bir pazar sabahı. Floransa'nın katedralinde, Santa Maria del Fiore'de, yüksek ayin yapılıyordu.

Üçüncü parçada önce Lorenzo'yu en yakın dostu Valori'nin anlatımıyla tanıyoruz (yüzü güzel sayılmazdı, ama saygı uyandırırdı; zihni ise şefkatli bir anaydı); sonra katedrale giriyoruz: Pazzi suikastı — iki taraf iki ayrı hikâye anlatır.

[BÖLÜMLER]

Dürüstlük notu: Pazzi suikastının anlatıları Medici süzgecinden geçmiştir; Pazzi'lerin kendi sesi bu kaynaklarda yoktur. Sinyal anı (komünyon/kaldırma) gibi çelişen ayrıntılar tek biçimde sunulmadı.

Önceki: 2/7 · Sıradaki: 4/7 — Aforoz, Osmanlı ve bankanın kapanışı.
#Medici #PazziSuikastı #LorenzoDeMedici #TarihBelgeseli
```

### Parça 4/7
```
Aforoz kararı 1 Haziran 1478'de çıktı; çok geçmeden Floransa'nın kendisine de yasak kondu. Papalık belgelerinin Lorenzo'ya "kötülüğün oğlu ve yıkımın evladı" dediği aktarılır (çeviri bize ait).

Dördüncü parçada savaş, Lorenzo'nun Napoli'ye "konuk mu, rehine mi" yolculuğu, Osmanlı bağlantısı (Bandini'nin İstanbul'dan Floransa'ya dönüşü, Otranto) ve bankanın şube şube kapanışı — 1494'e giden yol.

[BÖLÜMLER]

Önceki: 3/7 · Sıradaki: 5/7 — Savonarola, Fransa Kralı ve papa oğulları.
#Medici #Osmanlı #BankacılıkTarihi #TarihBelgeseli
```

### Parça 5/7
```
Nisan 1492'de Lorenzo, 43 yaşında, rahatlama umuduyla taşındığı Careggi villasında öldü. Başucunda iki dostu vardı: şair Poliziano ve genç filozof Pico della Mirandola.

Beşinci parçada Savonarola ve Fransa Kralı'nın Floransa'ya girişi, Medici'lerin sürgünü ve dönüşü, papa seçilen Medici oğulları (Leo X, Clement VII), Roma 1527 ve Floransa kuşatması — ve sonunda on yedi yaşında bir çocuğun seçilmesi.

[BÖLÜMLER]

Önceki: 4/7 · Sıradaki: 6/7 — Büyük dük ve iki Medici kraliçesi.
#Medici #Savonarola #Roma1527 #TarihBelgeseli
```

### Parça 6/7
```
Ocak 1537'de bir dükü kuzeni öldürmüş, Senato da yerine 17 yaşında Cosimo'yu seçmişti. Ertesi gün Senato koşulu yazıya geçirdi: Cosimo dük olmayacak, yalnızca "kentin başı ve birincisi" diye anılacaktı.

Altıncı parçada büyük dük Cosimo I — devlet, Uffizi ("yani ofisler") ve unvan — sonra Paris'e geçip iki Medici kraliçesini (Catherine ve Marie) ve onlara yazılan çatal, dondurma, zehir faturalarını tartıyoruz.

[BÖLÜMLER]

Önceki: 5/7 · Sıradaki: 7/7 — Yıldızlar, notalar ve son hesap.
#Medici #CatherineDeMedici #Uffizi #TarihBelgeseli
```

### Parça 7/7
```
16. yüzyılın sonunda Roma'da, Papa XIII. Gregorius'un desteğiyle ve Kardinal Ferdinando'nun himayesinde, bir Medici Doğu Dilleri Matbaası kuruldu.

Son parçada Medici'nin mirasını tartıyoruz: Galileo'nun "Medici yıldızları", matbaa, opera, piyano ve sert taşlar; Livornina, Fahreddin ve Mustafa Ağa; son Medici'ler (2026 DNA çalışması dahil) ve 1743 odasına dönüş. Sonda bir "sağlamlık haritası": anlatılanlardan hangisi sağlam, hangisi nitelikli, hangisi mit?

[BÖLÜMLER]

Not: "Medici Rönesans'ı yarattı" tezini desteklemiyoruz; kaynaklar "en görünür patronlardan biri" diyor. 2026 DNA çalışmasının Francesco I için gösterdiği sıtma bulgusu "zehir çürütüldü" anlamına gelmez; videoda bu ayrım korunur.

Önceki: 6/7 · Tüm film: oynatma listesinde.
#Medici #Galileo #Rönesans #TarihBelgeseli
```

## 4. Sabit yorum (yayından hemen sonra; parça başına)

```
📌 Rakamlar ve tarihler araştırma özetlerine dayanır; rivayetler videoda "rivayet" diye işaretlendi. Birincil metinlere (ör. Poliziano, Landucci) doğrudan erişemediğimiz yerlerde ikincil kaynakları açıkça belirttik. Tam kaynak/teyit tablosu isteyen yazsın, paylaşalım.
Soru: [1] Cosimo'nun "kefaret" yatırımı mı, iyilik mi? ([2]'de açılır) · [2] Bir hücreden dönüp devleti tahtsız yönetmek: dâhilik mi, kurnazlık mı? · [3] Pazzi suikastında Papa'nın payı sizce ne? · [4] Lorenzo'nun Napoli'ye gitmesi cesaret miydi, kumar mı? · [5] Savonarola kâhin miydi, demagog mu? · [6] "Büyük dük" unvanı meşruiyet mi, makyaj mı? · [7] "Medici Rönesans'ı yarattı" demek ne kadar doğru?
```
(Parçaya özel tek soru kullanılır; numarası parçayla eşleşir.)

## 5. Etiketler (virgülle)

`Medici, Medici Ailesi, Floransa, Rönesans, Lorenzo de Medici, Cosimo de Medici, Pazzi Suikastı, Savonarola, Catherine de Medici, Marie de Medici, Galileo, Uffizi, İtalya tarihi, tarih belgeseli, bankacılık tarihi, Zaman Kuryesi`

## 6. Studio kontrol listesi (parça başına ≤15 dk)

1. Kapak: parça başına `yayin/kapak_P#_A.jpg` (B/C yedek); yedi kapak tek aile (aynı çerçeve, parça numarası büyük). 2. Dil: Türkçe; kategori: Eğitim. 3. **Altyazı:** `medici_P#_tr.srt` (zamanlamalı). 4. Bölümler: açıklamadaki damgalar (ilk satır 0:00; her bölüm ≥10 sn; parça başına 2–3 bölüm).
5. **"Değiştirilmiş veya sentetik içerik":** **Evet** (yapay anlatıcı). 6. "Çocuklara özel değil"; yaş sınırı yok. 7. Oynatma listesi: **Medici (7 parça)** + **Uzun Dosya**.
8. **Bitiş ekranı** (son 7 sn): P1–P6 "SIRADAKİ PARÇA" + "Abone ol"; P7 "TÜM FİLM" + "Abone ol".
9. Yayın: Pazar 20:00 (+03), parçalar arası +7 gün (ya da hafta başı 2 parça). 10. Kısa fragmanlar: parça başına 1 dikey Kısa (kanca bölümü); başlık ve açıklama çakışmasız (SRT yükleme sorunu notu: Studio'da elle yüklenir).
11. Her parçanın açıklaması kendi içinde bağımsız okunur (önceki/sonraki parça bağlantıları yayın sırasında eklenir).

## 7. Dürüstlük ve kullanıcıya notlar

* Kaynak kapısı: ● (birincil metin okundu) **hiçbir satırda yok** — bu ortamda WebFetch ile birincil sayfalar açılamadı; tüm olgular ◐/○ düzeyindedir. Yayın öncesi `kaynaklar_P1…P7.md` içindeki "Yayın öncesi teyit listesi" sayfa düzeyinde gözden geçirilmelidir (özellikle HAFIZA-Y satırları: Mehmed'in ölümü 3 Mayıs 1481, İnebahtı sonucu).
* **Kulak denetimi** (özel adların okunuşu) kullanıcıdadır: `okunus_P*.md` listesindeki adları dinle; hatalı yerde tek cümle `ses_yama.py` ile yamanır.
* **c0 alıntı kartı:** "Hiçbir şey buradan çıkmayacak" **Anna Maria Luisa'nın sözü olarak sunulmaz**; sözleşmenin 3. maddesinin özetidir (c16 bunu söyler). Parça 1 başlığında/kapağında bu söz alıntı olarak kullanılmaz.
* Ses lisansı/plan: ElevenLabs ticari kullanım koşullarını kontrol et (Şarlken notu geçerli).
