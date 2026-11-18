#!/usr/bin/env python3
"""MARY STUART: efektler, yalnız numpy ile sentez (örnek ses ve ücretli üretim yok). Her olay sahnedeki eyleme bağlı (timeline.js).
Projektör: çok alçak, sürekli (sessiz film kimliği). Deniz, rüzgâr, nal, patlama, tüy kalem, mühür, kapı, anahtar, mum, baykuş, şömine, sikke, zincir, yırtılan kâğıt.
    python3 audio/efekt.py  -> audio/sfx.wav (48 kHz stereo)
"""
import json, re, wave
from pathlib import Path
import numpy as np

SR = 48000
HERE = Path(__file__).resolve().parent; FILM = HERE.parent
TL = (FILM / 'timeline.js').read_text(encoding='utf-8')
CUES = json.loads(TL.split('window.CUES = ')[1].split(';\n')[0])
WORDS = json.loads(TL.split('window.WORDS = ')[1].split(';\n')[0])
DUR = float(re.search(r'window\.DUR = ([\d.]+)', TL).group(1))
N = int(DUR * SR)
L = np.zeros(N, np.float32); R = np.zeros(N, np.float32)
rng = np.random.default_rng(1587)
def S(i): return CUES[i]['s']
def E(i): return CUES[i]['e']
def W(i, w, n=0):
    k = 0
    for x in WORDS:
        if x['id'] == i and x['w'].startswith(w):
            if k == n: return x['s']
            k += 1
    print('kelime yok', i, w); return S(i)
def put(sig, t, pan=0.0, g=1.0):
    a = int(t * SR); b = min(N, a + len(sig))
    if a >= N or b <= 0 or a < 0: return
    s = (sig[:b - a] * g).astype(np.float32)
    L[a:b] += s * np.float32(np.sqrt(.5 * (1 - pan))); R[a:b] += s * np.float32(np.sqrt(.5 * (1 + pan)))
def lp(x, fc):   # tek kutuplu alçak geçiren, FFT ile (uzun sinyallerde hızlı)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); return np.fft.irfft(X / (1 + (f / fc) ** 2), len(x)).astype(np.float32)
def hp(x, fc): return x - lp(x, fc)
def bp(x, f0, q=2.0):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR) + 1e-6; return np.fft.irfft(X / (1 + q * q * (f / f0 - f0 / f) ** 2), len(x)).astype(np.float32)
def zarf(n, a, r):
    e = np.ones(n, np.float32); a = max(1, int(a * SR)); r = max(1, int(r * SR)); e[:a] = np.linspace(0, 1, a); e[-r:] *= np.linspace(1, 0, r); return e

def deniz(t0, t1, g=1.0):
    n = int((t1 - t0) * SR); t = np.arange(n) / SR; x = rng.standard_normal(n).astype(np.float32)
    w = lp(x, 500) * 3 * (.55 + .45 * np.sin(2 * np.pi * t / 6.5) ** 2) + hp(lp(x, 3000), 900) * .6 * (.3 + .7 * np.sin(2 * np.pi * t / 6.5 + .8) ** 4)
    put(w * zarf(n, 2, 2.5), t0, -.3, .16 * g); put(np.roll(w, 7000) * zarf(n, 2, 2.5), t0, .3, .16 * g)
def ruzgar(t0, t1, g=1.0):
    n = int((t1 - t0) * SR); t = np.arange(n) / SR; x = rng.standard_normal(n).astype(np.float32)
    w = bp(x, 420, 1.5) * 2.5 * (.6 + .4 * np.sin(2 * np.pi * .11 * t) + .2 * np.sin(2 * np.pi * .37 * t))
    put(w * zarf(n, 1.5, 2), t0, -.4, .12 * g); put(np.roll(w, 9000) * zarf(n, 1.5, 2), t0, .4, .12 * g)
def nal(t0, t1, bpm=150, g=1.0, pan=0.0, yuru=False):
    b = 60 / bpm; t = t0; k = 0
    tik = lambda: (bp(rng.standard_normal(int(.06 * SR)).astype(np.float32), 900, 3) * np.exp(-np.arange(int(.06 * SR)) / 250)).astype(np.float32)
    while t < t1:
        offs = (0, .5) if yuru else (0, .12, .24, .33)
        for o in offs: put(tik(), t + o * b, pan + rng.uniform(-.1, .1), .5 * g * rng.uniform(.7, 1))
        t += b; k += 1
