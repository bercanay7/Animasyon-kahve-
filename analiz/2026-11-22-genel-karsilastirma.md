# Genel karşılaştırma: 11 uzun video ve dersler (22 Kasım 2026)

Kaynaklar: `2026-11-17-kanal-ortalamasi.md` ve ham verisi, `2026-11-18-sisifos-sonme.md`, 48. saat analizleri (Kafka, Ran, Mary Stuart), CLAUDE.md'deki Milton ve İkaros okumaları, `tahminler.md`.

**Okuma kuralı:** örneklem küçük (11 video). Bir ders kaç videoda görüldüyse o kadar güçlüdür; tek videoda görülen "ipucu"dur. Her dersin yanında kanıt sayısı var.

## 1. Videolar yan yana
Yaş farkı var: eski videolar için ilk 7 gün ya da ömür boyu, yeni videolar için 40–48. saat değeri. Karşılaştırılabilir olan sütun "2. gün testi": her video için aynı soruyu sorar.

| Video | Yayın | Süre | Konu | 2. gün göz atma testi | TO | 0:10 | 0:30 | Ort. izleme |
|---|---|---|---|---|---|---|---|---|
| Şarlken | 18 Eki | 21:27 | tarih | yok (kanalın kitlesi yoktu) | (az gösterim) | ≈85 | 78 | %43 |
| Orfeus | 22 Eki | 4:48 | mit | yok (1. gün 4 B, sonra düz) | %1,0 | ≈74 | 61 | %40 |
| **Sisifos** | 24 Eki | 7:05 | mit + felsefe | **11,7 B**, sonra 3 dalga daha | %2,2 | ≈79 | 61 | %42 |
| **Abdülhamid** | 29 Eki | 6:20 | Türk tarihi | **7,0 B** | %1,5 | ≈77 | 63 | %41 |
| **Prometheus** | 31 Eki | 23:56 | mit + felsefe | **17,6 B** | %1,9 | ≈84 | 72 | %38 |
| Medici | 5 Kas | 10:02 | tarih | 2,9 B, o gün TO %0,9 → söndü | %1,7 | ≈72 | 52 | %31 |
| Milton | 12 Kas | 25:46 | edebiyat | yok | %1,4–1,6 | ≈76 | 68 (40 sa) | %26 |
| İkaros | 14 Kas | 5:55 | mit | küçük (→ 9,5 B) | %0,8 | ≈66 | ~48 | %37 |
| Kafka | 16 Kas | 6:39 | edebiyat | yok (2,8 B) | %1,9 | ≈74 | 64 | %45 |
| Ran | 17 Kas | 8:03 | film | yok (2,2 B; 7. gün 3,9 B) | **%3,0** (7. gün %2,8) | ≈80 | 66 (7. gün 63) | %39 (7. gün %38) |
| Mary Stuart | 20 Kas | 20:49 | kitap + tarih | yok (2,2 B; 7. gün 3,0 B) | %2,3 (7. gün %2,4) | **≈88** (7. gün ≈87) | **70** (7. gün 70; Studio 74) | %36 (7. gün %37) |
| Narkissos | 24 Kas | 8:52 | mit + psikoloji | yok (46. sa 2,4 B) | %2,8 | – | – | **%48** |
| **Medyan** | | | | | %1,8 | ≈77 | 61 | %40 |

## 2. Dağıtım: izlenme neden az?
**Gözlem (11 video):** göz atma testi ya 2. gün gelir ya hiç gelmez. Gelen üç video (Sisifos, Abdülhamid, Prometheus) 24 Ekim – 31 Ekim arasında çıktı. 12 Kasım'dan beri altı video üst üste testi almadı.

**Elenen açıklamalar** (veri bunları zayıflatıyor):
- **"Kapak ve başlık zayıf":** son üç videonun TO'su %1,9–3,0, Sisifos'un ilk 7 günündeki %2,2'den düşük değil. Ran kanalın en yüksek TO'suyla test almadı.
- **"Video kötü":** Mary Stuart'ın açılışı (0:10 %88, 0:30 %70) ve Kafka'nın ortalaması (%45) kanalın en iyileri. Sisifos'un tutması daha yüksek değildi (0:30 %61).
- **"Uzun video cezası":** Prometheus 24 dakikayla en büyük testi aldı.
- **"Yayın sıklığı tek başına":** Prometheus, Abdülhamid'den iki gün sonra çıktı ve test aldı.

