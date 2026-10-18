# notlar_figur_lab.md — Figür Laboratuvarı teslim notları

Rol: FİGÜR LABORATUVARI (figür-lab). Kapsam: `stage.py` siluet figürlerinin "kâğıt-kesim / gölge-tiyatrosu" kalitesinde yeniden yazımı.
`stage.py`, `scenes_lib.py` ve diğer ortak dosyalara DOKUNULMADI; yalnız kayıt kancaları (`@ST.figx`) kullanıldı. `git` kullanılmadı.

## 1. Ne yapıldı (özet)
- Eski kaba/"blob" figürler tamamen yenilendi: oranlar ≈7–7,5 baş, 3/4 profil baş (burun, dudak, çene, sakal), şapka/başlık türe özgü,
  kumaş kıvrımları (koyu-açık mercekler + sol kenarda ince ışık), etek kenarında negatif-alan (kâğıt oyuğu) çentikler, dişli (dagged) etek,
  kürk yaka (düzensiz bulut kenarlı), süs bantları (elmas/tocapu/basamaklı sınır), ruff, düğme/zincir/kemer ayrıntıları.
- Işık dili: koyu gövde (`#0C0705`) + her parçanın **kendi sol-üst kenarında sıcak kenar ışığı** (kâğıt katmanı etkisi; yukarıdan aşağı sönümlü). Ayrıca yumuşak iç ışıltı (`glow`).
  Açık sisli zeminde de okunur (koyu siluet + ince sıcak kenar). `face=-1` aynalar (ışık sağa geçer).
- **49 tür** (19 istenen mevcut + 22 yeni + 8 ek): hepsi `@ST.figx`. Tür adları değişmedi; `figure(f, kind, x, y_ayak, h, col, rim, face, alpha, sway, rot, lean, bob)` imzası aynı.
- Hepsi sağa bakar (`face=+1`); ayak (0,0); yukarı −y.

## 2. Dosyalar
| dosya | içerik |
|---|---|
| `figs_kit.py` | geometri (köşe destekli spline `sp`, `limb`, `bar`, `lens`, `place`…), `Fig` (parça listesi: fill/cut/line/solid/glow + kenar ışığı), baş/sakal profilleri, eller, ayakkabı, tüy |
| `figs_parts.py` | şapkalar (≈25), `add_head` (boyun+baş+sakal+saç+şapka), `add_arm`, `add_leg`, `robe_path` (S eğrili/dişli cüppe), kıvrım yelpazesi, kürk şeridi, ruff, etek bandı |
| `figs_lab.py` | sivil türler: noble, merchant, cardinal, scribe, monk, woman, emperor_old, prince, page, seated, kneel, pair_old_prince |
| `figs_war.py` | asker/silahlı/yerli: pikeman, landsknecht, janissary, knight, conquistador, sailor, native (+ `torso`, `pike` yardımcıları) |
| `figs_horse.py` | at ve atlılar: horse, horse_walk, horse_rider, horse_rider_walk, cavalry_charge(+_b), sipahi(+_b) |
| `figs_more.py` | grup-2: child, peasant, fisherman, bearer, friar_writing, scholar_lectern, woman_seated, man_seated_bed, coffin, inca_noble, aztec_warrior, arquebusier, halberdier, crowd_a…f + bonus: torchbearer, standard_bearer, litter |
| `figs_sheet.py` | kontak sayfası/ızgara/benchmark aracı (aşağıda) |

Yükleme zinciri: `stage` → `figs_lab`, `figs_war` → (`figs_horse`, `figs_more`; `sk.optional_import` ile). Bir modül hata verirse uyarı basılır, öteki türler çalışır. Her import sırası sınandı (hatasız).
Yeni tür eklemek: `figs_more.py` içinde `@fx("ad") def f(h, lean): F = Fig(h, lean); ...; return F.build()`.

## 3. Kullanım notları (sahne ajanları için)
- `ST.figure(f, "noble", x, y_ayak, h, col="#0A0604", rim="#C58A44", face=1)`. Hall'daki `col`/`rim` değerleri aynen çalışır; `rim=None` → kenar ışığı yok (iç çizgiler yine türer).
  İç ayrıntı renkleri `col` ve `rim`'den türetilir → sisle karışmış (`mix(col, fog, …)`) renklerle de tutarlı.
