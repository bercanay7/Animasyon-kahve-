// Shorts yazı katmanları: kanca (üst, sürekli) + altyazı grupları (alt). Saydam PNG'ler; fonts.css (latin-ext) tarayıcıda.
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
const R = path.resolve(__dirname, '..'), E = JSON.parse(fs.readFileSync(path.join(R, 'shorts', 'edl.json'), 'utf8')), T = path.join(R, 'shorts', '_parca');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(R, 'shorts', 'yazi.html'));
  await p.evaluate(async () => { await document.fonts.load('130px "Bebas Neue"', 'İŞĞÜÇÖ'); await document.fonts.load('600 60px "Cormorant Garamond"', 'İşğüçöı'); });
  const out = [];
  for (let k = -1; k < E.cues.length; k++) {
    const c = k < 0 ? { s: 0, e: E.DUR, txt: '' } : E.cues[k];
    await p.evaluate(({ hook, txt, top }) => window.ciz(hook, txt, top), { hook: E.hook, txt: c.txt, top: k < 0 });
    const f = path.join(T, `y${k + 1}.png`); await p.screenshot({ path: f, omitBackground: true }); out.push([f, c.s, c.e]);
  }
  fs.writeFileSync(path.join(T, 'yazi.json'), JSON.stringify(out)); await b.close();
})();
