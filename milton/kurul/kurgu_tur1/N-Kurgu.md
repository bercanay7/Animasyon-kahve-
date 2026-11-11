# N-Kurgu (kurgu ve ritim uzmanı): kurgu turu 1 raporu

Ölçüm betikleri ve ham çıktılar: `/tmp/claude-0/-home-user/11d2c568-95b3-5772-9108-19223f852e25/scratchpad/kurul_N-Kurgu/`
(`dump.js` çekim listesi, `olc.py` + `olc_out.txt` süre/kesme/set/levha/geçiş/sessizlik, `koyu.py` + `koyu_out.txt` koyu oranı, `hareket.py` hareket; güncel özet sayfaları `oz/sayfa01..08.jpg`; ek kareler `k_sheet.jpg`).
Yöntem notu: çekim listesi (145 çekim: 142 plan + P000g, P002g, P051y) canlı `film.html` içinden dökülen `SHOTS` dizisidir, yani güncel kod. Hareket ölçümü yalnız eski `milton_v1.mp4` üzerinden yapıldı (düzeltme öncesi; yaklaşık, "durağan" bulguları kareyle doğruladım).

## 1. Puan ve karar

**7,7 / 10: RED** (eşik 9,0). Hiçbir ölçüt 7'nin altında değil ama "levha payı ve yığılması" 6,8.

| Ölçüt | Ağırlık | Puan |
|---|---|---|
| Kesme yeri ve ses uyumu | %25 | 9,0 |
| Tempo, plan süreleri, doruk ritmi | %20 | 7,8 |
| Görsel çeşitlilik / tekrar yönetimi | %20 | 7,5 |
| Ölçek, açık-koyu dengesi, levha yığılması | %15 | 6,8 |
| Geçiş dili (fade/cut/black) ve sessizlik kullanımı | %10 | 7,5 |
| Anlatım-görüntü eşlemesi | %10 | 8,6 |

Toplam (ağırlıklı) 7,9; ölü süre / boş levha cezasıyla 7,7.

Özet: kesmeler cümle başlarına tertemiz oturuyor (en güçlü yan). Zayıf yanlar: (a) film boyunca kesme ritmi neredeyse metronom, dorukta (özellikle L bölümü) tempo yükselmiyor, yavaşlıyor; (b) 20:19–22:45 arası 143 sn kesintisiz açık renkli levha bloğu, (c) birkaç sahnede aynı kadraj 3–5 plan üst üste, (d) 90 fade'in 42'si zaten sessizlikte yapılabilecekken konuşmanın üstüne biniyor, (e) boş/yazısız levha kareleri.

## 2. Ölçümler

### 2.1 Plan süreleri (145 çekim)
- Ortalama 10,66 sn, **ortanca 9,68 sn**, çeyrekler 6,75 / 9,68 / 14,05 sn.
- Dağılım: <3 sn: 4 · 3–5: 10 · 5–8: 39 · 8–10: 21 · 10–15: 44 · 15–20: 21 · 20–25: 4 · >25: 2.
- En kısa 10: P000g 0,90 · P002g 1,25 · P103 2,30 · P005 2,57 · P131 (bölüm kartı L01 4,01; yedek ölçü: P002 3,79) · P119 4,44 · P018 4,5 · P040 4,52 · P086 4,52 (üç satırlık "kısa" kuyruk yalnız ek çekimler ve bölüm kartları).
- En uzun 15: P142 30,5 (bitiş ekranı) · P137 25,4 · P099 24,6 · P138 22,6 · P140 22,4 · P121 20,8 · P009 19,7 · P115 18,8 · P109 18,7 · P130 18,6 · P126 18,5 · P124 18,0 · P046 18,0 · P016 17,7 · P051 17,7.
- 21 plan 15 sn'den, 6 plan 20 sn'den uzun. Planların %40'ı 10–20 sn: bir "yavaş akış" film.

**Bölüm bölüm** (bölüm = çapa harfi):

| Bölüm | Plan | Süre sn | Ort. plan sn | Kesme/dk |
|---|---|---|---|---|
| A kanca | 10 | 61,5 | 6,2 | 9,8 |
| B şair | 10 | 110,5 | 11,1 | 5,4 |
| C cennet | 12 | 129,7 | 10,8 | 5,6 |
| D savaş | 10 | 95,4 | 9,5 | 6,3 |
| E göl/meclis | 16 | 173,9 | 10,9 | 5,5 |
| F kapı | 9 | 84,0 | 9,3 | 6,4 |
| G Nifates | 18 | 192,8 | 10,7 | 5,6 |
| H Aden | 12 | 112,9 | 9,4 | 6,4 |
| I yılan | 9 | 95,9 | 10,7 | 5,6 |
| J alkış | 11 | 116,6 | 10,6 | 5,7 |
| K iki okuma | 16 | 189,9 | 11,9 | 5,1 |
| L gözyaşı | 12 | 183,0 | 15,3 | 3,9 |

