// Logo hareketini MP4'e çevirir: node kanal/logo/hareket_render.js [sn=6]
// Çıktı: kanal/logo/cikti/logo_hareket_1080p.mp4 (1920×1080, 30 fps, H.264 CRF 18, BT.709, sessiz)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const http = require('http'), fs = require('fs'), path = require('path');
const KOK = __dirname, FPS = 30, SN = +(process.argv[2] || 6);
const TUR = { '.html': 'text/html', '.js': 'text/javascript', '.woff2': 'font/woff2' };
const srv = http.createServer((q, r) => {
  const p = path.join(KOK, decodeURIComponent(q.url.split('?')[0]));
  if (!p.startsWith(KOK) || !fs.existsSync(p)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': TUR[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r);
}).listen(0);
(async () => {
  const out = path.join(KOK, 'cikti', 'logo_hareket_1080p.mp4');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-pix_fmt', 'yuv420p',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const b = await chromium.launch(), pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await pg.goto(`http://localhost:${srv.address().port}/hareket.html`);
  await pg.evaluate(() => window.hazir);
  for (let i = 0; i < SN * FPS; i++) {
    await pg.evaluate(t => frame(t), i / FPS);
    const png = await pg.screenshot({ type: 'png' });
    if (!ff.stdin.write(png)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  await b.close(); srv.close(); console.log('✓', out);
})();