def patlama(t):
    n = int(4 * SR); tt = np.arange(n) / SR; x = rng.standard_normal(n).astype(np.float32)
    s = lp(x, 160) * 6 * np.exp(-tt / .9) + hp(x, 1500) * np.exp(-tt / .08) * .6 + np.sin(2 * np.pi * 38 * tt) * np.exp(-tt / .6) * .8
    put(s, t, 0, .55)
def kalem(t0, t1, g=1.0):
    n = int((t1 - t0) * SR); t = np.arange(n) / SR; x = rng.standard_normal(n).astype(np.float32)
    s = bp(x, 3800, 2) * (np.abs(np.sin(2 * np.pi * 2.3 * t + np.sin(2 * np.pi * .7 * t))) ** 3)
    put(s * zarf(n, .2, .3), t0, .2, .1 * g)
def muhur(t):
    n = int(.5 * SR); tt = np.arange(n) / SR; s = lp(rng.standard_normal(n).astype(np.float32), 300) * 3 * np.exp(-tt / .05) + np.sin(2 * np.pi * 90 * tt) * np.exp(-tt / .08)
    put(s, t, 0, .3)
def kapi(t):
    n = int(2.5 * SR); tt = np.arange(n) / SR; s = lp(rng.standard_normal(n).astype(np.float32), 120) * 5 * np.exp(-tt / .35) + np.sin(2 * np.pi * 55 * tt) * np.exp(-tt / .5)
    put(s, t, -.1, .45)
def anahtar(t):
    for k, o in enumerate((0, .18, .3)):
        n = int(.15 * SR); tt = np.arange(n) / SR; s = bp(rng.standard_normal(n).astype(np.float32), 2500 + 600 * k, 4) * np.exp(-tt / .02) * 2
        put(s, t + o, .2, .35)
def mum(t):
    n = int(.6 * SR); tt = np.arange(n) / SR; s = lp(rng.standard_normal(n).astype(np.float32), 700) * np.exp(-((tt - .12) / .08) ** 2) * 2
    put(s, t, .1, .25)
def baykus(t):
    for k, (o, d) in enumerate(((0, .35), (.6, .9))):
        n = int(d * SR); tt = np.arange(n) / SR; f = 380 * (1 - .04 * tt / d); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) ** 1.5
        put(s.astype(np.float32), t + o, .45, .14)
def somine(t0, t1, g=1.0):
    n = int((t1 - t0) * SR); x = np.zeros(n, np.float32); k = rng.poisson(10 * (t1 - t0))
    for p in rng.integers(0, max(1, n - 2000), k): m = int(rng.integers(200, 1400)); x[p:p + m] += rng.standard_normal(m).astype(np.float32) * np.exp(-np.arange(m) / (m / 5)) * rng.uniform(.2, 1)
    s = hp(x, 1200) * .5 + lp(rng.standard_normal(n).astype(np.float32), 160) * 1.2
    put(s * zarf(n, 1, 1.5), t0, -.3, .12 * g)
def sikke(t0, k=10):
    for i in range(k):
        n = int(.4 * SR); tt = np.arange(n) / SR; f = rng.uniform(3200, 4800); s = (np.sin(2 * np.pi * f * tt) + .5 * np.sin(2 * np.pi * f * 1.48 * tt)) * np.exp(-tt / .06)
        put(s.astype(np.float32), t0 + i * .1 + rng.uniform(0, .05), rng.uniform(-.2, .2), .08)
def zincir(t0, t1):
    t = t0
    while t < t1:
        n = int(.12 * SR); tt = np.arange(n) / SR; s = bp(rng.standard_normal(n).astype(np.float32), rng.uniform(1800, 3200), 3) * np.exp(-tt / .03) * 2
        put(s, t, rng.uniform(-.2, .2), .22); t += rng.uniform(.08, .25)
def yirtik(t, d=1.2):
    n = int(d * SR); tt = np.arange(n) / SR; x = rng.standard_normal(n).astype(np.float32); s = hp(x, 1500) * (np.abs(np.sin(2 * np.pi * 23 * tt)) ** 2) * np.sin(np.pi * tt / d)
    put(s, t, 0, .2)

