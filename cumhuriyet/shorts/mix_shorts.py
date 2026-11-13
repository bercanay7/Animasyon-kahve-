"""Shorts sesi: filmin anlatım kesitleri + müzik yatağı (ilk kesit → final → kapanış kesiti, döngüye dikişsiz) + kesitlere ait efektler → shorts/mix_shorts.wav
Önce tools/mix.py --stems çalışmış olmalı (audio/stems/{vo,music,sfx}.wav). python3 shorts/mix_shorts.py"""
import os, sys, json
import numpy as np, soundfile as sf, pyloudnorm as pyln
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools'))
import mix as M
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(D)
SR = 48000
ed = json.load(open(os.path.join(D, 'edl.json')))
N = int(np.ceil(ed['DUR'] * SR))
meter = pyln.Meter(SR)
db = lambda g: 10 ** (g / 20)
def stem(name):
    p = os.path.join(os.environ.get('STEMS') or os.path.join(R, 'audio', 'stems'), name + '.wav')  # STEMS=… ile başka stem klasörü
    if not os.path.exists(p): return None
    x, sr = sf.read(p, always_2d=True); assert sr == SR, p
    return x.T
def cut_clips(src, xf=.05):
    """her kesitin film anındaki parçası, kesitin shorts yerine (kısa yumuşak kenarlarla)"""
    out = np.zeros((2, N)); k = int(xf * SR)
    for c in ed['EDL']:
        a, b = int(c['s'] * SR), min(N, int(c['e'] * SR)); n = b - a; f0 = int(c['f'] * SR)
        x = src[:, f0:f0 + n]; x = np.pad(x, ((0, 0), (0, n - x.shape[1]))).copy()
        r = np.linspace(0, 1, min(k, n)); x[:, :len(r)] *= r; x[:, n - len(r):] *= r[::-1]
        out[:, a:b] += x
    return out
vo = stem('vo')
if vo is None:  # stem yoksa ham anlatım
    import librosa
    vo = librosa.load(os.path.join(R, 'vo', 'vo.wav'), sr=SR, mono=True)[0]; vo = np.stack([vo, vo])
v = cut_clips(vo)
v *= db(-16 - meter.integrated_loudness(v.T))
# müzik yatağı (kanca kurulu H4): ilk kesitten başlayan filmin kendi müziği kesintisiz; G01'den önce finalin müziğine
# (G02 ile hizalı) 1,2 sn çapraz geçiş; kapanış kesitinde yine filmin o anki müziği (0,6 sn geçiş) → döngü dikişi sessiz ve kesintisiz
mu, msr = sf.read(os.path.join(R, 'audio', 'music.wav'), always_2d=True); mu = mu.T
assert msr == SR
def seg(f0, n):
    a = max(0, int(f0 * SR)); x = mu[:, a:a + n]
    return np.pad(x, ((0, 0), (0, n - x.shape[1])))
E_ = {c['id']: c for c in ed['EDL']}
t = np.arange(N) / SR
def xf(a, b, at, d):
    w = np.clip((t - (at - d / 2)) / d, 0, 1); w = np.sin(w * np.pi / 2) ** 2
    return a * np.cos(w * np.pi / 2) + b * np.sin(w * np.pi / 2)
first, last = ed['EDL'][0], ed['EDL'][-1]
bedA = seg(first['f'] - first['s'], N)
bedB = seg(E_['G02a']['f'] - E_['G02a']['s'], N)
bedC = seg(last['f'] - last['s'], N)
bed = xf(xf(bedA, bedB, E_['G01a']['s'], 1.2), bedC, last['s'], .6)
bed *= db(-21 - meter.integrated_loudness(bed.T))
# konuşma altında kısma
# döngüsel hesap: Shorts sonu başına bağlandığı için kısma kazancı da sarılır (dikişte seviye sıçraması olmaz)
P = 2 * SR; vm = v.mean(0); vw = np.concatenate([vm[-P:], vm, vm[:P]])
ve = M.envelope(vw) if hasattr(M, 'envelope') else np.abs(vw)
act = np.clip((20 * np.log10(ve + 1e-9) + 42) / 10, 0, 1)
look = int(.12 * SR); tg = np.concatenate([db(-8 * act)[look:], np.ones(look)])
if hasattr(M, 'smooth_gain'): tg = M.smooth_gain(tg, .1, .6)
else: tg = np.convolve(tg, np.ones(int(.2 * SR)) / int(.2 * SR), 'same')
bed *= tg[P:P + N]
fx = stem('sfx')
fx = cut_clips(fx, .06) * db(-1) if fx is not None else np.zeros((2, N))
mixd = v + bed + fx
mixd *= db(-14 - meter.integrated_loudness(mixd.T))
mixd = M.limiter(mixd, db(-1.6)) if hasattr(M, 'limiter') else np.clip(mixd, -.83, .83)
mixd *= db(-14 - meter.integrated_loudness(mixd.T)); mixd = np.clip(mixd, -db(-1.2), db(-1.2))
tp = M.true_peak(mixd) if hasattr(M, 'true_peak') else 20 * np.log10(np.abs(mixd).max())
print('LUFS', round(meter.integrated_loudness(mixd.T), 2), 'TP', round(tp, 2))
sf.write(os.path.join(D, 'mix_shorts.wav'), mixd.T.astype(np.float32), SR, subtype='PCM_24')
