import numpy as np, soundfile as sf, json, subprocess, librosa
from scipy import signal
from common import *
raw, _ = sf.read(P + 'vo/vo.wav', dtype='float32'); N = len(raw)
sel = json.load(open(P + 'vo/secim.json')); secn = list(sel.keys())
def load(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(r, np.float32).copy()
cache = {}
def env(x, w=int(.005 * SR)):
    n = len(x) // w; return 10 * np.log10((x[:n * w].astype(np.float64) ** 2).reshape(n, w).mean(1) + 1e-20)
def edge_end(t):   # cümle sonundan sonraki ilk ≥0,15 sn sıfır koşusunun başı
    i = int((t - 0.3) * SR)
    while True:
        while raw[i] != 0: i += 1
        j = i
        while j < N and raw[j] == 0: j += 1
        if j - i >= 0.15 * SR: return i
        i = j
def edge_start(t):  # cümle başından önceki son ≥0,15 sn sıfır koşusunun sonu
    i = int((t + 0.3) * SR)
    while True:
        while raw[i - 1] != 0: i -= 1
        j = i
        while j > 0 and raw[j - 1] == 0: j -= 1
        if i - j >= 0.15 * SR: return i
        i = j
k = None
out = []
for cue, kind in [('A04', 'end'), ('A06', 'start'), ('B05', 'end'), ('C14', 'end'), ('C17', 'start'), ('F07', 'end'), ('F09', 'start'), ('G06', 'end'), ('G07', 'start'), ('H05', 'end'), ('H05b', 'start'), ('L03', 'end'), ('L04', 'start'), ('C12', 'start')]:
    v = CUES[cue]
    e = edge_end(v['e']) if kind == 'end' else edge_start(v['s'])
    f = sel[secn[v['sec']]]
    if f not in cache: cache[f] = load(P + 'vo/' + f)
    a = cache[f]
    seg = raw[e - int(.45 * SR):e - int(.05 * SR)] if kind == 'end' else raw[e + int(.05 * SR):e + int(.45 * SR)]
    c = signal.fftconvolve(a, seg[::-1], 'valid'); j = int(np.argmax(np.abs(c)))
    te = j + len(seg) + int(.05 * SR) if kind == 'end' else j - int(.05 * SR)
    ee = env(a[max(0, te - SR):te + SR]); ref = np.percentile(ee, 90); mid = min(te, SR) // int(.005 * SR)
    if kind == 'end':
        q = mid
        while q < len(ee) and ee[q] - ref > -30: q += 1
        beyond = 5 * (q - mid)
        last = raw[e - int(.042 * SR):e - int(.012 * SR)]
    else:
        q = mid
        while q > 0 and ee[q - 1] - ref > -30: q -= 1
        beyond = 5 * (mid - q)
        last = raw[e + int(.012 * SR):e + int(.042 * SR)]
    sp = raw[int(v['s'] * SR):int(v['e'] * SR)]
    lv = 10 * np.log10((last.astype(np.float64) ** 2).mean() + 1e-20) - 10 * np.log10(np.percentile(sp.astype(np.float64) ** 2, 95) + 1e-20)
    out.append(dict(cue=cue, kind=kind, edge=round(e / SR, 3), cue_time=v['e'] if kind == 'end' else v['s'], speech_beyond_cut_ms=beyond, edge_level_dB_re_P95=round(float(lv), 1)))
    print(out[-1])
json.dump(out, open('edges3.json', 'w'), ensure_ascii=False, indent=1)
