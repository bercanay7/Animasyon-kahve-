#!/usr/bin/env python3
"""MARY STUART (Zaman Kuryesi): özgün sessiz film eşliği, yalnız numpy ile sentez (örnek ses yok, indirme yok, ücretli üretim yok).
Çalgılar: piyano (eğik tel kısmileri, iki tel, çekiç gürültüsü), armonyum (yavaş giriş, titreşim), düşük piyano tremolosu.
Ezgiler bu dosyada yazıldı; bilinen bir halk ya da dönem ezgisi kullanılmadı:
  MARY: re minör, yükselen altılıyla açılan şarkı ezgisi (Mary'nin kalbi).
  ELIZ: mi minör, tören adımlı kısa motif (Elizabeth'in aklı; uzaktan, yüksek ve seyrek).
  ANKA: "Sonumda başlangıcım": aynı dört nota önce inerek (son), sonra çıkarak (başlangıç) çalınır.
Her olay bir cümleye ya da sözcüğe bağlı (timeline.js). L11 ("Ve salon sustu") boyunca müzik susar.
    python3 audio/score.py  -> audio/music.wav (48 kHz stereo)
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
rng = np.random.default_rng(1542)

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

NOTA = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def midi(n):
    m = re.match(r'([A-G])([#b]?)(-?\d)', n); return 12 * (int(m.group(3)) + 1) + NOTA[m.group(1)] + {'#': 1, 'b': -1, '': 0}[m.group(2)]
def hz(m): return 440 * 2 ** ((m - 69) / 12)

# ── çalgılar (önbellekli) ──
_PC = {}
def piyano(m, v=.7, d=2.5):
    key = (m, round(v * 4) / 4, round(min(d, 6) * 2) / 2)
    if key in _PC: return _PC[key]
    f0 = hz(m); dd = key[2] + 1.2; n = int(dd * SR); t = np.arange(n) / SR; B = .00035 * (1 + max(0, 60 - m) * .02)
    s = np.zeros(n)
    for k in range(1, 14):
        fk = f0 * k * np.sqrt(1 + B * k * k)
        if fk > 9000: break
        a = (1 / k ** 1.15) * (.35 + .65 * key[1]) ** (k * .25) * (1 + .3 * np.exp(-((k - 2) ** 2)))
        dec = (.55 + .05 * (m - 48)) * (1 + k * .55)
        for det in (-.0006, .0006):
            s += a * np.sin(2 * np.pi * fk * (1 + det) * t + k) * (np.exp(-t * dec) * .7 + .3 * np.exp(-t * dec * .25))
    ham = rng.standard_normal(int(.012 * SR)) * np.exp(-np.arange(int(.012 * SR)) / 90) * .15
    s[:len(ham)] += ham
    rel = np.ones(n); r0 = int(key[2] * SR); rel[r0:] = np.exp(-np.arange(n - r0) / (.18 * SR))
    s *= rel * key[1]; s[:64] *= np.linspace(0, 1, 64)
    _PC[key] = (s / 3.2).astype(np.float32); return _PC[key]
_HC = {}
def armonyum(m, d, v=.5):
    key = (m, round(d * 4) / 4, round(v * 4) / 4)
    if key in _HC: return _HC[key]
    f0 = hz(m); n = int((key[1] + .8) * SR); t = np.arange(n) / SR
    s = sum((1 / k) * np.sin(2 * np.pi * f0 * k * t * (1 + .0015 * np.sin(2 * np.pi * 5.5 * t))) for k in (1, 2, 3, 4, 6)) + .3 * np.sin(2 * np.pi * f0 * .5 * t)
    e = np.minimum(1, t / .45) * np.where(t > key[1], np.exp(-(t - key[1]) / .25), 1)
    _HC[key] = (s * e * key[2] * .22 * (1 + .08 * np.sin(2 * np.pi * 4.8 * t))).astype(np.float32); return _HC[key]

def nota(n, t, d=1.0, v=.7, pan=0.0, g=1.0, cal='p'):
    for x in n.split('+'):
        if x == '-' or not x: continue
        m = midi(x); put(piyano(m, v, d) if cal == 'p' else armonyum(m, d, v), t, pan + (m - 62) * .006, g)
def dizi(seq, t0, bpm=66, v=.7, pan=0.0, g=1.0, cal='p', leg=1.15):
    """seq: [(nota|akor|'-', vuruş)] → bitiş zamanı"""
    t = t0; b = 60 / bpm
    for n, d in seq:
        if t >= DUR: break
        if n != '-': nota(n, t, d * b * leg, v, pan, g, cal)
        t += d * b
    return t
def arpej(akorlar, t0, t1, bpm=66, v=.45, pan=-.15, g=1.0, desen=(0, 1, 2, 1)):
    """akor dizisi (nota listesi, vuruş) t1'e dek döner; her vuruş iki sekizlik"""
    t = t0; b = 60 / bpm; i = 0
    while t < t1:
        ak, vu = akorlar[i % len(akorlar)]; ns = ak.split(); k = 0
        for j in range(int(vu * 2)):
            if t >= t1: break
            n = ns[desen[k % len(desen)] % len(ns)]; nota(n, t, b * .9, v * (1.1 if j == 0 else .85), pan, g); t += b / 2; k += 1
        i += 1
    return t
