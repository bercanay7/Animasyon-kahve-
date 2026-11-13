import numpy as np, soundfile as sf, json
from scipy import signal
from common import *
out = {}
mu = np.load('mu.npy', mmap_mode='r'); vo = np.load('vo.npy', mmap_mode='r')
def lev(a, b, x):
    i, j = int(a * SR), int(b * SR); s = np.asarray(x[..., i:j], np.float64); return 10 * np.log10((s ** 2).mean() + 1e-20)
# dip dönüşleri: [b-0.45, b+0.1] içinde 50 ms'lik pencereler arası en büyük adım
dips = {'D11 sonrası': 332.80, 'F14 olacak': W('F14', 'olacak') - 0.1, 'J02 zeustan': W('J02', 'zeustan') - 0.2}
out['dip_returns'] = {}
for k, b in dips.items():
    ts = np.arange(b - 0.5, b + 0.15, 0.05); L = [lev(t, t + 0.05, mu) for t in ts]
    out['dip_returns'][k] = dict(t=round(b, 2), before=round(L[0], 1), after=round(L[-1], 1), max_step_50ms=round(float(np.max(np.diff(L))), 1))
# eski ölçüm biçimi: dönüş anında 120 ms önce/sonra
    out['dip_returns'][k]['pm120'] = (round(lev(b - .15, b - .03, mu), 1), round(lev(b + .03, b + .15, mu), 1))
# I12 eski dip bölgesi
out['I12_old_dip_region_music'] = round(lev(1205.55, 1206.17, mu), 1)
# D11 sessizliği: müzik 50 ms seviyesi, -40 dB altındaki kesintisiz süre
ts = np.arange(330.9, 333.3, 0.05); L = np.array([lev(t, t + 0.05, mu) for t in ts])
ref = lev(326, 331, mu)
quiet = L < ref - 20
best, cur, st, bst = 0, 0, None, None
for i, q in enumerate(quiet):
    cur = cur + 1 if q else 0
    if cur == 1: st = ts[i]
    if cur > best: best, bst = cur, st
out['D11_silence'] = dict(ref_sentence_music=round(ref, 1), longest_20dB_below_s=round(best * 0.05, 2), start=round(float(bst), 2) if bst else None, min_level=round(float(L.min()), 1))
# alçak frekans mono uyumu (son miks)
sos = signal.butter(4, 120, 'lowpass', fs=SR, output='sos'); zi = np.zeros((sos.shape[0], 2, 2)); h = SR // 2
PL, PR, PM, PT = [], [], [], []
with sf.SoundFile(P + 'audio/mix.wav') as f:
    while True:
        x = f.read(SR * 30, dtype='float64', always_2d=True)
        if len(x) == 0: break
        y, zi = signal.sosfilt(sos, x, axis=0, zi=zi); n = len(y) // h
        L_ = y[:n*h, 0].reshape(n, h); R_ = y[:n*h, 1].reshape(n, h)
        PL.append((L_**2).mean(1)); PR.append((R_**2).mean(1)); PM.append((((L_+R_)/2)**2).mean(1)); PT.append((x[:n*h]**2).sum(1).reshape(n, h).mean(1) / 2)
PL, PR, PM, PT = map(np.concatenate, (PL, PR, PM, PT))
st_ = (PL + PR) / 2; loss = 10 * np.log10(PM / (st_ + 1e-20) + 1e-20); share = 10 * np.log10(st_ / (PT + 1e-20) + 1e-20)
big = share > -6
out['lf_mono'] = dict(weighted=round(float(10*np.log10(PM.sum()/st_.sum())), 2), n_lf_dominant=int(big.sum()), n_loss_gt3=int((big & (loss < -3)).sum()), worst=round(float(loss[big].min()), 2),
                      list=[(round(i*0.5, 1), round(float(loss[i]), 1)) for i in np.where(big & (loss < -3))[0]][:20])
json.dump(out, open('post.json', 'w'), indent=1, ensure_ascii=False); print(json.dumps(out, indent=1, ensure_ascii=False))
