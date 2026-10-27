# Sahne yapım rehberi

Bu dosya, sahne yazacak herkes içindir (alt ajanlar dahil). Önce `USLUP.md` (üslup şartnamesi) okunur, sonra bu dosya.

## Dosya düzeni
- `film.html`: betikleri sırayla yükler.
  - Sıra: `core` → `print` → `anim` → `people` → `props` → `film` → `ui` → `timeline` → `scenes` → `act*.js` → `main`.
  - Act dosyalarının yüklenme sırası önemli değildir; çekimler zamana göre sıralanır.
- `lib/actN.js`: her bölüm kendi dosyasındadır. **Bir ajan yalnız kendisine verilen act dosyasına ve o dosyaya özel yeni yardımcılara yazar.**
  - Ortak ilkellere (`print.js`, `people.js`, `props.js`, `ui.js`) dokunmaz. Eksik bir şey görürse kendi act dosyasında yerel bir yardımcı yazar.
- `timeline.js`: `window.CUES = {A01: {s, e}}` ve `window.WORDS = [{id, w, s, e}]`.
  - Seslendirme değişince yeniden üretilir.
  - Çekimler sabit saniyeye değil, **cümleye ya da kelimeye** bağlanır.

## Zamanlama
- `S('B03')`: cümlenin başladığı an; `Se('B03')`: bittiği an.
- `Wd('B03', 'idadi')`: o cümlede kelimenin başladığı an.
  - Kelime küçük harfle, şapkasız yazılır: `â→a`, `î→i`.
  - Kelimenin başı yeter; ör. `'darul'` Darülfünun'u yakalar.
  - `n` parametresi: n'inci geçiş. `end=true` verilirse kelimenin bitişi döner.
- `shot(at, (ctx, st) => {...}, { tr: { type, dur }, post: {...} })`: `at` anında başlayan çekim.
  - `st.t` mutlak zaman, `st.lt` çekimin yerel zamanı, `st.d` süresi, `st.p` 0..1 ilerlemesidir.
  - Geçiş tipleri: `press` (imza baskı merdanesi, 0,6–0,9 sn), `fade`, `black`, `cut`, `iris`, `wipe`, `clay` (gürültülü çözülme).
  - Bölüm girişleri `press`; bölüm içi geçişler çoğunlukla `cut` ya da kısa `press`.
- Çekimin ilk satırı **`setReg(tohum)`** olur; böylece her çekimin kayık baskısı sabit kalır.

## Çizim modeli (print.js)
- `paperBG(ctx)`: kâğıt zemin. Her çekim bununla başlar.
- `plate(ctx, 'ochre'|'khaki'|'red'|'navy'|'teal'|'gold'|'grey'|'sepia'|'skin'|'ink', yol, {a, n})`: renk kalıbını çarpma ile basar. `n:2` koyu ton verir.
- `knock(ctx, yol)`: nesnenin silueti kâğıt rengiyle doldurulur ve arkasındakini örter. Önce knock, sonra kalıplar, en son is.
- `inkStroke(ctx, yol, px)` ve `inkFill(ctx, yol)`: mürekkep. `cut(ctx, yol, px)` koyu kütle içinde kazınmış beyaz çizgi çizer.
- `halftone(ctx, kalıp, yol, yoğunluk, {cell, ang})` ve `radialHT(...)`: yarım ton. Yalnız durağan zemin, gök, deniz, duman ve haleye; **yüzlere ve hareketli figürlere asla.**
- Yol yardımcıları:
  - `SP(noktalar, kapalı, k)`: Catmull-Rom eğri;
  - `PL(noktalar)`: çokgen;
  - `rough(noktalar, genlik, tohum)`: sabit tohumlu kırık kenar.
- `txt(ctx, s, x, y, font, {align, ls, col, plate})` ve `scriptLine(ctx, sağX, y, uzunluk, yükseklik, tohum)`: soyut Osmanlıca yazı izi.
- **Çekimin sonunda bir şey yapma**: `post()` otomatik çalışır (`pressFinish`: taş greni, kâğıt lifi, vinyet, gren).
  - Ayar `shot(..., { post: { stone, grain, vig } })` ile verilir.

## Kişiler (people.js)
- `head3q(ctx, {x, y, s, dir, who, gear, gearCol, light, look, age, skin, tilt})`:
  - ¾ baş. `s` ölçektir: baş boyu ≈ 120·s px.
  - `dir:-1` sola bakar.
  - `who`: `'mk' | 'ismet' | 'fevzi' | 'karabekir' | 'alifuat' | 'rauf' | 'refet' | 'halide' | 'abdulhamid' | 'anon'`. Bu ortak kimlikler bütün bölümlerde aynı kalır; adı geçen kişiler için kendi kimliğini tanımlama. Anonim figür için `who:'anon'` ve gerekirse `id: {mus, hair, jaw, brow, ...}`.
  - Halide Edib: `who:'halide', gear:'carsaf'` (1919 mitingi) ya da `'basortu'` (Anadolu, haki ceketle).
  - Abdülhamid: `who:'abdulhamid', gear:'fes'`; kısa kırçıl sakal kimlikte tanımlı.
  - `gear`: `'kalpak' | 'fes' | 'kabalak' | null`.
  - `light`: `'front' | 'back' | 'top'`.
  - `skin: true` yalnız yakın planda kullanılır.
