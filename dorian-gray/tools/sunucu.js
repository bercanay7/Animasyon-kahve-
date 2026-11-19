// Yerel http sunucusu (kök: depo; file:// WebGL tuvalini kirletir). require('./sunucu').baslat() → port
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.woff2': 'font/woff2', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg' };
exports.baslat = () => new Promise(r => { const s = http.createServer((q, res) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); }).listen(0, '127.0.0.1', () => r(s)); });
exports.sayfa = async (br, port, q = '', w = 1920, h = 1080) => {
  const p = await br.newPage({ viewport: { width: w, height: h } });
  p.on('pageerror', e => console.log('[sayfa hatası]', e.message));
  p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log('[konsol]', m.text()); });
  await p.goto(`http://127.0.0.1:${port}/dorian-gray/film.html?render=1${q ? '&' + q : ''}`);
  await p.waitForFunction(() => window.READY || window.HATA, null, { timeout: 300000 });
  const h_ = await p.evaluate(() => window.HATA); if (h_) throw new Error(h_);
  return p;
};
