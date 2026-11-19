#!/usr/bin/env python3
"""DORIAN GRAY (Zaman Kuryesi): özgün eşlik, yalnız numpy ile sentez (örnek ses yok, indirme yok, ücretli üretim yok).
Çalgılar mary-stuart/audio/score.py'deki kendi sentezimiz: piyano (eğik tel kısmileri, çekiç gürültüsü), armonyum, alçak tremolo.
Ezgiler bu dosyada yazıldı; bilinen bir dönem ezgisi kullanılmadı:
  PORTRE: si minör, yüksek "müzik kutusu" motifi (tablo). Tablo değiştikçe aynı beş nota bozulur (fa doğal, do doğal: triton).
  VALS: re majör, 3/4 salon valsi (Dorian'ın gençliği, Londra salonları); yıllar geçince si minöre ve yavaşa döner.
  SIBYL: la majör, sahne şarkısı gibi ince ezgi; Sibyl kötü oynadığı gece yarıda kalır.
  HENRY: armonyumda alçak, kromatik inen dört nota (etki).
Her olay bir cümleye ya da sözcüğe bağlı (timeline.js). E09 ile G09 sonrasında müzik susar.
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
rng = np.random.default_rng(1890)

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
PORTRE = [('B5', .5), ('F#5', .5), ('D6', .5), ('C#6', .5), ('B5', 2)]
PORTRE_BOZUK = [('B5', .5), ('F5', .5), ('D6', .5), ('C6', .5), ('B5', 2)]
VALS = [('F#5', 1), ('A5', 1), ('D6', 1), ('C#6', 2), ('B5', 1), ('A5', 2), ('F#5', 1), ('G5', 1), ('B5', 1), ('E5', 1), ('F#5', 3),
        ('F#5', 1), ('A5', 1), ('D6', 1), ('E6', 2), ('D6', 1), ('C#6', 1), ('B5', 1), ('A5', 1), ('G5', 1), ('E5', 1), ('C#5', 1), ('D5', 3)]
VALS_AK = ['D2 A3+D4+F#4', 'D2 A3+D4+F#4', 'G2 B3+D4+G4', 'A2 A3+C#4+E4', 'D2 A3+D4+F#4', 'B1 B3+D4+F#4', 'E2 G3+B3+E4', 'A2 A3+C#4+G4']
VALS_MIN = [(n.replace('F#5', 'F#5').replace('C#6', 'C6').replace('A5', 'A5'), d) for n, d in VALS]
VALS_MIN_AK = ['B1 F#3+B3+D4', 'B1 F#3+B3+D4', 'E2 G3+B3+E4', 'F#2 F#3+A#3+C#4', 'B1 F#3+B3+D4', 'G1 G3+B3+D4', 'C#2 E3+G3+C#4', 'F#2 F#3+A#3+E4']
SIBYL = [('E5', 1), ('A5', 1), ('B5', .5), ('C#6', .5), ('B5', 1), ('A5', 1), ('F#5', 2), ('E5', 1), ('D5', .5), ('C#5', .5), ('E5', 1), ('A4', 3)]
SIBYL_AK = [('A2 E3 A3 C#4', 4), ('D3 A3 D4 F#4', 4), ('A2 E3 A3 C#4', 2), ('E2 B2 E3 G#3', 2), ('A2 E3 A3 C#4', 4)]
HENRY = [('D3', 1), ('C#3', 1), ('C3', 1), ('B2', 2)]
def vals_bas(akor, t0, t1, bpm=84, v=.36, g=1.0):
    t = t0; b = 60 / bpm; i = 0
    while t < t1 - .1:
        kok, ust = akor[i % len(akor)].split(); nota(kok, t, b, v, -.1, g); nota(ust, t + b, b * .5, v * .6, .05, g); nota(ust, t + 2 * b, b * .5, v * .6, .05, g); t += 3 * b; i += 1
    return t
def kutu(seq, t, bpm=88, v=.32, pan=.3): return dizi([(n.replace('5', '6').replace('6', '6') if False else n, d) for n, d in seq], t, bpm=bpm, v=v, pan=pan)

# ════════ beste ════════
# A · kanca: alçak si, örtü; "tabloya" sözünde portre motifi; "Biz göreceğiz" asılı akor
dron('B1 F#2', .2, S('A03') + 2, .32)
tremolo('B1', 'C2', S('A02') - .3, S('A03'), hiz=8, v=.22)
dizi(PORTRE, W('A01', 'tabloya'), bpm=96, v=.3, pan=.35)
nota('B2+F#3+D4', W('A01', 'görmeseydi'), 3.5, .35)
dizi(PORTRE, W('A03', 'örtünün') - .2, bpm=80, v=.24, pan=.35)
nota('G2+D3+B3+F#4', W('A03', 'göreceğiz'), 4, .45)
# B · Londra, haziran: vals; Henry'nin etkisi (armonyum); yaşlanacağını anlar → vals durur; dilek
vals_bas(VALS_AK, S('B01') - .3, S('B03'), bpm=84, v=.3)
dizi(VALS, S('B01') + 1.6, bpm=84, v=.36, pan=.15)
dizi(HENRY, S('B03') + .2, bpm=50, v=.42, cal='h')
dron('D3 A3', S('B03'), S('B04'), .22)
arpej([('G2 D3 G3 B3', 4), ('E2 B2 E3 G3', 4), ('A2 E3 A3 C#4', 4), ('D3 A3 D4 F#4', 4)], S('B04') - .2, S('B05') + .5, bpm=66, v=.26)
dizi(VALS[:6], W('B04', 'gençlik') + .3, bpm=70, v=.32, pan=.15)
dizi(HENRY, W('B04', 'gençliğin') if True else 0, bpm=46, v=.36, cal='h')
nota('D3+A3', S('B05'), 3, .3); dizi(PORTRE, W('B05', 'bitmiş'), bpm=84, v=.3, pan=.35)
nota('B2+F#3+C4', W('B05', 'yaşlanacağını'), 4, .45)   # vals susar, çözülmeyen akor
dron('B2 F#3', S('B06') - .2, E('B06') + .6, .32, g=1.0)
nota('D5+F#5', W('B06', 'kalsam'), 2, .2, .3); nota('C5+F#5', W('B06', 'yaşlansa'), 2, .2, .3)
vurus('B1+F#2', W('B06', 'ruhumu'), .55)
dizi(PORTRE_BOZUK, W('B06', 'ruhumu') + .5, bpm=70, v=.2, pan=.35)
dron('B2 D3 F#3', S('B07'), E('B07'), .2)
tremolo('F#2', 'G2', S('B08'), W('B08', 'cinayet'), hiz=12, v=.36)
nota('B1+F2+B2', W('B08', 'cinayet'), 3, .6)
# C · Sibyl: tiyatro şarkısı; kötü oynar (yarıda kalır); "Aşkımı öldürdün"; zalimlik çizgisi; dilek tuttu
arpej(SIBYL_AK, S('C01') + .5, S('C03'), bpm=72, v=.24); dizi(SIBYL, S('C01') + 2.2, bpm=72, v=.36, pan=.1)
dizi(SIBYL[:6], S('C02') + .4, bpm=72, v=.3, pan=.1)
dizi(SIBYL[:4] + [('-', 1), ('B5', .5), ('-', 1.5), ('A5', 1)], S('C03') + .3, bpm=60, v=.26, pan=.1)   # bocalayan şarkı
dron('A2 E3', S('C04'), S('C05'), .2); nota('A3+C#4+E4', W('C04', 'gerçekten'), 3, .25)
vurus('F#1+C2+F#2', W('C05', 'aşkımı'), .6)
dron('B1 F#2', S('C06'), S('C10') - .5, .3); tremolo('B1', 'C2', S('C06'), S('C09'), hiz=6, v=.2)
dizi(PORTRE_BOZUK, W('C07', 'zalimlik'), bpm=80, v=.32, pan=.35)
nota('B4+C5', W('C07', 'zalimlik') + .3, 3, .2, .3)
nota('B3+D4+F#4', S('C08') + .3, 3, .2)
vurus('B1+B2', W('C09', 'tutmuştu'), .6)
dron('E2 B2', S('C10'), S('C12') - .2, .2); dizi(SIBYL[:4], W('C10', 'mektup'), bpm=60, v=.24, pan=.1)
nota('E2+B2+G3', W('C10', 'haberle'), 4, .4)
dizi(HENRY, S('C11'), bpm=48, v=.36, cal='h'); dizi([(n.replace('C#', 'C'), d) for n, d in SIBYL[:6]], S('C11') + 2, bpm=60, v=.22, pan=.2)
# opera: kısa parlak salon akoru, sonra örtü ve kilit: aşağı inen portre motifi
arpej([('D3 A3 D4 F#4', 2), ('G2 D3 B3 G4', 2)], S('C12') - .1, S('C13'), bpm=96, v=.32)
nota('D4+F#4+A4+D5', S('C12') + .1, 2.5, .3, .2)
dron('B1 F#2 D3', S('C13'), E('C13') + 1, .26)
dizi([(n, d) for n, d in reversed(PORTRE)], W('C13', 'örtü'), bpm=70, v=.26, pan=.35)
nota('B2+F#3', W('C13', 'kilitler'), 3, .4)
# D · yıllar: vals si minörde ve yavaş; sarı kitap (Henry); ayna; "keyif verir"
vals_bas(VALS_MIN_AK, S('D01') - .3, E('D02') + .4, bpm=72, v=.28)
dizi(VALS_MIN, S('D01') + 1.5, bpm=72, v=.32, pan=.15)
dizi(HENRY, W('D01', 'sarı'), bpm=44, v=.32, cal='h')
dron('B2 F#3', S('D03'), E('D05') + .5, .22)
dizi(PORTRE_BOZUK, W('D03', 'aynayla'), bpm=80, v=.28, pan=.35); dizi(PORTRE, W('D03', 'aynayla') + 2.6, bpm=80, v=.24, pan=-.3)
nota('G4+B4+D5', W('D04', 'keyif'), 2.5, .26, .2)
nota('B2+D3+F3', W('D05', 'bedeli'), 3.5, .35)
# E · Basil'in son gecesi: sis; "Gel. Sana ruhumu göstereyim."; yukarı; perde; nefret; bıçak; susar
dron('B1 C2', S('E01'), S('E03'), .3); tremolo('B1', 'C2', S('E02'), S('E03'), hiz=5, v=.18)
dizi([('F#4', 1), ('E4', 1), ('D4', 2)], W('E02', 'günah'), bpm=60, v=.26, pan=-.1)
nota('C3+F#3+B3', W('E03', 'gel'), 3, .42)
tremolo('B1', 'F2', S('E04'), S('E05'), hiz=6, v=.22)
vurus('B1+F2+C3', W('E05', 'koparıp'), .65)
dizi(PORTRE_BOZUK, W('E05', 'tablosunu'), bpm=70, v=.3, pan=.35); nota('B2+C3+F3', W('E05', 'imzayı'), 4, .4)
dron('B2 D3 F#3', S('E06'), E('E06') + .5, .24); nota('D4+F#4+B4', W('E06', 'hiçbir'), 3, .22)
tremolo('B1', 'C2', S('E07'), S('E09'), hiz=10, v=.34); tremolo('F2', 'F#2', W('E07', 'nefret'), S('E09'), hiz=14, v=.28)
nota('B5+C6', W('E08', 'bıçak'), 1.5, .18, .4)
vurus('B1+C2+F2+B2', W('E09', 'öldürür'), .5)
sus_a = (W('E09', 'öldürür') + 1.2, S('E10') + .3)
dron('B1 F#2', S('E10') + .3, E('E10') + .8, .2)
# F · iyi olma kararı; "Sana Basil'i ben öldürdüm desem?"; kitap; Henry güler; keşke
arpej([('D3 A3 D4', 4), ('G2 D3 G3 B3', 4), ('E2 B2 E3 G3', 4), ('A2 E3 A3 C#4', 4)], S('F01'), E('F01'), bpm=60, v=.22)
dizi(SIBYL[:6], S('F01') + 2, bpm=60, v=.24, pan=.1)
nota('B2+F3', W('F02', 'öldürdüm'), 3, .4); dizi(HENRY, W('F02', 'güler'), bpm=56, v=.3, cal='h')
dizi(HENRY, S('F03'), bpm=44, v=.34, cal='h'); dron('D3 A3', S('F04'), E('F04'), .2)
arpej([('B2 F#3 B3 D4', 4), ('G2 D3 G3 B3', 4), ('E2 B2 E3 G3', 4), ('F#2 C#3 F#3 A#3', 4)], S('F05'), E('F05') + 1.5, bpm=56, v=.24)
dizi(VALS_MIN[:6], S('F05') + 1, bpm=56, v=.28, pan=.15)
# G · son gece: ayna; suçu dağıtır; yukarı; ikiyüzlülük; vicdan; bıçak → susar; çığlık sessizlikte; genç portre; yüzükler
dron('B1 F#2', S('G01'), E('G02'), .26)
dizi(PORTRE, W('G01', 'aynaya'), bpm=80, v=.26, pan=.35); nota('B3+D4+F4', W('G01', 'lanetti'), 3, .3)
tremolo('B1', 'C2', S('G02'), E('G02'), hiz=4, v=.16)
nota('D3+F#3+A3', S('G03'), 3, .24); tremolo('B1', 'F#2', W('G03', 'lambayı'), S('G04'), hiz=6, v=.2)
dizi(PORTRE_BOZUK, W('G04', 'perdeyi') + .3, bpm=70, v=.32, pan=.35); nota('B2+C3+F3', W('G04', 'ikiyüzlülüğün'), 4, .38)
dron('B1 F2', S('G05'), E('G06'), .22)
nota('F#3+B3', W('G06', 'güler'), 1.5, .2)
tremolo('B1', 'C2', S('G07'), S('G08'), hiz=8, v=.28); tremolo('F2', 'F#2', W('G07', 'vicdandı'), S('G08'), hiz=14, v=.32)
vurus('B1+C2+F2+B2', W('G08', 'saplar'), .55)
sus_b = (W('G08', 'saplar') + 1.4, S('G10') - .2)
dizi(PORTRE, S('G10') + .2, bpm=72, v=.3, pan=.35); nota('D4+F#4+B4', W('G10', 'genç'), 4, .24, .2)
dron('B1 F#2', S('G11'), E('G11') + 1, .26); nota('B2+D3+F3', W('G11', 'yüzüklerinden'), 4, .32)
# G12–G15 · 1895: belgesel; ağır piyano, mahkeme; bedeli yazar ödedi; mektup
arpej([('B2 F#3 B3 D4', 4), ('G2 D3 G3 B3', 4), ('D3 A3 D4 F#4', 4), ('F#2 C#3 F#3 A#3', 4)], S('G12') - .3, E('G13'), bpm=58, v=.22)
dizi(HENRY, S('G12') + 3, bpm=44, v=.26, cal='h')
nota('B2+F#3', W('G13', 'ahlaklı'), 3, .3)
dron('B1 F#2 B2', S('G14'), E('G14') + .6, .28); vurus('B1+B2', W('G14', 'yazar'), .5)
arpej([('D3 A3 D4 F#4', 4), ('B2 F#3 B3 D4', 4), ('G2 D3 G3 B3', 4), ('A2 E3 A3 C#4', 4)], S('G15'), E('G15') + .5, bpm=58, v=.22)
dizi(VALS[:11], S('G15') + 1, bpm=58, v=.28, pan=.15)
# G16–G17 · soru ve iksir: vals geri, portre motifi saf; bitiş ekranı
dron('B2 F#3', S('G16'), S('G17'), .22); dizi(PORTRE, W('G16', 'lanet'), bpm=80, v=.26, pan=.35)
nota('B3+D4+F#4', W('G16', 'yazıldı'), 3.5, .3)
vals_bas(VALS_AK, S('G17') - .3, DUR, bpm=78, v=.26); dizi(VALS, S('G17') + 1.2, bpm=78, v=.34, pan=.15)
dizi(PORTRE, E('G17') + 4, bpm=76, v=.26, pan=.35)

# ── oda yankısı (FFT ile, blok blok) ──
def yanki(x, sure=2.4, kuru=.8, islak=.32):
    n = int(sure * SR); t = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-t / .5); ir[:int(.02 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
    B = 1 << 20; F = 1 << int(np.ceil(np.log2(B + n))); H = np.fft.rfft(ir, F); y = np.zeros(len(x) + n, np.float32)
    for s in range(0, len(x), B):
        seg = x[s:s + B]; c = np.fft.irfft(np.fft.rfft(seg, F) * H, F)[:len(seg) + n]; y[s:s + len(c)] += c.astype(np.float32)
    return x * kuru + y[:len(x)] * islak
L = yanki(L); R = yanki(R)

# ── konuşma altında kısma, iki sessizlik, son ──
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
mask = np.ones(N, np.float32)
for sus0, sus1 in (sus_a, sus_b):
    a, b = int(sus0 * SR), int(sus1 * SR); f = int(.8 * SR); mask[a:b] = 0; mask[a - f:a] *= np.linspace(1, 0, f); mask[b:b + f] *= np.linspace(0, 1, f)
endf = np.ones(N, np.float32); g0 = int((DUR - 5) * SR); endf[g0:] = np.linspace(1, 0, N - g0)
L *= duck * mask * endf; R *= duck * mask * endf
pk = max(np.abs(L).max(), np.abs(R).max()); L /= pk / .7; R /= pk / .7
st = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'music.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print('audio/music.wav', round(DUR, 2), 'sn; sessizlikler', [tuple(round(x, 2) for x in s) for s in (sus_a, sus_b)], '; piyano notası önbelleği', len(_PC))
