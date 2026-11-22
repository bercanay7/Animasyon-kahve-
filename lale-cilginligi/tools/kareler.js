// Birden çok zamandan kare: node tools/kareler.js <klasör> <genişlik> t1 t2 …  → <klasör>/k_<t>.jpg (tek tarayıcı oturumu)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'); const S = require('./sunucu');
(async () => {
  const [out, w, ...ts] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const srv = await S.baslat(), br = await chromium.launch();
  try {
    const p = await S.sayfa(br, srv.address().port, process.env.EXTRA || '');
    for (const t of ts) {
      const b64 = await p.evaluate(([t, w]) => { const c = renderFrame(+t), s = document.createElement('canvas'); s.width = +w; s.height = Math.round(+w * 9 / 16); s.getContext('2d').drawImage(c, 0, 0, s.width, s.height); return s.toDataURL('image/jpeg', .9).split(',')[1]; }, [t, w]);
      fs.writeFileSync(path.join(out, `k_${t}.jpg`), Buffer.from(b64, 'base64'));
    }
  } finally { await br.close(); srv.close(); }
})();
