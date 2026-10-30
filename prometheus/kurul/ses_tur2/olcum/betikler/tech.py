import sys, numpy as np, soundfile as sf, json
from scipy import signal
from common import *
out = {}
x, sr = sf.read(P + 'audio/mix.wav', dtype='float32', always_2d=True); x = np.ascontiguousarray(x.T)
N = x.shape[1]; out['dur'] = N / SR
out['sample_peak_dBFS'] = float(20 * np.log10(np.abs(x).max()))
out['clip_samples_ge_-0.1dBFS'] = int((np.abs(x) >= 10 ** (-0.1 / 20)).sum())
out['dc'] = [float(x[c].mean()) for c in range(2)]
# gerçek tepe, 4x, 10 sn parçalar
tps = []
L, pad = SR * 10, 256
for a in range(0, N, L):
    m = 0
    for c in range(2):
        seg = x[c, max(0, a - pad):min(N, a + L + pad)].astype(np.float64)
        m = max(m, float(np.abs(signal.resample_poly(seg, 4, 1)).max()))
    tps.append((a / SR, 20 * np.log10(m + 1e-12)))
tps = np.array(tps); out['true_peak_dBTP'] = float(tps[:, 1].max())
out['tp_top_chunks'] = [(float(t), round(float(v), 2)) for t, v in tps[np.argsort(-tps[:, 1])[:8]]]
# K-ağırlıklı yükseklik
xk = kfilt(x)
ms = block_ms(xk, 0.1); np.save('mix_ms100.npy', ms)
out['integrated_LUFS'] = float(integrated(ms))
r = lra(ms); out['LRA'] = [round(float(v), 2) for v in r]
S = win_lufs(ms, 30); tS = (np.arange(len(S)) * 0.1 + 1.5)
np.save('mix_short.npy', np.stack([tS, S]))
valid = S > -70
out['short_pct'] = {p: round(float(np.percentile(S[valid], p)), 2) for p in (1, 5, 10, 50, 90, 95, 99)}
i = np.argmax(S); out['short_max'] = (round(float(tS[i]), 1), round(float(S[i]), 2))
# en sessiz (anlatım bölgesinde, 2-1421 sn)
m = (tS > 3) & (tS < 1420)
j = np.argmin(np.where(m, S, 99)); out['short_min_in_film'] = (round(float(tS[j]), 1), round(float(S[j]), 2))
# bölüm ortalamaları
secs = {}
for c, v in CUES.items(): secs.setdefault(v['sec'], [v['s'], v['e']]); secs[v['sec']][1] = v['e']
out['sec_short_median'] = {}
for k, (a, b) in secs.items():
    mm = (tS >= a) & (tS <= b)
    out['sec_short_median'][SECS[k]] = [round(float(np.median(S[mm])), 2), round(float(S[mm].min()), 2), round(float(S[mm].max()), 2)]
# mono uyumu
mono = (x[0] + x[1]) / 2
mk = kfilt(np.stack([mono, mono])); msm = block_ms(mk, 0.1); del mk
out['mono_fold_LUFS'] = float(integrated(msm))
side = (x[0] - x[1]) / 2
out['side_to_mid_dB'] = float(10 * np.log10((side.astype(np.float64) ** 2).mean() / (mono.astype(np.float64) ** 2).mean()))
# 1 sn korelasyon
h = SR; n = N // h
Lr = x[0, :n * h].reshape(n, h).astype(np.float64); Rr = x[1, :n * h].reshape(n, h).astype(np.float64)
corr = (Lr * Rr).sum(1) / np.sqrt((Lr ** 2).sum(1) * (Rr ** 2).sum(1) + 1e-20)
np.save('corr1s.npy', corr)
out['corr_pct'] = {p: round(float(np.percentile(corr, p)), 3) for p in (0.5, 1, 5, 50)}
out['corr_lt0_seconds'] = int((corr < 0).sum()); out['corr_lt0.3_seconds'] = int((corr < 0.3).sum())
out['corr_min'] = (int(np.argmin(corr)), round(float(corr.min()), 3))
# alçak frekans korelasyonu (<150 Hz)
sos = signal.butter(4, 150, 'lowpass', fs=SR, output='sos')
lo = signal.sosfilt(sos, x, axis=1)
Ll = lo[0, :n * h].reshape(n, h); Rl = lo[1, :n * h].reshape(n, h)
cl = (Ll * Rl).sum(1) / np.sqrt((Ll ** 2).sum(1) * (Rl ** 2).sum(1) + 1e-20)
out['lf_corr_min'] = round(float(cl.min()), 3); out['lf_corr_pct1'] = round(float(np.percentile(cl, 1)), 3)
# spektrum (Welch) orta kanal
f, Pm = signal.welch(mono, SR, nperseg=1 << 15)
tot = Pm.sum()
bands = [(0, 20), (20, 30), (30, 40), (40, 60), (60, 100), (100, 200), (200, 500), (500, 1000), (1000, 2000), (2000, 4000), (4000, 8000), (8000, 16000), (16000, 24000)]
out['band_share_dB'] = {f'{a}-{b}': round(float(10 * np.log10(Pm[(f >= a) & (f < b)].sum() / tot + 1e-20)), 1) for a, b in bands}
np.save('mix_psd.npy', np.stack([f, Pm]))
json.dump(out, open('tech.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
