# notlar_figur_lab.md — Figür Laboratuvarı teslim notları

Rol: FİGÜR LABORATUVARI (figür-lab). Kapsam: `stage.py` siluet figürlerinin "kâğıt-kesim / gölge-tiyatrosu" kalitesinde yeniden yazımı.
`stage.py`, `scenes_lib.py` ve diğer ortak dosyalara DOKUNULMADI; yalnız kayıt kancası `@ST.figx` kullanıldı (hiçbir `ST.figure/_fig_sprite` yaması YOK). `git` kullanılmadı. Soru sorulmadı; kararlar aşağıda.

## 1. Ne yapıldı (özet)
- Eski kaba/"blob" figürler tamamen yenilendi: ≈7–7,5 baş oranı, 3/4-profil baş (burun, dudak, çene, sakal/bıyık), türe özgü şapka/başlık (24 çeşit), cüppe/pelerin etek kıvrımları
  (koyu-açık mercek çizgiler + sol kenarda ince ışık), etekte negatif-alan (kâğıt oyuğu) çentikler, dişli (dagged) etek, düzensiz bulut kenarlı kürk yaka, ruff, süs bantları (elmas / tocapu / basamaklı sınır), zincir, düğme, kemer, kese.
- Işık dili: koyu gövde (`col`, varsayılan `#0C0705`) + her parçanın KENDİ sol-üst kenarında sıcak kenar ışığı (kâğıt-katman etkisi; yukarıdan aşağı sönümlü) + yumuşak iç ışıltı. Açık/sisli zeminde de okunur (koyu siluet + ince sıcak çizgi); `rim=None` → kenar ışığı yok.
- **52 tür** (19 istenen mevcut + 22 istenen yeni + 11 ek): hepsi `@ST.figx`. Tür adları değişmedi; `figure(f, kind, x, y_ayak, h, col, rim, face, alpha, sway, rot, lean, bob)` imzası aynı.
- Hepsi SAĞA bakar (`face=+1`); `face=-1` aynalar (kenar ışığı da aynalanır → ışık sağdan gelen sahnede kullan). Ayak (0,0), yukarı −y.
- Kararlar: (1) Kimlik gizli: `emperor_old/pair_old_prince` genel yaşlı hatlı (çene hafif belirgin, karikatür yok). (2) Yerli halk figürleri (Nahua/İnka/Aztek) gerçek aksesuarlarla ve onurlu duruşla; Kuzey Amerika "savaş bonesi" klişesi YOK. (3) Tahta/sandalye/yatak çerçevesi gibi mobilya figüre dahil edilmedi (sahne çizer); mobilyalı alternatif `seated_chair` ek tür olarak verildi. (4) Gerçek kişi karikatürü yok; Osmanlı figürleri genel tip.

## 2. Dosyalar (hepsi bu klasörde; yeni)
| dosya | içerik |
|---|---|
| `figs_kit.py` | geometri (köşe destekli spline `sp`, `limb`, `bar`, `lens`, `place`…), `Fig` (parça listesi: fill/cut/line/solid/glow + kenar ışığı + `merge`), baş/sakal profilleri, eller, ayakkabı, tüy |
| `figs_parts.py` | şapkalar, `add_head` (boyun+baş+sakal+saç+şapka), `add_arm`, `add_leg`, `robe_path` (S eğrili/dişli cüppe), kıvrım yelpazesi, kürk şeridi, ruff, etek bandı |
| `figs_lab.py` | noble, merchant, cardinal, scribe, monk, woman, emperor_old, prince, page, seated (+`seated_fig`), kneel, pair_old_prince |
| `figs_war.py` | pikeman, landsknecht, janissary, knight, conquistador, sailor, native (+ `torso`, `pike` yardımcıları); en sonda `figs_horse` ve `figs_more`'u yükler |
| `figs_horse.py` | horse, horse_walk, horse_rider, horse_rider_walk, cavalry_charge(+_b), sipahi(+_b) |
| `figs_more.py` | child, peasant, fisherman, bearer, friar_writing, scholar_lectern, woman_seated, man_seated_bed, coffin, inca_noble, aztec_warrior, arquebusier, halberdier, crowd_a…f; ek: torchbearer, standard_bearer, litter, ottoman_noble, peasant_scythe, seated_chair |
| `figs_sheet.py` | kontak sayfası / ızgara / benchmark aracı (aşağıda) |
| `notlar_figur_lab.md` | bu belge |