def dron(notalar, t0, t1, v=.5, g=1.0, pan=0.0):
    d = t1 - t0
    for n in notalar.split(): put(armonyum(midi(n), d, v), t0, pan, g)
def tremolo(a, b, t0, t1, hiz=12, v=.4, g=1.0):
    t = t0; k = 0
    while t < t1:
        u = (t - t0) / max(.1, t1 - t0); nota(a if k % 2 == 0 else b, t, .2, v * (.6 + .4 * u), -.2, g); t += 1 / hiz; k += 1
def dortnal(kok, t0, t1, bpm=150, v=.45, g=1.0):
    t = t0; b = 60 / bpm; ns = [kok, kok, kok.replace('2', '3')]
    while t < t1:
        for i, x in enumerate(ns): nota(x, t + i * b / 3, b / 3, v * (1 if i == 0 else .7), -.25, g)
        t += b
def vurus(n, t, v=.9, g=1.0): nota(n, t, 3.0, v, 0, g)

# ── temalar ──
MARY = [('A4', 1), ('F5', 1.5), ('E5', .5), ('D5', 1), ('C#5', 1), ('D5', .5), ('E5', .5), ('A4', 2), ('Bb4', 1), ('G5', 1.5), ('F5', .5), ('E5', 1), ('D5', 1), ('C#5', .5), ('E5', .5), ('D5', 2)]
MARY_AK = [('D3 A3 D4 F4', 4), ('A2 E3 A3 C#4', 4), ('G2 D3 G3 Bb3', 4), ('D3 A3 D4 F4', 2), ('A2 E3 G3 C#4', 2)]
MARY_MAJ = [('A4', 1), ('F#5', 1.5), ('E5', .5), ('D5', 1), ('C#5', 1), ('D5', .5), ('E5', .5), ('A4', 2), ('B4', 1), ('G5', 1.5), ('F#5', .5), ('E5', 1), ('D5', 1), ('C#5', .5), ('E5', .5), ('D5', 3)]
MARY_MAJ_AK = [('D3 A3 D4 F#4', 4), ('A2 E3 A3 C#4', 4), ('G2 D3 G3 B3', 4), ('A2 E3 A3 C#4', 2), ('D3 A3 D4 F#4', 2)]
ELIZ = [('E5', .5), ('B4', .5), ('E5', 1), ('F#5', .5), ('G5', .5), ('F#5', 1), ('E5', 2)]
ELIZ_AK = [('E3 B3 E4', 2), ('E3 B3 D4 G4', 2), ('C3 G3 E4', 2), ('B2 F#3 B3', 2)]
ANKA_SON = [('D6', .5), ('A5', .5), ('F5', .5), ('D5', 1.5)]
ANKA_BAS = [('D5', .5), ('F5', .5), ('A5', .5), ('D6', 1.5)]
DANS = [('C5', 1), ('F5', 1), ('A5', 1), ('G5', 1.5), ('F5', .5), ('E5', 1), ('F5', 1), ('D5', 1), ('C5', 1), ('Bb4', 1), ('A4', 1), ('G4', 1), ('F4', 3)]
def dans_bas(t0, t1, bpm=96, v=.4):
    t = t0; b = 60 / bpm; ak = ['F2 A3+C4', 'C2 G3+Bb3', 'F2 A3+C4', 'Bb1 F3+D4']; i = 0
    while t < t1:
        kok, ust = ak[i % 4].split(); nota(kok, t, b, v); nota(ust, t + b, b * .5, v * .7); nota(ust, t + 2 * b, b * .5, v * .7); t += 3 * b; i += 1

