#!/usr/bin/env python3
"""ÇERNOBİL'İN ÇAYI: özgün müzik, numpy sentezi (örnek ses yok, indirme yok, ücretli üretim yok).
Çalgılar: kemençe benzeri yaylı (Karadeniz; sıkışık, genizden, hızlı titreşim, süslemeli), piyano, cam bardak tınısı (kaşığın bardağa değmesi),
yaylı dron, matbaa nabzı (döner baskı makinesinin boğuk vuruşu: IV-V. bölümlerin altında). Radyasyon sesi (Geiger tıkırtısı) yok: görünmeyen duyulmaz da.
Ses dizisi: Re (Uşşak çeşnili minör: Re Mi Fa Sol La Si♭ Do). Yaprak ezgisi kemençede; bardak motifi piyano + cam (La Re).
Son: yaprak ezgisi izleyicinin bardağında Re üzerinde, açık beşliyle biter (çözülmez, sorulur).
    python3 audio/score.py → audio/music.wav (48 kHz stereo) + saniye saniye düzey özeti
"""
import json, re, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; FILM = HERE.parent
SR = 48000
rng = np.random.default_rng(16)
TL = (FILM / 'timeline.js').read_text(encoding='utf-8')
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', TL, re.S).group(1))
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', TL, re.S).group(1))
DUR = float(re.search(r'window\.DUR\s*=\s*([\d.]+)', TL).group(1))
N = int(DUR * SR) + SR
L = np.zeros(N); Rr = np.zeros(N)
S = lambda i: CUES[i]['s']; Ee = lambda i: CUES[i]['e']
def W(i, w, n=0):
    k = 0
    for x in WORDS:
        if x['id'] == i and x['w'].startswith(w):
            if k == n: return x['s']
            k += 1
    return S(i)
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def hz(n):
    m = re.match(r'([A-G])(b|#)?(-?\d)', n); p = NOTE[m[1]] + (-1 if m[2] == 'b' else 1 if m[2] == '#' else 0)
    return 440 * 2 ** ((p + 12 * (int(m[3]) + 1) - 69) / 12)
def put(t, sig, pan=0.0, g=1.0):
    i = int(t * SR)
    if i >= N or i + len(sig) <= 0: return
    if i < 0: sig = sig[-i:]; i = 0
    n = min(len(sig), N - i)
    L[i:i + n] += sig[:n] * g * np.sqrt(.5 * (1 - pan)); Rr[i:i + n] += sig[:n] * g * np.sqrt(.5 * (1 + pan))


def dron(n, dur, v=.2, acik=.5):
    """Yaylı dron: testere harmonikleri, yavaş vibrato, uzun giriş ve çıkış."""
    f = hz(n); t = np.arange(int(dur * SR)) / SR; s = np.zeros_like(t)
    vib = 1 + .003 * np.sin(2 * np.pi * 4.6 * t)
    for k in range(1, 10):
        if f * k > 6000: break
        s += (1 / k) * (acik ** (k - 1)) * np.sin(2 * np.pi * f * k * vib * t + rng.random() * 6)
    env = np.minimum(1, t / 1.6) * np.minimum(1, (dur - t) / 1.8)
    return v * env * s
def piyano(n, dur=3.0, v=.35):
    f = hz(n) if isinstance(n, str) else n; t = np.arange(int(dur * SR)) / SR; s = np.zeros_like(t)
    for k in range(1, 9):
        fk = f * k * (1 + .0004 * k * k)
        if fk > 10000: break
        dec = max(.3, 1.2 + .7 * k - f / 400)    # Dorian dersi: düşük notalarda sönüm eksiye düşmesin
        s += (1 / k ** 1.4) * np.exp(-t * dec) * np.sin(2 * np.pi * fk * t)
    s *= np.minimum(1, t / .004)
    return v * s
def bas(n, v=.5, dur=2.5):
    f = hz(n); t = np.arange(int(dur * SR)) / SR
    return v * np.exp(-t * 2.2) * (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2 * f * t))

