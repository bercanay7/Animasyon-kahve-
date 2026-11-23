"""Plan çapalarını zamana çevirir: python3 tools/plan_zaman.py [set ya da plan kimliği ...]
Çıktı: plan kimliği, başlangıç saniyesi, süre (bir sonraki plana kadar), set, çapa, kadraj."""
import json, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tl = open(os.path.join(ROOT, 'timeline.js'), encoding='utf-8').read()
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', tl, re.S).group(1))
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', tl, re.S).group(1))
DUR = float(re.search(r'window\.DUR\s*=\s*([\d.]+)', tl).group(1))
P = json.load(open(os.path.join(ROOT, 'animatik', 'planlar.json'), encoding='utf-8'))['planlar']
norm = lambda w: re.sub(r'[^\wçğıöşü]', '', w.lower().replace('â', 'a').replace('î', 'i').replace('û', 'u'))
def A(at):
    m = re.match(r'^([A-Z]\d+[a-z]?)(?:@([^#+-]+)(?:#(\d+))?)?([+-][\d.]+)?$', at)
    sid, w, n, off = m.group(1), m.group(2), int(m.group(3) or 0), float(m.group(4) or 0)
    t = CUES[sid]['s']
    if w:
        hits = [x for x in WORDS if x['id'] == sid and x['w'].startswith(norm(w))]
        if len(hits) > n: t = hits[n]['s']
    return t + off
T = sorted(((A(p['at']), p) for p in P), key=lambda x: x[0])
sec = [a.upper() for a in sys.argv[1:]]
for i, (t, p) in enumerate(T):
    if sec and p['set'] not in sec and p['id'] not in sec: continue
    d = (T[i + 1][0] if i + 1 < len(T) else DUR) - t
    print(f"{p['id']}  {t:8.2f}  {d:6.2f} sn  {p['set']}  {p['at']:18s} {p.get('kadraj', p.get('ne', ''))[:50]}")
