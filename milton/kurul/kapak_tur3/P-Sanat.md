# Kapak kurulu, tur 3: P-Sanat (gerileme kontrolü)

Ölçütler ve ağırlıklar tur 1 ve tur 2 ile aynı:

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
- `kapak_a.jpg` ve `kapak_b.jpg`.
- Filmin güncel açılış karesi (`v7b/t0004.60`).
- Kendi kırpmalarım ve küçültmelerim (scratchpad `psanat/t3_*`):
  - A: baş ve alev; iki tırnak.
  - B: sağ kenar ve damla.
  - İki kapak için 246, 168 ve 120 px küçültmeler.

## İddiaların doğrulaması (ölçüm)
- **A, parlaklık:**
  - ≥230 piksellerin 672/677'si alev kutusunda (x 1015–1115, y 300–480).
  - Kalan 5 piksel, kanat ve baş kenar ışığında tek tük JPEG pikseli.
  - Alev dışındaki en yüksek değer 240, ama alan yok denecek kadar küçük. **Tek odak: doğrulandı.**
- **A, kapanış tırnağı:** x ≈ 820–845, y 395–432; büyük harf hizasında. Kanat y 400–430'da x ≈ 885'te başlıyor; aradaki boşluk yaklaşık 40 px. Künye bandında değil. **Doğrulandı.**
- **A, açılış tırnağı:** bloğun solunda, dışarıda asılı (x ≈ 38–75). **Doğrulandı.**
- **B, parlaklık:**
  - ≥235 piksellerin 1168/1170'i damlada.
  - Damla ortalaması 213, yazı 200.
  - Yüzün sağ kenarı x ≤ 687. Saç topları yok. **Doğrulandı.**
- **Filmin açılışı:** figür artık kapaktakiyle aynı (kıvırcık baş, eğik duruş, göğüste alev). Kapak ile açılış aynı vaadi veriyor.

## Puanlar
| Ölçüt | A tur 2 | **A tur 3** | B tur 2 | **B tur 3** |
|---|---|---|---|---|
| 1 Kompozisyon (%20) | 8,5 | **9,0** | 8,6 | **9,0** |
| 2 Çizim (%25) | 8,2 | **8,8** | 7,8 | **8,8** |
| 3 Tipografi (%15) | 7,6 | **8,9** | 8,6 | **9,0** |
| 4 Üslup (%15) | 8,8 | **9,0** | 8,4 | **9,0** |
| 5 Küçük boy (%15) | 8,8 | **9,0** | 8,5 | **8,8** |
| 6 Kırmızı çizgi (%10) | 9,0 | **9,0** | 8,5 | **9,5** |
| **Ağırlıklı** | 8,4 | **8,9: RED** (eşiğin 0,1 altında, tek madde) | 8,3 | **9,0: ONAY** |

## Tur 2 bulgularının durumu
### A
| Bulgu | Durum |
|---|---|
| A-1 Tırnaklar | **Kapandı.** Asılı dizgi, Bebas ağırlığında; kapanış tırnağı büyük harf hizasında, kanada yaklaşık 40 px. Tırnaklar düz, ″ biçiminde; Bebas'ın kendi dilinde, kabul. |
| A-2 Alev tabanındaki tarak | **Kısmen.** Tarak gitti. Ama yerine gelen yuvarlak kor tabanı yeni bir soruna yol açtı (aşağıda). |
| A-3 Baş eğimi | **Kapandı.** Baş öne ve sola eğik okunuyor, 168 px'te de. Bukleler alçak; topuz okuması gitti. |
| A-4 Kanat dış kenarındaki saçak | **Kapandı.** Kenar sürekli mürekkep. İç vuruşların kenarları hafif dalgalı, ama gravür dokusu olarak kabul. |

### B
| Bulgu | Durum |
|---|---|
| B-1 Saç topları | **Kapandı** (kaldırıldı). Tespih okuması yok. |
| B-2 Yüzün sağ kenarı | **Kapandı.** Kenar eğriyi izliyor, yazıya 114 px kalıyor. |
| B-3 Islak iz | **Kapandı.** Kâğıt beyazı ve açık mavi. |
| B-4 Damla ile yazı dengesi | **Kısmen ama yeterli.** Damla yazıdan 13 birim açık (benim önerim 30'du). Doygun renk ve ≥235 tekliği odağı taşıyor. ONAY'ı engellemiyor. |
| B-5 Göz altındaki leke | **Kısmen ama yeterli.** 120 px'te hafif bir gri kalıyor; morluk gibi okunmuyor. |

## Yeni çıkan sorun (gerileme)
1. **A, alevin tabanı kâse gibi okunuyor** (x 1027–1110, y 440–476).
   - Üç dil, koyu kırmızı-kahve, yuvarlak dipli bir kütlede birleşiyor. Dibin sınırı karanlığa erimiyor, belirgin bir kâse eğrisi çiziyor.
   - Tam boyda ve 168 px'te "kandil, mumluk ya da mangal içinde alev" gibi okunuyor. Tur 1'deki "kâse" okuması başka bir biçimde geri geldi.
   - Kapağın 9'a çıkmasını tutan tek şey bu.
2. **(Küçük, puanı etkilemiyor) A, künyenin başı.** Bir ışın çizgisi künyenin başına giriyor (x 50–80, y ≈ 565). "—MILTON" gibi okunuyor. Künyenin arkasında ışınları 10 px kesmek yeter.
3. **(Küçük, B)** Göz hizasında dışa doğru sivri, kâğıt rengi bir kama var (x 600–622, y ≈ 265–280). "Kedi gözü sürmesi" gibi duruyor. İsteğe bağlı: kamayı yaklaşık %40 kısalt.

## A'yı 9'a taşıyacak tek madde
- **Alev tabanı** (x 1020–1115, y 430–480). *Son rötuş.*
  - Koyu kırmızı-kahve yuvarlak dibi kaldır. Dillerin en dış konturu y ≈ 455'te bitsin.
  - Altı belirgin bir sınır çizmesin: kor ışıması (radyal, yarıçap yaklaşık 45 px, merkez ≈ 1068, 455) pelerinin karasına yumuşakça erisin.
  - Mürekkep vuruşlarının alt uçları da sivrilerek açık bitsin.
  - Hedef: 168 px'te alev "bir kabın içinde" değil, "göğsün içinden" yanıyor gibi okunsun.

Bu düzeltme yapılırsa A'nın çizim puanı 9,2'ye, toplamı yaklaşık 9,0–9,1'e çıkar. Tek üyeli gerileme kontrolü yeterli.

## Not (kapsam dışı, film)
Filmin açılış karesindeki künye ("KAYIP CENNET · IV. 75") koyu bulutun üstünde koyu tonda kalıyor; neredeyse görünmüyor. Kurgu kurulunun dikkatine.
