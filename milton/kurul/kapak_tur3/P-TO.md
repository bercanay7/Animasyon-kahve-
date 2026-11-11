# Kapak kurulu, tur 3: P-TO (gerileme kontrolü)

Ölçütler ve ağırlıklar tur 1–2 ile aynı. Eşik 9,0; hiçbir ölçüt 7'nin altında olamaz. Koordinatlar 1280×720'dir.

Bakılanlar:
- kapaklar: `kapak_a.jpg`, `kapak_b.jpg`;
- film kareleri: `nif_is/v7b/t0004.60.png`, `goz0/ozet.jpg`;
- akış testi: `tur8/test/akis_koyu.jpg`;
- ölçümler PIL ile kendim yaptım.

## İddiaların doğrulanması
| İddia | Ölçtüğüm | Sonuç |
|---|---|---|
| Filmin açılış figürü kapağa uyduruldu | Doğru. t = 4,6 sn'de eğik baş, bukleler, tüylü kanat ve üç dilli alev var; sahne kapakla aynı. Filmde alev beyaz, kapakta turuncu (kabul edilebilir, tur 1'den beri biliniyor). | Kapandı |
| B: ilk kare göz + damla (0–0,9 sn), ardından figüre kesme | Doğru (`goz0/ozet.jpg`). Ancak filmdeki kadraj geniş ve damla küçük: 1920 genişlikte yaklaşık 25 px. Kapakta damla ≈ 190 px ve vurgu ögesi. | Büyük ölçüde |
| A: zemin açıldı; alev dışı en parlak 209; ≥230 piksellerin %100'ü alevde | Sol zemin ortalaması 199 (tur 2'de 188). ≥230 olan 654 pikselin 649'u alevde, 5'i kanat kenarında (x 883–1005, y 221–296). Alev dışı %99,9'luk dilim 214. | Doğru (pratikte %99) |
| A: tırnaklar ve künye | Tırnaklar Bebas ağırlığında. Künye ≈ 27 px ve 246 px boyda okunuyor. Kapanış tırnağı künye bandında değil. | Doğru |
| B: yüzün sağ kenarı sadeleşti, x 687 | En sağdaki açık piksel x = 687. Yazıya ≈ 115 px kalıyor. | Doğru |
| B: yüz tepe 210; ≥235 piksellerin %100'ü damlada | Yüzün %99'luk dilimi 215, yazınınki 212. ≥235 olan 1.046 pikselin 968'i damlada; kalanı damlanın ıslak izinde (x ≈ 450, y 373–450) ve göz bebeği parlamasında. Yani tamamı gözyaşı sisteminde. | Doğru |
| B: saç topları kaldırıldı | Doğru. | Kapandı |

## Gerileme var mı?
- **A, yazı boyu:** "BEN" harf yüksekliği y 225–353 = 129 px (%17,9). Tur 2'de 133 px (%18,5) idi. Eşiğin hemen altında; 168 px'te fark görünmüyor. Puan düşürmedim, not olarak yazdım.
- **Test seti hatası:** `tur8/test/akis_koyu.jpg`'de yan sütunun 5. satırında B yerine A'nın tur 2 sürümü (tırnaklı “ ” ve künyeli eski çizim) duruyor. Bu, B'nin akış görüntüsünün bu turda test edilmediği anlamına geliyor. Kapağın değil, test setinin hatası. B'nin akışta nasıl durduğunu tur 2'deki akış testinden ve kendi küçültmemden değerlendirdim.
- Başka gerileme görmedim.

## Puanlar (tur 2 → tur 3)
| Ölçüt (ağırlık) | A t2 | **A t3** | B t2 | **B t3** |
|---|---|---|---|---|
| 1 Anlaşılırlık (%25) | 9,0 | **9,0** | 8,5 | **9,0**: tarak kenar ve toplar gitti |
| 2 Merak (%20) | 8,5 | **9,0**: başlık 1 + 17. saniyedeki soru ("Onu orada tutan ne?") + kapaktaki cevap ipucu birbirine oturdu; tırnaklar artık doğal | 8,5 | **8,5** |
| 3 Vaat ve tutma (%20) | 9,0 | **9,5**: film figürü kapakla aynı | 7,5 | **8,5**: vaat ilk karede (0–0,9 sn), ama filmdeki damla küçük ve siyah-beyaz |
| 4 Ayrışma (%15) | 8,5 | **9,0**: zemin açıldı, akışta artık çamurlu değil | 8,5 | **8,5** |
| 5 Kelime (%10) | 8,5 | **8,5** | 9,0 | **9,0** |
| 6 Rozet, yazı, odak (%10) | 9,0 | **9,0** | 8,0 | **9,0**: odak tek |
| **Ağırlıklı** | 8,8 | **9,0: ONAY** | 8,3 | **8,7: RED** (teste girmesine onay veriyorum, aşağıya bak) |

