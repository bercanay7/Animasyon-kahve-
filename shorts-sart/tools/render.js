// Şart Shorts'u render: node /home/user/Animasyon-kahve-/shorts-sart/tools/render.js <proje> [çıktı.mp4]
// WORKERS=3 (ayrı Chromium'lar), MB=4 hareket bulanıklığı, SADECE_KODLA=1 kareleri yeniden üretmez.
// Ses: <proje>/audio/mix.wav (tools/miks.py). Çıktı 1080×1920, 30 fps, H.264 CRF 18, BT.709, AAC 256k, ses dili tur.
const { chromium } = require('playwright');
const { fork, spawnSync } = require('child_process');
const path = require('path'), fs = require('fs');
const { serve } = require('./sunucu');
const FPS = 30, MB = +(process.env.MB || 4), N = +(process.env.WORKERS || 3);
const EK = ad => /"mod":\s*"kirp"/.test(fs.readFileSync(path.join(__dirname, '..', ad, 'kurgu.js'), 'utf8')) ? '&rs=2' : ''; // kırpma kipi: film 2 kat çözünürlükte
const URL = (port, ad) => `http://127.0.0.1:${port}/shorts-sart/${ad}/index.html?render=1&notext=1${EK(ad)}`;

async function worker() {
  const { a, b, port, ad, tmp } = JSON.parse(process.env._JOB);
  const br = await chromium.launch(); const p = await br.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('[hata]', e.message));
  await p.goto(URL(port, ad)); await p.waitForFunction(() => window.READY, null, { timeout: 180000 });
  for (let i = a; i < b; i++) {
    const b64 = await p.evaluate(({ t, mb }) => renderShort(t, mb).toDataURL('image/jpeg', .96).split(',')[1], { t: i / FPS, mb: MB });
    fs.writeFileSync(path.join(tmp, `k${String(i).padStart(5, '0')}.jpg`), Buffer.from(b64, 'base64'));
    if ((i - a) % 30 === 0) process.send({ i });
  }
  await br.close(); process.exit(0);
}

async function main() {
  const dir = path.resolve(process.argv[2]), ad = path.basename(dir);
  const out = path.resolve(process.argv[3] || path.join(dir, `${ad}_sart.mp4`));
  const tmp = path.join(dir, '.kareler');
  const KODLA = !!process.env.SADECE_KODLA;
  if (!KODLA) { fs.rmSync(tmp, { recursive: true, force: true }); fs.mkdirSync(tmp, { recursive: true }); }
  const srv = await serve(); const port = srv.address().port;
  const br = await chromium.launch(); const pg = await br.newPage();
  await pg.goto(URL(port, ad)); await pg.waitForFunction(() => window.READY, null, { timeout: 180000 });
  const DUR = await pg.evaluate(() => SHORTS.DUR); await br.close();
  const NF = Math.round(DUR * FPS); console.log(`${ad}: ${DUR.toFixed(2)} sn, ${NF} kare, ${N} işçi, mb ${MB}`);
  const t0 = Date.now();
  if (!KODLA) await Promise.all([...Array(N)].map((_, w) => new Promise((res, rej) => {
    const a = Math.floor(NF * w / N), b = Math.floor(NF * (w + 1) / N);
    const c = fork(__filename, [], { env: { ...process.env, _JOB: JSON.stringify({ a, b, port, ad, tmp }) } });
    c.on('message', m => process.stdout.write(`\r[${w}] ${m.i}/${b}  ${((Date.now() - t0) / 1000) | 0} sn   `));
    c.on('exit', code => code === 0 ? res() : rej(new Error('işçi ' + w)));
  })));
  srv.close(); console.log(`\nkareler bitti (${((Date.now() - t0) / 1000) | 0} sn)`);
  const r = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(tmp, 'k%05d.jpg'), '-i', path.join(dir, 'audio', 'mix.wav'),
    '-map', '0:v', '-map', '1:a',
    '-vf', 'scale=in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', String(FPS),
    '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-metadata:s:a:0', 'language=tur', '-t', DUR.toFixed(3), '-movflags', '+faststart', out], { stdio: 'inherit' });
  if (r.status !== 0) throw new Error('ffmpeg');
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log('yazıldı:', out);
}
if (process.env._JOB) worker(); else main().catch(e => { console.error(e); process.exit(1); });
