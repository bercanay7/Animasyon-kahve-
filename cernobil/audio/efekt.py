#!/usr/bin/env python3
"""ÇERNOBİL'İN ÇAYI: efektler (numpy sentezi; örnek ses yok). python3 audio/efekt.py → audio/efekt.wav (48 kHz stereo)
Zamanlar timeline.js ve vo/shots.json'dan (node tools/plan_listesi.js). Radyasyonun sesi yok (Geiger tıkırtısı kullanılmaz)."""
import json, re, wave
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; FILM = HERE.parent; SR = 48000
rng = np.random.default_rng(11)
TL = (FILM / 'timeline.js').read_text(encoding='utf-8')
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', TL, re.S).group(1))
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', TL, re.S).group(1))
DUR = float(re.search(r'window\.DUR\s*=\s*([\d.]+)', TL).group(1))
SHOTS = json.loads((FILM / 'vo' / 'shots.json').read_text())
N = int(DUR * SR) + SR; L = np.zeros(N); R = np.zeros(N)
S = lambda i: CUES[i]['s']; Ee = lambda i: CUES[i]['e']
def W(i, w, n=0):
    k = 0
    for x in WORDS:
        if x['id'] == i and x['w'].startswith(w):
            if k == n: return x['s']
            k += 1
    return S(i)
def put(t, x, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(x), N - i)
    if n <= 0 or i < 0: return
    L[i:i + n] += x[:n] * g * np.sqrt(.5 * (1 - pan)); R[i:i + n] += x[:n] * g * np.sqrt(.5 * (1 + pan))
def lp(x, fc):   # FFT ile yumuşak alçak geçiren (scipy yok)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 / (1 + (f / fc) ** 2); return np.fft.irfft(X, len(x))
def hp(x, fc): X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= (f / fc) ** 2 / (1 + (f / fc) ** 2); return np.fft.irfft(X, len(x))
def gurultu(d, fc=2000): x = lp(rng.normal(0, 1, int(d * SR)), fc); return x / (np.abs(x).max() + 1e-9)
def zarf(n, at=.01, rl=.2):
    t = np.arange(n) / SR; d = n / SR; return np.minimum(1, t / at) * np.minimum(1, np.maximum(0, (d - t) / rl))
def gum(d=.5, f=55):
    t = np.arange(int(d * SR)) / SR; return np.sin(2 * np.pi * f * (1 + 1.2 * np.exp(-t * 25)) * t) * np.exp(-t * 9)
def yagmur(d): x = hp(rng.normal(0, 1, int(d * SR)), 1500); x = lp(x, 6000); x /= np.abs(x).max(); return x * .5 * zarf(len(x), 1.5, 1.5)
def gok(d=4): y = gurultu(d, 120) * 1.0; t = np.arange(len(y)) / SR; return y * (np.exp(-t * 1.1) * (1 + .6 * np.sin(t * 9))) * zarf(len(y), .03, 1.5)
def catirti(d, yog=10):
    y = gurultu(d, 900) * .25; n = len(y)
    for _ in range(int(d * yog)):
        i = rng.integers(0, max(1, n - 800)); k = rng.normal(0, 1, 600) * np.exp(-np.arange(600) / 70); y[i:i + 600] += k * .5
    return y * zarf(n, .8, .8)
def ruzgar(d): y = gurultu(d, 500); t = np.arange(len(y)) / SR; return y * (.55 + .45 * np.sin(2 * np.pi * .09 * t + 1)) * zarf(len(y), 2, 2)
def dalga(d): y = gurultu(d, 900); t = np.arange(len(y)) / SR; return y * (.4 + .6 * np.sin(2 * np.pi * .12 * t) ** 2) * zarf(len(y), 1.5, 1.5)
def mix(*xs):
    n = max(len(x) for x in xs); y = np.zeros(n)
    for x in xs: y[:len(x)] += x
    return y
