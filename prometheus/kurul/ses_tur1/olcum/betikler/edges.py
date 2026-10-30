import numpy as np, soundfile as sf, json
from scipy import signal
from common import *
raw, _ = sf.read(P + 'vo/vo.wav', dtype='float64'); N = len(raw)
z = raw == 0
# ≥0,15 sn sıfır koşuları = cümle arası boşluk
d = np.diff(np.r_[0, z.astype(np.int8), 0]); zs = np.where(d == 1)[0]; ze = np.where(d == -1)[0]
runs = [(a, b) for a, b in zip(zs, ze) if b - a >= 0.15 * SR]
bounds = [0] + [x for r in runs for x in r] + [N]
clips = [(bounds[i], bounds[i + 1]) for i in range(0, len(bounds) - 1, 2) if bounds[i + 1] - bounds[i] > 0.3 * SR]
k = kfilt(raw); fr = int(.05 * SR)
res = []
for a, b in clips:
    x = k[a:b]; n = len(x) // fr; p = (x[:n * fr] ** 2).reshape(n, fr).mean(1); lv = 10 * np.log10(p + 1e-20)
    ref = 10 * np.log10(p[lv > lv.max() - 25].mean())
    e0 = 10 * np.log10((k[a + int(.012 * SR):a + int(.042 * SR)] ** 2).mean() + 1e-20) - ref
    e1 = 10 * np.log10((k[b - int(.042 * SR):b - int(.012 * SR)] ** 2).mean() + 1e-20) - ref
    t0, t1 = a / SR, b / SR
    cue = next((c for c, v in CUES.items() if t0 - .5 <= v['s'] <= t1), '?')
    # ilk kelimeye kadar olan (klip başı) bölümün en yüksek 50 ms seviyesi
    fw = min((w['s'] for w in WORDS if w['id'] == cue), default=t0)
    pre = k[a:int((fw - .03) * SR)]
    m = len(pre) // fr
    prel = (10 * np.log10((pre[:m * fr] ** 2).reshape(m, fr).mean(1).max() + 1e-20) - ref) if m > 0 else None
    res.append((cue, round(t0, 2), round(t1, 2), round(e0, 1), round(e1, 1), round(prel, 1) if prel is not None else None, round(fw - t0, 2)))
out = {'n_clips': len(clips), 'n_cues': len(CUES)}
out['hot_start_gt-20'] = [r for r in res if r[3] > -20]
out['hot_end_gt-20'] = [r for r in res if r[4] > -20]
out['pre_word_noise_gt-30'] = [r for r in res if r[5] is not None and r[5] > -30]
out['edge_end_pct'] = {p: round(float(np.percentile([r[4] for r in res], p)), 1) for p in (50, 90, 99, 100)}
out['edge_start_pct'] = {p: round(float(np.percentile([r[3] for r in res], p)), 1) for p in (50, 90, 99, 100)}
json.dump(out, open('edges.json', 'w'), indent=1, ensure_ascii=False); print(json.dumps(out, indent=1, ensure_ascii=False))
