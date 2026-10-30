import re, json, numpy as np
from common import *
src = open(P + 'audio/score.py').read()
def _nw(w):
    w = w.replace('İ', 'i').replace('I', 'ı').lower().replace('â', 'a').replace('î', 'i').replace('û', 'u')
    return re.sub(r'[^\wçğıöşü]', '', w)
def Wn(i, w, n=0):
    k = 0
    for x in WORDS:
        if x['id'] == i and x['w'].startswith(_nw(w)):
            if k == n: return x
            k += 1
FX = 'hammer|chain_rattle|thunder|eagle_cry|wings|boom|throne_hit|quake|whoosh|metal|thud|debris|clinks'
ev = []
for m in re.finditer(r"^\s*(%s)\(W\('([A-Z]\d\d[a-z]?)',\s*'([^']+)'(?:,\s*(\d+))?\)\s*([+-]\s*[\d.]+)?(.*)$" % FX, src, re.M):
    fn, cid, w, n, off, rest = m.groups()
    x = Wn(cid, w, int(n or 0)); t0 = x['s'] + (float(off.replace(' ', '')) if off else 0)
    vel = re.search(r'vel=([\d.]+)', rest); ev.append(dict(fn=fn, cue=cid, word=w, t=round(t0, 3), vel=float(vel.group(1)) if vel else None, wordspan=(x['s'], x['e'])))
F = np.load('frames.npz'); FR = 0.02
V14, M14, VK, MK = F['v_1-4k'], F['m_1-4k'], F['v_k'], F['m_k']
dB = lambda p: 10 * np.log10(p + 1e-20)
DURS = {'hammer': .5, 'chain_rattle': .7, 'thunder': 1.5, 'eagle_cry': .75, 'wings': 1.0, 'boom': 1.0, 'throne_hit': 1.0, 'quake': 2.0, 'whoosh': .45, 'metal': .6, 'thud': .3, 'debris': .6, 'clinks': .5}
rows = []
for e in ev:
    a, b = e['t'], e['t'] + DURS[e['fn']]
    ws = [w for w in WORDS if w['e'] > a and w['s'] < b]
    res = []
    for w in ws:
        i0, i1 = int(max(a, w['s']) / FR), int(min(b, w['e']) / FR) + 1
        if i1 - i0 < 2: continue
        res.append((w['id'], w['w'], round(float(dB(V14[i0:i1].sum()) - dB(M14[i0:i1].sum())), 1), round(float(dB(VK[i0:i1].sum()) - dB(MK[i0:i1].sum())), 1)))
    e['overlap'] = res; e['min14'] = min([r[2] for r in res], default=None); rows.append(e)
out = {'n_events': len(rows), 'on_speech': sum(1 for r in rows if r['overlap']),
       'masking_lt6': [(r['fn'], r['cue'], r['word'], fmt(r['t']), r['vel'], r['overlap']) for r in sorted(rows, key=lambda r: (r['min14'] if r['min14'] is not None else 99)) if r['min14'] is not None and r['min14'] < 6]}
key = [r for r in rows if r['fn'] in ('hammer', 'thunder', 'eagle_cry', 'chain_rattle', 'throne_hit', 'quake')]
out['key_events'] = [(r['fn'], r['cue'], r['word'], fmt(r['t']), r['t'], r['vel'], r['min14']) for r in key]
json.dump(out, open('sfx.json', 'w'), indent=1, ensure_ascii=False); print(json.dumps(out, indent=1, ensure_ascii=False))
