"""Shorts sesi: anlatım + sürekli müzik yatağı (açılış → final) + kesitlere ait film efektleri → shorts/mix_shorts.wav"""
import os, sys, json
import numpy as np, soundfile as sf, librosa, pyloudnorm as pyln
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools'))
import mix as M
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
SR = 48000
ed = json.load(open(os.path.join(D, 'edl.json')))
N = int(np.ceil(ed['DUR'] * SR))
meter = pyln.Meter(SR)
db = lambda g: 10 ** (g / 20)
# anlatım
vo, _ = librosa.load(os.path.join(D, ed['TAKE'] + '.mp3'), sr=SR, mono=True)
vo = M.hp(vo, 70)
v = np.zeros(N); a = int(ed['VO_OFF'] * SR); v[a:a + len(vo)] = vo[:N - a]
v *= db(-16 - meter.integrated_loudness(v))
# müzik yatağı: film müziği 0.55'ten (zincir vuruşu görüntüyle hizalı), Camus kısmında finalin sıcak müziği (bitişle hizalı)
mu, msr = sf.read(os.path.join(R, 'audio', 'music.wav'), always_2d=True); mu = mu.T
def seg(f0, n):
    a = int(f0 * SR); x = mu[:, a:a + n]
    return np.pad(x, ((0, 0), (0, n - x.shape[1])))
xc = ed['EDL'][[c['f'] for c in ed['EDL']].index(296.0)]['s']  # "iki bin yıl" kesiti
bedA = seg(.55, N)
bedB = seg(424.9 - ed['DUR'], N)
t = np.arange(N) / SR
w = np.clip((t - (xc - .6)) / 1.2, 0, 1); w = np.sin(w * np.pi / 2) ** 2
bed = bedA * np.cos(w * np.pi / 2) + bedB * np.sin(w * np.pi / 2)
bed *= db(-22 - meter.integrated_loudness(bed.T))
# konuşma altında kısma
ve = M.envelope(v); act = np.clip((20 * np.log10(ve + 1e-9) + 42) / 10, 0, 1)
look = int(.12 * SR); tg = np.concatenate([db(-9 * act)[look:], np.ones(look)])
bed *= M.smooth_gain(tg, .1, .6)
# kapanış cümlesinin altında müzik ek -5 dB ("mutlu" öne çıksın)
ex = np.ones(N); ex[int(34.4 * SR):int(36.3 * SR)] = db(-5); ex[int(34.4 * SR):int(35.1 * SR)] = db(-8); ex[int(24.8 * SR):int(26.6 * SR)] = db(-5); ex[int(30.6 * SR):int(31.4 * SR)] = db(-3); ex[int(39.1 * SR):int(41.2 * SR)] = db(-3); ex = np.convolve(ex, np.ones(int(.2 * SR)) / int(.2 * SR), 'same'); bed *= ex
# efektler: her kesitin film anındaki efekt stemi (kısa çapraz geçişlerle)
fx_st, _ = sf.read(os.path.join(R, 'audio', 'stems', 'sfx.wav'), always_2d=True); fx_st = fx_st.T
fx = np.zeros((2, N)); xf = int(.06 * SR)
for c in ed['EDL']:
    a, b = int(c['s'] * SR), min(N, int(c['e'] * SR)); n = b - a
    sp = c.get('speed', 1); f0 = int(c['f'] * SR)
    if sp == 1: x = fx_st[:, f0:f0 + n]
    else:
        # hızlandırılmış kesit: ortam döngüleri normal hızda; tek seferlik efektler görüntüdeki yerlerine (f + (t - f) / hız) taşınır, perdeleri kaymaz
        ev = json.load(open(os.path.join(R, 'audio', 'sfx_events.json'))); evc = []
        for e in ev:
            if e.get('loop'):
                if e['t'] < c['f'] + n / SR and e['t'] + e['len'] > c['f']: evc.append(dict(e))
            elif c['f'] <= e['t'] < c['f'] + n * sp / SR: evc.append({**e, 't': c['f'] + (e['t'] - c['f']) / sp})
        dry, send = M.build_sfx('tr', events=evc)
        seg = lambda b_: b_[:, f0:f0 + n + int(2.5 * SR)]
        hp30 = M.signal.butter(4, 30, 'highpass', fs=SR, output='sos')
        wet = M.apply_reverb(np.stack([M.signal.sosfilt(hp30, ch) for ch in seg(send)]), M.reverb_ir())
        x = np.stack([M.signal.sosfilt(hp30, ch) for ch in seg(dry)])[:, :n] + wet[:, :n]
    x = np.pad(x, ((0, 0), (0, n - x.shape[1]))).copy()
    r = np.linspace(0, 1, min(xf, n)); x[:, :len(r)] *= r; x[:, n - len(r):] *= r[::-1]
    fx[:, a:b] += x
fx *= db(-2)
# vurgulu sözcüklerin altında efekt -4 dB
fe = np.ones(N)
for a0, b0, d0 in [(19.5, 21.0, -10), (25.4, 26.3, -4), (.6, 1.5, -6), (8.1, 8.9, -6), (24.9, 25.4, -5), (39.0, 39.6, -8)]: fe[int(a0 * SR):int(b0 * SR)] = db(d0)
fx *= np.convolve(fe, np.ones(int(.1 * SR)) / int(.1 * SR), 'same')
mixd = np.stack([v, v]) + bed + fx
mixd = M.limiter(mixd, .7)
mixd *= db(-14 - meter.integrated_loudness(mixd.T))
mixd = M.limiter(mixd, db(-1.6))
print('LUFS', round(meter.integrated_loudness(mixd.T), 2), 'TP', round(M.true_peak(mixd), 2))
sf.write(os.path.join(D, 'mix_shorts.wav'), mixd.T.astype(np.float32), SR, subtype='PCM_24')
