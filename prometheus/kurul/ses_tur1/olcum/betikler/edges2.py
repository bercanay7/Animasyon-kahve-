import numpy as np, soundfile as sf, json, subprocess
from scipy import signal
from common import *
raw, _ = sf.read(P + 'vo/vo.wav', dtype='float32')
sel = json.load(open(P + 'vo/secim.json')); secn = list(sel.keys())
def load(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(r, np.float32).copy()
cache = {}
def env(x, w=int(.005 * SR)):
    n = len(x) // w; return 10 * np.log10((x[:n * w].astype(np.float64) ** 2).reshape(n, w).mean(1) + 1e-20)
checks = [('A04', 'end', 25.40), ('B05', 'end', 74.55), ('C14', 'end', 204.58), ('G06', 'end', 730.56), ('H05', 'end', 889.08), ('L03', 'end', 1247.44),
          ('A06', 'start', 27.0), ('C12', 'start', 178.91), ('F09', 'start', 575.04), ('G07', 'start', 731.07), ('H05b', 'start', 889.58), ('L04', 'start', 1247.95)]
for cue, kind, t in checks:
    sec = CUES[cue]['sec']; f = sel[secn[sec]]
    if f not in cache: cache[f] = load(P + 'vo/' + f)
    a = cache[f]
    i = int(t * SR)
    # klibin kenarından 0,4 sn'lik iç parça ile çekimde yer bul
    seg = raw[i - int(.45 * SR):i - int(.05 * SR)] if kind == 'end' else raw[i + int(.05 * SR):i + int(.45 * SR)]
    c = signal.fftconvolve(a, seg[::-1], 'valid'); j = int(np.argmax(np.abs(c)))
    edge = j + len(seg) + int(.05 * SR) if kind == 'end' else j - int(.05 * SR)
    # çekimde kesimden sonra/önce 150 ms'nin seviyesi (konuşma seviyesine göre)
    ref = np.percentile(env(a[max(0, edge - SR):edge + SR]), 90)
    if kind == 'end': lost = env(a[edge:edge + int(.15 * SR)]); kept = env(a[edge - int(.05 * SR):edge])
    else: lost = env(a[edge - int(.15 * SR):edge]); kept = env(a[edge:edge + int(.05 * SR)])
    print(f"{cue:5s} {kind:5s} t={t:8.2f} take={f} | kesimin dışında kalan 150 ms: maks {lost.max() - ref:6.1f} dB, ort {10*np.log10(np.mean(10**(lost/10))) - ref:6.1f} dB | kalan 50 ms {kept.max() - ref:6.1f} dB (ref P90)")
print('---- kesimden sessizliğe (−30 dB re P90) kadar süre, çekimde')
for cue, kind, t in checks:
    sec = CUES[cue]['sec']; f = sel[secn[sec]]; a = cache[f]; i = int(t * SR)
    seg = raw[i - int(.45 * SR):i - int(.05 * SR)] if kind == 'end' else raw[i + int(.05 * SR):i + int(.45 * SR)]
    c = signal.fftconvolve(a, seg[::-1], 'valid'); j = int(np.argmax(np.abs(c)))
    edge = j + len(seg) + int(.05 * SR) if kind == 'end' else j - int(.05 * SR)
    e = env(a[max(0, edge - SR):edge + SR]); ref = np.percentile(e, 90); mid = min(edge, SR) // int(.005 * SR)
    if kind == 'end':
        k = mid
        while k < len(e) and e[k] - ref > -30: k += 1
        gapk = k
        while gapk < len(e) and e[gapk] - ref <= -30: gapk += 1
        print(f"{cue:5s} end   kesimden sonra konuşma {5*(k-mid):4d} ms sürüyor; ardından {5*(gapk-k):4d} ms sessizlik")
    else:
        k = mid
        while k > 0 and e[k - 1] - ref > -30: k -= 1
        gk = k
        while gk > 0 and e[gk - 1] - ref <= -30: gk -= 1
        print(f"{cue:5s} start kesimden önce {5*(mid-k):4d} ms konuşma (aynı kelimenin başı ya da önceki cümle); onun önünde {5*(k-gk):4d} ms sessizlik")
