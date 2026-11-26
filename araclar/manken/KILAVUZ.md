# manken-cizim: 3B manken + çizim gölgelendiricisi (`araclar/manken/`)

Yön metni ve başvurular: `kanal/motorlar/manken-cizim.md` (r8 gri kuru fırça storyboard, r1 ışık kamaları). Kapı sonucu ve dersler: `geriye_bakis.md`.

**Kural:** biçimi ışık kurar, çizgi değil.
- Ton iki-üç sert basamaktır; geçişi yumuşatma değil fırça sürtmesi verir.
- Karanlık kütleler birbirine karışır; kenar yalnız ışığın değdiği yerde belirir.
- Işık bir kama ya da konidir.

**Ne yapar:** anatomiyi, perspektifi ve gölgeyi kodla kurulmuş bir 3B manken verir; elle çizilmiş görünümü tek bir gölgelendirici zinciri verir. Kütüphane yok (düz WebGL2), dış model ya da doku yok.

## Dosyalar
| Dosya | Ne |
|---|---|
| `iskelet.js` | Saf matematik (tarayıcı + node): ölçüler, poz → kemik çerçeveleri, iki kemikli 3B ters kinematik, `yuruyus3B` (araclar/hareket çözücüsünü 3B'ye taşır), `karistir`, poz kütüphanesi `POZ.dur / egil / oku` |
| `manken.js` | WebGL2 çizim: gölge haritası → ana geçiş (ışık, fırça, basamak) → son işlem (palet, kontur, saçak, plakalar, gren). Global `MANKEN` |
| `deneme.html` | Üslup kapısı sahnesi: manzara (0–5 sn), 15 sn hareket (5–20), yakın plan (20–25). `?sahne=`, `?poz=dur|egil|oku`, `?bas=1` taramaları |
| `test.js` | `node araclar/manken/test.js`: ayak kayması (2B `test.js` ölçütü), kemik boyları, diz yönü, zemin, belirlenimcilik, pozlarda el omuzun altında |
| `kare.js` | Tek kare PNG + çizim/kodlama süresi ayrı ölçümü (SwiftShader, yerel http) |
| `render.js` | Dört işçili kare kare MP4 (mutlak yolla başlat) |
| `alt_bant.js` | Sahne boyunca bütün yazı çağrılarının y'sini ölçer (y > 880 yasak) |

## Kullanım (film.js çekimi içinde)
```html
<script src="../araclar/hareket/hareket.js"></script>
<script src="../araclar/manken/iskelet.js"></script>
<script src="../araclar/manken/manken.js"></script>
```
```js
MANKEN.init(1920, 1080, { rs: RS });                       // bir kez (main.js'te)
plan('P04', (ctx, st) => {
  const M = MANKEN, I = ISKELET;
  M.begin({ palet: 'r8', t: st.t, ortam: .14,
    isik: { tip: 'yon', konum: [-7.5, 4.3, -1.3], hedef: [.2, .5, -.2], alan: 6, uzak: 24 },   // ya da {tip: 'spot', aci: 30, ...}
    kamera: { konum: [1.6, 1.45, 5.4], hedef: [0, 1, -.4], fov: 40 } });
  M.kutu([0, -.05, 0], [14, .1, 14], { ton: .3 });        // set: kutular (merkez, boyut, {ton, don, kim})
  M.figur(I.POZ.dur([0, 0], Math.PI), { gozluk: true });
  M.l.font = '48px Courier Prime'; M.l.fillText('1971', 120, 140);   // 2B plakalar: k koyu, l mürekkep/yazı, a ışık (siyah zemine beyaz)
  M.ciz(ctx);
});
```
- **Sözcüğe bağlama:** yürüyüşün `go`'su, eğilme ve baş kaldırma yayları `S()` ve `Wd()` zamanlarıyla kurulur (`deneme.html`'de `yBas`, `tEg0`, `tBak`).
- **İkişer çizim:** figür pozu `floor(t·15)/15` ile örneklenir, kamera 30 kare/sn akar. Fırça tohumu da iki karede bir değişir. Hareket bulanıklığı yok.
- **Belirlenimcilik:** `Math.random` yok; aynı t her işçide aynı kare.
- **Yürüyüş:** `HAREKET.yuruyusYolu(g, {x0: 0, olcek: 1, go})` + `ISKELET.yuruyus3B(yol, t, {bas: [x, z], yaw})`. x'i elle değiştirme; hız ve faz aynı integralden gelir.

