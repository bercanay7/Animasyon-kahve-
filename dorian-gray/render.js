// Render (Dorian Gray): node /home/user/Animasyon-kahve-/dorian-gray/render.js [çıktı.mp4]   (mutlak yolla başlat: depo kökünde ilgisiz bir render.js var)
// Ortam:
//   WORKERS=4  paralel Chromium işçisi        (hareket bulanıklığı yok: gravür çizgisi ve portre karesi pahalı)
//   CRF=18  PRESET=slow  CHUNK=24 (sn)       ONLY=3,7  yalnız bu parçaları yeniden üret (öbür parçalar eski anahtarla da olsa korunur; uyarı yazılır)
//   ANIMATIK=1  hızlı animatik: 960×540, MB=1, CRF 23, veryfast, ayrı parça klasörü (.parts_animatik)
//   ARALIK=0-20  yalnız bu saniye aralığı (kendi parça klasörü; ses de kırpılır)
//   AUDIO=audio/mix.wav (yoksa vo/vo.wav; NOAUDIO=1 sessiz)   Q='notext=1' ek sayfa parametresi   PARTS=.parts (parça klasörü)
// Parça önbelleği: her parçanın yanında .key dosyası; anahtar = film.html'in yüklediği bütün kod + timeline.js + planlar.js + fonts + görseller + ayarlar.
// Anahtar değişince eski parça yeniden üretilir (29 Ekim dersi: kod değişse bile eski kareleri sessizce kullanmak).
// Çıktı: H.264 High, yuv420p, BT.709 etiketleri, AAC 256k 48 kHz, ses dili 'tur'; +faststart.
const { chromium } = require('playwright');
const { spawn, fork } = require('child_process');
const path = require('path'), fs = require('fs'), crypto = require('crypto');
const S = require('./tools/sunucu'); const ROOT = __dirname;

const FPS = 30;
const ANIM = !!process.env.ANIMATIK;
const RS = ANIM ? .5 : +(process.env.RS || 1);
const VW = Math.round(1920 * RS), VH = Math.round(1080 * RS);
const MB = 1;
const EXTRA = process.env.Q || '';
const PRESET = process.env.PRESET || (ANIM ? 'veryfast' : 'slow'), CRF = process.env.CRF || (ANIM ? '23' : '18');
// renk: JPEG kareler (tam aralık, BT.601) → BT.709 sınırlı aralık, akışta BT.709 etiketleri
const X264 = ['-vf', 'scale=in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
  '-c:v', 'libx264', '-preset', PRESET, '-crf', CRF, '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-g', '60', '-bf', '3'];
const ffwait = p => new Promise((res, rej) => p.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));

// ---- işçi ----
async function worker() {
  const port = +process.env._PORT;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: VW, height: VH } });
  page.on('pageerror', e => console.log('[hata]', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('[konsol]', m.text()); });
  const q = ['render=1', RS !== 1 ? 'rs=' + RS : '', EXTRA].filter(Boolean).join('&');
  await page.goto(`http://127.0.0.1:${port}/dorian-gray/film.html?${q}`);
  await page.waitForFunction(() => window.READY || window.HATA, null, { timeout: 300000 });
  const hata = await page.evaluate(() => window.HATA); if (hata) throw new Error(hata);
  const jq = ANIM ? .85 : .96;
  process.on('message', async job => {
    if (job.quit) { await browser.close(); process.exit(0); }
    const tmp = job.out + '.tmp.mp4';
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', ...X264, '-r', String(FPS), tmp], { stdio: ['pipe', 'ignore', 'inherit'] });
    for (let i = job.a; i < job.b; i++) {
      const b64 = await page.evaluate(({ t, mb, jq }) => window.renderFrame(t).toDataURL('image/jpeg', jq).split(',')[1], { t: i / FPS, mb: MB, jq });
      if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
      if ((i - job.a) % 15 === 0) process.send({ prog: job.k, done: i - job.a });
    }
    ff.stdin.end(); await ffwait(ff);
    fs.renameSync(tmp, job.out); fs.writeFileSync(job.out + '.key', job.key);
    process.send({ fin: job.k });
  });
  process.send({ ready: true });
}

