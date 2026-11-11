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

## Deterministik sahne kuralı (zorunlu)
Sahnedeki her şey zamanın saf fonksiyonu: `Date.now`, seed'siz `Math.random`, `setTimeout/setInterval`, ağ çağrısı, `repeat:-1` yasak. Kare sırasından bağımsız olmalı. Test: aynı kareyi iki kez (ve sıra değiştirerek) al, PNG özetleri (`sha256sum`) eşit olmalı.

## Teslim öncesi QA
1. **Contact sheet:** her 0.5 sn'den bir kare, tek görselde; kompozisyon/ritim bakışta okunur mu.
2. **Donma / ölü hareket:** 1 sn'den uzun süre hiç değişmeyen kare dizisi var mı (hook'ta asla).
3. **Ses-hareket hizası:** efekt vuruşu ile görsel vuruş aynı karede mi.
4. **Güvenli alan:** önemli öğe kare kenarlarından en az %5 (action-safe %90); altyazı title-safe %80 içinde.
5. Ses -14 LUFS, Türkçe karakter test cümlesi, ilk/orta/son karelere gözle bakış.
Kaynak fikirler: HyperFrames (Apache-2.0), claude-code-video-toolkit (MIT) — kendi cümlelerimizle.

## Not: bu repodaki iki render hattı
Asıl üretim hattı kökteki `render.js` (4 paralel Chromium işçisi, parça kalıcılığı, `Q=`/`AUDIO=`/`SHORTS=` env'leri; bkz. `sisifos/README.md`, CLAUDE.md). `araclar/render-sahne.js` yalnızca **küçük/deneme sahneler** için bağımsız yardımcıdır; Sisifos/Orfeus tarzı filmler için kökteki `render.js` kullanılır. Bu skill'in QA ve deterministiklik kuralları ikisi için de geçerli.
