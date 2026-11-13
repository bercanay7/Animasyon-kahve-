"""timeline.js'teki görünen sözcükleri (d) yeniden eşler; zamanlara ve ses dosyasına dokunmaz. python3 tools/fix_disp.py"""
import json, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dispmap import disp_map
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(R, 'timeline.js'); t = open(p, encoding='utf-8').read()
W = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', t, re.S).group(1))
alt = {s['id']: s['alt'] for s in json.load(open(os.path.join(R, 'senaryo.json')))['segments']}
bad = 0
for sid in alt:
    idx = [i for i, w in enumerate(W) if w['id'] == sid]
    ds = disp_map(alt[sid], [W[i]['w'] for i in idx])
    for i, dd in zip(idx, ds):
        if W[i]['d'] != dd: bad += 1
        W[i]['d'] = dd
    # görünen sözcüğün bitişi: grubundaki son seslendirme sözcüğünün bitişi
    for n, i in enumerate(idx):
        if W[i]['d']:
            k = n
            while k + 1 < len(idx) and not W[idx[k + 1]]['d']: k += 1
            W[i]['de'] = W[idx[k]]['e']
t = t[:t.index('window.WORDS = ')] + 'window.WORDS = ' + json.dumps(W, ensure_ascii=False) + ';' + t[t.index(';', t.index('window.WORDS = ') + len(json.dumps(W, ensure_ascii=False)) - 5) + 1:] if False else re.sub(r'window\.WORDS = \[.*?\];', lambda m: 'window.WORDS = ' + json.dumps(W, ensure_ascii=False) + ';', t, count=1, flags=re.S)
open(p, 'w', encoding='utf-8').write(t)
print('değişen', bad)
