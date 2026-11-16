#!/usr/bin/env python3
"""RAN (Zaman Kuryesi): özgün müzik ve efektler, yalnız numpy ile sentez (örnek ses yok, indirme yok, ücretli üretim yok).
Çalgılar: nefesli bambu flüt (shakuhachi/nōkan benzeri; miyako-bushi dizisi), alçak dron, taiko, ateş çıtırtısı, rüzgâr/yağmur, tek silah sesi.
Tōru Takemitsu'nun Ran müziği telifli: ezgi ya da motif taklidi yok; ezgiler burada yazıldı.
    python3 audio/score.py  -> audio/music.wav (48 kHz stereo, timeline.js DUR)
Her olay bir cümleye/kelimeye bağlı (timeline.js); sıraya dayanan bloklar (dron, ateş) yeni sıraya göre (vo/sira.json, 16 Kasım). H03 ("Hiçbir ses yok") boyunca müzik ve efekt tamamen susar (ma).
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
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(1985)

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
    if a >= N or b <= 0: return
    s = sig[:b - a] * g
    L[a:b] += s * np.sqrt(.5 * (1 - pan)); R[a:b] += s * np.sqrt(.5 * (1 + pan))

def lp(x, fc):   # tek kutuplu alçak geçiren (iki kez)
    a = np.exp(-2 * np.pi * fc / SR); y = x.copy()
    for _ in range(2):
        z = np.empty_like(y); acc = 0.0
        # vektörel değil ama kısa sinyallerde yeterli; uzunlar için blok
        z = _iir(y, a); y = z
    return y
def _iir(x, a):
    # y[n] = (1-a) x[n] + a y[n-1]  — kapalı biçim: kümülatif toplamla (sayısal kararlılık için bloklu)
    y = np.empty_like(x); prev = 0.0; B = int(max(8, min(4096, np.log(1e-9) / np.log(a))))
    for s in range(0, len(x), B):
        xb = x[s:s + B] * (1 - a); n = len(xb); p = a ** np.arange(n)
        c = np.cumsum(xb / p) * p + prev * a * p
        y[s:s + n] = c; prev = c[-1]
    return y
def hp(x, fc): return x - lp(x, fc)
def env(n, att, rel):
    e = np.ones(n); a = max(1, int(att * SR)); r = max(1, int(rel * SR))
    e[:a] = np.linspace(0, 1, a) ** 1.5; e[-r:] *= np.linspace(1, 0, r) ** 1.2
    return e

# ---------- çalgılar ----------
SC = {'D3': 146.83, 'Eb3': 155.56, 'G3': 196.0, 'A3': 220.0, 'Bb3': 233.08, 'D4': 293.66, 'Eb4': 311.13, 'G4': 392.0, 'A4': 440.0, 'Bb4': 466.16, 'D5': 587.33, 'Eb5': 622.25}
def flute_note(f, d, breath=.35, vib=.012):
    n = int(d * SR); t = np.arange(n) / SR
    slide = np.where(t < .14, .955 + .045 * (t / .14), 1.0)                   # alttan kayarak giriş
    meri = np.where(t > d * .78, 1 - .028 * np.clip((t - d * .78) / (d * .22), 0, 1) ** 1.5, 1.0)   # cümle sonu "meri" düşüşü
    vb = 1 + vib * np.clip((t - .35) / .4, 0, 1) * np.sin(2 * np.pi * 5.2 * t)
    ph = 2 * np.pi * np.cumsum(f * slide * meri * vb) / SR
    tone = np.sin(ph) + .32 * np.sin(2 * ph + .3) + .1 * np.sin(3 * ph)
    no = rng.standard_normal(n); no = hp(lp(no, f * 2.2), f * .6)
    br = no * (breath * (.6 + .4 * np.exp(-t / .12)))
    return (tone * .55 + br) * env(n, .09, min(.35, d * .4))
def flute(phrase, t0, pan=-.2, g=1.0):
    t = t0
    for nt, d in phrase:
        if nt != '-': put(flute_note(SC[nt], d + .08), t, pan, g)
        t += d
    return t
def drone(t0, t1, f, g=1.0, pan=0.0):
    n = int((t1 - t0) * SR); t = np.arange(n) / SR
    lfo = .75 + .25 * np.sin(2 * np.pi * .05 * t + f)
    s = (np.sin(2 * np.pi * f * t) + .45 * np.sin(2 * np.pi * f * 1.5 * t + 1) + .25 * np.sin(2 * np.pi * f * 2.003 * t)) * lfo
    s += lp(rng.standard_normal(n), 260) * .6
    put(s * env(n, 3, 4), t0, pan, .09 * g)
def taiko(t, g=1.0, pan=0.0):
    n = int(1.6 * SR); tt = np.arange(n) / SR
    f = 52 + 30 * np.exp(-tt / .05)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / .45)
    skin = lp(rng.standard_normal(n), 900) * np.exp(-tt / .04) * .5
    put((body + skin) * .9, t, pan, g)
def roll(t0, t1, g=.6):   # sıklaşan kalp atışı → tremolo
    t = t0; k = 0
    while t < t1:
        u = (t - t0) / (t1 - t0); taiko(t, g * (.5 + .5 * u), (k % 2 - .5) * .3); t += 1.1 - .95 * u; k += 1
def crackle(t0, t1, g=1.0):
    n = int((t1 - t0) * SR); x = np.zeros(n)
    k = rng.poisson(14 * (t1 - t0)); pos = rng.integers(0, max(1, n - 2000), k)
    for p in pos:
        m = rng.integers(200, 1600); x[p:p + m] += rng.standard_normal(m) * np.exp(-np.arange(m) / (m / 5)) * rng.uniform(.2, 1)
    rum = lp(rng.standard_normal(n), 180) * 1.4
    s = hp(x, 1200) * .5 + rum
    put(s * env(n, 1.2, 1.5), t0, .2, .16 * g); put(s[::-1] * env(n, 1.2, 1.5), t0, -.3, .1 * g)
def wind(t0, t1, g=1.0, rain=False):
    n = int((t1 - t0) * SR); t = np.arange(n) / SR
    w = lp(rng.standard_normal(n), 500) * (.6 + .4 * np.sin(2 * np.pi * .13 * t)) * 2
    if rain: w = w * .6 + hp(rng.standard_normal(n), 3000) * .35
    put(w * env(n, 1.5, 2), t0, -.4, .12 * g); put(np.roll(w, 3000) * env(n, 1.5, 2), t0, .4, .12 * g)
def shot(t):
    n = int(1.2 * SR); tt = np.arange(n) / SR
    s = rng.standard_normal(n) * np.exp(-tt / .012) + lp(rng.standard_normal(n), 400) * np.exp(-tt / .35) * .8
    put(s, t, .5, .7)

# ---------- beste (cümlelere bağlı) ----------
# A: yanan kale — ateş, alçak dron D; kanca sorusunda tek taiko; künyede flüt
crackle(0, S('A04'), 1.1); drone(0, S('C01') + 2, SC['D3'] / 2, 1.0)   # açılış: A01–A04 + B06–B07 (yeni sıra, vo/sira.json)
taiko(W('A03', 'yaptıkların'), .5)
flute([('D4', 1.2), ('Eb4', .7), ('G4', 2.0)], S('A04') - .2, g=.8)
# B: resimler — yumuşak dron, aralarda kısa flüt
drone(S('A05'), S('E07') + 2, SC['G3'] / 2, .8)   # taşınan blok: resimlerle çekilen film (E06'nın ardından)
flute([('A4', .9), ('G4', .6), ('Eb4', 1.6)], E('B03') - .6, g=.55)
flute([('D4', .8), ('-', .3), ('G4', 1.4)], E('B07') - .4, g=.6)
# C: üç ok — gündüz dronu; kırılmalar taiko
drone(S('C01'), S('D01') + 2, SC['D3'] / 2, .8)
flute([('G4', .7), ('A4', .7), ('Bb4', .9), ('A4', 1.4)], S('C01') - .5, pan=.2, g=.6)
taiko(W('C03', 'kırılır'), .8); taiko(W('C06', 'dizinde'), 1.0, .2); taiko(W('C06', 'dizinde') + .18, .5, -.2)
# D: kapılar — daha karanlık dron (Eb); "geçmiş"te vuruş
drone(S('D01'), S('E01') + 2, SC['Eb3'] / 2, 1.0)
taiko(W('D06', 'geçmiş'), .7); flute([('Eb4', 1.0), ('D4', 2.0)], E('D09') - .3, g=.6)
# E: üçüncü kale — kuşatmada sıklaşan davul, ateş, fırtına
drone(S('E01'), S('A05') + 2, SC['D3'] / 2, 1.2); drone(S('E07'), S('F01') + 2, SC['D3'] / 2, 1.2)
roll(S('E02'), W('E04', 'yaşlı'), .55); crackle(S('E03'), S('A05') + 1, 1.3)
taiko(W('E04', 'yaşlı'), .9)
wind(S('E07'), S('E09') + 1, 1.2, rain=True)
taiko(W('E09', 'hidetora'), .7)
# F: flüt — öne çıkan ezgi (kulübe); F03 sonrası 1,4 sn'lik boşlukta flüt yalnız
fl = [('D5', 1.4), ('Bb4', .8), ('A4', 1.0), ('G4', 2.2), ('-', .4), ('A4', .8), ('Bb4', .8), ('A4', 1.0), ('Eb4', 2.6)]
flute(fl, W('F03', 'flüt') - .2, pan=.25, g=1.0)
flute([('G4', 1.2), ('Eb4', .8), ('D4', 3.0)], S('F05') + .5, pan=.25, g=.55)
drone(S('F01'), S('G01') + 2, SC['G3'] / 2, .7)
# G: dönüş — barışma, kurşun, Sue'nün yolu
drone(S('G01'), S('H01') + 1, SC['D3'] / 2, .8)
flute([('A4', 1.0), ('Bb4', .8), ('D5', 2.4)], S('G02') - .3, g=.55)
shot(W('G04', 'kurşun'))
flute([('D5', 1.0), ('Bb4', .8), ('A4', 1.0), ('G4', 3.0)], W('G07', 'kardeşinin'), pan=.25, g=.75)
# H: surdaki adam — rüzgâr; H03'te tam sessizlik; sonra dron ve son ezgi
wind(S('H01'), S('H03') - .2, .6)
ma0, ma1 = S('H03') - .6, S('H04') - .1
drone(S('H04'), DUR, SC['D3'] / 2, .8)
flute([('D4', 1.0), ('Eb4', .8), ('G4', 1.4), ('A4', 2.4)], W('H09', 'sana'), pan=.2, g=.6)
flute([('G4', 1.2), ('A4', .8), ('Bb4', 1.0), ('A4', .8), ('G4', 1.2), ('Eb4', 1.0), ('D4', 4.0)], S('H11') + .5, pan=0, g=.9)

# ---------- konuşma altında kısma (anlatım duyulsun), ma, son ----------
def vo_env():
    with wave.open(str(FILM / 'vo' / 'vo.wav')) as w:
        sr = w.getframerate(); ch = w.getnchannels(); sw = w.getsampwidth(); d = w.readframes(w.getnframes())
    x = np.frombuffer(d, dtype={2: np.int16, 4: np.int32}[sw]).astype(np.float64)
    if ch > 1: x = x.reshape(-1, ch).mean(1)
    hop = sr // 100; m = len(x) // hop
    e = np.sqrt((x[:m * hop].reshape(m, hop) ** 2).mean(1)); e = e / (e.max() + 1e-9)
    on = (e > .04).astype(float); k = 25
    on = np.convolve(on, np.ones(k) / k, 'same')   # 0,25 sn yumuşatma
    return np.interp(np.arange(N) / SR, np.arange(m) / 100, np.clip(on * 1.4, 0, 1))
duck = 1 - .55 * vo_env()
mask = np.ones(N); a, b = int(ma0 * SR), int(ma1 * SR); f = int(.5 * SR)
mask[a:b] = 0; mask[a - f:a] = np.linspace(1, 0, f); mask[b:b + f] = np.linspace(0, 1, f)
endf = np.ones(N); g0 = int((DUR - 4) * SR); endf[g0:] = np.linspace(1, 0, N - g0)
L *= duck * mask * endf; R *= duck * mask * endf
pk = max(np.abs(L).max(), np.abs(R).max()); L /= pk / .7; R /= pk / .7
st = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'music.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print('audio/music.wav', round(DUR, 2), 'sn; ma', round(ma0, 2), '–', round(ma1, 2))
