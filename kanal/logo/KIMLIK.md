# Zaman Kuryesi: kimlik

26 Kasım 2026. Eski avatar (çift altın halka, çizgi film atlı ulak) ve kanal kapağı (Cinzel, yedi ayrı simge) yerine.

## Fikir
**Kum saatinin içinden geçen soru işareti.**
- Kanca üst haznede: geçmiş.
- Nokta boğazdan düşmüş, alt haznede tabana oturmuş: bugün.
- Sloganı tek şekilde söyler: *geçmişe gider, bir soruyla döner.*
- Soru işareti kahramandır (koyu, kontrastlı); kum saati zeminin bir tonu olarak çerçevedir. 24 px'te kalan şey "?" olur, sıradan bir kum saati değil.
- Kanca ve nokta, logo yazısının yazı tipi Fraunces 600'ün kendi "?" glifinden alındı. Cam da kalın-ince çizildi: levha dibinde 32, hazne ortasında 34, boğazda 11 birim. İşaretle yazı aynı elden çıkmış görünür; gravür hissi verir.

## YouTube'a yükleme (Studio → Özelleştirme → Marka)
1. **Resim:** `avatar_altin_800.png`, kırpmadan tamam.
2. **Banner görseli:** `kanal_kapagi_2560.jpg`. Önizlemede telefon, masaüstü ve TV görünümü kontrol edilir; kilit düzen her üçünde tam görünmeli.
3. **Video filigranı:** `filigran_150.png`, görünme zamanı "videonun sonu" değil **"videonun tamamı"**. Filigran sağ alt köşede durur ve altyazı bandına girmez.
4. Eski kapak `kanal/kanal_kapagi.jpg` ve `kanal/banner.html` arşiv olarak kalır.

## Dosyalar (`cikti/`)
| Dosya | Nerede |
|---|---|
| `avatar_altin_800.png` | **YouTube profil resmi** (ana) |
| `avatar_lacivert_800.png` | yedek; koyu akışta kenarı zemine karışır, ana avatar olmaz |
| `kanal_kapagi_2560.jpg` | **YouTube kanal kapağı** (2560×1440; kilit düzen telefonda görünen alanın içinde) |
| `filigran_150.png` | **YouTube marka filigranı** (Studio → Özelleştirme → Marka) |
| `yatay_lacivert.png` / `.svg`, `yatay_fildisi.png` / `.svg`, `yatay_lacivert_saydam.png` | yatay logo: bitiş ekranı, topluluk gönderisi, açıklama görseli |
| `isaret_*.svg` | yalnız işaret, yazısız; her boyda keskin |
| `logo_hareket_1080p.mp4` | 6,5 sn logo hareketi, sesli (−18,8 LUFS, tepe −1,2 dBFS). Kanal fragmanı, topluluk gönderisi, tanıtım. Kullanım sınırı aşağıda |
| `test_kucuk_boy.png`, `hareket_kareleri.jpg`, `surec.jpg` | denetim sayfaları; sürüm karşılaştırması |

Yeniden üretmek için:
- `node kanal/logo/uret.js`: PNG ve SVG'ler. Yazılı SVG için `OPENTYPE=/yol/opentype.js` verilir.
- `python3 kanal/logo/ses.py`, ardından `node kanal/logo/hareket_render.js`: hareket videosu, yaklaşık 40 sn sürer.

## Logo hareketi
- **Akış:** tabandaki nokta (bugün) → kum saati ters döner, nokta üste çıkar (geçmişe gider) → tanelere ayrılıp kancayı kurar → kum boğazdan ince akışla iner, nokta tabanda birikip oturur (bir soruyla döner) → soru 0,5 sn bütün okunur → işaret küçülüp sola kayar, yazı gelir.
- **Ses:** hepsi sentez, `ses.py`. Dönüşte hava hışırtısı, kum tıkırtıları ve akışı, noktanın oturuşunda tahta "tok", yazıyla tek sıcak çan.
- **Kullanım sınırı (kanal verisi):**
  - Videonun başına konmaz: kanca ilk cümlede, hikâye en geç 0:45'te başlar.
  - Hikâyenin ardına ayrı bir blok olarak da eklenmez: hikâye bitince izleyici gider. Bitiş ekranı hikâyenin son anının içinde kalır.
  - Yeri kanal fragmanı, topluluk gönderisi, tanıtım ve ileride bir seri açılışı.

