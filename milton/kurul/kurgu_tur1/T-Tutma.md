# T-Tutma: YouTube izleyici tutma stratejisti (ilk tam kurgu kurulu, tur 1)

Mercek: izleyici nerede kalır, nerede gider? Senaryo ve ses sabit; yalnız görüntü, kurgu ve ekran yazıları.
Kareler güncel hâlden `shot.js` ile alındı (11 Kasım; açılış, cennet, kapı düzeltmeleri dahil). Bütün kareler:
`/tmp/claude-0/-home-user/11d2c568-95b3-5772-9108-19223f852e25/scratchpad/kurul_T-Tutma/` (ilk 60 sn: `t*.png`, `b/`, `c/`; bölüm kartları: `k/`; ≥15 sn'lik planlar (her birinden 5 kare): `u/`; doruklar: `d/`, `e/`; son bölüm: `f/`; kontakt sayfaları `s1–s4.png`, `k1–k2.png`, `u1–u4.png`, `d1.png`, `f1.png`).
Hareket ölçümü: ≥15 sn'lik 28 planda %10/30/50/70/90 kareleri arasında ortalama piksel farkı (240×135 gri). Doku/kumlanma durağan (P016'da fark 0,0), yani ~5 üstü gerçek hareket demek.

## 1. Puan ve karar

