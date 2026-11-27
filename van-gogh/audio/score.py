#!/usr/bin/env python3
"""VAN GOGH'A KİM İNANDI? (Zaman Kuryesi): özgün müzik, yalnız numpy ile sentez (örnek ses yok, indirme yok, ücretli üretim yok).
Çalgılar dorian-gray/audio/score.py'den (mary-stuart sentezi): piyano, armonyum, tremolo. Ezgiler bu dosyada yazıldı.
  ZARF motifi (fa majör): la-do-fa-mi-do; Theo'nun her ay yolladığı zarf. Sarı zarflar gelince bir oktav yukarıda.
  TREN: alçak re minör ostinato (gece treni); gündüz yumuşar.
  NİNNİ: yüksek, müzik kutusu gibi (beşik, badem dalı).
  Renk doruğu (F04) tam akorlar ve armonyum kabarması; G09 "öldü"de müzik tamamen susar (yalnız rüzgâr efekti).
    python3 van-gogh/audio/score.py  -> van-gogh/audio/music.wav (48 kHz stereo); STEM=ton: yalnız tonlu iz (telefon denetimi)
"""
import json, re, wave, os
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
rng = np.random.default_rng(1853)

def S(i): return CUES[i]['s']
def E(i): return CUES[i]['e']
def W(i, w, n=0):
    k = 0
    for x in WORDS:
        if x['id'] == i and x['w'].startswith(w):
            if k == n: return x['s']
            k += 1
    print('kelime yok', i, w); return S(i)
SUS = []   # [t0, t1]: müziğin tamamen sustuğu aralıklar (sonda uygulanır)
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
        dec = max(.3, .55 + .05 * (m - 48)) * (1 + k * .55)
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
ZARF = [('A4', .5), ('C5', .5), ('F5', 1), ('E5', .5), ('C5', 1.5)]
ZARF_UST = [(n.replace('4', '5').replace('5', '6', 1) if False else n, d) for n, d in ZARF]
def oktav(seq, k=1): return [(re.sub(r'(-?\d)', lambda m: str(int(m.group(1)) + k), n) if n != '-' else n, d) for n, d in seq]
ZARF_MIN = [('A4', .5), ('C5', .5), ('D5', 1), ('C5', .5), ('A4', 1.5)]
NINNI = [('C6', .5), ('A5', .5), ('F5', .5), ('A5', .5), ('G5', 1), ('E5', 1), ('F5', 2)]
AK_F = [('F2 C4 F4 A4', 2), ('C2 C4 E4 G4', 2), ('D2 D4 F4 A4', 2), ('A#1 D4 F4 A#4', 2)]
AK_D = [('D2 D4 F4 A4', 2), ('A#1 D4 F4 A#4', 2), ('G1 D4 G4 A#4', 2), ('A1 C#4 E4 A4', 2)]
AK_PARLAK = [('F2 A3 C4 F4 A4', 2), ('A#1 A#3 D4 F4', 2), ('C2 G3 C4 E4', 2), ('F2 A3 C4 F4', 2)]
def tren(t0, t1, bpm=132, v=.3, g=1.0, kok='D2'):
    t = t0; b = 60 / bpm; i = 0
    while t < t1:
        nota(kok, t, b * .5, v * (1 if i % 4 == 0 else .7), -.2, g); nota(kok.replace('2', '3'), t + b / 2, b * .4, v * .55, -.2, g)
        if i % 2 == 0: nota(kok.replace('2', '4'), t, b * .4, v * .7, .2, g)   # telefon bandı: üst oktav
        t += b; i += 1
def ak(akor, t, d=3.0, v=.45, g=1.0): nota('+'.join(akor.split()), t, d, v, 0, g)

