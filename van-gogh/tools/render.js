// Van Gogh filmi render: plan başına parça (önbellek), 15 çizim/sn → 30 kare/sn (kare çoğaltma), H.264 CRF 18, BT.709.
// node /home/user/Animasyon-kahve-/van-gogh/tools/render.js <çıktı.mp4>   (mutlak yolla başlat)
// Ortam: WORKERS=3 · ONLY=A01,B02 (yalnız bu planlar) · SS=1.5 · PARCA=klasör (varsayılan van-gogh/.parts) · SES=audio/mix.wav · ARALIK=planA-planB
// Önbellek anahtarı: kod ve zaman çizelgesi özeti + plan kimliği + kare aralığı (KEY). Şüphede .parts elle silinir.
const { chromium } = require('playwright'); const { spawn, fork } = require('child_process'); const crypto = require('crypto');
const path = require('path'), fs = require('fs');
const S = require('../../dorian-gray/tools/sunucu.js');
const KOK = path.join(__dirname, '..'), FPS = 15, N = +(process.env.WORKERS || 3), SS = process.env.SS || '1.5';
const PARCA = process.env.PARCA || path.join(KOK, '.parts');
const X264 = ['-vf', 'scale=in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
  '-c:v', 'libx264', '-preset', process.env.PRESET || 'slow', '-crf', process.env.CRF || '18', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-g', '60', '-r', '30'];
const bekle = p => new Promise((r, j) => p.on('close', c => (c === 0 ? r() : j(new Error('ffmpeg ' + c)))));
function ozet() {
  const h = crypto.createHash('sha1'), ekle = f => h.update(fs.readFileSync(f));
  for (const d of [path.join(KOK, 'lib'), path.join(KOK, '..', 'araclar', 'tablo')]) for (const f of fs.readdirSync(d).filter(f => /\.js$/.test(f)).sort()) ekle(path.join(d, f));
  for (const f of ['film.html', 'timeline.js']) ekle(path.join(KOK, f));
  // figür klipleri anahtara girmez (yeniden çizilen klip parçayı bozmaz; gerekirse ONLY= ile plan yeniden çizilir)
  return h.digest('hex').slice(0, 10);
}
async function isci() {
  const br = await chromium.launch(), p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('[hata]', e.message));
  await p.goto(`http://127.0.0.1:${process.env._PORT}/van-gogh/film.html?render=1&ss=${SS}`);
  await p.waitForFunction(() => window.READY || window.HATA, null, { timeout: 900000 });
  process.on('message', async is => {
    if (is.bitti) { await br.close(); process.exit(0); }
    const tmp = is.out + '.tmp.mp4';
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', ...X264, tmp], { stdio: ['pipe', 'ignore', 'inherit'] });
    let top = 0;
    for (let i = is.f0; i < is.f1; i++) {
      const r = await p.evaluate(t => { const a = performance.now(); window.renderAt(t); window.BITIR(); return { d: performance.now() - a, u: document.getElementById('c').toDataURL('image/jpeg', .95).split(',')[1] }; }, (i + .5) / FPS);
      top += r.d; if (!ff.stdin.write(Buffer.from(r.u, 'base64'))) await new Promise(r_ => ff.stdin.once('drain', r_));
    }
    ff.stdin.end(); await bekle(ff); fs.renameSync(tmp, is.out);
    process.send({ fin: is.id, ort: top / Math.max(1, is.f1 - is.f0), n: is.f1 - is.f0 });
  });
  process.send({ hazir: true });
}
async function usta() {
  const cikti = process.argv[2]; if (!cikti) { console.error('Kullanım: node van-gogh/tools/render.js çıktı.mp4'); process.exit(1); }
  fs.mkdirSync(PARCA, { recursive: true });
  const srv = await S.baslat(), port = srv.address().port;
  const br = await chromium.launch(), p = await br.newPage();
  await p.goto(`http://127.0.0.1:${port}/van-gogh/film.html?render=1&ss=1`);
  await p.waitForFunction(() => window.READY || window.HATA, null, { timeout: 900000 });
  const { PL, DUR } = await p.evaluate(() => ({ PL: window.PLANLAR, DUR: window.DUR })); await br.close();
  const KEY = ozet(), FT = Math.round(DUR * FPS);
  const isler = PL.map((q, i) => { const f0 = Math.round(q.s * FPS), f1 = i + 1 < PL.length ? Math.round(PL[i + 1].s * FPS) : FT; return { id: q.id, f0, f1, out: path.join(PARCA, `${String(i).padStart(3, '0')}_${q.id}_${f0}_${f1}_${KEY}.mp4`) }; }).filter(q => q.f1 > q.f0);
  const sec = process.env.ONLY ? process.env.ONLY.split(',') : null;
  const yap = isler.filter(q => (!sec || sec.includes(q.id)) && !fs.existsSync(q.out)).sort((a, b) => (b.f1 - b.f0) - (a.f1 - a.f0));   // uzun planlar önce
  console.log(`${isler.length} plan, ${FT} çizim (15/sn); yapılacak ${yap.length} plan, ${yap.reduce((a, q) => a + q.f1 - q.f0, 0)} çizim; anahtar ${KEY}`);
  const t0 = Date.now(); let biten = 0;
  await Promise.all(Array.from({ length: Math.min(N, yap.length) }, () => new Promise(res => {
    const w = fork(__filename, [], { env: { ...process.env, _ISCI: '1', _PORT: port } });
    const ver = () => { const is = yap.shift(); if (is) w.send(is); else { w.send({ bitti: true }); res(); } };
    w.on('message', m => { if (m.hazir) ver(); if (m.fin) { biten += m.n; console.log(`${m.fin} ${m.n} çizim, ort ${m.ort.toFixed(0)} ms | toplam ${biten}, ${((Date.now() - t0) / 1000 / 60).toFixed(1)} dk`); ver(); } });
  })));
  srv.close();
  if (sec) { console.log('ONLY: birleştirme atlandı'); return; }
  const eksik = isler.filter(q => !fs.existsSync(q.out)); if (eksik.length) { console.log('eksik parça:', eksik.map(q => q.id).join(',')); return; }
  const liste = path.join(PARCA, 'liste.txt'); fs.writeFileSync(liste, isler.map(i => `file '${path.basename(i.out)}'`).join('\n'));
  const ses = process.env.SES || path.join(KOK, 'audio', 'mix.wav');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', liste, ...(fs.existsSync(ses) ? ['-i', ses, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '192k', '-metadata:s:a:0', 'language=tur'] : []),
    '-c:v', 'copy', '-movflags', '+faststart', '-shortest', cikti], { stdio: 'inherit' });
  await bekle(ff); console.log('bitti:', cikti, ((Date.now() - t0) / 60000).toFixed(1), 'dk');
}
(process.env._ISCI ? isci() : usta()).catch(e => { console.error(e); process.exit(1); });
