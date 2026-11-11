# Kapak kurulu, tur 2: P-Sanat (sanat yönetmeni)

Ölçütler ve ağırlıklar tur 1 ile aynı:

| Ölçüt | Ağırlık |
|---|---|
| Kompozisyon | %20 |
| Çizim | %25 |
| Tipografi | %15 |
| Üslup | %15 |
| Küçük boy | %15 |
| Kırmızı çizgi | %10 |

Eşik 9,0; hiçbir ölçüt 7'nin altında olamaz. Koordinatlar 1280×720.

**Bakılanlar:**
- Kapaklar: `kapak_a.jpg`, `kapak_b.jpg`, `kapak_a_sade.jpg`, `kapak_b_vektor.jpg`.
- Test seti: `tur7b/yanyana168.png`.
- Kendi kırpma ve küçültmelerim (scratchpad `psanat/t2_*`): A'da baş ve alev, figür, kapanış tırnağı; B'de saç, iris, damla, yüz kenarı; 246, 168 ve 120 px küçültmeler.

**Ölçümler (PIL):**

| | A | B |
|---|---|---|
| Büyük harf yüksekliği | "BEN" y 220–352 = 133 px (%18,5) | "PİŞMAN" P harfi y 155–290 = 136 px (%18,9); yazı bloğu y 126–485, x 801–1240 |
| Tırnaklar | açılış “ x 48–113, y 141–188; kapanış ” x 741–804, y 548–595 | – |
| Künye | x 53–666, y 564–591 | – |
| Parlaklık ≥245 | yalnız x 1005–1034, y 375–397: orta alev dilinin çekirdeği. **Tek odak sağlandı.** | x 381–684, y 94–619: yüzün kâğıdı ve göz akı. Damla ortalaması 201, yazı ortalaması 200. |
| Rozet bölgesi | ortalama 73, sapma 68 (etek ve kanat uçları) | boş (sapma 0,9) |
| Koyu piksel oranı | %31,8 | %69,0 |

## 1. Çapraz eleştiri (P-TO'nun tur 1 raporu)

### Katıldıklarım
- **A'da alevin tek ve en parlak odak olması.**
  - Tur 1'de ben de "en parlak yer alevin dili değil, tabandaki kâse" demiştim. P-TO aynı sorunu zemin tarafından gördü: zemin alevden parlaktı.
  - İkisi birlikte doğru çözümü verdi: zemin %10 koyulaştı, çekirdek orta dile kondu. Ölçüm artık ≥245 parlaklığın yalnız alev çekirdeğinde olduğunu gösteriyor.
- **Köşe bulutlarının kalkması ve açık tema için koyu çerçeve.** Doğru; çerçeve açık akışta kenarı geri getiriyor.
- **"ŞEYTAN AĞLADI" yerine "PİŞMAN MIYDI?".** Vaaz kalıbıyla çakışma bulgusu benim merceğimde yoktu; isabetli. "PİŞMAN MIYDI?" Bebas'ta "AĞLADI"dan daha dengeli bir blok da veriyor.
- **B'nin vaadinin açılışta karşılanması** (10. saniyedeki göz planı). Kapağın dürüstlüğü benim "üslup ve dürüstlük" ölçütüme de giriyor; bu ekleme B'yi filme bağladı.
- **Figüre duygu vermek** (baş eğimi, "göğsünü kavrama"). Aynı sonuca vardık.
- **Turuncu yazı sürümünü teste sokmamak** (`yazirenk`). Aynı gerekçe: ikinci renk odağı.
- **Tur 5 B'deki "posta pulu" görüntüsü** (tırtıklı göz levhası). Benim tur 1'de baktığım tur 6 sürümünde tırtık yoktu; bu yüzden göremedim, ama bulgu doğru. Yeni B'nin sol üst köşesinde benzer bir sorun yeniden doğdu (aşağıda: "saç" topları).

