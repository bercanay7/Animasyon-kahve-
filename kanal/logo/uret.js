// Kimlik dosyalarını üretir: node kanal/logo/uret.js
// Çıktı: kanal/logo/cikti/  (PNG'ler Playwright ile, SVG'ler doğrudan logo.js'ten)
// Yazılı SVG için opentype.js (MIT) gerekir: OPENTYPE=/yol/node_modules/opentype.js node uret.js
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ZK = require('./logo.js');
const KOK = __dirname, CIK = path.join(KOK, 'cikti');
fs.mkdirSync(CIK, { recursive: true });

const TUR = { '.html': 'text/html', '.js': 'text/javascript', '.woff2': 'font/woff2', '.jpg': 'image/jpeg', '.png': 'image/png' };
const srv = http.createServer((q, r) => {
  const p = path.join(KOK, decodeURIComponent(q.url.split('?')[0]));
  if (!p.startsWith(KOK) || !fs.existsSync(p)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': TUR[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r);
}).listen(0);

// 1) Yalın işaret SVG'leri (yazısız, yalnız yol)
for (const d of ['altin', 'lacivert', 'fildisi', 'tek_acik', 'tek_koyu'])
  fs.writeFileSync(path.join(CIK, `isaret_${d}.svg`), ZK.svg(d, 800, d.startsWith('tek') ? {} : { daire: d === 'altin' }));

// 2) Yazılı yatay SVG: harfler yola çevrilir (font gömülmez)
try {
  const ot = require(process.env.OPENTYPE || 'opentype.js');
  const fl = ot.loadSync(path.join(KOK, 'fonts/fraunces-latin-600.woff'));
  const fx = ot.loadSync(path.join(KOK, 'fonts/fraunces-latin-ext-600.woff'));
  const yaziYolu = (s, x, y, boy, iz) => {
    let d = '';
    for (const ch of s) {
      const f = fl.charToGlyphIndex(ch) ? fl : fx;
      d += f.getPath(ch, x, y, boy).toPathData(2);
      x += f.getAdvanceWidth(ch, boy) + iz;
    }
    return { d, x };
  };
  for (const [ad, duzen] of [['yatay_lacivert', 'lacivert'], ['yatay_fildisi', 'fildisi']]) {
    const k = ZK.DUZEN[duzen];
    // işaret 528 birim yüksekliği 260 px'e iner; yazı 150 px, harf arası .06em
    const olc = 260 / 528, isX = 80, yY = 60;
    const t = yaziYolu('ZAMAN KURYESİ', isX + 400 * olc + 56, yY + 190, 150, 9);
    const W = Math.ceil(t.x + 70), H = 380;
    const zemin = duzen === 'lacivert' ? `<rect width="${W}" height="${H}" fill="${k.zemin}"/>` : `<rect width="${W}" height="${H}" fill="${k.zemin}"/>`;
    fs.writeFileSync(path.join(CIK, `${ad}.svg`),
      `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">${zemin}` +
      `<g transform="translate(${isX} ${yY}) scale(${olc}) translate(-200 -136)">${ZK.isaret(k.cam, k.kum)}</g>` +
      `<path d="${t.d}" fill="${k.cam}"/></svg>`);
  }
} catch (e) { console.log('yazılı SVG atlandı (opentype.js yok):', e.message); }

(async () => {
  const port = srv.address().port, b = await chromium.launch();
  async function cek(m, out, w, h, ek = '', o = {}) {
    const pg = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await pg.goto(`http://localhost:${port}/sayfa.html?m=${m}${ek}`);
    await pg.evaluate(() => window.hazir); await pg.waitForTimeout(200);
    const el = o.secici ? await pg.$(o.secici) : null;
    const opt = { path: path.join(CIK, out), omitBackground: !!o.saydam, type: out.endsWith('.jpg') ? 'jpeg' : 'png' };
    if (out.endsWith('.jpg')) opt.quality = 92;
    if (el) await el.screenshot(opt); else await pg.screenshot(opt);
    await pg.close(); console.log('✓', out);
  }
  await cek('avatar', 'avatar_altin_800.png', 800, 800, '&d=altin');
  await cek('avatar', 'avatar_lacivert_800.png', 800, 800, '&d=lacivert');
  await cek('filigran', 'filigran_150.png', 150, 150, '&d=altin', { saydam: 1 });
  await cek('yatay', 'yatay_lacivert.png', 1600, 400, '&d=lacivert&bg=%23101B33', { secici: '.yatay' });
  await cek('yatay', 'yatay_fildisi.png', 1600, 400, '&d=fildisi&bg=%23F3EAD7', { secici: '.yatay' });
  await cek('yatay', 'yatay_lacivert_saydam.png', 1600, 400, '&d=lacivert', { secici: '.yatay', saydam: 1 });
  await cek('kapak', 'kanal_kapagi_2560.jpg', 2560, 1440);
  await cek('test', 'test_kucuk_boy.png', 1500, 600, '', { secici: '.sheet' });
  await b.close(); srv.close();
})();
