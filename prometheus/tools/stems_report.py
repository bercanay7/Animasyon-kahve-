"""Stem dengesi: bölüm başına LUFS ve en yüksek efekt anları (python3 tools/stems_report.py)"""
import soundfile as sf, numpy as np, pyloudnorm as pyln, json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
st = {n: sf.read(os.path.join(ROOT, f'audio/stems/{n}.wav'))[0] for n in ['vo', 'music', 'sfx']}
cues = json.loads(re.search(r'window\.CUES = (\{.*?\});', open(os.path.join(ROOT, 'timeline.js')).read()).group(1))
m = pyln.Meter(SR)
def L(x, a, b):
    try: return m.integrated_loudness(x[int(a * SR):int(b * SR)])
    except Exception: return -99
sec = {}
for k, v in cues.items():
    sec.setdefault(k[0], [1e9, 0]); sec[k[0]][0] = min(sec[k[0]][0], v['s']); sec[k[0]][1] = max(sec[k[0]][1], v['e'])
for k, (a, b) in sec.items():
    print(k, f'{a:6.1f}-{b:6.1f}', '  '.join(f'{n}:{L(x, a, b):6.1f}' for n, x in st.items()))
def mom(x, w=.4):
    p = (x ** 2).mean(1); c = np.concatenate([[0], np.cumsum(p)]); n = int(w * SR)
    e = (c[n:] - c[:-n]) / n
    return 10 * np.log10(e[::480] + 1e-12)
v, s, mu = mom(st['vo']), mom(st['sfx']), mom(st['music'])
seen = []
for i in np.argsort(-s):
    t = i * 480 / SR
    if all(abs(t - u) > 2 for u in seen): seen.append(t)
    if len(seen) >= 18: break
for t in sorted(seen):
    i = int(t * SR / 480); print(f'{t:7.2f}s sfx {s[i]:6.1f} dB  vo {v[i]:6.1f}  music {mu[i]:6.1f}')
