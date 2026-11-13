# mix.py zincirini değiştirmeden yeniden üretir: işlenmiş anlatım (mono), yankı gönderimi ve kısılmış müzik (stereo), sınırlayıcı öncesi
import sys, os, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal
sys.path.insert(0, '/home/user/Animasyon-kahve-/prometheus/tools')
import mix as M
OUT = os.path.dirname(os.path.abspath(__file__))
SR, N, db, A = M.SR, M.N, M.db, M.A
meter = pyln.Meter(SR)
vo, sr = sf.read(A('vo/vo.wav'), always_2d=False, dtype='float32')
vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]
vo = M.hp(vo, 70)
vo *= db(-16 - meter.integrated_loudness(vo))
vo = M.voice_chain(vo)
vo = (vo * db(-16 - meter.integrated_loudness(vo))).astype(np.float32)
ve = M.envelope(vo).astype(np.float32)
act = np.clip((20 * np.log10(ve + 1e-9) + 42) / 10, 0, 1); del ve
target = db(-3 * act).astype(np.float32); del act
look = int(.12 * SR); target = np.concatenate([target[look:], np.ones(look, np.float32)])
duck = M.smooth_gain(target, .1, 1.5).astype(np.float32); del target
np.save(os.path.join(OUT, 'duck.npy'), duck[::480].copy())   # 100 Hz
ir = M.reverb_ir(1.2)
send = np.stack([signal.oaconvolve(vo * np.float32(db(-26)), ir[c].astype(np.float32))[:N].astype(np.float32) for c in range(2)])
np.save(os.path.join(OUT, 'vo.npy'), vo); np.save(os.path.join(OUT, 'send.npy'), send); del send
mu, msr = sf.read(A('audio/music.wav'), always_2d=True, dtype='float32')
mu = np.ascontiguousarray(mu.T)
mu = np.pad(mu, ((0, 0), (0, max(0, N - mu.shape[1]))))[:, :N]
hp35 = signal.butter(4, 35, 'highpass', fs=SR, output='sos')
for c in range(2): mu[c] = M.peq(signal.sosfilt(hp35, mu[c]), 60, -2.5, .7).astype(np.float32)
g = db(-21 - meter.integrated_loudness(mu.T)); print('music norm gain dB', 20*np.log10(g))
mu *= np.float32(g)
np.save(os.path.join(OUT, 'mu_preduck.npy'), mu)
mu *= duck
mu = M.limiter(mu, db(-8), look=.005, rel=.15).astype(np.float32)
np.save(os.path.join(OUT, 'mu.npy'), mu)
print('ok', flush=True)