### Katılmadıklarım
- **"Gözyaşını ≈1,5 kat büyüt, içine beyaz ışık ver (≥240)."**
  - Tur 6'daki 1,5 kat büyük vektör damla tam olarak benim "emoji" bulgumu doğurdu. Yaklaşık 300 px boyunda, irisin iki katıydı; gravür dilinden çıkıyordu.
  - Gelinen 1,3 kat ve gravür çizimli uzlaşma doğru.
  - Damla, en parlak nokta olmak zorunda değil. Gravürde göz akı ve alnın kâğıdı doğal olarak en açık yerdir; damlayı ayıran parlaklık değil, karedeki tek **doygun renk** olması. Bulanık testte bu yeterli.
  - Ama P-TO'nun asıl kaygısına katılıyorum: damla yazıyla aynı parlaklıkta (201'e 200) ve yazıyla yarışmamalı. Aşağıdaki B-4 düzeltmesine bak.
- **A için üçüncü test seçeneği olarak koyu A.**
  - Koyu A filmin açılış karesiyle eşleşmiyor; açılış açık kâğıt zeminde. Bu yüzden kanalın "kapak = ilk 5 saniye" kuralını zayıflatıyor.
  - Koyu akışta da zeminle eriyor.
  - Test değişkeni olarak savunulabilir, ana aday olarak değil. Test kapasitesi B′'ye ayrılmalı.
- **"Yazıyı %4 büyüt."** Artık gerek yok. Harf yüksekliği %18,5'te, eşiğin üstünde. A'da sağdaki boşluk zaten tırnakla dolmuş; büyütmek kanat boşluğunu daha da daraltır.

