import numpy as np, soundfile as sf, json, librosa
from scipy import signal
from common import *
ed = json.load(open(P + 'shorts/edl.json')); F0 = ed['F0']; ca, cb = ed['CUTS'][0]
y, _ = sf.read(P + 'shorts/mix_shorts.wav', dtype='float64', always_2d=True); y = y.T
x, _ = sf.read(P + 'audio/mix.wav', start=int((F0 - 1) * SR), stop=int((ed['F1'] + 1) * SR), dtype='float64', always_2d=True); x = x.T
s = ca - F0; i = int(s * SR)
out = {'cut_film': [ca, cb], 'seam_short_s': round(s, 3), 'dur': round(y.shape[1] / SR, 3)}
d = np.abs(np.diff(y, axis=1)).max(0)
out['max_jump_seam_pm50ms'] = round(float(d[i - 2400:i + 2400].max()), 4)
out['jump_p999_file'] = round(float(np.percentile(d, 99.9)), 4); out['jump_p50_seam_region_1s'] = round(float(np.median(d[i - SR:i + SR])), 5)
def env(z, lo=None, hi=None, w=.005):
    if lo or hi:
        sos = signal.butter(4, [lo, hi] if lo and hi else (hi or lo), ('bandpass' if lo and hi else ('lowpass' if hi else 'highpass')), fs=SR, output='sos'); z = signal.sosfilt(sos, z, axis=1)
    h = int(w * SR); n = z.shape[1] // h; return 10 * np.log10((z[:, :n*h] ** 2).reshape(2, n, h).mean((0, 2)) + 1e-20)
h = int(.005 * SR); k = i // h
for name, lo, hi in [('geniş', None, None), ('<150 Hz', None, 150), ('400-500 Hz (A4)', 400, 500), ('1-4k', 1000, 4000)]:
    e = env(y, lo, hi); seg = e[k - 60:k + 61]
    out['env_' + name] = dict(before_0_3s=round(float(np.mean(e[k - 60:k - 10])), 1), after_0_3s=round(float(np.mean(e[k + 10:k + 61])), 1), seam_min=round(float(seg[50:71].min()), 1), seam_max=round(float(seg[50:71].max()), 1))
    # filmde kesmesiz aynı konum (kesimin başı) için karşılaştırma: film ca öncesi ve cb sonrası
    ef = env(x, lo, hi); kf_a = int((ca - (F0 - 1)) * SR) // h; kf_b = int((cb - (F0 - 1)) * SR) // h
    out['env_' + name]['film_at_ca'] = round(float(np.mean(ef[kf_a - 10:kf_a])), 1); out['env_' + name]['film_at_cb'] = round(float(np.mean(ef[kf_b:kf_b + 10])), 1)
# kroma ve spektral süreklilik: kesimden önceki ve sonraki 0,3 sn
def chroma(z): return librosa.feature.chroma_stft(y=z.mean(0).astype(np.float32), sr=SR, n_fft=8192, hop_length=2048).mean(1)
def spec(z):
    f, p = signal.welch(z.mean(0), SR, nperseg=4096); m = (f > 30) & (f < 8000); return 10 * np.log10(p[m] + 1e-20)
A, B = y[:, i - int(.35 * SR):i - int(.05 * SR)], y[:, i + int(.05 * SR):i + int(.35 * SR)]
cos = lambda u, v: float(np.dot(u, v) / np.linalg.norm(u) / np.linalg.norm(v))
out['chroma_cos_seam'] = round(cos(chroma(A), chroma(B)), 3); out['spec_dist_seam_dB'] = round(float(np.sqrt(np.mean((spec(A) - spec(B)) ** 2))), 2)
# başvuru: filmde, kesmesiz, ardışık iki 0,3 sn pencere (aynı bölgede, çeşitli konumlarda)
refs = []
for t in np.arange(1055.0, 1068.0, 0.5):
    j = int((t - (F0 - 1)) * SR); A2, B2 = x[:, j - int(.35 * SR):j - int(.05 * SR)], x[:, j + int(.05 * SR):j + int(.35 * SR)]
    refs.append((round(cos(chroma(A2), chroma(B2)), 3), round(float(np.sqrt(np.mean((spec(A2) - spec(B2)) ** 2))), 2)))
r = np.array(refs); out['ref_chroma_cos_min_med'] = [float(r[:, 0].min()), float(np.median(r[:, 0]))]; out['ref_spec_dist_med_max'] = [float(np.median(r[:, 1])), float(r[:, 1].max())]
# stereo ilinti geçiş boyunca
seg = y[:, i - 2400:i + 2400]; out['corr_seam_100ms'] = round(float((seg[0] * seg[1]).sum() / np.sqrt((seg[0] ** 2).sum() * (seg[1] ** 2).sum())), 3)
# konuşma: kesime en yakın kelimeler
out['nearest_words'] = [(w['w'], round(w['e'], 2)) for w in WORDS if ca - 1 < w['e'] < ca] + [(w['w'], round(w['s'], 2)) for w in WORDS if cb < w['s'] < cb + 1]
m = pyln.Meter(SR); out['LUFS'] = round(m.integrated_loudness(y.T), 2)
out['TP'] = round(20 * np.log10(max(np.abs(signal.resample_poly(y[c], 4, 1)).max() for c in range(2))), 2)
json.dump(out, open('seam.json', 'w'), indent=1, ensure_ascii=False); print(json.dumps(out, indent=1, ensure_ascii=False))
