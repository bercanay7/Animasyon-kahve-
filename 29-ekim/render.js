// 29 Ekim çıktıları (Playwright + ffmpeg gerekir):
//   node render.js story            → 29-ekim-story.png
//   node render.js video            → 29-ekim-zumba.mp4
//   FRAMES=0,45,300 node render.js video  → sadece frames/ altına PNG kareler (önizleme)
// Sayfalar sahte bir http kökünden servis edilir; böylece fotoğraflar tuvali "kirletmez" ve toDataURL çalışır.
const { chromium } = require('playwright');
const { spawn, spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const HERE = __dirname, ROOT = path.resolve(HERE, '..'), ORIGIN = 'http://navitas.local/';
const SRC = path.join(HERE, 'kaynak', 'zumba-kaynak.mp4');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.woff2': 'font/woff2', '.jpg': 'image/jpeg', '.png': 'image/png' };
const what = process.argv[2] || 'story';

// Kaynak videodan kareler: dans bölümü 1080x1920'ye büyütülmüş, kapanıştaki yatay çekim kırpılıp 1280x720
function extractFrames() {
  const v = path.join(HERE, 'build', 'v'), w = path.join(HERE, 'build', 'w');
  if (fs.existsSync(path.join(w, '0563.jpg'))) return;
  fs.mkdirSync(v, { recursive: true }); fs.mkdirSync(w, { recursive: true });
  const run = args => { const r = spawnSync('ffmpeg', ['-v', 'error', '-y', '-i', SRC, ...args], { stdio: 'inherit' }); if (r.status) process.exit(1); };
  run(['-vf', "select='lte(n,420)',scale=1080:1920:flags=lanczos,unsharp=5:5:0.45", '-vsync', '0', '-start_number', '0', '-q:v', '2', path.join(v, '%04d.jpg')]);
  run(['-vf', "select='between(n,464,563)',crop=576:324:0:350,scale=1280:720:flags=lanczos,unsharp=5:5:0.45", '-vsync', '0',
    '-start_number', '464', '-q:v', '2', path.join(w, '%04d.jpg')]);
}

(async () => {
  if (what === 'video') extractFrames();
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.route(ORIGIN + '**', route => {
    const p = path.join(ROOT, decodeURIComponent(new URL(route.request().url()).pathname));
    if (!p.startsWith(ROOT) || !fs.existsSync(p)) return route.fulfill({ status: 404, body: '' });
    route.fulfill({ status: 200, body: fs.readFileSync(p), contentType: MIME[path.extname(p)] || 'application/octet-stream' });
  });
  page.on('pageerror', e => console.error('Sayfa hatası:', e.message));
  const grabPNG = () => page.evaluate(() => document.getElementById('c').toDataURL('image/png').split(',')[1]).then(b => Buffer.from(b, 'base64'));

  if (what === 'story') {
    await page.goto(ORIGIN + '29-ekim/story.html');
    await page.evaluate(() => window.ready);
    const out = path.join(HERE, '29-ekim-story.png');
    fs.writeFileSync(out, await grabPNG());
    console.log('Hazır: ' + out);
  } else {
    await page.goto(ORIGIN + '29-ekim/zumba.html?render=1');
    await page.evaluate(() => window.ready);
    const { DUR, FPS } = await page.evaluate(() => ({ DUR: window.DUR, FPS: window.FPS }));
    const grab = async i => { await page.evaluate(t => window.renderFrame(t), i / FPS); return grabPNG(); };
    if (process.env.FRAMES) {
      fs.mkdirSync(path.join(HERE, 'frames'), { recursive: true });
      for (const f of process.env.FRAMES.split(',').map(Number))
        fs.writeFileSync(path.join(HERE, 'frames', `f${String(f).padStart(4, '0')}.png`), await grab(f));
    } else {
      const out = path.join(HERE, '29-ekim-zumba.mp4'), total = Math.round(DUR * FPS);
      // Ses: kaynağın kendi müziği, sona doğru yumuşakça kısılır
      const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-i', SRC,
        '-map', '0:v', '-map', '1:a', '-af', `afade=t=out:st=${(DUR - 0.9).toFixed(2)}:d=0.9`, '-t', DUR.toFixed(3),
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', String(FPS),
        '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
      for (let i = 0; i < total; i++) {
        const buf = await grab(i);
        if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
        if (i % 30 === 0) process.stdout.write(`\r${i}/${total}`);
      }
      ff.stdin.end();
      await new Promise(r => ff.on('close', r));
      console.log('\nHazır: ' + out);
    }
  }
  await browser.close();
})();
