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
| M1 | Kancadan sonra tek kaynak cümlesi (0:33 "Stefan Zweig'ın anlattığı bu hikâyede biri kalbiyle yaşar, öteki aklıyla") ve kişisel soru ("Sen hangisisin?"), hikâye 0:40'ta. Köprü kaybı Ran'dakinden (9 puan) küçük: 0:31–0:42 arasında ≤5 puan. | 0:31 ve 0:42 değerleri | **Tuttu** (45. saat): 0:31 %70 → 0:42 %67, 3 puan. 0:10 %88, 0:30 %70: kanalın en iyi açılışı. |
| M2 | 4:19–4:44 "Zweig'a göre…" art arda iki yorum cümlesi (D14–D15): bu 25 sn'de yerel düşüş (≥3 puan) ya da Studio "Düşüş" işareti. | eğri + Studio işaretleri | **Tutmadı:** 4:19–4:44 %48 → %51 → %49, düşüş yok; Studio düşüşü 12:35–12:47 (sayvandaki söz). Yazarın somut bir seçim hakkındaki yargısı tutuyor; "göre" kendi başına işaret değil. |
| M3 | İki kuralın çatıştığı yer: ikinci yarıda yeni kişiler (Walsingham 13:21, Babington 14:06) ama anlatım somut (fıçılarda mektup, şifre, kopya). Başkanın tahmini: **somut olay ağır basar**, 13:20–14:40 dik değil. Tutmazsa "yeni ad" ipucu kurala yaklaşır. | 13:20–14:40 dakika başına kayıp / gövde ortalaması | **Tuttu:** 0 puan/dk (gövde 1,5); bölüm boyunca %43 dümdüz. Somut olay yeni adlara ağır bastı. |