def adim(sert=1.0): return mix(gum(.12, 90) * .6, gurultu(.08, 1500) * zarf(int(.08 * SR), .002, .05) * .3) * sert
def kos(t0, t1, ara=.3, g=.5, pan=0):
    t = t0
    while t < t1: put(t, adim(), g, pan); t += ara
def kapi(): x = gum(.4, 70); y = gurultu(.25, 2500) * zarf(int(.25 * SR), .002, .2) * .5; z = np.zeros(int(.45 * SR)); z[:len(x)] += x; z[:len(y)] += y; return z
def tik(): x = gurultu(.03, 5000) * zarf(int(.03 * SR), .001, .02); return x
def _slayt():   # fener slaytının değişimi: mandal tıkı + camın sürtünmesi
    a = tik() * .8; b = gurultu(.35, 1200) * zarf(int(.35 * SR), .04, .2) * .35; c = tik() * .6
    y = np.zeros(int(.5 * SR)); y[:len(a)] += a; y[int(.06 * SR):int(.06 * SR) + len(b)] += b; y[int(.42 * SR):int(.42 * SR) + len(c)] += c; return y
def kus(f=4000, d=.09): t = np.arange(int(d * SR)) / SR; return np.sin(2 * np.pi * (f + 1500 * np.sin(t * 70)) * t) * np.exp(-t * 28)
def kanat(d=.6): y = gurultu(d, 700); t = np.arange(len(y)) / SR; return y * (np.sin(2 * np.pi * 14 * t) > 0) * zarf(len(y), .02, .3) * .5
def balta(): return mix(gum(.18, 120) * .7, gurultu(.06, 3000) * zarf(int(.06 * SR), .001, .05) * .6)
def tuk(): return mix(gum(.15, 160) * .6, tik() * .4)
def silah(): return mix(gurultu(.9, 2500) * zarf(int(.9 * SR), .001, .8), gum(.6, 50) * .9)
def sicrama(): y = gurultu(1.2, 2500) * zarf(int(1.2 * SR), .01, 1.0); return y
def puf(): y = gurultu(.3, 900) * zarf(int(.3 * SR), .02, .25) * .5; return y
def ortam(a, b, f, g, pan=0):
    if b > a: put(a, f(b - a), g, pan)


PL = {s['id']: s for s in SHOTS}
P = lambda i, k=0.0: PL[i]['at'] + k
PE = lambda i: PL[i]['end']
def flas(): return mix(tik() * .9, gurultu(.18, 3500) * zarf(int(.18 * SR), .001, .15) * .5, gum(.08, 400) * .2)   # deklanşör + flaş patlaması
def tus(): return mix(tik() * .7, gum(.05, 900) * .25)
def daktilo(t0, t1, hiz=9, g=.25, pan=0):
    t = t0; r = np.random.default_rng(int(t0 * 10))
    while t < t1: put(t, tus(), g * (.7 + .3 * r.random()), pan); t += (1 / hiz) * (.6 + .8 * r.random())
    put(t1, mix(gum(.2, 300) * .3, tik()), g, pan)   # satır sonu zili yerine sert tuş
def muhur(): return mix(gum(.25, 80) * 1.0, gurultu(.06, 1800) * zarf(int(.06 * SR), .001, .05) * .5)
def merdane(d=1.0): y = gurultu(d, 300); t = np.arange(len(y)) / SR; return y * (.6 + .4 * np.sin(2 * np.pi * 11 * t)) * zarf(len(y), .1, .3)
def sayfa(): y = gurultu(.45, 2500) * zarf(int(.45 * SR), .05, .25); return y * .6
def kasik(): t = np.arange(int(1.2 * SR)) / SR; return sum(a * np.exp(-t * d) * np.sin(2 * np.pi * f * t) for f, a, d in [(3520, 1, 6), (5100, .5, 9), (8100, .3, 14)])
def kaynama(d):
    y = gurultu(d, 2500) * .3; n = len(y)
    for _ in range(int(d * 25)):
        i = rng.integers(0, max(1, n - 2000)); tt = np.arange(1500) / SR; y[i:i + 1500] += np.sin(2 * np.pi * (300 + rng.random() * 500) * tt) * np.exp(-tt * 60) * .4
    return y * zarf(n, .5, .5)
