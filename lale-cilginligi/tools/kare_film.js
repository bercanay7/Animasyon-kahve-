// node tools/kare_film.js t çıktı.png [genişlik]  (film.html'den tek kare)
const { chromium } = require('playwright'); const S = require('./sunucu');
(async () => { const [t, out, w] = process.argv.slice(2); const srv = await S.baslat(); const br = await chromium.launch();
  const p = await S.sayfa(br, srv.address().port, '');
  const b64 = await p.evaluate(([t, w]) => { const c = renderFrame(+t); if (!w) return c.toDataURL('image/png').split(',')[1]; const s = document.createElement('canvas'); s.width = +w; s.height = Math.round(+w * 9 / 16); s.getContext('2d').drawImage(c, 0, 0, s.width, s.height); return s.toDataURL('image/png').split(',')[1]; }, [t, w]);
  require('fs').writeFileSync(out, Buffer.from(b64, 'base64')); await br.close(); srv.close(); })();
