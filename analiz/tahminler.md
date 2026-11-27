# Tempo tahminleri (yayından önce yazılır, 48. saatte sınanır)

**Neden:** eğri nerede düştüğünü gösterir, nedenini göstermez. Tahmin yayından önce yazılmazsa her düşüşe sonradan bir açıklama bulunur. Burada yazılan tahmin değiştirilmez; sonuç sütunu 48. saat ve 7. gün verisiyle doldurulur. Tutan tahmin ipucunu kurala çevirir, tutmayan kuralı zayıflatır.

**Araç:** `araclar/analiz/tempo_kontrol.py senaryo.json timeline.js --yazar "..."` (aday listesi; karar başkanın).
**Ölçüm:** `araclar/analiz/elde_tutma.py` (Studio ekran görüntüsünden eğri). Eğri ~100–400 izleyicilik; bir izleyici ≈ 1 puan. ±3 puanın altındaki fark "yok" sayılır.
**Gövde ortalaması:** 1:00 ile hikâyenin bittiği an arasındaki dakika başına kayıp (puan/dk). Bir bölümün "dik" sayılması için bunun en az 1,5 katı olmalı.

**Aracın Ran'da sınanması (geriye dönük, 20 Kasım):** iki "art arda soyut" dizisi Ran'ın en kötü iki yerine düştü (0:15–0:41 köprü; 2:20–2:32 Studio düşüşü). İkinci yarıdaki yeni adlar Tsurumaru ve Sue'yu buldu (gövdenin büyük düşüşü). En iyi tutan yapım bölümü yalnız "yazar anılıyor" (Y) işareti aldı, soyut sayılmadı. Yani araç geçmiş veride doğru yeri gösterdi; ileriye dönük değeri aşağıdaki tahminlerle sınanacak.

---

## Mary Stuart (20:49; yayın 20 Kasım 18:00; 48. saat 22 Kasım, 7. gün 27 Kasım)
| # | Tahmin | Nasıl sınanır | Sonuç |
|---|---|---|---|
| M1 | Kancadan sonra tek kaynak cümlesi (0:33 "Stefan Zweig'ın anlattığı bu hikâyede biri kalbiyle yaşar, öteki aklıyla") ve kişisel soru ("Sen hangisisin?"), hikâye 0:40'ta. Köprü kaybı Ran'dakinden (9 puan) küçük: 0:31–0:42 arasında ≤5 puan. | 0:31 ve 0:42 değerleri | **Tuttu** (45. saat): 0:31 %70 → 0:42 %67, 3 puan. 0:10 %88, 0:30 %70: kanalın en iyi açılışı. **7. gün:** 0:31 %69 → 0:42 %64, 5 puan; sınırda tuttu. |
| M2 | 4:19–4:44 "Zweig'a göre…" art arda iki yorum cümlesi (D14–D15): bu 25 sn'de yerel düşüş (≥3 puan) ya da Studio "Düşüş" işareti. | eğri + Studio işaretleri | **Tutmadı:** 4:19–4:44 %48 → %51 → %49, düşüş yok; Studio düşüşü 12:35–12:47 (sayvandaki söz). Yazarın somut bir seçim hakkındaki yargısı tutuyor; "göre" kendi başına işaret değil. **7. gün:** yine tutmadı (%46 → %49 → %50,5). |
| M3 | İki kuralın çatıştığı yer: ikinci yarıda yeni kişiler (Walsingham 13:21, Babington 14:06) ama anlatım somut (fıçılarda mektup, şifre, kopya). Başkanın tahmini: **somut olay ağır basar**, 13:20–14:40 dik değil. Tutmazsa "yeni ad" ipucu kurala yaklaşır. | 13:20–14:40 dakika başına kayıp / gövde ortalaması | **Tuttu:** 0 puan/dk (gövde 1,5); bölüm boyunca %43 dümdüz. Somut olay yeni adlara ağır bastı. **7. gün:** yine 0 puan/dk (gövde 1,6). |

