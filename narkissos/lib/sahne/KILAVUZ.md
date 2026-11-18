# Sahne üretim kılavuzu (Narkissos ve Eko)

Set sahipleri için. Önce bunu, sonra `planlar.md`'deki genel kuralları ve kendi planlarını, sonra `lib/havuz.js`, `lib/cam.js` ve kapı kodunu (`kapi/vazo/nark.js`, `kapi/vazo/README.md`) oku. Kanal kuralları `CLAUDE.md`'de.

## Dosya düzeni ve sahiplik
- **SAHİP-1** (A–C, P001–P034): `lib/sahne/s1/{cam,havuz,nehir,kehanet,delfi,orman,friz,yanki,dag,yazi}.js`
- **SAHİP-2** (D–F, P035–P098): `lib/sahne/s2/{havuz,orman,yanki,dag,kehanet,yeralti,belge,yazi,dere,cam,friz,son}.js`
- Yalnız kendi `s1/` ya da `s2/` dosyalarına yaz. **Ortak dosyalara dokunma:** `lib/vazo/*`, `lib/film.js`, `lib/ilkel.js`, `lib/su.js`, `lib/cam.js`, `lib/havuz.js`, `lib/yer_tutucu.js`, `lib/main.js`, `film.html`, `render.js`, `planlar.*`, `timeline.js`, `tools/*`. İhtiyacını raporda "motordan istek" diye yaz; ortak bir kurucuyu değiştirmek istersen kendi dosyana kopyala ve set önekiyle yeniden adlandır.
- Genel adlar dosya önekiyle başlar: `s1havuz_…`, `s2belge_…` (bütün betikler aynı küresel kapsamı paylaşır; `const` çakışması sayfayı durdurur). Tercihen her şeyi dosyadaki `(() => { … })()` içinde tut.
- Geçici dosyalar scratchpad'de. Commit yapma. `pkill -f`, `playwright install`, `NODE_PATH` yok.
- Plan listesi değişirse (başkan) `python3 tools/iskelet_uret.py --denetle` her planın tam bir dosyada kayıtlı olduğunu denetler. Set dosyasında kaydı olmayan plan `lib/eksik` yer tutucusuyla oynar (konsolda uyarı).

## Çekim sistemi (`lib/film.js`)
```js
plan('P053', (ctx, st) => { /* sahne: baseT(ctx) zaten uygulanmış, mantıksal 1920×1080 */ },
  { over: (ctx, st) => { /* ekran yazıları, kamera dönüşümü olmadan */ }, tr: trOf('P053') /* varsayılan */, mb: 8 /* isteğe bağlı */, post: { tex: .3 } });
```
- `st`: `{ t (film zamanı), lt (çekim içi), d (süre), p (0..1), at, end, id }`. Çekim, bir sonraki planın çapasına kadar sürer.
- Çapalar anlatıma bağlı, **sabit saniye yazma**: `S('E04')` cümle başı, `Se('E04')` sonu, `Wd('E04', 'benim')` kelime başı (`Wd(id, w, n, true)` kelime sonu), `A('E04@benim+0.3')` plan yazımı, `PA('P053')` planın başı, `PE('P053', 1)` planın 2. eyleminin zamanı (planlar.json `eylem[1].at`). Eylemleri `PE` ile bağlamak plan listesiyle tutarlılığı garanti eder.
- Zaman çizelgesi değişebilir (`vo/oneri/timeline_oneri.js` uygulanırsa 27 cümlenin sınırı kayar). Bu yüzden her olay kelimeye bağlanır; çekim içinde `st.lt` ile saniye saymak yerine `st.t - Wd(…)` kullan.
- Geçiş: `trOf(id)` planlar.json'dakini verir. `normTransitions` aynı set içindeki fade'i kesmeye çevirir, setler arası fade'i ≤ 0,7 sn yapıp sessizliğe kaydırır. Fade bu filmde **eşikli çözülmedir** (iki kare saydamlıkla karışmaz, gri ara kare yok). Ayrıca `black`, `white` (beyaz zemin hatıraya), `bloom` (`{cx, cy}` merkezinden açılır). Bir fade'i bilerek korumak: `tr: { …trOf(id), keep: true }`.
- Hareket bulanıklığı render'da her karede 4 alt kare (180°). Çok hızlı harekette çekime `mb: 8–12`. Alt kareler kesmenin öbür yanına taşmaz.
- Son işlem (kil dokusu, vinyet, gren) otomatik; beyaz zemin ve belge planlarında `post: { tex: .25, vig: .5 }` gibi hafiflet.

