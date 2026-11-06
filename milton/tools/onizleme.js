// Deneme sahnesinden kısa önizleme videosu: node tools/onizleme.js <sahne> <süre-sn> <çıktı.mp4> [başlangıç]
// (kurul için hareket ve kamera önizlemesi; 30 fps, 2 alt örnekli hareket bulanıklığı)
const { chromium } = require('playwright');
const path = require('path'); const { spawn } = require('child_process');
(async () => {
  const [scene, dur, out, t0 = '0'] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.log('[err]', e.message));
  await page.goto('file://' + path.resolve(__dirname, '..', 'film.html') + '?render=1&scene=' + scene);
  await page.evaluate(() => window.ready);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-i', '-', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-preset', 'fast', out]);
  const n = Math.round(+dur * 30);
  for (let i = 0; i < n; i++) {
    const b64 = await page.evaluate(t => { renderFrameMB(t, 2); return document.getElementById('c').toDataURL('image/jpeg', .9).split(',')[1]; }, +t0 + i / 30);
    ff.stdin.write(Buffer.from(b64, 'base64'));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  await browser.close(); console.log('hazır', out);
})();
