// Yerel http sunucusu (orfeus/ kökü). file:// görseller tuvali kirletir (Ran dersi); render, kare ve özet araçları sayfayı buradan açar.
// Kullanım: const { serve } = require('./sunucu'); const srv = await serve(); srv.address().port
// Doğrudan: node tools/sunucu.js [port]  (tarayıcıda canlı önizleme: http://127.0.0.1:<port>/film.html)
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css', '.json': 'application/json', '.woff2': 'font/woff2',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.wav': 'audio/wav', '.mp3': 'audio/mpeg' };
function serve(port = 0) {
  return new Promise(r => {
    const s = http.createServer((q, res) => {
      const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
      if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(f).toLowerCase()] || 'application/octet-stream', 'Cache-Control': 'no-store' });
      fs.createReadStream(f).pipe(res);
    }).listen(port, '127.0.0.1', () => r(s));
  });
}
module.exports = { serve, ROOT };
if (require.main === module) serve(+process.argv[2] || 8765).then(s => console.log(`http://127.0.0.1:${s.address().port}/film.html`));
