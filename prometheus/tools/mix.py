"""Son miks: anlatım + müzik (efektler müzikle birlikte score.py'de sentezlendi) → audio/mix.wav (-14 LUFS, ≤ -1 dBTP)

python3 tools/mix.py            # tam miks
python3 tools/mix.py --stems    # ayrıca audio/stems/vo.wav ve music.wav (Shorts kaynağı)
"""
import json, sys, os, re
import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal
from scipy.ndimage import maximum_filter1d, uniform_filter1d

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
A = lambda p: os.path.join(ROOT, p)
TL = open(A('timeline.js')).read()
DUR = float(re.search(r'window\.DUR\s*=\s*([\d.]+)', TL).group(1))
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', TL).group(1))
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', TL, re.S).group(1))
N = int(np.ceil(DUR * SR))
db = lambda g: 10 ** (g / 20)
rng = np.random.default_rng(7)
def W(i, w, n=0):
    k = 0
    for x in WORDS:
        if x['id'] == i and x['w'].startswith(w):
            if k == n: return x['s']
            k += 1
    return CUES[i]['s']
def We(i, w, n=0):
    k = 0
    for x in WORDS:
        if x['id'] == i and x['w'].startswith(w):
            if k == n: return x['e']
            k += 1
    return CUES[i]['e']


def env_ad(n, a, d, shape=4.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) * shape / max(d, 1e-4))
    return e

def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], 'bandpass', fs=SR, output='sos')
    return signal.sosfilt(sos, x)

def lp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, 'lowpass', fs=SR, output='sos'), x)

def hp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, 'highpass', fs=SR, output='sos'), x)

def reverb_ir(dur=2.4, pre=.02):
    n = int(dur * SR); t = np.arange(n) / SR
    ir = []
    for ch in range(2):
        x = rng.standard_normal(n) * np.exp(-t * 6.9 / dur)
        x = lp(x, 5200) * (1 - np.exp(-t * 300))
        ir.append(np.concatenate([np.zeros(int(pre * SR)), x]))
    ir = np.array(ir); ir /= np.sqrt(np.sum(ir ** 2, axis=1, keepdims=True))
    return ir

def apply_reverb(x, ir):
    return np.stack([signal.oaconvolve(x[c], ir[c])[:N] for c in range(2)])

def envelope(x, win=.03):
    w = int(win * SR)
    e = np.sqrt(np.maximum(0, uniform_filter1d(x ** 2, max(1, w), mode='nearest')))
    return e

def smooth_gain(target, att=.08, rel=.6):
    """tek kutuplu, ayrı saldırı/bırakma ile kazanç yumuşatma (100 Hz kontrol hızı)"""
    hop = SR // 100; tg = target[::hop]; g = np.empty_like(tg); cur = 1.0
    aa, ar = np.exp(-1 / (att * 100)), np.exp(-1 / (rel * 100))
    for i, v in enumerate(tg):
        c = aa if v < cur else ar; cur = c * cur + (1 - c) * v; g[i] = cur
    return np.interp(np.arange(len(target)), np.arange(len(g)) * hop, g)

def peq(x, f0, gdb, q=1.0):
    A = 10 ** (gdb / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w), 1 - al * A]; a = [1 + al / A, -2 * np.cos(w), 1 - al / A]
    return signal.lfilter(np.array(b) / a[0], np.array(a) / a[0], x)

def compress(x, thr_db, ratio=3.0, att=.008, rel=.1):
    w = int(.005 * SR); p = np.sqrt(np.maximum(0, uniform_filter1d(x ** 2, max(1, w), mode='nearest'))) + 1e-9
    lvl = 20 * np.log10(p); over = np.maximum(0, lvl - thr_db); gr = -over * (1 - 1 / ratio)
    hop = SR // 1000; g = gr[::hop]; out = np.empty_like(g); cur = 0.0
    aa, ar = np.exp(-1 / (att * 1000)), np.exp(-1 / (rel * 1000))
    for i, v in enumerate(g):
        c = aa if v < cur else ar; cur = c * cur + (1 - c) * v; out[i] = cur
    gg = np.interp(np.arange(len(x)), np.arange(len(out)) * hop, out)
    return x * 10 ** (gg / 20), gg