def kurek(): return mix(gurultu(.5, 1200) * zarf(int(.5 * SR), .05, .3) * .6, gum(.2, 70) * .5)
def ates(d): return catirti(d, 18) * .8 + gurultu(d, 200) * .3
def damla(): t = np.arange(int(.25 * SR)) / SR; return np.sin(2 * np.pi * (900 + 700 * np.exp(-t * 40)) * t) * np.exp(-t * 30) * .5
def kalabalik(d): y = gurultu(d, 600); t = np.arange(len(y)) / SR; return y * (.6 + .3 * np.sin(2 * np.pi * .7 * t) * np.sin(2 * np.pi * .23 * t)) * zarf(len(y), 1, 1)
def saat_tik(t0, t1, g=.12):
    t = t0
    while t < t1: put(t, tik() * .6, g, .3); t += 1.0
def motor(d): t = np.arange(int(d * SR)) / SR; y = (np.sin(2 * np.pi * 45 * t) + .5 * np.sin(2 * np.pi * 90 * t)) * (.6 + .4 * np.sin(2 * np.pi * 6 * t)); return y * zarf(len(y), .8, .8) * .5
def sutdok(d=1.6): return gurultu(d, 900) * zarf(int(d * SR), .2, .6) * .6

# geçişler: merdane (zaman sıçraması), sayfa (mekân sıçraması)
for s in SHOTS:
    if s['tr'] == 'merdane': put(s['at'], merdane(1.0), .35)
    elif s['tr'] == 'sayfa': put(s['at'], sayfa(), .4)