Yükleme zinciri: `stage` (sonunda) → `figs_lab`, `figs_war` → (`figs_horse`, `figs_more`); hepsi `sk.optional_import` ile: bir modül hata verirse uyarı basılır, öteki türler çalışır. Her import sırası (`shots`, `scenes_lib`, `stage`, `compose`, tek tek `figs_*`) denendi: temiz, 52 tür kayıtlı.
Yeni tür eklemek: `figs_more.py` içinde `@fx("ad") def f(h, lean): F = Fig(h, lean); ...; return F.build()`.

## 3. Kullanım notları (sahne ajanları için)
- `ST.figure(f, "noble", x, y_ayak, h, col="#0A0604", rim="#C58A44", face=1)`. Hall'daki `col`/`rim` değerleri aynen çalışır. İç ayrıntı renkleri `col` ve `rim`'den türer → sisle karışmış (`mix(col, fog, …)`) renklerle tutarlı. Uzak sıralarda `rim=None` ya da kısık rim ver (kalabalıkta parlak çizgi gürültüsü olmasın).
- `h` ≈ figürün piksel boyu (şapka/tüy dahil tepe ≈ 0.9–1.1h; tablodaki "tepe"). Mızrak/pike/alebard/sancak h'ın 1.3–1.9 katına çıkar; "yatay" sütunu h=1 birimine göre sol…sağ sınırdır (mızrak/at/sedye geniştir). Çekim çerçevesini buna göre kur.
- `lean` (±0.02–0.1): üst gövdeyi ayaktan kaydırır (tepede ≈1,5·lean·h). `crowd()`'ın verdiği ±0.02 ince varyasyondur.
- Önbellek: sprite `(tür, round(h), col, rim, round(lean,2))` anahtarlı; statik katmanda ilk maliyet bir kez ödenir. Dinamik (`dyn`) çizimde aynı `h`'ı koru (her yeni `h` yeni sprite pişirir).
- Süvari/atlı türlerinde `h` = **zeminden binicinin başlığına** toplam boy (at kulağı h/1.2); `horse`/`horse_walk`'ta `h` = at kulak yüksekliği.
- Animasyon: `cavalry_charge` ↔ `cavalry_charge_b` (ve `sipahi` ↔ `sipahi_b`) 5–7 karede bir dönüşümlü çiz → dörtnala; `horse` ↔ `horse_walk` → adım. Dörtnalada toynaklar 0.03–0.07h havada: `y_ayak`'ı ≈0.05h aşağı al ya da toz/duman ekle. `sway`/`rot`/`bob` ile ek hareket.
- Işıklı öğeler (mum, meşale, fitil): `friar_writing` (mum), `torchbearer` (meşale), `arquebusier` (fitil ucu) sıcak parlamayı sprite'a pişirir (titremez); titreme için sahne `dyn`'inde ek `kPlus` ışıma çiz.
- `litter` ortada, iki `bearer`: arka taşıyıcı x−0.52h, ön taşıyıcı x+0.52h (aynı y_ayak, face=1) → sırıklar birleşir (denendi: `out/frames/figs_test_litter.png`).
- Sandalye/taht: `seated` mobilyasızdır (sahne tahtı arkaya çizer; oturak yüksekliği ≈0.27h → tahtın oturak çizgisine `y_ayak`'ı göre hizala). Sahnede taht yoksa `seated_chair`.
- Fiziksel olarak yanlış kombinasyonlar: `face=-1` + `lean` işareti de aynalanır; negatif `h` desteklenmez.

## 4. Tür kataloğu (ölçüler h=1 birimine göre; grup: 1 = istenen mevcut, 2 = istenen yeni, ek = fazladan)
| ad | grup | yatay (sol…sağ) | tepe | h / ölçek | ayak–hizalama | açıklama |
|---|---|---|---|---|---|---|
| `noble` | 1 | -0.22 … +0.23 | 1.02 | tepe 1.02h (baret tüyü dahil); ≈7,4 baş | ayak y=0; ön ayak sağda | Holbein tarzı soylu: dişli (dagged) dizüstü cüppe + etek bandı, kürk klapa, baret+tüy, sivri sakal, zincir; sağ eli belde, uzak elde eldiven |
| `merchant` | 1 | -0.20 … +0.22 | 0.96 | tepe 0.94h | ayak y=0 | Tüccar/banker: ayak bileği boy kürk yakalı cüppe, kemer+kese, elinde defter, yuvarlak bone |
| `cardinal` | 1 | -0.32 … +0.24 | 0.95 | tepe 0.95h | ayak y=0; arka etek sürüntüsü solda −0.32h | Kardinal: geniş kenarlı galero + püsküllü kordonlar (1-2-3), mozzetta, arkaya savrulan uzun etek, göğüste rulo |
| `scribe` | 1 | -0.17 … +0.26 | 0.94 | tepe 0.93h | ayak y=0; tüy kalem sağda +0.26h | Katip: baldır boy gömlek+çorap, öne eğik, bilgin kepi, eğik yazı levhası + tüy kalem, hokka |
| `monk` | 1 | -0.22 … +0.22 | 0.94 | tepe 0.95h | ayak y=0 | Keşiş: kukuletalı habit, düğümlü ip kuşak, tespih, başı eğik, ellerini kolun içinde kavuşturmuş |
| `woman` | 1 | -0.28 … +0.26 | 0.93 | tepe 0.93h (kadın oranı) | ayak y=0; etek −0.28h … +0.26h | Soylu kadın: dar korse + geniş çan etek (arkada sürüntü, elmas bant), uzun peçe, kavuşmuş eller |
| `emperor_old` | 1 | -0.21 … +0.22 | 0.91 | tepe 0.89h (kambur) | ayak y=0; baston sağda +0.21h | Yaşlı imparator: bükülü, kürk yakalı ağır cüppe, bastonlu; yumuşak bone, kısa gri sakal (kimlik gizli) |
| `prince` | 1 | -0.29 … +0.19 | 1.00 | tepe 1.00h | ayak y=0; kılıç ucu solda −0.29h | Genç soylu/prens: kısa pelerin, kılıç kabzasında el, çorap bacak, şişkin pantolon, ruff, baret+tüy |
| `page` | 1 | -0.12 … +0.19 | 0.97 | tepe 0.95h (çocuk oranı) | ayak y=0 | Sayfa (uşak çocuk): kısa tunik, rulo mektup uzatır |
| `seated` | 1 | -0.29 … +0.29 | 1.00 | h = AYAKTA boy eşdeğeri; oturunca tepe 0.78h (asa 1.0h) | ayak y=0; oturak yüksekliği ≈0.27h; sandalye/taht YOK (sahne tahtı arkaya çizer) | Tahtta taçlı imparator: dik oturuş, ermin yaka+benekler, imparatorluk tacı (haç), asa; mantı arkadan yere |
| `kneel` | 1 | -0.39 … +0.28 | 0.76 | h = ayakta boy eşdeğeri; tepe 0.76h | ayak y=0; arka diz/baldır yerde (solda −0.39h) | Tek diz çökmüş dilekçi/biat eden: başı eğik, eller dizde, pelerin arkaya sürünür |
| `pair_old_prince` | 1 | -0.42 … +0.41 | 1.00 | h = PRENSİN boyu (tepe 1.00h) | ayak y=0; imparator solda/geride, prens sağda; ikisi de sağa bakar | KİLİT FİGÜR (c0/c12): bükülü yaşlı imparator + önde baston; uzanan kolu/eli genç prensin omzunda |
| `pikeman` | 1 | -0.14 … +0.21 | 1.80 | gövde 0.94h, pike ucu 1.80h | ayak y=0; pike yerde x=+0.17h | Piyade (pike): kasket, göğüs zırhı, 3 uyluk levhası, iki elle dik pike |
| `landsknecht` | 1 | -0.26 … +0.64 | 1.84 | gövde 1.0h, pike ucu 1.84h (diyagonal) | ayak y=0; geniş duruş; pike sağda +0.64h | Landsknecht: tabak şapka + 4 tüy, yırtmaçlı şişkin kol/pantolon, Katzbalger kılıç, önde diyagonal pike |
| `janissary` | 1 | -0.27 … +0.24 | 1.30 | gövde ≈1.0h (börk dahil), tüfek 1.3h | ayak y=0; kılıç solda −0.27h | Yeniçeri: börk (sırtta sarkan uç, önde kaşıklık), kaftan+kuşak, kilij, yerde fitilli tüfek, bıyık |
| `knight` | 1 | -0.21 … +0.23 | 1.08 | tepe 1.08h (tüy dahil) | ayak y=0; kılıç ucu yerde x=+0.175h | Tam zırhlı şövalye: armet+tüy, omuzluk, tassets, diz levhası, iki el kılıç kabzasında |
| `conquistador` | 1 | -0.30 … +0.38 | 1.64 | gövde 1.0h, mızrak+flama 1.64h | ayak y=0; rapier solda −0.30h; flama sağda +0.38h | Fatih: morion, peascod göğüs zırhı, pelerin, rapier, bele dayalı kol, flamalı mızrak |
| `sailor` | 1 | -0.17 … +0.20 | 0.99 | tepe 0.95h | yalın ayak y=0 | Denizci: Frig tipi yün bere, bol gömlek, dizaltı pantolon, omuzda halat kangı, kemerde bıçak |
| `native` | 1 | -0.13 … +0.22 | 1.04 | tepe 1.04h | ayak y=0; asa sağda +0.18h | Mezoamerika (Nahua) soylusu: omuzda düğümlü tilma (basamaklı sınır), süslü bel bezi, bağlı sandalet, alın bandı+tüy, asa — onurlu, karikatürsüz |
| `arquebusier` | 2 | -0.19 … +0.61 | 1.23 | gövde 1.0h; namlu ucu +0.61h / 1.23h | ayak y=0; fitil ucu parlar (glowdot, sprite'a pişmiş) | Fitilli tüfekli (arcabucero): sarkık şapka+tüy, bandolier (barut tüpleri), omuzda arkebüz, yanan fitil |
| `halberdier` | 2 | -0.20 … +0.29 | 1.75 | gövde 0.94h; alebard ucu 1.75h | ayak y=0; sap x=+0.185h | Alebardiyer: kasket, göğüs zırhı, iki elle dik alebard (uç+balta+kanca), kılıç |
| `horse` | 2 | -0.75 … +0.75 | 1.11 | h = KULAK ucu yüksekliği (tepe 1.09h); withers 0.77h; gövde −0.56…+0.43h, baş +0.76h | toynaklar y=0; kuyruk solda, burun sağda | Tek at, duran: kemerli boyun, ince başlı, yele tutamları, perçem, dizgin/burunluk, kuyruk sarkık |
| `horse_walk` | 2 | -0.75 … +0.76 | 1.08 | aynı | ön yakın bacak havada (diz bükük) | Yürüyen at (horse ile dönüşümlü çizilirse adım hissi) |
| `horse_rider` | 2 | -0.63 … +0.63 | 1.64 | h = zeminden binici miğferine; at kulağı h/1.2, binici oturma boyu 0.45·(h/1.2); mızrak ucu 1.59h | toynak y=0 | Zırhlı atlı: kapariş (at örtüsü), armet+tüy, dik mızrak; duran at |
| `horse_rider_walk` | 2 | -0.63 … +0.63 | 1.62 | aynı (mızrak ileri-yukarı eğik, flamalı) | toynak y=0 | Yürüyen at + zırhlı atlı (Mühlberg/Tiziano tarzı duruş) |
| `cavalry_charge` | 2 | -0.91 … +1.57 | 1.09 | h = zeminden binici miğferine; mızrak ucu sağda +1.60h | dörtnalada toynaklar ≈0.07h havada (y_ayak'ı ≈0.05h aşağı al ya da toz ekle) | Dörtnala süvari hücumu POZ A (uzamış): yatay mızrak + flama, kuyruk/yele geriye |
| `cavalry_charge_b` | 2 | -0.96 … +1.50 | 1.09 | aynı | toynaklar ≈0.03h havada | Dörtnala POZ B (toplanmış): A ile 5–7 karede bir dönüşümlü çiz |
| `sipahi` | 2 | -0.91 … +0.77 | 1.27 | h = zeminden başlığa (sorguç/kılıç ucu ≈1.1h) | dörtnala A pozu; toynaklar havada | Osmanlı sipahisi: sarık+sorguç, kaftan, sırtta yuvarlak kalkan, havada kilij, süslü at örtüsü |
| `sipahi_b` | 2 | -0.96 … +0.63 | 1.27 | aynı | B pozu (toplanmış) | Sipahi: A ile dönüşümlü |
| `peasant` | 2 | -0.15 … +0.25 | 1.12 | tepe 1.12h (hasır şapka) | ayak y=0; yaba yerde x=+0.20h | Köylü: geniş kenarlı şapka, bol gömlek, dizlik; yere basan yaba |
| `fisherman` | 2 | -0.12 … +0.61 | 1.20 | tepe 1.20h (olta ucu +0.61h sağda) | yalın ayak y=0 | Balıkçı: Frig bere, paçaları sıvalı, sırık olta + ip + balık, sepet |
| `bearer` | 2 | -0.47 … +0.53 | 0.94 | tepe 0.91h; sırık −0.47…+0.53h | ayak y=0; sırık omuz hizası y=−0.77h | Sedye/tahtırevan taşıyıcısı: omuzda uzun sırık (iki ucunda bağ halkası), çömelik yürüyüş |
| `inca_noble` | 2 | -0.14 … +0.22 | 1.14 | tepe 1.14h (asa ucu dahil) | ayak y=0; asa sağda +0.18h | İnka soylusu: llautu bandı + alında saçak (mascaypacha) + iki tüy, kulak diski, unku (tocapu bantları), yacolla mantı, tören asası — onurlu |
| `aztec_warrior` | 2 | -0.24 … +0.27 | 1.08 | tepe 1.08h | ayak y=0; macuahuitl sağda +0.27h | Aztek savaşçı: quetzal tüy tacı, sırt tüy standardı, yuvarlak chimalli (tüy saçaklı), macuahuitl, kapitone zırh, tocapu bantları — onurlu, doğru aksesuvar |
| `friar_writing` | 2 | -0.29 … +0.43 | 0.75 | h = ayakta boy eşdeğeri; tepe 0.75h; −0.29…+0.43h | tabure/masa y=0; mum alevi y≈−0.55h (glowdot) | Yazan keşiş: eğik yazı levhası, tüy kalem, mum + sıcak ışıma, kukuletalı |
| `scholar_lectern` | 2 | -0.21 … +0.43 | 0.95 | tepe 0.95h; kürsü +0.43h | ayak y=0 | Kürsüde konuşan bilgin: açık kitap, bilgin kepi, kürk yaka |
| `child` | 2 | -0.12 … +0.17 | 0.94 | tepe 0.94h (≈8 yaş, ≈5.7 baş) | ayak y=0 | Çocuk: kısa tunik, bir eli sallıyor |
| `woman_seated` | 2 | -0.30 … +0.30 | 0.80 | tepe 0.80h | ayak y=0; sandalye YOK (etek örter) | Peçeli oturan kadın (pencere önü): başı hafif eğik, kucakta tespih, dökümlü etek |
| `man_seated_bed` | 2 | -0.31 … +0.53 | 0.63 | tepe 0.63h; −0.31…+0.53h | yatak çerçevesi YOK; yastık + battaniye dahil | Yatakta oturan hasta yaşlı adam: yastıklara yaslı, takke, elinde kadeh, battaniye dalgalı |
| `coffin` | 2 | -0.93 … +0.97 | 0.66 | h = tabut yükseklik birimi: uzunluk 1.9h, yükseklik 0.66h | sehpa y=0; geniş (omuz) ucu SAĞda | Tabut siluet: örtülü sehpa, eğimli kapak, haç, kenar çivileri (şamdan yok) |
| `crowd_a` | 2 | -0.20 … +0.19 | 0.96 | 0.94h | ayak y=0 | Kalabalık A: kasketli adam, kısa pelerin, çorap bacak |
| `crowd_b` | 2 | -0.22 … +0.21 | 0.94 | 0.94h | ayak y=0 | Kalabalık B: peçeli kadın, uzun elbise |
| `crowd_c` | 2 | -0.18 … +0.19 | 0.99 | 0.99h | ayak y=0 | Kalabalık C: sarkık geniş şapkalı adam, uzun palto, bele el |
| `crowd_d` | 2 | -0.21 … +0.20 | 0.97 | 0.98h | ayak y=0 | Kalabalık D: kukuletalı yoksul/keşiş |
| `crowd_e` | 2 | -0.14 … +0.21 | 1.05 | 1.05h (asa dahil) | ayak y=0 | Kalabalık E: morionlu asker, göğüslük, kısa asa |
| `crowd_f` | 2 | -0.20 … +0.20 | 1.02 | 1.02h | ayak y=0 | Kalabalık F: baretli soylu, kürk yakalı cüppe |
| `torchbearer` | ek | -0.21 … +0.49 | 1.50 | tepe 1.50h (alev parlaması dahil) | ayak y=0; meşale sağ üstte | Meşaleci: yüksekte meşale + sıcak parlama (sprite'a pişmiş; titreme için sahnede ek kPlus ışıma çiz) |
| `standard_bearer` | ek | -0.14 … +0.83 | 1.91 | gönder ucu 1.91h; bayrak +0.83h sağda | ayak y=0; gönder x=+0.20h | Sancaktar: yüksek gönderde çatal kuyruklu bayrak (açık tonlu çapraz = Burgonya haçı), morion |
| `litter` | ek | -0.99 … +0.99 | 0.80 | h = taşıyıcı boyu; sırık −0.99…+0.99h, y=−0.77h | iki `bearer`: arka x−0.52h, ön x+0.52h (aynı y_ayak, face=1); litter ortada | Sedye/tahtırevan: perdeli kabin + çatı + püskül, sırığa asılı |
| `ottoman_noble` | ek | -0.19 … +0.23 | 0.98 | tepe 1.0h (kavuk dahil) | ayak y=0 | Osmanlı devlet adamı (genel tip): kavuk+sarık sargısı, ankle boy kaftan, geniş kuşak + hançer, sivri çizme, bıyık |
| `peasant_scythe` | ek | -0.35 … +0.61 | 1.27 | tepe 1.12h; tırpan ucu 1.22h, bıçak +0.43h sağda | ayak y=0; sap solda −0.34h | Tırpanlı köylü: omuzda tırpan (uzun sap + kıvrık bıçak), geniş şapka, bol gömlek |
| `seated_chair` | ek | -0.32 … +0.29 | 1.08 | seated ile aynı birim; yüksek arkalık 1.07h | ayak y=0; sandalye arkalığı solda −0.32h | Yüksek arkalıklı (oyma tepelikli) sandalye/taht + taçlı oturan: sahne tahtı yoksa kullan |

## 5. Kontak sayfaları (`out/frames/figs_sheet_N.png`, N=1…26)
Her sayfa 2 tür; her tür 5 boy (150, 300, 450, 600, 800 px) × 2 arka plan (solda koyu amber degrade, sağda açık sisli gri). Sayfa → tür: `figs_sheet_1.png` → noble, merchant; `figs_sheet_2.png` → cardinal, scribe; `figs_sheet_3.png` → monk, woman; `figs_sheet_4.png` → emperor_old, prince; `figs_sheet_5.png` → page, seated; `figs_sheet_6.png` → kneel, pair_old_prince; `figs_sheet_7.png` → pikeman, landsknecht; `figs_sheet_8.png` → janissary, knight; `figs_sheet_9.png` → conquistador, sailor; `figs_sheet_10.png` → native, arquebusier; `figs_sheet_11.png` → halberdier, horse; `figs_sheet_12.png` → horse_walk, horse_rider; `figs_sheet_13.png` → horse_rider_walk, cavalry_charge; `figs_sheet_14.png` → cavalry_charge_b, sipahi; `figs_sheet_15.png` → sipahi_b, peasant; `figs_sheet_16.png` → fisherman, bearer; `figs_sheet_17.png` → inca_noble, aztec_warrior; `figs_sheet_18.png` → friar_writing, scholar_lectern; `figs_sheet_19.png` → child, woman_seated; `figs_sheet_20.png` → man_seated_bed, coffin; `figs_sheet_21.png` → crowd_a, crowd_b; `figs_sheet_22.png` → crowd_c, crowd_d; `figs_sheet_23.png` → crowd_e, crowd_f; `figs_sheet_24.png` → torchbearer, standard_bearer; `figs_sheet_25.png` → litter, ottoman_noble; `figs_sheet_26.png` → peasant_scythe, seated_chair.
Ek test görüntüleri: `out/frames/figs_test_room.png` (oda: ay ışığı + mum + yatak), `out/frames/figs_test_litter.png` (sedye + 2 taşıyıcı), `out/frames/figs_test_battle.png` (sisli açık zeminde pike blokları + arkebüzcüler + süvari), `out/frames/figs_test_crowd.png` (crowd_a…f ile 4 sıra kalabalık), `out/frames/c0_t8.png`, `c0_t24.5.png` (salon).

## 6. Performans (ölçüm; makine paylaşımlı, yük ≈11/4 çekirdek → ±2× gürültü)
- `figure()` önbellekli çizim: tipik 0.03–0.2 ms, en kötü ≈0.5 ms (gürültülü ölçümde 2.5 ms) → **≤10 ms hedefi büyük farkla sağlanır**. 170 figürlük sahne tekrar çizimi: 4 ms.
- İlk (önbelleksiz) sprite kurulumu, h=520: medyan ≈5 ms; ağır kahramanlar (pair_old_prince, horse_rider, cavalry_charge, sipahi, seated_chair) 12–20 ms (bir kez). h=300'de yarısı.
- `crowd()` 4 sıra (≈70 figür, crowd_a…f) ilk çizim ≈275 ms, önbellekli ≈25 ms → kalabalık `layers()` içinde (statik) çizilmeli (hall zaten öyle).
- `python3 preview_chapter.py c0 --check`: theatre çekimleri 141–185 ms/kare (yeni figürlerle fark yok); uyarı yok.
- Dayanıklılık testi: tüm türler × boylar (40–1200 px) × lean ±0.06 × rim=None/renkli × face=±1 → hata yok.
- Kenar ışığı hilali katmansız çift-kırpma ile çizilir (saveLayer'a göre ≈%10–50 hızlı).

## 7. Araçlar
```
python3 figs_sheet.py --pages                       # out/frames/figs_sheet_1…26.png
python3 figs_sheet.py --scales noble,monk --out out/frames/x.png
python3 figs_sheet.py --grid noble,monk,woman --h 520 --cols 3 [--mist] [--cellw 700] --out out/frames/g.png
python3 figs_sheet.py --bench                       # ilk/önbellekli figure() süresi
```
Hall testi: `python3 preview_chapter.py c0 --at 8,24.5`.

## 8. Bilinen kusurlar / ana ajandan istekler
1. **Sprite çözünürlüğü (yakın çekim)**: `figure()` sprite'ı tam `h` pikselinde pişirir; kamera zoom ≥1,5'te figürler bilineer büyür (arka plan katmanları da 1× pişip aynı şekilde büyüdüğü için uyumlu, yine de yakın çekimde hafif yumuşak). İSTEK (stage.py, isteğe bağlı): `_fig_sprite`'ı 2× pişirip `figure()`'da 0,5× çizmek, ya da `bake()`'i zoom'a göre büyütmek.
2. **Önbellek boyutu**: `crowd()` her figüre ±%8 rastgele boy verir → çok sayıda benzersiz sprite (her biri 0,2–1,5 MB; `lru_cache(1024)` en kötü ≈0,5 GB). İSTEK: `figure()` içinde `hpx`'i 4'ün katına yuvarlamak (<%1 ölçek farkı) ya da çekim başına önbelleği boşaltmak.
3. Eller sade (boğum + başparmak var, parmak ayrımı yok); yüz içi/göz yok (siluet).
4. Kenar ışığı yönü sabit sol-üst; ışık sağdan gelen sahnede `face=-1` kullan ya da `rim` rengini kısık ver.
5. Dörtnala/yürüyüş yalnız 2 poz; çok akıcı bacak animasyonu için ek poz gerekir (istenirse `HORSE_*`/`GALLOP_*` sözlükleri `figs_horse.py` içinde, eklem listeleriyle kolayca çoğaltılır).
6. `STIL_REHBERI.md` bölüm 6'daki "Figür türleri" satırı yeni adlarla güncellenebilir (liste yukarıdaki tabloda).