def kemence(n, dur=1.0, v=.3, sus=False):
    """Kemençe benzeri: testere harmonikleri, 1,3 ve 2,6 kHz geniz bölgesi, hızlı titreşim (6,5 Hz), yay gürültüsü, kısa giriş."""
    f = hz(n) if isinstance(n, str) else n; t = np.arange(int(dur * SR)) / SR; s = np.zeros_like(t)
    vib = 1 + .006 * np.sin(2 * np.pi * 6.5 * t) * np.minimum(1, t / .25)
    for k in range(1, 18):
        fk = f * k
        if fk > 9000: break
        form = 1 + 2.2 * np.exp(-((fk - 1300) / 500) ** 2) + 1.4 * np.exp(-((fk - 2600) / 700) ** 2)
        s += form / k * np.sin(2 * np.pi * fk * vib * t + rng.random() * 6)
    s += .06 * rng.normal(0, 1, len(t))   # yay sürtünmesi
    env = np.minimum(1, t / .06) * np.minimum(1, (dur - t) / .08)
    if sus:   # süsleme: başta üst komşu notadan hızlı iniş
        g2 = np.exp(-t / .05); s = s * (1 - g2 * .5) + .5 * g2 * np.sin(2 * np.pi * f * 1.12 * t)
    return v * env * s / 6
def cam(n='A5', v=.25, dur=2.2):
    """Çay bardağına değen kaşık: uyumsuz kısmiler, hızlı sönüm."""
    f = hz(n); t = np.arange(int(dur * SR)) / SR
    s = sum(a * np.exp(-t * d) * np.sin(2 * np.pi * f * r * t) for r, a, d in [(1, 1, 3.5), (2.76, .5, 5), (5.4, .3, 8), (8.9, .15, 12)])
    return v * s * np.minimum(1, t / .002)
