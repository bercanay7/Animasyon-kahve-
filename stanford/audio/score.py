#!/usr/bin/env python3
"""STANFORD 1971: özgün müzik, numpy sentezi (örnek ses yok, indirme yok, ücretli üretim yok).
Ton hüküm vermez (kanal dersleri §17): müzik bant sahnesinde çekilir, yerini teybin hışırtısına ve motoruna bırakır.
Çalgılar: bant hışırtısı ve hafif titreşim (bütün filmin altında; telefon bandında ≥ 280 Hz katman), floresan uğultusu (120 Hz, ABD şebekesi; yalnız bodrum),
kısık piyano "sayım" motifi (Re Fa La Sol: dört sayım), yaylı dron (Re, La), tek piyano akoru (Re La Mi: çözülmeyen beşli + dokuzlu).
Son: "Peki."den önce ve sonra sessizlik; çıkış sorusunda sayım motifi yavaşlar ve açık beşliyle biter (sorulur, çözülmez).
    python3 audio/score.py → audio/music.wav (48 kHz stereo) + saniye saniye düzey özeti (tam bant ve 300 Hz üstü)
"""
import json, os, re, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; FILM = HERE.parent
SR = 48000
STEM = os.environ.get('STEM')   # STEM=ton: hışırtı, uğultu ve motor olmadan (telefon denetimi için tonlu iz)
rng = np.random.default_rng(71)
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
    f = hz(n); t = np.arange(int(dur * SR)) / SR; s = np.zeros_like(t)
    vib = 1 + .003 * np.sin(2 * np.pi * 4.3 * t)
    for k in range(1, 10):
        if f * k > 6000: break
        s += (1 / k) * (acik ** (k - 1)) * np.sin(2 * np.pi * f * k * vib * t + rng.random() * 6)
    env = np.minimum(1, t / 2.0) * np.minimum(1, (dur - t) / 2.0)
    return v * env * s
def piyano(n, dur=3.0, v=.35, kisik=False):
    f = hz(n) if isinstance(n, str) else n; t = np.arange(int(dur * SR)) / SR; s = np.zeros_like(t)
    for k in range(1, 9):
        fk = f * k * (1 + .0004 * k * k)
        if fk > 10000: break
        dec = max(.3, 1.2 + .7 * k - f / 400) * (2.2 if kisik else 1)   # kısık (keçeli): üst kısmiler çabuk söner
        s += (1 / k ** (1.9 if kisik else 1.4)) * np.exp(-t * dec) * np.sin(2 * np.pi * fk * t)
    s *= np.minimum(1, t / .004)
    return v * s
def akor(t0, notes, v=.16, dur=6):
    for i, n in enumerate(notes): put(t0 + i * .03, piyano(n, dur, v), (i - 1) * .25)
SAYIM = ['D4', 'F4', 'A4', 'G4']
def sayim(t0, v=.12, ara=.62, tekrar=1, son=None):
    t = t0
    for r in range(tekrar):
        for i, n in enumerate(SAYIM):
            nn = son if (son and r == tekrar - 1 and i == 3) else n
            put(t, piyano(nn, 2.2, v * (1 - .1 * i), kisik=True), (i - 1.5) * .15); t += ara
    return t
def ust(n):   # aynı nota, telefon hoparlörünün çalabildiği bölgeye (≥ 280 Hz) oktavla taşınır (Frankenstein dersi)
    m = re.match(r'([A-G][b#]?)(-?\d)', n); k = int(m[2])
    while hz(m[1] + str(k)) < 280: k += 1
    return m[1] + str(k)
UST = float(os.environ.get('UST', .50))   # 25 Kasım telefon denetimi: tonlu müzik telefonda saniyelerin yalnız %45'inde duyuluyordu
def pad(t0, t1, notes, v=.06):
    for i, n in enumerate(notes):
        put(t0, dron(n, max(.5, t1 - t0), v), pan=(i - 1) * .3)
        put(t0, dron(ust(n), max(.5, t1 - t0), v * UST, .4), pan=-(i - 1) * .3)
def ugultu(t0, t1, v=.012):
    """Floresan: 120 Hz + harmonikler (240, 360, 480; telefon bandına taşar), yavaş titreme."""
    if STEM == 'ton': return
    t = np.arange(int((t1 - t0) * SR)) / SR; s = np.zeros_like(t)
    for k, a in [(1, 1), (2, .7), (3, .5), (4, .35), (6, .2)]: s += a * np.sin(2 * np.pi * 120 * k * t + k)
    s *= (1 + .15 * np.sin(2 * np.pi * .23 * t)) * np.minimum(1, t / 1.5) * np.minimum(1, (t1 - t0 - t) / 1.5)
    put(t0, v * s, 0)
