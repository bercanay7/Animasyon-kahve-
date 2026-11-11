---
name: cizim
description: Canvas'ta çizim ve görsel stil — Rough.js elle çizilmiş görünüm, Lucide/Tabler ikonları (SVG→Path2D), fontlar (Baloo 2, Patrick Hand), renk/kompozisyon kuralları. Yeni karakter, nesne, arka plan veya ikon çizilirken kullan.
---
# Çizim

Kütüphaneler `araclar/vendor/` içinde (bkz. araclar/vendor/README.md), fontlar `araclar/fonts/`. İnternetten yeni varlık eklemeden önce `lisans-kontrol` skill'ini oku.

## Rough.js (MIT) — elle çizilmiş görünüm
```js
const rc = rough.canvas(cv);
rc.rectangle(x,y,w,h,{fill:'#E17610',fillStyle:'solid',stroke:INK,strokeWidth:6,roughness:1.6,seed:boil});
```
**Boil** (çizgi titremesi): `seed = Math.floor(t*8)+1` → saniyede 8 farklı titreşim. Seed sabit değilse her kare rastgele olur → mutlaka seed ver.

## İkonlar (Lucide ISC, Tabler MIT)
SVG `<path d>` değerini `new Path2D(d)` ile al, `ctx.scale(boyut/24)` + `ctx.stroke(path)`; stroke-width 2, round cap/join. Yeni ikon: `npm i lucide-static` (geçici dizin) → `araclar/vendor/icons/` + README tablosu.

## Fontlar (OFL)
Baloo 2 800 (başlık, yuvarlak), Patrick Hand 400 (el yazısı). Her `@font-face`'te latin + latin-ext ayrı `unicode-range` (ş ğ ı İ için latin-ext şart). Büyük harf `İ`/`ı` için canvas'ta `toUpperCase()` yerine `toLocaleUpperCase('tr')`.

## Stil kuralları
- Kalın dış çizgi (5-8 px) + düz dolgu; 4-5 renkli palet; marka rengi baskın (Navitas: #E17610, #202F50).
- Her karede tek odak; okunurluk: başlık ≥ 120 px (1080p), kontrast yüksek.
- Gölge = aynı şeklin 8 px kaydırılmış koyu kopyası (flat, blur yok).
- 16:9'da güvenli alan: kenarlardan %5 içeride.

## Geçiş/efekt tarifleri (canvas'ta kendimiz yazarız)
zoomBlur (merkezden alt-kare ölçek ortalaması), rgbSplit (R/G/B kanalları farklı ofsetle çiz, `globalCompositeOperation='lighter'`), clockWipe (`arc` ile kırpma maskesi), lightLeak (sıcak renkli radial gradient, `screen` blend), pixelate (küçük canvas'a çiz, büyüt, `imageSmoothingEnabled=false`). Çizgi kalınlığı ≥ 2 px (küçük ekranda kaybolmasın).
Kaynak fikirler: claude-code-video-toolkit (MIT), anthropics/skills slack-gif-creator (Apache-2.0).
