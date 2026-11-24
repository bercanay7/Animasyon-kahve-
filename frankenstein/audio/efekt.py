#!/usr/bin/env python3
"""FRANKENSTEIN: efektler (numpy sentezi; örnek ses yok; scipy yok). python3 audio/efekt.py → audio/efekt.wav (48 kHz stereo)
Zamanlar timeline.js (cümle/kelime) ve vo/shots.json'dan (node tools/plan_listesi.js). Fener geçişlerinde slayt makinesinin tıkırtısı."""
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
def slayt():   # fener slaytının değişimi: mandal tıkı + camın sürtünmesi
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

# fener geçişleri (bölüm kartları: iris) ve mekân sıçramaları: slayt makinesi
for i, s in enumerate(SHOTS):
    if s['tr'] in ('iris', 'kayma'): put(s['at'], slayt(), .5)
# A: oda gecesi
ortam(0, S('A04'), lambda d: yagmur(d), .06)
kos(S('A02') + .3, S('A02') + 2.2, .22, .45, -.3); put(S('A02') + 1.6, kapi(), .5, -.6)
# B: 1816 yağmuru ve fırtına
ortam(S('B01') - .5, S('B03'), yagmur, .22); put(W('B02', 'şimşek') + .2, gok(4.5), .7, .2)
ortam(S('B03'), S('B08'), yagmur, .08)
put(W('B07', 'patladı') + .1, gok(6), .9)
ortam(W('B07', 'bunu'), S('B08'), yagmur, .2)
ortam(S('B08'), S('B12'), catirti, .3, -.4)
ortam(S('B12'), S('B16'), yagmur, .07); put(S('B15') - .1, gok(3), .3)
put(S('B16') + .5, tik(), .2)
# C: laboratuvar (yağmur), kaçış, buzul rüzgârı, kulübe ateşi
ortam(S('C01') - 1, S('C06'), yagmur, .08)
kos(S('C04') + .1, S('C04') + 1.8, .22, .45, -.4); put(S('C04') + 1.6, kapi(), .5, -.7)
ortam(S('C06') - .3, S('C09'), ruzgar, .35)
ortam(S('C09'), S('D01') - 1, catirti, .28)
# D: orman, ateş, köy, odunluk, ilkbahar, su
ortam(S('D01') - .5, S('D04'), ruzgar, .15)
for i in range(6): put(S('D03') + .2 + i * .17, kus(3600 + i * 300), .18, .4)
put(W('D03', 'korkuttu'), kanat(.8), .3, .5)
ortam(S('D04'), S('D05'), catirti, .35, .3); put(W('D04', 'çektim'), puf(), .4)
for i in range(6): put(W('D05', 'taşlarla') + i * .25, tuk(), .4, .5 - i * .15)
ortam(S('D06'), S('D08'), ruzgar, .12)
for i in range(6): put(S('D08') + .2 + i * .45, balta(), .35, .2)
for i in range(8): put(S('D09') + 1 + i * .9, kus(4200 + 200 * (i % 3)), .12, .5)
ortam(S('D11'), S('D12'), dalga, .15)
put(W('D11', 'sıçradım'), sicrama(), .25)
ortam(S('D12'), S('D13'), catirti, .08)
# E: kapı vuruşu, ateş, kapı açılışı, yangın, nehir, kurşun
for i in range(3): put(W('E01', 'çaldım') + .3 + i * .35, tuk(), .5)
ortam(S('E02'), S('E05'), catirti, .3)
put(S('E05'), kapi(), .8, -.5); put(W('E05', 'vurdu'), gum(.3, 80), .4)
ortam(S('E08') - .2, S('E09'), lambda d: catirti(d, 30), .55)
ortam(S('E09'), Ee('E10') + 1, dalga, .25); put(W('E09', 'atladım') + .2, sicrama(), .45)
put(W('E10', 'ateş') + .1, silah(), .75, .4)
# F: çayır akşamı, madalyon, deniz, mumlar
for i in range(5): put(S('F01') + 1 + i * 1.4, kus(3000 + 400 * i, .07), .08, -.3)
ortam(S('F08'), S('F11'), dalga, .3)
ortam(S('F09'), S('F11'), ruzgar, .15)
put(W('F09', 'parçaladı'), gum(.5, 70), .6); put(W('F09', 'parçaladı') + .1, gurultu(.6, 3000) * zarf(int(.6 * SR), .01, .5), .35)
for i in range(3): put(W('F11', 'sevdiklerini') + i * .9, puf(), .5)
# G: buz denizi, kamara, buz salı
ortam(S('G01') - 1, S('G05') + 8, ruzgar, .3)
ortam(S('G05'), S('G05') + 9, dalga, .35)
# H: önsöz, düş (ateş), bitiş
put(S('H02') + .2, tik(), .2); put(W('H02', 'yıllar'), slayt(), .4)
ortam(S('H06'), W('H06', 'uyandım'), catirti, .22)
ortam(S('H11') - .5, DUR, catirti, .18)

out = np.stack([L, R], 1); pk = np.abs(out).max(); out = out / pk * .8 if pk > 0 else out
with wave.open(str(HERE / 'efekt.wav'), 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print('efekt.wav', round(DUR, 1), 'sn')
