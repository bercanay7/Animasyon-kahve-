// Render: node render.js [çıktı.mp4]
// Ortam: WORKERS=4, MB=4 (hareket bulanıklığı alt kare), CRF=18, CHUNK=24 (sn), ONLY=3,7 (yalnız bu parçaları yeniden üret),
//        AUDIO=audio/mix.wav (NOAUDIO=1 ile sessiz), PAGE=film.html, Q='rs=2&notext=1' (ek sayfa parametreleri),
//        SHORTS=1 (shorts.html'deki dikey kurguyu 1080×1920 üretir), PARTS=.parts (kalıcı parça klasörü)
// Film sabit uzunlukta parçalara bölünür; parçalar kalıcıdır, böylece bir düzeltmeden sonra yalnızca etkilenen parça yeniden render edilir.
const { chromium } = require('playwright');
const { spawn, fork } = require('child_process');
const path = require('path');
const fs = require('fs');

const FPS = 30;
const SHORTS = !!process.env.SHORTS;
const PAGE = process.env.PAGE || (SHORTS ? 'shorts.html' : 'film.html');
const EXTRA = process.env.Q || (SHORTS ? 'rs=2&notext=1' : '');
// renk: JPEG kareler (tam aralık, BT.601) → BT.709 sınırlı aralık, akışta BT.709 etiketleri (HD standardı)
const X264 = ['-vf', 'scale=in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:v', 'libx264', '-preset', process.env.PRESET || 'slow', '-crf', process.env.CRF || '18', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
  '-g', '60', '-bf', '3', '-x264-params', 'aq-mode=3:aq-strength=0.9:psy-rd=1.0,0.15'];
const ffwait = p => new Promise((res, rej) => p.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));

async function worker() {
  const browser = await chromium.launch({ args: ['--disable-web-security'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.log('[err]', e.message));
  await page.goto('file://' + path.resolve(__dirname, PAGE) + '?render=1' + (EXTRA ? '&' + EXTRA : ''));
  await page.evaluate(() => window.ready);
  const mb = +(process.env.MB || 4);
  process.on('message', async job => {
    if (job.quit) { await browser.close(); process.exit(0); }
    const tmp = job.out + '.tmp.mp4';
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', ...X264, '-r', String(FPS), tmp],
      { stdio: ['pipe', 'ignore', 'inherit'] });
    for (let i = job.a; i < job.b; i++) {
      const b64 = await page.evaluate(({ t, mb, shorts }) => {
        const cv = shorts ? renderShortFrame(t, mb) : (mb > 1 ? renderFrameMB(t, mb) : renderFrame(t), document.getElementById('c'));
        return cv.toDataURL('image/jpeg', .96).split(',')[1];
      }, { t: i / FPS, mb, shorts: SHORTS });
      if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
      if ((i - job.a) % 15 === 0) process.send({ prog: job.k, done: i - job.a });
    }
    ff.stdin.end();
    await ffwait(ff);
    fs.renameSync(tmp, job.out);
    process.send({ fin: job.k });
  });
  process.send({ ready: true });
}

async function master() {
  const out = path.resolve(process.argv[2] || (SHORTS ? 'prometheus_shorts.mp4' : 'prometheus.mp4'));
  let DUR;
  if (SHORTS) DUR = JSON.parse(fs.readFileSync(path.join(__dirname, 'shorts', 'edl.json'), 'utf8')).DUR;
  else DUR = +fs.readFileSync(path.join(__dirname, 'timeline.js'), 'utf8').match(/window\.DUR\s*=\s*([\d.]+)/)[1];
  const total = Math.round(DUR * FPS), CH = Math.round((+process.env.CHUNK || 24) * FPS);
  const dir = path.join(__dirname, process.env.PARTS || (SHORTS ? '.parts_shorts' : '.parts'));
  fs.mkdirSync(dir, { recursive: true });
  const chunks = [];
  for (let a = 0, k = 0; a < total; a += CH, k++) chunks.push({ k, a, b: Math.min(total, a + CH), out: path.join(dir, `c${String(k).padStart(3, '0')}.mp4`) });
  const only = process.env.ONLY ? process.env.ONLY.split(',').map(Number) : null;
  const todo = chunks.filter(c => only ? only.includes(c.k) : !fs.existsSync(c.out));
  console.log(`${chunks.length} parça, ${todo.length} render edilecek`);
  const nW = Math.min(+(process.env.WORKERS || 4), todo.length), t0 = Date.now(), prog = {};
  let doneFrames = 0; const need = todo.reduce((s, c) => s + c.b - c.a, 0);
  await Promise.all(Array.from({ length: nW }, () => new Promise((res, rej) => {
    const w = fork(__filename, ['--worker']);
    const next = () => { const j = todo.shift(); if (j) w.send(j); else w.send({ quit: true }); };
    w.on('message', m => {
      if (m.ready) next();
      if (m.prog !== undefined) { prog[m.prog] = m.done; }
      if (m.fin !== undefined) { doneFrames += chunks[m.fin].b - chunks[m.fin].a; delete prog[m.fin]; next(); }
      const d = doneFrames + Object.values(prog).reduce((s, v) => s + v, 0), el = (Date.now() - t0) / 1000;
      process.stdout.write(`\r${d}/${need} kare  ${el.toFixed(0)} sn  kalan ~${(el / Math.max(d, 1) * (need - d) / 60).toFixed(1)} dk   `);
    });
    w.on('exit', c => c === 0 ? res() : rej(new Error('işçi çıktı: ' + c)));
  })));
  const list = path.join(dir, 'list.txt');
  fs.writeFileSync(list, chunks.map(c => `file '${c.out}'`).join('\n'));
  const mix = path.join(__dirname, process.env.AUDIO || (SHORTS ? 'shorts/mix_shorts.wav' : 'audio/mix.wav'));
  const lang = process.env.LANG3 || (/lang=en/.test(EXTRA) ? 'eng' : 'tur'); // ses kanalının dil etiketi (YouTube ve oynatıcılar için)
  const audio = !process.env.NOAUDIO && fs.existsSync(mix) ? ['-i', mix, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-metadata:s:a:0', `language=${lang}`] : [];
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, ...audio, '-c:v', 'copy', '-movflags', '+faststart', '-shortest', out],
    { stdio: ['ignore', 'ignore', 'inherit'] });
  await ffwait(ff);
  console.log(`\nHazır: ${out}  (${(fs.statSync(out).size / 1e6).toFixed(1)} MB, ${((Date.now() - t0) / 60000).toFixed(1)} dk)`);
}

if (process.argv[2] === '--worker') worker().catch(e => { console.error(e); process.exit(1); });
else master().catch(e => { console.error(e); process.exit(1); });
