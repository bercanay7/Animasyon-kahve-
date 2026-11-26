// node kurye/blender/eklem_disa.js [t1,t2,…]  → kurye/blender/eklem.json
// Sahneyi başsız tarayıcıda açar, kuryenin eklemlerini 15 çizim/sn (ya da verilen anlarda) dışa yazar.
const { chromium } = require('playwright'); const S = require('../../dorian-gray/tools/sunucu.js'); const fs = require('fs'), path = require('path');
(async () => {
  const srv = await S.baslat(), br = await chromium.launch(), p = await br.newPage();
  await p.goto(`http://127.0.0.1:${srv.address().port}/kurye/tablo.html?render=1&ss=1`);
  await p.waitForFunction(() => window.READY || window.HATA, null, { timeout: 180000 });
  const ts = process.argv[2] ? process.argv[2].split(',').map(Number) : Array.from({ length: 376 }, (_, k) => k / 15);
  const d = await p.evaluate(ts => ts.map(t => ({ t, ...window.kuryeEklem(t) })), ts);
  fs.writeFileSync(path.join(__dirname, 'eklem.json'), JSON.stringify(d));
  console.log(d.length, 'kare yazıldı');
  await br.close(); srv.close();
})().catch(e => { console.error(e); process.exit(1); });