### P-TO'nun gözünden kaçtığını düşündüklerim
- Çizim kalitesi:
  - A'nın piktogram figürü;
  - boncuklu kanat vuruşları ve zikzak kanat uçları;
  - B'nin emoji damlası ve jant kapağı irisi.

  Bunlar 168 px'te görünmüyor, ama tam boyda, TV'de (izleyicinin %22'si) ve kapağa tıklanıp açılan izleme sayfasında görünüyor. Kanalın kalite vaadine giriyor.
- **"Kutsal Kalp" benzerliği:** simetrik duruş, iki eliyle göğsündeki alevi sunması ve arkasındaki ışınlar. Artık kapandı.
- Turuncu alev ve mavi damla filmde yok; filmde ikisi de kâğıt beyazı. P-TO turuncuyu "kabul edilebilir" saydı, ben de öyle. Ama aynı mantıkla B'nin mavisinin de yalnız tonlama olarak gelmesi gerektiğini ekliyorum; şu anki sürüm bunu yapıyor.

## 2. Yeni puanlar

| Ölçüt (ağırlık) | A tur 1 | **A tur 2** | B tur 1 | **B tur 2** |
|---|---|---|---|---|
| 1 Kompozisyon (%20) | 8,0 | **8,5** | 7,5 | **8,6** |
| 2 Çizim (%25) | 6,8 | **8,2** | 6,0 | **7,8** |
| 3 Tipografi (%15) | 8,5 | **7,6** | 8,0 | **8,6** |
| 4 Üslup (%15) | 8,5 | **8,8** | 6,5 | **8,4** |
| 5 Küçük boy (%15) | 8,5 | **8,8** | 8,5 | **8,5** |
| 6 Kırmızı çizgi (%10) | 8,0 | **9,0** | 9,0 | **8,5** |
| **Ağırlıklı** | 7,9 | **8,4: RED** | 7,4 | **8,3: RED** |

İki kapak da ciddi biçimde iyileşti; artık hiçbir ölçüt 7'nin altında değil. Kalan işlerin hepsi son rötuş düzeyinde, B'de bir tane küçük yeniden çizim var. Aşağıdaki düzeltmelerle ikisinin de 9,0'ı geçmesini bekliyorum.

- **A'nın tipografi puanı düştü (8,5 → 7,6).** Nedeni eklenen tırnaklar:
  - Ayrı bir ağır serif yazı tipindeler.
  - Kapanış tırnağı künye satırının sonuna düşüyor; "MILTON · KAYIP CENNET”" gibi, yani künye alıntılanmış gibi okunuyor.
  - Kanada yaklaşık 20 px kalıyor; 30 px eşiğinin altında.
  - Sade sürümle bu ölçüt 8,6 olur ve A 8,6'ya çıkar.
- **B'nin kırmızı çizgi puanı düştü (9,0 → 8,5).** Sol üstteki "saç ipucu", ince bir çizgiye dizilmiş siyah toplardan oluşuyor (x 0–250, y 0–125). Tespih ya da boncuk dizisi gibi okunabiliyor. Küçük bir risk, ama kolayca giderilir.

## 3. Tur 1 bulgularının durumu

### A
| # | Bulgu | Durum | Not |
|---|---|---|---|
| A1 | Baş ve gövde piktogram gibi, duygu yok | **Kısmen** | Kıvırcık saç kütlesi ve kambur, geniş omuzlar piktogramı kırdı; sabit kalınlıktaki kontur gitti. Ama 0,4 rad eğim kapakta okunmuyor: baş (x 960–1040, y 185–262) hâlâ dik duruyor gibi. Saç, arkadan görülen bir "topuz" gibi de okunabiliyor. |
| A2 | Alev el ve kâse gibi | **Kısmen** | Pençeler gitti, üç dil doğru, çekirdek orta dilde. Yeni sorun: tabanda eşit aralıklı dikey mürekkep dişleri (x 975–1050, y 430–466). Alev bir tarak ya da ızgaradan çıkıyor gibi; tabanı karanlığa erimiyor, dişlerle kesiliyor. |
| A3 | Boncuklu kanat iç çizgileri | **Kapandı** | Vuruşlar kesintisiz ve sivriliyor. |
| A4 | Kesik ve noktalı kanat konturu | **Kısmen** | Kanatların üst ve dış kenarında hâlâ testere gibi kâğıt saçağı var (sol x 826–850, y 95–330; sağ x 1195–1218, y 95–330). |
| A5 | Şimşek zikzaklı kanat uçları | **Kapandı** | Ayrık uçlar y ≈ 640'ta bitiyor. |
| A6 | Ayaklar | **Kapandı** | |
| KR | "Kutsal Kalp" benzerliği | **Kapandı** | Eller yok, alev göğsün içinde yanıyor, sunma jesti yok. |

### B
| # | Bulgu | Durum | Not |
|---|---|---|---|
| B1 | Emoji damla | **Kapandı** | Kontur, iç vuruşlar ve tek parlama yayı var; mavi tonlama olarak geliyor. Gravür diline oturdu. |
| B2 | Islak iz boru gibi | **Kısmen** | İz artık ince, ama **gri** (x 445–470, y 370–490). Karede dördüncü bir ton oluyor: ne kâğıt, ne mürekkep, ne de damlanın mavisi. |
| B3 | Jant kapağı iris | **Kapandı** | Işınsal ince vuruşlar, ayrı göz akı, gravürdeki gibi köşeli pencere yansıması. |
| B4 | Yüzün sağ kenarı tarak ya da glitch gibi | **Kısmen** | Çizgiler artık sivriliyor, ama hepsi yatay ve aynı yönde uzuyor (x 600–758). Bir yüz konturu çizmiyor; "hız çizgisi" ya da tarayıcı hatası gibi duruyor. Uçları P harfine 43 px kalıyor. |
| B5 | Göz altındaki koyu leke | **Kısmen** | Tam boyda tarama oldu. 120 px'te göz altında hâlâ gri bir leke (x 300–560, y 380–470). |
| B6 | Cabanel kimliği yok | **Açık** | Eklenen "saç ipucu" saç gibi değil, siyah top dizisi gibi okunuyor (bkz. kırmızı çizgi). 168 px'te köşede bir leke olarak kalıyor; P-TO'nun tur 1'deki "kir lekesi" uyarısının aynısı. |
| B7 | Kare üstten ağır, sağ alt ölü | **Kapandı** | Yazı bloğu y 126–485 arasında, ortada. |
| B8 | Yazı ile yüzün parlaklık dengesi | **Kısmen** | Yazı 200, damla 201; yüz ≥245. Damla rengiyle ayrışıyor, ama yazıdan açık değil. |

## 4. Kalan düzeltmeler (yalnız 9'a taşıyacak olanlar, sırayla)

### A
1. **Tırnaklar.** *Son rötuş.* İki seçenek var:
   - **(a) Tercihim:** tırnakları kaldır, künyeyi alıntı imzası olarak koru: `— MILTON, KAYIP CENNET`, x 53'ten başlayarak, aynı Cinzel ve ton.
     - Başta uzun çizgi olan bir künye, sözün alıntı olduğunu Türkçe dizgide tek başına anlatır.
     - Künye Cinzel'de olduğu için filmin başlık yazısına da bağlanıyor.
     - Bu çözümün hassasiyet üyesinin isteğini karşılayıp karşılamadığını o doğrulamalı.
   - **(b) Tırnak şart ise:**
     - Tırnaklar Bebas'ın kendi tırnakları olsun ya da Cinzel'de ince olsun; boyları büyük harf yüksekliğinin yaklaşık %40'ı.
     - **Asılı** dur: “ yazı sınırının dışında olsun (x ≈ 14–40, üstü BEN'in büyük harf üstüne, y ≈ 220, hizalı).
     - ” CEHENNEMİM'in son M'sinin sağında, büyük harf üstüne hizalı dursun (y ≈ 394).
     - Buna yer açmak için yazı bloğunu %6 küçült (sağ kenar x ≈ 752). Böylece ” x ≈ 760–790'a düşer ve kanada en az 30 px kalır.
     - Tırnak hiçbir koşulda künye satırının yanına düşmemeli.
2. **Alev tabanındaki tarak.** *Son rötuş.*
   - x 975–1050, y 430–466 arasındaki eşit dikey dişleri kaldır.
   - Mürekkep vuruşları her dilin içinde, dilin eğrisini izleyerek yukarı doğru sivrilsin. Dil başına 1–2 tane olsun, boyları farklı.
   - Taban y ≈ 440'tan itibaren kor ışımasıyla karanlığa erisin; düz bir alt sınır olmasın.
3. **Baş eğimi.** *Son rötuş (küçük yeniden çizim).*
   - Baş kütlesini (x 960–1040, y 185–262) boyun köküne göre 15–18 px sola ve 10 px aşağı kaydır.
   - Eğimi 0,4'ten yaklaşık 0,55 rad'a çıkar.
   - Başın sağ üst kenarına (güneş tarafı) 3 px kesintisiz bir kenar ışığı ver. Eğim siluette 168 px'te okunsun.
   - Saç kütlesinin tepesindeki yuvarlak "topuz" çıkıntısını 20 px alçalt: kıvırcık bukleler başı sarsın, tepede toplanmasın.
4. **Kanat dış kenar saçağı.** *Son rötuş.* x 826–850 ve 1195–1218 arasında, y 95–330 boyunca testere gibi kâğıt kenarını kaldır. Kenar ışığı yalnız güneşe bakan iç kenarlarda olsun; sürekli, 3 px.
5. **Rozet bölgesi.** Değiştirme. Rozet eteğin karasına oturuyor; okunurluk kaybı yok.

### B
1. **Sol üstteki "saç" topları.** *Yeniden çizim (küçük).*
   - x 0–250, y 0–125 arasındaki siyah top dizisini ve altındaki çizgiyi kaldır.
   - Yerine filmdeki Cabanel karesinin dili kullanılsın: kalın koyu kütle ve içinde eş merkezli, sivrilen 4–6 kâğıt rengi yay. Bu, bir ya da iki iri S bukle olarak okunur. Kadraj köşesinden girsin, x 0–200, y 0–110.
   - Yapılamazsa tamamen kaldır. Leke ve tespih okuması, kimlik ipucundan daha pahalı.
2. **Yüzün sağ kenarı.** *Son rötuş.*
   - Yatay çizgilerin uçları bir şakak ve elmacık eğrisini izlesin: üstte x ≈ 640'ta, göz hizasında x ≈ 690'da, altta x ≈ 620'de bitsin.
   - Uzunlukları düzensiz kalsın, ama hiçbiri x 700'ü geçmesin. Yazıya en az 100 px kalır, "hız çizgisi" görüntüsü gider.
3. **Islak iz.** *Son rötuş.* Gri izi (x 445–470, y 370–490) damlayla aynı dile çek: kâğıt beyazı, damla tarafında hafif mavi tonlu, bir kenarında 1,5–2 px mürekkep çizgisi. Gri ton kalmasın (`KILAVUZ` "Üslup dili" madde 1).
4. **Damla ile yazı dengesi.** *Son rötuş.*
   - Damlanın üst üçte birini neredeyse beyaza aç (≈ #eef8ff, parlaklık ≥235); alt kısım mavi kalsın.
   - Ya da yazıyı #c4bcae'ye çek (≈190).
   - Damla, yazıdan en az 30 birim açık olsun. Rengi ve parlaklığı birlikte damlayı tek odak yapar.
5. **Göz altındaki leke.** *Son rötuş.* x 300–560, y 400–470 arasındaki taramayı seyrelt: çizgi aralığı yaklaşık 1,5 kat. 120 px'te morluk ya da akmış rimel okuması tamamen kalksın.

## 5. Ana sürüm seçimleri
- **A: tırnaklı mı, sade mi?** Şu anki tırnaklı sürüm sade sürümden **kötü**. Tırnakların yazı tipi uyumsuz, yerleri yanlış ve kanada 30 px'ten az kalıyor. Ama künye değerli: filme ve kaynağa bağlıyor, hassasiyet isteğini karşılıyor.
  - **Önerim:** sade gövde + künye (`— MILTON, KAYIP CENNET`), tırnaksız; düzeltme A-1(a).
  - Hassasiyet üyesi tırnağı şart koşarsa A-1(b) ile düzeltilmiş tırnaklı sürüm.
  - Mevcut iki dosyadan birini seçmek zorundaysak `kapak_a_sade`. Ama alıntı belirsizliği hassasiyet alanının vetosuna giriyorsa, karar onun.
- **B: gravür damla mı, vektör mü?** **Gravür damla.**
  - 168 px'te (`yanyana168.png`) vektör damla biraz daha doygun ve iri, ama fark küçük. İki damla da okunuyor.
  - Gravür damla filmle ve gözün diliyle aynı elden çıkmış görünüyor.
  - Tam boyda, TV'de ve izleme sayfasında vektör damla emoji olarak kalıyor.
  - Okunurluktaki küçük kaybı B-4'teki parlaklık rötuşu kapatır.

## 6. En emin olmadığım nokta
1. **A'nın yeni başı.** Kıvırcık saç kütlesi Cabanel'in meleğiyle tutarlı, ama siluette arkadan görülen bir kadın topuzu ya da antik bir büst gibi de okunabilir. Bu okumanın izleyicide ne kadar yaygın olacağından emin değilim. A-3'teki "topuzu alçalt, bukleler başı sarsın" düzeltmesi bu riski azaltır. Başkanın tam boyda kendisi bakmasını öneririm.
2. **B'deki tespih okuması.** Kesin değil: belki yalnız ben böyle görüyorum. Düzeltme ucuz olduğu için yine de yaptırılmalı.
