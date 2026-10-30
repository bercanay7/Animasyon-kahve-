"""Shorts sesi: filmin son miksinden (audio/mix.wav) kesintisiz kesit; yumuşak giriş/çıkış, -14 LUFS / -1,6 dBTP → shorts/mix_shorts.wav"""
import os, sys, json
import numpy as np, soundfile as sf, pyloudnorm as pyln
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools'))
import mix as M
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
ed = json.load(open(os.path.join(D, 'edl.json')))
x, SR = sf.read(os.path.join(R, 'audio', 'mix.wav'), always_2d=True); x = x.T
a, n = int(ed['F0'] * SR), int(np.ceil(ed['DUR'] * SR))
y = x[:, a:a + n].copy(); y = np.pad(y, ((0, 0), (0, n - y.shape[1])))
fi, fo = int(.25 * SR), int(1.4 * SR)
y[:, :fi] *= np.sin(np.linspace(0, np.pi / 2, fi)) ** 2
y[:, n - fo:] *= np.cos(np.linspace(0, np.pi / 2, fo)) ** 2
meter = pyln.Meter(SR); db = lambda g: 10 ** (g / 20)
y *= db(-14 - meter.integrated_loudness(y.T))
y = M.limiter(y, db(-1.6))
print('LUFS', round(meter.integrated_loudness(y.T), 2), 'TP', round(M.true_peak(y), 2), 'süre', round(n / SR, 2))
sf.write(os.path.join(D, 'mix_shorts.wav'), y.T.astype(np.float32), SR, subtype='PCM_24')
