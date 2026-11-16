// node tools/ozet.js [çıktı.jpg] [plan süzgeci regex] — her planın ortasından bir kare; 8 sütunlu kurgu özeti (kurulsuz başkan bakışı)
const { chromium } = require('playwright'); const path = require('path'), http = require('http'), fs = require('fs'), { execFileSync } = require('child_process');
const ROOT = path.resolve(__dirname, '..');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2', '.json': 'application/json' };
(async () => {
  const out = process.argv[2] || 'animatik/ozet.jpg', flt = new RegExp(process.argv[3] || '.');
  const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': MIME[path.extname(f).toLowerCase()] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(0);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('console', m => { if (/plan|yok|HATA/.test(m.text())) console.log(m.text()); }); p.on('pageerror', e => console.log('HATA', e.message));
  await p.goto(`http://127.0.0.1:${srv.address().port}/film.html?render=1`); await p.waitForFunction(() => window.READY, null, { timeout: 90000 });
  const shots = await p.evaluate(() => { shotAt(0); return SHOTS.map((s, i) => ({ id: s.id, t: s.at + Math.min(2.5, ((SHOTS[i + 1] ? SHOTS[i + 1].at : DUR) - s.at) * .6) })); });
  const dir = path.join(ROOT, 'animatik', 'kare'); fs.mkdirSync(dir, { recursive: true });
  const files = [];
  for (const s of shots) { if (!flt.test(s.id)) continue; const b64 = await p.evaluate(t => renderFrame(t).toDataURL('image/jpeg', .85).split(',')[1], s.t); const f = path.join(dir, s.id + '.jpg'); fs.writeFileSync(f, Buffer.from(b64, 'base64')); files.push([s.id, f, s.t]); }
  await b.close(); srv.close();
  fs.writeFileSync(path.join(dir, 'liste.json'), JSON.stringify(files));
  execFileSync('python3', ['-c', `
import json,sys
from PIL import Image, ImageDraw
F=json.load(open(sys.argv[1])); W,H=480,270; C=8; R=(len(F)+C-1)//C
im=Image.new('RGB',(W*C,(H+22)*R),'white'); d=ImageDraw.Draw(im)
for i,(pid,f,t) in enumerate(F):
  x,y=(i%C)*W,(i//C)*(H+22); im.paste(Image.open(f).resize((W,H)),(x,y+22)); d.text((x+6,y+4),f'{pid}  {int(t//60)}:{t%60:04.1f}',fill='black')
im.save(sys.argv[2],quality=80)`, path.join(dir, 'liste.json'), path.resolve(ROOT, out)]);
  console.log('özet', out, files.length, 'plan');
})();
