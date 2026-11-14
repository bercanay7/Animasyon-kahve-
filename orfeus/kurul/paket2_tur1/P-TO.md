# Orfeus paket 2, tur 1: TO/paketleme + "ilk kez gören izleyici" (bağımsız ilk bakış)

**Bakılanlar:** `paket2/*.jpg`, `test/karsilastirma.jpg`, `test/akis_koyu.jpg`.
Test setindeki süre rozeti "25:46" yazıyor; görmezden geldim.

**Ölçüm (720 px'lik karede, harf yüksekliği):**

| Kapak | 1. satır | 2. satır |
|---|---|---|
| son_adim | "SON ADIMDA" 97 px (%13,5) | "BAKTI" 140 px (%19,4) |
| eski_a | "ARKANA" 92 px (%12,8) | "BAKMA!" 139 px (%19,3) |
| eski_b | "NEDEN" 95 px (%13,2) | "BAKTI?" 139 px (%19,3) |

- Üç kapakta da yazı bloğunun üst kenarı y = 17–18 px'te, yani kenara yapışık. Sağ kenar x ≈ 1244 (36 px pay).
- Vurgu kelimesi her kapakta %18'in üstünde. Birinci satırların %18'in altında kalmasını, ikincil satır oldukları için kabul ediyorum.

**Okuma:** Görüntü güçlü ve üç kapakta da aynı: ¾ yüz, gözyaşı, iki parmak ucu arasındaki kıvılcım tek odak, sıcak ve soğuk renk zıtlığı. Tutma %45,8 ile kanalın en iyisi, yani vaat yanıltmıyor. TO'nun %1,45'te kalmasını görüntüye değil yazıya ve başlığa bağlıyorum.

## Puanlar

| Öğe | Puan | Karar | Gerekçe |
|---|---|---|---|
| son_adim "SON ADIMDA / BAKTI" | **9,0** | ONAY | "Az kalmıştı" gerilimini ekliyor. Miti bilen tanır, bilmeyen "neye baktı, neden son adımda?" diye merak eder. Ağlayan yüz cümlenin bedelini gösteriyor. Ovidius ("kenardan çok uzak değillerdi") ve Vergilius ("ışığa varmışken") ile sadık bir özet. "Neden" kalıbı yok. |
| eski_a "ARKANA BAKMA!" | **8,5** | Kontrol | Güçlü ve tanıdık bir yasak. Ama vaadi miti bilenin cümlesi; yeni bir şey söylemiyor. 22,9 B gösterimde %1,45 TO'nun bir parçası bu kapak. |
| eski_b "NEDEN BAKTI?" | **7,5** | RED | "Neden …?" kalıbı: Sisifos başlığında ve Milton'ın yeni başlığında var, kanal kuralına takılıyor. Sorusu son_adim'in örtük merakının daha zayıf bir biçimi. Testten çıksın. |
| O1 "Orfeus Neden Son Adımda Arkasına Baktı? \| …" | **6,5** | RED | (a) son_adim'in yazısını kelimesi kelimesine tekrar ediyor; (b) "Neden" kalıbı Milton'ın yeni başlığıyla art arda geliyor; (c) mobilde "…Ar/kasına Baktı? \| Or…" diye iki satıra bölünüyor (akış taklidinde görünüyor). |
| O2 "Ölülerden Dönüşün Tek Şartı: Arkana Bakma \| …" | **7,5** | RED (bu test için) | Kanca güçlü: ölüm, dönüş, tek şart. Ama eski_a ile aynı testte kapak yazısını tekrar ediyor; tek başlık iki kapakla da çalışmalı. Yalnız son_adim tek başına yayına çıkarsa 8,5 olur. |
| O3 (şimdiki) "Orfeus ve Evridiki: Ölüleri İkna Etti, Kendini Durduramadı" | **8,0** | — | Paradoks iyi ve iki kapağı da tekrar etmiyor. Ama mobilde ilk 19 karakter adlara gidiyor; kanca ikinci yarıda kalıyor. |
| **O4 (önerim)** "Ölüleri İkna Etti, Kendini Durduramadı \| Orfeus ve Evridiki" | **8,5** | ONAY'a yakın | O3'ün aynı kelimeleri, sırası çevrilmiş: paradoks önde, adlar kuyrukta. Kalıp, Milton'ın "Neden" başlığıyla çakışmıyor. Kapak "son adımda baktı" deyince başlık nedenini ("kendini durduramadı") veriyor; tekrar değil, tamamlama. |

## Önerilen test

- **Kapaklar:** son_adim + eski_a. eski_a, kazanmış olan ya da yerleşik kontrol olarak kalır.
- **Başlık:** O4, testten önce bir kez değiştirilir; test sürerken dokunulmaz.
- **Paket bütün:** 8,5. Düzeltme 1 ile 9 olur.

## Düzeltmeler (en çok 3; 1920×1080)

1. **son_adim: yazı bloğunu 30 px aşağı al.** Şimdiki blok x ≈ 1100–1866, y ≈ 25–396. "SON ADIMDA"nın üst kenarı y ≈ 26'da, kenara yapışık; TV ve yuvarlak köşeli mobil kırpmada harf tepeleri kesilmeye yaklaşıyor. Üst pay ≥ 55 px olmalı. BAKTI'nın alt kenarı y ≈ 426'ya iner; Evridiki'nin başına (y ≈ 470) hâlâ 30 px'ten fazla kalır. Aynı kayma eski_a için de yapılabilir; testi bozmaz.
2. **Eski testin sonucunu oku** (Studio → Test ve karşılaştır, eski_a ve eski_b, izlenme süresi payı).
   - eski_b açık farkla kazandıysa kontrol olarak o kalır; "Neden" kalıbı riskini o zaman veri öder.
   - Belirsizse eski_a kalır.
   - Sonuç `orfeus/` kaydına yazılsın.
3. **Akış taklidini O4 ile yeniden üret,** rozeti 4:48 yaparak. 4:48'lik kısa rozet bu videonun lehine bir sinyal (25 dakikalık Milton'ın tersine düşük taahhüt); taklitte doğru görünmeli.

## En emin olmadığım nokta

"SON ADIMDA BAKTI" miti bilmeyen biri için öznesiz kalabilir: "kim baktı, neye?" Bu merak mı yaratır, kafa karışıklığı mı, emin değilim. Görüntü (ağlayan adam, uzanan el, silinen kadın) cevabı büyük ölçüde veriyor. Ama 120 px'te Evridiki'nin "silinen" parçacıkları okunmuyor; geriye "ağlayan iki kişi" kalıyor. Testin son_adim aleyhine çıkması hâlinde ilk şüphelim bu, yazı değil.
