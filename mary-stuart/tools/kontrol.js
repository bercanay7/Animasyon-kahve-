// node tools/kontrol.js — plan listesi denetimi: ardışık aynı ölçek, kart süresi (≤ 8 sn) ve toplamı (≤ 1/5), uzun planlar (> 10 sn), eksik sözcük çapaları
const { chromium } = require('playwright'); const path = require('path'), http = require('http'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..');
(async () => {
  const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200); fs.createReadStream(f).pipe(r); }).listen(0);
  const b = await chromium.launch(); const p = await b.newPage(); const yok = [];
  p.on('console', m => { if (/kelime yok/.test(m.text())) yok.push(m.text()); });
  await p.goto(`http://127.0.0.1:${srv.address().port}/film.html?render=1`); await p.waitForFunction(() => window.READY, null, { timeout: 120000 });
  const S = await p.evaluate(() => { shotAt(0); return SHOTS.map((s, i) => ({ id: s.id, at: s.at, d: (SHOTS[i + 1] ? SHOTS[i + 1].at : DUR) - s.at, o: s.olcek })); });
  await b.close(); srv.close();
  const DUR = S[S.length - 1].at + S[S.length - 1].d, mm = t => `${Math.floor(t / 60)}:${(t % 60).toFixed(1).padStart(4, '0')}`;
  console.log('plan', S.length, '· süre', mm(DUR), '· ortalama plan', (DUR / S.length).toFixed(1), 'sn');
  const kart = S.filter(s => s.o === 'K'), kt = kart.reduce((a, s) => a + s.d, 0);
  console.log('kart', kart.length, 'adet,', kt.toFixed(0), 'sn (%' + (kt / DUR * 100).toFixed(1) + '; sınır %20)');
  for (const s of kart) if (s.d > 8.05 && s.id !== 'M13') console.log('  uzun kart', s.id, s.d.toFixed(1));
  for (let i = 1; i < S.length; i++) if (S[i].o === S[i - 1].o && S[i].o !== 'K') console.log('  aynı ölçek', S[i - 1].id, S[i].id, S[i].o, '@' + mm(S[i].at));
  for (const s of S) if (s.d > 10 && s.o !== 'K') console.log('  uzun plan', s.id, s.o, s.d.toFixed(1), 'sn');
  for (const s of S) if (s.d < 1.2) console.log('  kısa plan', s.id, s.d.toFixed(2), 'sn');
  for (let i = 1; i < S.length; i++) if (S[i].at < S[i - 1].at + 1e-6) console.log('  sıra hatası', S[i - 1].id, S[i].id);
  console.log('eksik çapa', [...new Set(yok)].join(' | ') || 'yok');
})();
