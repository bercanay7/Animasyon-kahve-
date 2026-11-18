// Kapı klibi: node render.js <çıktı.mp4>   Ortam: WORKERS=3, MB=4 (hareket bulanıklığı alt kare), CRF=18, Q='dikey=1' (ek sayfa parametresi)
// Her işçi ardışık bir kare aralığını kendi parçasına kodlar; parçalar sonda kayıpsız birleştirilir. Ses yok.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.woff2': 'font/woff2' };
function serve() { return new Promise(r => { const s = http.createServer((q, res) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); }).listen(0, '127.0.0.1', () => r(s)); }); }
const FPS = 30, DUR = 19.5, N = Math.round(DUR * FPS);
const WORKERS = +process.env.WORKERS || 3, MB = +process.env.MB || 4, CRF = process.env.CRF || '18', EXTRA = process.env.Q || '';
// JPEG kareler tam aralık BT.601 → BT.709 sınırlı aralık, akışta BT.709 etiketleri
const X264 = ['-vf', 'scale=in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
  '-c:v', 'libx264', '-preset', 'medium', '-crf', CRF, '-pix_fmt', 'yuv420p', '-r', String(FPS)];
(async () => {
  const out = path.resolve(process.argv[2] || 'kapi.mp4');
  const tmp = out + '.parts'; fs.mkdirSync(tmp, { recursive: true });
  const srv = await serve(), port = srv.address().port;
  const t0 = Date.now(); let done = 0;
  const per = Math.ceil(N / WORKERS);
  const work = async w => {
    const a = w * per, b = Math.min(N, a + per); if (a >= b) return null;
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    page.on('pageerror', e => console.log('[hata]', e.message));
    await page.goto(`http://127.0.0.1:${port}/vazo/index.html?render=1${EXTRA ? '&' + EXTRA : ''}`);
    await page.waitForFunction(() => window.READY, null, { timeout: 60000 });
    const seg = path.join(tmp, `p${String(w).padStart(2, '0')}.mp4`);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', ...X264, seg], { stdio: ['pipe', 'ignore', 'inherit'] });
    for (let i = a; i < b; i++) {
      const b64 = await page.evaluate(({ t, mb }) => window.renderAt(t, mb).toDataURL('image/jpeg', .96).split(',')[1], { t: i / FPS, mb: MB });
      if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
      if (++done % 30 === 0) console.log(`${done}/${N} kare, ${((Date.now() - t0) / done / 1000 * WORKERS).toFixed(2)} sn/kare/işçi`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    await browser.close();
    return seg;
  };
  const segs = (await Promise.all([...Array(WORKERS).keys()].map(work))).filter(Boolean);
  fs.writeFileSync(path.join(tmp, 'list.txt'), segs.map(s => `file '${s}'`).join('\n'));
  await new Promise(r => spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'list.txt'), '-c', 'copy', '-movflags', '+faststart', out], { stdio: 'inherit' }).on('close', r));
  for (const s of segs) fs.unlinkSync(s); fs.unlinkSync(path.join(tmp, 'list.txt')); fs.rmdirSync(tmp);
  const sec = (Date.now() - t0) / 1000;
  console.log(`bitti: ${out}  ${sec.toFixed(0)} sn toplam, ${(sec / N * WORKERS).toFixed(2)} sn/kare/işçi (MB=${MB}, ${WORKERS} işçi)`);
  srv.close();
})();
