// node /home/user/Animasyon-kahve-/araclar/manken/render.js <sahne.html (depo köküne göre)> <çıktı.mp4>   (mutlak yolla başlat)
// manken-cizim sahneleri için dört işçili kare kare render: yerel http sunucusu (file:// WebGL'i kirletir), SwiftShader.
// Sözleşme: window.READY, window.DUR, window.renderAt(t) → <canvas id="c">. Aynı t her işçide aynı kare (tohum t'den).
// Ortam: WORKERS=4 · FPS=30 · CRF=18 · PRESET=slow · ARALIK=0-5 (saniye) · Q='sahne=yakin' ek sorgu · SURE=1 kare sürelerini yaz
// Çıktı: H.264 High yuv420p, BT.709 etiketleri, sessiz AAC (ses dili 'tur'); +faststart.
const { chromium } = require('playwright');
const { spawn, fork } = require('child_process');
const path = require('path'), fs = require('fs');
const S = require('../../dorian-gray/tools/sunucu.js');
const FPS = +(process.env.FPS || 30), N = +(process.env.WORKERS || 4), CRF = process.env.CRF || '18', PRESET = process.env.PRESET || 'slow';
const X264 = ['-vf', 'scale=in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
  '-c:v', 'libx264', '-preset', PRESET, '-crf', CRF, '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-g', '60'];
const bekle = p => new Promise((r, j) => p.on('close', c => (c === 0 ? r() : j(new Error('ffmpeg ' + c)))));

async function isci() {
  const br = await chromium.launch(), p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('[hata]', e.message));
  await p.goto(`http://127.0.0.1:${process.env._PORT}/${process.env._SAHNE}?render=1${process.env.Q ? '&' + process.env.Q : ''}`);
  await p.waitForFunction(() => window.READY || window.HATA, null, { timeout: 120000 });
  process.on('message', async is => {
    if (is.bitti) { await br.close(); process.exit(0); }
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', ...X264, '-r', String(FPS), is.out], { stdio: ['pipe', 'ignore', 'inherit'] });
    let top = 0;
    for (let i = is.a; i < is.b; i++) {
      const r = await p.evaluate(t => { const a = performance.now(); const c = window.renderAt(t); (window.BITIR || MANKEN.bitir)(); const d = performance.now() - a; return { d, u: c.toDataURL('image/jpeg', .96).split(',')[1] }; }, i / FPS);
      top += r.d;
      if (!ff.stdin.write(Buffer.from(r.u, 'base64'))) await new Promise(r_ => ff.stdin.once('drain', r_));
    }
    ff.stdin.end(); await bekle(ff);
    process.send({ fin: is.k, ort: top / (is.b - is.a) });
  });
  process.send({ hazir: true });
}

async function usta() {
  const [sahne, cikti] = process.argv.slice(2);
  if (!sahne || !cikti) { console.error('Kullanım: node araclar/manken/render.js araclar/manken/deneme.html cikti.mp4'); process.exit(1); }
  const srv = await S.baslat(), port = srv.address().port;
  const br = await chromium.launch(), p = await br.newPage();
  await p.goto(`http://127.0.0.1:${port}/${sahne}?render=1${process.env.Q ? '&' + process.env.Q : ''}`);
  await p.waitForFunction(() => window.READY || window.HATA, null, { timeout: 120000 });
  const DUR = await p.evaluate(() => window.DUR); await br.close();
  const [ra, rb] = process.env.ARALIK ? process.env.ARALIK.split('-').map(Number) : [0, DUR];
  const f0 = Math.round(ra * FPS), f1 = Math.round(rb * FPS), dir = cikti + '.parcalar';
  fs.mkdirSync(dir, { recursive: true });
  const CH = Math.ceil((f1 - f0) / (N * 3)), isler = [];
  for (let a = f0, k = 0; a < f1; a += CH, k++) isler.push({ k, a, b: Math.min(f1, a + CH), out: path.join(dir, `p${String(k).padStart(3, '0')}.mp4`) });
  console.log(`${sahne} | ${(f1 - f0)} kare, ${isler.length} parça, ${N} işçi`);
  const t0 = Date.now(), sira = isler.slice(), ortalar = [];
  await Promise.all(Array.from({ length: N }, () => new Promise(res => {
    const w = fork(__filename, [], { env: { ...process.env, _ISCI: '1', _PORT: port, _SAHNE: sahne } });
    const ver = () => { const is = sira.shift(); if (is) w.send(is); else { w.send({ bitti: true }); res(); } };
    w.on('message', m => { if (m.hazir) ver(); if (m.fin !== undefined) { ortalar.push(m.ort); process.stdout.write(`parça ${m.fin} (kare ort. ${m.ort.toFixed(0)} ms) `); ver(); } });
  })));
  srv.close();
  fs.writeFileSync(path.join(dir, 'liste.txt'), isler.map(i => `file '${path.basename(i.out)}'`).join('\n'));
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(dir, 'liste.txt'), '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000',
    '-map', '0:v', '-map', '1:a', '-shortest', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-metadata:s:a:0', 'language=tur', '-movflags', '+faststart', cikti], { stdio: 'inherit' });
  await bekle(ff);
  for (const i of isler) fs.unlinkSync(i.out); fs.unlinkSync(path.join(dir, 'liste.txt')); fs.rmdirSync(dir);
  const sn = (Date.now() - t0) / 1000, ort = ortalar.reduce((a, b) => a + b, 0) / ortalar.length;
  console.log(`\nbitti: ${cikti} | ${sn.toFixed(0)} sn duvar saati, ${((f1 - f0) / sn).toFixed(2)} kare/sn toplam, tek işçide çizim ort. ${ort.toFixed(0)} ms/kare (4 işçi aynı çekirdekleri paylaşır)`);
}
(process.env._ISCI ? isci() : usta()).catch(e => { console.error(e); process.exit(1); });
