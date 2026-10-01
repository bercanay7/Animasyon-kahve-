// Kare kare render: node render.js [çıktı.mp4]
// Gerekenler: Playwright (Chromium) ve ffmpeg.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const out = process.argv[2] || 'dunya-kahve-gunu.mp4';
const only = process.env.FRAMES; // örn. FRAMES=0,90,200 → sadece PNG kareler

(async () => {
  const browser = await chromium.launch(
    process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(__dirname, 'animation.html') + '?render=1');
  await page.evaluate(() => window.ready);
  const { DUR, FPS } = await page.evaluate(() => ({ DUR: window.DUR, FPS: window.FPS }));
  const mb = +(process.env.MB_SAMPLES || 8); // hareket bulanıklığı alt kare sayısı (1 = kapalı)
  const grab = async t => Buffer.from((await page.evaluate(({ t, mb }) => {
    if (mb > 1) window.renderFrameMB(t, mb); else window.renderFrame(t);
    return document.getElementById('c').toDataURL('image/png').split(',')[1];
  }, { t, mb })), 'base64');

  if (only) {
    fs.mkdirSync('frames', { recursive: true });
    for (const f of only.split(',').map(Number)) {
      fs.writeFileSync(`frames/f${String(f).padStart(4, '0')}.png`, await grab(f / FPS));
    }
    await browser.close(); return;
  }

  const total = Math.round(DUR * FPS);
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    ...(fs.existsSync(path.join(__dirname, 'audio.wav'))
      ? ['-i', path.join(__dirname, 'audio.wav'), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000']
      : ['-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000']),
    '-map', '0:v', '-map', '1:a', '-shortest',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
    '-r', String(FPS), '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out],
    { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let i = 0; i < total; i++) {
    const buf = await grab(i / FPS);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 30 === 0) process.stdout.write(`\r${i}/${total}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log(`\nHazır: ${out}`);
})();