def hisirti(t0, t1, v=.010):
    """Bant hışırtısı: 2–7 kHz bant gürültüsü (FFT süzgeci), çok hafif genlik titreşimi (wow)."""
    if STEM == 'ton': return
    n = int((t1 - t0) * SR); x = rng.normal(0, 1, n)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR); X *= ((f > 1800) & (f < 7500)) * 1.0 + ((f > 300) & (f <= 1800)) * .25; x = np.fft.irfft(X, n)
    x /= np.abs(x).max() + 1e-9; t = np.arange(n) / SR
    x *= (1 + .08 * np.sin(2 * np.pi * .7 * t)) * np.minimum(1, t / 1.0) * np.minimum(1, (t1 - t0 - t) / 1.0)
    put(t0, v * x, .1)
def motor(t0, t1, v=.008):
    """Teyp motoru: 50 Hz ve 400 Hz civarı ince vızıltı (yalnız bant çalarken)."""
    if STEM == 'ton': return
    t = np.arange(int((t1 - t0) * SR)) / SR
    s = .6 * np.sin(2 * np.pi * 50 * t) + .4 * np.sin(2 * np.pi * 397 * t + .3 * np.sin(2 * np.pi * .9 * t))
    s *= np.minimum(1, t / .4) * np.minimum(1, (t1 - t0 - t) / .4); put(t0, v * s, -.1)

# ---------------------------------------------------------------- bütün film: bant hışırtısı (telefon bandı katmanı)
hisirti(0, DUR + .5, .009)
# ---------------------------------------------------------------- A: kanca (bodrum uğultusu; sayım motifi; teyp)
ugultu(S('A01'), S('A02'), .012)
sayim(S('A01') + .5, v=.11)
pad(S('A01'), Ee('A03') + 1, ['D2', 'A2'], .05)
motor(W('A01', 'dizilmiş') - .2, W('A01', 'dizilmiş') + 3.5, .006)
put(W('A01', 'sen') - .1, piyano('F4', 4, .14), 0)
motor(S('A02'), Ee('A02'), .006)
akor(W('A03', 'son') - .1, ['D3', 'A3'], .12, 5)
# ---------------------------------------------------------------- B: yazı tura (ilan, yönlendirme, polis, numaralar)
pad(S('B01'), Ee('B10'), ['D2', 'A2'], .045)
sayim(S('B02') + .6, v=.09, ara=.55)
put(W('B04', 'güç', 1), piyano('D3', 5, .18), 0)
ugultu(S('B07'), Ee('B10'), .011)
put(S('B09') + .2, piyano('A3', 3, .1), .2)
# ---------------------------------------------------------------- C: altı gün (bodrum)
ugultu(S('C01'), Ee('C12'), .012)
pad(S('C01'), Ee('C04'), ['D2', 'A2', 'F3'], .045)
sayim(S('C01') + 2.5, v=.09, ara=.5, tekrar=2)
pad(S('C05'), Ee('C08'), ['D2', 'Bb2'], .05)   # akşam vardiyası: altı derece (gölge)
for t in [W('C06', 'şınav'), W('C06', 'keyfi'), W('C06', 'yemeği')]: put(t, piyano('D2', 2.5, .12, kisik=True), 0)
put(S('C07'), piyano('Bb3', 4, .1), .2)
pad(S('C09'), Ee('C09') + .5, ['D2', 'A2'], .04)
# C10: "Buna bakamıyorum": müzik tamamen çekilir (aşağıda kısma), sonra tek nota
put(Ee('C10') + .3, piyano('A3', 5, .12), 0)
pad(S('C11'), Ee('C13') + 1, ['D2', 'A2'], .04)
sayim(S('C13') + .2, v=.1, ara=.62)
# ---------------------------------------------------------------- D: bant (müzik çekilir: hışırtı + motor; anahtar cümlelerde tek nota)
motor(S('D01'), Ee('D14'), .007)
pad(S('D01'), Ee('D02') + 1, ['D2', 'A2'], .035)
pad(Ee('D02') + .5, Ee('D14') + 1, ['D2', 'A2'], .028)   # telefon denetimi: bant boyunca ince zemin (önce 2 dk tonsuzdu)
put(S('D05') - .2, piyano('D3', 5, .14), 0)
put(S('D10') - .2, piyano('F3', 5, .14), 0)
put(W('D14', 'markın') - .1, piyano('A2', 6, .14), 0)   # açık bırakılan soru
pad(S('D15'), Ee('D17') + 1, ['D2', 'A2'], .035)
# ---------------------------------------------------------------- E: iki gardiyan (iki çalgı: gece altı derece, gündüz sayım)
pad(S('E01'), Ee('E07'), ['D2', 'Bb2'], .045)
ugultu(S('E02'), Ee('E04'), .01)
put(W('E06', 'buna'), piyano('D3', 4, .12), 0)
put(S('E08'), piyano('D2', 5, .14, kisik=True), 0)   # ölüm tarihi
pad(S('E08') + 1.5, Ee('E09') + 1, ['D2', 'A2'], .03)   # telefon denetimi: 8:27–8:49 tonsuzdu
pad(S('E10'), S('E13') + 1, ['D2', 'A2'], .04)
sayim(S('E10') + .5, v=.08, ara=.6)
pad(S('E13'), Ee('E14') + 1, ['D2', 'A2', 'F3'], .04)
# ---------------------------------------------------------------- F: cevap ("Peki." çevresinde sessizlik; açık beşli)
motor(S('F02'), Ee('F03'), .007)
pad(Ee('F02') - 1, S('F03'), ['D2', 'A2'], .03)
pad(S('F01'), Ee('F02'), ['D2', 'A2'], .035)
akor(Ee('F03') + 1.0, ['D3', 'A3', 'E4'], .13, 7)          # "Peki."den sonra: çözülmeyen akor
pad(S('F04'), DUR, ['D2', 'A2'], .045)
t = sayim(S('F05') + .3, v=.1, ara=.8, son='A4')          # sayım yavaşlar, Sol yerine La: açık kalır
akor(t + .4, ['D3', 'A3'], .1, 9)
sayim(Ee('F05') + 3, v=.07, ara=1.0, tekrar=2, son='A4')  # bitiş ekranı (son 20 sn)

