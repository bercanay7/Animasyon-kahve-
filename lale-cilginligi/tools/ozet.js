// Kurgu özeti: her plandan bir kare (plan süresinin %60'ı), 6×4'lük sayfalar. node tools/ozet.js <klasör> [P001-P030]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'); const S = require('./sunucu'); const { execFileSync } = require('child_process');
(async () => {
  const out = process.argv[2]; fs.mkdirSync(out, { recursive: true }); const ar = process.argv[3];
  const srv = await S.baslat(), br = await chromium.launch();
  try {
    const p = await S.sayfa(br, srv.address().port, process.env.EXTRA || '');
    const list = await p.evaluate(() => { shotAt(0); return SHOTS.map((s, i) => { const st = shotState(i, s.at); return { id: s.id, t: s.at + st.d * .6, d: st.d }; }); });
    let sec = list; if (ar) { const [a, b] = ar.split('-'); sec = list.filter(x => x.id >= a && x.id <= b); }
    for (const x of sec) { const b64 = await p.evaluate(t => { const c = renderFrame(t), s = document.createElement('canvas'); s.width = 480; s.height = 270; s.getContext('2d').drawImage(c, 0, 0, 480, 270); return s.toDataURL('image/jpeg', .85).split(',')[1]; }, x.t);
      fs.writeFileSync(path.join(out, `${x.id}.jpg`), Buffer.from(b64, 'base64')); }
    fs.writeFileSync(path.join(out, 'liste.json'), JSON.stringify(sec));
    execFileSync('python3', ['-c', `
import json,os
from PIL import Image, ImageDraw, ImageFont
o='${out}'; L=json.load(open(o+'/liste.json')); fn=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
for s in range(0,len(L),24):
  part=L[s:s+24]; c=Image.new('RGB',(6*484,4*300),'white'); d=ImageDraw.Draw(c)
  for i,x in enumerate(part):
    im=Image.open(o+'/'+x['id']+'.jpg'); X=(i%6)*484; Y=(i//6)*300; c.paste(im,(X,Y)); d.text((X+4,Y+272),x['id']+'  '+str(round(x['d'],1))+' sn',fill=(200,0,0),font=fn)
  c.save(o+'/sayfa_%02d.jpg'%(s//24+1),quality=82)`]);
    console.log(sec.length, 'plan');
  } finally { await br.close(); srv.close(); }
})();