# ════════ beste ════════
# A · kanca: alçak tremolo (gerilim), kırmızıda akor; Solway'de Mary teması ilk kez, ince
tremolo('D2', 'A2', .3, S('A03') - .5, hiz=10, v=.35)
vurus('D2+A2+D3+F3', W('A01', 'kırmızı'), .8)
nota('D5+F5+A5', W('A01', 'kırmızı') + .05, 3.5, .35, .2)
arpej(MARY_AK, S('A03') - .3, S('A06'), bpm=60, v=.32)
dizi(MARY[:8], S('A03') + 1.0, bpm=60, v=.42, pan=.1)
nota('A3+D4+F4', W('A04', 'rakibine'), 3, .5); nota('Bb2', W('A04', 'rakibine'), 3, .5)
dizi(ELIZ[:3], S('A05') + 1.2, bpm=80, v=.4, pan=.3)
dron('D3 A3', S('A06') - .2, S('A07') - .2, .35)
dizi([('A5', .5), ('F5', .5), ('D5', 1)], W('A06', 'sen'), bpm=70, v=.3, pan=.2)
dizi(ANKA_BAS, S('A07'), bpm=80, v=.3, pan=.25)   # beşik: müzik kutusu
# B · Fransa: beşik; savaş (alçak); dans (fa majör, 3/4); dul; elveda
dizi([('D6', 1), ('A5', 1), ('F5', 1), ('E5', 1), ('D5', 2)], S('B01') + .2, bpm=72, v=.28, pan=.3)
dron('D2 A2', S('B02'), W('B02', 'kral') + 1, .45)
tremolo('D2', 'Eb2', S('B02') + .5, W('B02', 'kral'), hiz=8, v=.3)
dron('D3 F3 A3', W('B02', 'kral'), W('B03', 'ölür') + .4, .3)
vurus('D1+D2', W('B03', 'ölür'), .7)
dizi(ANKA_BAS, W('B03', 'kraliçe') - .3, bpm=70, v=.35, pan=.25)
dans_bas(W('B04', 'şiir') - .3, S('B05') + 2.5, bpm=100, v=.32); dizi(DANS, W('B04', 'şiir'), bpm=100, v=.4, pan=.15)
arpej([('F3 C4 F4 A4', 4), ('Bb2 F3 Bb3 D4', 4)], S('B05'), S('B06'), bpm=66, v=.3)
dron('D3 A3', S('B06'), S('B07') - .3, .35)
vurus('A1+A2', W('B06', 'gerçek'), .6)
dizi(ELIZ, S('B07') + .4, bpm=72, v=.38, pan=.3)
tremolo('D2', 'A2', S('B08'), W('B08', 'bedelini'), hiz=8, v=.3)
vurus('D1+A1+D2', W('B08', 'bedelini'), .75)
arpej(MARY_AK, S('B09'), S('B12') - .2, bpm=56, v=.3)
dizi(MARY, S('B10') + 1, bpm=56, v=.38, pan=.1)
nota('D4+F4+A4', W('B11', 'elveda'), 4, .32, .2)
# C · sis: armonyum dronu; Knox: alçak akorlar
dron('D2 A2 D3', S('C01') - 1, S('C05') + 1, .5)
for k, w in enumerate(['keder', 'acı', 'karanlık']): vurus(['D1+D2', 'C1+C2', 'Bb0+Bb1'][k], W('C02', w), .7)
dizi([('A4', 1), ('F5', 2), ('E5', 1), ('D5', 2)], S('C05') + 1.5, bpm=60, v=.35, pan=.1)
arpej(MARY_AK[:3], S('C05'), S('C06') + 5, bpm=60, v=.26)
dizi(MARY[:4], S('C06') + .5, bpm=60, v=.38)
# D · kuzenler: yüzük (yüksek, ince), elçi ve Elizabeth motifi, satranç (kesik), Darnley (Mary teması majör)
arpej([('D4 F#4 A4 D5', 4), ('G3 B3 D4 G4', 4)], S('D01') - .5, S('D03'), bpm=72, v=.26)
dizi(MARY_MAJ[:8], S('D01') + .5, bpm=72, v=.36, pan=.15)
dortnal('D2', S('D03'), W('D03', 'yaz'), bpm=150, v=.3)
dizi(ELIZ, S('D05') + .2, bpm=76, v=.36, pan=.3); arpej(ELIZ_AK, S('D05'), S('D09'), bpm=76, v=.24)
dizi(ELIZ, S('D07') + .3, bpm=76, v=.32, pan=.35)
nota('E5+B5', W('D09', 'halde'), 1.5, .3, .3)
dron('E3 B3', S('D10'), S('D11'), .3); dizi([('B5', 1), ('G5', 1), ('E5', 2)], S('D10') + 2, bpm=60, v=.3, pan=.35)
for k in range(9): nota(['A2', 'E3'][k % 2], S('D11') + k * .9, .3, .35)          # satranç: kesik adımlar
for k in range(10): nota(['B2', 'F#3'][k % 2], S('D12') + k * .9, .3, .35)
nota('E3+B3+E4', W('D13', 'gözdesi'), 2, .45)
arpej(MARY_MAJ_AK, W('D14', 'kalbini'), S('E01') - 1, bpm=66, v=.32)
dizi(MARY_MAJ, W('D14', 'uzun'), bpm=66, v=.45, pan=.1)
dizi(MARY_MAJ[8:], S('D16') - .5, bpm=66, v=.4)
# E · Holyrood: soğuma; gerilim; cinayet (durur); kaçış (dörtnal); doğum; Greenwich dansı; Elizabeth'in kederi
dron('D3 F3 A3', S('E01'), S('E03'), .3)
tremolo('C#2', 'D2', S('E03'), S('E05'), hiz=9, v=.3)
tremolo('C#2', 'D2', S('E05'), W('E05', 'öldürdü'), hiz=14, v=.45)
vurus('C#1+G1+C#2', W('E05', 'öldürdü'), .9)
dron('D2 A2', S('E06') + .5, S('E07') - .2, .3)
dortnal('D2', W('E07', 'iki'), S('E08'), bpm=150, v=.4)
dizi(ANKA_BAS + ANKA_BAS, S('E08') - .2, bpm=72, v=.32, pan=.3)
dans_bas(S('E09'), W('E10', 'oturdu'), bpm=100, v=.28); dizi([(n, d) for n, d in ELIZ] + [('G5', 1), ('A5', 1), ('B5', 2)], S('E09') + .3, bpm=100, v=.36, pan=.3)
nota('E4+G4+B4', W('E10', 'oturdu'), 3, .3)
dron('E3 B3', W('E10', 'iskoçya') - .3, S('E11'), .28)
dizi(ELIZ, S('E11') + .2, bpm=84, v=.36, pan=.3)
dizi([('E5', 1), ('D5', 1), ('C5', 1), ('B4', 3)], W('E12', 'içi'), bpm=60, v=.32, pan=.3); arpej([('A2 E3 A3 C4', 4), ('E2 B2 E3 G3', 4)], S('E12'), S('F01') - .5, bpm=60, v=.22)
# F · Bothwell
dron('D2 A2', S('F01') - .5, S('F02') + 3, .3)
vurus('C1+G1+C2+Db2', W('F02', 'havaya'), 1.0); tremolo('C1', 'Db1', W('F02', 'havaya') + .1, W('F02', 'havaya') + 2.5, hiz=18, v=.6)
dron('C3 Eb3 G3', S('F03'), S('F04'), .28)
for k in range(12): nota(['D2', 'D2', 'Eb2'][k % 3], S('F04') + k * .7, .4, .45)
dizi(ELIZ_AK and [('E4', 1), ('G4', 1), ('B4', 2), ('A4', 1), ('G4', 1), ('E4', 2)], S('F05'), bpm=60, v=.32, pan=.3)
arpej([('C3 G3 C4 E4', 4), ('A2 E3 A3 C4', 4), ('F2 C3 F3 A3', 4), ('G2 D3 G3 B3', 4)], S('F06'), S('F07') + 1, bpm=60, v=.24)   # en yakın an: tek yumuşak majör
dizi([('E5', 1), ('D5', .5), ('C5', .5), ('E5', 2)], W('F06', 'sizin'), bpm=60, v=.34, pan=.3)
nota('D3+A3', S('F08'), 2, .4); tremolo('D2', 'Eb2', S('F09'), S('F10') - .3, hiz=10, v=.35)
dron('D3 A3', S('F10'), S('F13'), .25)
nota('C#3+G3', W('F12', 'zorla'), 3, .5)
dron('D2 A2 F3', S('F13'), S('F14'), .3)
for k in range(8): nota(['D3+F3+A3', 'D3+F#3+A3'][k % 2], S('F14') + k * 2.2, 2, .26)   # tutku mu, zor mu: minör/majör gidip gelir
nota('D3+A3', W('F17', 'kimse'), 4, .3)
# G · Lochleven
for k in range(7): vurus('D1', S('G01') + k * 1.2, .4)
dron('D2 A2', S('G01'), S('G03'), .3)
dron('A2 E3', S('G03') - .5, S('G04'), .35)
# G04: sessizlik (yalnız alçak tek nota)
nota('D2', S('G05') + .3, 4, .35); dizi([('D5', 2), ('C#5', 2), ('C5', 2), ('B4', 2), ('Bb4', 4)], S('G05') + .5, bpm=60, v=.3, pan=.2)
dizi(ANKA_BAS, W('G05', 'kral') - .4, bpm=70, v=.3, pan=.3)
dizi(MARY[:8], S('G06') + .2, bpm=56, v=.32)
dron('A2 E3', S('G07') - .3, S('G08'), .3)
dizi([('D4', .5), ('F4', .5), ('A4', .5), ('D5', .5), ('F5', .5), ('A5', 1)], S('G08') + 1, bpm=110, v=.38, pan=.2)
nota('A2+E3', W('G08', 'kilitledi'), 2, .5)
arpej([('D3 A3 D4 F4', 2), ('C3 G3 C4 E4', 2)], S('G09'), S('G10'), bpm=100, v=.32)
dizi([('A5', .5), ('F5', .5), ('D5', .5), ('A4', .5), ('F4', .5), ('D4', .5), ('A3', .5), ('D3', 2)], W('G10', 'dağıldı') - .6, bpm=120, v=.4)
# H · Solway (karar): kaçış, gece, kıyı; Mary teması tam ve geniş (birinci doruk)
dortnal('D2', S('H01') - .5, S('H03') - .2, bpm=150, v=.42)
dron('D2 A2', S('H03'), S('H04'), .3)
dizi([('A5', 1.5), ('F5', 1.5)], W('H03', 'baykuşlar'), bpm=50, v=.25, pan=.4)
arpej(MARY_AK, S('H04'), S('H07'), bpm=56, v=.24)
dizi(MARY[:8], S('H05') + .3, bpm=56, v=.36, pan=.1)
nota('D1+A1', S('H06') + .2, 3, .5)
dron('D3 A3', S('H07'), S('H10'), .26)
dizi(ELIZ[:4], W('H09', 'elizabethten') - .3, bpm=70, v=.3, pan=.3)
for k in range(8): nota('A4', S('H10') + k * .6, .2, .25, .2)   # bekleyiş (saat)
arpej(MARY_AK, S('H11'), S('H12'), bpm=60, v=.28)
arpej(MARY_AK, S('H12') - .5, S('H14'), bpm=54, v=.36, desen=(0, 1, 2, 3, 2, 1))
dizi(MARY, S('H12') + .2, bpm=54, v=.52, pan=.1)
dron('D3 A3 F4', S('H14'), S('H16'), .26)
vurus('D1+A1+D2+F2', W('H16', 'kaçmış'), .85)
dizi([('F5', 1), ('E5', 1), ('D5', 3)], S('H17'), bpm=56, v=.3)
# I · on dokuz yıl: saat gibi ostinato; anka; zincir; Walsingham
for k in range(int((S('I06') - S('I01')) / .8)): nota(['A4', 'E4'][k % 2], S('I01') + k * .8, .15, .26, .2)
dron('D2 A2', S('I01'), S('I06'), .26)
vurus('D1+D2', W('I04', 'öldürürse'), .6)
dizi(MARY[:4], S('I06') + .2, bpm=56, v=.3)
nota('D3+A3+D4', W('I07', 'reddetti'), 2, .45)
dron('E3 B3', S('I08'), S('I10'), .26)
dizi(ANKA_SON, S('I10'), bpm=72, v=.3, pan=.3)
dron('D3 A3', S('I11'), S('I14'), .22)
dizi(ANKA_SON + [('-', 1)] + ANKA_BAS, S('I12') + .1, bpm=66, v=.42, pan=.25)
dizi(ANKA_BAS, W('I13', 'ateşin'), bpm=72, v=.34, pan=.3)
t = S('I14'); k = 0
while t < S('I15'):
    nota(['D2', 'D2', 'Eb2'][k % 3], t, .3, .3 + .25 * (t - S('I14')) / (S('I15') - S('I14'))); t += .9 - .5 * (t - S('I14')) / (S('I15') - S('I14')); k += 1
