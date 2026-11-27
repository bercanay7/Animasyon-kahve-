// Orfeus kapağı (kapak sistemi, 27 Kasım): node <mutlak>/orfeus/tools/kapak.js <çıktı_klasörü> <ad> '<json>'
//   ör. node orfeus/tools/kapak.js orfeus/kapak A '{}'   ·   node orfeus/tools/kapak.js orfeus/kapak A_yazisiz '{"yazisiz":1}'
// Her sürüm ayrı node süreciyle çekilir (Gılgamış dersi: sayfanın ilk çizimi sonrakilerden ayrılabiliyor). Çıktı: <ad>.png (1920, ara dosya) + <ad>.jpg (1280×720).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'); const { serve } = require('./sunucu'); const { execFileSync } = require('child_process');
(async () => {
  const [out, ad, js] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true }); const o = JSON.parse(js || '{}');
  const srv = await serve(), br = await chromium.launch();
  try {
    const p = await br.newPage({ viewport: { width: 1920, height: 1080 } }); p.on('pageerror', e => console.log('[hata]', e.message)); p.on('console', m => console.log('[sayfa]', m.text()));
    await p.goto(`http://127.0.0.1:${srv.address().port}/kapak_sistem.html`); await p.waitForFunction(() => window.READY, null, { timeout: 120000 });
    const b64 = await p.evaluate(o => window.kapak(o).toDataURL('image/png').split(',')[1], o);
    const png = path.join(out, ad + '.png'); fs.writeFileSync(png, Buffer.from(b64, 'base64'));
    execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', png, '-vf', 'scale=1280:720:flags=lanczos', '-q:v', '2', path.join(out, ad + '.jpg')]);
    console.log(ad, (fs.statSync(path.join(out, ad + '.jpg')).size / 1e6).toFixed(2), 'MB');
  } finally { await br.close(); srv.close(); }
})();
