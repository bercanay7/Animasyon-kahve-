// Plan listesi (render etmeden): node tools/plan_listesi.js > planlar.json  → [{id, at, d, set, olcek}]
const { chromium } = require('playwright'); const S = require('./sunucu');
(async () => { const srv = await S.baslat(), br = await chromium.launch();
  try { const p = await S.sayfa(br, srv.address().port, '');
    const L = await p.evaluate(() => { shotAt(0); return SHOTS.map((s, i) => { const st = shotState(i, s.at); const P = window.PLAN[s.id] || {}; return { id: s.id, at: +s.at.toFixed(2), d: +st.d.toFixed(2), set: P.set, olcek: P.olcek }; }); });
    process.stdout.write(JSON.stringify(L, null, 0)); } finally { await br.close(); srv.close(); } })();