arpej([('G2 D3 G3 B3', 4), ('D3 A3 D4 F#4', 4)], S('I15'), S('I16'), bpm=66, v=.24)
dizi(MARY[:4], S('I16') + .3, bpm=48, v=.3)
dizi([('E3', 1), ('B2', 1), ('E3', 1), ('F#3', .5), ('G3', .5), ('F#3', 1), ('E3', 2)], S('I17') + .3, bpm=60, v=.4, pan=-.2)
# J · mektuplar
dron('D3 A3', S('J01'), S('J03'), .24)
dizi([('D5', .5), ('F5', .5), ('A5', 1)], W('J02', 'açıldı'), bpm=90, v=.3, pan=.3)
for k in range(10): nota(['D4', 'A3'][k % 2], S('J03') + k * .55, .2, .26)
dizi(MARY[:8], S('J04') - .2, bpm=66, v=.32)
for k in range(int((S('J06') - S('J05')) / .45)): nota('E5' if k % 4 == 0 else 'B4', S('J05') + k * .45, .1, .22, .3)   # şifre: tıkırtı
tremolo('D2', 'Eb2', S('J06'), S('J07'), hiz=9, v=.3)
vurus('D2+A2+D3', S('J07') + .1, .55)
dron('D2 A2', S('J08'), S('J10'), .28)
vurus('Bb0+Bb1', W('J10', 'darağacı'), .7)
arpej(MARY_AK, S('J12'), S('J13'), bpm=56, v=.24); dizi(MARY[:8], W('J12', 'vicdanınıza'), bpm=56, v=.38)
nota('D3+G#3+D4', W('J13', 'geriye'), 4, .35)
# K · Elizabeth, Elizabeth'e karşı: motif iki sesli (kanon), belirsiz akorlar
dizi(ELIZ, S('K01') - .3, bpm=66, v=.36, pan=.35); dizi([(n.replace('5', '4'), d) for n, d in ELIZ], S('K02'), bpm=66, v=.32, pan=-.3); dizi(ELIZ, S('K02') + 1.8, bpm=66, v=.3, pan=.35)
dron('E3 B3', S('K03'), S('K05'), .26)
for k, w in enumerate(['desem', 'desem', 'cevapsız']): nota(['E3+G3+B3', 'E3+G#3+B3', 'E3+A3+B3'][k], W('K04', w, min(k, 1)) if w == 'desem' else W('K04', w), 3, .3)
vurus('E1+B1+E2', W('K05', 'imzaladı') + .3, .8)
dron('D2 A2', S('K06'), S('K10'), .26)
nota('C#5', W('K07', 'kısaltmanın'), 2, .3, .3)
tremolo('D2', 'Eb2', S('K08'), S('K09'), hiz=6, v=.2)
nota('D3+F3+A3', W('K09', 'kanun'), 4, .35)
dortnal('D2', S('K10'), W('K10', 'elizabethin'), bpm=150, v=.38)
dizi(ELIZ[:4], W('K10', 'elizabethin'), bpm=60, v=.3, pan=.35)
tremolo('D2', 'A2', S('K11'), S('L01') - .5, hiz=8, v=.3)
vurus('D1+D2', W('K11', 'öğrendi'), .7)
# L · Kırmızı: gece korali (armonyum), son mektup; salon; kızıl; sessizlik; tül; köpek; Elizabeth'in kırık motifi
for k, ak in enumerate(['D3 A3 D4 F4', 'Bb2 F3 Bb3 D4', 'G2 D3 G3 Bb3', 'A2 E3 A3 C#4', 'D3 A3 D4 F4', 'F2 C3 F3 A3', 'G2 D3 G3 Bb3', 'A2 E3 G3 C#4']):
    dron(ak, S('L01') + k * 4, S('L01') + k * 4 + 4.2, .3)