**Tempo eğrisi** (60 sn pencerede kesme): 10 · 5 · 6 · 5 · 6 · 6 · 6 · 6 · 5 · 6 · 7 · 6 · 6 · 5 · 7 · 5 · 5 · 7 · 6 · 5 · 5 · 5 · 6 · **4 · 3 · 2** (ortalama 5,6). Düz çizgi; yalnız açılış hızlı, son üç dakika yavaşlıyor.

**Doruklar** (±30 sn kesme): G07 12:10 → 6 (plan 12,6 sn), J07 18:28 → 6 (plan 18,7 sn), L03 23:00 → 5, L07 24:00 → 4 (plan 25,4 sn). **Doruklarda tempo değişmiyor** (G07, J07) ya da düşüyor (L03, L07). G07'de bir plan içi hareket var (hareket ölçümü 10,3: en yüksek) ama kesme ritmi aynı. L bölümü (23:00–25:45) bilinçli yavaşlama sayılabilir; yine de "gözyaşı" doruğunda (L03 → L07) 14–25 sn'lik üç plan arka arkaya yeni bir görsel olay getirmiyor (bkz. madde 5, 6).

### 2.2 Kesme yeri (144 kesme, P000g hariç)
- **129 / 144 kesme cümle başının ±100 ms'si içinde**, ortanca uzaklık 0 ms (hepsi cümle başına çapalı). 0 kesme kelimenin içine düşüyor (kelime başından >80 ms sonra ve bitişinden >80 ms önce). Yani "yanlış yere kesme" yok.
- Cümle ortasına bilinçli düşen 4 kesme (hepsi ek çekim): P005 33,18 (A04 +12,96 "zincirlerle"), P012 109,90 (B04 +10,88 "yazarı"), P044 436,47 (E04 +11,10 "destan", fade), P051y 521,38 (E11 +17,67). Kelimeye bağlı, uygun.
- **Cümle bittikten sonra >600 ms geç gelen 10 kesme**: hepsi `black` bölüm geçişi (P008, P030, P056, P065, P083, P095, P104, P115, P119, P131) ve hepsi `end:true` (siyaha geçiş sessizlikte oynuyor, kart cümle başında tam). Kasıtlı, doğru. Cümleden >400 ms erken kesme (kelime ya da cümle çapasından): yalnız bu 10 black (−1,4 sn) ve P140 (−1,2 sn).
- **Kesme hep cümle başında olduğu için kesme ritmi cümle yapısını izliyor; plan içi bölünme yok.** 80 sn'den uzun hikâye boşluklarında bile plan içi kamera/olay dışında kesme yok. Bu, tempo olarak "metronom" hissi ve doruk bulgusunun kaynağı.

### 2.3 Tekrar ve çeşitlilik
**Set yoğunluğu** (süre, film payı): KIT 23 plan 291,7 sn %18,9 · ADN 19 / 187,9 / %12,2 · NIF 16 / 174,4 / %11,3 · MEC 12 / 123,1 / %8,0 · CEN 13 / 114,1 / %7,4 · ODA 10 / 110,4 / %7,1 · KIY 9 / 104,8 / %6,8 · OKU 8 / 102,4 / %6,6 · SAV 9 / 89,4 · KAO 7 / 76,2 · GOL 8 / 62,7 · KAP 4 / 43,8 · CIK 2 · CAB 3 · LON 2.
59 set bloğu, ortalama blok 2,46 plan.

**En uzun tek-set blokları:**

| Blok | Plan | Süre | Zaman |
|---|---|---|---|
| KIY P046–P052 | 8 | 94,1 sn | 7:37–9:11 |
| CEN P017–P025 | 9 | 92,3 sn | 2:43–4:15 |
| SAV P030–P038 | 9 | 89,4 sn | 5:01–6:28 |
| ADN P097–P103 | 7 | 81,5 sn | 16:21–17:42 |
| MEC P104–P110 | 7 | 68,9 sn | 17:40–18:50 |
| ADN P090–P095 | 6 | 64,2 sn | 15:08–16:10 |
| OKU P123–P126 | 4 | 54,6 sn | 21:05–21:59 |
| NIF P079–P082 | 4 | 50,4 sn | 13:22–14:11 |

