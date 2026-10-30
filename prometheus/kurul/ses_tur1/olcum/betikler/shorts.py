import numpy as np, soundfile as sf, json
from scipy import signal
from common import *
x, _ = sf.read(P + 'shorts/mix_shorts.wav', dtype='float64', always_2d=True); x = x.T
ed = json.load(open(P + 'shorts/edl.json'))
out = {'dur': x.shape[1] / SR, 'F0': ed['F0'], 'F1': ed['F1']}
m = pyln.Meter(SR); out['LUFS'] = round(m.integrated_loudness(x.T), 2)
out['TP'] = round(20 * np.log10(max(np.abs(signal.resample_poly(x[c], 4, 1)).max() for c in range(2))), 2)
out['sample_peak'] = round(20 * np.log10(np.abs(x).max()), 2)
xk = kfilt(x); ms = block_ms(xk, 0.1); S = win_lufs(ms, 30); Mo = win_lufs(ms, 4)
out['LRA'] = [round(float(v), 2) for v in lra(ms)]
out['momentary_first_1s'] = [round(float(v), 1) for v in Mo[:8]]  # 0.4 s pencere, 0.1 adım: 0.0-0.4 ... 0.7-1.1
out['momentary_last'] = [round(float(v), 1) for v in Mo[-10:]]
def rmsdb(a, b): seg = x[:, int(a * SR):int(b * SR)]; return round(float(10 * np.log10((seg ** 2).mean() + 1e-20)), 1)
out['rms_0-0.1'] = rmsdb(0, .1); out['rms_0.1-0.3'] = rmsdb(.1, .3); out['rms_0.3-1.0'] = rmsdb(.3, 1.0)
out['rms_last_0.1'] = rmsdb(out['dur'] - .1, out['dur']); out['rms_last_1s'] = rmsdb(out['dur'] - 1, out['dur'])
# kelimeler (kısa film zamanına göre)
F0 = ed['F0']
ws = [w for w in WORDS if w['s'] >= F0 - 0.5 and w['e'] <= ed['F1'] + 0.5]
out['first_word'] = (ws[0]['w'], round(ws[0]['s'] - F0, 2)); out['last_word'] = (ws[-1]['w'], round(ws[-1]['s'] - F0, 2), round(ws[-1]['e'] - F0, 2))
fo_start = out['dur'] - 1.4
out['fade_out_start'] = round(fo_start, 2)
g = lambda t: np.cos(np.pi / 2 * min(1, max(0, (t - fo_start) / 1.4))) ** 2
out['fade_gain_at_last_word_start_end_dB'] = [round(20 * np.log10(g(ws[-1]['s'] - F0) + 1e-9), 2), round(20 * np.log10(g(ws[-1]['e'] - F0) + 1e-9), 2)]
# kısa süreli seyir
out['short_term_pct'] = {p: round(float(np.percentile(S[S > -70], p)), 1) for p in (5, 50, 95)}
np.save('shorts_mom.npy', Mo)
json.dump(out, open('shorts.json', 'w'), indent=1, ensure_ascii=False); print(json.dumps(out, indent=1, ensure_ascii=False))
