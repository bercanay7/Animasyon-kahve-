---
name: render
description: Canvas animasyonunu kare kare MP4'e çevirme, deterministik zaman çizgisi (GSAP seek), hareket bulanıklığı, ffmpeg/YouTube export, altyazı yakma, thumbnail. Video render edilirken, export ayarı sorulurken veya yeni sahne yazılırken kullan.
---
# Render ve export

**Mevcut dosyalara (render.js, animation.html, audio.py) dokunma.** Yeni işler `araclar/` altında.

## Sahne sözleşmesi
Bir sahne HTML'i şunları sunar: `<canvas id="c">`, `window.ready` (Promise), `window.DUR`, `window.FPS`, `window.renderFrame(t)`, `window.renderFrameMB(t, n)`. `render(t)` YALNIZCA `t`'ye bağlı olmalı (Math.random, Date, performance.now yok → seed'li rastgele).
Referans: `araclar/ornek-sahne.html`.

## Render
```bash
NODE_PATH=$(npm root -g) SIZE=1920x1080 node araclar/render-sahne.js araclar/ornek-sahne.html cikti.mp4
# env: AUDIO=ses.wav  MB_SAMPLES=8 (1=blur kapalı)  FRAMES=0,30,60 (yalnız PNG → frames/)
```
Hızlı kontrol: önce `FRAMES=...` ile birkaç kare al, bak; sonra tam render.

## Deterministik zaman (GSAP)
`gsap.timeline({paused:true})`, her karede `tl.time(t)`. `gsap.ticker.lagSmoothing(0)`. Durum nesnesini (S) tween'le, çizimi S'ten yap. Fizik (matter-js) için sabit adımla önceden simüle et, kare dizisini sakla (örnekte `simulateBeans`).

## ffmpeg tarifleri
- YouTube: `-c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart -r 30|60`, ses AAC 192k 48 kHz.
- Ses: hedef -14 LUFS, TP -1.5 (`loudnorm`). Ölçüm için `ses` skill'i.
- Altyazı yakma: `ffmpeg -i in.mp4 -vf "subtitles=alt.ass:fontsdir=araclar/fonts" out.mp4` (ASS, UTF-8; font adı dosyadaki gerçek ad olmalı).
- Dikey Shorts: `SIZE=1080x1920`, sahne 9:16 yazılmış olmalı.
- Thumbnail: sahnenin tek karesi (`FRAMES=n`) 1280x720 PNG; ya da Playwright ile HTML→PNG. <2 MB, yüz/ana nesne büyük, 3-4 kelimeyi geçme.

## Sık hatalar
Font yüklenmeden render (→ `document.fonts.load` + `ready` bekle, Türkçe test cümlesiyle: `AaİıŞşĞğÜüÖöÇç`); `toDataURL` için canvas CSS boyutu değil width/height attr belirler; alt-kare blur render süresini n kat artırır.
