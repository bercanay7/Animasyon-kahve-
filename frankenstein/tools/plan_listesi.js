// Normalleştirilmiş çekim listesini yazar: node tools/plan_listesi.js → vo/shots.json [{id, at, end, tr}] (efekt.py ve denetim için)
const { chromium } = require('playwright'); const { serve } = require('./sunucu'); const fs = require('fs'), path = require('path');
(async () => { const srv = await serve(), b = await chromium.launch(), p = await b.newPage();
  p.on('console', m => { if (/yok|bozuk|iki kez/.test(m.text())) console.log('k:', m.text()); });
  await p.goto(`http://127.0.0.1:${srv.address().port}/film.html?render=1`); await p.waitForFunction(() => window.READY, null, { timeout: 120000 });
  const L = await p.evaluate(() => window.shotList().map(s => ({ ...s, olcek: (PLAN[s.id] || {}).olcek, set: (PLAN[s.id] || {}).set })));
  fs.writeFileSync(path.join(__dirname, '..', 'vo', 'shots.json'), JSON.stringify(L, null, 0)); console.log(L.length, 'çekim');
  // denetim: ardışık aynı ölçek, 8 sn'yi aşan kart
  for (let i = 1; i < L.length; i++) if (L[i].olcek === L[i - 1].olcek && L[i].olcek !== 'kart') console.log('aynı ölçek arka arkaya:', L[i - 1].id, L[i].id, L[i].olcek);
  await b.close(); srv.close(); })();
