import json, re, numpy as np
from scipy import signal
import pyloudnorm as pyln
SR = 48000
P = '/home/user/Animasyon-kahve-/prometheus/'
TL = open(P + 'timeline.js').read()
DUR = float(re.search(r'window\.DUR\s*=\s*([\d.]+)', TL).group(1))
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', TL).group(1))
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', TL, re.S).group(1))
ORDER = list(CUES.keys())
SECS = ["Zincirdeki Titan","Erhat'ın sorusu","Taht kavgası","Dinmez öfke","Mekone","Duruşma","Savunma","Tanıklar","Sır","Zincirin öbür ucu","Kartal/fırtına","Herakles→Oppenheimer","Başkaldıran yaratık","Çevirmenler"]
def kfilt(x):
    m = pyln.Meter(SR)
    y = x.astype(np.float64)
    for f in m._filters.values():
        y = signal.lfilter(f.b, f.a, y, axis=-1)
    return y
def block_ms(xk, blk=0.1):
    """kanal toplamlı K-ağırlıklı ortalama kare, blk sn bloklarla. xk: (C, N) veya (N,)"""
    if xk.ndim == 1: xk = xk[None]
    h = int(blk * SR); n = xk.shape[1] // h
    return (xk[:, :n * h] ** 2).reshape(xk.shape[0], n, h).mean(2).sum(0)
def win_lufs(ms, k):
    c = np.concatenate([[0], np.cumsum(ms)])
    w = (c[k:] - c[:-k]) / k
    return -0.691 + 10 * np.log10(w + 1e-20)
def integrated(ms100):
    L = win_lufs(ms100, 4)
    p = 10 ** ((L[::1] + 0.691) / 10)
    g = L > -70
    rel = -0.691 + 10 * np.log10(p[g].mean()) - 10
    g2 = L > rel
    return -0.691 + 10 * np.log10(p[g2].mean())
def lra(ms100):
    S = win_lufs(ms100, 30)[::1]
    S = S[S > -70]
    rel = -0.691 + 10 * np.log10((10 ** ((S + 0.691) / 10)).mean()) - 20
    S = S[S > rel]
    return np.percentile(S, 95) - np.percentile(S, 10), np.percentile(S, 10), np.percentile(S, 95)
def W(i, w, n=0, end=False):
    k = 0
    for x in WORDS:
        if x['id'] == i and x['w'].startswith(w):
            if k == n: return x['e'] if end else x['s']
            k += 1
    raise KeyError((i, w, n))
def fmt(t): return f"{int(t//60)}:{t%60:05.2f}"
