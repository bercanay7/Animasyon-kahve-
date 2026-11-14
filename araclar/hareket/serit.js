// araclar/hareket/serit.js: hareketli bir figürü izleyen, büyütülmüş kare şeridi (animatör gözüyle denetim).
// Fikir: JDhruv14/line-art-animation references/verify.md (MIT). Mevcut her sahneyle çalışır (milton, ikaros, sisifos…):
// sözleşme window.ready + window.renderFrame(t) + <canvas id="c">. Odak sırası: --odak x,y > window.SERIT_ODAK(t) > kare ortası.
//
//   node araclar/hareket/serit.js <sahne.html> <cikti.png> <t0> <t1> [kare=8] [--kutu 420x520] [--buyut 1] [--odak 960,600] [--sorgu "a=b"]
// Örnek (bir adım döngüsü, 8 kare):
//   node araclar/hareket/serit.js araclar/hareket/ornek.html serit.png 1.0 2.0 8
// Bakılacaklar: basan ayak zemindeki çentiğe göre yerinde mi; kalça basışta iniyor, geçişte yükseliyor mu;
// öndeki bacak üstte mi; kol ve çanta gecikip oturuyor mu; kareler arasında sıçrama var mı.
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');

const a = process.argv.slice(2), arg = (ad, vars) => { const i = a.indexOf('--' + ad); if (i < 0) return vars; const v = a[i + 1]; a.splice(i, 2); return v; };
const kutu = arg('kutu', '420x520').split('x').map(Number), buyut = +arg('buyut', 1), odak = arg('odak', null), sorgu = arg('sorgu', '');
const [sahne, cikti, t0s, t1s, ns] = a;
if (!sahne || !cikti || t0s === undefined || t1s === undefined) {
  console.error('Kullanım: node araclar/hareket/serit.js <sahne.html> <cikti.png> <t0> <t1> [kare] [--kutu GxY] [--buyut k] [--odak x,y] [--sorgu "a=b"]');
  process.exit(1);
}
const t0 = +t0s, t1 = +t1s, n = Math.max(2, +(ns || 8));

(async () => {
  const tarayici = await chromium.launch();
  const sayfa = await tarayici.newPage({ viewport: { width: 1920, height: 1080 } });
  await sayfa.goto('file://' + path.resolve(sahne) + '?render=1' + (sorgu ? '&' + sorgu : ''));
  await sayfa.evaluate(() => window.ready);
  const png = await sayfa.evaluate(({ t0, t1, n, kutu, buyut, odak }) => {
    const c = document.getElementById('c'), [w, h] = kutu, k = buyut;
    const rs = c.width / 1920;                          // ?rs=2 gibi yüksek çözünürlüklü sahneler için
    const out = document.createElement('canvas'); out.width = w * k * n + 4 * (n - 1); out.height = h * k + 34;
    const o = out.getContext('2d'); o.fillStyle = '#888'; o.fillRect(0, 0, out.width, out.height);
    const sabit = odak ? odak.split(',').map(Number) : null;
    for (let i = 0; i < n; i++) {
      const t = t0 + (t1 - t0) * i / (n - 1);
      window.renderFrame(t);
      const [cx, cy] = sabit || (window.SERIT_ODAK ? window.SERIT_ODAK(t) : [960, 540]);
      const x = i * (w * k + 4);
      o.imageSmoothingEnabled = k < 2;
      o.drawImage(c, (cx - w / 2) * rs, (cy - h / 2) * rs, w * rs, h * rs, x, 0, w * k, h * k);
      o.fillStyle = '#111'; o.fillRect(x, h * k, w * k, 34);
      o.fillStyle = '#fff'; o.font = '20px monospace'; o.fillText(`t=${t.toFixed(3)}  #${i}`, x + 8, h * k + 24);
    }
    return out.toDataURL('image/png').split(',')[1];
  }, { t0, t1, n, kutu, buyut, odak });
  fs.writeFileSync(cikti, Buffer.from(png, 'base64'));
  await tarayici.close();
  console.log('Hazır:', cikti);
})();
