// Yerel http sunucusu, DEPO KÖKÜNDEN (shorts-sart sayfaları filmlerin motorlarını ../../narkissos/lib/… yoluyla yükler).
// file:// görseller tuvali kirletir (Ran dersi); render ve kare araçları sayfayı buradan açar.
// Doğrudan: node shorts-sart/tools/sunucu.js [port] → http://127.0.0.1:<port>/shorts-sart/narkissos/index.html
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css', '.json': 'application/json', '.woff2': 'font/woff2',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.wav': 'audio/wav', '.mp3': 'audio/mpeg', '.ttf': 'font/ttf' };
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
if (require.main === module) serve(+process.argv[2] || 8766).then(s => console.log(`http://127.0.0.1:${s.address().port}/shorts-sart/`));
