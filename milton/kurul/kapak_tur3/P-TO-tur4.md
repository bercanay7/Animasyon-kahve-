# Kapak kurulu, tur 4: P-TO, B için tek maddelik gerileme kontrolü

Ölçütler ve ağırlıklar tur 1–3 ile aynı.

## Doğrulama

### Filmin ilk karesi (0–0,45 sn, `oku_is/goz1/t0000.45.png`, 1920×1080)
Göz, kaş, damla ve kolun üst kenarı kadrajda.

| Ölçü | Değer | Hedef |
|---|---|---|
| Göz konturu (x ≈ 445–1370) | ≈ 925 px, kadraj genişliğinin ≈ %48'i | ~%45 |
| Damla (x ≈ 1015–1135, y ≈ 575–800) | ≈ 225 px yükseklik | ≥ 80 px |

İstenen ölçek sağlandı. Tarama aralığı normal, yani yakınlaştırma değil yeniden çizim olduğu doğru.

### Kapak ile filmin eşleşmesi
Damla biçimi, sağ üstteki ince parlama yayı, ışınsal vuruşlu iris ve kare pencere yansıması kapak B ile aynı dilde. Fark yalnız renk: filmde siyah-beyaz, kapakta mavi. Bu kabul edilebilir (gerekçe tur 3'te).

10. saniyedeki geri çağrı planı daha geniş kadrajda (göz ≈ %35). Bu sorun değil: o plan vaadi taşımıyor, hatırlatıyor.

### Kapak B'de gerileme
| Ölçüm | Değer |
|---|---|
| ≥235 olan pikseller | 1.051; bunların 1.045'i gözyaşı sisteminde (damla, iz, parlama) |
| Yüz, %99'luk dilim | 215 |
| Yüzün en sağdaki açık pikseli | x 687 |
| Rozet bölgesi ortalaması | 19,0 (boş) |

- Göz köşesindeki kamanın kısalması 168 px'te fark edilmiyor.
- Düzeltilmiş akış testinde (`tur9/test/akis_koyu.jpg`) yan sütunda artık B var ve tur 2–3'teki gibi okunuyor.
- **Gerileme yok.**

### Kapak A
| Ölçüm | Değer |
|---|---|
| "BEN" harf yüksekliği | y 222–352 = 131 px (%18,2): eşiğin üstüne döndü |
| ≥230 olan pikseller | 606; bunların 603'ü alevde |

- Alev dibi artık kâse ya da mangal gibi değil, kor ışımasına eriyor.
- **Gerileme yok; 9,0 korunuyor.**

## B puanı (tur 3 → tur 4)
| Ölçüt (ağırlık) | t3 | **t4** | Not |
|---|---|---|---|
| 1 Anlaşılırlık (%25) | 9,0 | **9,0** | |
| 2 Merak (%20) | 8,5 | **8,5** | |
| 3 Vaat ve tutma (%20) | 8,5 | **9,5** | Vaat ilk karede, kapağın ölçeğinde ve çizim dilinde. Otomatik oynatma önizlemesinin ilk karesi de bu. |
| 4 Ayrışma (%15) | 8,5 | **8,5** | |
| 5 Kelime (%10) | 9,0 | **9,0** | |
| 6 Rozet, yazı, odak (%10) | 9,0 | **9,0** | |
| **Ağırlıklı** | 8,7 | **8,9** | 2,25 + 1,70 + 1,90 + 1,28 + 0,90 + 0,90 = 8,93 |

## Karar
- **A: 9,0, ONAY** (korunuyor).
- **B: 8,9, RED.** Eşiğin 0,07 altında; hiçbir ölçüt 7'nin altında değil.
  - Tur 3'te istediğim tek madde tam ve beklenenin üstünde karşılandı.
  - Kalan açık, kapağın yapısal tavanından geliyor: tek renkli koyu zeminin akışta ayrışması (8,5) ve "kimin gözü?" sorusunu başlığın taşıması (merak 8,5). Bunlar kapağın fikrini değiştirmeden kapanmaz ve yeni bir tur maliyetine değmez.
- **Test planı değişmedi ve onaylıyorum:** A ana kapak, B ikinci seçenek; başlık sabit `Kayıp Cennet: Şeytan Cehennemden Neden Kaçamadı? | Milton`. B'nin teste girmesine onay veriyorum: test yalnız gösterimlerin bir kısmında B'yi dener ve kazananı izlenme süresi payına göre seçer. Bundan sonra B için bir rötuş turu önermiyorum.

## En emin olmadığım nokta
Yeni ilk karede damla kadrajın merkezinde ve büyük. A'dan gelen izleyici bu 0,9 saniyede "yanlış videoya mı geldim?" diye düşünebilir mi? Etkisini düşük görüyorum, çünkü 0,9. saniyede "Ben cehennemim" figürü ve sesi başlıyor. 48. saat analizinde tutma grafiğinin ilk 3 saniyesine bakılmalı.
