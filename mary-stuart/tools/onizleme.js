// node tools/onizleme.js t0 t1 çıktı.mp4 [ses.wav] — bir aralığı tam kalitede (30 fps) üç paralel sayfayla render eder; ses vo/vo.wav'dan kesilir
const { chromium } = require('playwright'); const path = require('path'), http = require('http'), fs = require('fs'), { spawn, execFileSync } = require('child_process');
const ROOT = path.resolve(__dirname, '..'), FPS = 30;
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.jpg': 'image/jpeg', '.woff2': 'font/woff2' };
(async () => {
  const [t0, t1] = process.argv.slice(2, 4).map(Number), out = path.resolve(process.argv[4] || 'onizleme.mp4'), ses = process.argv[5] || path.join(ROOT, 'vo/vo.wav');
  const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': MIME[path.extname(f).toLowerCase()] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(0);
  const b = await chromium.launch(), N = 3, f0 = Math.round(t0 * FPS), f1 = Math.round(t1 * FPS), per = Math.ceil((f1 - f0) / N), parts = [];
  await Promise.all(Array.from({ length: N }, async (_, k) => {
    const a = f0 + k * per, e = Math.min(f1, a + per); if (a >= e) return; const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    await p.goto(`http://127.0.0.1:${srv.address().port}/film.html?render=1`); await p.waitForFunction(() => window.READY, null, { timeout: 120000 });
    const tmp = out + `.p${k}.mp4`; parts[k] = tmp;
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-pix_fmt', 'yuv420p', tmp], { stdio: ['pipe', 'ignore', 'inherit'] });
    for (let i = a; i < e; i++) { const b64 = await p.evaluate(t => renderFrame(t).toDataURL('image/jpeg', .92).split(',')[1], i / FPS); if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r)); if (k === 0 && (i - a) % 60 === 0) process.stdout.write(`\r${i - a}/${e - a}`); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }));
  await b.close(); srv.close();
  const list = out + '.txt'; fs.writeFileSync(list, parts.filter(Boolean).map(f => `file '${f}'`).join('\n'));
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-ss', String(t0), '-t', String(t1 - t0), '-i', ses, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', out]);
  for (const f of parts.filter(Boolean)) fs.unlinkSync(f); fs.unlinkSync(list);
  console.log('\nhazır', out, (fs.statSync(out).size / 1e6).toFixed(1), 'MB');
})();