# kupür ve belge planları: kâğıt sesi
for i in ['P04', 'P32', 'P37', 'P49', 'P60', 'P62', 'P76']: put(P(i), sayfa(), .25, .2)
# KANCA: Rize basın toplantısı
ortam(P('P01'), PE('P02'), kalabalik, .12)
for t in [S('A01') + 1.2, S('A01') + 2.3, W('A01', 'bardak') + .2, P('P02', .5), P('P02', 2.6)]: put(t, flas(), .45, -.2)
put(W('A01', 'çay') + .3, kasik(), .18, .1)
ortam(P('P03'), PE('P03'), lambda d: gurultu(d, 200) * .4, .2)   # boş depo uğultusu
put(P('P05', .4), kasik(), .22)
# I. YAPRAK
ortam(P('P07'), PE('P08'), ruzgar, .14)
ortam(P('P11'), PE('P11'), ruzgar, .08); put(W('B04', 'sütler'), sutdok(), .3, -.2)
ortam(P('P12'), PE('P14'), yagmur, .3); put(P('P13', .2), gok(3), .25)
ortam(P('P15'), PE('P15'), dalga, .18)
ortam(P('P17'), PE('P17'), lambda d: gurultu(d, 3000) * .15, .15)   # televizyon hışırtısı
ortam(P('P18'), PE('P20'), ruzgar, .1)
for t in np.arange(P('P18'), PE('P20'), 1.7): put(t, kus(3600 + 400 * np.sin(t)), .05, .5)
put(P('P19', .5), gurultu(.12, 3000) * zarf(int(.12 * SR), .002, .1), .3)   # yaprak koparılır
ortam(P('P21'), PE('P22'), motor, .2)
put(P('P24', .7), sayfa(), .2)
# II. BARDAK
ortam(P('P26'), PE('P26'), motor, .06)
for k in range(12): put(W('C02', 'saniyede') + k, tik(), .2)   # sayaç (saniyede bir; Geiger değil)
put(P('P28', .3), muhur(), .5)
daktilo(P('P29'), P('P29', 2.4), g=.2); put(P('P29', .45), muhur(), .5)
ortam(P('P30'), PE('P31'), kalabalik, .12); put(W('C05', 'demli') + .1, flas(), .4)
put(P('P33', .8), kasik(), .2)
ortam(P('P34'), PE('P34'), kaynama, .25)
put(P('P35', .5), kasik(), .15)
put(P('P37', .3), muhur(), .3)
# III. YİRMİ SAAT
daktilo(P('P38'), Ee('D01') - .5, g=.22)
ortam(P('P39'), PE('P39'), lambda d: gurultu(d, 200) * .4, .2)
put(P('P40', .5), kasik(), .15)
for k in range(int((PE('P41') - P('P41')) / .9)): put(P('P41', .3 + k * .9), kurek() * .5, .2)
daktilo(P('P42'), Ee('D05') - .3, g=.22)
ortam(P('P43'), PE('P44'), kalabalik, .1); saat_tik(P('P43'), PE('P43'))
for k in range(6): put(P('P43', 1 + k * .9), kasik(), .08, (k % 3 - 1) * .5)
for k in range(3): put(P('P44', .2 + k * .4), adim(), .3, .5)
put(W('D08', 'kabul'), muhur() * .5, .3)
put(P('P47', .6), sayfa(), .2)
ortam(P('P48'), PE('P48'), lambda d: gurultu(d, 4000) * zarf(int(d * SR), .2, .5) * .5, .2)   # akan su
ortam(P('P50'), PE('P50'), motor, .25)
put(W('D13', 'bakkalda'), muhur(), .4)
# IV. ÖLÇÜLMEYEN
ortam(P('P52'), PE('P54'), lambda d: gurultu(d, 150) * .3, .15)
daktilo(P('P55'), P('P55', 1.5), g=.15)
daktilo(P('P56'), P('P56', 4), g=.15, pan=-.3)
for t in [P('P57', .3), W('F06', 'karar')]: put(t, muhur(), .45)
ortam(P('P58'), PE('P58'), yagmur, .3)
# V. DEPO
ortam(P('P59'), PE('P59'), ruzgar, .15)
ortam(P('P61'), PE('P61'), ates, .3); saat_tik(P('P61'), PE('P61'), .08)
ortam(P('P63'), PE('P64'), ruzgar, .2)
for k in range(10): put(P('P63', 1 + k * .55), adim(), .2, -.3 + k * .06)
for k in range(8): put(P('P64', .5 + k * .7), gurultu(.3, 1800) * zarf(int(.3 * SR), .05, .2), .12, -.5)   # branda çırpınır
ortam(P('P65'), PE('P65'), lambda d: gurultu(d, 200) * .3, .15)
for k in range(int((PE('P65') - P('P65')) / .8)): put(P('P65', .3 + k * .8), damla(), .25, (k % 3 - 1) * .4)
ortam(P('P66'), PE('P66'), ruzgar, .25)
ortam(P('P67'), PE('P68'), ruzgar, .1)
for k in range(int((PE('P68') - P('P68')) / 1.3)): put(P('P68', .4 + k * 1.3), kurek(), .35)
ortam(P('P70'), PE('P72'), ruzgar, .12)
daktilo(P('P71'), Ee('E12'), g=.2)
put(W('E15', 'valisi'), muhur(), .5)
put(P('P75', 1), sayfa(), .3)
# VI. BUGÜN
put(P('P79') + 0, sayfa(), .2); put(W('G04', 'vazgeçiyorlar'), muhur(), .5)
for k in range(20): put(W('G05', 'yirmi') + k * .08, tik() * .5, .15, -.5 + k * .05)
put(P('P84', .5), kasik(), .25)
put(P('P85', .8), kasik(), .2)

pk = max(np.abs(L).max(), np.abs(R).max()) + 1e-9; L /= pk / .7; R /= pk / .7
out = (np.clip(np.stack([L, R], 1), -1, 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'efekt.wav'), 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
print('efekt.wav', round(DUR, 1), 'sn')