## Görüntünün ayarları
- `palet`: `'r8'` (nötr gri, beyaz yalnız ışık lekesi, kâğıt ve parıltı) ya da `'r1'` (tek sıcak aile, saf siyah ve beyaz yok) ya da `{p: [4 renk], m, par}`.
- Basamaklar: değer = ton × (ortam + ışık × kazanç). `esik [kara, koyu]` varsayılan `[.045, .16]`, orta→ışık eşiği koyu × 2,6.
  - Işıksız yüzeyin değeri (ton × ortam) bir eşiğin dibine düşmemeli; düşerse yüzey karlanır.
  - Ölçü: duvar `ton .42`, `ortam .14` → koyu gri; zemin `ton .3` → kara.
- Figür: giysi `ton .07` (ışıkta koyu gri, gölgede kara), ten `yuz .19` (ışıkta orta gri). Beyaz figürde yok.
- `firca` (eşik bozma), `kuru` (orta tonda düşey kıl izi, nesne uzayında), `surtme` (koyu kütlenin alt kenarından sarkan saçak), `kontur`, `gren`, `vinyet`, `gok` (arka plan basamağı 0–3).

## Kurallar (kapıdan çıkan)
- **Yüz:** hiçbir zaman önden tam ışıkta gösterilmez. Yalnız ¾ gölgede (ışık yanı düzlem, öbür yan karanlığa karışır) ya da profil siluetinde. Önden aydınlık figür ressam mankeni okunur (`?poz=dur`).
- **Tek ışık.** İç mekânda pencere kaması ya da yan lamba. Masanın tepesinde tek lamba ve karşısında ikinci kişi kurulmaz (sorgu odası).
- **Sokak lambası düz direk:** L kol ve sarkan lamba darağacı okunur.
- **Pencere kayıtları yalnız dikey:** kesişen dikey + yatay kayıt yerde haç gölgesi bırakır.
- **Gözlük ince çerçevedir.** Cam yalnız parıltı olarak görünür; opak koyu cam güneş ya da aynalı gözlük okunur. Parıltı iki camda aynı yönde, kısa, sıcak (`par` rengi); ayna simetrisi "öfkeli kaş" yapar.
- **Işık kaynağı gölge haritasının içinde kalmaz:** lamba başını ve direği `golgeYok` ile işaretle. Işık noktası bir kutunun içinde kalırsa her şey karanlıkta kalır.

## Ölçümler (SwiftShader, 4 çekirdek; 26 Kasım 2026)
- Tek işçide kare: 0,17–0,35 sn; ilk kare 0,3–0,47 sn (derleme).
- Dört işçi aynı çekirdekleri paylaşınca 0,9 sn/kare; duvar saati ≈ 2,9 kare/sn (25 sn sahne 4–4,5 dk). 10 dakikalık film ≈ 1 sa 45 dk.
- Bütçe (tek işçide ≤ 1 sn) tuttu; 15 kare/sn'ye gerek kalmadı.
- Hızlandırma gerekirse: `MANKEN.init(..., {olcek: .75})` ana geçişi küçültür; `smN: 512` gölge haritasını küçültür.

## Boya kipi (`kip: 'boya'`; 26 Kasım, kullanıcının örneklerinden)
Kullanıcı r8/r1 kalıbını bıraktı; gönderdiği örneklerin (geyik, iskambil, merdiven ve çerçeveler, satranç, orkestra, BMW) ortak dili bu kipte:
- **Renkli ışık:** sıcak ışık (`renkler.isik`), soğuk gölge (`renkler.golge`).
- **Hava:** sis (`sis`) ve gölge haritasında yürüyen ışık hüzmesi (`huzme`, `huzmeBoy`).
- **Işık saçan yüzey:** `isima`; çevresinde parıltı (`parilti`).
- **Gölgesiz renkli nokta ışıklar:** `noktalar: [{konum, yaricap, renk, guc}]`, en çok 8.
- **Toz:** hüzmede yanan zerreler (`MANKEN.toz(min, max, n)`, `toz`, `tozBoy`).
- **Fırça:** nesne uzayında renk ve değer oynayan darbeler.
- **Ton ayarı:** gölge mora, ışık altına; `doygunluk`.

Nesne rengi `renk: [r, g, b]`; figür `M.figur(poz, {giysi, pantolon, ten})`. Ana geçiş `olcek: .6` ile küçük çizilir (boyalı görüntü buna dayanır; SwiftShader'da hüzme pahalı).

Deneme: `kurye.html` (15 sn, kanal kimliği adayı). Karanlık salonda yürüyen kurye; soldaki pencerelerden altın hüzme; sağda her biri başka bir çağa açılan renkli kapı (gök + ufuk + tek siluet). Kurye bir kapının önünde durup ona döner.
- Ölçüm: tek işçide 0,85–1,2 sn/kare (bütçenin sınırında).
- Simge taraması: kapı siluetlerinde haç, minare, kubbe, hilal, yıldız yok; pencereler yalnız dikey boşluk.
- Baş: ense ve şakaklar saç kütlesidir. Arkadan bakınca ten bir yüz gibi okunuyordu.
