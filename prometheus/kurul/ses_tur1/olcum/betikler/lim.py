import numpy as np, soundfile as sf, json
from common import *
vo = np.load('vo.npy', mmap_mode='r'); send = np.load('send.npy', mmap_mode='r'); mu = np.load('mu.npy', mmap_mode='r')
mix, _ = sf.read(P + 'audio/mix.wav', dtype='float32', always_2d=True)
N = len(vo); b = 480; nb = N // b
num = np.zeros(nb); den = np.zeros(nb); res = np.zeros(nb); mixe = np.zeros(nb)
for c in range(2):
    pre = (np.asarray(vo) + np.asarray(send[c]) + np.asarray(mu[c]))[:nb * b].astype(np.float64).reshape(nb, b)
    m = mix[:nb * b, c].astype(np.float64).reshape(nb, b)
    num += (m * pre).sum(1); den += (pre * pre).sum(1); mixe += (m * m).sum(1)
    del pre, m
g = num / (den + 1e-20)
ok = den > np.percentile(den, 30)
k = np.median(g[ok])
gr = 20 * np.log10(np.maximum(g, 1e-6) / k)
# artık: g*pre ile mix arasındaki ilinti (blok içi)
fit = (num ** 2) / (den * mixe + 1e-30)
out = {'k_dB': round(float(20 * np.log10(k)), 2), 'fit_median': round(float(np.median(fit[ok])), 5), 'fit_p1': round(float(np.percentile(fit[ok], 1)), 4)}
grs = gr[ok]
out['gr_pct'] = {p: round(float(np.percentile(grs, p)), 2) for p in (0.1, 1, 5, 50)}
out['sec_gr_lt_-1dB'] = round(float((grs < -1).sum() * 0.01), 2); out['sec_gr_lt_-2dB'] = round(float((grs < -2).sum() * 0.01), 2); out['sec_gr_lt_-3dB'] = round(float((grs < -3).sum() * 0.01), 2)
# en derin olaylar
tt = (np.arange(nb) + 0.5) * 0.01
idx = np.where(ok & (gr < -1.5))[0]
ev = []
if len(idx):
    for grp in np.split(idx, np.where(np.diff(idx) > 20)[0] + 1):
        i = grp[np.argmin(gr[grp])]; t0 = tt[i]
        cue = next((c for c, v in CUES.items() if v['s'] - .1 <= t0 <= v['e'] + .1), 'boşluk')
        w = next((x['w'] for x in WORDS if x['s'] - .05 <= t0 <= x['e'] + .05), '')
        ev.append((round(float(t0), 2), round(float(gr[i]), 2), round(len(grp) * 0.01, 2), cue, w))
out['events_lt_-1.5dB'] = sorted(ev, key=lambda z: z[1])[:25]; out['n_events'] = len(ev)
np.save('gr.npy', np.stack([tt, gr]).astype(np.float32))
json.dump(out, open('lim.json', 'w'), indent=1, ensure_ascii=False); print(json.dumps(out, indent=1, ensure_ascii=False))
