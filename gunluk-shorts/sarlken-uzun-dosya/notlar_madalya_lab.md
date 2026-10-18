# Madalya-lab notları (medal_extra.py + icons_extra.py)

`medal.py` ve `icons.py` **hiç değiştirilmedi** (26 eski madalya ve 32 eski simge birebir aynı). shots.py iki modülü otomatik yükler; doğrulandı (`import shots` → uyarı yok, ≈0,25 sn).

## 1. Madalyalar — 23 yeni anahtar (`medal.PEOPLE`, `medal.INSCR`)
Doğrulama sayfası: `out/frames/medals_extra_sheet.png` (altın, 6×4). Önerilen metal (rehberdeki koda göre):

| anahtar | kim | metal önerisi |
|---|---|---|
| filip, maria_burgonya, fernando, isabel_kastilya, karl_cocuk, mary_macar, sarlman | Habsburg hattı / atalar | gold |
| lajos2, zapolya, doria | Macaristan / Cenova | silver |
| louise_savoy | Fransa | royal |
| catherine_aragon | İngiltere | crimson |
| frederik_bilge, johann_friedrich | Saksonya (Reform) | teal |
| padilla, bravo, maldonado, maria_pacheco | Komünero (idam/yas anında `onyx` seyrek) | silver |
| atahualpa, moctezuma, magellan, welser | Yeni Dünya / fatih / banker | bronze |
| sepulveda | bilgin | ivory (ya da violet) |

Halka yazıları Latince (U→V); Atahualpa Quechua (`ATAWALLPA · SAPA · INKA · TAWANTINSUYU`), Moctezuma Nahuatl (`MOTEUCZOMA · XOCOYOTZIN · HUEY · TLATOANI`). İkonografi tahmini/stilize; yerli hükümdarlar onurlu tasvir (kulak diski/makarası, mascapaicha, turkuaz diadem, tokapu/tilmatli).

**İsteğe bağlı varyantlar:** `karl_genc_x, karl_olgun_x, karl_yasli_x, fransuva_x` — eski yüz parametreleriyle, ama giysili/kürklü büst + zengin başlık/sakal (eski `karl_*`/`fransuva` aynen duruyor; hangisini kullanacağın ana ajan kararı — video boyunca aynı seti kullan). Kıyas için: `medal.medal_sheet(['karl_genc','karl_genc_x','karl_olgun','karl_olgun_x',...], 'gold', cols=4, size=480, out=...)`.

**Mimari:** `_x=True` olan kişiler genişletilmiş hatta çizilir (medal.portrait_height yamalı; eski anahtarlar eski hatta gider). Yeni tablolar: `HAIR, BEARD, BUST, HAT, ACC` (`@reg(HAT,"ad")`). Hazır türler: saç wavy/bowl/long_flow/crop/child/inca/sides/thin_back · sakal trim/cropped/goatee/full_round/broad/long_flow/white_long/short_gray/ship/chinstrap (+ bıyık `must`: short/droop/handle/pencil/long) · başlık burg_bonnet, barrete, castilian_veil, imperial_crown, hennin, gable_hood, french_hood, widow_wimple, toca, child_cap, kalpak, beret_wide, beret_feathers, mascapaicha, xiuhhuitzolli (=`copilli`), seaman_cap, biretta, merchant_cap, royal_cap_crown, kalot, toque_brim, feather_beret, plain_coif · giysi fur_jacket, dark_doublet, dark_gown_collar, mantle_brooch, jeweled_gown, gown_fur, black_dress, dark_gown_plain, child_doublet, leather_jerkin, cloak_buttons, lawyer_robe, fur_gown_wide, courtly_jacket, dolama, dark_robe, tunic_inca, tilmatli, explorer_doublet, academic_robe, fur_gown_merchant · takı ear_inca/ear_aztec/ear_pearl.
Ek yüz parametreleri: `eye, brow_style, lash, mouth, ear, cheek, puff, ck` (çocuk alt-yüz sıkıştırma), `nback` (ince boyun), `iris`.
Bust, eski madalyalardan farklı olarak **giysi/yaka/takı görünür** (boyun daha kısa, omuz eğimli); `scale`/`dy` kişiye göre ayarlı (taçlı/tüylü başlıklar halka içinde kesilmiyor).
Denendi: gold/royal/forest/bronze/teal/crimson, 120/200/340/640/900 px, `flip=True`, `shots.draw_medal`.

## 2. Simgeler — 32 yeni (`icons.names()` → 66 ad)
press, chest, globe, compass, helmet, horse, arquebus, flag, candle, sun_disc, feather, bell, ballot, gavel, pillars, cane, pickaxe, galley, litter, chains, lightning, heart, fist, mountain, elector_hat, foot_gout, bed, tent, ladder, crown_cracked, sack, book_open. Takma ad: `gun`=arquebus, `sun`=sun_disc (rehberdeki adlar). Sayfa: `out/frames/icons_extra_sheet.png`; çok metal: `icons_extra.sheet(keys, metals=(...), cols, size, out)`. 120/200/460 px ve 8 metalde okunuyor.

## 3. Bilinen kusurlar
- Eski 26 madalyada boyun çıplak/kesik kalır (medal.py'ye dokunulmadı); `medals` çekiminde eski+yeni yan yana (ör. juana+filip) yeni olan daha zengin görünür.
- Yüzler aynı profil şablonundan (burun/çene/dudak/alın parametreleri + saç/sakal/başlık farkı); ince yüz ayrımı sınırlı. ≤150 px'te sakal/kürk dokusu bulanır, silüet okunur.
- Sarlman: saç+sakal+taç yoğun (küçük boyutta saç/sakal kaynaşır). Mary (Macar): dul başlığı + beyaz fırfır yaka, çene bilerek açık.
- Simgeler: horse/arquebus/mountain stilize-naif; mountain (Potosí) piramide benzeyebilir; crown_cracked yalnız `imperial_crown` üstüne kırık çizgi ve kayma.
- Ana ajandan istek yok.
