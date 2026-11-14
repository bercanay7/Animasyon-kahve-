# Hareket kılavuzu: yürüyüş, yay, sarkaç (araclar/hareket/)

Kaynak: [JDhruv14/line-art-animation](https://github.com/JDhruv14/line-art-animation) (MIT, commit c43d698, 10 Kasım 2026). `lib/gait.ts` ve `lib/motion.ts` düz JS'ye uyarlandı. Özgün dosyalar ve lisans `araclar/vendor/line-art-animation/` klasöründe, başvuru için duruyor.

**Neden:** CLAUDE.md'ye göre kodla çizimin zayıf yanı "karmaşık beden hareketi". Şimdiye kadar yürüyüşler elle kuruluyordu: Sisifos'ta Camus sabit hızla kayıyordu, Milton'da `walk: true` yalnız duran bir pozdu. Bu çözücü ayak kaymasını matematiksel olarak sıfırlıyor (`test.js`: 10⁻¹³ px).

**Mevcut motorlara dokunmaz.** Tek bir global tanımlar (`HAREKET`), `core.js` ile çakışmaz. Bir filmde kullanmak için `film.html`'e bir satır eklenir:
```html
<script src="../araclar/hareket/hareket.js"></script>
```

## Dosyalar
| Dosya | Ne |
|---|---|
| `hareket.js` | `yuruyus`, `yuruyusYolu`, `yayIzi`, `sarkacIzi`, `ivme`, `sira`, `kipir`, `tohumlu`, `yerlestir`, `diz` |
| `ornek.html` | Siluet figür yürür, durur, selam verir, yürümeye devam eder; kollar yayla, çanta sarkaçla hareket eder. Sözleşmesi `render-sahne.js` ile aynıdır. |
| `serit.js` | Figürü izleyen büyütülmüş kare şeridi. **Her sahnede çalışır** (milton, ikaros, sisifos…). |
| `test.js` | `node araclar/hareket/test.js` ile çalışır. Ayak kayması, kalça inişi, durma, determinizm, yay ve sarkacı sınar. |

## Figür uzayı
- Ayaklar y = 120'de, kalça x = 40'ın üstünde; figür +x'e bakar ve boyu ≈ 95 birimdir.
- `HAREKET.yerlestir(ctx, x, zeminY, yon, olcek)`, (40, 120) noktasını sahnede (x, zeminY)'ye koyar.
- Bütün ölçüler (`AYAR` içindeki adım, kalkış, uyluk) bu uzaya göredir. Bizim figürlerimiz başka boydaysa ölçeği `olcek` ile ver, `AYAR`'ı değiştirme.

## Kullanım
```js
const g = HAREKET.yuruyus({ tip: 'yuru' });            // 'yuru' | 'surun' (uzun etek, chiton, yaşlı) | 'kos'
const go = t => HAREKET.rampa(t, 0, .5) * (1 - HAREKET.rampa(t, 3.2, 3.7));   // başla / dur
const yol = HAREKET.yuruyusYolu(g, { t0: 0, t1: DUR, x0: 260, yon: 1, olcek: 4.6, go });
// her karede:
const y = yol(t);       // { x, faz, go, hiz, poz: { kalca, ayaklar[0..1]{bilek, diz, egim, basiyor}, on, inis } }
```
- **Sözcüğe bağlamak:** `go`'yu `S()`/`Wd()` zamanlarıyla kur, ör. `t => HAREKET.rampa(t, Wd('B04','yürüdü'), Wd('B04','yürüdü') + .5)`.
- **x'i elle değiştirme:** hem faz hem x aynı `go` integralinden gelir; ayrı bir hız verilirse ayak kayar. Figürün daha hızlı gitmesi gerekiyorsa `adim` ya da `tur`'u değiştir veya tip olarak `kos` seç; zamanı sıkıştırman gerekiyorsa varışları sıkıştır, yürüyüşü değil.
- **Çizim sırası:** önce arka bacak (`1 - poz.on`, bir ton açık), sonra gövde ve kollar, en son öndeki bacak.
- **Giysi:** bacaklar görünmese de çözülür. Etek ya da pelerin `poz.ayaklar[poz.on].diz` ve iki bilekten çizilir; böylece adımla açılıp kapanır.

## Yay ve sarkaç: render'a uygun
Kaynaktaki `spring.step(dt)` durumludur, oysa bizim `render.js` kareleri 4 işçide sırasız çizer. Bu yüzden ikisi de **t'nin saf fonksiyonudur**: `t0..t1` arası 240 Hz sabit adımla bir kez simüle edilir, sonra okunur.
```js
const kol = HAREKET.yayIzi({ hedef: t => .42 * Math.sin(2 * Math.PI * yol(t).faz) * yol(t).go, k: 60, d: 9, t0: 0, t1: DUR });
const fener = HAREKET.sarkacIzi({ kuvvet: HAREKET.ivme(yol), k: 14, d: 1.6, t0: 0, t1: DUR, itmeler: [[Wd('C03','rüzgâr'), 1.5]] });
```
- **Yay** (kol, dirsek, kanat ucu, pelerin, saç): `k` sertlik, `d` sönüm. Ağırbaşlı hareket için k 40–60, d 6–9.
- **Sarkaç** (fener, çanta, kandil, zincir halkası, asılı tabela): `kuvvet(t)` = rüzgâr + taşıyanın ivmesi; vuruş için `itmeler: [[t, hız]]` kullan.
- **Kural:** asılı ve bağlı her şey bir yay ya da sarkaçla hareket eder. Serbest dönen sinüs ancak `kipir` gibi katmanlı ve küçük boşta salınımlarda kabul edilir.

## Denetim: animatör gözüyle (kurgu kuruluna kanıt)
```bash
node araclar/hareket/serit.js araclar/hareket/ornek.html serit.png 1.0 2.0 8
```
```bash
node araclar/hareket/serit.js milton/film.html nif.png 640 642 9 --odak 960,620 --kutu 600x700
```
- Odak sırası: `--odak x,y`, yoksa sahnedeki `window.SERIT_ODAK(t)`, o da yoksa kare ortası.
- Şeritte bakılacaklar:
  - basan ayak yerinde mi (zemine çentik koy);
  - kalça basışta iniyor, geçişte yükseliyor mu;
  - öndeki bacak üstte mi;
  - kol ve çanta gecikip oturuyor mu;
  - kareler arasında sıçrama var mı.
- Şerit, kurula verilen "yaptım" iddiasının kanıtıdır (CLAUDE.md: iddia kare ya da ölçümle verilir).

## Kaynaktan alınan, araçta olmayan kurallar
- **Hareketi ölçmek:** bir başvuru klibine "aynısı" deniyorsa zamanlama tahmin edilmez, ölçülür (`vendor/line-art-animation/references/matching.md`, `scripts/clip.ts`). Değişken kare hızlı kliplerde süreye göre örnekle (`-vf fps=30`).
- **Etkileşim değil tepki:** dünya tepki verir. Selam verirken önce dur (`go` ~0,4 sn'de 0'a iner), sonra jest yap, sonra devam et. Tipik süreler: selam 2,6 sn, şapka çıkarma 1,6 sn.
- **Yeni demek yeni:** başvurudaki karakter kopyalanmaz; ortam ve zamanlama hissi korunur.
- **Ölçek kontrolü:** yetişkin ≈ saniyede 2 adım; takunya ya da uzun etekte adım daha kısa ve alçak; koşan çocuk ≈ saniyede 4 adım, öne eğik.