- `h` ≈ figürün piksel boyu (şapka/tüy ile ≈ 1.0–1.1h). Mızrak/pike/alebard/flama h'ın 1.3–1.9 katına kadar çıkar: tabloda "tepe" ve "yatay" sütunları `h=1` birimine göre ölçülmüş sınırlardır.
- `lean` (±0.02–0.1): üst gövdeyi y=0 çevresinde kaydırır (kayma = 1,5·lean·h tepede). Kalabalıkta `crowd()`'ın verdiği ±0.02 ince varyasyondur.
- Önbellek: sprite `(tür, round(h), col, rim, lean)` anahtarlı. Statik katmanda ilk kare maliyeti bir kez ödenir.
- Süvari/atlı türlerinde `h` = **zeminden binicinin başlığına** toplam boy (at kulağı ≈0.70h). `horse` ve `horse_walk`'ta `h` = at kulak yüksekliği.
- Animasyon: `cavalry_charge` ↔ `cavalry_charge_b` (ve `sipahi` ↔ `sipahi_b`) 5–7 karede bir dönüşümlü çizilirse dörtnala olur (iki poz); `horse` ↔ `horse_walk` yürüyüş. Dörtnalada toynaklar 0.03–0.07h havadadır: `y_ayak`'ı ≈0.05h aşağı al ya da toz/duman ekle.
- Işıklı öğeler (mum, meşale, fitil): `friar_writing` (mum), `torchbearer` (meşale), `arquebusier` (fitil ucu) sıcak parlamayı spritea pişirir (titremez); titreme için sahne `dyn` içinde ek `kPlus` ışıma çizilebilir.
- Oturan/yatan türlerde mobilya YOK (`seated`: taht arkada sahnede; `woman_seated`: sandalye yok; `man_seated_bed`: yatak çerçevesi yok ama yastık+battaniye dahil; `friar_writing`: masa+tabure+mum dahil).
- `litter`: iki `bearer` ile birlikte: arka taşıyıcı x−0.85h, ön taşıyıcı x+0.85h (aynı y_ayak, face=1); sırık hizaları (y=−0.765h) örtüşür.
- Yerli halk figürleri (`native` Mezoamerika/Nahua, `inca_noble`, `aztec_warrior`): kıyafet/aksesuar doğru (llautu+mascaypacha, tocapu, tilma, chimalli, macuahuitl, quetzal tüy tacı), duruş onurlu; Kuzey Amerika "savaş bonesi" klişesi, vahşi/karikatür öğe YOK.
  Gerçek kişi karikatürü yok: `emperor_old`/`pair_old_prince`'te çene yalnız hafif belirgin (kimlik gizli kalır).

