# Madalya-lab notları (medal_extra.py + icons_extra.py)

`medal.py` ve `icons.py` **hiç değiştirilmedi**. shots.py iki modülü otomatik yükler (`import shots` uyarısız, ≈0,25 sn).

## 1. Madalyalar — şimdi 49 kişinin hepsi aynı standartta (giysili/yakalı/takılı büst, kısa boyun, halka içinde kesilmeyen başlık)
Kontak sayfaları: `out/frames/medals_all_sheet.png` (49 kişi, 8 sütun, altın) · `out/frames/medals_extra_sheet.png` (23 yeni kişi).

**Eski 26 anahtar yükseltildi** (anahtar adları, yüz parametreleri ve `INSCR` aynı; çizim `_x` hattına geçti): karl_genc, karl_olgun, karl_yasli, fransuva (= `*_x` sürümleri), henri8, luther, melanchthon, suleyman, barbaros, fugger, klemens, felipe2, juana, isabel, ferdinand, maksimilyan, kortes, pizarro, lascasas, moritz, orange, margareta, tiziano, durer, elkano, makedonya. **Eski çizimler `<anahtar>_old`** anahtarıyla duruyor (örn. `luther_old`, aynı `INSCR`); `*_x` anahtarları da duruyor (karl/fransuva için eşdeğer).
**23 yeni kişi:** filip, fernando, maria_burgonya, isabel_kastilya, sarlman, karl_cocuk, padilla, bravo, maldonado, maria_pacheco, frederik_bilge, johann_friedrich, louise_savoy, catherine_aragon, mary_macar, lajos2, zapolya, doria, atahualpa, moctezuma, magellan, sepulveda, welser.

Önerilen metal (rehber kodu): Habsburg hattı/atalar gold (+ karl_*, felipe2, ferdinand, maksimilyan, juana, isabel, margareta, mary_macar) · fransuva, louise_savoy royal · suleyman, barbaros forest · klemens violet · luther, melanchthon, frederik_bilge, johann_friedrich, moritz teal · henri8, catherine_aragon crimson · fugger, kortes, pizarro, elkano, magellan, welser, atahualpa, moctezuma bronze · tiziano, durer, lascasas, sepulveda ivory · diğerleri silver.
Halka yazıları: Latince; Atahualpa Quechua, Moctezuma Nahuatl. İkonografi stilize/tahmini; yerli hükümdarlar onurlu tasvir.

**Mimari:** `_x=True` kişiler genişletilmiş hatta çizilir (`medal.portrait_height` yamalı; `*_old` ve başka eski kayıtlar eski hatta gider). Tablolar `HAIR, BEARD, BUST, HAT, ACC` (`@reg(HAT,"ad")`). Yeni türler: saç tonsure/curly/wavy/bowl/long_flow/crop/child/inca/sides/thin_back · sakal long_pointed_x/trim/cropped/goatee/full_round/broad/long_flow/white_long/short_gray/ship/chinstrap (+`must`) · başlık tudor_bonnet, barett_plain, turban_x, turban_small_x, gold_haube, camauro_x, mourning_veil, jeweled_net, broad_hat, morion_x, knit_cap, diadem + öncekiler (hennin, gable_hood, french_hood, mascapaicha, xiuhhuitzolli=copilli, kalpak…) · giysi monk_habit, kaftan_x, ruff_black_x, cassock_x, armor_x (+gv="greek") + öncekiler. Parametreler: `eye, brow_style, lash, mouth, ear, cheek, puff, ck, nback, iris, nobadge, plumed, peak, nochain`.
Tarama (3. madde): 49 kişi × (düz+flip) hatasız; gold/royal/forest/violet/teal/bronze/crimson, 120–900 px denendi; ölçüm: tüm başlık/tüy uçları halkanın iç çemberinin içinde (r ≤ 385 / 400), bust alt kenarda halkaya kadar uzanıyor (boyun/omuz havada kesilmiyor).

## 2. Simgeler — 32 yeni (`icons.names()` → 66 ad)
press, chest, globe, compass, helmet, horse, arquebus, flag, candle, sun_disc, feather, bell, ballot, gavel, pillars, cane, pickaxe, galley, litter, chains, lightning, heart, fist, mountain, elector_hat, foot_gout, bed, tent, ladder, crown_cracked, sack, book_open. Takma ad: `gun`=arquebus, `sun`=sun_disc. Sayfa `out/frames/icons_extra_sheet.png`; `icons_extra.sheet(keys, metals, cols, size, out)`. 70/120/200/460 px ve 8 metalde okunuyor.

## 3. Bilinen kusurlar
- Yüzler aynı profil şablonundan (burun/çene/dudak/alın parametreleri + saç/sakal/başlık/giysi farkı); ince yüz ayrımı sınırlı. ≤150 px'te sakal/kürk dokusu bulanır, silüet okunur.
- Basitleştirmeler: Luther'in tonsürü yok (siyah Barett + kısa yan saç); Süleyman sarığı sade sarmal; Pizarro morion'u geniş siperlikli kask gibi okunuyor; İskender'de diadem + dalgalı saç (sade zırh); Maksimilyan şapkası stilize.
- Sarlman: saç+sakal+taç yoğun. Margareta ile Mary (Macar) benzer dul başlığı taşır (Margareta'da alın sivrisi + inci).
- Simgeler: horse/arquebus/mountain stilize-naif; crown_cracked yalnız `imperial_crown` üstüne kırık çizgi ve kayma.
