#!/usr/bin/env python3
"""FRANKENSTEIN: özgün müzik, numpy ile sentez (örnek ses yok, indirme yok, ücretli üretim yok).
Çalgılar: cam armonika (fantazmagorya gösterilerinin çalgısı: yavaş girişli, titreşimli cam tonu), yaylı dron, piyano (Mary), kontrbas darbesi.
Ses dizisi: Re minör. El motifi (yaratık): A4 D5 C5 A4 (uzanır, geri düşer). Mary teması (piyano): Dm Bb F C arpej.
Son: el motifi Re majörde çözülür (H08–H11: "ona karşı bir sevgim var").
    python3 audio/score.py  → audio/music.wav (48 kHz stereo) + saniye saniye düzey özeti (Dorian dersi: müzik gerçekten var mı?)
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

def armonika(n, dur=3.0, v=.4):
    """Cam armonika: temel + zayıf 2. ve 3. kısmi, 0,12 sn yavaş giriş, hafif genlik titreşimi ve iki kolun vuruşması."""
    f = hz(n); t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / .14) * np.exp(-t * .55 / max(1, dur / 3)) * np.minimum(1, (dur - t) / .25)
    trem = 1 + .06 * np.sin(2 * np.pi * 5.2 * t + rng.random() * 6)
    s = np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.003 * t) + .18 * np.sin(2 * np.pi * 2 * f * t) + .06 * np.sin(2 * np.pi * 3.01 * f * t)
    return v * env * trem * s / 1.6
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
def kume(t0, notes, dur=4, v=.12):   # uyumsuz armonika kümesi (dehşet)
    for i, n in enumerate(notes): put(t0 + i * .05, armonika(n, dur, v), pan=(i - len(notes) / 2) * .2)
ELM = ['A4', 'D5', 'C5', 'A4']      # el motifi
def el(t0, ara=.62, v=.32, oct=0, son=None):
    notes = ELM if not son else ELM[:-1] + [son]
    for i, n in enumerate(notes):
        nn = n[:-1] + str(int(n[-1]) + oct)
        put(t0 + i * ara, armonika(nn, 2.6 if i < 3 else 4.5, v), pan=-.15 + i * .1)
MARY = [['D3', 'F3', 'A3', 'D4'], ['Bb2', 'D3', 'F3', 'Bb3'], ['F2', 'A2', 'C3', 'F3'], ['C3', 'E3', 'G3', 'C4']]
def mary(t0, t1, ara=.34, v=.16, ak=MARY):
    t, i = t0, 0
    while t < t1:
        ch = ak[(i // 8) % len(ak)]; n = ch[[0, 1, 2, 3, 2, 1, 2, 3][i % 8]]
        put(t, piyano(n, 2.4, v * (1.15 if i % 8 == 0 else 1)), pan=.25); t += ara; i += 1
def ust(n):   # aynı nota, telefon hoparlörünün çalabildiği bölgeye (≥ 280 Hz) oktavla taşınır
    k = int(n[-1])
    while hz(n[:-1] + str(k)) < 280: k += 1
    return n[:-1] + str(k)
UST = .30    # 24 Kasım müzik denetimi: dron 70–150 Hz'deydi; telefonda (izleyicinin %48'i) uzun aralıklar müziksiz duyuluyordu
def pad(t0, t1, notes, v=.08):
    for k, n in enumerate(notes):
        put(t0, dron(n, t1 - t0, v, .45), pan=(k - 1) * .3)
        put(t0, dron(ust(n), t1 - t0, v * UST, .5), pan=-(k - 1) * .3)

# ---------------------------------------------------------------- A: kanca
pad(0, S('A02'), ['D2', 'A2'], .10)
el(W('A01', 'elini') - .2, v=.3)
kume(S('A02') + .1, ['C#5', 'D5', 'G#4'], 2.5, .1); put(S('A02') + .1, bas('D2', .45))
put(S('A03'), armonika('F4', 6, .14)); put(W('A03', 'frankenştayn'), armonika('E4', 5, .16), pan=.3)
pad(S('A02') + 1, S('A04') + .5, ['D2', 'A2'], .07)   # 0:21–0:23 kancada istenmemiş boşluk vardı
pad(S('A04'), Ee('A05') + 1.5, ['D2', 'F2'], .08)
for i, n in enumerate(['A4', 'D5', 'E5']): put(W('A05', 'canavar') + i * .7, armonika(n, 4, .22))
# ---------------------------------------------------------------- B: 1816 (Mary teması; fırtına; uyanık düş)
pad(S('B01'), S('B03'), ['D2', 'A2', 'D3'], .07)
mary(S('B03') - .3, S('B06'), v=.13)
put(S('B04') + .5, armonika('F5', 4, .12)); put(S('B05') + .5, armonika('E5', 5, .12))
pad(S('B06'), S('B08'), ['Bb1', 'F2'], .09)
put(W('B06', 'sönmüştü'), bas('Bb1', .5, 4)); put(W('B07', 'patladı'), bas('G1', .7, 5)); kume(W('B07', 'patladı') + .2, ['G3', 'Ab3', 'D4'], 6, .08)
pad(S('B08'), S('B12'), ['D2', 'A2', 'F3'], .06)
for i, k in enumerate(['B09', 'B10', 'B11']): put(S(k), piyano(['D4', 'F4', 'A4'][i], 3, .14), pan=.3)
pad(S('B12'), S('B16'), ['D2', 'Eb2'], .08)
kume(S('B13') + 1, ['D5', 'Eb5', 'A4'], 7, .07); el(S('B14') + .3, v=.22, oct=1, son='G#4'); put(S('B15'), bas('D2', .6, 3)); kume(S('B15') + .05, ['C#5', 'D5'], 2, .1)
mary(S('B16'), Ee('B16') + 1, v=.15)
# ---------------------------------------------------------------- C: Kasım gecesi (laboratuvar, buzul)
pad(S('C01') - 1, S('C03'), ['D2', 'A2'], .09)
put(S('C03') + .3, armonika('A5', 6, .2)); pad(S('C03'), S('C04') + 1, ['D2', 'Ab2'], .09)
kume(S('C04'), ['C#5', 'D5', 'G#4'], 2.5, .1); put(S('C04'), bas('D2', .5))
for k, w in [('sefil', 'D4'), ('alçak', 'C4'), ('canavar', 'Bb3')]: put(W('C05', k), piyano(w, 3, .2))
pad(S('C06'), S('C09'), ['A1', 'E2', 'A2'], .08); put(S('C06') + .5, armonika('E6', 6, .07))
el(S('C07') + .2, v=.24, oct=-1)
pad(S('C09'), S('D01') - .5, ['F2', 'C3'], .08)
# ---------------------------------------------------------------- D: yaratığın anlatısı (el motifi açılır; ilkbaharda Fa majör)
pad(S('D01') - 1.2, S('D04'), ['D2', 'A2'], .07)
for i, k in enumerate(['işık', 'karanlık', 'açlık', 'soğuk']): put(W('D01', k), armonika(['A5', 'D4', 'F4', 'E4'][i], 2.5, .14))
el(W('D02', 'yükseldi'), v=.26)
for i in range(5): put(S('D03') + .4 + i * .23, armonika(['D6', 'F6', 'E6', 'A6', 'G6'][i], .8, .05), pan=.4)
pad(S('D04') - .5, S('D06'), ['D2', 'A2'], .06); put(W('D04', 'çektim'), bas('D2', .4)); put(W('D04', 'çektim'), armonika('C#5', 1.5, .1))
kume(S('D05') + .4, ['F4', 'Gb4', 'C5'], 4, .07)
pad(S('D06'), S('D08'), ['F2', 'C3'], .07)
FA = [['F3', 'A3', 'C4', 'F4'], ['Bb2', 'D3', 'F3', 'Bb3'], ['C3', 'E3', 'G3', 'C4'], ['F3', 'A3', 'C4', 'F4']]
mary(S('D08'), S('D11'), ara=.36, v=.12, ak=FA)
for i, k in enumerate(['baba', 'anne', 'kardeş']): put(W('D10', k), armonika(['C5', 'A4', 'F4'][i], 2.5, .14))
put(W('D10', 'benim'), bas('D2', .4, 4)); pad(W('D10', 'benim'), S('D11'), ['D2', 'A2'], .08)
kume(W('D11', 'sıçradım'), ['Eb5', 'D5', 'A4'], 3, .1)
pad(S('D11') - .5, S('D12') + 1, ['D2', 'A2'], .06)   # sudaki yüz: 5:30–5:32 boşluğu
pad(S('D12'), S('E01'), ['D2', 'F2', 'A2'], .07)
el(S('D13') + 1, v=.22)
# ---------------------------------------------------------------- E: kör adam (en sıcak an; sonra kırılma)
pad(S('E01') - 1.2, S('E02'), ['F2', 'C3'], .06); mary(S('E02') - .5, S('E05'), ara=.4, v=.11, ak=FA)
el(W('E04', 'elini') - .3, v=.28, son='F4')
put(S('E05'), bas('D1', .9, 4)); kume(S('E05') + .05, ['C#5', 'D5', 'G#4', 'A4'], 3, .12)
put(W('E06', 'kaldırmadım'), armonika('D4', 5, .15))
pad(S('E07'), S('E09'), ['D2', 'Ab2'], .09)
pad(S('E09'), S('E10') + 3, ['F2', 'C3'], .06)
put(W('E10', 'iyiliğimin'), bas('D2', .5, 4))
# ---------------------------------------------------------------- F: ben de yaratabilirim
pad(S('F01') - 1.2, S('F03'), ['D2', 'A2'], .07)
put(W('F02', 'frankenştayn'), bas('D2', .7, 3)); kume(W('F02', 'frankenştayn'), ['D4', 'Eb4', 'A4'], 4, .1)
pad(S('F03'), S('F05'), ['D1', 'Eb2'], .09)
put(S('F04'), bas('Bb1', .7, 3)); kume(S('F04') + .1, ['Bb3', 'B3', 'E4'], 3, .1)
for i, n in enumerate(['A5', 'F5', 'D5', 'E5']): put(S('F05') + .4 + i * 1.1, armonika(n, 3, .13))
pad(S('F05') + 4, S('F09'), ['D2', 'A2'], .07)
pad(S('F09'), S('G01') - 1, ['D2', 'Eb2', 'A2'], .07); put(W('F09', 'parçaladı'), bas('D2', .6)); kume(W('F09', 'parçaladı'), ['C#5', 'D5'], 2, .1)
for i in range(3): put(W('F11', 'sevdiklerini') + i * .9, piyano(['A2', 'F2', 'D2'][i], 3, .3))
# ---------------------------------------------------------------- G: buzlar (el motifi döner)
pad(S('G01') - 1.2, S('G05') + 7, ['D2', 'A2', 'E3'], .06)
el(W('G02', 'uzanmıştı') - .4, ara=.8, v=.26)
put(S('G04'), armonika('F4', 5, .12))
for i, n in enumerate(['A4', 'F4', 'D4']): put(W('G05', 'dalgalar') + i * 1.6, armonika(n, 5, .12 - i * .03))
# ---------------------------------------------------------------- H: çirkin evladım (Mary teması; sonda Re majörde çözülür)
mary(S('H02'), S('H05'), v=.11)
pad(S('H05'), S('H08'), ['D2', 'A2'], .07)
for i, n in enumerate(['A4', 'D5', 'F5', 'E5', 'D5']): put(S('H06') + .3 + i * 1.2, armonika(n, 3, .1))
RE = [['D3', 'F#3', 'A3', 'D4'], ['G2', 'B2', 'D3', 'G3'], ['D3', 'F#3', 'A3', 'D4'], ['A2', 'C#3', 'E3', 'A3']]
mary(S('H08'), S('H11') + 1, v=.13, ak=RE)
el(W('H08', 'sevgim') - .1, v=.26, son='D4')
pad(S('H09'), DUR, ['D2', 'A2', 'F#3'], .06)
el(W('H11', 'ekranda') - .4, ara=.7, v=.24, son='D5')

# ---------------------------------------------------------------- yankı + anlatım altında kısma + son
def yanki(x, sure=3.2, kuru=.6):
    n = int(sure * SR); t = np.arange(n) / SR; ir = rng.normal(0, 1, n) * np.exp(-t * 2.6) * .02; ir[0] = 0
    m = 1 << int(np.ceil(np.log2(len(x) + n)))
    return kuru * x + np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[:len(x)]
L = yanki(L); Rr = yanki(Rr)
g = np.ones(N); hop = SR // 100
for c in CUES.values():
    a, b = int((c['s'] - .15) * SR), int((c['e'] + .1) * SR); g[max(0, a):min(N, b)] = 10 ** (-5 / 20)
# H06'dan sonra 1,6 sn: müzik kabarmasın (Fable)
a = int(Ee('H06') * SR); g[a:a + int(1.6 * SR)] = 10 ** (-9 / 20)
k = np.ones(25) / 25; gs = np.repeat(np.convolve(g[::hop], k, 'same'), hop)[:N]; gs = np.pad(gs, (0, N - len(gs)), 'edge')
L *= gs; Rr *= gs
pk = max(np.abs(L).max(), np.abs(Rr).max()); L /= pk / .8; Rr /= pk / .8
fade = np.minimum(1, (N - np.arange(N)) / (3 * SR)); L *= fade; Rr *= fade
out = (np.clip(np.stack([L, Rr], 1), -1, 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'music.wav'), 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
rms = np.sqrt(np.mean(L[:len(L) // SR * SR].reshape(-1, SR) ** 2, 1)) + 1e-9; db = 20 * np.log10(rms)
print(f'music.wav {DUR:.1f} sn | medyan {np.median(db):.1f} dBFS | -60 dB üstü saniye: {(db > -60).sum()}/{len(db)} | -40 dB üstü: {(db > -40).sum()}')
print('bölüm başı düzeyleri:', ' '.join(f"{i}:{db[int(S(i))]:.0f}" for i in ['A01', 'B01', 'C01', 'D01', 'D08', 'E02', 'F04', 'G02', 'H06', 'H11']))
sess = [i for i in range(len(db)) if db[i] < -60]
print('müziksiz saniyeler (-60 altı):', len(sess), sess[:40])
