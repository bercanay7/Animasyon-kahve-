"""timeline.js'ten müzik için ipucu dosyası (audio/cues.md) üretir: toplam süre, bölüm aralıkları, tüm cümleler.
Kullanım: python3 tools/cues.py"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
js = open(os.path.join(ROOT, 'timeline.js')).read()
CUES = json.loads(re.search(r'window\.CUES = (.*?);\n', js, re.S).group(1))
DUR = float(re.search(r'window\.DUR = ([\d.]+)', js).group(1))
segs = json.load(open(os.path.join(ROOT, 'senaryo.json')))['segments']
secs = []
for s in segs:
    if s['id'] not in CUES: continue
    if not secs or secs[-1][0] != s['bolum']: secs.append([s['bolum'], CUES[s['id']]['s'], CUES[s['id']]['e']])
    secs[-1][2] = CUES[s['id']]['e']
end = max(c['e'] for c in CUES.values())
out = [f'Toplam süre: {DUR:.2f} sn (anlatım {end:.2f} sn\'de biter; sonrası ~{DUR - end:.0f} sn bitiş ekranı/end screen müziği)', '', '## Bölümler (anlatım başlangıç/bitiş, sn)']
out += [f'- {b}: {a:.2f} – {e:.2f}' for b, a, e in secs]
out += ['', '## Tüm cümleler']
out += [f"- {s['id']} {CUES[s['id']]['s']:.2f}–{CUES[s['id']]['e']:.2f}: {s['alt']}" for s in segs if s['id'] in CUES]
os.makedirs(os.path.join(ROOT, 'audio'), exist_ok=True)
open(os.path.join(ROOT, 'audio', 'cues.md'), 'w').write('\n'.join(out) + '\n')
print(out[0])
