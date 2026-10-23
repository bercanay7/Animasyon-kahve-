"""Altyazı: senaryo 'alt' metni + kelime zamanları → sisifos.tr.srt (python3 tools/srt.py)"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAXL, MAXC = 42, 84  # satır / altyazı başına karakter

segs = json.load(open(os.path.join(ROOT, 'senaryo.json')))['segments']
tl = open(os.path.join(ROOT, 'timeline.js')).read()
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', tl, re.S).group(1))

def fmt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

def wrap(words):
    """iki satıra dengeli böl"""
    s = ' '.join(words)
    if len(s) <= MAXL: return s
    best, bi = 1e9, 1
    for i in range(1, len(words)):
        a, b = ' '.join(words[:i]), ' '.join(words[i:])
        cost = abs(len(a) - len(b)) - (12 if words[i - 1][-1] in ',.:;…?!' else 0) + 100 * max(0, len(a) - MAXL, len(b) - MAXL)
        if cost < best: best, bi = cost, i
    return ' '.join(words[:bi]) + '\n' + ' '.join(words[bi:])

cues = []
for sg in segs:
    toks = sg['alt'].split()
    ws = [w for w in WORDS if w['id'] == sg['id'] and w['d']]
    if len(ws) != len(toks):
        print('UYARI: kelime sayısı uyuşmuyor', sg['id'], len(ws), len(toks))
    n = min(len(ws), len(toks))
    # cümle sonları ve virgüllerde bölünen parçalar (≤ MAXC)
    chunk = []
    for i in range(n):
        chunk.append(i)
        txt = ' '.join(toks[j] for j in chunk)
        end_sent = toks[i][-1] in '.?!…' or toks[i].endswith('.”') or toks[i].endswith('?”')
        nxt = ' '.join(toks[j] for j in chunk + [i + 1]) if i + 1 < n else ''
        if i == n - 1 or (end_sent and len(txt) > 18) or len(nxt) > MAXC:
            cues.append([ws[chunk[0]]['s'], ws[chunk[-1]]['e'], wrap([toks[j] for j in chunk])])
            chunk = []

# süreleri düzenle: en az 1.0 sn, bir sonrakine 80 ms boşluk, okunabilirlik için en fazla +0.6 sn uzat
for i, c in enumerate(cues):
    nxt = cues[i + 1][0] if i + 1 < len(cues) else c[1] + 3
    c[1] = min(max(c[1] + .35, c[0] + 1.0), nxt - .08)

out = os.path.join(ROOT, 'sisifos.tr.srt')
with open(out, 'w', encoding='utf-8') as f:
    for i, (a, b, t) in enumerate(cues, 1):
        f.write(f'{i}\n{fmt(a)} --> {fmt(b)}\n{t}\n\n')
print(len(cues), 'altyazı →', out)
