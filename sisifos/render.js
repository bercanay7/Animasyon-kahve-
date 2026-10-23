// Tam film render: node render.js [çıktı.mp4]
// Ortam: WORKERS=4 (paralel Chromium), MB=4 (hareket bulanıklığı alt kare), CRF=20, FROM/TO (sn, kısmi render), NOAUDIO=1
// Her işçi kendi aralığını ayrı bir parçaya kodlar; parçalar yeniden kodlamadan birleştirilip miks ile paketlenir.
const { chromium } = require('playwright');
const { spawn, fork } = require('child_process');
const path = require('path');
const fs = require('fs');

const FPS = 30;
const CRF = process.env.CRF || '20';
const X264 = ['-c:v', 'libx264', '-preset', process.env.PRESET || 'slow', '-crf', CRF, '-profile:v', 'high', '-pix_fmt', 'yuv420p',
  '-g', '60', '-bf', '3', '-x264-params', 'aq-mode=3:aq-strength=0.9:psy-rd=1.0,0.15'];
const ffwait = p => new Promise((res, rej) => p.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));

async function worker(a, b, out) {
  const browser = await chromium.launch({ args: ['--disable-web-security'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.log('[err]', e.message));
  await page.goto('file://' + path.resolve(__dirname, 'film.html') + '?render=1');
  await page.evaluate(() => window.ready);
  const mb = +(process.env.MB || 4);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', ...X264, '-r', String(FPS), out],
    { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let i = a; i < b; i++) {
    const b64 = await page.evaluate(({ t, mb }) => {
      mb > 1 ? renderFrameMB(t, mb) : renderFrame(t);
      return document.getElementById('c').toDataURL('image/jpeg', .96).split(',')[1];
    }, { t: i / FPS, mb });
    if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (process.send && (i - a) % 15 === 0) process.send({ done: i - a });
  }
  ff.stdin.end();
  await ffwait(ff);
  await browser.close();
}

async function master() {
  const out = path.resolve(process.argv[2] || 'sisifos.mp4');
  const DUR = +fs.readFileSync(path.join(__dirname, 'timeline.js'), 'utf8').match(/window\.DUR\s*=\s*([\d.]+)/)[1];
  const f0 = Math.round((+process.env.FROM || 0) * FPS), f1 = Math.round((process.env.TO ? +process.env.TO : DUR) * FPS);
  const nW = +(process.env.WORKERS || 4), tmp = path.join(path.dirname(out), '.parts');
  fs.mkdirSync(tmp, { recursive: true });
  const step = Math.ceil((f1 - f0) / nW), parts = [], prog = new Array(nW).fill(0), t0 = Date.now();
  const jobs = [];
  for (let k = 0; k < nW; k++) {
    const a = f0 + k * step, b = Math.min(f1, a + step);
    if (a >= b) break;
    const p = path.join(tmp, `part${k}.mp4`); parts.push(p);
    const ch = fork(__filename, ['--worker', a, b, p]);
    ch.on('message', m => {
      prog[k] = m.done;
      const d = prog.reduce((x, y) => x + y, 0), el = (Date.now() - t0) / 1000;
      process.stdout.write(`\r${d}/${f1 - f0} kare  ${el.toFixed(0)} sn  kalan ~${(el / Math.max(d, 1) * (f1 - f0 - d) / 60).toFixed(1)} dk   `);
    });
    jobs.push(new Promise((res, rej) => ch.on('exit', c => c === 0 ? res() : rej(new Error('işçi ' + k + ' çıktı: ' + c)))));
  }
  await Promise.all(jobs);
  const list = path.join(tmp, 'list.txt');
  fs.writeFileSync(list, parts.map(p => `file '${p}'`).join('\n'));
  const mix = path.join(__dirname, 'audio', 'mix.wav');
  const audio = !process.env.NOAUDIO && fs.existsSync(mix)
    ? ['-ss', String(f0 / FPS), '-t', String((f1 - f0) / FPS), '-i', mix, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000']
    : [];
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, ...audio, '-c:v', 'copy', '-movflags', '+faststart', '-shortest', out],
    { stdio: ['ignore', 'ignore', 'inherit'] });
  await ffwait(ff);
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(`\nHazır: ${out}  (${(fs.statSync(out).size / 1e6).toFixed(1)} MB, ${((Date.now() - t0) / 60000).toFixed(1)} dk)`);
}

if (process.argv[2] === '--worker') worker(+process.argv[3], +process.argv[4], process.argv[5]).then(() => process.exit(0), e => { console.error(e); process.exit(1); });
else master().catch(e => { console.error(e); process.exit(1); });