// ---- anahtar: sayfanın yüklediği her şey + ayarlar ----
function renderKey() {
  const h = crypto.createHash('sha1');
  const html = fs.readFileSync(path.join(ROOT, 'film.html'), 'utf8');
  const files = ['film.html', '../milton/fonts.css', 'kapi/vendor/impasto.js', 'kapi/vendor/plate.js', ...[...html.matchAll(/<script[^>]* src="([^"]+)"/g)].map(m => m[1])];
  for (const d of ['gorsel']) for (const f of fs.readdirSync(path.join(ROOT, d)).sort()) { const p = path.join(d, f); if (fs.statSync(path.join(ROOT, p)).isFile()) files.push(p); }
  for (const f of files) { h.update(f + '\0'); h.update(fs.readFileSync(path.join(ROOT, f))); }
  h.update(JSON.stringify({ FPS, RS, MB, EXTRA, PRESET, CRF }));
  return h.digest('hex').slice(0, 16);
}

async function master() {
  const out = path.resolve(process.argv[2] || path.join(ROOT, ANIM ? 'dorian_animatik.mp4' : 'dorian-gray.mp4'));
  const DUR = +fs.readFileSync(path.join(ROOT, 'timeline.js'), 'utf8').match(/window\.DUR\s*=\s*([\d.]+)/)[1];
  const [ra, rb] = process.env.ARALIK ? process.env.ARALIK.split('-').map(Number) : [0, DUR];
  const f0 = Math.round(ra * FPS), f1 = Math.min(Math.round(rb * FPS), Math.round(DUR * FPS)), CH = Math.round((+process.env.CHUNK || 24) * FPS);
  const dir = path.join(ROOT, process.env.PARTS || ((ANIM ? '.parts_animatik' : '.parts') + (process.env.ARALIK ? '_' + ra + '-' + rb : '')));
  fs.mkdirSync(dir, { recursive: true });
  const key = renderKey();
  const chunks = [];
  for (let a = f0, k = 0; a < f1; a += CH, k++) chunks.push({ k, a, b: Math.min(f1, a + CH), key, out: path.join(dir, `c${String(k).padStart(3, '0')}.mp4`) });
  const valid = c => fs.existsSync(c.out) && fs.existsSync(c.out + '.key') && fs.readFileSync(c.out + '.key', 'utf8') === key;
  const only = process.env.ONLY ? process.env.ONLY.split(',').map(Number) : null;
  const todo = chunks.filter(c => only ? (only.includes(c.k) || !fs.existsSync(c.out)) : !valid(c));
  if (only) { const eski = chunks.filter(c => !todo.includes(c) && !valid(c)).map(c => c.k); if (eski.length) console.log(`UYARI: ONLY ile eski anahtarlı parçalar korunuyor: ${eski.join(',')}`); }
  console.log(`anahtar ${key} | ${ANIM ? 'ANIMATİK ' : ''}${VW}×${VH} MB=${MB} CRF=${CRF} | ${(ra).toFixed(1)}–${(f1 / FPS).toFixed(1)} sn | ${chunks.length} parça, ${todo.length} render edilecek`);
  const srv = await S.baslat(), port = srv.address().port;
  const nW = Math.min(+(process.env.WORKERS || 4), todo.length), t0 = Date.now(), prog = {};
  let doneFrames = 0; const need = todo.reduce((s, c) => s + c.b - c.a, 0);
  await Promise.all(Array.from({ length: nW }, () => new Promise((res, rej) => {
    const w = fork(__filename, ['--worker'], { env: { ...process.env, _PORT: String(port) } });
    const next = () => { const j = todo.shift(); if (j) w.send(j); else w.send({ quit: true }); };
    w.on('message', m => {
      if (m.ready) next();
      if (m.prog !== undefined) prog[m.prog] = m.done;
      if (m.fin !== undefined) { const c = chunks[m.fin]; doneFrames += c.b - c.a; delete prog[m.fin]; next(); }
      const d = doneFrames + Object.values(prog).reduce((s, v) => s + v, 0), el = (Date.now() - t0) / 1000;
      process.stdout.write(`\r${d}/${need} kare  ${el.toFixed(0)} sn  ${(el / Math.max(d, 1) * nW).toFixed(2)} sn/kare/işçi  kalan ~${(el / Math.max(d, 1) * (need - d) / 60).toFixed(1)} dk   `);
    });
    w.on('exit', c => c === 0 ? res() : rej(new Error('işçi çıktı: ' + c)));
  })));
  srv.close();
  const list = path.join(dir, 'list.txt');
  fs.writeFileSync(list, chunks.map(c => `file '${c.out}'`).join('\n'));
  const mixP = process.env.AUDIO ? path.resolve(ROOT, process.env.AUDIO) : [path.join(ROOT, 'audio', 'mix.wav'), path.join(ROOT, 'vo', 'vo.wav')].find(f => fs.existsSync(f));
  const audio = !process.env.NOAUDIO && mixP && fs.existsSync(mixP)
    ? [...(ra > 0 ? ['-ss', String(ra)] : []), '-t', String((f1 - f0) / FPS), '-i', mixP, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-metadata:s:a:0', 'language=tur'] : [];
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, ...audio, '-c:v', 'copy', '-movflags', '+faststart', '-shortest', out], { stdio: ['ignore', 'ignore', 'inherit'] });
  await ffwait(ff);
  console.log(`\nHazır: ${out}  (${(fs.statSync(out).size / 1e6).toFixed(1)} MB, ${((Date.now() - t0) / 60000).toFixed(1)} dk; ses: ${audio.length ? path.relative(ROOT, mixP) : 'yok'})`);
}

if (process.argv[2] === '--worker') worker().catch(e => { console.error(e); process.exit(1); });
else master().catch(e => { console.error(e); process.exit(1); });
