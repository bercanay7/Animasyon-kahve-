// node tools/kisa_kare.js çıktı.png t [edl adı] — Shorts karesi
const { chromium } = require('playwright'); const path = require('path'), http = require('http'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
(async () => { const [out, t, edl] = process.argv.slice(2);
  const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200); fs.createReadStream(f).pipe(r); }).listen(0);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } }); p.on('pageerror', e => console.log('HATA', e.message));
  await p.goto(`http://127.0.0.1:${srv.address().port}/shorts.html?render=1${edl ? '&edl=' + edl : ''}`); await p.waitForFunction(() => window.READY && window.renderShortFrame, null, { timeout: 120000 }); await p.waitForTimeout(300);
  const b64 = await p.evaluate(t => renderShortFrame(+t).toDataURL('image/png').split(',')[1], t); fs.writeFileSync(out, Buffer.from(b64, 'base64')); await b.close(); srv.close(); })();