# ---------------------------------------------------------------- yankı + anlatım altında kısma + sessizlikler + son
def yanki(x, sure=2.6, kuru=.65):
    n = int(sure * SR); t = np.arange(n) / SR; ir = rng.normal(0, 1, n) * np.exp(-t * 3.0) * .02; ir[0] = 0
    m = 1 << int(np.ceil(np.log2(len(x) + n)))
    return kuru * x + np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[:len(x)]
L = yanki(L); Rr = yanki(Rr)
g = np.ones(N); hop = SR // 100
for c in CUES.values():
    a, b = int((c['s'] - .15) * SR), int((c['e'] + .1) * SR); g[max(0, a):min(N, b)] = 10 ** (-5 / 20)
# müziğin tamamen çekildiği yerler (hışırtı da kısılır): "Buna bakamıyorum" ve "Peki."
for a_, b_ in [(S('C10') - 1.0, Ee('C10') + .2), (S('F03') - .8, Ee('F03') + .9)]:
    g[max(0, int(a_ * SR)):int(b_ * SR)] = 10 ** (-28 / 20)
k = np.ones(25) / 25; gs = np.repeat(np.convolve(g[::hop], k, 'same'), hop)[:N]; gs = np.pad(gs, (0, N - len(gs)), 'edge')
L *= gs; Rr *= gs
pkf = HERE / 'music_pk.json'
if STEM: pk = json.load(open(pkf))['pk']   # tonlu iz tam müzikle aynı ölçekte
else: pk = max(np.abs(L).max(), np.abs(Rr).max()); json.dump({'pk': pk}, open(pkf, 'w'))
L /= pk / .8; Rr /= pk / .8
fade = np.minimum(1, (N - np.arange(N)) / (3 * SR)); L *= fade; Rr *= fade
out = (np.clip(np.stack([L, Rr], 1), -1, 1) * 32767).astype(np.int16)
with wave.open(str(HERE / ('music_%s.wav' % STEM if STEM else 'music.wav')), 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
# düzey eğrisi (kanal kuralı: her müzik üretiminden sonra): tam bant ve 300 Hz üstü
def saniye_db(x):
    r = np.sqrt(np.mean(x[:len(x) // SR * SR].reshape(-1, SR) ** 2, 1)) + 1e-9; return 20 * np.log10(r)
db = saniye_db(L)
X = np.fft.rfft(L); f = np.fft.rfftfreq(len(L), 1 / SR); X[f < 300] = 0; ust = saniye_db(np.fft.irfft(X, len(L)))
print(f'music.wav {DUR:.1f} sn | medyan {np.median(db):.1f} dBFS | -60 dB üstü saniye: {(db > -60).sum()}/{len(db)} | -40 dB üstü: {(db > -40).sum()}')
print(f'300 Hz üstü: medyan {np.median(ust):.1f} dBFS | -60 dB üstü saniye: {(ust > -60).sum()}/{len(ust)}')
print('bölüm başı düzeyleri:', ' '.join(f"{i}:{db[int(S(i))]:.0f}" for i in ['A01', 'B01', 'C01', 'C10', 'D01', 'D05', 'E01', 'F01', 'F03', 'F05']))
sess = [i for i in range(len(db)) if db[i] < -60]
print('müziksiz saniyeler (-60 altı):', len(sess), sess[:40])
araliklar = []; i = 0
while i < len(ust):
    if ust[i] < -60:
        j = i
        while j < len(ust) and ust[j] < -60: j += 1
        if j - i >= 4: araliklar.append((i, j))
        i = j
    else: i += 1
print('300 Hz üstünde 4 sn\'yi aşan müziksiz aralıklar:', araliklar)