- A: 2,25 + 1,80 + 1,90 + 1,35 + 0,85 + 0,90 = 9,05.
- B: 2,25 + 1,70 + 1,70 + 1,28 + 0,90 + 0,90 = 8,73.

## Filmdeki damlanın siyah-beyaz kalması
Bu karara katılıyorum.
- Film tek renkli, kapakta tek vurgu rengi kullanmak kanalın kapak kuralı. A'da da alev filmde beyaz, kapakta turuncu.
- İzleyicinin tanıyacağı şey renk değil, "büyük göz + düşen damla" imgesi.
- Sorun renk değil **ölçek.** 0–0,9 sn'deki planda damla yaklaşık 25 px, yani kadrajın %1'inden az. Kapaktaki imgeyi bu kadar kısa sürede tanıtacak kadar büyük değil.

## Tur 2 bulgularının durumu
| Tur 2 bulgusu | Durum |
|---|---|
| A-1 Filmin açılış figürü kapakla eşleşsin | **Kapandı** |
| A-2 Zemin açılsın (≈198), alev dışı ≤210 | **Kapandı** (199 / 214; ihmal edilebilir sapma) |
| A-3 Künye büyütülsün (isteğe bağlı) | **Kapandı** |
| B-1 Göz planı açılışta | **Büyük ölçüde kapandı.** 6,3 sn yerine 0 sn'de ve ses başlamadan; bu daha iyi bir çözüm. Ölçek sorunu açık. |
| B-2 Sağ kenarın tarak etkisi | **Kapandı** |
| B-3 Yüz beyazı ≤215, odak damlada | **Kapandı** |
| B-4 Sol üstteki toplar | **Kapandı** (kaldırıldı) |

## B'yi 9'a taşıyacak madde (tek madde)
1. **Filmdeki 0–0,9 sn göz planını kapağın kadrajına yaklaştır.**
   - Göz + damla alanına ≈ 2,5× yakınlaş. Göz kadraj genişliğinin ≈ %45'ini, damla ≥ 80 px'i (1920 düzleminde) kaplasın.
   - Plan ses başlamadan ve kesmeden önce olduğu için A01 → A02 eşleme kesmesini etkilemez.
   - Siyah-beyaz kalabilir.
   - Bu yapılırsa vaat 8,5'ten 9,5'e çıkar; B ≈ 8,9–9,0 olur.

## Test planı
**Onaylıyorum: A ana kapak, B ikinci seçenek.**
- Başlık sabit: `Kayıp Cennet: Şeytan Cehennemden Neden Kaçamadı? | Milton`.
- B'nin teste girmesine 8,7 ile onay veriyorum. Eksik kalan tek ölçüt vaat. Vaat zaten ilk karede karşılanıyor; ölçek sorununu en doğru "Test ve karşılaştır" ölçer, çünkü kazananı izlenme süresi payına göre seçiyor. B'nin vaadi tutmazsa test onu cezalandırır ve A kalır.
- Yukarıdaki tek maddelik düzeltme yapılırsa B de eşiği geçer; yapılması önerilir, ama yayını bekletecek kadar değil.
- Yayından önce `tur8/test/akis_koyu.jpg` B ile yeniden üretilip bir kez bakılmalı (test seti hatası).

## En emin olmadığım nokta
0,9 sn'lik sessiz göz planının A'dan gelen izleyiciyi kısa bir an şaşırtıp şaşırtmayacağı. A'nın vaadi ("Ben cehennemim") 0,9. saniyede başlıyor, yani etkisini düşük görüyorum. Ama bunu ancak tutma grafiğinin ilk 3 saniyesi gösterir. 48. saat analizinde bakılmalı.
