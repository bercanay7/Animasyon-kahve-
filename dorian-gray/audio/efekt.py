#!/usr/bin/env python3
"""DORIAN GRAY: efektler, yalnız numpy ile sentez (örnek ses ve ücretli üretim yok). Yardımcılar mary-stuart/audio/efekt.py'den (kendi kodumuz).
Oda sessizliği ve saat, bahçe kuşları, palet bıçağı, tiyatro uğultusu ve seyrek alkış, merdiven adımları, örtü, kapı, anahtar, sokakta nal ve rüzgâr,
gaz lambası, şömine, perde yırtılması, boğuk düşüş (kan ve bıçak sesi yok), mahkeme uğultusu, sayfa. G09'daki çığlık duyulmaz: sessizlik taşır.
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
rng = np.random.default_rng(1891)
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


def kus(t0, t1, g=1.0):
    t = t0
    while t < t1:
        for k in range(int(rng.integers(2, 5))):
            d = rng.uniform(.06, .14); n = int(d * SR); tt = np.arange(n) / SR; f0 = rng.uniform(2600, 4200)
            f = f0 * (1 + .25 * np.sin(np.pi * tt / d) * rng.choice([-1, 1])); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) ** 2
            put(s.astype(np.float32), t + k * .16, rng.uniform(-.6, .6), .05 * g)
        t += rng.uniform(1.2, 3.0)
def saat(t0, t1, g=1.0):
    t = t0; k = 0
    while t < t1:
        n = int(.05 * SR); tt = np.arange(n) / SR; s = bp(rng.standard_normal(n).astype(np.float32), 2200 if k % 2 else 1700, 5) * np.exp(-tt / .006) * 2
        put(s, t, .35, .1 * g); t += 1.0; k += 1
def adim(t0, t1, hiz=.55, g=1.0, pan=0.0, merdiven=False):
    t = t0; k = 0
    while t < t1:
        n = int(.18 * SR); tt = np.arange(n) / SR; s = lp(rng.standard_normal(n).astype(np.float32), 400 if merdiven else 700) * 3 * np.exp(-tt / .03) + np.sin(2 * np.pi * (70 if merdiven else 110) * tt) * np.exp(-tt / .04) * .6
        put(s, t, pan + rng.uniform(-.05, .05), .22 * g * rng.uniform(.8, 1)); t += hiz * rng.uniform(.92, 1.08); k += 1
def kumas(t, d=1.0, g=1.0):
    n = int(d * SR); tt = np.arange(n) / SR; x = rng.standard_normal(n).astype(np.float32)
    s = bp(x, 2400, .8) * np.sin(np.pi * tt / d) ** 1.5 * (.6 + .4 * np.sin(2 * np.pi * 7 * tt))
    put(s, t, .1, .18 * g)
def kaziyici(t, d=.7, g=1.0):
    n = int(d * SR); tt = np.arange(n) / SR; x = rng.standard_normal(n).astype(np.float32)
    s = bp(x, 5200, 6) * np.sin(np.pi * tt / d) + .15 * np.sin(2 * np.pi * 3100 * tt) * np.sin(np.pi * tt / d)
    put(s.astype(np.float32), t, .2, .14 * g)
def ugultu(t0, t1, g=1.0, f0=500):
    n = int((t1 - t0) * SR); t = np.arange(n) / SR; x = rng.standard_normal(n).astype(np.float32)
    w = bp(x, f0, .9) * (.7 + .3 * np.sin(2 * np.pi * .23 * t)) * 2
    put(w * zarf(n, 1.2, 1.5), t0, -.2, .07 * g); put(np.roll(w, 13000) * zarf(n, 1.2, 1.5), t0, .2, .07 * g)
def alkis(t0, d=2.5, kac=6, g=1.0):
    for i in range(kac):
        t = t0 + rng.uniform(0, .4); hz_ = rng.uniform(2.0, 2.8)
        while t < t0 + d * rng.uniform(.5, 1):
            n = int(.05 * SR); tt = np.arange(n) / SR; s = bp(rng.standard_normal(n).astype(np.float32), rng.uniform(1200, 2200), 1.5) * np.exp(-tt / .008) * 2
            put(s, t, rng.uniform(-.7, .7), .1 * g); t += 1 / hz_
def gaz(t0, t1, g=1.0):
    n = int((t1 - t0) * SR); x = rng.standard_normal(n).astype(np.float32); put(hp(x, 4000) * zarf(n, .8, .8), t0, .3, .025 * g)
def dusus(t, g=1.0):
    n = int(1.6 * SR); tt = np.arange(n) / SR; s = lp(rng.standard_normal(n).astype(np.float32), 140) * 6 * np.exp(-tt / .18) + np.sin(2 * np.pi * 48 * tt) * np.exp(-tt / .25)
    put(s, t, 0, .4 * g)
def sayfa(t):
    n = int(.45 * SR); tt = np.arange(n) / SR; s = hp(rng.standard_normal(n).astype(np.float32), 1800) * np.sin(np.pi * tt / .45) ** 2 * (1 + np.sin(2 * np.pi * 9 * tt))
    put(s, t, .15, .12)
def lamba_koy(t):
    n = int(.3 * SR); tt = np.arange(n) / SR; s = bp(rng.standard_normal(n).astype(np.float32), 900, 3) * np.exp(-tt / .02) * 2 + np.sin(2 * np.pi * 1900 * tt) * np.exp(-tt / .05) * .2
    put(s.astype(np.float32), t, .1, .25)

# ── olaylar ──
kumas(W('A03', 'örtünün'), 1.2, .8)
kus(S('B01'), E('B02'), .6); kus(S('B04'), E('B04'), 1.0)
kaziyici(W('B08', 'palet'), .9)
ugultu(S('C01') + .5, E('C03'), .9); alkis(E('C02') - .4, 2.0, 7, .8); alkis(E('C03') - .5, 1.6, 3, .6)   # ikinci gece: seyrek
kapi(W('C05', 'sahne') + .2)
adim(S('C06'), W('C06', 'durur'), hiz=.6, g=.8, pan=-.2)
saat(S('C07'), E('C09') + 1.5, .7)
kapi(W('C10', 'haberle') - .4)
adim(S('C13') + 1, W('C13', 'odasına') + 1, hiz=.5, g=.8, merdiven=True); kumas(W('C13', 'örtü') - .3, 1.4, 1.0); kapi(W('C13', 'kapıyı')); anahtar(W('C13', 'kilitler'))
ugultu(S('D02'), E('D02'), .7, 420); nal(S('D02'), E('D02'), bpm=60, g=.35, yuru=True, pan=.3)
anahtar(S('D03') + .3); saat(W('D03', 'aynayla'), E('D05'), .6)
ruzgar(S('E01') - .5, E('E03'), .7); nal(S('E01'), E('E01') + 1, bpm=56, g=.35, yuru=True, pan=-.4); gaz(S('E01'), E('E02'), 1.0)
adim(S('E04'), W('E04', 'lambayı'), hiz=.48, g=.9, merdiven=True); anahtar(W('E04', 'kilitli') + .2); lamba_koy(W('E04', 'masaya'))
yirtik(W('E05', 'koparıp'), 1.0); kumas(W('E05', 'fırlatır'), .8, 1.2)
saat(S('E06'), W('E09', 'öldürür'), .5)
dusus(W('E09', 'öldürür') + .1, 1.0)
saat(S('E10') + .5, E('E10') + 1, .6)
somine(S('F01'), E('F04') + .5, .8); somine(S('F05'), E('F05') + 1, .5)
saat(S('G01'), E('G02'), .5)
adim(W('G03', 'lambayı'), E('G03') + .4, hiz=.48, g=.8, merdiven=True); kumas(W('G04', 'perdeyi'), 1.0, 1.0)
yirtik(W('G08', 'saplar'), .6); dusus(W('G08', 'saplar') + .5, .8)
kapi(S('G10') - .1); adim(S('G10') + .4, W('G10', 'portresini'), hiz=.45, g=.7, pan=.2)
ugultu(S('G12'), E('G12') + .5, .8, 380); sayfa(W('G12', 'sayfalar')); sayfa(S('G13') + .3)

# ── kısma, çıkış ──
pk = max(np.abs(L).max(), np.abs(R).max()); L /= pk / .7; R /= pk / .7
endf = np.ones(N, np.float32); g0 = int((DUR - 5) * SR); endf[g0:] = np.linspace(1, 0, N - g0); L *= endf; R *= endf
st = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'sfx.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print('audio/sfx.wav', round(DUR, 2), 'sn')
