// node tools/klip_cek.js <html> <çıktı.mp4> "v=manzara" <süre sn> [fps] — kare kare render → ffmpeg (deneme klibi; ses yok)
const { chromium } = require('playwright'); const path = require('path'), http = require('http'), fs = require('fs'), { spawn } = require('child_process');
const ROOT = path.resolve(__dirname, '..');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2', '.json': 'application/json' };
(async () => {
  const [html, out, qs, dur, fpsA] = process.argv.slice(2); const fps = +(fpsA || 30), N = Math.round(+dur * fps);
  const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': MIME[path.extname(f).toLowerCase()] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(0);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('HATA', e.message));
  await p.goto(`http://127.0.0.1:${srv.address().port}/${html}?${qs}`); await p.waitForFunction(() => window.READY, null, { timeout: 60000 });
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', out]);
  const t0 = Date.now();
  for (let i = 0; i < N; i++) {
    await p.evaluate(t => window.render(t), i / fps);
    const buf = await p.evaluate(() => document.getElementById('c').toDataURL('image/jpeg', .92).split(',')[1]);
    if (!ff.stdin.write(Buffer.from(buf, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 90 === 0) console.log(i, '/', N, ((Date.now() - t0) / (i + 1)).toFixed(0), 'ms/kare');
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); srv.close(); console.log('bitti', out);
})();
