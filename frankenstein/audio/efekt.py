#!/usr/bin/env python3
"""GILGAMIŞ: efektler (numpy sentezi; örnek ses yok). python3 audio/efekt.py → audio/efekt.wav (48 kHz stereo)
Zamanlar timeline.js (cümle/kelime) ve vo/shots.json'dan (geçişler; node tools/plan_listesi.js)."""
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
def lp(x, a):  # birinci derece alçak geçiren (blok döngüsü)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc = a * acc + (1 - a) * x[i]; y[i] = acc
    return y
def gurultu(d, a=.9): return lp(rng.normal(0, 1, int(d * SR)), a)
def zarf(n, at=.01, rl=.2):
    t = np.arange(n) / SR; d = n / SR; return np.minimum(1, t / at) * np.minimum(1, np.maximum(0, (d - t) / rl))
def bas(d=.5, f=55):
    t = np.arange(int(d * SR)) / SR; return np.sin(2 * np.pi * f * (1 + 1.2 * np.exp(-t * 25)) * t) * np.exp(-t * 9)
def muhur():   # kile bastırılan mühür: alçak gümleme + sürtünme
    x = bas(.6, 48) * .9; s = gurultu(.5, .95) * 4; s *= zarf(len(s), .05, .35)
    y = np.zeros(int(.7 * SR)); y[:len(x)] += x; y[:len(s)] += s * .35; return y
def catirti(d, yog=12):  # meşale çıtırtısı
    y = gurultu(d, .97) * 1.5; n = len(y)
    for _ in range(int(d * yog)):
        i = rng.integers(0, max(1, n - 600)); k = rng.normal(0, 1, 400) * np.exp(-np.arange(400) / 60); y[i:i + 400] += k * .6
    return y * zarf(n, 1, 1)
def su(d, hiz=.35):  # dalga/su şıpırtısı
    y = gurultu(d, .985) * 6; t = np.arange(len(y)) / SR; return y * (.5 + .5 * np.sin(2 * np.pi * hiz * t)) ** 2 * zarf(len(y), 1, 1)
def ruzgar(d): y = gurultu(d, .993) * 10; t = np.arange(len(y)) / SR; return y * (.6 + .4 * np.sin(2 * np.pi * .08 * t + 1)) * zarf(len(y), 2, 2)
def cik(f=4200, d=.08):  # kuş cıvıltısı
    t = np.arange(int(d * SR)) / SR; return np.sin(2 * np.pi * (f + 1800 * np.sin(t * 60)) * t) * np.exp(-t * 30)
def agustos(d): t = np.arange(int(d * SR)) / SR; return np.sin(2 * np.pi * 5200 * t) * (np.sin(2 * np.pi * 38 * t) > .2) * zarf(len(t), .3, .5) * .25
def gurleme(d=2.5): y = gurultu(d, .997) * 18; return y * zarf(len(y), .05, 1.6)
def tislama(d=.9): y = rng.normal(0, 1, int(d * SR)); y = y - lp(y, .6); return y * zarf(len(y), .15, .4) * .5
def surgu(d=.6): y = gurultu(d, .8) * 2 * zarf(int(d * SR), .05, .1); x = bas(.3, 90); y[-len(x):] += x * .8; return y
def kazi(d=.25): y = rng.normal(0, 1, int(d * SR)); y = y - lp(y, .9); return y * zarf(len(y), .01, .1) * .35

# geçişler
for s in SHOTS:
    if s['tr'] == 'muhur': put(s['at'], muhur(), .55)
# ortamlar
def ortam(a, b, f, g, pan=0):
    if b > a: put(a, f(b - a), g, pan)
ortam(S('A01'), Ee('A01') + .3, su, .10)
ortam(S('A02'), Ee('A02') + .5, catirti, .10, .3)
ortam(S('B04'), Ee('B07') + .5, ruzgar, .06)
ortam(S('C05'), Ee('C05') + 1, lambda d: ruzgar(d) * .3, .06)
for k in range(int((Ee('C05') - S('C05')) * 4)): put(S('C05') + k * .25 + rng.random() * .2, cik(3500 + rng.random() * 2500), .05, rng.random() * 1.6 - .8)
put(W('C05', 'ağustosböcekleri'), agustos(4), .12, .3)
ortam(S('D01'), Ee('D13') + 1.5, catirti, .08, .3)
ortam(S('D14'), Ee('E02') + 1, ruzgar, .07)
ortam(S('E05'), Ee('F06') + 1, su, .08)
ortam(S('G06'), Ee('G09') + 1, su, .08)
ortam(S('H01'), DUR, lambda d: ruzgar(d) * .5, .05)
# tek olaylar
put(W('A01', 'kaptırdı') - .2, tislama(), .35, -.3)
put(W('G07', 'aldı', 1) - .2, tislama(), .35, -.3)
put(W('B10', 'sarstılar'), bas(.8, 40), .5)
for k in range(5): put(W('B10', 'yıktılar') + k * .09, kazi(.12), .5, (k - 2) * .2)
put(W('C08', 'kestiler') + .3, bas(1.2, 35), .6); put(W('C08', 'kestiler'), kazi(.6), .5)
put(W('E05', 'sürgüledi'), surgu(), .45, -.2)
put(S('D11') + .3, surgu(), .4, .3)
for k in range(7): put(W('D12', 'altı') + k * .8, kazi(.2), .35, .3)
for k in range(3): put(S('F04') + 1.5 + k * 2.6, gurleme(), .3, (k - 1) * .4)
put(W('F04', 'kile'), bas(1.5, 30), .5)
for k in range(7): put(W('F08', 'her') + k * .8, kazi(.15), .25, .4)
put(S('G03') + .4, su(1.5, 1.2), .25)
out = np.stack([L, R], 1); pk = np.abs(out).max() + 1e-9; out = out / pk * .7
with wave.open(str(HERE / 'efekt.wav'), 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print('efekt.wav', round(DUR, 1), 'sn; muhur geçişi:', sum(1 for s in SHOTS if s['tr'] == 'muhur'))
