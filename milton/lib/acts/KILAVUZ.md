# Sahne üretim kılavuzu (Milton: Kayıp Cennet)

Bu dosya bölüm sahnelerini yazan ajanlar içindir. Önce bunu, sonra `animatik/planlar.json`'daki kendi planlarını, sonra `lib/sahne/gol.js` (onaylı üslup karesi) ve `lib/film.js` dosyalarını oku.

## Dosya düzeni ve sahiplik
- Her bölüm tek dosya: `lib/acts/sNN.js` (NN = bölüm sırası, 00–12). Yalnız kendi dosyana ve gerekiyorsa `lib/sahne/<set>.js` adlı kendi set dosyana yaz. Ortak dosyalara (`gravur.js`, `prim.js`, `siluet.js`, `kanat.js`, `film.js`, `main.js`, `film.html`, `planlar_kaynak.py`) dokunma; ihtiyacını raporda "motordan istek" diye yaz.
- Geçici dosyalar scratchpad'de, adında bölüm kodun olsun. Commit yapma. `pkill -f`, `playwright install`, `NODE_PATH` yok.
- Dosyan yüklendiğinde yalnız `plan(...)` çağrıları ve kendi yardımcı işlevlerin çalışır. Genel adlar bölüm önekiyle başlar (`s03_...`); başka bölümün adıyla çakışma.

