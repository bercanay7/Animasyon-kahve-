// Belirli planlardan kare (planın oranı p, varsayılan .55) ve küçük montaj: node tools/kareler.js ÇIKTI.png ID[@p] ID[@p] ...
const { chromium } = require('playwright'); const { serve } = require('./sunucu'); const fs = require('fs');
(async () => {
  const out = process.argv[2], ids = process.argv.slice(3);
  const srv = await serve(), b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('HATA', e.message)); p.on('console', m => { if (/yok|bozuk|iki kez/.test(m.text())) console.log('k:', m.text()); });
  await p.goto(`http://127.0.0.1:${srv.address().port}/film.html?render=1`); await p.waitForFunction(() => window.READY, null, { timeout: 120000 });
  const url = await p.evaluate(async (ids) => {
    const L = window.shotList(), W = 640, H = 360, cols = 2, rows = Math.ceil(ids.length / cols);
    const m = document.createElement('canvas'); m.width = W * cols; m.height = H * rows; const x = m.getContext('2d');
    ids.forEach((q, k) => { const [id, pp] = q.split('@'); const s = L.find(s => s.id === id); if (!s) return; const t = typeof pp === 'string' && pp.startsWith('t') ? +pp.slice(1) : s.at + (s.end - s.at) * (+(pp ?? .55)); const c = window.renderAt(t, 1); x.drawImage(c, (k % cols) * W, Math.floor(k / cols) * H, W, H); x.fillStyle = '#fff'; x.font = '18px sans-serif'; x.fillText(q + ' t=' + t.toFixed(1), (k % cols) * W + 8, Math.floor(k / cols) * H + 22); });
    return m.toDataURL('image/png');
  }, ids);
  fs.writeFileSync(out, Buffer.from(url.split(',')[1], 'base64')); await b.close(); srv.close();
})();
