// Dorian Gray üslup kapısı: kareler, kapak, video ve süre ölçümü (yerel http; file:// WebGL tuvalini kirletir).
//   node render.js <mod> kareler        → anahtar kareler (PNG)
//   node render.js <mod> kapak          → kapak.jpg (1280×720) + 168/246/120 px küçültmeler
//   node render.js <mod> video          → <mod>.mp4 (8 sn, 30 fps, H.264 CRF 18, BT.709, sessiz)
//   node render.js <mod> olc            → tek işçi kare süresi (çizim + JPEG)
// mod: gravur | impasto | karma. Ortam: OUT (çıktı kökü), WORKERS (video, varsayılan 3)
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const BASE = process.env.OUT || '/tmp/claude-0/-home-user/06a13132-db14-5a13-9630-f9f2e06ea0e6/scratchpad/kapi';
const FPS = 30, DUR = 8.0;
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.woff2': 'font/woff2', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg' };
function serve() { return new Promise(r => { const s = http.createServer((q, res) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); }).listen(0, '127.0.0.1', () => r(s)); }); }
async function sayfa(br, port, mod, ek = '') {
  const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('[sayfa hatası]', e.message));
  p.on('console', m => { if (m.type() === 'error') console.log('[konsol]', m.text()); });
  const t0 = Date.now();
  await p.goto(`http://127.0.0.1:${port}/dorian-gray/kapi/index.html?render=1&mod=${mod}${ek}`);
  await p.waitForFunction(() => window.READY || window.HATA, null, { timeout: 600000 });
  const hata = await p.evaluate(() => window.HATA); if (hata) throw new Error(hata);
  console.log(`${mod}: kurulum ${((Date.now() - t0) / 1000).toFixed(1)} sn`, JSON.stringify(await p.evaluate(() => window.STROKES)));
  return p;
}
const resim = async (p, t, tur = 'png', q = .96) => Buffer.from(await p.evaluate(({ t, tur, q }) => window.renderAt(t).toDataURL('image/' + tur, q).split(',')[1], { t, tur, q }), 'base64');
const KARELER = [['a_uzanma', 1.2], ['b_cekis', 3.1], ['c_acilis', 4.6], ['d_son', 7.6]];
async function main() {
  const [mod, is] = process.argv.slice(2), OUT = path.join(BASE, mod); fs.mkdirSync(OUT, { recursive: true });
  const srv = await serve(), port = srv.address().port;
  const br = await chromium.launch();
  try {
    if (is === 'kareler') { const p = await sayfa(br, port, mod);
      for (const [ad, t] of KARELER) { const t0 = Date.now(); fs.writeFileSync(path.join(OUT, ad + '.png'), await resim(p, t)); console.log(ad, t, (Date.now() - t0) + ' ms'); } }
    else if (is === 'kapak') { const p = await sayfa(br, port, mod, '&kapak=1'), f = path.join(OUT, 'kapak_1920.png');
      fs.writeFileSync(f, await resim(p, +(process.env.KT || 3.75)));
      execFileSync('python3', ['-c', `from PIL import Image
im=Image.open('${f}').convert('RGB'); o='${OUT}'
im.resize((1280,720),Image.LANCZOS).save(o+'/kapak.jpg',quality=92,subsampling=0)
for w,h in [(246,138),(168,94),(120,68)]: im.resize((w,h),Image.LANCZOS).save(o+f'/kapak_{w}.png')
g=im.convert('L').resize((480,270)); g.save(o+'/kapak_gri.png')`]);
      console.log('kapak', fs.statSync(path.join(OUT, 'kapak.jpg')).size, 'bayt'); }
    else if (is === 'olc') { const p = await sayfa(br, port, mod), s = [];
      await resim(p, .5, 'jpeg');
      for (const t of [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]) { const t0 = Date.now(); await resim(p, t, 'jpeg'); s.push(Date.now() - t0); }
      console.log(mod, 'kare süreleri (ms):', s.join(' '), '| ortalama', Math.round(s.reduce((a, b) => a + b) / s.length)); }
    else if (is === 'video') {
      const nW = +(process.env.WORKERS || 3), total = Math.round(DUR * FPS), per = Math.ceil(total / nW), parts = [], t0 = Date.now();
      await Promise.all(Array.from({ length: nW }, async (_, k) => {
        const a = k * per, b = Math.min(total, a + per); if (a >= b) return;
        const b2 = await chromium.launch(); const p = await sayfa(b2, port, mod);
        const f = path.join(OUT, `.parca${k}.mp4`); parts[k] = f;
        const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
          '-vf', 'scale=in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709',
          '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-r', String(FPS), f], { stdio: ['pipe', 'ignore', 'inherit'] });
        for (let i = a; i < b; i++) { const buf = await resim(p, i / FPS, 'jpeg'); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
          if ((i - a) % 60 === 0) console.log(`işçi ${k}: ${i - a}/${b - a}  ${((Date.now() - t0) / 1000).toFixed(0)} sn`); }
        ff.stdin.end(); await new Promise((r, j) => ff.on('close', c => c ? j(new Error('ffmpeg ' + c)) : r())); await b2.close();
      }));
      const lst = path.join(OUT, '.liste.txt'); fs.writeFileSync(lst, parts.filter(Boolean).map(f => `file '${f}'`).join('\n'));
      const mp4 = path.join(OUT, mod + '.mp4');
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', mp4]);
      parts.filter(Boolean).forEach(f => fs.unlinkSync(f));
      console.log(mod + '.mp4', fs.statSync(mp4).size, 'bayt', ((Date.now() - t0) / 1000).toFixed(0), 'sn toplam (' + nW + ' işçi)'); }
  } finally { await br.close(); srv.close(); }
}
main().catch(e => { console.error(e); process.exit(1); });
