# Y-Altyazı düzeltme raporu (kurgu tur 1)

Değişen dosyalar: yalnız `tools/srt.py` (ve çıktısı `milton.tr.srt`). `senaryo.json` ve `timeline.js` dokunulmadı. Rapordaki 2. bulgu ("Milton'ın" → "Milton'un") başkan kararıyla reddedildi; yazım değişmedi.

## Ne değişti (`tools/srt.py`)

| Madde | Satır | Değişiklik |
|---|---|---|
| 1. Tek harfli kısaltma | 89 (cümle bölme), 26 (`pen_end`) | `[A-ZÇĞİÖŞÜ]\.` ("C.", "S.") cümle sonu sayılmaz; satır/altyazı kırarken de "C." sonrasında kesme cezası 200. |
| 2. Dile duyarlı ceza | 18-70 | `DANGLE` (bir, bu, şu, o, en, çok, daha, bütün, her, hiç, ve, ama, ya da, ki, için, gibi, kadar, ile, de/da, mi/mı/mu/mü) sonda +60; "belki" +50; tamlayan eki (`'ın/'in/'un/'ün`, `-nın/-nin/-nun/-nün`) +50; `ADJNUM` (sıfat/sayı: ilk, son, tek, aynı, iki, üç…) +40; `LEAD` (kadar, gibi, için, ile, mi…) satır/altyazı başında +40; ad-soyad ("John|Milton") +40; noktalama sonrası ödül -25, bağlaç (ve, ama, ki…) ile başlayan parça -25 (ödül toplamı -30'u aşmaz). `wrap2` bunları satır kırmada kullanır; satır sınırı 42, yumuşak 44 (43-44 için karakter başına 15, üstü 100). Üç satır yok. |
| 3. Açık tırnak | 42-53 | Altyazının son 4 sözcüğünde açılıp kapanmayan “ için +100 (satır kırmada son 2 sözcük); ilk sözcüğü kapanış tırnağı (”) olan parça +80. Alıntıyı kapatan 1-2 sözcüklük cümle ("Bağışlanmaya?”") öncekiyle birleşir (satır 94). |
| 4. 7 sn sınırı | 7, 101, 116 | 6,4 sn'yi aşan cümle en az 2 altyazıya bölünür; ":" bölmesi -5 ödül. |
| Altyazı bölme | 102-127 | Parça maliyeti: uzunluk dengesi + `brk_pen` + her parçanın `wrap2` maliyeti + okuma hızı cezası (17 kr/sn). 81-86 karaktere küçük ceza (`CUEMAX`). Bir fazla parça (+40) ya da (tek altyazıda bedel yüksekse) ikiye bölme denenir (satır 120-126). |
| 5. Boşluk | 133-145 | `gap_after`: cümle ortasında 0 ms (bitiş = sonrakinin başı), cümle sonunda 80 ms. |
| 6. Okuma hızı | 145 | Hız aşımını gidermek için erken başlama payı 0,25 → 0,5 sn (yalnız gerektiğinde; 379 altyazının 376'sı yine tam 0 ms). |

## Önce / sonra

| Ölçüt | Önce | Sonra |
|---|---|---|
| Toplam altyazı | 379 | 384 |
| Metin `alt` ile kelime kelime birebir (2605 kelime) | evet | evet |
| 42'yi aşan satır (43-44, yumuşak sınır içinde) | 1 | 6 (hiçbiri 44'ü aşmıyor) |
| Üç satırlı | 0 | 0 |
| < 1 sn | 0 | 0 |
| > 7 sn | 1 (#203) | 0 |
| > 17 kr/sn (> 20) | 3 (0) | 3 (0); en yüksek 18,3 → 18,5 |
| Çakışma | 0 | 0 |
| 80 ms boşluk | 80 | 26 (hepsi cümle sonu) |
| Cümle içi geçişte 0 ms / 80 ms | 0 / 53 | 41 / 0 (kalanlar doğal duraklar, > 0 ms) |
| Satır sonunda ve/bir/bu/en/… | 17 | 0 |
| Altyazı sonunda ve/bir/bu/en/… | 9 | 0 |
| Satır sonunda tamlayan eki | 3 | 1 |
| Altyazı sonunda tamlayan eki | 2 | 0 |
| Sonda açık tırnak (son 4 sözcük, cümle ortası) | 5 | 0 |
| İlk sözcüğü yalnız kapanış tırnağı | 1 | 0 |
| Başlangıç senkronu (kelimeyle 0 ms) | 372 | 379'dan 376'sı; 3 altyazı 100 ms'den erken |

Önce ölçümü aynı betikle aynı sayıma uygulanmış eski `milton.tr.srt` (araç değişmeden yeniden üretilince birebir aynı çıktı verdi) üzerindendir.

## Rapordaki 15 kötü bölme

1. #311/312 "C." | "S. Lewis": düzeldi. Yeni: "Yirminci yüzyılda ise|Narnia'nın yazarı C. S. Lewis," ‖ "Kayıp Cennet'e Önsöz adlı|kitabında tam tersini savundu."
2. #38/39 "Milton'ın" | "gözleri": düzeldi (3 altyazı): "…ilk dizeleri|çok daha önce," ‖ "Milton'ın gözleri henüz görürken," ‖ "bir tiyatro oyununun açılışı…"
3. #50-53: düzeldi. "Bir gün, Milton'ın anlattığına göre," ‖ "Tanrı bütün melekleri toplar|ve Oğul'u onların başına geçirir."; "…sayılacak|ve dönüşü olmayan bir karanlığa düşecektir."
4. #176/177: düzeldi. "Sonra kendine bir soru sorar:|“Sadık kalanlar gibi senin de özgür" (açılış artık sonda değil).
5. #198/199 ve #362/363: düzeldi. "Bu yüzden,|barışı bağışlamaktan o ne kadar uzaksa," ve "Şeytan bunu da biliyordu:|“Barışı bağışlamaktan o ne kadar uzaksa,".
6. #246/247: düzeldi. "“Kim yükselmeye kalkarsa,|yükseldiği kadar alçalmak zorundadır."
7. #251/252: kısmen. "en" ve "Havva'nın|masumiyeti" ayrılığı gitti ("Havva'nın masumiyeti karşısında Şeytan,|kendi kötülüğünden…"); "Sonra destanın belki de en şaşırtıcı|anı gelir:" içinde sıfat|ad (şaşırtıcı|anı) kaldı. Neden: "şaşırtıcı" küçük `ADJNUM` listesinde yok, genel sıfat sezgisi yok.
8. #170/171: düzeldi. "hem de Tanrı için:|“Benden böyle bir karşılığı hak etmemişti."
9. #157/158: düzeldi. "Sonunda uzakta bir şey görür:|cennete altın bir zincirle asılı," ‖ "ayın yanındaki|en küçük yıldız kadar bir dünya."
10. #349/350: düzeldi. "Şeytan destanın bir yerinde ağlıyor;|başka bir yerinde,"
11. #308/309: düzeldi. "Blake'in gerekçesi şuydu:|Milton gerçek bir şairdi" (ardından "ve farkında olmadan…").
12. #12/13: düzeldi (3 altyazı): "Buradaki Şeytan, bir şairin kaleminden|çıkmış bir karakter; biz de bu hikâyeyi" ‖ "bir din anlatısı olarak değil,|bir edebiyat eseri olarak okuyacağız."
13. #27, #124, #139, #143: hepsi düzeldi ("bir şair değil,|bir devrimciydi", "yıkılmış|bir başmelek", "edemediği|bu yolculuğa", "Cehennemin kapısında,|onu çok iyi tanıyan biri").
14. #375/376: düzeldi. "Ateşi insanlar için çalan bir başka asinin,|Prometheus'un hikâyesi ekranda." (44/31) ve "Romantik şair Shelley'ye göre|Prometheus'a benzeyen tek hayalî karakter,".
15. #11: düzeldi. "Bu hikâye bir şiirden:" ‖ "John Milton'ın destanından,|Kayıp Cennet'ten."

Ek: #203 (7,01 sn) ikiye bölündü ("Bu sözleri söylerken yüzü üç kez değişir:" ‖ "öfkeyle, kıskançlıkla, umutsuzlukla."). #82 43 kr'lık satır artık 81 karakterlik altyazıdan ayrı parçada ("“Asıl kölelik budur:|akılsıza ya da kendinden" ‖ …).

## Düzelmeyen ya da yeni çıkan durumlar

- **Satır 43 karakter (6 yer: #27, #50, #54, #151, #226, #380):** yumuşak sınır (44) içinde, bilerek kabul. Daha kötü bir kesme ya da üç satır gerektirirdi.
- **> 17 kr/sn (3 altyazı):** sayı aynı kaldı, ama kümesi değişti: #170 "Sana dostça seslenmiyorum." (17,7), #239 "İyiliğin ne kadar heybetli|olduğunu hisseder" (18,5; yeni, cümle bölme sonucu, komşuları bitişik olduğu için uzatılamıyor), #248 "Bir zamanlar en yüce yer için yarışan ben," (17,7). Eski #198 hız aşımı, başlangıç payı 0,5 sn'ye çıkarılarak giderildi. En yüksek hız 18,3'ten 18,5'e çıktı; sayı artmadı.
- **Erken başlama:** #199 "“Beni cezalandıran da bunu biliyor." konuşmadan 479 ms önce açılıyor (önceki altyazıdan sonraki 0,7 sn'lik sessizlikte; hız için). #248 ve #279 da 130-150 ms önde.
- **Kalan tek kötü altyazı sonu/satır sonu:** #64 "…yüzü|ve yalanlarıyla, cennetin" ve #330 "Hürmüz'ün ve Hindistan'ın|hazinelerinden". "cennetin" gibi apostrofsuz tamlayanlar sezgisel regex'e yakalanmıyor; "Hindistan'ın hazinelerinden" tek satırda 54 karakter olduğundan kırılması kaçınılmaz.
- **#186 (ve benzerleri):** "Bağışlanmaya?”" artık tek başına altyazı değil; ama "Bir an yumuşar: “Pişmanlığa hiç yer|kalmadı mı? Bağışlanmaya?”" tek altyazıya girdi (64 kr).
- **Tırnak cezası kapsamı:** cümle sonunda biten ve tırnağı sonraki cümleye taşan altyazılar (ör. #1 "“Hangi yana kaçsam cehennem.") cezaya girmez; cümle sınırı kesindir.
- Ölçüm betikleri: `.../scratchpad/m/olc.py` (önce/sonra tablosu), `show.py` (örnek gösterimi). Önceki araç ve çıktı yedekleri: `.../scratchpad/srt.onceki.py`, `.../scratchpad/milton.tr.onceki.srt`.