def limiter(x, ceil=.89, look=.005, rel=.08):
    a = np.max(np.abs(x), axis=0)
    w = int(look * SR)
    pk = maximum_filter1d(a, w + 1, origin=-(w // 2))  # ileriye bakan tepe
    need = np.minimum(1, ceil / (pk + 1e-9))
    hop = 48; tg = need[::hop]; g = np.empty_like(tg); cur = 1.0; ar = np.exp(-hop / (rel * SR))
    for i, v in enumerate(tg):
        cur = v if v < cur else ar * cur + (1 - ar) * v; g[i] = cur
    gg = np.interp(np.arange(x.shape[1]), np.arange(len(g)) * hop, g)
    gg = np.minimum(gg, need)  # kesin tavan
    return x * gg

def true_peak(x):
    # 4× aşırı örnekleme parça parça (tam uzunlukta 4× dizi ~4 GB bellek ister)
    m, L, pad = 0.0, SR * 10, 256
    for c in range(x.shape[0]):
        for a in range(0, x.shape[1], L):
            seg = x[c, max(0, a - pad):min(x.shape[1], a + L + pad)].astype(np.float64)
            m = max(m, float(np.max(np.abs(signal.resample_poly(seg, 4, 1)))))
    return 20 * np.log10(m + 1e-12)


def voice_chain(vo):
    # cümle kazançları: fısıltı etiketli "Ama ne diyorum?" (F14) yaklaşık 12 dB sessiz geliyor (okunuş denemesi): +6 dB
    # ses kurulu tur 1: "diyorum" fısıltının içinde ayrıca +3 dB; en sessiz iki cümle (C18, L01) +2 / +1,5 dB
    gains = [(W('F14', 'ama') - .1, W('F14', 'olacak') - .05, 6.0), (W('F14', 'diyorum') - .03, We('F14', 'diyorum') + .05, 9.0),
             (CUES['C18']['s'] - .05, CUES['C18']['e'] + .05, 2.0), (CUES['L01']['s'] - .05, CUES['L01']['e'] + .05, 1.5)]
    g = np.ones(len(vo))
    for a, b, d in gains:
        g[int(a * SR):int(b * SR)] = db(d)
    g = uniform_filter1d(g, int(.04 * SR), mode='nearest')
    vo = vo * g
    vo = peq(vo, 250, -2, .9); vo = peq(vo, 3500, 1.5, .8)
    L = pyln.Meter(SR).integrated_loudness(vo)
    vo, gr = compress(vo, L + 6, 3.0)
    vo = limiter(vo[None, :], db(pyln.Meter(SR).integrated_loudness(vo) + 11))[0]
    return vo


def main():
    # bellek: 24 dk × 48 kHz stereo ≈ 550 MB/kanal (float64); ara diziler silinir, büyük diziler float32 tutulur
    stems = '--stems' in sys.argv
    meter = pyln.Meter(SR)
    vo, sr = sf.read(A('vo/vo.wav'), always_2d=False, dtype='float32')
    assert sr == SR
    vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]
    vo = hp(vo, 70)
    vo *= db(-16 - meter.integrated_loudness(vo))
    vo = voice_chain(vo)
    vo = (vo * db(-16 - meter.integrated_loudness(vo))).astype(np.float32)   # anlatım -16 LUFS
    ve = envelope(vo).astype(np.float32)
    act = np.clip((20 * np.log10(ve + 1e-9) + 42) / 10, 0, 1); del ve
    target = db(-3 * act).astype(np.float32); del act
    look = int(.12 * SR); target = np.concatenate([target[look:], np.ones(look, np.float32)])
    duck = smooth_gain(target, .1, 1.5).astype(np.float32); del target   # yavaş bırakma: cümle aralarında pompalama yok
    ir = reverb_ir(1.2)
    vo_send = np.stack([signal.oaconvolve(vo * np.float32(db(-26)), ir[c].astype(np.float32))[:N].astype(np.float32) for c in range(2)])
    mu, msr = sf.read(A('audio/music.wav'), always_2d=True, dtype='float32')
    assert msr == SR
    mu = np.ascontiguousarray(mu.T)
    mu = np.pad(mu, ((0, 0), (0, max(0, N - mu.shape[1]))))[:, :N]
    hp35 = signal.butter(4, 35, 'highpass', fs=SR, output='sos')
    for c in range(2): mu[c] = peq(signal.sosfilt(hp35, mu[c]), 60, -2.5, .7).astype(np.float32)
    mu *= np.float32(db(-21 - meter.integrated_loudness(mu.T)))
    mu *= duck; del duck
    # vuruşların tepeleri son sınırlayıcıyı çalıştırıp anlatımı bastırmasın: müzik kendi sınırlayıcısından geçer (ses kurulu tur 1)
    # sınırlayıcı yalnız konuşma sırasında sıkı (-8 dBFS); konuşmasız boşlukta doruklar serbest (-1 dBFS) (ses kurulu tur 2)
    va = (np.clip((20 * np.log10(envelope(vo) + 1e-9) + 42) / 10, 0, 1) > .3).astype(np.float32)
    va = uniform_filter1d(maximum_filter1d(va, int(.5 * SR)), int(.03 * SR))
    mu = limiter(mu, (db(-8) * va + db(-1) * (1 - va)).astype(np.float32), look=.005, rel=.15).astype(np.float32); del va
    mix = np.empty((2, N), np.float32)
    for c in range(2): mix[c] = vo + vo_send[c] + mu[c]
    if stems:
        os.makedirs(A('audio/stems'), exist_ok=True)
        sf.write(A('audio/stems/vo.wav'), (np.stack([vo, vo]) + vo_send).T, SR, subtype='FLOAT')
        sf.write(A('audio/stems/music.wav'), mu.T, SR, subtype='FLOAT')
    del vo, vo_send, mu
    mix = limiter(mix, .7).astype(np.float32)
    mix *= np.float32(db(-14 - meter.integrated_loudness(mix.T)))
    tpT = -1.0
    mix = limiter(mix, db(tpT - .6)).astype(np.float32)
    for _ in range(8):
        tp = true_peak(mix)
        if tp <= tpT: break
        mix = limiter(mix, db(tpT - .6 - (tp - tpT) - .1)).astype(np.float32)
    print(f'LUFS {meter.integrated_loudness(mix.T):.2f}  TP {true_peak(mix):.2f} dBTP  süre {N / SR:.2f}s', flush=True)
    sf.write(A('audio/mix.wav'), mix.T, SR, subtype='PCM_24')


if __name__ == '__main__':
    main()
