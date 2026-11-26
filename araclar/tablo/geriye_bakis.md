# tablo motoru: geriye bakış (Mektuplar, 26 Kasım 2026)

Yöntem: kullanıcı yaratıcılığı tamamen bıraktı ("iyiyi kendi standardına göre belirle"). Başkan üretti, yönü olmayan bağımsız bir eleştirmen (aynı ajan, beş tur, `SendMessage` ile sürdürüldü) yalnız filmi izleyip sert, zamanlı bulgu verdi. Her bulgu karede doğrulandı; doğrulanmayan reddedildi (v1'deki "duş kapısı" iddiası).

## Sürüm sürüm (25 sn kimlik filmi)
| Sürüm | Değişen | Eleştirinin ana bulgusu |
|---|---|---|
| v1 | ilk yağlıboya; mektuplar kuşa döner | filtre görünümü, hedef tahtası güneş, köz taç, 18. saniyeden sonra hiçbir şey olmuyor, figür delik gibi |
| v2 | yön izleyen fırça, güneş ayrı ve batıyor, tek mektup, çiçek | (kendi denetim: şapka kıvırcık, çiçek haç) |
| v3 | kamera koreografisi, dönen yapraklar, ses, siyah-beyaz | taç bulanık leke, 4 sn boşluk, şapka boynuz ya da korkuluk, damga çiçek |
| v4 | fırçalı taç, çiçek girdiği yerden, palto, ayak sesi, −16 LUFS | — |
| v5 | kurye Blender'da | kostüm asker ya da elbise, heykel figür, 2 sn boşluk |
| v6 | sivil palto, oyunculuk (iki adım), ağaç titrer | ışınsal parıltı örümcek, camda kırık |
| v7 | parıltı yok, atkı, baş kalkar | **engel yok; iki sürüm de bitmiş.** Siyah-beyaz daha güçlü imge, renkli daha güçlü hikâye |

## Dersler (birden çok turda doğrulandı)
- **Durağan katman önbelleği** kareyi 7,2 sn'den ~1 sn'ye indirdi; 25 sn'lik film 88 dk'dan ~11 dk'ya düştü. Önce ölç, sonra hızlandır.
- **Simge riski küçük boyda artar.** Bu filmde yakalananlar:
  - dört yapraklı çiçek → haç;
  - halka darbeli disk → hedef;
  - ışınsal parıltı → örümcek, kırık cam;
  - yana düz çıkan atkı ucu → tüfek;
  - omuz çıkıntısı → apolet;
  - düz tepeli geniş kenarlı şapka ve uzun koyu palto → din adamı;
  - kıvrık uçlu kenar → süvari;
  - A-kesim etek ve ince boyun → elbise;
  - parlak disk başın arkasında → hale (kurye güneşin solunda durur).
- **Sebep-sonuç 0,5 sn içinde görünmeli.** Mektup taca girdikten 2–4 sn sonra açan çiçek, kopuk okundu.
- **Kabartma ışığı ince lekede halka çizer** (DAB yüksekliği). Çiçek, yaprak ve ışık için `hgt` ≈ 0 ve fırça (BRUSH) kullanılır.
- **Karanlık üstünde yarı saydam açık leke** gri ya da haki okunur; ışık efekti yerine boyalı nesne (çiçek) daha iyi.
- **Figür için Blender** (yalnız figür, boyama yine bizim): siluet, palto ve şapka sorunlarını çözdü; 376 kare 84 sn. Sahnenin tamamı Blender'a taşınmadı (düz render "bilgisayar görüntüsü" okunur).
- **Ses kulakla dinlenmeden** düzey eğrisi ve spektrumla denetlendi. Doruk müziğin değil anlatının doruğuna konur; efekt yatağı kendi doruğuna göre düzeylenir (ortam yatağına göre ölçeklenen esinti +27 dB çıkmıştı).

## Açık kalanlar (engel değil)
- Sol omuzda hafif çıkıntı.
- 60 Hz altında bas şişmesi izi.
- Tekerlek izleri hâlâ paralel okunuyor.
- Meşe salınımı zayıf.

## Üslup kapısı: orta ve yakın plan (27 Kasım)
- Sahne yöneticisi (`sahne.js`) ve figür modülü (`figur.js`); Mektuplar ikisine taşındı, karelerde fark 0.
- **Plan kipi:** kamera yönü ve eğimi aynı, konum figüre yaklaşır.
  - Sonsuzdaki katmanlar (gök, güneş, tepeler) aynı resimle; dar açı onları büyütür.
  - Ağaç gibi uzak nesne paralaksla konumlanıp ölçeklenir.
  - Yakın tarla ve başaklar ekran koordinatında yeniden boyanır.
  - Figür o kameradan Blender'da yeniden render edilir.
- **Kurgu:** `kurye/kurgu.sh` (geniş, orta, geniş, yakın, geniş; ses kesintisiz). Manzara, orta plan figür, yakın plan ve 15 sn hareket aynı filmde.
- **Yakın plandaki dersler:**
  - Darbe boyu figürün büyüklüğüyle ölçeklenmezse figür pürüzsüz 3B render (CG) okunur.
  - Arkadan bakılan başta ten rengi soluk yumurta okunur; saç, kulak ve ense çıkıntısı gerekir.
  - Kulak açık renkte olursa başın ortasında delik gibi durur; karşı ışıkta kulak koyu olur.
  - Tepe düz ve yüksek şapka silindir şapka okunur.
  - Kesintisiz kenar ışığı çıkartma kenarı okunur; öbek öbek kırılır.
- **Hız:** yakın planda kare 4 işçiyle 16 sn (figür alanı büyük, darbe sayısı çok). Açık iş: figür örnekleme adımı ölçekle büyümeli.
- **Açık kalan:** orta ve yakın planda figür hâlâ biraz "kil" okunuyor. Yüz ve el yakın planına girilmedi; kural gereği girilmez, sırt, siluet ve nesne yakın planı kullanılır.