**Kalan açıklamalar** (ikisi de veriyle uyumlu, ayrılamıyor):
1. **Kanalın izleyici havuzu (Sisifos etkisi):** test gelen videolar Sisifos günde 18–22 B gösterimdeyken çıktı. Sisifos söndükçe (8 Kasım'dan beri ~3 günde bir yarılanarak) yeni videoların testi küçüldü (İkaros 9,5 B → Kafka 2,8 B → Ran ve Mary 2,2 B). YouTube yeni videoyu önce kanalı izlemiş kişilere gösteriyor; o kişilerin çoğu Sisifos'tan geldi.
2. **Kapının gücü:** Sisifos ilk dalgasını havuz yokken aldı (Orfeus'un o güne kadarki izleyicisi ~200). Konusu Türk YouTube'unda zaten geniş bir izleyicisi olan Camus ve absürt, sorusu izleyicinin kendi hayatına sorulan bir soruydu. Yani havuz yokken de dalga mümkün; bunun için konunun kendi izleyici kitlesi büyük olmalı.

**Sonuç:** iki açıklama da aynı yere çıkıyor. Kanalın büyümesi şu an tek tek videoların kalitesine değil, **yeni bir kapıya** bağlı: kendi kitlesi geniş bir konudan gelecek ve havuzu yeniden dolduracak bir video. Narkissos ("narsisizm") tam bu denemedir.

## 3. Paketleme dersleri
| Ders | Kanıt | Güç |
|---|---|---|
| **Talep kontrolü TO'yu medyanın üstüne taşıyor.** Kuraldan önceki yedi videonun TO medyanı %1,6; kuraldan sonraki üçünde %1,9 / %3,0 / %2,3. | 10 video | güçlü |
| Tanıdık kapı başlıkta öne alınınca (Kral Lear, I. Elizabeth) TO yükseliyor; kapı zayıfken (Milton, İkaros) en düşük TO'lar. | 5 video | güçlü |
| Kapak testinde iki seçenek aynı fikrin iki yazılışıysa sonuç berabere (Prometheus, Abdülhamid, Medici). Tek net kazanan iki ayrı vaat taşıyan Sisifos'tu. | 4 video | orta |
| Yayından sonra paketlemeyi değiştirmek ölü videoyu diriltebilir (Abdülhamid: 372 → 1.101 görüntüleme). | 1 video | ipucu |
| **TO tek başına dalga getirmiyor.** Ran %3,0 ile test almadı; Medici testte TO %0,9'a düşünce söndü. TO gerekli ama yeterli değil. | 3 video | orta |

## 4. İzleyiciyi tutan ve kaybettiren (eğri dersleri)
| Ders | Görüldüğü yer | Kanıt |
|---|---|---|
| **İlk kare kapağın vaadi, somut ve dramatik.** En iyi 0:10'lar: Mary Stuart 88 (idam sabahı, kırmızı), Şarlken 85, Prometheus 84, Ran 80. En kötü İkaros 66. | 6 video | güçlü |
| **Kancadan hikâyeye köprü sıfır cümle; en çok bir kimlik cümlesi.** Köprüde kayıp: İkaros (Ovidius), Kafka (bilinen ilk cümle), Ran (Shakespeare, −9). Mary Stuart'ta tek kaynak cümlesi + kişisel soru yalnız −3. | 4 video | güçlü |
| **Somut olay tutar, soyut açıklama düşürür.** Mary: arma ve meşruiyet 24 sn'de −11, Rizzio ve Babington bölümleri dümdüz. Ran: üç kaybın üçü de karşılaştırma ya da kavram. İkaros: hikâye bitip yorum başlayınca. | 3 video, 8 nokta | **en güçlü** |
| **Yazar adı sorun değil; olaydan kopuk açıklama sorun.** Mary'de "Zweig'a göre" yargıları tuttu (tahmin M2 tutmadı), Ran'da yazar + yapım anekdotu "Önemli an" oldu. | 2 video | orta |
| **Ad değil, ad + geçmiş anlatımı düşürür.** Ran'da Tsurumaru ve Sue geçmişleriyle girince −18; Mary'de Walsingham ve Babington eylemle girince 0. Medici: çok ad + soyut finans. | 3 video | orta |
| **Ana merak sorusunun cevabı bir sahnedir, kavram değil.** Ran 2:20 ("eklediği şey: geçmiş") ve Mary 17:40 ("Neden kırmızı?" yorumu, −7): cevap kavram olunca kayıp. | 2 video | orta |
| **Hikâye bitince izleyici gider;** iksir ve çağrı hikâyenin son anına bağlanır. İkaros (yorum bölümü), Mary (doruktan sonra 45 sn'de −7); Ran'da çağrı son ana bağlıydı, yalnız −2. | 3 video | güçlü |
| **Bölüm damgaları gezinme aracıdır:** izleyici bölüm başlarına ve kapağın vaat ettiği ana atlıyor (Ran'da üç bölüm başında yükseliş; Mary'de kırmızının ortaya çıktığı ana atlama). | 2 video | orta |
| **İzleyici belgeye ve dönüm anına geri sarıyor:** Mary'de Elizabeth'in mektubu, Paulet'nin reddi, "kraliyet ailesi Mary'nin soyundan"; Milton'da dört küçük artış; Sisifos'ta doruk. Shorts bu anlardan seçilir. | 3 video | orta |
| **Uzunluk tutmayı bozmuyor:** ortalama izleme yüzdesi her uzunlukta %35–45 bandında (istisna Milton %26). Gösterim başına izlenme süresinde uzun videolar önde (Mary 0,17 dk, Prometheus 0,11). | 10 video | güçlü |

## 5. Ölçme dersleri
- **Aynı yaştaki veriyle karşılaştır:** ilk 48 saatin 0:30'u aboneler yüzünden şişer (Milton 40. saatte %68, 4. günde %56).
- **Tahmin yayından önce yazılır:** Mary Stuart'ta üç tahminin ikisi tuttu. Tutmayan (M2) kuralı inceltti: "göre" sözcüğü değil, olaydan kopuk açıklama.
- **Tempo aracı geriye dönük doğru yeri buluyor:** `tempo_kontrol.py` Mary Stuart'ta ilk iki dakikadaki tek soyut diziyi (B06–B07, 1:12–1:30) işaretledi; filmin en büyük içerik kaybı tam orası. Art arda soyut üç diziden ikisi gerçek kayıp (1:12, 17:38), biri tutmadı (4:19 Zweig yargıları). 22 Kasım'dan beri araç ilk iki dakikadaki soyut adayları ayrıca "E" ile işaretliyor.
- **Eğri ~100–150 izleyicilik:** bir izleyici ≈ 1 puan. Tek videodaki küçük kıpırtı ders değildir; ders iki üç videoda görülen örüntüdür.

## 6. Sonraki adımlar (öneri)
1. **Üretimde değişmeyecekler:** talep kontrolü, köprüsüz kanca, somut olay ilkesi, çağrının hikâyenin son anına bağlanması. Bunlar artık çok videoda doğrulandı.
2. **Bir sonraki senaryoya eklenecekler:**
   - ilk iki dakikada soyut arka plan yok (gerekiyorsa bir nesne ya da sahneyle);
   - ana sorunun cevabı bir sahne;
   - doruğu taşıyacak kişi ilk perdede eylemle ekilir.
3. **Dağıtım için denemeler:**
   - **Narkissos'a temiz bir hafta:** 24 Kasım'da çıkarsa Mary Stuart'ın penceresiyle çakışır, sonuç yine okunamaz. Öneri 27 Kasım. Karar kullanıcının.
   - **Kapı videosu:** Narkissos test alırsa "kapının gücü" açıklaması güçlenir; ardından ≥5 gün sonra çıkan video da test alırsa "havuz" açıklaması da güçlenir.
   - **Shorts ayrı içeriktir:** uzun videoya izleyici taşımıyor (Milton), ama kanalın havuzunu büyütür. Eğrideki artışlardan seçilir; en güçlü cümle ilk saniyede.
   - **Dış paylaşım:** havuz küçükken YouTube dışından gelen izleyici yeni sinyal verir; maliyeti yok.
4. **Ölçüm:** her yeni video bu tabloya 48. saat ve 7. gün satırıyla eklenir.
