"""Shorts sesi: filmin son miksinden (audio/mix.wav) kesintisiz kesit; yumuşak giriş/çıkış, -14 LUFS / -1,6 dBTP → shorts/mix_shorts.wav"""
import os, sys, json
import numpy as np, soundfile as sf, pyloudnorm as pyln
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools'))
import mix as M
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
ed = json.load(open(os.path.join(D, 'edl.json')))
x, SR = sf.read(os.path.join(R, 'audio', 'mix.wav'), always_2d=True); x = x.T
a, n = int(ed['F0'] * SR), int(np.ceil(ed['DUR'] * SR))
# atlama kesmeleri: filmden parça parça alınır, birleşmeler 80 ms eşit güçlü geçişle (müzik yatağında tık olmaz)
xf = int(.08 * SR); pieces, t0 = [], ed['F0']
for ca, cb in ed.get('CUTS', []) + [[ed['F1'], None]]:
    pieces.append(x[:, int(t0 * SR):int(ca * SR) + (xf // 2 if cb else 0)].copy()); t0 = (cb or 0) - xf / 2 / SR
y = pieces[0]
for p_ in pieces[1:]:
    w = np.linspace(0, np.pi / 2, xf); y = np.concatenate([y[:, :-xf], y[:, -xf:] * np.cos(w) + p_[:, :xf] * np.sin(w), p_[:, xf:]], 1)
y = y[:, :n]; y = np.pad(y, ((0, 0), (0, n - y.shape[1])))
fi, fo = int(.12 * SR), int(.35 * SR)   # F1 son kelimeden 0,35 sn sonra: solma kelimeden sonra başlar, döngü dikişi ≈ 0,5 sn (Shorts kurulu tur 1)
y[:, :fi] *= np.sin(np.linspace(0, np.pi / 2, fi)) ** 2
y[:, n - fo:] *= np.cos(np.linspace(0, np.pi / 2, fo)) ** 2
meter = pyln.Meter(SR); db = lambda g: 10 ** (g / 20)
y *= db(-14 - meter.integrated_loudness(y.T))
y = M.limiter(y, db(-1.6))
print('LUFS', round(meter.integrated_loudness(y.T), 2), 'TP', round(M.true_peak(y), 2), 'süre', round(n / SR, 2))
sf.write(os.path.join(D, 'mix_shorts.wav'), y.T.astype(np.float32), SR, subtype='PCM_24')
