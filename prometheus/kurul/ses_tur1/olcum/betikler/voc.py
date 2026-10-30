import numpy as np, soundfile as sf, json, librosa
from scipy import signal
from common import *
raw, _ = sf.read(P + 'vo/vo.wav', dtype='float32'); N = len(raw)
proc = np.load('vo.npy', mmap_mode='r')
k = kfilt(raw)
fr = int(0.05 * SR)
def lev(x):  # K-ağırlıklı etkin konuşma seviyesi (50 ms kareler, en yükseğin 25 dB altına kadar)
    n = len(x) // fr
    if n < 2: return np.nan
    p = (x[:n * fr].astype(np.float64) ** 2).reshape(n, fr).mean(1)
    d = 10 * np.log10(p + 1e-20); g = d > d.max() - 25
    return -0.691 + 10 * np.log10(p[g].mean())
sos_lo = signal.butter(4, [100, 1000], 'bandpass', fs=SR, output='sos'); sos_hi = signal.butter(4, [2000, 6000], 'bandpass', fs=SR, output='sos')
sos_air = signal.butter(4, 7000, 'highpass', fs=SR, output='sos')
rows = []
for c, v in CUES.items():
    a, b = int(v['s'] * SR), int(v['e'] * SR)
    x = raw[a:b]; xk = k[a:b]
    L = lev(xk)
    lo = (signal.sosfilt(sos_lo, x) ** 2).mean(); hi = (signal.sosfilt(sos_hi, x) ** 2).mean(); air = (signal.sosfilt(sos_air, x) ** 2).mean()
    f0 = librosa.yin(x[::3].astype(np.float32), fmin=60, fmax=320, sr=SR // 3, frame_length=1024)
    rmsf = librosa.feature.rms(y=x[::3], frame_length=1024, hop_length=256)[0]
    m = min(len(f0), len(rmsf)); f0, rmsf = f0[:m], rmsf[:m]
    voiced = rmsf > rmsf.max() * 0.1
    nw = sum(1 for w in WORDS if w['id'] == c)
    Lp = lev(np.asarray(proc[a:b]))
    rows.append(dict(id=c, sec=v['sec'], s=v['s'], e=v['e'], L=round(L, 2), Lproc=round(Lp, 2), tilt=round(10 * np.log10(hi / lo), 2), air=round(10 * np.log10(air / lo), 2),
                     f0=round(float(np.median(f0[voiced])), 1), wps=round(nw / (v['e'] - v['s']), 2)))
json.dump(rows, open('voc_rows.json', 'w'), ensure_ascii=False)
# bölüm özetleri
out = {'sections': {}}
for s in range(14):
    r = [x for x in rows if x['sec'] == s]
    out['sections'][SECS[s]] = {q: round(float(np.median([x[q] for x in r])), 2) for q in ('L', 'tilt', 'air', 'f0', 'wps')}
Ls = np.array([x['L'] for x in rows]); out['L_sd'] = round(float(Ls.std()), 2); out['L_range'] = [round(float(Ls.min()), 2), round(float(Ls.max()), 2)]
Lp = np.array([x['Lproc'] for x in rows]); out['Lproc_sd'] = round(float(Lp.std()), 2); out['Lproc_range'] = [round(float(Lp.min()), 2), round(float(Lp.max()), 2)]
out['Lproc_lowest'] = sorted([(x['id'], x['Lproc']) for x in rows], key=lambda z: z[1])[:6]
out['Lproc_highest'] = sorted([(x['id'], x['Lproc']) for x in rows], key=lambda z: -z[1])[:6]
jumps = []
for p, q in zip(rows, rows[1:]):
    jumps.append(dict(a=p['id'], b=q['id'], dL=round(q['L'] - p['L'], 2), dLp=round(q['Lproc'] - p['Lproc'], 2), dtilt=round(q['tilt'] - p['tilt'], 2), df0=round(q['f0'] - p['f0'], 1), secb=p['sec'] != q['sec']))
out['jumps_big_proc'] = [j for j in jumps if abs(j['dLp']) >= 3]
out['jumps_secboundary'] = [j for j in jumps if j['secb']]
out['tilt_range'] = [min(x['tilt'] for x in rows), max(x['tilt'] for x in rows)]
# kelime düzeyi F14
def wl(x0, x1, arr):
    a, b = int(x0 * SR), int(x1 * SR); return lev(np.asarray(arr[a:b])) if b - a > 2 * fr else np.nan
f14 = [w for w in WORDS if w['id'] == 'F14'][:12]
kp = None
out['F14_words'] = [(w['w'], round(wl(w['s'], w['e'], k), 1), round(wl(w['s'], w['e'], proc), 1)) for w in f14]
# klip kenarları ve nefesler
nz = np.abs(raw) > 0
d = np.diff(nz.astype(np.int8)); st = np.where(d == 1)[0] + 1; en = np.where(d == -1)[0] + 1
if nz[0]: st = np.r_[0, st]
if nz[-1]: en = np.r_[en, N]
clips = [(a, b) for a, b in zip(st, en) if b - a > 0.2 * SR]
out['n_clips'] = len(clips)
edge = []
for a, b in clips:
    x = raw[a:b]; full = 10 * np.log10((x.astype(np.float64) ** 2).mean() + 1e-20)
    e0 = 10 * np.log10((x[int(.012 * SR):int(.032 * SR)].astype(np.float64) ** 2).mean() + 1e-20)
    e1 = 10 * np.log10((x[-int(.032 * SR):-int(.012 * SR)].astype(np.float64) ** 2).mean() + 1e-20)
    edge.append((round(a / SR, 2), round(b / SR, 2), round(e0 - full, 1), round(e1 - full, 1)))
out['edge_hot'] = [e for e in edge if e[2] > -12 or e[3] > -12]
# nefes / konuşma dışı ses: kelimeler dışındaki (klip içi) 50 ms karelerin seviyesi, cümle seviyesine göre
wint = np.zeros(N // fr, bool)
for w in WORDS: wint[int((w['s'] - .04) * SR) // fr:int((w['e'] + .04) * SR) // fr + 1] = True
n = N // fr; p = (k[:n * fr] ** 2).reshape(n, fr).mean(1); dB = -0.691 + 10 * np.log10(p + 1e-20)
inclip = np.zeros(n, bool)
for a, b in clips: inclip[a // fr:b // fr] = True
cand = np.where(inclip & ~wint[:n] & (dB > -45))[0]
ev = []
if len(cand):
    grp = np.split(cand, np.where(np.diff(cand) > 1)[0] + 1)
    for g in grp:
        t = g[0] * fr / SR; ev.append((round(t, 2), round(len(g) * 0.05, 2), round(float(dB[g].max()), 1)))
out['nonword_events_gt-45LUFS'] = len(ev); out['nonword_top'] = sorted(ev, key=lambda z: -z[2])[:15]
# klik: 5 ms HF enerjisi, çevresine göre
hp = signal.sosfilt(signal.butter(4, 5000, 'highpass', fs=SR, output='sos'), raw)
f5 = int(.005 * SR); m5 = len(hp) // f5; e5 = (hp[:m5 * f5].astype(np.float64) ** 2).reshape(m5, f5).mean(1) + 1e-20
from scipy.ndimage import median_filter
loc = median_filter(e5, 41)
r = 10 * np.log10(e5 / loc); bbe = 10 * np.log10((raw[:m5 * f5].astype(np.float64) ** 2).reshape(m5, f5).mean(1) + 1e-20)
cl = np.where((r > 18) & (e5 > 1e-7))[0]
out['click_candidates'] = [(round(i * f5 / SR, 3), round(float(r[i]), 1), round(float(10 * np.log10(e5[i])), 1)) for i in cl[np.argsort(-r[cl])][:12]]
json.dump(out, open('voc.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
