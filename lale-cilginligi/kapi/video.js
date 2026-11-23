// node kapi/video.js sahne süre çıktı.mp4  (tek işçi, 30 kare/sn, kare süresi ölçülür)
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const S = require('../tools/sunucu');
(async () => { const [sc, dur, out] = process.argv.slice(2); const srv = await S.baslat(); const br = await chromium.launch(); const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('[hata]', e.message));
  await p.goto(`http://127.0.0.1:${srv.address().port}/lale-cilginligi/kapi/kapi.html?render=1&scene=${sc}`); await p.waitForFunction(() => window.READY || window.HATA);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'ignore', 'inherit'] });
  const N = Math.round(+dur * 30), t0 = Date.now();
  for (let i = 0; i < N; i++) { const b64 = await p.evaluate(t => window.renderFrame(t).toDataURL('image/jpeg', .95).split(',')[1], i / 30); if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r)); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); console.log(sc, N, 'kare', ((Date.now() - t0) / N / 1000).toFixed(2), 'sn/kare'); await br.close(); srv.close(); })();