def nabiz(t0, t1, bpm=76, v=.22):
    """Matbaa nabzı: boğuk vuruş + kâğıt hışırtısı, her vuruşta."""
    d = 60 / bpm; t = t0
    while t < t1:
        tt = np.arange(int(.35 * SR)) / SR; kick = np.sin(2 * np.pi * (55 + 40 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9)
        put(t, kick, 0, v); put(t + d / 2, rng.normal(0, 1, int(.08 * SR)) * np.exp(-np.arange(int(.08 * SR)) / SR * 40) * .3, .3, v * .5)
        t += d
YAPRAK = [('D4', .5), ('F4', .5), ('G4', .5), ('A4', 1.0), ('G4', .5), ('F4', .5), ('E4', .5), ('D4', 1.5)]
def yaprak(t0, v=.26, hiz=1.0, oct=0, son=None):
    t = t0; notes = YAPRAK if not son else YAPRAK[:-1] + [(son, 2.5)]
    for i, (n, d) in enumerate(notes):
        nn = n[:-1] + str(int(n[-1]) + oct); put(t, kemence(nn, d * hiz * 1.05, v, sus=(i in (3, 7))), pan=-.1); t += d * hiz
def bardak(t0, v=.3):
    put(t0, cam('A5', .22), .2); put(t0 + .02, piyano('A4', 3, v), -.1); put(t0 + .55, piyano('D5', 4, v * .9), .1)
def pad(t0, t1, notes, v=.08):
    for i, n in enumerate(notes): put(t0, dron(n, t1 - t0, v), pan=(i - 1) * .3)

# ---------------------------------------------------------------- A: kanca (bardak motifi; Çaykur cümlesinde dron)
bardak(S('A01') + .3)
pad(S('A02'), Ee('A03') + 1, ['D2', 'A2'], .07)
put(W('A03', 'neye') - .2, piyano('F4', 4, .22), 0)
# ---------------------------------------------------------------- B: yaprak (kemençe ezgisi; yağmur)
pad(S('B01'), Ee('B12'), ['D2', 'A2', 'D3'], .05)
yaprak(S('B01') + .4); yaprak(S('B02') + .6, v=.2, hiz=1.15)
for t in [S('B03'), S('B04')]: put(t, bas('D2', .4), 0)
pad(S('B05'), Ee('B06'), ['Bb1', 'F2'], .06)
put(W('B06', 'rengi'), piyano('A5', 3, .12), .3); put(W('B06', 'kokusu'), piyano('G5', 3, .12), 0); put(W('B06', 'tadı'), piyano('F5', 3, .12), -.3)
yaprak(S('B09') + .3, v=.18, hiz=.9)
yaprak(S('B10') + .5, v=.14, hiz=.8, oct=-1)
# ---------------------------------------------------------------- C: bardak (sayılar; bakan)
pad(S('C01') - .5, Ee('C04') + 1, ['D2', 'A2'], .05)
for i, t in enumerate([S('C02'), W('C02', 'saniyede')]): put(t, piyano('A5', 1.5, .1), 0)
put(S('C04'), bas('D2', .5), 0); put(S('C04'), dron('C#3', 6, .05), .2)
bardak(S('C05') + .2, .26)
pad(S('C04'), Ee('C09'), ['D2', 'A2', 'F3'], .05)
put(Ee('C10') + .2, cam('A5', .2), 0); put(Ee('C10') + .4, piyano('D4', 5, .2), 0)   # "aklında tut"
# ---------------------------------------------------------------- D: yirmi saat (iki taraf: iki çalgı)
pad(S('D01'), Ee('D13'), ['D2', 'A2'], .045)
nabiz(S('D06'), Ee('D06'), bpm=60, v=.12)
put(S('D08'), piyano('D3', 4, .25), -.4); put(W('D08', 'odtünün'), piyano('Bb3', 4, .25), .4)
yaprak(S('D10') + .5, v=.12, hiz=1.1, oct=-1)
# ---------------------------------------------------------------- F: ölçülmeyen (seyrek piyano; boşluk)
pad(S('F01'), Ee('F07') + 1, ['D2', 'A2'], .04)
for i, n in enumerate(['A4', 'F4', 'E4', 'D4']): put(S('F04') + i * 2.2, piyano(n, 4, .14), 0)
put(S('F07'), kemence('A3', 4, .12), 0)
# ---------------------------------------------------------------- E: depo (matbaa nabzı; yığılan baskı)
nabiz(S('E01'), Ee('E09'), bpm=72, v=.16)
pad(S('E01'), Ee('E09'), ['D2', 'A2', 'Eb3'], .05)
put(S('E08'), bas('D2', .55), 0)
put(S('E10'), dron('D2', 9, .09), 0); put(S('E10') + .2, cam('A5', .18), 0)
pad(S('E11'), Ee('E16'), ['D2', 'G2', 'Bb2'], .045)
# ---------------------------------------------------------------- G: bugün (laboratuvar; izleyicinin bardağı)
pad(S('G01'), Ee('G04'), ['D2', 'A2'], .04)
pad(S('G05') - .5, Ee('G06') + 1, ['D2', 'A2', 'E3'], .05)
for i, n in enumerate(['D4', 'E4', 'F4', 'A4', 'G4']): put(S('G05') + i * 1.5, piyano(n, 3, .14), (i - 2) * .2)
pad(S('G07'), DUR, ['D2', 'A2', 'D3'], .05)
bardak(S('G09') + .2, .22)
yaprak(S('G10') + .3, v=.2, son='A4')
put(Ee('G10') + 1.0, cam('D6', .15), 0)

# ---------------------------------------------------------------- yankı + anlatım altında kısma + son
def yanki(x, sure=3.2, kuru=.6):
    n = int(sure * SR); t = np.arange(n) / SR; ir = rng.normal(0, 1, n) * np.exp(-t * 2.6) * .02; ir[0] = 0
    m = 1 << int(np.ceil(np.log2(len(x) + n)))
    return kuru * x + np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[:len(x)]
L = yanki(L); Rr = yanki(Rr)
g = np.ones(N); hop = SR // 100
for c in CUES.values():
    a, b = int((c['s'] - .15) * SR), int((c['e'] + .1) * SR); g[max(0, a):min(N, b)] = 10 ** (-5 / 20)
# doruk cümlelerinden önce sessizlik (C10 sözü, E13 köylülerin sorusu): müzik tamamen çekilir
for i in ['C10', 'E13']:
    a = int((S(i) - 1.2) * SR); b = int(Ee(i) * SR); g[max(0, a):b] = 10 ** (-30 / 20)
k = np.ones(25) / 25; gs = np.repeat(np.convolve(g[::hop], k, 'same'), hop)[:N]; gs = np.pad(gs, (0, N - len(gs)), 'edge')
L *= gs; Rr *= gs
pk = max(np.abs(L).max(), np.abs(Rr).max()); L /= pk / .8; Rr /= pk / .8
fade = np.minimum(1, (N - np.arange(N)) / (3 * SR)); L *= fade; Rr *= fade
out = (np.clip(np.stack([L, Rr], 1), -1, 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'music.wav'), 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
rms = np.sqrt(np.mean(L[:len(L) // SR * SR].reshape(-1, SR) ** 2, 1)) + 1e-9; db = 20 * np.log10(rms)
print(f'music.wav {DUR:.1f} sn | medyan {np.median(db):.1f} dBFS | -60 dB üstü saniye: {(db > -60).sum()}/{len(db)} | -40 dB üstü: {(db > -40).sum()}')
print('bölüm başı düzeyleri:', ' '.join(f"{i}:{db[int(S(i))]:.0f}" for i in ['A01', 'B01', 'C01', 'D01', 'F01', 'E01', 'E10', 'G01', 'G09', 'G10']))
sess = [i for i in range(len(db)) if db[i] < -60]
print('müziksiz saniyeler (-60 altı):', len(sess), sess[:40])