**Aynı kadraj tekrarları** (özet sayfalarına bakarak):
- **Savaş D02–D06 (P031, P033, P034, P035, P036):** iki melek bulutlu kayalarda, aynı kompozisyon beş planda (305–360 sn; P032 yakın ve P035 zırh yakın araya giriyor). Yorgunluk riski ORTA: 55 sn.
- **Kıyı E06–E08 (P046, P047, P048):** aynı kadraj, yalnız alıntı yazısı değişiyor (P047 → P048 "aynı kare", 15,6 sn'lik üç plan). Bilinçli bir "alıntı yığılma" tasarımı ama gerçek ikinci kadraj yok. P049–P052 farklı (omuz, ay kalkanı, profil, ordu), sorun üç plana sığdırılabilir.
- **Nifates G03–G16 (P068, P069, P074, P075, P076, P079, P080, P081, P082):** 9 plan yamaç + güneş + profil/arka figür; kadraj ölçeği değişiyor ama sahne aynı. Toplam NIF 174 sn (%11). Araya KIT levhaları (P071, P073, P077, P078) girip rahatlatıyor; yorgunluk riski ORTA-YÜKSEK özellikle P079–P082 (13:22–14:11, 4 plan 50 sn aralıksız).
- **Aden I04–I05 (P097, P098):** aynı kare (yılan + Şeytan yürüyor, yazı değişiyor), 28,5 sn; **I06–I07 (P099, P100):** aynı yılan karesi 32 sn. Toplam 61 sn'de iki kadraj.
- **Salon J02–J05 (P105, P106, P107, P108):** salon + taht + kalabalık, yaklaşık aynı geniş plan; P107 ≈ P105 ≈ P108'in dış çerçevesi (36 sn) ve P104, P109–P114 aynı salon: MEC J bloğu 69 sn, 7 plan.
- **Aden H11–H12 (P093, P094):** aynı kare (üç melek solda, Şeytan sağda), 31 sn.
- **Göl/Nifates figürü A01 → G02 → G07 → L07** (frontal kanatlı siluet, göğsünde alev): P001, P066, P072, P137 (ayrıca L09 aynası P140): **dört kez, bilinçli geri çağrı**: korunmalı. P066 ile P072 arası (11:07 → 12:10) 63 sn: çok yakın ama G02 kuruluş, G07 doruk; sorun değil.
- **Göl karesi** (A04 → D10 → E01 → E02 → E03 → E05, ayrıca L06 küçük): P004, P039, P040, P041, P042 (yaklaşık 56 sn'de beş plan, 6:28–7:25): E02–E03 (P041, P042) aynı kare, 29,8 sn.
- **Oda** (B02–B06, A06, E04@destan, G02b, K04, L09): 10 plan, 110 sn; aralarında hep başka set olduğundan ve dönüşler anlamlı olduğundan (şair = anlatıcı) **bilinçli**. B bölümünde ODA üst üste P009–P010 (36 sn) ve P013–P014 (21,7 sn); kadraj ölçeği farklı, sorun yok.
- **Nifates + hep aynı "güneş"** film boyunca ≥5 kez: evet (P064–P082, P068'den P082'ye kadar 9 plan).
- **İki siluet / "Asıl başaldıran kim?" levhası** (C12 = P029 → K16 = P130): bilinçli geri çağrı, korunmalı.

**Hangi tekrar bilinçli, hangisi yorgunluk:** bilinçli: A01 → G02 → G07 → L07 → L09 zinciri, C12 → K16, E11 → L04, A04 → D10 → L06 (gölün üç çağrısı). Yorgunluk: D02–D06 beş plan, G09–G16 (P074–P082) dokuz plan, I04–I07 (P097–P100), J02–J05 (P105–P108), E06–E08.

### 2.4 Ölçek, açık-koyu
**Ölçek:** özet sayfalara göre çok kadraj geniş-orta; yakın plan ("göz, el, zincir, kitap, nesne") sayısı yaklaşık 10: P005 zincir, P013 mum + yığın, P032 Abdiel, P035 zırh, P088 karabatak alev, P092 mızrak ucu, P101 el + meyve, P103 yılanın gözü, P133 göz (Cabanel; tek gerçek yüz yakın planı), P012 kapıdaki şair. Yani film büyük ölçüde "siluet / orta-geniş" kadrajlarla ilerliyor; yakın plan oranı %7, ve çoğu (P005, P013, P035) hikâyenin ilk 6 dk'sında. **Hikâyenin 6:30–22:45 aralığı yakın plansız** (P088 karabatak ve P101 el hariç) ve en kritik duygusal an olan Nifates iç konuşması (G03–G12: 12:10 doruğu) yalnızca orta boy siluetlerle kuruluyor. Ölçek çeşitliliği orta (G bölümünde iyi: P066 ufak figür → P068 orta → P072 yakın siluet).

**Koyu oranı** (her plandan bir karede parlaklık <60 piksel %'si; `koyu_out.txt`): ortanca %51,5. 60 sn pencerelerde (süre ağırlıklı): 49 · 63 · 35 · 27 · 38 · 55 · 69 · 53 · 67 · 68 · 55 · **24 · 30 · 23 · 26** · 58 · 56 · 55 · 69 · 64 · **31 · 19 · 19** · 49 · 66 · 6.
- Büyük dalgalar: 2:00–5:00 açık cennet, 5:00–11:00 koyu (göl, kıyı, salon, kapı), 11:00–15:00 açık (Nifates, Aden gündüz), 15:00–20:00 koyu (alkış, yılan, salon), 20:00–22:45 çok açık levhalar, 23:00–25:00 koyu. Bu bloklar 3–6 dk uzunlukta; hepsi içinde ara karşıt kareler var, 60 sn'den uzun saf "hep koyu" blok yok. **Hep açık: P066–P071 (11:01–12:04, 63 sn) ve P122–P130 (20:53–22:45, 111 sn)**.
- **Sert açık ↔ koyu geçişler** (ardışık planlar, koyu oranı farkı ≥45 puan): P005 → P006 (66 → 2; 35,8 sn fade 0,8), P006 → P007 (2 → 58), P015 → P016 (53 → 1; 142,7 fade), P042 → P043 (71 → 7; 425,4 fade), P043 → P044 (7 → 54), P076 → P077 (61 → 4; 771,6 fade), P100 → P101 (19 → 70), **P102 → P103 (37 → 99; 1043,5 cut'ı kasıtlı), P117 → P118 (1 → 100, mum söner)**, P118 → P119 (100 → 1; black), P120 → P121 (2 → 57), P121 → P122 (57 → 1), P130 → P131 (20 → 94), P131 → P132 (94 → 23), P135 → P136 (74 → 14), **P140 → P141 (83 → 1; 1502,8 fade 0,8)**. Bunların çoğu 0,8 sn fade ile yumuşatılmış; en sert olanlar: levha ↔ gravür ikilisi (kâğıt beyazı ↔ siyah) ve P140 → P141 (kapanışta kör şair karanlığından kâğıt beyazına). Kâğıt beyazı (ortalama parlaklık ~190) kartı 24 kez TV'de gözü yorabilir, özellikle P117–P118–P119 (beyaz → siyah → beyaz) 8,5 sn içinde.

### 2.5 Levha (KIT + OKU) planları
- **KIT 23 plan, 291,7 sn (%18,9); OKU 8 plan, 102,4 sn (%6,6); toplam 31 plan, 394,1 sn = %25,5** (filmin dörtte biri levha).
- Art arda levha blokları (≥2 plan ya da ≥15 sn): P006 15 sn (0:35) · P015–P016 23,6 sn (2:16) · P026 16,3 · P077–P078 25,7 sn (12:51) · P111–P112 22,3 sn (18:45) · P117 16,1 sn · **P119–P130 12 plan 143,3 sn (20:19–22:42)** · P135–P136 28,9 sn (23:17) · **P141–P142 43,2 sn (25:02, bitiş)**.
- 3 dk'lık dilimlerde levha payı: 21 · 15 · 6 · 4 · 27 · 1 · **44 · 73** · 28 %. 18:00–24:00 aralığı levhaya bağımlı (iki okuma); 21:00–24:00'te %73.
- **20:21–22:45 "İki okuma" bölümü**: 12 plan, 143 sn, hepsi kâğıt zeminli levha (K05 başlık kartı, K06 sayfa, K07 Blake, K08 alıntılar, K10 kitap, K11–K12 merdiven, K13 Blake mi Lewis mi, K14 yazı, K15/K15b zincir/Cromwell, K16 iki siluet). Bu blok ham ölçümde de en durağan: OKU ortalama hareket 0,68 (gravür setleri 2–5), KIT 0,74. P127 (K14) 6,85 sn'nin ilk ~4 sn'si iki süsten ibaret boş kâğıt (1316,0 ve 1318,0 sn karelerinde yazı yok; yazı 1320,5'te belirmeye başlıyor); P117 (K03) 1203 sn'de yalnız dikey bir çizgi; P016 (B09) 11,5 sn boyunca aynı taslak sayfası.
- **35–50 sn başlık levhası (P006, 15 sn):** sorun değil: tek levha, güçlü bir "kitap" kimliği; ancak ilk dakikada hareketsiz kart olması 10–15 sn kaybı riskinde. P006 15 sn boyunca hareket ölçümü düşük; "1667 başlık sayfası + alev/tarama" hareketi onu hafifletiyor.

### 2.6 Geçişler (145 çekim)
- **fade 90 (%62), cut 43 (%30), black 11 + black-end 1 (P140 1,2 sn), paper 1 (P017 1,0 sn)**. Toplam geçiş süresi: fade 72,9 sn, black 15,2 sn, paper 1 sn (≈ 89 sn, filmin %5,8'i).
- **Bölüm başları tutarlı mı:** evet: B, C?, D, F, G, H, I, J, K(K01 ve K05), L bölüm kartları `black dur 1,4 end:true` (10 adet; E01 kartı P040 `fade`, C01 kartı P018 `fade`, B01 = P008 black, sadece C ve E bölüm kartları farklı). C01 (P018) ve E01 (P040) geçişleri fade 0,8, yani 2 bölüm kartı bu kuralın dışında. **Bölüm başı geçiş desenini bozan iki istisna:** P018 (C01), P040 (E01).
- **Ardışık yumuşak geçiş koşuları (≥2):** P006–P011 (6), **P013–P031 (19 ardışık yumuşak geçiş!, 2:01–5:05)**, P040–P041, P043–P046 (4), P050–P051, P052–P053, P056–P057, P061–P065 (5), P067–P068, P070–P071, P073–P074, P077–P079 (3), **P082–P091 (10; 14:02–15:19)**, P094–P097 (4), P103–P105 (3), P111–P112. B–C bölümleri (2:01–5:05, tam 3 dakika) neredeyse hiç sert kesme içermez: "yumuşak ve uykulu" bir 3 dk. D bölümünde kesme geri geliyor (7/10), E'de karışık, G'de 7 cut, J'de 6 cut, K'de (14 fade + 2 black) ve L'de (10 fade + 2 black) hiç `cut` yok: iki okuma ve son bölüm tümüyle fade.
- **Fade'lerin 42'si (90'ın) kendinden önce ≥1,2 sn sessizlik olan cümle başında**; yani dissolve konuşmanın ilk 0,8 sn'sini kaplıyor (yeni görüntü cümle başladıktan 0,8 sn sonra tam), hâlbuki o sessizlikte geçiş bitebilirdi (`tr.end:true` ile, 10 black'te zaten böyle). Yalnızca 16 fade <0,8 sn'lik boşlukta; yani geçişin cümlenin içine binmesi orada kaçınılmaz.

### 2.7 Anlatım-görüntü eşlemesi (27 plan örneği, her bölümden en az 1)
Baktığım planlar ve kısa hükümler: P001, P004, P010, P014, P019, P024, P031, P037, P046, P051, P058, P062, P064, P068, P072, P078, P085, P093, P099, P102, P105, P109, P114, P121, P126, P133, P137, P140.
- **Doğru eşleşenler** (kare cümleyle aynı şeyi söylüyor): P001 (Nifates silueti = "Ben cehennemim" kancası), P004 (gölde gözler açılır, "dokuz gün düşmüştü"), P010 (iki kız, harfler uçuyor), P019, P037 ("ışıktan savaş arabası": figürsüz ışık), P058 (kadın araya girer), P064, P068 (Ey güneş!: figür güneşe karşı), P072, P078 (döngü: diz çöken/başı dönen), P085, P093 (parlak melekler/sönük Şeytan), P109 (dönüşüm), P121 (Blake kitabı/künye), P126 ("Blake mi, Lewis mi?": taç + taht), P133 (göz yaşı), P137.
- **Spoiler/erken söyleyen:** P098 (I05): yazı kartı "yükseldiği kadar alçalmak zorundadır" yılan karesi, yeni bir görsel bilgi vermiyor (P097 ile aynı). P137 L07: gölün çözülmüş zincirleri + "kendi elinden kendi" hâlâ sahne P001'in aynısı: yeni bilgi yok; cümleyi karşılıyor.
- **Geç kalan / zayıf:** P099 (I06, 24,6 sn): "Havva'nın masumiyeti karşısında Şeytan sersem bir iyilikte donakalır" cümlesi için karede yılanın uzak, küçük Havva figürü: duygu kare olarak okunmuyor, 24,6 sn tek plan; P114 (J11, 17,7 sn): "Şeytan destandan çekilir; onu orada tutan neydi?" karede boş taht salonu: anlam doğru (yokluk) ama 6 sn durağan; P105 (J02, 16,9 sn): "sıradan asker kılığında saraya girer" ilk 4 sn salon boş; P014 (B06, 15,5 sn) "kör"ün anlatımı için pencere: yeterli ama uzun; P024 (C07): konuşma (10 sn) boyunca konuşan yok, saflar var: doğru bir tercih ("dinleyen saflar").
- **Genel:** görüntü cümleden "önce" konuşmuyor; hemen hepsi cümle başında eşleşiyor. Bu kurgu için güvenli ama "görüntü bir adım önde" ya da "kelimeyle kesme" (yalnız 3 yerde) kullanılmıyor.

### 2.8 Sessizlikler (cümleler arası ≥1,2 sn: 69 boşluk)
En uzunlar: G16 → H01 3,40 sn (845,7–849,1) · J11 → K01 3,26 · K16 → L01 3,24 · I10 → J01 3,04 · G14 → G15 2,76 · L08b → L09 2,76 · H12 → I01 2,68 · D10 → E01 2,70 · C12 → D01 2,74 · E15 → F01 2,75 · G09 → G09b 2,62 · A06 → B01 2,58.
- 11 boşlukta (bölüm geçişlerinde) görüntü bir *olay*: black kart (1,4 sn) o sessizlikte oynuyor, kart yazısı beliriyor: iyi.
- Kalan ~58 boşlukta çekim sessizlik boyunca **önceki planın kuyruğunu tutuyor** ve yeni plan cümle başı ile başlıyor (fade'li olanlarda dissolve cümlenin içine biniyor, 42 durum). Ölçüm: planların 30/145'inde son 2 sn'de hareket durmuş. Bu sessizliklerde görüntünün ya bir "nefes" ya da bir "sonraki plana hazırlık" olması gerekirdi. Örnekler: P061–P063 arası, G09 → G09b 2,62 sn (753,1'den önce Şeytan Nifates'te diz çöktükten sonra boş), G14 → G15 2,76 (818,1–820,9), D10 → E01 2,70.

## 3. Engelleyici bulgular
Yayını kesin durduran bir kurgu hatası yok. Ancak şu iki bulgu 9/10'a engel:
1. **İki okuma bloğu (P119–P130, 20:19–22:42, 143 sn)**: 12 plan peş peşe kâğıt-beyazı levha, en düşük hareket, yazısız/boş kare dilimleri (P127, P117), 7+ dk boyunca gravür yok. TV'de ve telefonda "film durdu, slayt başladı" hissi; filmin en kritik gerçek tartışma bölümü olduğu için tutma riski yüksek.
2. **Doruklarda tempo ve görsel olay yok** (G07, J07 ritmi ortalamada, L03–L07 yavaş: 14–25 sn planlar), ve bilinen yorgunluk kümeleri (D02–D06, P074–P082, P097–P100, P105–P108).

## 4. Sıralı düzeltme listesi

1. **K bloğunu (P119–P130) böl ve koyu gravür araya sok.** (21:20–22:45; ölçüm: 143 sn tek tonlu, OKU hareket 0,68.) Çare: (a) P121 (20,8 sn) → 0–9 sn kitap+Blake levhası, 9–20,8 sn Blake'in anlattığı "Şeytan'ın tarafında" için koyu gravür karesi (E11 ya da A04'ten 4–5 sn ödünç: "Milton Şeytan'ı konuşturken özgür"); (b) P124 → P126 arasına (21:50) 6–8 sn'lik **koyu** bir plan: Cromwell/taç yerine Şeytan'ın gölde Beelzebub'a konuştuğu E03 kadrajının yeniden çağrısı (P042 kadrajı; çekim yeni çizim gerektirmez). Böylece açık-koyu-açık nefes verir. Beklenen kazanç: +0,6.
2. **P127 (K14, 1315,0–1321,85) ve P117 (K03, 1198,4–1214,5) boş başlangıç**: P127'nin yazısını 1315,0'a değil cümle başına (~0,3 sn) sabitle; şu an ilk ~5 sn boş. P117 "İnsan aldatıldı" metnini 1203'ten önce göster; 16 sn'nin 5–6 sn'si neredeyse boş. Çare: yazıları kelime zamanlarına (`Wd`) bağla ya da planı ikiye böl. Kazanç +0,3.
3. **Fade'leri sessizliğe taşı (42 yer)**: ≥1,2 sn boşluğu olan fade'lerde `tr.end:true`, dur 0,6–0,8, böylece dissolve sessizlikte biter, cümle yeni karede başlar. Liste: P003, P004, P009, P015, P016, P018 (…) bu boşluklar: A03/A04, B01/B02, B08, B09, B10/C01 … (tam liste `olc_out.txt` "silences" kısmında "cut-in-gap" satırları; fade'li olanlar). Kazanç +0,4 (konuşmanın ilk kelimelerinde iki görüntü üst üste binmesi biter).
4. **Doruklara tempo ver:**
   - G07 (P072, 724,1–736,7): 12,6 sn → "kamera siluetin içine girer" iki parçaya: 0–5 sn frontal siluet (şimdiki), 5–12,6 sn dolu göl (alev) yakın plan; ritim: kısa kesme "Ben cehennemim" kelimesinde (`Wd('G07','cehennemim')`: sert cut).
   - J07 (P109, 1099,4–1118,1): 18,7 sn tek plan; dönüşümün üç aşaması (yüz sivrilir / kollar yapışır / yığılır) için 3 kesme: 0–6 geniş salon, 6–12 yakın (kollar), 12–18,7 yüzüstü yılan; kelimelere bağla ("sivrildiğini", "yapışır", "yığılır").
   - L03 → L07 (1375–1451): P133 (11,2) göz, P134 (10,7), P135 (14,7), P136 (14,2), P137 (25,4) için P137'yi üçe böl: 0–8 sn çözülmüş zincirler, 8–16 sn Abdiel'in sözü ("zincir bekle": P032 yakın plan çağrısı), 16–25,4 sn kendi zinciri (alev). Kazanç +0,5.
5. **P137 (L07, 1426,07–1451,47) 25,4 sn tek plan**: yukarıdaki bölme; ölçüm: L bölümü ort. plan 15,3 sn, kesme/dk 3,9 (filmin en yavaşı). Kazanç dahil.
6. **D02–D06 (P031, P033–P036, 305–363 sn)**: aynı kadraj beş plan. Çare: P033'ü (D04 "kılıç iner") P031'in kadrajından ayır: ters açı (Abdiel'in arkasından Şeytan, alçak kamera), P034'ü yakın ("kılıcı sağ yanını yarar") ve P036'yı (toplar) araya tek yakın plan olarak al; yani 3 farklı kadraj. Kazanç +0,3.
7. **Nifates P074–P082 (746–849 sn)**: dokuz plan yamaç + güneş. Çare: P079 (G13 "mesafe açılır") ve P080 (G14 gölge Aden'e ulaşır) arasına tek bir **koyu karşıt plan** (örn. P076'nın ordu gözleri çağrısı 5 sn, ya da A04 gölü 4 sn) ve P081–P082 (G15–G16) ikisini tek plana indir (28 sn → 14 sn kadraj değişimi + kısa levha). Kazanç +0,3.
8. **Aden/yılan I04–I07 (P097–P100, 974–1036)**: P097/P098 aynı kare 28,5 sn; P099/P100 aynı kare 32 sn. Çare: P098'i yılanın ağzı yakın plan (duman akışı: P098 tarifi) olarak çiz ya da P097 → P098'de kamera yakınlaştır; P099 (24,6 sn) → 0–10 sn uzakta Havva, 10–24,6 sn Havva'nın yüzüne yakın silüet ("sersem bir iyilik"). Kazanç +0,3.
9. **Salon J02–J05 (P105–P108, 1062–1099)**: 3 plan aynı geniş kadraj; P107 (5 sn "bekleyiş", hareket 0,02: ölçüm kare neredeyse donmuş): P107'yi sil ya da P108 ile birleştir ve "bekleyiş"i yakın plan (kalabalığın boyunları) ile ver. Kazanç +0,2.
10. **P140 → P141 sert geçişi (1502,77)**: koyu (83%) → kâğıt beyazı (1%) 0,8 sn fade; kapanış "iki soru" levhasına geçiş film boyunca en sert. Çare: 1,2 sn fade ve P141 zeminini ilk 1,5 sn'de koyu kenarlıklı açılışla ya da P140 sonunda kâğıt rengine kayan ışık (şairin ışığı beyaza dönüşsün). Kazanç +0,2.
11. **Bölüm kartı tutarlılığı**: P018 (C01) ve P040 (E01) `fade 0,8` yerine öteki on karta uygun `black 1,4 end:true`; ya da tersi: kasıtlı iki hafif kart ise bunu KILAVUZ'a yaz. Kazanç +0,1.
12. **B–C bölümü 19 ardışık fade (P013–P031, 2:01–5:05)**: bu 3 dakikada hiç sert kesme yok. Çare: 5–6 yerde `cut` (örn. P020 → P021, P024 → P025, P027 → P028: Abdiel yürüyüşü, ve C08 yıldız sahnesi "ordunun üçte biri" kelimesinde): fade'leri cut'a çevir, yalnız mekân/zaman atlamalarında fade tut. Kazanç +0,2.
13. **P005 (33,18) ve P012, P044 gibi cümle içi ek çekimler**: iyi çalışıyor (3 örnek); aynı yöntemi uzun planlara yay: P051 (23,7 sn: yalnızca P051y ek çekimi var; ordu ve gözyaşı için bir kez daha yakın plan ekle ("üç kez dener" 'üç kez' kelimesinde 3 kısa yakın), P099 (24,6) ve P121 (20,8) ve P137 (25,4). Kazanç +0,3.
14. **Yakın plan oranı %7**: Şeytan'ın yüzü/eli/gözü Nifates iç konuşmasında (G03–G12, 11:26–13:10) hiç yok; P069 ("Hak etmemişti") ve P074 ("Pişmanlığa hiç yer kalmadı mı?") için omuz-üstü ya da siluet yarım yüz yakın plan (P050 profil çağrısı, h≈150) ekle. Yeni çizim gerektirmeyen çözüm: kamera z 1,0 → 1,6 yakınlaşma, figür kadrajın %80'ini doldursun. Kazanç +0,2.
15. **Boş yazılı levha açılışları**: P119 (K05) başlık kartı 3,0 sn tek kart + P118 mum siyahı: beyaz → siyah → beyaz 8,5 sn. Çare: P118'i (mum söner, 6,5 sn) P119'dan ayırma ama P117 → P118 geçişini `cut` (mumun sönmesi = karardıktan sonra kâğıt) yap; fade'siz olsun. Kazanç +0,1.

## 5. İyi olan ve korunması gereken
1. **Kesmelerin cümle başına oturması**: 129/144 kesme ±100 ms'de, 0 kelime-içi kesme; ek çekimler kelimeye bağlı (P005, P012, P044, P051y). Dokunma.
2. **Bölüm kartı siyah geçişi** (`black 1,4 end:true`): sessizlikte oynuyor, tutarlı 10/12; hikâyeye bölüm yapısı (tutma verisi) veriyor.
3. **Bilinçli geri çağrılar**: A01 → G02/G07 → L07 → L09 zinciri ve C12 → K16, E11 → L04 gibi.
4. **Açılış 60 sn**: 10 kesme/dk, 5 farklı set (NIF, CEN, KAO, GOL, KIT/ODA); P000g, P002g ek çekimler ritmi hızlandırıyor.
5. **Ölçek oyunu G bölümünde** (P066 küçük figür, P068 orta, P072 frontal, P082 yine küçük yalnız figür) ve **D10/E01 çemberi**: göl karesine dönüş.

## 6. En emin olmadığım nokta
Plan içi hareketin gerçek hacmi: hareket ölçümü eski `milton_v1.mp4` (düzeltme öncesi) üzerinden 2 fps ile yapıldı ve çekim zamanları küçük kaymalı olabilir. Dolayısıyla "P107 neredeyse donmuş", "P117/P127 ilk 5 sn boş" gibi hükümlerin P127 ve P117'sini taze karelerle doğruladım (k_sheet.jpg), ama P107, P114, P130, P140'ın "durağan" hükmü yalnız eski renderdan. Ayrıca "yorgunluk" ve "bilinçli tekrar" ayrımı bir izleyici testi olmadan öznel: özellikle D02–D06 ve Nifates dizisi kısa kesme eklemeden de "ritüel" olarak okunabilir.