# ════════ beste ════════
# A · kanca: fa'da örtü; soru cümlesinde zarf motifi; "ekleniyor"da motif bir oktav yukarıda (badem dalı); A03 asılı akor, kısılır
dron('F2 C3', .3, S('A03') + 2.5, .26)
dizi(ZARF, W('A01', 'kim') - .1, bpm=76, v=.34, pan=.25)
dizi(oktav(ZARF), W('A01', 'ekleniyor'), bpm=88, v=.26, pan=.35)
arpej([('F3 A3 C4 F4', 2), ('C3 G3 C4 E4', 2)], S('A02'), S('A03'), bpm=70, v=.24)
ak('D3 A3 E4 F4', S('A03') + .2, 4, .32)
# B · Paris: yürüyen arpej; Louvre'da motif; banknotlar; "hayır"da re minör asılı; gece treni ostinatosu, "Ertesi"de fa'ya açılır
arpej(AK_F, S('B01') - .2, S('B04'), bpm=72, v=.26)
dizi(ZARF, W('B02', 'louvre'), bpm=72, v=.32, pan=.25)
dizi(ZARF, S('B04') + .3, bpm=80, v=.28, pan=.2); dizi(ZARF, S('B04') + 3.6, bpm=80, v=.26, pan=.2); dizi(ZARF, S('B04') + 6.9, bpm=80, v=.24, pan=.2)
arpej(AK_F, S('B05'), S('B07'), bpm=76, v=.24)
arpej([('F3 A3 C4', 2), ('A#2 D3 F3', 2)], S('B07'), W('B07', 'hayır') - .3, bpm=66, v=.22)
ak('D2 A2 D3 F3 A3', W('B07', 'hayır'), 4.5, .4); dron('A3 D4', W('B07', 'hayır') + 2, S('B08') + 1, .14)
tren(S('B08') - .3, W('B08', 'ertesi'), bpm=128, v=.26)
ak('F2 C3 F3 A3 C4', W('B08', 'ertesi'), 4, .36)
# C · Arles: daha aydınlık; "sarı"da yüksek motif; "Sensiz" uzun akor; Gauguin hareket; iki zarf yankısı
arpej(AK_PARLAK, S('C01') - .2, S('C04'), bpm=80, v=.24)
dizi(oktav(ZARF), W('C04', 'sarı'), bpm=84, v=.3, pan=.3)
arpej(AK_PARLAK, S('C04') + 2, S('C07'), bpm=80, v=.24)
for i in range(10): nota(['C6', 'A5', 'F6', 'G5', 'E6'][i % 5], S('C05') + .3 + i * .5, .6, .14, .4)   # yıldızlar
ak('A#2 F3 A3 D4', W('C07', 'sensiz'), 5, .4)
dizi(ZARF, S('C08') + .4, bpm=70, v=.3, pan=.25)
arpej(AK_PARLAK, S('C09') - .2, S('C10') + 3.4, bpm=92, v=.26)
dizi([('A4', .5), ('C5', .5), ('F5', 1)], S('C10') + .4, bpm=80, v=.3, pan=-.3); dizi([('A4', .5), ('C5', .5), ('F5', 1)], S('C10') + .9, bpm=80, v=.3, pan=.3)
# D · nişan (sıcak), telgraf (müzik iner), gece treni (hızlı), biletler (sessize yakın), evlilik, ilk sarı zarflar
arpej(AK_F, S('D01') - .2, S('D02'), bpm=66, v=.24)
dizi(ZARF, W('D01', 'nişanlanır') - 1.6, bpm=66, v=.3, pan=.25)
tremolo('D2', 'C#2', W('D02', 'ertesi'), S('D03'), hiz=9, v=.24); tremolo('D4', 'C#4', W('D02', 'ertesi'), S('D03'), hiz=9, v=.2)
tren(S('D03') - .2, S('D04'), bpm=150, v=.3)
ak('D3 F3 A3', S('D04') + .2, 3, .22)
arpej(AK_F, S('D06') - .3, S('D07'), bpm=72, v=.24)
dron('F2 C3', S('D07'), E('D07') + 1, .22)
dizi(oktav(ZARF), W('D07', 'sarı') - .2, bpm=80, v=.32, pan=.3); dizi(oktav(ZARF), W('D07', 'kabarır') - .4, bpm=84, v=.26, pan=.35)
# E · Saint-Rémy: armonyum dronu, seyrek yüksek notalar; üç tablo sözcüğünde üç akor
dron('A2 E3', S('E01') - .3, S('E03'), .3)
for i in range(12): nota(['E5', 'A5', 'B5', 'E6'][i % 4], S('E01') + .8 + i * 1.6, .9, .16, .3)
for w, a_ in (('selviler', 'A2 E3 A3 C#4 E4'), ('buğday', 'F#2 C#3 F#3 A3 C#4'), ('yıldızlı', 'D2 A2 D3 F#3 A3')): ak(a_, W('E03', w), 2.2, .4)
ak('E2 B2 E3 G#3 B3', W('E03', 'yüz'), 3, .36)
arpej(AK_F, S('E04') - .2, E('E04') + 1, bpm=74, v=.22)
# F · badem: köşe (ninni), dergi, doğum (ninni), RENK DORUĞU, "hastalandım"da minör, satış, defter, on tablo
dizi(NINNI, S('F01'), bpm=84, v=.22, pan=.35)
arpej(AK_F, S('F02') - .2, S('F03'), bpm=76, v=.24)
dizi(NINNI, S('F03') + .5, bpm=72, v=.26, pan=.35); dizi(NINNI, W('F03', 'vincent') - .2, bpm=72, v=.2, pan=.4)
dron('F2 C3 F3 A3', S('F04') - .3, E('F04') + 1.5, .38, g=1.1)
arpej(AK_PARLAK, S('F04') - .2, E('F04') + 1, bpm=84, v=.34)
dizi(oktav(ZARF), S('F04') + .4, bpm=60, v=.4, pan=.25); dizi(ZARF, W('F04', 'mavi') - .2, bpm=60, v=.34, pan=.1)
ak('F2 C3 A3 C4 F4 A4', W('F04', 'büyük') - .1, 5, .45)
arpej([('D3 F3 A3', 2), ('A#2 D3 F3', 2)], S('F05'), W('F05', 'hastalandım'), bpm=66, v=.22)
ak('D2 A2 D3 F3', W('F05', 'hastalandım'), 4, .34)
arpej(AK_F, S('F06') - .2, S('F08') + 4, bpm=74, v=.22)
dizi(ZARF, W('F06', 'dört') - .1, bpm=74, v=.3, pan=.25)
# G · Auvers: ninni (amca, beşik), tarla (geniş), gerilim (armonyum), tarlalar (kabaran), taslak, eşleme motifi, SESSİZLİK, Theo
dizi(NINNI, S('G01') + .3, bpm=72, v=.24, pan=.35)
arpej(AK_F, S('G02') - .2, S('G05'), bpm=70, v=.22)
dizi(ZARF, W('G02', 'şaka') - .3, bpm=84, v=.24, pan=.2)
dron('D2 G#2 D3', S('G05'), S('G06'), .26, g=.9)
tremolo('A2', 'A#2', W('G05', 'gergin') - .5, S('G06'), hiz=6, v=.2)
dron('F2 C3', S('G06') - .2, E('G06') + .5, .3)
arpej(AK_PARLAK, W('G06', 'tarlaları') - 1, E('G06') + 1, bpm=78, v=.3)
ak('F2 C3 F3 A3 C4 F4', W('G06', 'tarlaları'), 5, .42)
for i, n in enumerate(['C5', 'A4', 'F4', '-', 'C5', 'D5']): nota(n, S('G07') + .5 + i * 1.1, 1.2, .2, .3) if n != '-' else None
dizi(ZARF, S('G08') + .2, bpm=64, v=.34, pan=.25)
ak('A#2 F3 D4 F4', W('G08', 'payın'), 3, .34)
ak('D3 A3 D4', S('G09') + .2, 3.5, .22)
SUS.append((W('G09', 'öldü'), S('G10') - .2))                     # olay anı: müzik yok, yalnız rüzgâr
dizi(ZARF_MIN, S('G10') + .1, bpm=54, v=.28, pan=.2)
ak('D2 A2 F3', W('G10', 'ah') - .1, 4, .3)
dizi(ZARF_MIN, S('G11') + .2, bpm=50, v=.22, pan=.2)
SUS.append((E('G11') + .2, S('H01') - .4))
# H · Jo: tren (gündüz, yumuşak), sergi, defter, motif (saklar), 1905 kabarma, üç cilt, tarla, çeviri, müze (motif tam)
tren(S('H01') - .3, S('H02'), bpm=112, v=.18, kok='F2'); dron('A3 C4 F4', S('H01'), S('H02'), .2)
dizi(ZARF, S('H01') + 2, bpm=70, v=.24, pan=.25)
arpej(AK_F, S('H02') - .2, S('H04'), bpm=78, v=.22)
dizi(ZARF, S('H04') + .1, bpm=70, v=.32, pan=.25)
dron('F2 C3 A3', S('H05') - .3, E('H05') + 1, .3)
arpej(AK_PARLAK, S('H05'), E('H06'), bpm=78, v=.26)
dizi(oktav(ZARF), W('H05', 'gelmiş'), bpm=70, v=.32, pan=.3)
arpej([('F3 A3 C4', 2), ('D3 F3 A3', 2)], S('H07') - .2, S('H09'), bpm=62, v=.2)
dizi(ZARF, S('H09') + .2, bpm=62, v=.24, pan=.2)
dron('F2 C3', S('H10') - .3, E('H10') + 2, .32)
arpej(AK_PARLAK, S('H10') - .2, E('H10') + 1.5, bpm=72, v=.28)
dizi(oktav(ZARF), W('H10', 'bugün') - .1, bpm=64, v=.38, pan=.25)
ak('F2 C3 A3 C4 F4', W('H10', 'müzede') - .2, 5, .4)
# I · cevap: motif (Theo), motif üstte (Jo), soru (asılı), bitiş: motif ve uzun fa akoru
dizi(ZARF, S('I01') + .2, bpm=70, v=.32, pan=.2)
arpej(AK_F, S('I01'), S('I03'), bpm=70, v=.24)
dizi(oktav(ZARF), S('I02') + .3, bpm=70, v=.3, pan=.3)
ak('D3 A3 C4 E4 A4', S('I03') + .2, 4.5, .32); dron('A3 E4', S('I03'), S('I04'), .14)
arpej(AK_PARLAK, S('I04') - .3, DUR - 4, bpm=66, v=.24)
dizi(oktav(ZARF), S('I04') + 1, bpm=60, v=.32, pan=.25); dizi(ZARF, S('I04') + 9, bpm=56, v=.28, pan=.2)
ak('F2 C3 A3 C4 F4', DUR - 9, 8, .38)

