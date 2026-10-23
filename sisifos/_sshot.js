const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => { const [out, ...ts] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--disable-web-security'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('[err]', e.message));
  await p.goto('file://' + path.resolve(__dirname, 'shorts.html') + '?render=1&rs=2&notext=1'); await p.evaluate(() => window.ready);
  for (const t of ts) { const b64 = await p.evaluate(t => renderShortFrame(+t, 1).toDataURL('image/jpeg', .9).split(',')[1], t); fs.writeFileSync(path.join(out, `s${(+t).toFixed(2).padStart(6, '0')}.jpg`), Buffer.from(b64, 'base64')); }
  await b.close(); })();
