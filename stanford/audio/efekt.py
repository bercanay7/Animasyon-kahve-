#!/usr/bin/env python3
"""STANFORD 1971: efektler, numpy sentezi (örnek ses yok). Çekim listesi vo/shots.json (tools/plan_listesi.js) ve timeline.js'ten.
Makara tıkı ve bant başlangıcı, bandın durması, bandın bitişi (boşalan makara, çırpan uç), daktilo (döküm ve belge planları),
kelepçe, söndürücü, dolap kapısı, ayak sesi, tebeşir. Hiçbiri anlatımın üstüne binmez (anlatım altında −6 dB).
    python3 audio/efekt.py → audio/efekt.wav"""
import json, re, wave
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; FILM = HERE.parent
SR = 48000; rng = np.random.default_rng(1971)
TL = (FILM / 'timeline.js').read_text(encoding='utf-8')
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', TL, re.S).group(1))
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', TL, re.S).group(1))
DUR = float(re.search(r'window\.DUR\s*=\s*([\d.]+)', TL).group(1))
SH = json.load(open(FILM / 'vo' / 'shots.json'))
N = int(DUR * SR) + SR; L = np.zeros(N); R = np.zeros(N)
S = lambda i: CUES[i]['s']; Ee = lambda i: CUES[i]['e']
def W(i, w, n=0):
    k = 0
    for x in WORDS:
        if x['id'] == i and x['w'].startswith(w):
            if k == n: return x['s']
            k += 1
    return S(i)
def put(t, s, pan=0., g=1.):
    i = int(t * SR); n = min(len(s), N - i)
    if n <= 0 or i < 0: return
    L[i:i + n] += s[:n] * g * np.sqrt(.5 * (1 - pan)); R[i:i + n] += s[:n] * g * np.sqrt(.5 * (1 + pan))
T = lambda d: np.arange(int(d * SR)) / SR
def bant(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tik(v=.5, f=2400, d=.03):
    t = T(d); return v * np.exp(-t * 180) * (np.sin(2 * np.pi * f * t) + .5 * rng.normal(0, 1, len(t)))
def tus():   # daktilo tuşu: kısa metal vuruş + gövde
    t = T(.06); return .35 * np.exp(-t * 120) * (np.sin(2 * np.pi * 1800 * t) * .5 + rng.normal(0, 1, len(t))) + .2 * np.exp(-t * 60) * np.sin(2 * np.pi * 160 * t)
def daktilo(t0, sure=2.0, hiz=9):
    t = t0; r = rng
    while t < t0 + sure: put(t, tus(), (r.random() - .5) * .3, .5); t += 1 / hiz * (.6 + .8 * r.random())
    put(t + .1, tik(.4, 3200, .12), .2, .6)   # satır sonu çanı yok: yalnız şaryo tıkı
def makara_basla(t0):
    put(t0, tik(.7, 1500, .05), -.1); put(t0 + .12, tik(.5, 900, .04), .1)
    t = T(1.2); s = bant(rng.normal(0, 1, len(t)), 300, 2500) * np.minimum(1, t / .6) * .05; put(t0 + .15, s, 0)
def makara_dur(t0):
    t = T(1.4); f = 400 * np.exp(-t * 1.4); s = .12 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6); put(t0, s, 0); put(t0 + 1.3, tik(.6, 1300, .05), 0)
def bant_bitti(t0, sure=6):   # boşalan makarada bandın ucu her turda çırpar
    t = t0; per = .42
    while t < t0 + sure: put(t, tik(.35, 700, .04), .15, .8); t += per; per *= 1.04
def kelepce(t0):
    for i in range(5): put(t0 + i * .045, tik(.45, 3000 + i * 150, .04), 0)
def sondurucu(t0, sure=2.5):
    t = T(sure); s = bant(rng.normal(0, 1, len(t)), 1500, 9000) * np.minimum(1, t / .08) * np.minimum(1, (sure - t) / .6) * .25; put(t0, s, .3)
def kapi(t0, v=.6):
    t = T(.8); s = v * np.exp(-t * 9) * (np.sin(2 * np.pi * 90 * t) + .5 * np.sin(2 * np.pi * 210 * t)) + .3 * v * np.exp(-t * 40) * rng.normal(0, 1, len(t)); put(t0, s, -.2)
def adim(t0, n=6, ara=.55):
    for i in range(n):
        t = T(.12); s = .25 * np.exp(-t * 45) * (rng.normal(0, 1, len(t)) * .6 + np.sin(2 * np.pi * 110 * t)); put(t0 + i * ara, s, (-1) ** i * .15)
def tebesir(t0, sure=2.0):
    t = T(sure); s = bant(rng.normal(0, 1, len(t)), 2500, 8000) * (.5 + .5 * np.sin(2 * np.pi * 3.1 * t) ** 2) * .05; put(t0, s, .2)

# ---------------------------------------------------------------- olaylar
makara_basla(W('A01', 'dizilmiş') - .3); makara_basla(S('A02') + .3)
makara_dur(W('A03', 'son') + .2)
tebesir(W('B04', 'can') - .1, 1.6); tebesir(W('B04', 'korku') - .1, 1.2)
kelepce(W('B06', 'kelepçe'))
adim(S('B07') + .2, 8, .5)
sondurucu(W('C02', 'söndürücüyle') - .1)
kapi(W('C03', 'çıkarılıyor'))
kapi(W('C07', 'karanlık') + .3, .45)
makara_basla(S('D01') + 2.0)
makara_dur(W('D14', 'markın'))
makara_basla(S('F02') + .2)
makara_dur(W('F03', 'peki') + .6)   # rev3: bant bitmez, makaralar durur (Fable E3)
# daktilo: döküm ve belge planlarının başında
YAZI = {'dokum', 'rapor', 'dergi', 'z2018', 'ilan', 'kurallar', 'kart'}
for x in SH:
    if x.get('set') in YAZI and x['end'] - x['at'] > 2.5: daktilo(x['at'] + .15, min(2.2, (x['end'] - x['at']) * .4))

# ---------------------------------------------------------------- anlatım altında kısma, yaz
g = np.ones(N); hop = SR // 100
for c in CUES.values(): g[max(0, int((c['s'] - .1) * SR)):int((c['e'] + .05) * SR)] = 10 ** (-6 / 20)
k = np.ones(15) / 15; gs = np.repeat(np.convolve(g[::hop], k, 'same'), hop)[:N]; gs = np.pad(gs, (0, N - len(gs)), 'edge')
L *= gs; R *= gs
pk = max(np.abs(L).max(), np.abs(R).max(), 1e-9); L /= pk / .8; R /= pk / .8
out = (np.clip(np.stack([L, R], 1), -1, 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'efekt.wav'), 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
print('efekt.wav', round(DUR, 1), 'sn')
