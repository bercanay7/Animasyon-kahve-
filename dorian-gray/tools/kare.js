// Tek kareler: node tools/kare.js <klasör> t1 t2 ... | P012 P013 (plan kimliği: plan ortası) ; EXTRA='notext=1'
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'); const S = require('./sunucu');
(async () => {
  const [out, ...ts] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const srv = await S.baslat(), br = await chromium.launch();
  try {
    const p = await S.sayfa(br, srv.address().port, process.env.EXTRA || '');
    for (const a of ts) {
      const t = /^P\d+/.test(a) ? await p.evaluate(id => { const i = SHOTS.findIndex(s => s.id === id); if (i < 0) return -1; shotAt(0); const j = SHOTS.findIndex(s => s.id === id); const st = shotState(j, SHOTS[j].at); return SHOTS[j].at + st.d * .6; }, a) : +a;
      if (t < 0) { console.log('plan yok', a); continue; }
      const t0 = Date.now(); const b64 = await p.evaluate(t => renderFrame(t).toDataURL('image/png').split(',')[1], t);
      const fn = path.join(out, (/^P/.test(a) ? a + '_' : 't') + t.toFixed(2) + '.png'); fs.writeFileSync(fn, Buffer.from(b64, 'base64'));
      console.log(fn, Date.now() - t0, 'ms');
    }
  } finally { await br.close(); srv.close(); }
})();