**7,6 / 10: RED** (eşik 9,0; iki ölçüt 7'nin altında)

| Ölçüt | Ağırlık | Puan | Gerekçe |
|---|---|---|---|
| İlk 30 sn: kanca ve kapak vaadi | %30 | 8,0 | İlk kare gözyaşlı göz (kapak B), 0,9. sn'de kapak A'nın figürü, 4,0. sn'de "Ben cehennemim." yazısı: vaat 5 saniyede karşılanıyor. Ama 0:20–0:24 neredeyse siyah ekran var ve A03'te figür küçük. |
| 30–60 sn: eşik ve çıkış kapısı | %15 | **6,8** | P006: 15 sn'lik başlık sayfası (40–49. sn arasında kıpırtısız) ve tam bu sırada "din anlatısı değil" uyarısı. Arkasından iki karanlık oda planı geliyor. |
| Bölüm açılışları | %15 | 8,5 | 11 kartın hepsi soru taşıyor, arka planları farklı; 9'unda karttan sonraki ilk 10 sn soruya görüntüyle karşılık veriyor. K05 → K06 zayıf. |
| Gövde temposu ve sarkma | %20 | 7,5 | Hikâye bölümü (0:56–19:34) iyi akıyor. Ama son 6 dakikanın %37'si kâğıt levha (KIT); ilk 10 dakikada bu oran %13. |
| Ödül anları ve geri çağrılar | %10 | 8,0 | A01 → L07 zincir ödülü güçlü. G07'nin "siluetin içi" ilk kez gören biri için düz göl planı gibi okunuyor. E11'in gözyaşı görünmüyor. |
| Kapanış ve bitiş ekranı | %10 | **6,5** | Anlatıcı "ekranda" dediği an (25:19,8) sol kutu boş. 30 sn boş levha var; L10'un yazısı bitiş ekranının üstünde hayalet gibi kalıyor. |

Ağırlıklı ortalama: 7,6.

## 2. Engelleyici bulgular (tutma merceğinden)

1. **P006 (0:35,8–0:50,8) başlık levhası, 15 sn.** Kayıp ilk 10–15 saniyede başlıyor, 0:30 ile 1:00 arası ikinci kapı. Yazılar 36–40. sn'de dizilir; sonra 40–49. sn arasında kare kıpırdamıyor (`t0040/44/48.png`). Anlatım da tam bu sırada konuyu bırakıp çerçeve uyarısı yapıyor. Telefondaki yeni izleyici (%95) burada "asıl video bitti, şimdi ders başlıyor" diye okur. Çerçeve levhası kalmalı (hassasiyet şartı); ama durağan kalmamalı.
2. **L11 (25:15–25:46) bitiş ekranı.** Anlatıcı 25:19,8'de "Prometheus'un hikâyesi **ekranda**" diyor. YouTube bitiş ekranı öğeleri en çok son 20 saniyede, yani ancak 25:26'dan sonra çıkabilir. Bu yüzden o anda sol kutu boş bir çerçeve (`f/t1516.00.png`, `u/t1518.49.png`). Söz ile görüntü çelişiyor ve sondaki 10 sn izleme süresi boşa gidiyor.
3. **0:20,2–0:24,5 neredeyse siyah ekran** (P004'ün başı; `t0020.50`, `b/t0021.00`, `b/t0023.00`, `t0024.00`). Merak sorusundan hemen sonra 4 saniye boyunca yalnız iki ince göz çizgisi ve soluk bir leke görünüyor. Telefonda bu "yükleniyor ya da bitti" gibi algılanır. Kaybın en yoğun olduğu ilk 30 saniyede bu kabul edilmez.

## 3. Sıralı düzeltme listesi

| # | Zaman / plan | Yer (1920×1080) | Sorun (ilk kez gören ne sanıyor?) | Somut görsel çare | Kazanç |
|---|---|---|---|---|---|
| 1 | 0:35,8–0:50,8 · P006 (A05) | Bütün kare; boş alan y 700–880 | "Kitap tanıtımı başladı, hikâye bitti." 9 sn hareketsiz yazı. | (a) Bütün plan boyunca yavaş itme (z 1,00 → 1,08); (b) "bir şairin **kaleminden** çıkmış" (42,7. sn) kelimesinde sayfanın alt yarısında (x 760–1160, y 640–860) bir tüy kalem A01'in kanatlı siluetini mürekkeple çizsin, göğsündeki alev en son yansın; (c) "din anlatısı **değil**" (47,3) kelimesinde kâğıt çizgisi hafifçe kayıp alt satır ("bir destanın okuması") girsin. Böylece çerçeve levhası, kapağın figürüyle görsel bir köprü olur. Senaryo değişmez. | +0,5 (0:30–1:00 kaybı) |
| 2 | 0:20,2–0:24,5 · P004 başı | Merkez (960, 470) | 4 sn siyah ekran: "video takıldı." | Tam siyahı ≤0,5 sn'ye indir. Gözler "gözlerini" (21,2) kelimesinde iri ve kâğıt beyazı açılsın (her biri ≥160 px, alevin yansıması), "başlar"da (22,5) geri çekilme başlasın, göl "yanan"da (23,7) tam görünsün. | +0,4 |
| 3 | 25:15,4–25:26 · P142 (L11) | Sol kutu x 52–310 / 640 ölçeğinde ≈ x 160–930, y 560–920 | "Ekranda" denince boş kutu görünüyor. | Sol kutuya kendi Prometheus videomuzun vazo üsluplu karesini (kanalın kendi çizimi) koy; 25:26'dan sonra YouTube öğesi onun üstüne otursun. L10 → L11 geçişinde L10 yazısının kutuların arkasından görünmesini (`f/t1516.00.png`) temiz bir kesmeyle gider. Abone çemberine "abone" (25:36,7) kelimesinde küçük bir ışık nabzı ver. | +0,3 |
| 4 | 0:11,3–0:20,2 · P003 (A03) | Figür (960, 300), ~120 px; telefonda ~27 px | Soru (17,2–18,0) soruluyor ama görüntüde onu "tutan" bir şey yok; figür küçük. | Plan boyunca figüre doğru yavaş itme (figür 18. sn'de kare yüksekliğinin ≥%30'u olsun); "tutan" (17,6) kelimesinde figürün bileğinden cehennem ağzına inen ince, soluk bir zincir çizgisi yansın ve sönsün. Böylece L07'deki "zinciri kendi eliyle vurdu" cevabının tohumu ekilir ve cevap sona saklanır. | +0,3 |
| 5 | 20:24–20:41 · P119–P120 (K05, K06) | K06: sol sütun x 700–900 / 640 ölçeğinde; sağ yarı boş | Bölüm "Bu destanın kahramanı kim?" diye açılıyor; cevap olarak 8,5 sn tire tire sahte metin geliyor ("yarım kalmış taslak"). Kart da levha olduğu için art arda 11,5 sn kâğıt var. | K06'da tire satırlar yerine sayfanın sağ yarısına küçük iki siluet koy: solda ışıkta Oğul'un ışığı, sağda A01 figürü. "Kahraman kim?" sorusu görüntüyle sorulsun. "adil" (yaklaşık 1231) kelimesinde yazı zaten geliyor, o kalsın. | +0,25 |
| 6 | 19:58–20:06 · P117 (K03) | Bütün kare | Ortası çizgili boş levha (`u/t1200.05.png`). "Dileyebilir miydi?" sorusunda ekranda bir şey yok. | "dileyebilir miydi" (1199,7) kelimesinde sol sütuna K02'nin diz çöken iki küçük figürü, sağ sütuna dik duran A01 figürü insin. Yazılar sonra altlarına gelsin. | +0,2 |
| 7 | 2:22,7–2:40,4 · P016 (B09) | Sağ yarı x 1000–1800 boş | 17,7 sn kıpırtısız sayfa (fark 0,0); sağ yarı bomboş. | "tiyatro oyununun" (149,6) kelimesinde sağ yarıda sahne perdesi çizgisi ve sahnede tek küçük siluet belirsin; "güneşe" (156,1) kelimesinde sayfadaki güneş ile siluet arasına ışın çizgisi çekilsin. Bu, G03'ün vaadini (oraya geleceğiz) görselle verir. | +0,2 |
| 8 | 24:40–24:51 · P140 (L09) | Figür x ~750–990, gerisi siyah | Kapanıştan önce 11 sn karanlık ve küçük figür (`u/t1482.63`, `t1491.58`). | Işığın yükselmesini "göksel **ışık**" (1487,9) kelimesine çek (şu an ~1497'de); itme figüre doğru olsun, figür kareyi ≥%45 doldursun. | +0,2 |
| 9 | 8:23,7–8:47,4 · P051 (E11) | Profil yüzü ≈ (900, 520) | "Gözlerinden yaşlar boşanır" (521,7–523,1) dendiğinde gözyaşı ~15 px'lik beyaz bir çizik; telefonda görünmüyor. L04 (23:06) bu ana geri çağrı yapıyor, ödül zinciri kopuyor. | "yaşlar" kelimesinde yüze yaklaş (profil kareyi ≥%40 doldursun); A01/L03 dilinde kâğıt beyazı, iri tek damla çiz. L04'te de aynı damla görünsün. | +0,2 |
| 10 | 12:04–12:16 · P072 (G07) | Bütün kare (`d/t0733.90`) | Siluetin içine girildiğinde kare, A04/D10'daki göl planıyla aynı. İlk kez gören "başa döndük" sanıyor, "içindeki göl" fikrini okumuyor. | Gölü siluetin kenar çizgisi içinde göster: kanatların ve başın dış çizgisi karenin kenarında ince bir kâğıt maskesi olarak kalsın (ya da kenarda alevli bir göğüs kafesi çizgisi). İtme bitince 0,5 sn tutup "Ben cehennemim" yazsın. | +0,2 |
| 11 | 22:24–22:37 · P130 (K16) | İki pano üst yarıda; alt yarı boş | 13 sn hareketsiz (fark 0,0–0,2), sonra soru geliyor. | "kalabalığı peşine takan" (1348,2) kelimesinde sol panodaki önder kolunu kaldırsın, kalabalık bir adım öne kaysın; "tek başına duran" (1350,9) kelimesinde sağ panodaki figüre ışık. "tutsağısın" (1357,4) kelimesinde sol önderin bileğine zincir halkası. | +0,15 |
| 12 | 4:12,7–4:29 · P026 (C09) | Profil (960, 640) | 16 sn kıpırtısız; yalnız kelimeler beliriyor. | "kendini küçük düşürülmüş" kelimelerinde yarım yüzün ışık tarafı biraz kararsın (ışık/gölge çizgisi x 960'tan 900'e kaysın); bu "iki cevap yan yana yürüyecek" fikrini hareketle verir. | +0,1 |
| 13 | 18:19–18:38 · P109 (J07) | Figür x 830–1000, y 300–760 (`u3`) | Filmin dönüşüm dorukunda figür karenin üçte biri kadar, çizgili bir sütuna dönüyor; telefonda olay okunmuyor. | Dönüşüm boyunca figüre itme (baş kareyi ≥%50 doldursun); "yüzünün sivrildiğini" kelimesinde yüz yakın plan, "yüzüstü" kelimesinde geniş plana kesme. | +0,15 |
| 14 | 1:02,5–1:08 · P009 (B02 başı) | Sağ %60 (x 760–1920) tam siyah (`u/t0064.47`) | Bölüm kartından sonraki ilk 6 sn'de karenin çoğu boş; plandaki "pencere, ay" yok. | Pencereye ay ekle; "zihninde dizeler" (66,5) kelimesinde dize çizgileri hemen başlasın (şu an ~68'de). | +0,1 |
| 15 | Son 6 dk (19:34–25:46) genel | KIT levhaları: K03, K06, K08, K14, K16, L05, L06, L08b, L10, L11 = 137 sn (%37) | Hikâye 19:34'te bitiyor; deneme bölümü kâğıt ve yazı ağırlıklı. Uzun videoda tutma eğrisi en çok burada düşer. | En az üç levhayı sahneye çevir: K08 (Şeytan sözleri) A01, E07 ve E03 küçük karelerinin yanına gelsin; K14 K01'in ova karesi üstünde dursun; L10'un iki sorusunun altına Cabanel gözü ve Nifates silueti küçük resim olarak girsin. | +0,2 |

Toplam beklenen kazanç: yaklaşık +3,4 puan. Puan tavanı 10 olduğu için gerçekçi hedef 9,0–9,3; ilk dört madde tek başına 8,8'e taşır.

## Görev ayrıntıları

### İlk 60 saniye (5 sn'lik dilimler)
- **0–5:** İlk kare (otomatik oynatma önizlemesi) gözyaşlı Cabanel gözü; kapak B'yi doğrudan karşılıyor. 0,9. sn'de A01 figürü güneşin önünde, göğsünde alevle kapak A'ya bire bir uyuyor. "Ben cehennemim." yazısı 4,0. sn'de geliyor. **Kalma nedeni:** iki kapağın vaadi de 1 saniyede karşılanıyor. Sessiz otomatik oynatmada (altyazı açık) göz ve figür güçlü. **Risk:** kapakta alev turuncu, gözyaşı mavi; videoda tek renk. Küçük bir beklenti farkı, kabul edilebilir.
- **5–10:** Aynı kadrajda ışıklı başmelek (A02). Siyahtan beyaza eşleme kesmesi güçlü bir "önce/sonra" vaadi veriyor.
- **10–15:** 10,0–11,28 arasında göz geri çağrısı var; anlatım bu sırada sessiz. Kapak B ile gelen izleyici için iyi bir hatırlatma; ötekiler için hafif bir bilmece, zararsız. A03 mağara geniş planı başlıyor; figür küçük (madde 4).
- **15–20:** "Onu orada tutan ne?" yazısı 17,2'de geliyor, iyi. Görüntü soruyu desteklemiyor: tutan bir şey görünmüyor (madde 4).
- **20–25:** Siyah ekran ve ince göz çizgileri. **Filmin ilk dakikasındaki en büyük çıkış riski** (madde 2).
- **25–35:** Göl üslup karesi ve "GÖRÜNÜR KARANLIK" yazısı; zincir yakın planı (33,2). Güçlü ve doku zengin.
- **35–50:** Başlık sayfası levhası (madde 1). Çıkış kapısı.
- **50–56:** Kör şairin karanlık odası; mum. "hiçbir şey göremiyordu" bir kanca, kalmayı destekliyor.
- **56–60:** "KÖR ŞAİR" kartı ve sorusu. İyi bir menteşe.

**Şarlken (%79) ile karşılaştırma:** ilk 20 saniye onunla yarışabilir. 20–25 ve 35–50 arasındaki iki boşluk düzeltilmezse 0:30'da %65–70 bandında kalır.

### Bölüm kartları (11 kart + kartsız 2 bölüm)
Kart süreleri: B01 5,6 · C01 4,5 · D01 8,7 · E01 4,5 · F01 7,6 · G01 5,1 · H01 4,4 · I01 3,4 · J01 4,3 · K05 3,0 · L01 2,6 sn.
- Hepsi başlık + soru biçiminde. Arka planlar kendi setlerinden geldiği için tekdüze değil (mum, bulut, mızrak safları, göl, kapı, güneş, bahçe, gece suyu, boş taht, kâğıt, siyah çerçeve).
- Karttan sonraki ilk 10 sn soruyu görüntüyle karşılayanlar: C01 (başmelek), D01 (Abdiel ile Şeytan karşı karşıya), F01 (iki bekçi), G01 (yakın siluet ve güneş), H01 (duvardan sıçrayış, karabatak), I01 (dünya çevresinde gece sayacı), J01 (boş taht → tahtta beliriş), L01 (Cabanel çerçevesi). Zayıf olanlar: B01 (6 sn karanlık, madde 14) ve **K05** (sahte metin, madde 5). E01'de soru "ilk ne söyler?" ve cevap 13. saniyede yazıyla geliyor, yeterli.
- D01 kartının sorusu yok (yalnız "DOKUZ GÜN"). Anlatım soruyu zaten soruyor; tutarlılık için kartta da kısa bir soru satırı olsun.
- K01 "Bütün dünya önlerindeydi" kartsız; ova planı kendi başına açılış gibi duruyor, sorun değil.

### En riskli 10 an (zaman sırasıyla)
1. **0:20–0:24** siyah ekran (madde 2).
2. **0:36–0:50** başlık levhası (madde 1).
3. **1:02–1:08** karanlık oda (madde 14).
4. **2:22–2:40** taslak sayfası (madde 7).
5. **4:12–4:29** C09 (madde 12).
6. **19:58–20:06** boş K03 levhası (madde 6).
7. **20:21–20:32** K05 + sahte metin (madde 5).
8. **22:24–22:37** K16 (madde 11).
9. **24:40–24:51** karanlık L09 (madde 8).
10. **25:15–25:46** bitiş ekranı (madde 3).

Aynı setin ≥40 sn sürdüğü bloklar (CEN 92 sn, SAV 88, KIY 94, ADN 83, MEC 67): hepsinde kadraj ve eylem değişiyor, risk değil. Nifates bloğu (10:49–14:09) filmin "önemli an"ı olmaya aday.

### Ödül anları
- **A01 → L07 (23:46–24:11): güçlü.** Zincirler 24:02'den itibaren figürü sarıyor; "gururu" yazısı A01'in yazısıyla aynı yerde. Gerçek bir "bekledin, değdi" anı.
- **G07 (12:04):** yazı tekrarı doğru yerde, ama göl karesi "içinde" okunmuyor (madde 10).
- **J07 (18:19):** dönüşüm fikri iyi; ölçek küçük (madde 13).
- **L03 (22:55–23:06):** gözyaşı damlası 23:05 civarında beliriyor; kapak B'nin ödülü, doğru yerde. Damlanın beliriş anı "dolu" kelimesine denk geliyorsa korunsun.
- **L09:** madde 8.

### Shorts adayları (koşullar sağlanıyor)
1. **"Ben cehennemim" itirafı:** EDL ile G02b + G06–G08: 11:12,6–11:20,0 + 11:52,4–12:26,2 (≈41 sn).
   - İlk cümle "Ve şimdi, Milton'ın yıllar önce, gözleri henüz görürken yazdığı o ilk dizeler." İlk kare genç Milton (çerçeve var).
   - G08 "cennet gibi kalıyor" ile biter; G14'e varmaz.
2. **"Cehennemde kral":** E05–E08: 7:22,1–8:01,6, 1 sn müzik kuyruğuyla ≈40 sn.
   - İlk cümle "Sonra gölden kalkar. Milton'a göre…" İlk kareye üstte "Milton · Kayıp Cennet, I. kitap" künyesi konmalı; açılıştaki "Sonra" kelimesi Shorts için zayıf.
   - Kanalın en tanınan dizesiyle biter.
3. **Lewis'in küçülme merdiveni:** K10–K13'ün ilk yarısı: 21:00,4–21:46,0 (≈45,6 sn).
   - İlk cümle "C. S. Lewis, Kayıp Cennet'e Önsöz adlı kitabında…" (güçlü çerçeve). Merdiven animasyonu Shorts dikey kadrajına uygun.
   - "…bir meleği yazıyor" sorusuyla, ucu açık biter.
   - (Yedek: L02–L05 Cabanel gözyaşı, 22:47–23:32, 45 sn. İlk cümle bir tabloyu anlatıyor, Milton adı ancak L04'te geçiyor; ilk cümle koşulunu karşılamadığı için yedek.)

### Son 90 saniye
- L08 (24:11–24:34), L08b, L09, L10 (25:02,8–25:15,4; yorum çağrısı) ve L11.
- L10'un iki sorusu düz kâğıt üstünde 12,7 sn duruyor; yorum çağrısı için yeterli, ama yukarıdaki küçük resim önerisi (madde 15) hafızayı tetikler.
- Bitiş ekranı 30,5 sn; ilk 10,5 sn'de YouTube öğesi konamaz (madde 3).
- 30 sn'lik sabit kare, 25:46'lık filmde ortalama izleme yüzdesini en çok ~1 puan düşürür. Asıl zarar oranda değil, "ekranda" sözünün boşa düşmesinde.
- Bitiş ekranını 20 sn'ye indirmek senaryo değişikliği gerektirir (L11 anlatımı 22 sn), kapsam dışı. Çare: ilk 10 sn'yi kendi Prometheus görselimizle doldurmak.
- Abone çağrısı yalnız bitiş ekranında. CLAUDE.md "doruk ~son dakika" diyor; L07 doruğu (24:00) için anlatım sabit, görsel bir çağrı da önermiyorum (doruğu böler).

### Yayın paketi (`youtube.md`)
- **Açıklamanın ilk satırı** uyarıyla başlıyor ("Bu video bir edebiyat okumasıdır…"). Arama ve önerilende görünen ilk ~120 karakter kanca taşımıyor. Öneri: ilk satır "“Hangi yana kaçsam cehennem. Ben cehennemim.” Bunu söyleyen, bir zamanlar cennetin en parlak meleğiydi." olsun, uyarı ikinci paragrafa insin. Hassasiyet üyesi uyarının ilk satırda kalmasını şart koştuysa bu öneri onun vetosuna tabidir; başkan çözsün.
- **Bölüm adları:** çoğu iyi ("Ben cehennemim", "Kör şair", "Güneşe itiraf", "Yılanın içinde", "Bir damla yaş"). Zayıf olanlar:
  - "Bütün dünya önlerindeydi": uzun ve merak uyandırmıyor. Öneri: "Âdem bağışlandı, ya Şeytan?"
  - "Alkış": tek kelimesi bağlamsız. Öneri: "Alkış yerine tıslama".
  - "Dokuz gün": iyi ama "Cennette ilk kılıç" daha çok çeker.

  Bölüm adları ilerleme çubuğunda göründüğü için atlamayı değil merakı beslesin.
- Başlık adayı 1 ("Şeytan Cehennemden Neden Kaçamadı?") açılıştaki "Onu orada tutan ne?" sorusuyla bire bir eşleşiyor. Tutma açısından en iyisi o.

## 4. İyi olan ve korunması gereken
1. 0. kare göz + 0,9. sn A01 + 4. sn "Ben cehennemim." yazısı: iki kapağın vaadi de 5 sn içinde karşılanıyor.
2. A01 → G07 → L07 üçlü geri çağrısı ve L07'deki kendi zinciri: filmin ödülü.
3. Soru taşıyan bölüm kartları: soru anlatıcının sesiyle aynı anda ekranda; arka planlar çeşitli.
4. Siyah-beyaz eşleme kesmeleri (A01/A02, C12/K16 panoları): telefonda bile okunan güçlü siluetler.
5. Hikâye gövdesi (0:56–19:34): aynı sette bile eylem ve kadraj sürekli değişiyor; ≥15 sn'lik planların çoğunda gerçek hareket var.

## 5. Tahmin
- **0:30'da kalan: %64–71.** Kapak vaadi hızlı karşılanıyor (Sisifos'taki "kapak ile açılış farklı" dersi uygulanmış). Ama 0:20'deki siyah boşluk ve küçük A03 figürü yüzünden Şarlken'in %79'una yetişmesi zor. Madde 2 ve 4 yapılırsa üst sınır %74.
- **Ortalama izleme: %25–31 (6:30–8:00).** Prometheus 24 dk'da %28,1 tuttu. Hikâye gövdesi Prometheus kadar güçlü, ama 19:34'ten sonraki deneme bölümü levha ağırlıklı ve 0:35–0:50 eşiği ilk dakikadaki düşüşü (%70 → %55) büyütebilir. Madde 1, 5, 6 ve 15 yapılırsa %29–33.

## 6. En emin olmadığım nokta
- 10,0–11,28'deki sessiz göz geri çağrısı, kapak B ile gelmeyen izleyicide bağlamsız bir kesme gibi duruyor. Bunun merak mı, kafa karışıklığı mı yarattığını ancak A/B tutma eğrisi gösterir. Göz planı yeniden çizildiği için ayrıntısını değil yerini değerlendirdim; yeri bence doğru.
- P006'nın gerçek kayıp etkisini de kestiremiyorum. Sisifos ve Prometheus'ta benzer bir "çerçeve levhası" yoktu, karşılaştıracak veri yok.
