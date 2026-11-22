#!/usr/bin/env python3
"""LALE ÇILGINLIĞI: efektler, yalnız numpy ile sentez (örnek ses ve ücretli üretim yok). Yardımcılar dorian-gray/audio/efekt.py'den (kendi kodumuz).
Meyhane uğultusu, mezat tokmağı, sikke, kâğıt, tüy kalem, matbaa presi, kış rüzgârı ve nal, kapı vuruşu, mühür, dalga ve martı, gece böcekleri, kalabalık.
Şiddet sesi yok (1730: kapı kapanır, sessizlik).
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
rng = np.random.default_rng(1637)
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

def ugultu(t0, t1, g=1.0, pan=0.0):   # kalabalık meyhane/kalabalık uğultusu: bant geçiren gürültü, hece gibi dalgalanan zarf
    n = int((t1 - t0) * SR); t = np.arange(n) / SR; x = rng.standard_normal(n).astype(np.float32)
    s = bp(x, 520, 1.2) * 2 * (.6 + .4 * np.abs(np.sin(2 * np.pi * 3.1 * t) * np.sin(2 * np.pi * .7 * t + 1)))
    s += bp(rng.standard_normal(n).astype(np.float32), 900, 1.6) * (.5 + .5 * np.abs(np.sin(2 * np.pi * 2.3 * t + 2)))
    put(s * zarf(n, 1.2, 1.5), t0, pan - .3, .1 * g); put(np.roll(s, 5000) * zarf(n, 1.2, 1.5), t0, pan + .3, .1 * g)
def tokmak(t, g=1.0):   # mezat tokmağı: tahta vuruş
    n = int(.4 * SR); tt = np.arange(n) / SR; s = bp(rng.standard_normal(n).astype(np.float32), 700, 2.5) * np.exp(-tt / .025) * 4 + np.sin(2 * np.pi * 180 * tt) * np.exp(-tt / .04)
    put(s, t, .1, .5 * g)
def kagit(t, d=.5, g=1.0, pan=0.0):   # kâğıt hışırtısı
    n = int(d * SR); tt = np.arange(n) / SR; s = hp(rng.standard_normal(n).astype(np.float32), 2500) * (np.abs(np.sin(2 * np.pi * 9 * tt)) ** 2) * np.sin(np.pi * tt / d)
    put(s, t, pan, .2 * g)
def sikke(t, n_=3, g=1.0):   # sikke şıngırtısı
    for k in range(n_):
        n = int(.5 * SR); tt = np.arange(n) / SR; f = 2400 + rng.uniform(-300, 600)
        s = (np.sin(2 * np.pi * f * tt) + .5 * np.sin(2 * np.pi * f * 2.76 * tt)) * np.exp(-tt / .12)
        put(s.astype(np.float32), t + k * rng.uniform(.06, .14), rng.uniform(-.3, .3), .08 * g)
def pres(t, g=1.0):   # matbaa presi: tahta gıcırtı + baskı darbesi
    n = int(.9 * SR); tt = np.arange(n) / SR; s = lp(rng.standard_normal(n).astype(np.float32), 200) * 4 * np.exp(-((tt - .5) / .04) ** 2) + bp(rng.standard_normal(n).astype(np.float32), 1100, 6) * np.exp(-((tt - .2) / .15) ** 2) * .6
    put(s, t, -.2, .35 * g)
def bocek(t0, t1, g=1.0):   # gece cırcır böcekleri
    n = int((t1 - t0) * SR); tt = np.arange(n) / SR
    for f, ph in ((4300, 0), (4700, 1.3)):
        s = np.sin(2 * np.pi * f * tt) * (np.sin(2 * np.pi * 28 * tt) > .2) * (np.sin(2 * np.pi * .9 * tt + ph) > -.1)
        put((s * zarf(n, 1, 1.5)).astype(np.float32), t0, -.5 if ph == 0 else .5, .018 * g)
def dalga(t0, t1, g=1.0): deniz(t0, t1, g)
def martilar(t0, t1, g=1.0):
    t = t0
    while t < t1:
        n = int(.5 * SR); tt = np.arange(n) / SR; f = 1500 + 500 * np.sin(np.pi * tt / .5); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / .5) ** 2
        put(s.astype(np.float32), t, rng.uniform(-.6, .6), .03 * g); t += rng.uniform(1.5, 3.5)
def vurkapi(t, g=1.0):   # kapıya üç vuruş
    for o in (0, .32, .64):
        n = int(.3 * SR); tt = np.arange(n) / SR; s = lp(rng.standard_normal(n).astype(np.float32), 400) * 4 * np.exp(-tt / .03)
        put(s, t + o, -.1, .45 * g)
def yaprak(t0, t1, g=1.0):   # çiçek/rüzgârda yaprak hışırtısı
    n = int((t1 - t0) * SR); tt = np.arange(n) / SR; s = hp(rng.standard_normal(n).astype(np.float32), 1800) * (.4 + .6 * np.abs(np.sin(2 * np.pi * .4 * tt)))
    put(s * zarf(n, 1, 1.5), t0, .3, .03 * g)

# ════════ olaylar ════════
# kanca: terazi gıcırtısı, mezat salonu uğultusu ve tokmak, İstanbul gecesi, kalabalık
kagit(S('A01') + .3, .3, .5); ugultu(S('A03'), S('A06'), 1.0); tokmak(W('A05', 'veriliyor'), 1.0); sikke(W('A05', 'beş', 1), 3)
bocek(S('A06'), W('A06', 'patrona'), .8); ugultu(W('A06', 'patrona'), S('A07'), .6, .2)
kagit(S('A07') + .3, .6)
# yol: kış rüzgârı, araba (nal), çiçek demeti hışırtısı; mektup kalemi; Leiden bahçe kuşları yerine rüzgâr; hırsız (kazma)
ruzgar(S('B01'), S('B04'), .8); nal(S('B01') + .5, S('B01') + 6, bpm=96, g=.4, yuru=True); yaprak(W('B01', 'demet'), S('B02') + 4)
kalem(S('B04') + .5, E('B04') - .2); ruzgar(S('B05'), S('B06'), .4)
for k in range(5): kagit(S('B06') + 1 + k * 1.3, .25, .5, -.2)
# alev: yaprak, ayna sessizliği, kese itilir
yaprak(S('C01'), S('C03')); sikke(W('C06', 'üç'), 5, .8)
# rüzgâr ticareti: kâğıt imzası, el değiştiren kâğıtlar, rüzgârda kâğıtlar, meyhane arka oda uğultusu, mezat, tokmak
kalem(S('D02') + 2, S('D02') + 6); kagit(S('D03'), .4); kagit(S('D03') + 1.2, .4, 1, .3); kagit(S('D03') + 2.4, .4, 1, -.3)
ruzgar(S('D04') - .2, S('D05'), 1.2); [kagit(S('D04') + k * .5, .3, .7, (-1) ** k * .4) for k in range(6)]
ugultu(S('D05'), S('D07'), .8); ugultu(S('D07'), S('D09'), 1.2); tokmak(W('D08', 'mezat'), 1); sikke(W('D08', 'kâğıt') if False else W('D08', 'her'), 7, .9)
# çöküş: uğultu kesilir; boş salon; Amsterdam tartışma uğultusu; kapıya vuruş; mühür
ugultu(S('E01'), W('E01', 'kimse'), .9); kagit(S('E02') + 1, .4, .6)
ugultu(S('E03'), E('E03'), .7); vurkapi(W('E04', 'satıcılar'), .9); kapi(S('E05') + .5); muhur(W('E06', 'yüzde'))
# efsane: matbaa presi, kâğıt; Mackay: kalem; rıhtım: dalga, martı; arşiv: sayfa
for k in range(3): pres(S('F01') + .3 + k * 1.3)
kagit(S('F02') + .2, .5); kalem(S('F04') + 1, E('F04')); dalga(S('F05'), E('F05') + .5, .7); martilar(S('F05'), E('F05'))
for k in range(4): kagit(S('F07') + k * 1.1, .3, .6)
for k in range(3): kagit(S('F08') + 1 + k * 2, .5, .7)
kagit(W('F11', 'tutulmayan'), .6, 1.2)
# İstanbul: su, kayık; Saadabad; gece böcekleri ve kandil; çarşı uğultusu; defter kalemi; mühür; gemi
dalga(S('G01'), S('G02') + 2, .4); bocek(S('G03'), S('G04'), 1); ugultu(S('G05'), E('G05') + .5, .6)
kalem(S('G06') + 1, E('G06')); muhur(W('G07', 'el')); dalga(S('G07'), E('G07'), .5); kalem(W('G09', 'dört'), W('G09', 'dört') + 1.5)
# 1730: kalabalık büyür, kapı kapanır; sessizlik; rüzgâr
ugultu(S('H02'), S('H03') + 1, 1.3); kapi(W('H03', 'öldürülüyor') - .3); ruzgar(S('H05'), E('H06') + .5, .5)
# ad: gazete matbaası, sayfa, sikkeler (bin altın), kitap
pres(S('I03') + .3); kagit(S('I03') + 2, .5); sikke(S('I04') + .5, 9, .9); kagit(S('I05') + .4, .5); kagit(S('I07') + .4, .6)
kagit(W('I08', 'sonradan'), .8, 1.0)
# son: kitaplar, meyhane uğultusu, terazi, kâğıt, tarla rüzgârı
kagit(S('J02') + .5, .5); ugultu(S('J03'), E('J03') + .3, .6); kagit(S('J05') + .5, .4); ruzgar(S('J06'), DUR - 1, .4); yaprak(S('J06'), DUR - 2)

pk = max(np.abs(L).max(), np.abs(R).max()); L /= pk / .6; R /= pk / .6
endf = np.ones(N, np.float32); g0 = int((DUR - 3) * SR); endf[g0:] = np.linspace(1, 0, N - g0); L *= endf; R *= endf
st = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'sfx.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print('audio/sfx.wav', round(DUR, 2), 'sn')
