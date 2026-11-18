// node tools/olc.js t1 t2 ... — her an için kare süresini ölçer (ısınmadan sonra), ton/redraw/film ayrımıyla
const { chromium } = require('playwright'); const path = require('path'), http = require('http'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2', '.json': 'application/json' };
(async () => {
  const ts = process.argv.slice(2).map(Number);
  const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': MIME[path.extname(f).toLowerCase()] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(0);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('console', m => console.log('>', m.text()));
  const t0 = Date.now(); await p.goto(`http://127.0.0.1:${srv.address().port}/film.html?render=1`); await p.waitForFunction(() => window.READY, null, { timeout: 120000 }); console.log('yükleme', Date.now() - t0, 'ms');
  for (const t of ts) {
    const r = await p.evaluate(t => { renderFrame(t); const a = performance.now(); for (let i = 1; i <= 4; i++) renderFrame(t + i / 30); const b = performance.now(); const c = renderFrame(t).toDataURL('image/jpeg', .96); const d = performance.now(); return [(b - a) / 4, d - b]; }, t);
    console.log('t=' + t, 'kare', r[0].toFixed(0), 'ms; jpeg', r[1].toFixed(0), 'ms');
  }
  await b.close(); srv.close();
})();
