// Yeni sahneler için bağımsız render (mevcut render.js'e dokunmaz).
// Kullanım:  NODE_PATH=$(npm root -g) SIZE=1920x1080 node araclar/render-sahne.js araclar/ornek-sahne.html cikti.mp4
// Env: SIZE=GxY (vars. 1920x1080) · AUDIO=ses.wav (yoksa sessiz) · MB_SAMPLES=8 (1=blur kapalı) · FRAMES=0,30,60 (yalnız PNG)
// Sahne sözleşmesi: window.ready, window.DUR, window.FPS, window.renderFrame(t), window.renderFrameMB(t, n), <canvas id="c">
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path'), fs = require('fs');

const scene = process.argv[2], out = process.argv[3] || 'cikti.mp4';
if (!scene) { console.error('Kullanım: node araclar/render-sahne.js <sahne.html> [cikti.mp4]'); process.exit(1); }
const [VW, VH] = (process.env.SIZE || '1920x1080').split('x').map(Number);
const audio = process.env.AUDIO;
const mb = +(process.env.MB_SAMPLES || 8);

(async () => {
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  const page = await browser.newPage({ viewport: { width: VW, height: VH } });
  await page.goto('file://' + path.resolve(scene) + '?render=1');
  await page.evaluate(() => window.ready);
  const { DUR, FPS } = await page.evaluate(() => ({ DUR: window.DUR, FPS: window.FPS }));
  const grab = async t => Buffer.from((await page.evaluate(({ t, mb }) => {
    if (mb > 1) window.renderFrameMB(t, mb); else window.renderFrame(t);
    return document.getElementById('c').toDataURL('image/png').split(',')[1];
  }, { t, mb })), 'base64');

  if (process.env.FRAMES) {
    fs.mkdirSync('frames', { recursive: true });
    for (const f of process.env.FRAMES.split(',').map(Number))
      fs.writeFileSync(`frames/f${String(f).padStart(4, '0')}.png`, await grab(f / FPS));
    await browser.close(); return;
  }
  const total = Math.round(DUR * FPS);
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    ...(audio && fs.existsSync(audio)
      ? ['-i', audio, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000']
      : ['-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000']),
    '-map', '0:v', '-map', '1:a', '-shortest',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
    '-r', String(FPS), '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out],
    { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let i = 0; i < total; i++) {
    const buf = await grab(i / FPS);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 30 === 0) process.stdout.write(`\r${i}/${total}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await browser.close();
  console.log(`\nHazır: ${out}`);
})();
