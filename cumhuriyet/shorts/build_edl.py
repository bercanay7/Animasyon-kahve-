"""Shorts kurgu listesi: filmin kendi cümlelerinden kesitler (yeni seslendirme yok) → shorts/edl.js, edl.json
Kurgu (yönetmenlik kurulu önerisi): A01 → A02 → A04 → A05 → G01 → G02, sonda kanal çağrısı.
python3 shorts/build_edl.py"""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
t = open(os.path.join(R, 'timeline.js'), encoding='utf-8').read()
C = json.loads(re.search(r'window\.CUES = (\{.*?\});', t).group(1))
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', t, re.S).group(1))
SEN = json.load(open(os.path.join(R, 'senaryo.json')))['segments']
ALT = {s['id']: s['alt'] for s in SEN}
# her kesit: cümle kimliği, kesit içi kırpma merkezleri (cx: 9:16 pencerenin film x merkezi), altyazı yeri (capY)
PLAN = [
    dict(id='A01', pre=.35, post=.35, cx0=1150, cx1=1050, capY=1250),
    dict(id='A02', pre=.25, post=.45, cx0=900, capY=1300),
    dict(id='A04', pre=.25, post=.35, cx0=960, z0=1.0, z1=1.06, capY=1280),
    dict(id='A05', pre=.2, post=.55, cx0=960, capY=1300),
    dict(id='G01', pre=.35, post=.5, cx0=960, capY=1280),
    dict(id='G02', pre=.25, post=.6, cx0=960, capY=1300),
]
EDL, groups, s = [], [], 0.0
for p in PLAN:
    f0, f1 = C[p['id']]['s'] - p['pre'], C[p['id']]['e'] + p['post']
    clip = {**p, 'f': round(f0, 3), 's': round(s, 3), 'e': round(s + f1 - f0, 3)}
    EDL.append(clip)
    # altyazı: alt metnindeki görünen kelimeler, filmdeki kelime zamanlarına (tts) sırayla eşlenir
    ws = [w for w in WORDS if w['id'] == p['id']]
    disp = re.sub(r'\s+', ' ', ALT[p['id']]).replace('…', '… ').split()
    disp = [d for d in disp if re.sub(r'[^\wçğıöşüÇĞİÖŞÜâÂ]', '', d)]
    # tts'te yıllar yazıyla: kelime sayısı farklıysa zamanlar orantılı dağıtılır
    n, m = len(disp), len(ws)
    cur = []
    for k, d in enumerate(disp):
        j0 = int(k * m / n); j1 = max(j0, int((k + 1) * m / n) - 1)
        w = {'w': d, 's': round(ws[j0]['s'] - f0 + s, 3), 'e': round(ws[min(j1, m - 1)]['e'] - f0 + s, 3)}
        cur.append(w)
        if d[-1] in '.,:?!…”' or len(cur) == 3:
            groups.append({'s': cur[0]['s'], 'e': cur[-1]['e'], 'words': cur}); cur = []
    if cur: groups.append({'s': cur[0]['s'], 'e': cur[-1]['e'], 'words': cur})
    s += f1 - f0
for i in range(len(groups) - 1): groups[i]['e'] = min(groups[i]['e'] + .25, groups[i + 1]['s'] - .02)
CTA = round(s, 2); DUR = round(s + 2.4, 2)
EDL[-1]['e'] = DUR  # son kesit çağrı boyunca sürer (film görüntüsü devam eder)
out = {'EDL': EDL, 'GROUPS': groups, 'CTA': CTA, 'DUR': DUR}
open(os.path.join(D, 'edl.js'), 'w').write('// shorts/build_edl.py tarafından üretildi\nwindow.SHORT = ' + json.dumps(out, ensure_ascii=False) + ';\n')
json.dump(out, open(os.path.join(D, 'edl.json'), 'w'), ensure_ascii=False, indent=1)
print('süre', DUR, 'kesit', len(EDL), 'grup', len(groups))
for c in EDL: print(f"{c['id']}: shorts {c['s']:.2f}–{c['e']:.2f}  film {c['f']:.2f}")
