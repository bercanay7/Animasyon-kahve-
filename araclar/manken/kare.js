// node araclar/manken/kare.js <sahne.html (depo köküne göre)> <çıktı klasörü> <t1,t2,…> [sorgu]
// Tek kare çizer, PNG yazar ve süreleri ayrı ölçer: çizim (sahne + 3B + son işlem, GPU bitene kadar) ve kodlama (PNG).
// Yerel http sunucusu üzerinden (file:// WebGL tuvalini kirletir); varsayılan başsız Chromium = SwiftShader.
const { chromium } = require('playwright'); const S = require('../../dorian-gray/tools/sunucu.js');
const fs = require('fs'), path = require('path');
const [sahne, dir, ts, sorgu = ''] = process.argv.slice(2);
if (!sahne || !dir || !ts) { console.error('Kullanım: node araclar/manken/kare.js araclar/manken/deneme.html cikti/ 0,5.5,12 [sahne=yakin]'); process.exit(1); }
(async () => {
  const srv = await S.baslat(), br = await chromium.launch();
  try {
    const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
    p.on('pageerror', e => console.log('[sayfa hatası]', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('[konsol]', m.text()); });
    await p.goto(`http://127.0.0.1:${srv.address().port}/${sahne}?render=1${sorgu ? '&' + sorgu : ''}`);
    await p.waitForFunction(() => window.READY || window.HATA, null, { timeout: 120000 });
    const h = await p.evaluate(() => window.HATA); if (h) throw new Error(h);
    fs.mkdirSync(dir, { recursive: true });
    const gl = await p.evaluate(() => { const g = document.createElement('canvas').getContext('webgl2'); const e = g.getExtension('WEBGL_debug_renderer_info'); return e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : g.getParameter(g.RENDERER); });
    console.log('GL:', gl);
    for (const t of ts.split(',').map(Number)) {
      const r = await p.evaluate(t => { const a = performance.now(); window.renderFrame(t); (window.BITIR || MANKEN.bitir)(); const b = performance.now();
        const u = document.getElementById('c').toDataURL('image/png'); const c = performance.now(); return { ciz: b - a, kod: c - b, u: u.split(',')[1] }; }, t);
      const f = path.join(dir, `k_${t.toFixed(2)}${sorgu ? '_' + sorgu.replace(/[^\w]+/g, '_') : ''}.png`);
      fs.writeFileSync(f, Buffer.from(r.u, 'base64'));
      console.log(`t=${t}  çizim ${r.ciz.toFixed(0)} ms  PNG ${r.kod.toFixed(0)} ms  → ${f}`);
    }
  } finally { await br.close(); srv.close(); }
})().catch(e => { console.error(e); process.exit(1); });