## Çekim sistemi (`lib/film.js`)
```js
plan('P016', (ctx, st) => levha(ctx, cam, () => { /* dünya koordinatında çizim */ }, [zeminTonu, taramaAçısı, üslupKimliği]),
  { tr: { type: 'cut' | 'fade' | 'black' | 'paper', dur: 1.0, end: true }, over: (ctx, st) => { /* ekran yazıları */ } });
```
- `st`: `{ t (film zamanı), lt (çekim içi zaman), d (çekim süresi), p (0..1), at, end }`. Çekim, plan listesindeki bir sonraki planın çapasına kadar sürer.
- Çapalar anlatıma bağlıdır: `S('B04')` cümle başı, `Se('B04')` sonu, `Wd('B04', 'kelime')` kelime zamanı, `A('B04@kelime+0.3')`. **Hiçbir saniyeyi sabit yazma**; çekim içi olayları `st.lt` yerine mümkün olduğunca `st.t - Wd(...)` ile kelimeye bağla (bir çekim yeniden seslendirilecek, süreler birkaç saniye oynar).
- Kamera: `{ cx, cy, z }` (ekran merkezine gelen dünya noktası, yakınlık). `camLerp(a, b, p)` ile yumuşak hareket. **Varsayılan hareket yatay kaydırmadır** (yatay tarama çizgileri değişmez; sıkıştırma ve çizim hızı için en iyisi). **Yakınlık değişimi en çok %10, en az 6 sn, başta ve sonda yumuşak** (A04 kurulu: 1,25 → 1,0 geri çekilme çizgileri pompaladı ve bit hızını 7–9 Mbps'e çıkardı). Daha yakın kadraj için sahneyi o ölçekte çiz ve kes. Kaydırma ya da yakınlaşma; ikisi birden değil.
- Siyahtan ya da karanlıktan açılış saydamlıkla yapılmaz (gri geçiş baskı dilinde yok): sahne ışıkla açılır (baskıdan önce ton katmanı `multiply` ile karartılır; önce odak açılır, çizgiler kalınken incelerek belirir).
- Geçiş: bölüm içi `fade` (0,6–1,0 sn) ya da `cut`; bölüm başı `black` (1,2–1,6 sn, `end: true`); cennete giriş `paper`.
- Yazılar `over` içinde, baskıdan sonra çizilir: `chapterCard(ctx, 'BAŞLIK', 'soru', lt, süre)`, `quote(ctx, '“…”', x, y, lt, { t0, kaynak: 'KAYIP CENNET · IV. 75' })`, `etiket(ctx, 'ABDIEL', x, y, lt, süre)`, `txt(...)`. Yazı metinleri `planlar.json`'daki `yazi` alanından; değiştirme, ekleme (alıntılar kurul onaylı). Telefon kuralı: alıntı ≥ 64 px, etiket ≥ 40 px; yazı x 120–1800, y 90–880 (alt bant altyazıya ayrılır); yazı parlak ya da çok taralı zemine gelmesin (arkasındaki yumuşak koyu zemin yeterli olmalı).
- Tek çekim denemek için: `SCENES` yerine doğrudan film zamanıyla kare al (aşağıda).

## Çizim motoru
- `GR` (gravur.js): ton katmanı `GR.tx` (1 = kâğıt, 0 = mürekkep; `GR.tone(v)`), tarama yaması `GR.px`. `GR.fill(path, ton, { th, id })` ikisine birden basar. Koyuluk ~%93 üstü düz siyah, ~%7 altı temiz kâğıt; arası çizgi kalınlığıdır. `GR.frame(x, y, açı, yan, ölçek)` / `GR.unframe()` yerel çerçeve. Üslup kimlikleri: 0 genel, 1 gök, 2 bulut, 3 alev, 4 kaya, 5 ten, 6 tüy, 7 ışın, 8 su, 9 zırh.
- `PR` (prim.js): `cloud`, `smoke`, `flame`, `flameBank`, `rock`, `shafts` (ince huzmeler), `cuts` (kenar vuruşları), `glow`, `lake`, `chain`, `rays` (yalnız `slit` için).
- `SF` (siluet.js): `SF.rig({ x, y (kalça), h (baş boyu), facing, twist, lean, head, shTilt, armN, armF, legN, legF })` → eklemler; `SF.draw(J, { lum, lit, t, cloak, robe, legs, skirt, waterY, spear, lines, eye, wind, seed })`. `lum`: 1 ışıklı … 0 düz siyah siluet (plan listesindeki `lum` değerini kullan).
- `KN` (kanat.js): `KN.feathered({ span, open, lift, droop, ruin, dark, rim, root, anchor, lit, t, seed })`, `KN.bat(...)`; `GR.frame` içinde, omuz kökünde (bkz. `gol.js`).
- Rastgelelik yalnız `rng(seed)`, `hash`, `noise1/2`, `fbm1`; `Math.random` yok. Parametre değişince parça sayısı ve sırası değişmesin (sıçrama olmaz).

## Üslup dili (kurul onaylı; sapma)
1. **Üç değer:** düz siyah kütle, temiz kâğıt, ikisinin arasında yalnız geçişlerde seyrek kalın tarama. Gri, yarı saydam çizgi, bulanıklık yok.
2. **Cehennem tarifi (koyu sahneler: göl, kıyı, Pandemonium, kapı, Kaos):** koyu kütleler düz siyah; biçimi ışık yanındaki tek kenar ışığı ve **kütlenin içine giren, sivrilen, uzunluğu ve aralığı düzensiz beyaz vuruşlar** verir (kenara koşut "eko" çizgisi değil). Tarama yatay. Karede tek odak; odak karenin en parlak yeri (temiz kâğıt) ve figürün arkasında.
3. **Açık tarif (cennet, Aden gündüzü, çıkış, Nifates göğü; tur 2 sonrası bağlayıcı):**
   - Gökte eş merkezli halka YOK ("plak/hedef tahtası" gibi okunur, açık zeminde göz yorar). Işık merkezinin çevresi geniş temiz kâğıt; dışa doğru seyrek ışınsal tarama: `GR.hatch({ type: 'ray', cx, cy, n: 84–100, id: 10, w: 3 })`. Gök tonu .6'nın altına inmez.
   - **Beyaz figür her zaman koyu bir kütlenin önünde durur; koyu figür açık zeminin önünde.** Açık zemin üstünde konturla ayrılan beyaz figür yasak ("boyama kitabı").
   - **Ana figür ters ışıkta koyu siluettir** (`cen_aydin(..., { back: true })`: `KN.feathered` büyük kanat, kenar ışığı, beyaz iç vuruşlar); parlaklığını çevresindeki temiz kâğıt ve (başmelekte) alnının üstündeki sabah yıldızı anlatır. Işıklı figür yalnız ÇİZGİLİ olur (`plain` yok: tüy çizgili kanat, zırh eteği) ve koyu bulut kütlesinin önünde durur. İç çizgisiz düz kâğıt figür yalnız çok uzak, küçük figürde (Abdiel kalabalığın içinde) ve A02 eşleme kesmesinde. Saflar tek tek figür değil, baş-omuz yumrulu KÜTLE + seyrek mızrak. Koyu kütleler biçimsiz yumru değil, katmanlı bulut terasıdır (`cen_bulutKat`).
   - Açık karede yazı paneli (yumuşak koyu gölge) kullanılmaz: yazı temiz kâğıtta mürekkeple ya da koyu kütlenin üstünde kâğıt rengiyle.
   - Tanrı ve Oğul yalnız ışıktır. Örnek: `lib/sahne/cennet.js`, `lib/acts/cen.js`.
4. **Koyu piksel oranı hedefi** (parlaklığı 60'ın altındaki piksel): cehennem %65–75, geçiş sahneleri (oda, kitap, Nifates) %50–60, cennet ve Aden %30–45. Yüksek karşıtlıklı çizgili alan karenin %30–40'ını geçmesin.
5. **Alev:** her boyda kâğıt beyazı kütle + içinde sivrilen 2–3 mürekkep vuruşu (`flameBank` bunu kendisi yapar: `solidBelow: 500`); yay taraması yalnız kadrajı kesen en yakın alevde. Hız düşük (`speed` .5–.7).
6. **Çizgi:** en ince yer 2 px, uçlar küt; birbirine 8 px'ten yakın koşut çizgi yok. Tarama aralığı 9–12,5 px (motor ayarlı; değiştirme).
7. **Figür kullanımı:** Şeytan çoğunlukla orta ve uzak planda (h 50–110), kanat ve pelerinle sarılı koyu siluet. Yüz ve beden yakın planı yok; duygu duruşla (baş açısı, omuz, kanat) verilir. Kalabalık saflar üst üste binen sıralar hâlinde, uzaklaştıkça küçülür (aynı figürün eşit aralıklı kopyaları "oyuncak asker" gibi okunur); cennetteki melekler `robe` ile.
8. **Hareket:** az ama anlamlı. Durağan nesnenin çizgisi kıpırdamaz; hareket yavaş ve sürekli. Kare başına çizim ≤ 1,2 sn.

## Kırmızı çizgiler (hassasiyet ve hukuk; istisnasız)
1. Tanrı ve Oğul figürle çizilmez; ışıkta yüz, el, hale, haç yok.
2. Âdem ile Havva yalnız uzak, örtülü siluet (kadrajın en çok %15'i), çoğunlukla arkadan; yüz yakın planı, çıplaklık, sarılma ya da öpüşme yok.
3. Günah figürü örtülü siluet; II.760–814 görsele girmez.
4. Pandemonium Dor sütunlu, altın tavanlı bir tapınak; kubbe, minare, hilal, sarık, Arap harfi, Osmanlı motifi yok.
5. Eğilme sahnelerinde (C04, E15, J07) secde ya da saf düzeni çağrışımı yok; Batı saray selamı.
6. Şeytan'ın bedeninde çıplaklık çağrışımı yok.
7. Cabanel yalnız gözler ve kollar; gövde görünmez.
8. Başkaldırı hiçbir dinî topluluk, Türk tarihinden figür ya da güncel siyasi hareketle eşleştirilmez; taht ve şeytanlar hiçbir etnik ya da dinî topluluğa benzemez.
9. Gerçek kişiler (Milton, kızları, Cromwell, Blake, Lewis) gerçekçi portre olarak çizilmez; dönem silueti yeter.

## Sınama (her çekim için)
```bash
cd /home/user/Animasyon-kahve-/milton
node shot.js <scratchpad klasörün> <t1> <t2> ...     # film zamanı (saniye); çekim başı, ortası, sonu ve bir sonraki kare (t + 0.0333)
```
- Çekimin zamanını öğrenmek için: `node -e "..."` yerine `timeline.js`'i oku (`CUES`), ya da tarayıcıda `PA('P016')`.
- Her kareye Read ile bak; 640 ve 427 px küçültmesine de bak (telefon). Kendine sor: ne anlatıyor, odak nerede, ucuz duran bir yer var mı, kırmızı çizgi var mı?
- Ölç: ardışık kare farkı (hareketsiz bölgede ~0), koyu piksel oranı (hedefe uygun mu), kare başına süre.

## Rapor
Çekim çekim tek satır (plan kimliği, ne çizildi, bilinen zayıflık), kare yolları, ölçümler, motordan istekler, plan listesinden saptığın yer varsa gerekçesi.
