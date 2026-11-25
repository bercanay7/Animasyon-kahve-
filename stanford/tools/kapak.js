// Kapak çek: node tools/kapak.js <çıktı_klasörü> A '{}' B '{"satir":["DOSTUNU","7 GÜN GÖMMEDİ"]}' ... → <ad>.png ve .jpg (1280×720)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'); const { serve } = require('./sunucu'); const { execFileSync } = require('child_process');
(async () => {
  const [out, ...args] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const srv = await serve(), br = await chromium.launch();
  try {
    const p = await br.newPage({ viewport: { width: 1920, height: 1080 } }); p.on('pageerror', e => console.log('[hata]', e.message));
    await p.goto(`http://127.0.0.1:${srv.address().port}/kapak.html`); await p.waitForFunction(() => window.READY, null, { timeout: 120000 });
    for (let i = 0; i < args.length; i += 2) {
      const v = args[i], o = JSON.parse(args[i + 1] || '{}'), ad = (o.ad || v);
      const b64 = await p.evaluate(([v, o]) => window.kapak(v, o).toDataURL('image/png').split(',')[1], [v, o]);
      const png = path.join(out, ad + '.png'); fs.writeFileSync(png, Buffer.from(b64, 'base64'));
      execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', png, '-vf', 'scale=1280:720:flags=lanczos', '-q:v', '2', path.join(out, ad + '.jpg')]);
      console.log(ad, (fs.statSync(path.join(out, ad + '.jpg')).size / 1e6).toFixed(2), 'MB');
    }
  } finally { await br.close(); srv.close(); }
})();
