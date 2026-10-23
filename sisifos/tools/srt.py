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

MERGE = {('C03', 'Kızsa,'): 2}
cues = []
for sg in segs:
    toks = sg['alt'].split()
    ws = [w for w in WORDS if w['id'] == sg['id'] and w['d']]
    # altyazıda tek sözcük, anlatım zamanlamasında iki sözcük olan kısaltmalar ("Kız ise" → duyulan "Kızsa,")
    for (sid, tok), k in MERGE.items():
        if sid == sg['id'] and tok in toks:
            i = toks.index(tok); ws = ws[:i] + [{**ws[i], 'e': ws[i + k - 1]['e']}] + ws[i + k:]
    if len(ws) != len(toks):
        print('UYARI: kelime sayısı uyuşmuyor', sg['id'], len(ws), len(toks))
    n = min(len(ws), len(toks))
    # önce cümlelere, uzun cümleleri dengeli parçalara böl (tek kelimelik yetim altyazı kalmasın; virgül tercih edilir)
    sents, cur = [], []
    for i in range(n):
        cur.append(i)
        if i == n - 1 or toks[i][-1] in '.?!…' or toks[i].endswith('.”') or toks[i].endswith('?”'):
            sents.append(cur); cur = []
    # çok kısa cümleleri (≤ 2 kelime) bir sonrakiyle birleştir
    merged = []
    for sn in sents:
        if merged and len(merged[-1]) <= 2 and len(' '.join(toks[j] for j in merged[-1] + sn)) <= MAXC: merged[-1] += sn
        else: merged.append(sn)
    for sn in merged:
        L = len(' '.join(toks[j] for j in sn))
        k = max(1, -(-L // MAXC))
        if k == 1: parts = [sn]
        else:
            # k parçaya böl: hedef uzunluklara en yakın, virgüllü sınırları ödüllendiren dinamik bölme
            import itertools
            best, parts = 1e9, None
            for cuts in itertools.combinations(range(1, len(sn)), k - 1):
                ps = [sn[a_:b_] for a_, b_ in zip((0,) + cuts, cuts + (len(sn),))]
                ls = [len(' '.join(toks[j] for j in pp)) for pp in ps]
                cost = sum(abs(l - L / k) for l in ls) + 200 * sum(max(0, l - MAXC) for l in ls) - sum(10 for pp in ps[:-1] if toks[pp[-1]][-1] in ',;:') + 100 * sum(1 for pp in ps if len(pp) < 2)
                if cost < best: best, parts = cost, ps
        for pp in parts:
            cues.append([ws[pp[0]]['s'], ws[pp[-1]]['e'], wrap([toks[j] for j in pp])])

# süreleri düzenle: en az 1.0 sn, bir sonrakine 80 ms boşluk, okunabilirlik için en fazla +0.6 sn uzat
for i, c in enumerate(cues):
    nxt = cues[i + 1][0] if i + 1 < len(cues) else c[1] + 3
    c[1] = min(max(c[1] + .35, c[0] + 1.0), nxt - .08)

out = os.path.join(ROOT, 'sisifos.tr.srt')
with open(out, 'w', encoding='utf-8') as f:
    for i, (a, b, t) in enumerate(cues, 1):
        f.write(f'{i}\n{fmt(a)} --> {fmt(b)}\n{t}\n\n')
print(len(cues), 'altyazı →', out)
