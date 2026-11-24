// node render.js  → ogretmenler-gunu-story.png (1080x1920), ogretmenler-gunu-gonderi.png (1080x1350)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  for (const [f, h, out] of [['story', 1920, 'ogretmenler-gunu-story.png'], ['feed', 1350, 'ogretmenler-gunu-gonderi.png']]) {
    const p = await b.newPage({ viewport: { width: 1080, height: h } });
    await p.goto('file://' + path.resolve(__dirname, 'afis.html') + '?f=' + f);
    await p.evaluate(() => window.ready);
    await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(__dirname, out) });
    console.log('Hazır:', out);
  }
  await b.close();
})();