# ── projektör: alçak dişli uğultusu + 24 Hz tıkırtı (sessiz film); çok düşük ──
n = N; t = np.arange(n, dtype=np.float32) / SR
uğ = lp(rng.standard_normal(n).astype(np.float32), 180) * .8 + .3 * np.sin(2 * np.pi * 48 * t)
tik = (np.mod(t * 24, 1) < .004).astype(np.float32) * rng.uniform(.5, 1, n).astype(np.float32)
proj = (uğ + hp(tik, 2000) * 1.5) * .025
L += proj; R += proj

# ── olaylar ──
deniz(S('A03') - .5, S('A05'), 1.0)
ruzgar(S('B02'), W('B02', 'kral'), .9); mum(W('B03', 'ölür'))
deniz(S('B10'), S('C01') - 1, .9); deniz(S('C01') - 1, S('C02'), .7)
nal(S('C03'), S('C04'), bpm=70, g=.5, yuru=True); ruzgar(S('C03'), S('C04'), .6)
nal(S('D03'), W('D03', 'yaz'), g=.6)
nal(W('E07', 'iki'), S('E08'), g=.7); ruzgar(S('E07'), S('E08'), .5)
patlama(W('F02', 'havaya')); ruzgar(S('F03'), S('F04'), .5)
kalem(S('F05') + .3, S('F06') - .3, .9)
nal(S('F11'), S('F12'), g=.5, pan=.3); deniz(S('F11'), S('F12'), .6); kapi(W('F12', 'zorla'))
ruzgar(S('G01'), S('G02'), .6); deniz(S('G03'), S('G04'), .4); mum(W('G04', 'düşürdü'))
ruzgar(S('G07'), S('G08'), .7); anahtar(W('G08', 'kilitledi'))
ruzgar(S('G10'), S('H01'), .6)
nal(S('H01') - .3, S('H03') - .3, g=.8); ruzgar(S('H01'), S('H03'), .8)
somine(S('H03') + 2, S('H04'), .6); baykus(W('H03', 'baykuşlar'))
deniz(S('H05'), S('H08'), .9); deniz(S('H12'), S('H14'), 1.1)
kalem(W('H13', 'ertesi'), S('H14'), 1.0); muhur(S('H08') + 1); kalem(W('H15', 'sadık'), W('H15', 'meri') + .5, 1.0); muhur(W('H15', 'meri') + .4)
yirtik(W('I07', 'reddetti')); nal(W('I14', 'kuzeyin'), W('I14', 'italyan') - .5, g=.5)
zincir(W('I14', 'zincir'), E('I14')); sikke(W('I15', 'yıllık'))
nal(S('J03'), S('J04'), bpm=60, g=.4, yuru=True); kalem(S('J04'), S('J05'), .8)
kalem(W('J05', 'kopyalanıyor'), W('J05', 'yoluna'), .7); muhur(W('J05', 'yoluna') + .3); muhur(W('J07', 'cevap'))
kalem(W('J10', 'darağacı') - .3, W('J10', 'darağacı') + 1.4, 1.0)
nal(S('J11'), S('J12'), bpm=90, g=.4, yuru=True)
kalem(W('K05', 'imzaladı') - .2, W('K05', 'imzaladı') + 1.5, 1.2); mum(W('K08', 'sessizce'))
nal(S('K10'), W('K10', 'elizabethin'), g=.7)
kalem(S('L02'), S('L03') + 6, .7); somine(S('L07'), S('L11') + .5, .8)
mum(W('M03', 'öldü'))
deniz(S('L06'), S('L07'), .6); deniz(S('M12') - .5, DUR, .7)

# ── kısma (anlatım altında az), çıkış ──
pk = max(np.abs(L).max(), np.abs(R).max()); L /= pk / .7; R /= pk / .7
endf = np.ones(N, np.float32); g0 = int((DUR - 5) * SR); endf[g0:] = np.linspace(1, 0, N - g0); L *= endf; R *= endf
st = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'sfx.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print('audio/sfx.wav', round(DUR, 2), 'sn')