## Narkissos (8:52; yayın 24 Kasım 18:00 (kullanıcı, 23 Kasım); 48. saat 26 Kasım, 7. gün 1 Aralık)
| # | Tahmin | Nasıl sınanır | Sonuç |
|---|---|---|---|
| N1 | Köprü yok (kanca sorusu A05'ten sonra ilk cümle hikâye, 0:33). 0:20–0:45'te Ran'daki "düşüp geri çıkma" görülmez; 0:30 (48. saat) ≥ %65. | 0:20–0:45 eğrisi, 0:30 | |
| N2 | Hikâye 6:23'te bitiyor; ardından 2 dakikalık kavram tarihi (1646 öğüt kitabı, 1898 hekim, 1899 psikiyatr, Freud). Filmin büyük gövde düşüşü burada, en dik yer F06–F07 (7:19–7:40, "Freud'a göre… Ona göre…", aracın tek soyut dizisi). 6:23–7:50 dik (≥1,5 × gövde ortalaması). | dakika başına kayıp | |
| N3 | 0:49 Delfi öğüdü (tek bağlam cümlesi, hikâyenin içinde): küçük, ≤3 puan. | 0:45–1:00 | |

## Dorian Gray (8:16; yayın 28 Kasım 18:00 (kullanıcı, 23 Kasım); 48. saat 30 Kasım, 7. gün 5 Aralık)
| # | Tahmin | Nasıl sınanır | Sonuç |
|---|---|---|---|
| D1 | Kanca kurala uygun: kimlik tek cümle (A02 Wilde, 1890) + somut söz (A03 "Bu örtünün altını yıllarca kimse görmedi. Biz göreceğiz."), hikâye 0:24. Köprü kaybı yok; 0:17–0:30 düz ya da yükselen (Kafka'daki söz gibi). 0:30 (48. saat) ≥ %65. | 0:17–0:30, 0:30 | |
| D2 | 1:15 B07 dergi/kitap karşılaştırması: tek soyut cümle; küçük düşüş olabilir, ≤4 puan. | 1:12–1:25 | |
| D3 | **Doğal deney (N2 ile karşılaştırma):** hikâye 6:43'te bitiyor; ardından gelen bölüm somut bir anekdot (1895 mahkemesi, avukat romandan sayfa okur, Wilde hapse girer). Tahmin: 6:45–7:35 dik değil (< 1,5 × gövde ortalaması) ve Narkissos'un 6:23–7:50'sinden yatık. İki video da hikâye bittikten sonra gerçek dünyaya geçiyor; biri somut, biri soyut. | iki videonun aynı bölümü yan yana | |

## Lale Çılgınlığı (10:02; yayın 2 Aralık 2026 18:00 (23 Kasım kararı; önce 11 Aralık); 48. saat = 4 Aralık 18:00, 7. gün = 9 Aralık)
Yazıldı: 22 Kasım 2026, senaryo rev2 (seslendirmeden önce). Zamanlar seslendirmeden sonra cümle kimliğinden eklendi; tahminin içeriği değişmedi.
**Zamanlar:** B01 0:44,6 (ilk 20 sn: 0:44,6–1:04,6); F08 5:18,4 – F11 sonu 5:51,0; G01 5:53,0 (+30 sn: 6:23); I03 8:01,3 – I07 sonu 8:45,9.
**Not (Fable son okuması, 22 Kasım, yayından önce):** üç izleyici kişiliği de ilk düşüşü 0:44–1:33'te gördü ("önce seksen yıl geriye" ile üçüncü zaman sıçraması, adsız elçi ve botanikçi, Latince mektup). L1 bu tahmine karşı çıkan bir okuma; yayından önce görüntüyle karşılandı (B01'in ilk 4,8 sn'sinde 1554 · 1637 · 1730 zaman çizgisi; B04'te çarşıda akçeyle çiçek; B05'te soğan sandığı). L1 bu hâliyle sınanır; tutmazsa düşüş görüntünün değil anlatımın sorunudur (seslendirme sabit kaldı).
| # | Tahmin | Nasıl sınanır | Sonuç |
|---|---|---|---|
| L1 | Kanca uzun (~44 sn: Alkmaar mezadı + İstanbul ikizi + "Lale Devri adını kim koydu?") ve ardından zaman sıçraması ("Önce seksen yıl geriye: 1554"). Sıçrama somut bir sahneyle (elçiye çiçek sunuluyor) açıldığı için köprü kaybı yok: B01'in ilk 20 sn'sinde ≤ 4 puan; 0:30 (48. saat) ≥ %65. | B01 ± 20 sn, 0:30 | |
| L2 | **Doğal deney (Mary Stuart M2 ile aynı soru):** efsanenin çürütülmesi (F08–F11, Goldgar) bir yorum değil, olay olarak kuruldu (arşive dönüş, "bulamıyor", "tutulmayan sözler"). Tahmin: F08–F11 dik değil (< 1,5 × gövde ortalaması). Tutmazsa: izleyici çürütmeyi olay değil açıklama sayıyor. | F08 başı – F11 sonu, dakika başına kayıp / gövde | |
| L3 | **Türk izleyicinin kapısı:** İstanbul bölümü (G01) yeni bir "ikinci hikâye" açar; doruk kişileri kancada ekildiği ve "Lale Devri" okuldan tanıdık olduğu için G01'den sonraki 30 sn'de düşüş yok (≤ 2 puan) ya da yükseliş; "Ad" bölümü (A07'nin merakının cevabı, I03–I07) Studio'da "Önemli an" ya da yerel yükseliş. | G01 + 30 sn; I03–I07 eğri ve Studio işaretleri | |

## Gılgamış (~10:30; yayın 6 Aralık 2026 18:00 (kullanıcı, 23 Kasım); 48. saat = 8 Aralık 18:00, 7. gün = 13 Aralık; 23 Kasım yazıldı, seslendirmeden önce; zamanlar seslendirmeden sonra eklenir, tahmin değişmez)
| # | Tahmin | Nasıl sınanır | Sonuç |
|---|---|---|---|
| G1 | Kanca kurala uygun: kanca sorusundan (A05) sonraki ilk cümle hikâye (B01), kimlik kancanın içinde. Kancanın kendisi iki somut sahne (bitki/yılan, ölü dost) ve bir alıntı (surlar). 0:30 (48. saat) ≥ %65 ve kanca sonu → B03 arasında ≥ 3 puanlık düşüş yok. | 0:30; A05–B03 aralığı | |
| G2 | Yatağın başı (D04–D13: Şamaş'ın sözü, kalbin durması, gelin gibi örtme, "burnundan kurt düşene kadar") filmin en iyi tutan bölümü: ya Studio "Önemli an" bu aralıkta ya da bölümde dakika başına kayıp gövde ortalamasının yarısından az. | Studio işaretleri; dakika başına kayıp | |
| G3 | Hikâye H04'te (surun içi) bitiyor; ardından ~50 sn kuyruk (destanın açılışı, sandık ve tablet, Hattuşa, "yabancı sensin", soru). Kuyruk somut nesne ve olaylarla kurulduğu için dik değil: H05–H10 dakika başına kayıp < 1,5 × gövde ortalaması (Narkissos N2'deki soyut kuyruğun tersi). İkinci yarıda ilk kez adı geçen Urşanabi (E09; rolü kancada ekildi) düşüş getirmez (≤ 3 puan). | H05–H10 ve E09 çevresi | |

---

## Dağıtım sınaması: kanal sorunu mu, havuz mu? (23 Kasım 2026, Narkissos yayından önce yazıldı)
**Soru (kullanıcı, 23 Kasım):** Elizabeth Shorts'u ~400 izlendi (kanalın en düşük Shorts'u); 12 Kasım'dan beri altı uzun video büyük göz atma testi almadı. Algoritmayla bir sorun mu var?
**İki açıklama ve neyi öngördükleri:**
- **Kanal düzeyinde kısıtlama** (ceza, politika, "yapay/özgün olmayan içerik" damgası): yeni videonun gösterimi konudan bağımsız düşük kalır; TO ve tutma iyi olsa bile.
- **Havuz** (Sisifos'un getirdiği izleyici söndü, yeni video önce küçük bir kitleye gösteriliyor): gösterim konunun kendi talebine bağlıdır; Türk izleyicinin aradığı bir konu havuzun dışına taşar.
**Ölçüt (Narkissos 48. saat, 26 Kasım):** "narsisizm" kanalın şimdiye kadarki en geniş arama kapısı.
- Gösterim **≥ 8 B** ya da 2. gün tek günde ≥ 5 B → havuz açıklaması güçlenir, kanal cezası zayıflar.
- Gösterim **< 3 B** ve TO ≥ %2, 0:30 ≥ %65 → beşinci kez aynı tablo; o zaman kanal düzeyine bakılır: Studio → Kanal Analytics → Erişim (son 90 gün gösterim eğrisi ve kaynakları), Studio'daki kısıtlama/politika bildirimleri, videolardaki "değiştirilmiş ya da sentetik içerik" ayarı ve aynı tarihte yayımlanan Shorts'ların "izlemeye devam eden" oranı.
- Arası (3–8 B): karar 7. güne kalır.
**Shorts notu:** tek bir Shorts'un 400 izlenmesi tek başına sinyal değil; Shorts dağıtımı ilk saatlerde "izlemeye devam eden / kaydıran" oranına bakar. Ölçüt: izlemeye devam eden ≥ %60 ise içerik değil dağıtım, < %50 ise ilk saniyeler sorunlu.
**Shorts sonucu (23 Kasım, kullanıcı):** Elizabeth Shorts'u ("Elizabeth Onu İdam Ettirdi. Taht Kime Kaldı?") izlemeye devam eden **%27**: akışta gösterilen ~1.500 kişinin ~%73'ü kaydırdı, YouTube göstermeyi bıraktı. Ceza değil, ilk saniyeler. Kanalın öteki ölçülen Shorts'u da aynı bantta (Milton %32–38). Ortak yanları: yatay filmden kırpılmış kareler (dikeyde küçük figür, düşük kontrast), üstte başlık bandı, ilk saniyede hareket yok.

## Dikey Shorts deneyi (Narkissos; 23 Kasım yazıldı, yayından önce)
- **Ne değişti:** yatay filmden kırpma yerine plan başına dikey mercekle yeniden çizim (figür kadrajı dolduruyor, keskin); ilk karede yazılı ve sesli kişisel soru + telefon camında hareket; üstte künye bandı yok; altyazı ortada, sağ sütun boş; 24,5 sn.
- **Tahmin S1:** izlemeye devam eden **≥ %60** (Elizabeth %27, Milton %32–38). Tutarsa: kırpma biçimi bırakılır, Shorts dikey merceğe geçer. %40–60: biçim yardımcı ama ilk saniye hâlâ zayıf. **< %40:** sorun kadraj değil, kanalın Shorts'taki konusu ya da ilk cümle; Shorts bir süre bırakılır.
- **Ölçüm:** Shorts'un 48. saati (Studio → Shorts → "izlemeye devam eden" ve görüntüleme).

## Sonuçlar
(48. saat ve 7. gün verisi geldikçe doldurulur. Üç tahminden ikisi tutmazsa araç ve kurallar gözden geçirilir.)
- **Mary Stuart (45. saat, 22 Kasım):** M1 ve M3 tuttu, M2 tutmadı. Tempo aracının M işareti inceltilir: "göre" sözcüğü değil, olaydan kopuk açıklama kaybettiriyor (1:12–1:36 arma ve meşruiyet: 24 sn'de −11; 17:38–18:03 "Neden kırmızı?" yorumu: −7). Ayrıntı `2026-11-22-mary-stuart-45saat.md`.
