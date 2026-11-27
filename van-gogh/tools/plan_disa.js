// node van-gogh/tools/plan_disa.js → van-gogh/vo/planlar.json (plan tablosu: id, sahne, ölçek, başlangıç, süre, not) — miks ve plan listesi için
const { chromium } = require('playwright'); const S = require('../../dorian-gray/tools/sunucu.js'); const fs = require('fs'), path = require('path');
(async () => { const srv = await S.baslat(), br = await chromium.launch(), p = await br.newPage();
  await p.goto(`http://127.0.0.1:${srv.address().port}/van-gogh/film.html?render=1&ss=1`); await p.waitForFunction(() => window.READY || window.HATA, null, { timeout: 600000 });
  const P = await p.evaluate(() => ({ planlar: window.PLANLAR, dur: window.DUR })); fs.writeFileSync(path.join(__dirname, '..', 'vo', 'planlar.json'), JSON.stringify(P, null, 1));
  console.log(P.planlar.length, 'plan'); await br.close(); srv.close(); })();
