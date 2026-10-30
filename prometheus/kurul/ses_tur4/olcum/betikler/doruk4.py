import numpy as np, soundfile as sf, json
from common import *
dB = lambda p: 10 * np.log10(p + 1e-20)
def mixlev(path, a, b):
    x, _ = sf.read(path, start=int(a*SR), stop=int(b*SR), dtype='float64', always_2d=True)
    xk = kfilt(x.T); return round(float(-0.691 + 10*np.log10((xk**2).sum(0).mean())), 1)
OLD1 = '/tmp/claude-0/-home-user/c3662c9d-24be-574f-ac5d-de35ddf76b95/scratchpad/mix_before_ses1.wav'; NEW = P + 'audio/mix.wav'
T2_old = {'A04 başlık sonrası': -16.0, 'C18 sonrası motif': -15.3, 'J04→J05 boşluğu': -17.0, 'K06 sonrası boşluk': -15.2, 'C10 indirdi': -16.0, 'bitiş ekranı': -19.6, 'J04 Prometheus özgürdür': -12.7, 'I10 fırtına': -14.0}
spots = [('A04 başlık sonrası', 25.5, 27.0), ('C18 sonrası motif', 234.7, 236.9), ('J04→J05 boşluğu', 1082.8, 1084.19), ('K06 sonrası boşluk', 1386.22, 1389.26), ('C10 indirdi', 178.0, 178.9), ('bitiş ekranı', 1421.64, 1435.0), ('J04 Prometheus özgürdür', 1081.45, 1082.8), ('I10 fırtına', 1166.5, 1185.0)]
import json as _j
_d3 = _j.load(open('../ses3/doruk3.json')); T2 = {r[0]: r[3] for r in _d3}; T1 = {r[0]: r[1] for r in _d3}
out = []
for n, a, b in spots:
    r = (n, T1[n], T2[n], mixlev(NEW, a, b)); out.append(r); print(f'{n:26s} tur1 {r[1]:6.1f}  tur3 {r[2]:6.1f}  tur4 {r[3]:6.1f}')
ms = np.load('mix_short.npy'); i = np.argmax(ms[1]); print('en yüksek kısa süreli', round(float(ms[0][i]), 1), round(float(ms[1][i]), 2))
for t in (1083.5, 1387.5, 26.0, 235.5):
    j = np.argmin(abs(ms[0] - t)); print('kısa süreli @', t, round(float(ms[1][j]), 2))
json.dump(out, open('doruk4.json', 'w'), ensure_ascii=False)