## Narkissos (8:52; yayın 24 Kasım 18:00 (kullanıcı, 23 Kasım); 48. saat 26 Kasım, 7. gün 1 Aralık)
| # | Tahmin | Nasıl sınanır | Sonuç |
|---|---|---|---|
| N1 | Köprü yok (kanca sorusu A05'ten sonra ilk cümle hikâye, 0:33). 0:20–0:45'te Ran'daki "düşüp geri çıkma" görülmez; 0:30 (48. saat) ≥ %65. | 0:20–0:45 eğrisi, 0:30 | **Tuttu.** 0:32 %67 (Studio "0:30'da %67,3"); 0:21 %70 → 0:48 %66, düşüp geri çıkma yok (Ran'da 0:31–0:40 −10). |
| N2 | Hikâye 6:23'te bitiyor; ardından 2 dakikalık kavram tarihi (1646 öğüt kitabı, 1898 hekim, 1899 psikiyatr, Freud). Filmin büyük gövde düşüşü burada, en dik yer F06–F07 (7:19–7:40, "Freud'a göre… Ona göre…", aracın tek soyut dizisi). 6:23–7:50 dik (≥1,5 × gövde ortalaması). | dakika başına kayıp | **Tuttu.** 6:21 %47 → 7:52 %38: 5,9 puan/dk; gövde (1:00–6:21) 2,8 puan/dk → **2,1 ×**. En dik 6:32–6:59 (−4) ve 7:20–7:52 (−3). Studio işareti yok. |
| N3 | 0:49 Delfi öğüdü (tek bağlam cümlesi, hikâyenin içinde): küçük, ≤3 puan. | 0:45–1:00 | **Sınırda tutmadı.** 0:48 %66 → 0:59 %62 (−4; ±3 gürültü eşiğinin hemen üstü). |

## Dorian Gray (8:16; yayın 28 Kasım 18:00 (kullanıcı, 23 Kasım); 48. saat 30 Kasım, 7. gün 5 Aralık)
| # | Tahmin | Nasıl sınanır | Sonuç |
|---|---|---|---|
| D1 | Kanca kurala uygun: kimlik tek cümle (A02 Wilde, 1890) + somut söz (A03 "Bu örtünün altını yıllarca kimse görmedi. Biz göreceğiz."), hikâye 0:24. Köprü kaybı yok; 0:17–0:30 düz ya da yükselen (Kafka'daki söz gibi). 0:30 (48. saat) ≥ %65. | 0:17–0:30, 0:30 | |
| D2 | 1:15 B07 dergi/kitap karşılaştırması: tek soyut cümle; küçük düşüş olabilir, ≤4 puan. | 1:12–1:25 | |
| D3 | **Doğal deney (N2 ile karşılaştırma):** hikâye 6:43'te bitiyor; ardından gelen bölüm somut bir anekdot (1895 mahkemesi, avukat romandan sayfa okur, Wilde hapse girer). Tahmin: 6:45–7:35 dik değil (< 1,5 × gövde ortalaması) ve Narkissos'un 6:23–7:50'sinden yatık. İki video da hikâye bittikten sonra gerçek dünyaya geçiyor; biri somut, biri soyut. | iki videonun aynı bölümü yan yana | |

## Lale Çılgınlığı (10:02; yayın 10 Aralık 2026 18:00 (27 Kasım: şerit denemesi için Frankenstein'la yer değiştirdi; önce 6, 2 ve 11 Aralık); 48. saat = 12 Aralık 18:00, 7. gün = 17 Aralık)
Yazıldı: 22 Kasım 2026, senaryo rev2 (seslendirmeden önce). Zamanlar seslendirmeden sonra cümle kimliğinden eklendi; tahminin içeriği değişmedi.
**Zamanlar:** B01 0:44,6 (ilk 20 sn: 0:44,6–1:04,6); F08 5:18,4 – F11 sonu 5:51,0; G01 5:53,0 (+30 sn: 6:23); I03 8:01,3 – I07 sonu 8:45,9.
**Not (Fable son okuması, 22 Kasım, yayından önce):** üç izleyici kişiliği de ilk düşüşü 0:44–1:33'te gördü ("önce seksen yıl geriye" ile üçüncü zaman sıçraması, adsız elçi ve botanikçi, Latince mektup). L1 bu tahmine karşı çıkan bir okuma; yayından önce görüntüyle karşılandı (B01'in ilk 4,8 sn'sinde 1554 · 1637 · 1730 zaman çizgisi; B04'te çarşıda akçeyle çiçek; B05'te soğan sandığı). L1 bu hâliyle sınanır; tutmazsa düşüş görüntünün değil anlatımın sorunudur (seslendirme sabit kaldı).
| # | Tahmin | Nasıl sınanır | Sonuç |
|---|---|---|---|
| L1 | Kanca uzun (~44 sn: Alkmaar mezadı + İstanbul ikizi + "Lale Devri adını kim koydu?") ve ardından zaman sıçraması ("Önce seksen yıl geriye: 1554"). Sıçrama somut bir sahneyle (elçiye çiçek sunuluyor) açıldığı için köprü kaybı yok: B01'in ilk 20 sn'sinde ≤ 4 puan; 0:30 (48. saat) ≥ %65. | B01 ± 20 sn, 0:30 | |
| L2 | **Doğal deney (Mary Stuart M2 ile aynı soru):** efsanenin çürütülmesi (F08–F11, Goldgar) bir yorum değil, olay olarak kuruldu (arşive dönüş, "bulamıyor", "tutulmayan sözler"). Tahmin: F08–F11 dik değil (< 1,5 × gövde ortalaması). Tutmazsa: izleyici çürütmeyi olay değil açıklama sayıyor. | F08 başı – F11 sonu, dakika başına kayıp / gövde | |
| L3 | **Türk izleyicinin kapısı:** İstanbul bölümü (G01) yeni bir "ikinci hikâye" açar; doruk kişileri kancada ekildiği ve "Lale Devri" okuldan tanıdık olduğu için G01'den sonraki 30 sn'de düşüş yok (≤ 2 puan) ya da yükseliş; "Ad" bölümü (A07'nin merakının cevabı, I03–I07) Studio'da "Önemli an" ya da yerel yükseliş. | G01 + 30 sn; I03–I07 eğri ve Studio işaretleri | |

## Gılgamış (11:17; yayın 2 Aralık 2026 18:00 (kullanıcı, 23 Kasım: Lale'den önce; önce 6 Aralık); 48. saat = 4 Aralık 18:00, 7. gün = 9 Aralık; 23 Kasım yazıldı, seslendirmeden önce; zamanlar seslendirmeden sonra eklenir, tahmin değişmez)
**Zamanlar (seslendirmeden sonra, 23 Kasım; tahminler değişmedi):** A05 0:32,1, B01 0:42,3 (hikâye başı), B03 sonu 1:05,0; D04 3:38,7 – D13 sonu 4:51,8; E09 6:23,2; H04 sonu 10:01,0; H05 10:02,5 – H10 sonu 10:51,1.
| # | Tahmin | Nasıl sınanır | Sonuç |
|---|---|---|---|
| G1 | Kanca kurala uygun: kanca sorusundan (A05) sonraki ilk cümle hikâye (B01), kimlik kancanın içinde. Kancanın kendisi iki somut sahne (bitki/yılan, ölü dost) ve bir alıntı (surlar). 0:30 (48. saat) ≥ %65 ve kanca sonu → B03 arasında ≥ 3 puanlık düşüş yok. | 0:30; A05–B03 aralığı | |
| G2 | Yatağın başı (D04–D13: Şamaş'ın sözü, kalbin durması, gelin gibi örtme, "burnundan kurt düşene kadar") filmin en iyi tutan bölümü: ya Studio "Önemli an" bu aralıkta ya da bölümde dakika başına kayıp gövde ortalamasının yarısından az. | Studio işaretleri; dakika başına kayıp | |
| G3 | Hikâye H04'te (surun içi) bitiyor; ardından ~50 sn kuyruk (destanın açılışı, sandık ve tablet, Hattuşa, "yabancı sensin", soru). Kuyruk somut nesne ve olaylarla kurulduğu için dik değil: H05–H10 dakika başına kayıp < 1,5 × gövde ortalaması (Narkissos N2'deki soyut kuyruğun tersi). İkinci yarıda ilk kez adı geçen Urşanabi (E09; rolü kancada ekildi) düşüş getirmez (≤ 3 puan). | H05–H10 ve E09 çevresi | |

## Frankenstein (11:04; yayın 6 Aralık 2026 18:00 (kullanıcı, 27 Kasım: şerit denemesi için Lale'yle yer değiştirdi); 48. saat = 8 Aralık 18:00, 7. gün = 13 Aralık; 23 Kasım yazıldı, render'dan önce)
**Zamanlar (seslendirmeden sonra):** A05 0:34,3, B01 0:44,6 (hikâye başı); kör adam E02–E04 6:02–6:22; F03 7:18; G02 8:33 (halka); H01 9:10 – H10 sonu 10:37.
| # | Tahmin | Nasıl sınanır | Sonuç |
|---|---|---|---|
| F1 | Kanca iki kapak vaadini ilk cümlede karşılıyor (el ve "18 yaşında"); hikâye 0:44,6'da başlıyor. 0:30 (48. saat) ≥ %65 ve A05 → B03 (0:34–1:08) arasında ≥ 3 puanlık düşüş yok. 1816 bölümü (B, 0:44–2:56) ilk iki dakikanın soyutluk riskini taşıyor (Tambora, yarış): B07 (1:34–1:48) çevresinde düşüş kanca sonrası ortalamayı aşmaz. | 0:30; 0:34–1:08; 1:34–1:48 | |
| F2 | Yaratığın birinci tekil anlatısı (D01–F05, 4:05–7:45) filmin en iyi tutan bölümü: ya Studio "Önemli an" bu aralıkta (özellikle kör adam, 6:02–6:30) ya da bu aralıkta dakika başına kayıp gövde ortalamasının yarısından az. | Studio işaretleri; dakika başına kayıp | |
| F3 | Hikâye G05'te (9:07) bitiyor; ardından ~90 sn Mary bölümü (adsız kitap, afiş, 1831 önsözü, 1815 günlüğü, "çirkin evladım"). Kapak B'nin ve peşinden gidilen sorunun cevabı burada olduğu için kuyruk dik değil: H01–H10 dakika başına kayıp < 1,5 × gövde ortalaması. Tutmazsa kanal dersi güçlenir: yazarın hikâyesi bile, yaratığın hikâyesi bitince "ek" sayılıyor. | H01–H10 | |


## Çernobil'in çayı (14 Aralık 2026 önerisi; 24 Kasım'da, seslendirmeden önce yazıldı)
Zamanlar tahmini (seslendirmeden sonra `cernobil/timeline.js` ile güncellenir).
| # | Tahmin | Ölçü | Sonuç |
|---|---|---|---|
| Ç1 | Kapı kanalın en büyüğü ("çernobil" medyanı Sisifos'un 8 katı): gösterim ilk 48 saatte kanalın uzun video medyanını iki katından fazla aşar; TO ≥ %2,5 (başlıkta "sen" ve kapakta bilinen sahne). | 48. saat gösterim, TO | |
| Ç2 | Kanca (0:00-0:30) iki bilinen olguyla (bardak ↔ 56 bin ton) açılıyor, köprü yok: 0:30'da kalan ≥ %65 (kanal medyanı %61). | elde tutma 0:30 | |
| Ç3 | "Depo" bölümü (vadi, valiler, fırın, kırık seralar, çürüme, fabrika bahçeleri, köylülerin sorusu) somut olay dizisi: dakika başına kayıp gövde ortalamasından düşük; "Ölçülmeyen" (bilimin cevabı yok) bölümü ise ortalamanın üstünde kaybettirir. Tersi çıkarsa ders: belirsizlik dürüstlüğü izleyiciyi tutuyor. | bölüm bölüm dakika başına kayıp | |

---

## Stanford Hapishane Deneyi (18 Aralık 2026 önerisi; 48. saat = 20 Aralık 18:00, 7. gün = 25 Aralık; 25 Kasım'da, seslendirmeden önce yazıldı)
Yeni değişken: senaryodan önce kanca araştırması (`stanford/arastirma/`). Araştırmanın getirdiği tek yeni şey sorudan hemen sonra ikinci kanca (bant); ST1 onu sınar. (S1–S3 adları Narkissos Shorts tahminiyle çakıştığı için 25 Kasım'da ST1–ST3 oldu.)

| # | Tahmin | Ölçü | Sonuç |
|---|---|---|---|
| ~~S1~~ ST1 | **İkinci kanca** (bant, ilk 5 sn'de teyp ayrıntısı + ≈0:15'te bant ve "ondan bir şey istiyor").<br>(a) **Şekil:** 0:10'dan 0:30'a kayıp ≤ 6 puan (Kafka −9, Ran −13, Mary −18); ≈0:17–0:30 arasında eğri ≥ −2.<br>(b) **Mutlak:** 48. saatte 0:30 ≥ %72 (aynı yaştaki 6 videonun 0:30 medyanı 67: Mary 70, Prometheus 70, Milton 68, Ran 66, Kafka 64, İkaros ~48; ön okuma), 7. günde ≥ %66 (karar).<br>Tutmazsa ders: kancaya ikinci vaat eklemek kanalda tek soru kadar etkili değil. (25 Kasım: S1 → ST1, çıta kanal dersleri §15'e göre yeniden yazıldı; sayılar 18 Aralık'tan önce Studio verisiyle kilitlenir.) | elde tutma 0:10, 0:30 (48. saat ve 7. gün) | |
| ~~S2~~ ST2 | III. bölüm (bant: müdür ↔ Mark, zaman damgalı sözler) filmin en düz bölümü olur: dakika başına kayıp gövde ortalamasının altında; bölüm başı yükselişinin en büyüğü "III. Bant"ta. Tersi çıkarsa ders: iki kişinin dökümü, soyut olmasa da, uzun alıntı dizisi olarak düşürüyor. (rev2: bölüm sonundaki iddia–karşı iddia kuyruğu tek cümleye indi.) | bölüm bölüm dakika başına kayıp; bölüm başı yükselişleri | |
| ~~S3~~ ST3 | Son 60 sn ("Peki." ve soru), Mary Stuart'taki doruk sonrası kaybın (45 sn'de −7) yarısından az kaybettirir; izleyicinin kendi cevabını yazdığı yorumların oranı kanalın önceki videolarından yüksek olur. | son dakika eğrisi; yorum sayısı ve içeriği | |

**Stanford, yayından önce eklenen not (26 Kasım, rev3 ve Fable'ın üç izleyici okumasından sonra):** üç izleyicinin ortak düşüş yerleri 2:30–2:46, 3:46–4:20, 6:04–6:17 ve 6:36–7:22. Sonuncusu (bant bölümünden sonra dört kaynak) üçünün de en olası bırakma anı. 48. saatte bu dört aralığın dakika başına kaybı gövde ortalamasıyla karşılaştırılır; ST2 (bant bölümü düz) 4:21–6:36 için geçerli. Film rev3'te 11:11'den 11:53'e uzadı: son bölüm müdürün notuyla (F03b) bitiyor; ST3'teki "son 60 sn" 10:53–11:53 olarak okunur.

## Dağıtım sınaması: kanal sorunu mu, havuz mu? (23 Kasım 2026, Narkissos yayından önce yazıldı)
**Soru (kullanıcı, 23 Kasım):** Elizabeth Shorts'u ~400 izlendi (kanalın en düşük Shorts'u); 12 Kasım'dan beri altı uzun video büyük göz atma testi almadı. Algoritmayla bir sorun mu var?
**İki açıklama ve neyi öngördükleri:**
- **Kanal düzeyinde kısıtlama** (ceza, politika, "yapay/özgün olmayan içerik" damgası): yeni videonun gösterimi konudan bağımsız düşük kalır; TO ve tutma iyi olsa bile.
- **Havuz** (Sisifos'un getirdiği izleyici söndü, yeni video önce küçük bir kitleye gösteriliyor): gösterim konunun kendi talebine bağlıdır; Türk izleyicinin aradığı bir konu havuzun dışına taşar.
**Ölçüt (Narkissos 48. saat, 26 Kasım):** "narsisizm" kanalın şimdiye kadarki en geniş arama kapısı.
- Gösterim **≥ 8 B** ya da 2. gün tek günde ≥ 5 B → havuz açıklaması güçlenir, kanal cezası zayıflar.
- Gösterim **< 3 B** ve TO ≥ %2, 0:30 ≥ %65 → beşinci kez aynı tablo; o zaman kanal düzeyine bakılır: Studio → Kanal Analytics → Erişim (son 90 gün gösterim eğrisi ve kaynakları), Studio'daki kısıtlama/politika bildirimleri, videolardaki "değiştirilmiş ya da sentetik içerik" ayarı ve aynı tarihte yayımlanan Shorts'ların "izlemeye devam eden" oranı.
- Arası (3–8 B): karar 7. güne kalır.
**Sonuç (26 Kasım, 46. saat; `2026-11-26-narkissos-48saat.md`):** gösterim **2,4 B**, TO %2,8, ortalama izleme %47,6 (kanalın en iyisi); 0:30 eğri gelmediği için bekliyor. Ölçüte göre kanal düzeyine bakılır (beşinci kez aynı tablo). Not: trafik karışımı farklı (önerilen %24,7, kanal sayfası %16, göz atma %41); ceza beklentisini zayıflatıyor ama ölçüt denetimi istiyor.
**Kanal denetimi (26 Kasım gecesi, Studio salt okuma raporu; `2026-11-26-narkissos-48saat.md`):** ceza yok (ihtar, kısıtlama, özgün olmayan içerik uyarısı yok; kitle "çocuklara özel değil"). "Değiştirilmiş içerik" Evet olan (Ran, Mary Stuart, Kafka) ve Hayır olan (Narkissos, Milton) videolar aynı gösterimde: ayar dağıtımı açıklamıyor. Kanalın haftalık gösterimi 1–7 Kas 158,5 B → 64,2 B → 33,7 B → 22–25 Kas 14,5 B (4 gün): her hafta yarıya yakın. **Hüküm: kanal cezası yok; havuz sönüyor.** "Narsisizm" arama kapısı 48 saatte 5 görüntüleme getirdi; önerilen kaynakları narsisizmle ilgisiz genel Türkçe videolar (YouTube videoyu geniş kitlede küçük örneklerle deniyor).
**Shorts notu:** tek bir Shorts'un 400 izlenmesi tek başına sinyal değil; Shorts dağıtımı ilk saatlerde "izlemeye devam eden / kaydıran" oranına bakar. Ölçüt: izlemeye devam eden ≥ %60 ise içerik değil dağıtım, < %50 ise ilk saniyeler sorunlu.
**Shorts sonucu (23 Kasım, kullanıcı):** Elizabeth Shorts'u ("Elizabeth Onu İdam Ettirdi. Taht Kime Kaldı?") izlemeye devam eden **%27**: akışta gösterilen ~1.500 kişinin ~%73'ü kaydırdı, YouTube göstermeyi bıraktı. Ceza değil, ilk saniyeler. Kanalın öteki ölçülen Shorts'u da aynı bantta (Milton %32–38). Ortak yanları: yatay filmden kırpılmış kareler (dikeyde küçük figür, düşük kontrast), üstte başlık bandı, ilk saniyede hareket yok.

## Şerit denemesi (27 Kasım 2026, kullanıcı onayladı; Gılgamış yayından önce yazıldı)
- **Soru:** gösterim neden her videoda 48 saatte 2–3 B'de duruyor? Kanal cezası elendi (26 Kasım denetimi). Kalan iki aday: (1) videolar birbirini beslemiyor (90 günde bitiş ekranı payı %0,1, oynatma listesi %0,4; Narkissos'un önerilen kaynaklarında kendi videomuz yok); (2) kanalın kitle kimliği dağınık (önerilen kaynakları narsisizmle ilgisiz genel videolar; son iki haftada film, Kafka, İngiliz tarihi, mit, Osmanlı art arda).
- **Düzen:** aynı şeritte dört video art arda: Narkissos (24 Kas) → Dorian Gray (28 Kas) → Gılgamış (2 Ara) → Frankenstein (6 Ara); Lale 10 Aralık'a kaydı. Her birinin bitiş ekranında anlatımın adını verdiği video kalır, ikinci öğe şeritteki bir önceki ya da sonraki video olur; Sisifos ve Prometheus'un bitiş ekranları Narkissos'a bağlanır.
- **Tahmin Ş1:** Gılgamış ve Frankenstein 48 saatte **≥ 4 B** gösterim alır (son dört videoda 2,2–2,8 B) ve Gelişmiş mod → Önerilen videolar listesinde şeritteki kendi videolarımızdan en az biri ilk 5'te çıkar.
- **Tahmin Ş2:** kanal genelinde bitiş ekranı payı (son 28 gün) 13 Aralık'ta %0,1'in üstünde, ≥ %0,5.
- **Tutmazsa:** ana şüpheli yapı değil, kapak ve başlığın ana sayfadaki rekabeti (marka analizi, `2026-11-27-marka-analizi-prompt.md`). Lale (şerit dışı, 10 Ara) karşılaştırma için kullanılır.

## Dikey Shorts deneyi (Narkissos; 23 Kasım yazıldı, yayından önce)
- **Ne değişti:** yatay filmden kırpma yerine plan başına dikey mercekle yeniden çizim (figür kadrajı dolduruyor, keskin); ilk karede yazılı ve sesli kişisel soru + telefon camında hareket; üstte künye bandı yok; altyazı ortada, sağ sütun boş; 24,5 sn.
- **Tahmin S1:** izlemeye devam eden **≥ %60** (Elizabeth %27, Milton %32–38). Tutarsa: kırpma biçimi bırakılır, Shorts dikey merceğe geçer. %40–60: biçim yardımcı ama ilk saniye hâlâ zayıf. **< %40:** sorun kadraj değil, kanalın Shorts'taki konusu ya da ilk cümle; Shorts bir süre bırakılır.
- **Ölçüm:** Shorts'un 48. saati (Studio → Shorts → "izlemeye devam eden" ve görüntüleme).
- **Ara okuma (≈20. saat, 25 Kasım, kullanıcının ekran görüntüleri):** izlemeye devam eden **%43,2** (kaydıran %56,8); görüntüleme ≈ 1,35 B, eğri ~4. saatte düzleşti (YouTube ilk deneme grubundan sonra göstermeyi bıraktı); kaynak %95,8 Shorts akışı; izlenme süresinin %97,3'ü abone olmayanlardan. **S1 bandı %40–60: biçim yardımcı oldu (Elizabeth %27, Milton %32–38'den +5–16 puan), ilk saniye hâlâ zayıf.** 48. saat değeri gelince kesinleşir.
  - **2. gün (Studio salt okuma raporu, 26 Kasım gecesi):** izlemeye devam eden %43,2, 1.331 görüntüleme, ortalama 0:13 (değişmedi). S1: **kısmen** (%40–60). Aynı tabloda: Sisifos şart Shorts'u (26 Kas) %35,9 · 1.228; Elizabeth %28,3; Kafka %33,7; İkaros %19,1. Narkissos şart Shorts'u (25 Kas) son 15 içerik listesinde görünmüyor.
  - Sonuç olarak yapılan: yayımlanmamış Narkissos şart Shorts'unun ilk 3,5 sn'si sıkılaştırıldı ("Kâhinin cevabı tek bir şarttır:" girişi atıldı; ses "Oğlum uzun yaşayacak mı?" → "Kendini tanımazsa." ile açılıyor, şart 4,1 sn yerine 3,2 sn'de bitiyor ve ilk duyulan söz içeriksiz bir giriş değil, ölüm-kalım sorusu). S2 bu sürümle ölçülür.
  - Not: soru Shorts'u planlanan 26 Kasım yerine uzun videoyla aynı gün yayına girmiş görünüyor (20. saat verisi 25 Kasım öğleden sonra). Narkissos uzun videosunun 48. saat okumasında Shorts'tan gelen izleyici ayrı tutulmalı (Studio → trafik kaynağı "Shorts" satırı).

## Şart Shorts'ları (23 Kasım yazıldı, yayından önce; `shorts-sart/`)
- **Ne değişti:** ilk cümle kişisel soru değil, mitin içindeki tek cümlelik şart (yazılı ilk karede, sesli ≤ 1,5 sn'de); görüntüde şartı çiğnemek üzere olan figür; şart ile çiğnendiği an arası ≤ 15 sn; son kare ilk kareye döner.
- **Tahmin S2 (açılış karşılaştırması):** Narkissos şart Shorts'unda (26 Kasım 20:00; 25 Kasım'da 30 Kasım'dan öne alındı) izlemeye devam eden, aynı mitin soru Shorts'undan (%43,2, 20. saat) **en az 10 puan yüksek**, yani ≥ %53. İkisi de aynı çizim hattı ve aynı sahneler; fark yalnız açılış. Tutmazsa: "şart" kalıbı kanal için ayırt edici değil, 703 binlik İkarus örneği kanalın değil konunun ya da hesabın başarısı.
- **Tahmin S3:** Gılgamış şart Shorts'unda (4 Aralık) izlemeye devam eden **≥ %60** ve görüntüleme Narkissos şart Shorts'unun 48. saatinden yüksek (Gılgamış adı Türkçe aramada daha çok tanınıyor: `talep.py` öneri 14, Narkissos 9).
- **Ölçüm:** her Shorts'un 48. saati (Studio → Shorts → "izlemeye devam eden" ve görüntüleme).
- **Narkissos şart Shorts'u (eski açılışlı 23 Kasım dosyası) yanlışlıkla 25 Kasım'da yayına girdi:** 5. saatte **4 görüntüleme** (kullanıcı). Soru Shorts'u aynı yaşta yüzlerdeydi; bu, akışın ilk deneme grubuna bile girmemek demek. Olası nedenler (sınanacak, kesin değil): aynı filmden, aynı sahnelerle (yüz ve yansıma) bir gün arayla ikinci Shorts, tekrarlayan içerik gibi bastırılmış olabilir; ya da ilk gösterim gecikmeli gelir (Shorts'ta 24–48 saat sonra açılan dalga görülür). Silinmez, 48. saatte yeniden bakılır. **Ders adayı:** aynı filmden iki Shorts arasında en az bir hafta ve farklı sahneler.
- **Tahmin S4 (günlük seri, 26–30 Kasım, 25 Kasım yazıldı):** beş Shorts'tan en az birinde 20. saatte izlemeye devam eden ≥ %55. En yükseği şart ilk sözcükte açılanlardan biri olur (Prometheus ya da İkaros), çünkü soru Shorts'unda kayıp ilk saniyedeydi. Tutmazsa sorun açılış cümlesinde değil, ilk karede ya da Shorts'ta kanalın konusunda aranır.

## Sonuçlar
(48. saat ve 7. gün verisi geldikçe doldurulur. Üç tahminden ikisi tutmazsa araç ve kurallar gözden geçirilir.)
- **Mary Stuart (45. saat, 22 Kasım):** M1 ve M3 tuttu, M2 tutmadı. Tempo aracının M işareti inceltilir: "göre" sözcüğü değil, olaydan kopuk açıklama kaybettiriyor (1:12–1:36 arma ve meşruiyet: 24 sn'de −11; 17:38–18:03 "Neden kırmızı?" yorumu: −7). Ayrıntı `2026-11-22-mary-stuart-45saat.md`.
- **Mary Stuart (7. gün, 27 Kasım):** M1 sınırda tuttu (5 puan), M2 tutmadı, M3 tuttu. Hüküm değişmedi. Kapak testi berabere (%57/%42). 3,0 B gösterim, dalga yok.