## 4. Tür kataloğu (ölçüler h=1 birimine göre; "yatay" x aralığı, "tepe" en üst nokta)
| ad | grup | yatay (sol…sağ) | tepe | h / ölçek | ayak–hizalama | açıklama |
|---|---|---|---|---|---|---|
| `noble` | 1 | -0.22 … +0.23 | 1.02 | h ≈ ayaktan baret tüyüne (tepe 1.02h) | ayak y=0; ön ayak sağda | Holbein tarzı soylu: dişli (dagged) dizüstü cüppe, kürk klapa, baret+tüy, sivri sakal, zincir; sağ eli belde (akimbo), uzak elde eldiven |
| `merchant` | 1 | -0.20 … +0.22 | 0.96 | h ≈ ayak→şapka (0.94h) | ayak y=0 | Tüccar/banker: ayak bileği boy kürk yakalı cüppe, kemer+kese, elinde defter, yuvarlak bone |
| `cardinal` | 1 | -0.32 … +0.24 | 0.95 | h ≈ ayak→galero (0.95h) | ayak y=0; arka etek sürüntüsü sol −0.32h | Kardinal: geniş kenarlı galero + püsküllü kordonlar, mozzetta, arkaya savrulan uzun etek, göğüste rulo |
| `scribe` | 1 | -0.17 … +0.26 | 0.94 | h ≈ 0.93h | ayak y=0; tüy kalem sağ +0.26h | Katip: baldır boy gömlek+çorap, öne eğik, bilgin kepi, eğik yazı levhası + tüy kalem, hokka |
| `monk` | 1 | -0.22 … +0.22 | 0.95 | h ≈ 0.95h | ayak y=0 | Keşiş: kukuletalı habit, ip kuşak (düğümlü), tespih, başı eğik, elleri kolun içinde |
| `woman` | 1 | -0.28 … +0.26 | 0.93 | h ≈ 0.93h (kadın oranı) | ayak y=0; etek sol −0.28h … sağ +0.26h | Soylu kadın: dar korse + geniş çan etek (arkada sürüntü), uzun peçe, kavuşmuş eller |
| `emperor_old` | 1 | -0.21 … +0.22 | 0.91 | tepe 0.89h (kambur) | ayak y=0; baston sağ +0.21h | Yaşlı imparator: bükülü, kürk yakalı ağır cüppe, bastonlu; yumuşak bone, kısa gri sakal |
| `prince` | 1 | -0.29 … +0.19 | 1.00 | h ≈ ayak→baret tüyü (1.00h) | ayak y=0; kılıç ucu sol −0.29h | Genç soylu/prens: kısa pelerin, kılıç kabzasında el, çorap bacak, şişkin pantolon, ruff, baret+tüy |
| `page` | 1 | -0.12 … +0.19 | 0.97 | h ≈ 0.95h (çocuk oranı, baş büyük) | ayak y=0 | Sayfa (uşak çocuk): kısa tunik, rulo mektup uzatır |
| `seated` | 1 | -0.29 … +0.29 | 1.00 | h = AYAKTA boy eşdeğeri; oturunca tepe 0.78h (asa 1.0h) | ayak y=0; oturak ≈0.27h; sandalye/taht YOK (sahne tahtı arkaya çizer) | Tahtta taçlı imparator: dik oturuş, ermin yaka+benekler, imparatorluk tacı (haç), asa; mantı arkadan yere |
| `kneel` | 1 | -0.39 … +0.28 | 0.76 | h = ayakta boy eşdeğeri; tepe 0.76h | ayak y=0 | Tek diz çökmüş dilekçi/biat eden: başı eğik, eller dizde, cüppe arkaya sürünür |
| `pair_old_prince` | 1 | -0.42 … +0.41 | 1.00 | h = PRENSİN boyu (tepe 1.00h) | ayak y=0; imparator solda/geride, prens sağda; ikisi de sağa bakar | KİLİT FİGÜR (c0/c12): bükülü yaşlı imparator + önde baston; uzanan kolu/eli genç prensin omzunda |
| `pikeman` | 1 | -0.13 … +0.21 | 1.80 | gövde 0.94h, pike ucu 1.80h | ayak y=0; pike yerde x=+0.17h | Piyade (pike): kasket, göğüs zırhı, uyluk levhaları, iki elle dik pike |
| `landsknecht` | 1 | -0.26 … +0.64 | 1.84 | gövde 1.0h, pike ucu 1.84h (diyagonal) | ayak y=0; geniş duruş; pike sağ +0.64h | Landsknecht: tabak şapka + 4 tüy, yırtmaçlı şişkin kol/pantolon, Katzbalger kılıç, önde diyagonal pike |
| `janissary` | 1 | -0.27 … +0.24 | 1.30 | gövde ≈ 1.0h (börk dahil), tüfek 1.3h | ayak y=0; kılıç sol −0.27h | Yeniçeri: börk (sırtta sarkan uç, kaşıklık), kaftan+kuşak, kilij, yerde fitilli tüfek, bıyık |
| `knight` | 1 | -0.21 … +0.23 | 1.08 | tepe 1.08h (tüy dahil) | ayak y=0; kılıç ucu yerde x=+0.175h | Tam zırhlı şövalye: armet+tüy, omuzluk, tassets, diz levhası, iki el kılıç kabzasında |
| `conquistador` | 1 | -0.30 … +0.38 | 1.64 | gövde 1.0h, mızrak+flama 1.64h | ayak y=0; rapier sol −0.30h; flama sağ +0.38h | Fatih: morion, peascod göğüs zırhı, pelerin, rapier, bele dayalı kol, flamalı mızrak |
| `sailor` | 1 | -0.17 … +0.20 | 0.95 | h ≈ 0.95h | yalın ayak y=0 | Denizci: yün bere, bol gömlek, dizaltı pantolon, omuzda halat kangı, kemerde bıçak |
| `native` | 1 | -0.13 … +0.22 | 1.04 | tepe 1.04h | ayak y=0; asa sağ +0.18h | Mezoamerika soylusu (Nahua): omuzda düğümlü tilma (basamaklı sınır), süslü bel bezi, bağlı sandalet, alın bandı+tüy yelpazesi, asa — onurlu, karikatürsüz |
| `arquebusier` | 2 | -0.19 … +0.61 | 1.23 | gövde 1.0h; namlu ucu sağ +0.61h (1.23h) | ayak y=0; fitil ucu parlar (glowdot) | Fitilli tüfekli (arcabucero): sarkık şapka+tüy, bandolier (barut tüpleri), omuzda arkebüz, yanan fitil (ışıma) |
| `halberdier` | 2 | -0.20 … +0.29 | 1.75 | gövde 0.94h; alebard ucu 1.75h | ayak y=0; sap x=+0.185h | Alebardiyer: kasket, göğüs zırhı, iki elle dik alebard (mızrak ucu+balta+kanca), kılıç |
| `horse` | 2 | -0.77 … +0.77 | 1.11 | h = KULAK ucu yüksekliği (yele dahil tepe 1.11h) | toynaklar y=0; kuyruk solda, burun sağda | Tek at, duran (baş kalkık, yeleli, dizgin) |
| `horse_walk` | 2 | -0.77 … +0.77 | 1.11 | aynı | ön yakın bacak havada | Yürüyen at (horse ile dönüşümlü çizilirse yürüme hissi) |
| `horse_rider` | 2 | -0.54 … +0.54 | 1.59 | h = zeminden binici miğferine (at kulağı 0.70h); mızrak ucu 1.59h | toynak y=0 | Zırhlı atlı: kapariş (at örtüsü), armet+tüy, dik mızrak + flama; duran at |
| `horse_rider_walk` | 2 | -0.54 … +0.54 | 1.57 | aynı (mızrak ileri-yukarı eğik) | toynak y=0 | Yürüyen at + zırhlı atlı; Mühlberg/Tiziano tarzı eğik mızrak |
| `cavalry_charge` | 2 | -0.77 … +1.60 | 1.02 | h = zeminden binici miğferine; mızrak ucu sağ +1.60h | dörtnalada toynaklar ≈0.07h havada (y_ayak'ı ≈0.05h aşağı al ya da toz ekle) | Dörtnala süvari hücumu POZ A (uzamış): yatay mızrak + flama, kuyruk/yele geriye |
| `cavalry_charge_b` | 2 | -0.81 … +1.55 | 1.01 | aynı | toynaklar ≈0.03h havada | Dörtnala POZ B (toplanmış): A ile 5–7 karede bir dönüşümlü çiz |
| `sipahi` | 2 | -0.77 … +0.56 | 1.10 | h = zeminden başlığa | dörtnala (A pozu), toynaklar havada | Osmanlı sipahisi: sarık+sorguç, kaftan, sırtta yuvarlak kalkan, havada kilij, süslü at örtüsü |
| `sipahi_b` | 2 | -0.81 … +0.51 | 1.10 | aynı | (B pozu) | Sipahi, toplanmış poz (A ile dönüşümlü) |
| `peasant` | 2 | -0.15 … +0.25 | 1.12 | tepe 1.12h (hasır şapka) | ayak y=0; yaba yerde x=+0.20h | Köylü: geniş kenarlı şapka, bol gömlek, dizlik; yere basan yaba |
| `fisherman` | 2 | -0.12 … +0.61 | 1.20 | tepe 1.20h (olta ucu sağ +0.61h) | yalın ayak y=0 | Balıkçı: yün bere, paçaları sıvalı, sırık olta + ip + balık, sepet |
| `bearer` | 2 | -0.47 … +0.53 | 0.91 | h ≈ 0.91h; sırık −0.47 … +0.53h | ayak y=0; sırık omuz hizası y=−0.765h | Sedye/tahtırevan taşıyıcısı: omuzda uzun sırık (iki ucunda bağ halkası), çömelik yürüyüş |
| `inca_noble` | 2 | -0.14 … +0.22 | 1.14 | tepe 1.14h (asa ucu dahil) | ayak y=0; asa sağ +0.18h | İnka soylusu: llautu bandı + alında saçak (mascaypacha) + iki tüy, büyük kulak diski, unku (tocapu desenli bantlar), yacolla mantı, tören asası — onurlu |
| `aztec_warrior` | 2 | -0.24 … +0.27 | 1.08 | tepe 1.08h | ayak y=0; macuahuitl sağ +0.27h | Aztek savaşçı: quetzal tüy tacı, sırt tüy standardı, yuvarlak chimalli kalkan (tüy saçaklı), macuahuitl, kapitone zırh, tocapu bantları — onurlu, doğru aksesuvar |
| `friar_writing` | 2 | -0.29 … +0.43 | 0.75 | h = ayakta boy eşdeğeri; tepe 0.75h; genişlik −0.29 … +0.43h | tabure/masa y=0; mum alevi (glowdot) y≈−0.55h | Yazan keşiş: eğik yazı levhası, tüy kalem, mum + sıcak ışıma, kukuletalı |
| `scholar_lectern` | 2 | -0.21 … +0.43 | 0.95 | tepe 0.95h; kürsü sağ +0.43h | ayak y=0 | Kürsüde konuşan bilgin: açık kitap, bilgin kepi, kürk yaka |
| `child` | 2 | -0.12 … +0.17 | 0.94 | h ≈ 0.94h (8 yaş oranı, baş büyük) | ayak y=0 | Çocuk: kısa tunik, bir eli sallıyor |
| `woman_seated` | 2 | -0.30 … +0.30 | 0.80 | tepe 0.80h | ayak y=0; tabure/sandalye YOK (etek örter) | Peçeli oturan kadın (pencere önü): başı hafif eğik, kucakta tespih, dökümlü etek |
| `man_seated_bed` | 2 | -0.31 … +0.53 | 0.63 | tepe 0.63h; genişlik −0.31 … +0.53h | yatak çerçevesi YOK; yastık + battaniye dahil | Yatakta oturan hasta yaşlı adam: yastıklara yaslı, takke, elinde kadeh, battaniye dalgalı |
| `coffin` | 2 | -0.93 … +0.97 | 0.66 | h = tabut yükseklik birimi: uzunluk 1.9h, yükseklik 0.66h | sehpa y=0; geniş (omuz) ucu SAĞda | Tabut siluet: örtülü sehpa, eğimli kapak, haç, kenar çivileri (şamdan yok) |
| `crowd_a` | 2 | -0.20 … +0.19 | 0.96 | 0.94h | ayak y=0 | Kalabalık A: kasketli adam, kısa pelerin, çorap bacak |
| `crowd_b` | 2 | -0.22 … +0.21 | 0.94 | 0.94h | ayak y=0 | Kalabalık B: peçeli kadın, uzun elbise |
| `crowd_c` | 2 | -0.18 … +0.19 | 0.99 | 0.99h | ayak y=0 | Kalabalık C: sarkık geniş şapkalı adam, uzun palto, bele el |
| `crowd_d` | 2 | -0.21 … +0.20 | 0.98 | 0.98h | ayak y=0 | Kalabalık D: kukuletalı yoksul/keşiş |
| `crowd_e` | 2 | -0.14 … +0.21 | 1.05 | 1.05h (asa dahil) | ayak y=0 | Kalabalık E: morionlu asker, göğüslük, kısa asa |
| `crowd_f` | 2 | -0.20 … +0.20 | 1.02 | 1.02h | ayak y=0 | Kalabalık F: baretli soylu, kürk yakalı cüppe |
| `torchbearer` | bonus | -0.21 … +0.49 | 1.50 | tepe 1.50h (alev parlaması dahil) | ayak y=0; meşale sağ üstte | Meşaleci: yüksekte tutulan meşale + sıcak parlama (halo sprite'a pişirilmiş; titreme sahne ışığıyla verilir) |
| `standard_bearer` | bonus | -0.14 … +0.83 | 1.91 | gönder ucu 1.91h; bayrak sağ +0.83h | ayak y=0; gönder x=+0.20h | Sancaktar: yüksek gönderde çatal kuyruklu bayrak (açık tonlu çapraz = Burgonya haçı), morion |
| `litter` | bonus | -0.99 … +0.99 | 0.80 | h = taşıyıcı boyu; sırık −0.99 … +0.99h, y=−0.77h | iki `bearer`: arka −0.85h, ön +0.85h (face=1) | Sedye/tahtırevan: perdeli kabin + çatı + püskül, sırığa asılı |

Not: grup "1" = istenen mevcut türler (yenilendi), "2" = yeni türler, "bonus" = istenmeyen ek türler.

## 5. Performans (ölçüm)
- `figure()` önbellekli çizim: ≤ 0.4 ms (çoğu < 0.15 ms). İlk (önbelleksiz) sprite kurulumu: çoğu 3–8 ms, ağır kahramanlar (noble, pair_old_prince, horse_rider, cavalry_charge, sipahi) h=520'de 11–16 ms (bir kez).
- `crowd()` ile 4 sıra (≈70 figür, crowd_a…f) ilk çizim ≈275 ms, önbellekli ≈25 ms. Bu nedenle kalabalık `layers()` içinde (statik) çizilmeli (zaten öyle).
- `python3 preview_chapter.py c0 --check`: theatre çekimleri 141–185 ms/kare (yeni figürlerle fark yok; figürler önbellekte).
- Dayanıklılık testi: 49 tür × boylar (40–1200 px) × lean ±0.06 × rim=None/renkli × face=±1 → hata yok.

## 6. Araçlar
```
python3 figs_sheet.py --pages                       # out/frames/figs_sheet_1…25.png (sayfa başına 2 tür, 5 boy: 150/300/450/600/800 px × 2 arka plan: kehribar degrade | açık sisli gri)
python3 figs_sheet.py --scales noble,monk --out out/frames/x.png
python3 figs_sheet.py --grid noble,monk,woman --h 520 --cols 3 [--mist] --out out/frames/g.png
python3 figs_sheet.py --bench                       # ilk/önbellekli figure() süresi
```
Hall testi: `python3 preview_chapter.py c0 --at 8,24.5`.

## 7. Bilinen kusurlar / ana ajandan istekler
1. **Sprite çözünürlüğü**: `figure()` sprite'ı tam `h` pikselinde pişirir; kamera zoom ≥1,5 olan yakın çekimlerde bilineer büyütme kenarları hafif yumuşatır. İSTEK (stage.py): `figure(..., ss=2)` ya da `_fig_sprite`'ı 2× pişirip 0,5× çizmek (yalnız yakın çekim figürleri için).
2. **Önbellek boyutu**: `crowd()` her figüre ±%8 rastgele boy verir → çok sayıda benzersiz sprite (her biri 0,3–1,5 MB, `lru_cache(1024)` en kötü ≈0,5 GB). İSTEK: `figure()` içinde `hpx`'i 4'ün katına yuvarlamak (%1'den az ölçek farkı) ya da çekim başına önbelleği boşaltmak.
3. Eller (özellikle yumruk) sade; 800 px üstünde parmaklar ayrı çizilmez (boğum + başparmak var).
4. Kenar ışığı yönü sabit (sol-üst); ışık sağdan gelen sahnede `face=-1` kullan ya da `rim` rengini kısık ver.
5. Gözler/yüz içi gösterilmez (siluet); mimik yok.
6. `STIL_REHBERI.md` bölüm 6'daki "Figür türleri" satırı yeni adlarla güncellenebilir (liste yukarıdaki tabloda).
