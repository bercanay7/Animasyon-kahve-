// Kapak çek: node tools/kapak.js <çıktı_klasörü> A '{"z":1.4}' B '{}' ...  → <ad>.png (1920×1080) ve .jpg (1280×720, <2 MB)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'); const S = require('./sunucu'); const { execFileSync } = require('child_process');
(async () => {
  const [out, ...args] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const srv = await S.baslat(), br = await chromium.launch();
  try {
    const p = await br.newPage({ viewport: { width: 1920, height: 1080 } }); p.on('pageerror', e => console.log('[hata]', e.message));
    await p.goto(`http://127.0.0.1:${srv.address().port}/dorian-gray/kapak.html?render=1`);
    await p.waitForFunction(() => window.READY || window.HATA, null, { timeout: 300000 });
    await p.evaluate(() => document.fonts.load('400 200px "Bebas Neue"', 'KİMSE GÖRMEDİ GERÇEK YÜZÜ BURADA ŞÜÇ'));
    for (let i = 0; i < args.length; i += 2) {
      const v = args[i], o = JSON.parse(args[i + 1] || '{}'), ad = (o.ad || v);
      const b64 = await p.evaluate(([v, o]) => window.kapak(v, o).toDataURL('image/png').split(',')[1], [v, o]);
      const png = path.join(out, ad + '.png'); fs.writeFileSync(png, Buffer.from(b64, 'base64'));
      execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', png, '-vf', 'scale=1280:720:flags=lanczos', '-q:v', '2', path.join(out, ad + '.jpg')]);
      console.log(ad, (fs.statSync(path.join(out, ad + '.jpg')).size / 1e6).toFixed(2), 'MB');
    }
  } finally { await br.close(); srv.close(); }
})();