## Ortak ilkeller (imzalar; ayrıntı dosyalardaki yorumlarda)
**Kamera ve katman** (`lib/ilkel.js`): `camAt(ctx, fx, fy, z)` · `camMix(a, b, u)` ([fx,fy,z] arası) · `slowZoom(ctx, st, fx, fy, z0, z1)` · `layer(ad)` (temiz ara tuval) · `jointPt`.
**Zemin ve doğa:** `glaze(ctx, gx, gy, gr, warm)` (siyah sır + alttan sıcak ışık) · `whiteGround(ctx, o)` (lekythos hatıra zemini) · `waterBody(ctx, clip, wy, t, o)` · `shoreLine` · `farBank` · `ledge(ctx, xe, gy, wy)` · `crag(ctx, pts, o)` (world.js) · `vaseTree(ctx, x, y, s, seed, t, {branches, reach, fill, ink})` · `groundBand` · `grass` · `narcissus(ctx, x, y, s, t, seed, {dir, h, tilt, open})` (`open` 0 tomurcuk → 1 açık; P074 açılma) · `motesN(ctx, t, n, seed, cx, cy, rx, ry, a)` (P065 ışık noktaları) · `meander(ctx, x0, x1, y, h, col, bg)` (style.js) · `column(ctx, x, y0, y1, w, col, inc)` (env.js).
**Figür:** `figure(ctx, f)` (vazo motoru) · `litFigure(ctx, f, {x, y, r, c:'rgba(…,A)', a, dark})` (alttan ışıklı; `f.layerA` saydamlık, P065 incelme için) · `joints(ctx, f)` → `{J, M}` · `headPt(ctx, J, M, EYE_Q)` (göz) · `placeNeck` · `proneFig(px, gy, s, p, o)` + `pPose(o)` (yüzüstü uzanma; diz çökme yok) · `LK_NK` (Narkissos: efeb başı, khiton) · `LK_MOD` (bugünün genci) · `walkScene` (walk.js) · `spear`. Yürüyen/koşan figürde `araclar/hareket/` (ayak kaymaz) önerilir.
**Su** (`lib/su.js`): `mirror(ctx, drawFn, wy, clipFn, t, {a, dx, calm, rings, warpBox, calmAt})` · halka nesnesi `{x, y, t0, A, sq, v, lam, k, reach, life, shear, noLines, mask}` · `warpRings`, `ringLines` · `refLag(t)` (yansıma gecikmesi kuralı) · `refLock(t)` · `withFigT(tt, fn)` (yansımayı geçmiş zamanın göz kırpmasıyla çizmek).
**Cam** (`lib/cam.js`): `phoneScene(ctx, t, {...PH3, m, cam, light, refA, thumb, feed, feedA, headNod, rings})` · `thumbFlick(t, [zamanlar])` · `feedOffset` · `glassGlare` · `phoneFeed` · `phoneHand` · biçim dönüşümü `morphPts(A, B, m)`, `roundRectPts`, `ellipsePts` (ilkel.js).
**Havuz kurucuları** (`lib/havuz.js`; kapı planları B, C, D):
- `havuzGenis(ctx, t, {cam, fig, trees, nerg, refA, rings})` + `avciYuru(c, t, {tA, tStop, tLean0, tLean1})`
- `kiyiOrta(ctx, t, {cam, look, reach, smile, lag, refA, rings, pose: tt => ({look, reach})})`
- `yakinYuz(ctx, t, {T: {son, ben, tear, hit, lean0, sad1}, cam, lag, refA, rings, noBank, noTear, handOff, pose})` → `{f, eye, reye}`. T'de verilmeyen olay olmaz (ör. `T.hit` yoksa damla ve halka yok).
**Yazı** (`lib/film.js`, yalnız `over` içinde): `txt(ctx, s, x, y, {px, font, col, align, ls, panel})` · `quote(ctx, s, x, y, st.lt, {px ≥ 64, t0, per, kaynak})` · `etiket(ctx, s, x, y, st.lt, d)` · `kunye(ctx, s, st.lt, d)` (sol alt, y ≈ 846) · `buyukSoz(ctx, 'O benim.', st.t, Wd('E04','benim'))` (Bebas, kırmızı) · `FONT.baslik/alinti/metin/buyuk` · `YAZI.krem/kil/kirmizi/sepya`. `txt`/`quote` merkezi y > 880'i aşacaksa kendiliğinden yukarı iter.
**Sahnenin parçası olan yazı** (draw içinde, `notext`'te de kalır): `dipintoYaz(ctx, 'ΝΑΡΚΙΣΣΟΣ', x, y, h, p)` (Yunan fırça harfleri) · `txtDipinto(ctx, 'KENDİNİ TANIMAZSA', x, y, px, p)` (Türkçe dipinto).
**Görseller:** `gorsel('tempesta1606.jpg')` (Image) · `belgeCiz(ctx, ad, x, y, w, h, {frame, pad, mult, a})`. Liste ve lisans `kaynak/GORSELLER.md`. Dosyalar: `tempesta1606.jpg`, `callot1646_resim_satir.jpg`, `callot1646_satir.jpg`, `callot1646_resim.jpg`, `ellis1898_satir.png`, `ellis1898_iki_satir.png`, `ellis1898_sayfa_basi.png`, `freud1914_s1_ust.jpg`, `freud1914_s1_baslik.jpg`, `freud1914_s1_tam.jpg`.
**Yer tutucu:** `yt(id)`, `ytYazi(id)`: henüz çizilmemiş plan; ölçeğe göre kadraj, eylem anında halka çakması, üstte plan kartı.

## Kurallar (planlar.md "Genel kurallar"; her plan)
- **Ölçek:** plan listesindeki ölçeğe uy; ardışık iki plan aynı ölçekte değil (sınırdaki komşunu başka sahip çiziyorsa kurgu özetinde birlikte bak).
- **Donuk plan yok:** her plan ilk saniyeden hareketli (yavaş kamera + su, ot, ışık kıpırtısı) ve eylemleri sözcüğe bağlı. Kamera: kaydırma ya da yakınlaşma; yakınlık değişimi ≤ %10, yumuşak.
- **Yansıma gecikmesi (tek kural):** D03'ten (P038) E04 'benim'e (P053) kadar yansıma 9 kare geç izler; A bölümü havuz planları da (tanınmadan önce). Kullanım: `const lag = refLag(t); mirror(ctx, c => withFigT(t - lag, () => figure(c, poz(t - lag))), …)`. 'benim'den sonra birebir. P004'te kilitlenme yok.
- **Gözyaşı halkası:** damla + halka + yüzün dağılması yalnız P062. P007'de esinti, P061'de yazı halkasız batar.
- **Hatıra dili:** P057 ve P060 beyaz zemin (`whiteGround`, `STY.white`, sepya çizgi).
- **Beden sürekliliği:** P065'ten itibaren beden incelir (renk solar, kenar yumuşar, ışık noktaları), P067, P068, P070 aynı beden; kayboluş P073, nergis P074.
- **Dipinto dili:** konuşma dipintosu Türkçe; Latince yalnız künyede; Yunanca yalnız ad etiketleri ve Delfi taşı.
- **Hassasiyet:** secde, dört ayak üstü, diz çökme yok; hale (başın çevresinde halka ya da ışık; halka çizgilerine `mask`, ilk halka baştan ≥ 60 px), haç, altı köşeli yıldız (nergis yandan basık çizilir) yok; çıplaklık yok (khiton uyluk ortasında); Eko baştan ayağa örtülü değil, yüzünü yapraklarla örter; ruh sağlığıyla alay yok; telefon bölümünde ahlak dersi yok; Juno ve öç tanrıçası figürle çizilmez (ışık, tavus kuşu simgesi). Dudak teması ve "öpüşme ekseni" yok.
- **Yazı:** ekran yazısı ve künye y ≤ 880 (alt bant altyazının); x 120–1800; alıntı ≥ 64 px, etiket/künye ≥ 40 px; yazı metinleri planlar.json `yazi` alanından (değiştirme, ekleme).
- **Belirlenimcilik:** `Math.random`, `Date.now`, `performance.now` yok; `rng(tohum)`, `hash`, `noise1/2`, `fbm1`. Parametre değişince çizilen parça sayısı ve sırası sıçramasın.
- **Hız:** mb=4 ile kare başına ≤ 1,2 sn (kapı D planı 1,1–1,3 sn). `warpRings` pahalıdır: `warpBox` ver, sönmüş halkayı `life` ile kapat.

## Deneme
```
node tools/kare.js /tmp/…/k P053 P053:0.2 benim=278.5 --mb=4        # tek kareler (planın ortası, oranı ya da saniye)
node tools/kare.js /tmp/…/k P053 --notext                            # ekran yazısız
python3 tools/kurgu_ozet.py /tmp/…/oz 0.5 --sec='P0(3[5-9]|4)'       # setinin kurgu özeti (her plandan bir kare, ölçek etiketli)
ANIMATIK=1 ARALIK=270-290 node /home/user/Animasyon-kahve-/narkissos/render.js /tmp/…/p053.mp4   # hızlı hareket denemesi (960×540, sesli)
python3 tools/donma.py /tmp/…/p053.mp4 0.9 0.8 1.0 --bas=270          # donma taraması
node -e "new Function(require('fs').readFileSync('lib/sahne/s2/havuz.js','utf8'))"   # sözdizimi
```
Raporunda: çizdiğin planlar, ölçülen kare süresi, kendi karelerine bakışın, hassasiyet notları, motordan istekler.