- `bust(ctx, {x, y, s, dir, coat:'kaput'|'setre'|'civil', col, w, len, seed})`: aynı x, y, s ile başın altına gövdeyi çizer. Önce bust, sonra head3q.
- `arm(ctx, omuz, el, {upper, fore, w, col, bend})` ve `handDraw(ctx, x, y, açı, s, 'point'|'rest'|'hold', {side})`.
  - El boyu kol ağzına göre: `handDraw(..., armSonucu.w2 / 20, ...)`.
  - Omuz ile hedef arası en çok `(upper+fore)·.85` olsun; dirsek 10–20° bükülsün, kol tam gerilmesin.
- **Kol pozları:**
  - `arkada`: `bust({arms:'back'})` ile kol çizilmez, kaput kolları yanlarda görünür.
  - `tutma`: ön kollar kaputun önünden çıkar; kök siluetin içindedir.
  - `işaret`: kol omuz ekleminden çıkar; işaret eden figürde `bust({w:.86})`.
- `bust` diğer seçenekleri:
  - `turn` 0..1: gövde bakış yönüne döner.
  - `sep:true`: öndeki figüre 8 px kâğıt ayırma konturu.
  - `back:true`: arkadaki figür koyu basılır.
- Onaylı şablon: `SCENES.alagoz` (lib/scenes.js) ve `board/tur4/kare_v4.jpg`. Yakın plan başlar: `board/tur4/baslar_v4.jpg`.
- **Dönem başlıkları:**
  - fes: 1880–1908 okul ve Selanik;
  - kabalak: 1911–18 cepheleri;
  - kalpak: 1919–23;
  - 1923 Çankaya'da sivil giyim, başı açık.
- **Saygı kuralları:**
  - Gerçek kişiler konuşturulmaz, ağızları oynamaz.
  - Kamera göz hizasındadır; alttan açı ve hale yok.
  - Mustafa Kemal kadronun içinde durur.
  - Kan yok. Kayıp, boş başlık ve boşalan sırayla anlatılır.

## Nesneler (props.js)
- `staffMap(ctx, {x, y, w, rot, front, arrows})`: Sakarya kurmay haritası. Döndürdüğü `toWorld(u, v)` harita yerel koordinatını ekrana çevirir.
- `gasLamp(ctx, x, y, s)`, `woodTable(ctx, y0)`, `binoculars`, `compass`, `paperSheet(ctx, x, y, w, h, rot, tohum, {rows, header})`.
- `stampOxcart(ctx, x, y, s, faz)` ve `stampWoman(ctx, x, y, s, faz)`: damga siluetler. Poz evresi `Math.floor(t*6)%2`.

## İzleyici katmanı (ui.js)
- `chapterCard(ctx, 'II', 'SELANİK', 'altyazı', lt, d)`: sol altta kâğıt künye kutusu.
- `nameTag(ctx, x, y, 'İSMET', '36 yaşında', lt, d, {align})`: kişinin ilk görünüşünde, yaşla birlikte.
- `stamp(ctx, 'ANKARA · 28 EKİM 1923', x, y, lt, d)`: daktilo damgası.
- `quote(ctx, metin, x, y, lt, d, {cite})`, `bigStamp(ctx, '600+', x, y, lt, d, {plate:'red'})`, `tickerTape(ctx, metin, y, lt, d)`.
- **Yazı kuralları:**
  - 1928 öncesi sahnelerin **içindeki** yazı (tabela, gazete, kitap, harita) Osmanlıca soyut yazı izidir (`scriptLine`).
  - Selanik'teki Fransızca ve Rumca tabelalar serbesttir.
  - Latin harfli yazı yalnız izleyici katmanında (`ui.js`) kullanılır. Büyük harf yüksekliği en az ~54 px.

## Palet (USLUP.md)
- Kâğıt, is ve en çok 3 renk kalıbı.
- **Kırmızı finale saklanır.** Finalden önce yalnız vurgu olarak (fes, cephe hattı, sancak) ve alanın en çok %15'i.
- Bölümlerin kalıpları:
  - I: sepya + vurgu kırmızısı;
  - II: turkuaz (deniz) + lacivert (gece);
  - III (1908): kırmızı/turkuaz/altın kartpostal bolluğu;
  - IV (savaş): haki + toprak (okra) + is;
  - V: okra + haki + gri;
  - 0 ve VI: hepsi.

## Kamera ve hareket
- `cam(ctx, {x, y, z, r}, k)`: k = paralaks derinliği (0 sabit, 1 tam). Yakınlaşma en çok %8; yavaş Ken Burns.
- **Pozlar ikişer karede değişir:** figür animasyonunda `const tf = Math.floor(t * 15) / 15;` kullan. Kamera ve geçişler 30 fps akıcıdır.
- Her çekimde **bir** odak noktası olur ve karenin en parlak noktası orasıdır.

## Performans ve test
- Bir kare `MB=1` ile 400 ms'yi geçmemeli. Yarım ton ve harita gibi durağan katmanlar çekim başına bir kez offscreen canvas'a çizilip önbelleğe alınır.
- Kare çekmek için: `node shot.js board/actN 12.5 20.0` (saniye listesi). Çıkan PNG'lere Read ile bak.
- Belirli bir cümlenin zamanını görmek için: `node -e "require('./timeline.js')"` çalışmaz. `timeline.js` içinde `"B03"` aranır.
- Hata konsolda `[err]` olarak görünür.
