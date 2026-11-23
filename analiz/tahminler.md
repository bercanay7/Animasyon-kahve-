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

## Sonuçlar
(48. saat ve 7. gün verisi geldikçe doldurulur. Üç tahminden ikisi tutmazsa araç ve kurallar gözden geçirilir.)
- **Mary Stuart (45. saat, 22 Kasım):** M1 ve M3 tuttu, M2 tutmadı. Tempo aracının M işareti inceltilir: "göre" sözcüğü değil, olaydan kopuk açıklama kaybettiriyor (1:12–1:36 arma ve meşruiyet: 24 sn'de −11; 17:38–18:03 "Neden kırmızı?" yorumu: −7). Ayrıntı `2026-11-22-mary-stuart-45saat.md`.
