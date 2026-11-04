// Builds each audience's price list from sablon.html and renders it to a single-page PDF sized to the
// content (phone-friendly, 1080 px wide) plus a JPG preview.
// Usage: NODE_PATH=$(npm root -g) node tenisci-spa-fiyat/render.js [tenisci|karaca]
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const dir = __dirname;
const wa = (text) => 'https://wa.me/905330713373?text=' + encodeURIComponent(text);

const TENIS_IKON = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><circle cx="24" cy="24" r="20"/><path d="M9.5 10.5c6.5 7.5 6.5 19.5 0 27"/><path d="M38.5 10.5c-6.5 7.5-6.5 19.5 0 27"/></svg>';
const YAPRAK_IKON = '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 39C9 21 21 9 40 8c0 19-12 31-31 31z"/><path d="M9 39l18-18"/></svg>';
const KORT = `  <svg class="court" viewBox="-20 -60 2417 1217" fill="none" stroke="#f5ede4" stroke-width="16" aria-hidden="true">
    <rect x="0" y="0" width="2377" height="1097"/>
    <path d="M0 137H2377M0 960H2377M1188.5 -60V1157M548.5 137V960M1828.5 137V960M548.5 548.5H1828.5"/>
  </svg>
`;

const VARIANTS = {
  tenisci: {
    pdf: 'navitas-tenisci-spa-fiyat-listesi.pdf',
    jpg: 'onizleme-tenisci.jpg',
    BASLIK_DUZ: 'Tenisçilere Özel Spa Fiyat Listesi',
    BASLIK: 'Tenisçilere özel<br>spa fiyatları',
    IKON: TENIS_IKON,
    KURAL: 'Tenisçi fiyatı için <a href="{{WA}}">WhatsApp’tan yazmanız</a> ya da söylemeniz yeterli.',
    MOTIF: KORT,
    ORTAK: '',
    WA: wa('Merhaba, tenisçilere özel spa fiyat listesinden yazıyorum. Randevu almak istiyorum. (Ref: TENIS-PDF)'),
  },
  karaca: {
    pdf: 'navitas-karaca-spa-fiyat-listesi.pdf',
    jpg: 'onizleme-karaca.jpg',
    BASLIK_DUZ: 'Karaca Çalışanlarına Özel Spa Fiyat Listesi',
    BASLIK: 'Karaca çalışanlarına<br>özel spa fiyatları',
    IKON: YAPRAK_IKON,
    KURAL: 'Randevu için <a href="{{WA}}">WhatsApp’tan yazın</a>.',
    MOTIF: '',
    // Karaca's own logo, unmodified, from karaca.com (use approved by the business owner, 2026-11-04).
    ORTAK: '    <div class="partner"><span class="x" aria-hidden="true">×</span><img src="logo/karaca.svg" alt="Karaca"></div>\n',
    WA: wa('Merhaba, Karaca çalışanlarına özel spa fiyat listesinden yazıyorum. Randevu almak istiyorum. (Ref: KARACA-PDF)'),
  },
};

function build(v) {
  let html = fs.readFileSync(path.join(dir, 'sablon.html'), 'utf8');
  for (const key of ['BASLIK_DUZ', 'BASLIK', 'IKON', 'KURAL', 'MOTIF', 'ORTAK', 'WA']) {
    html = html.split('{{' + key + '}}').join(v[key]);
  }
  html = html.split('{{WA}}').join(v.WA); // the rule line can carry the link too
  if (/\{\{[A-Z_]+\}\}/.test(html)) throw new Error('unfilled placeholder: ' + html.match(/\{\{[A-Z_]+\}\}/)[0]);
  return html;
}

(async () => {
  const names = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(VARIANTS);
  const browser = await chromium.launch();
  for (const name of names) {
    const v = VARIANTS[name];
    if (!v) throw new Error('unknown variant: ' + name);
    const tmp = path.join(dir, `.${name}.html`); // beside the template so relative paths resolve
    fs.writeFileSync(tmp, build(v));
    const page = await browser.newPage({ viewport: { width: 1080, height: 1200 }, deviceScaleFactor: 2 });
    await page.goto('file://' + tmp, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const height = await page.evaluate(() => Math.ceil(document.querySelector('.page').getBoundingClientRect().height));
    await page.emulateMedia({ media: 'screen' });
    await page.pdf({
      path: path.join(dir, v.pdf), width: '1080px', height: height + 'px',
      printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, pageRanges: '1',
    });
    await page.screenshot({ path: path.join(dir, v.jpg), fullPage: true, type: 'jpeg', quality: 86 });
    await page.close();
    fs.unlinkSync(tmp);
    console.log(name, 'height', height, '->', v.pdf);
  }
  await browser.close();
})();
