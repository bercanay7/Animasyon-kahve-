# araclar/ — yeni animasyon araç kutusu

Mevcut dosyalara (animation.html, render.js, audio.py …) dokunmaz; yalnızca ekler.

- `vendor/` — GSAP, Rough.js, matter-js, Lucide ikonları (lisanslar vendor/README.md)
- `fonts/` — Baloo 2, Patrick Hand (OFL, Türkçe karakterli)
- `ornek-sahne.html` — 1920×1080, 4 sn çalışan örnek (zaman çizgisi + elle çizim + fizik + ikon)
- `render-sahne.js` — herhangi bir sahneyi MP4'e çeviren bağımsız render
- `ASSETS.md` — her varlığın lisans kaydı
- `hareket/` — yürüyüş çözücüsü, yay/sarkaç, kare şeridi (`KILAVUZ.md`; `node araclar/hareket/test.js`)
- `lemo/` — Lemo-Opuscar üslup kataloğu ve `getir.sh` (belgeler depoya kopyalanmaz)
- `ADAYLAR.md` — incelenen açık kaynak depolar ve kararlar
- `vendor/line-art-animation/` — hareket kütüphanesinin özgün kaynağı (MIT)

```bash
NODE_PATH=$(npm root -g) node araclar/render-sahne.js araclar/ornek-sahne.html ornek.mp4
```
Skill'ler: `.claude/skills/` → render, cizim, karakter, ses, yonetmenlik, lisans-kontrol.
