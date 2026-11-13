// Kare kare render: node render.js [çıktı.mp4]  (FRAMES=0,150,300 → yalnızca PNG kareler, MB_SAMPLES=1 → bulanıklıksız)
// Gerekenler: Playwright (Chromium) ve ffmpeg.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const out = process.argv[2] || 'cumhuriyet-103.mp4';
const only = process.env.FRAMES; // örn. FRAMES=0,90,200 → sadece PNG kareler

(async () => {
  const browser = await chromium.launch(
    { args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'], ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('console', m => m.type() === 'error' && console.error(m.text())); page.on('pageerror', e => console.error(e));
  await page.goto('file://' + path.resolve(__dirname, 'animation.html') + '?render=1');
  await page.evaluate(() => window.ready);
  const { DUR, FPS } = await page.evaluate(() => ({ DUR: window.DUR, FPS: window.FPS }));
  const mb = +(process.env.MB_SAMPLES || 8); // hareket bulanıklığı alt kare sayısı (1 = kapalı)
  const grab = async t => Buffer.from((await page.evaluate(({ t, mb }) => {
    const n = window.mbSamples ? window.mbSamples(t, mb) : mb;
    if (n > 1) window.renderFrameMB(t, n); else window.renderFrame(t);
    return document.getElementById('c').toDataURL('image/png').split(',')[1];
  }, { t, mb })), 'base64');

  if (only) {
    fs.mkdirSync(process.env.FRAMES_DIR || 'frames', { recursive: true });
    for (const f of only.split(',').map(Number)) {
      fs.writeFileSync(`${process.env.FRAMES_DIR || 'frames'}/f${String(f).padStart(4, '0')}.png`, await grab(f / FPS));
    }
    await browser.close(); return;
  }

  const total = Math.round(DUR * FPS);
  // Tuvalin saydam olduğu yerlerde altına konacak film (window.UNDERLAY = { src, at })
  const under = await page.evaluate(() => window.UNDERLAY || null);
  const underPath = under && path.join(__dirname, under.src);
  const useUnder = underPath && fs.existsSync(underPath);
  if (under && !useUnder) console.error(`Uyarı: ${under.src} yok, önce ./kaynaklar.sh çalıştırın`);
  const hasAudio = fs.existsSync(path.join(__dirname, 'audio.wav'));
  const vgraph = useUnder
    ? `color=c=black:s=1080x1920:r=${FPS}:d=${DUR}[base];[2:v]setpts=PTS-STARTPTS+${under.at}/TB[u];` +
      `[base][u]overlay=eof_action=pass[bu];[bu][0:v]overlay=format=auto,format=yuv420p[v]`
    : `[0:v]format=yuv420p[v]`;
  const agraph = hasAudio ? `;[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]` : `;[1:a]anull[a]`;
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    ...(hasAudio ? ['-i', path.join(__dirname, 'audio.wav')] : ['-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000']),
    ...(useUnder ? ['-i', underPath] : []),
    '-filter_complex', vgraph + agraph, '-map', '[v]', '-map', '[a]', '-t', String(DUR),
    '-c:v', 'libx264', '-preset', process.env.PRESET || 'slow', '-crf', process.env.CRF || '18', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
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