## Renk
| Ad | Hex | Rol |
|---|---|---|
| Altın | `#E2B04F` | avatar zemini; koyu zeminde soru işareti |
| Lacivert | `#101B33` | koyu zemin; altın ve fildişi zeminde soru işareti; yazı |
| Koyu altın | `#9C6F22` | altın zeminde kum saati; açık zeminde slogan |
| Gece | `#46598A` | lacivert zeminde kum saati |
| Fildişi | `#F3EAD7` | açık zemin; koyu zeminde yazı |
| Kum | `#B89A62` | fildişi zeminde kum saati |

Kural: soru işareti her zaman zeminle en yüksek kontrastta; kum saati zeminin bir tonu. Kırmızı yok.

## Yazı
- **Fraunces 600** (OFL): "ZAMAN KURYESİ", büyük harf, harf arası .06em.
- **Cormorant Garamond italik 500** (OFL): slogan, küçük harf.
- Cinzel artık kimlikte kullanılmaz; videoların kendi üslubunda kullanılabilir.

## Kullanım
- Kilit düzen: işaret yüksekliği yazı boyunun 1,75 katı. Yazı ile işaret arası yazı boyunun .36'sı. Slogan başlığın sol kenarında.
- En küçük boy: işaret 24 px (avatar dairesi). Yatay logo 240 px enin altında kullanılmaz; orada yalnız işaret.
- Yapılmaz:
  - işaret döndürülmez, eğilmez;
  - soru işaretine gölge ya da parlama verilmez;
  - kum saatine soru işaretinden güçlü renk verilmez;
  - nokta ile kanca ayrı yerlere taşınmaz (hilal-yıldız riski; nokta her zaman kancanın dikey ekseninde).

## Hassasiyet taraması
Tam boy karelerde ve hareketin her karesinde bakıldı (Fable üç tur, yönetmen her turda karede doğruladı).
- Fable'ın birinci okuması: v1'deki kiremit damla ve yarım daire "kan lekesi" gibi okunabiliyordu. Kırmızı çıkarıldı.
- Fable'ın ikinci okuması: v2'de lacivert zeminde altın yığın ile dik kesik çizgi birlikte "kubbe ve alem" siluetine yaklaşıyordu. Yığın ve çizgi kaldırıldı.
- Kanca ve nokta aynı dikey eksende; hilal-yıldız dizilişi yok. Halka, hale, haç ve selam okunmuyor.
- Kapakta simetrik kanatlı figür yok (eski kapakta vardı).
- Harekette yan yatmış kum saati papyon ya da sonsuzluk gibi okunabilir; listede yok, zararsız. Tane bulutu altın renkte; kan okunmuyor. Kanca kurulurken nokta ekranda olmadığından hilal ve nokta hiçbir karede birlikte durmuyor.

## Nasıl geldik
Karşılaştırma: `cikti/surec.jpg` (eski → ilk taslak → v1 → v2 → v3).
1. Piyasa (Fable): kazanan avatarlar tek kalın şekil, düz zemin, en çok iki renk (Kings and Generals, OverSimplified, CrashCourse, TED-Ed). Eski avatar 24 px'te dizinin en zayıf okunanıydı.
2. Üç ilk taslak (posta damgası, kum saati + soru, ZK monogramı) küçük boyda sınandı; kum saati + soru kazandı.
3. v1: lacivert kum saati, kiremit soru. Fable: soru tablaya biniyor, sap boğaza sıkışıyor, kırmızı damla riski var, işaret ile yazı iki ayrı dil.
4. v2: roller ters çevrildi, soru Fraunces glifi oldu, boşluklar ölçüldü. Fable: kahraman küçük, yığın nokta olarak okunmuyor, kubbe riski var.
5. v3: noktası tabana düşmüş soru işareti, ince uzun ve dışa şişkin kum saati, soru %19 büyüdü. Logo hareketi eklendi.
6. Son tur:
   - Fable'ın bulguları: hareket sırasında işaret yazıya biniyordu, nokta tavanda asılı kalıyordu, ses yoktu, cam ile soru iki ayrı çizim diliydi.
   - Hepsi düzeltildi: hareket yeniden zamanlandı, ses eklendi, cam kalın-ince çizildi.
   - Geri çevrilen bulgu: "slogan 1080p'de 14 px" ölçümü yanlıştı; slogan 54 px.