dizi(MARY[:8], S('L03') + .5, bpm=50, v=.32)
dron('D3 A3 F4', S('L05'), S('L06'), .24)
arpej(MARY_AK[:2], S('L06'), S('L07'), bpm=50, v=.26); dizi([('A4', 1), ('F5', 2)], S('L06') + .3, bpm=50, v=.34)
for k in range(5): vurus('D2+A2', S('L07') + k * 2.6, .5)   # salon: alçak, yavaş vuruşlar
nota('D4+F#4+A4+D5', W('L08', 'kızıl'), 5, .45, .1); nota('D2+A2', W('L08', 'kızıl'), 5, .5)
dron('D3 F#3 A3', W('L08', 'kızıl') + 1, S('L10'), .26)
dizi([('F#5', 1), ('E5', 1), ('D5', 2)], W('L09', 'ağlamayın'), bpm=56, v=.3, pan=.2)
dron('D3 A3', S('L10'), S('L11'), .28)
sus0, sus1 = S('L11') - .3, S('L12') - .4      # salon sustu: müzik yok
dizi(MARY_MAJ[:8], S('L12') + .3, bpm=52, v=.34); arpej(MARY_MAJ_AK, S('L12'), S('L16'), bpm=52, v=.24)
dizi(MARY_MAJ[8:], S('L14') + .3, bpm=52, v=.34)
dizi([('A5', 2), ('F#5', 2), ('D5', 4)], S('L16') + .2, bpm=54, v=.28, pan=.3)
nota('D2+A2+D3', S('L17') + .2, 4, .45)
dizi([('D5', .5), ('F#5', .5), ('A5', 1), ('F#5', 2)], W('L18', 'köpeği'), bpm=66, v=.3, pan=.25)
dizi([('E5', .5), ('B4', .5), ('E5', 1), ('-', 1), ('F#5', .5), ('G5', .5), ('-', 1), ('E5', 3)], S('L19') + .2, bpm=60, v=.34, pan=.3)
dron('E3 B3', S('L19'), S('L21'), .26)
nota('E3+G3+B3+D#4', W('L21', 'niyetimin'), 4, .4)    # çözülmeyen akor
# M · kim kazandı: Elizabeth'in töreni; ölüm; James; anka motifi; iki tema birlikte (mezarlar); son
dizi([(n, d * 1.5) for n, d in ELIZ], S('M01'), bpm=60, v=.38, pan=.3); arpej(ELIZ_AK, S('M01'), S('M03'), bpm=60, v=.26)
vurus('E1+B1+E2', W('M03', 'öldü'), .6)
arpej(MARY_MAJ_AK, S('M04'), S('M07'), bpm=60, v=.28); dizi(MARY_MAJ, S('M04') + .3, bpm=60, v=.42, pan=.1)
dizi(ANKA_SON + [('-', .5)] + ANKA_BAS, S('M07'), bpm=66, v=.42, pan=.25)
arpej([('D3 A3 D4 F#4', 4), ('B2 F#3 B3 D4', 4), ('G2 D3 G3 B3', 4), ('A2 E3 A3 C#4', 4)], S('M08'), S('M11'), bpm=56, v=.26)
dizi(MARY_MAJ[:8], S('M09') + .5, bpm=56, v=.36, pan=-.15); dizi([(n.replace('#', ''), d) for n, d in ELIZ], S('M09') + 2.6, bpm=56, v=.3, pan=.35)   # iki ezgi ilk kez birlikte
dron('D3 A3 D4', S('M10'), S('M11'), .24)
nota('D4+G4+A4', S('M11') + .2, 5, .35)    # soru: asılı akor
arpej(MARY_MAJ_AK, S('M12') - .3, DUR, bpm=60, v=.28); dizi(MARY_MAJ, S('M12'), bpm=60, v=.42, pan=.1)
dizi(ANKA_BAS, S('M13') + 3, bpm=60, v=.32, pan=.25)

