// node tools/kare_cek.js <html (ran/ altına göre)> <çıktı.png> "v=manzara&t=3" — kendi küçük http sunucusunu açar (file:// görselleri WebGL'i kirletir)
const { chromium } = require('playwright'); const path = require('path'), http = require('http'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2', '.json': 'application/json' };
(async () => {
  const [html, out, qs] = process.argv.slice(2);
  const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': MIME[path.extname(f).toLowerCase()] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(0);
  const port = srv.address().port;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('HATA', e.message));
  await p.goto(`http://127.0.0.1:${port}/${html}?${qs || ''}`);
  await p.waitForFunction(() => window.READY, null, { timeout: 60000 });
  await p.screenshot({ path: out }); await b.close(); srv.close();
})();
