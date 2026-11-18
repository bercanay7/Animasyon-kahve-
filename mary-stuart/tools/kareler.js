// node tools/kareler.js [klasör] — her plandan iki tam boy kare (%35 ve %85 anında), denetim için; ayrıca liste.json (id, ölçek, zaman, anlatım)
const { chromium } = require('playwright'); const path = require('path'), http = require('http'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
(async () => {
  const dir = path.resolve(process.argv[2] || 'animatik/denetim'); fs.mkdirSync(dir, { recursive: true });
  const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200); fs.createReadStream(f).pipe(r); }).listen(0);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(`http://127.0.0.1:${srv.address().port}/film.html?render=1`); await p.waitForFunction(() => window.READY, null, { timeout: 120000 });
  const shots = await p.evaluate(() => { shotAt(0); return SHOTS.map((s, i) => { const e = SHOTS[i + 1] ? SHOTS[i + 1].at : DUR; return { id: s.id, olcek: s.olcek, at: s.at, end: e }; }); });
  const seg = JSON.parse(fs.readFileSync(path.join(ROOT, 'senaryo.json'), 'utf8')).segments, tl = fs.readFileSync(path.join(ROOT, 'timeline.js'), 'utf8');
  const CUES = JSON.parse(tl.split('window.CUES = ')[1].split(';\n')[0]);
  const liste = [];
  for (const s of shots) {
    const anlat = seg.filter(x => CUES[x.id].e > s.at && CUES[x.id].s < s.end).map(x => x.id + ': ' + x.alt).join(' / ');
    const kare = [];
    for (const [k, f] of [['a', .35], ['b', .85]]) { const t = s.at + (s.end - s.at) * f; const b64 = await p.evaluate(t => renderFrame(t).toDataURL('image/jpeg', .82).split(',')[1], t); const fn = `${s.id}_${k}.jpg`; fs.writeFileSync(path.join(dir, fn), Buffer.from(b64, 'base64')); kare.push(fn); }
    liste.push({ ...s, at: +s.at.toFixed(2), end: +s.end.toFixed(2), kare, anlatim: anlat });
  }
  fs.writeFileSync(path.join(dir, 'liste.json'), JSON.stringify(liste, null, 1)); await b.close(); srv.close(); console.log(liste.length, 'plan,', liste.length * 2, 'kare →', dir);
})();