# ── oda yankısı (FFT ile, blok blok) ──
def yanki(x, sure=2.2, kuru=.82, islak=.3):
    n = int(sure * SR); t = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-t / .45); ir[:int(.02 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
    B = 1 << 20; F = 1 << int(np.ceil(np.log2(B + n))); H = np.fft.rfft(ir, F); y = np.zeros(len(x) + n, np.float32)
    for s in range(0, len(x), B):
        seg = x[s:s + B]; c = np.fft.irfft(np.fft.rfft(seg, F) * H, F)[:len(seg) + n]; y[s:s + len(c)] += c.astype(np.float32)
    return x * kuru + y[:len(x)] * islak
L = yanki(L); R = yanki(R)

# ── konuşma altında kısma, sessizlik, son ──
def vo_env():
    with wave.open(str(FILM / 'vo' / 'vo.wav')) as w:
        sr = w.getframerate(); ch = w.getnchannels(); sw = w.getsampwidth(); d = w.readframes(w.getnframes())
    x = np.frombuffer(d, dtype={2: np.int16, 4: np.int32}[sw]).astype(np.float32)
    if ch > 1: x = x.reshape(-1, ch).mean(1)
    hop = sr // 100; m = len(x) // hop
    e = np.sqrt((x[:m * hop].reshape(m, hop) ** 2).mean(1)); e = e / (e.max() + 1e-9)
    on = np.convolve((e > .04).astype(float), np.ones(30) / 30, 'same')
    return np.interp(np.arange(N) / SR, np.arange(m) / 100, np.clip(on * 1.4, 0, 1)).astype(np.float32)
duck = 1 - .5 * vo_env()
mask = np.ones(N, np.float32); a, b = int(sus0 * SR), int(sus1 * SR); f = int(.6 * SR)
mask[a:b] = 0; mask[a - f:a] = np.linspace(1, 0, f); mask[b:b + f] = np.linspace(0, 1, f)
endf = np.ones(N, np.float32); g0 = int((DUR - 5) * SR); endf[g0:] = np.linspace(1, 0, N - g0)
L *= duck * mask * endf; R *= duck * mask * endf
pk = max(np.abs(L).max(), np.abs(R).max()); L /= pk / .7; R /= pk / .7
st = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'music.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print('audio/music.wav', round(DUR, 2), 'sn; sessizlik', round(sus0, 2), '–', round(sus1, 2), '; piyano notası önbelleği', len(_PC))