# boşluk dolguları (düzey eğrisinde −60 dB altı kalan bilinçsiz aralıklar)
dron('F2 C3', S('C05') - .3, S('C08') + .5, .2); dron('C4 F4', S('C08') + 3, S('C09'), .16)
arpej([('D3 F3 A3', 2), ('A#2 D3 F3', 2)], S('D04') + 2, S('D06'), bpm=64, v=.2)
dron('F2 C3', S('G01') - 1.5, S('G02') + 1, .2)
dron('F2 C3', S('G07') - .3, S('G08') + .5, .2)
dron('F2 A2 C3', S('H09') - .3, S('H10'), .22)
dron('F2 C3', E('E04') + .5, S('F02'), .18)
# ── son: sessizlikler, yumuşak sınır, normalize ──
for a, b in SUS:
    i0, i1 = int(a * SR), int(b * SR); f = int(.6 * SR)
    L[i0:i0 + f] *= np.linspace(1, 0, min(f, N - i0)).astype(np.float32)[:len(L[i0:i0 + f])]; R[i0:i0 + f] *= np.linspace(1, 0, min(f, N - i0)).astype(np.float32)[:len(R[i0:i0 + f])]
    L[i0 + f:i1] = 0; R[i0 + f:i1] = 0
X = np.stack([L, R], 1); pk = np.max(np.abs(X)) + 1e-9; X = X / pk * .5
fo = int(3 * SR); X[-fo:] *= np.linspace(1, 0, fo)[:, None]
with wave.open(str(HERE / 'music.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(X, -1, 1) * 32767).astype(np.int16).tobytes())
print('music.wav', round(DUR, 1), 'sn')
