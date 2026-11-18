// Narkissos risograf kapısı: kare, kapak ve video üretimi (yerel http sunucusu; file:// WebGL tuvalini kirletir).
//   node render.js kareler            → anahtar kareler (PNG 1920×1080)
//   node render.js kare 12.2 [mb]     → tek kare (PNG)
//   node render.js kapak              → kapak.jpg + kapak_yazisiz.jpg (1280×720, PIL ile küçültülür)
//   node render.js dikey              → dikey_D.png (1080×1920, D planı)
//   node render.js video [mb]         → kapi.mp4 (19,5 sn, 30 fps, sessiz; varsayılan mb=4)
//   node render.js olc [mb]           → tek işçi kare süresi ölçümü
// Ortam: OUT (çıktı klasörü), WORKERS (video işçi sayısı, varsayılan 3)
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const OUT = process.env.OUT || '/tmp/claude-0/-home-user/d2cf6cd4-4d63-590c-86cd-58e0a7f88ab8/scratchpad/kapi/riso';
const FPS = 30, DUR = 19.5;
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.woff2': 'font/woff2', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg' };
function serve() { return new Promise(r => { const s = http.createServer((q, res) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); }).listen(0, '127.0.0.1', () => r(s)); }); }

async function sayfa(br, port, q, w = 1920, h = 1080) {
  const p = await br.newPage({ viewport: { width: w, height: h } });
  p.on('pageerror', e => console.log('[sayfa hatası]', e.message));
  p.on('console', m => { if (m.type() === 'error') console.log('[konsol]', m.text()); });
  await p.goto(`http://127.0.0.1:${port}/riso/index.html?render=1${q ? '&' + q : ''}`);
  await p.waitForFunction(() => window.READY || window.HATA, null, { timeout: 30000 });
  const hata = await p.evaluate(() => window.HATA); if (hata) throw new Error(hata);
  return p;
}
const png = async (p, t, mb, dosya) => { const b64 = await p.evaluate(({ t, mb }) => window.renderAt(t, mb).toDataURL('image/png').split(',')[1], { t, mb }); fs.writeFileSync(dosya, Buffer.from(b64, 'base64')); };

const KARELER = [['A_cam', 1.5], ['A_gecis', 3.0], ['B', 5.0], ['C', 9.0], ['D_once', 11.0], ['D_halka', 12.2], ['D_toparlanma', 13.8], ['D_benim', 15.0], ['E', 18.5]];

async function main() {
  const [mod, a1, a2] = process.argv.slice(2);
  fs.mkdirSync(path.join(OUT, 'kareler'), { recursive: true });
  const srv = await serve(), port = srv.address().port;
  const br = await chromium.launch();
  try {
    if (mod === 'kareler' || mod === 'kare') {
      const p = await sayfa(br, port, '');
      const list = mod === 'kare' ? [['kare_' + a1, +a1]] : KARELER;
      const mb = mod === 'kare' ? +(a2 || 1) : 4;
      for (const [ad, t] of list) { const t0 = Date.now(); await png(p, t, mb, path.join(OUT, 'kareler', ad + '.png')); console.log(ad, t, (Date.now() - t0) + ' ms'); }
    } else if (mod === 'kapak') {
      for (const [q, ad] of [['kapak=1', 'kapak'], ['kapak=0', 'kapak_yazisiz']]) {
        const p = await sayfa(br, port, q);
        const f = path.join(OUT, ad + '_1920.png');
        const b64 = await p.evaluate(() => document.getElementById('c').toDataURL('image/png').split(',')[1]);
        fs.writeFileSync(f, Buffer.from(b64, 'base64'));
        execFileSync('python3', ['-c', `from PIL import Image;im=Image.open('${f}').convert('RGB').resize((1280,720),Image.LANCZOS);im.save('${path.join(OUT, ad + '.jpg')}',quality=92,subsampling=0)`]);
        console.log(ad, fs.statSync(path.join(OUT, ad + '.jpg')).size, 'bayt');
        await p.close();
      }
    } else if (mod === 'dikey') {
      const p = await sayfa(br, port, 'w=1080&h=1920', 1080, 1920);
      await png(p, +(a1 || 15.0), 4, path.join(OUT, 'dikey_D.png'));
      console.log('dikey_D.png');
    } else if (mod === 'olc') {
      const p = await sayfa(br, port, '');
      const mb = +(a1 || 4), sure = {};
      for (const t of [1.5, 3.0, 5.0, 9.0, 12.2, 15.0, 18.5]) {
        await p.evaluate(({ t, mb }) => window.renderAt(t, mb), { t, mb });
        const t0 = Date.now(); await p.evaluate(({ t, mb }) => window.renderAt(t, mb).toDataURL('image/jpeg', .96).length, { t: t + 1 / 30, mb }); sure[t] = Date.now() - t0;
      }
      console.log('mb=' + mb, JSON.stringify(sure), 'ortalama', Math.round(Object.values(sure).reduce((a, b) => a + b, 0) / 7), 'ms/kare (çizim + baskı + JPEG)');
    } else if (mod === 'video') {
      const mb = +(a1 || 4), nW = +(process.env.WORKERS || 3), total = Math.round(DUR * FPS);
      const per = Math.ceil(total / nW), parts = [], t0 = Date.now();
      await Promise.all(Array.from({ length: nW }, async (_, k) => {
        const a = k * per, b = Math.min(total, a + per); if (a >= b) return;
        const p = await sayfa(br, port, '');
        const f = path.join(OUT, `.parca${k}.mp4`); parts[k] = f;
        const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
          '-vf', 'scale=in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709',
          '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-r', String(FPS), f], { stdio: ['pipe', 'ignore', 'inherit'] });
        for (let i = a; i < b; i++) {
          const b64 = await p.evaluate(({ t, mb }) => window.renderAt(t, mb).toDataURL('image/jpeg', .96).split(',')[1], { t: i / FPS, mb });
          if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
          if ((i - a) % 30 === 0) console.log(`işçi ${k}: ${i - a}/${b - a}  ${((Date.now() - t0) / 1000).toFixed(0)} sn`);
        }
        ff.stdin.end(); await new Promise((r, j) => ff.on('close', c => c ? j(new Error('ffmpeg ' + c)) : r()));
        await p.close();
      }));
      const list = path.join(OUT, '.liste.txt'); fs.writeFileSync(list, parts.filter(Boolean).map(f => `file '${f}'`).join('\n'));
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', '-movflags', '+faststart', path.join(OUT, 'kapi.mp4')]);
      parts.filter(Boolean).forEach(f => fs.unlinkSync(f)); fs.unlinkSync(list);
      const el = (Date.now() - t0) / 1000;
      console.log(`kapi.mp4  mb=${mb}  ${nW} işçi  ${el.toFixed(0)} sn  (${(el * nW / total).toFixed(2)} sn/kare/işçi)`);
    } else console.log('kullanım: node render.js kareler|kare T [mb]|kapak|dikey|video [mb]|olc [mb]');
  } finally { await br.close(); srv.close(); }
}
main().catch(e => { console.error(e); process.exit(1); });
