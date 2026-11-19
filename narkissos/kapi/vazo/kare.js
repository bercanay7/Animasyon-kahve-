// Tek kareler: node kare.js <çıktı_klasörü> ad=t[,mb] ... | ad=kapak:A | ad=dikey:t
// Örn: node kare.js /tmp/k A_cam=1.5 D_benim=15.0,4 kapak=kapak:yazili dikey_D=dikey:13.8
// Yerel http sunucusu (narkissos/kapi kökü: ../ortak/ erişilir); kareler canvas.toDataURL ile alınır.
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.woff2': 'font/woff2', '.png': 'image/png', '.jpg': 'image/jpeg' };
function serve() { return new Promise(r => { const s = http.createServer((q, res) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); }).listen(0, '127.0.0.1', () => r(s)); }); }
(async () => {
  const [out, ...jobs] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const srv = await serve(), port = srv.address().port;
  const browser = await chromium.launch();
  const pages = {};
  const get = async (q) => {
    if (pages[q]) return pages[q];
    const p = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    p.on('pageerror', e => console.log('[hata]', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('[konsol]', m.text()); });
    await p.goto(`http://127.0.0.1:${port}/vazo/index.html?render=1${q}`);
    await p.waitForFunction(() => window.READY, null, { timeout: 60000 });
    return (pages[q] = p);
  };
  for (const j of jobs) {
    const [ad, spec] = j.split('=');
    let q = '', fn;
    if (spec.startsWith('kapak:')) { q = '&kapak=' + spec.slice(6); fn = () => window.renderAt(0, 1); }
    else if (spec.startsWith('dikey:')) { q = '&dikey=1'; }
    const [tS, mbS] = spec.replace(/^dikey:/, '').split(',');
    const p = await get(q);
    const t0 = Date.now();
    const b64 = await p.evaluate(({ t, mb, kap, fmt }) => { const c = window.renderAt(t, mb); return c.toDataURL(fmt, .96).split(',')[1]; },
      { t: +tS || 0, mb: +mbS || 1, kap: !!q.includes('kapak'), fmt: ad.endsWith('.jpg') ? 'image/jpeg' : 'image/png' });
    const fn2 = path.join(out, ad.includes('.') ? ad : ad + '.png');
    fs.writeFileSync(fn2, Buffer.from(b64, 'base64'));
    console.log(fn2, ((Date.now() - t0) / 1000).toFixed(2) + ' sn');
  }
  await browser.close(); srv.close();
})();
