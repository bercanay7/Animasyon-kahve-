#!/usr/bin/env python3
"""LALE ÇILGINLIĞI (Zaman Kuryesi): özgün eşlik, yalnız numpy ile sentez (örnek ses yok, indirme yok, ücretli üretim yok).
Çalgılar: kendi sentezimiz. piyano ve armonyum mary-stuart/dorian-gray'den (alçak nota hatası düzeltilmiş: dec = max(.3, …));
yeni: VİRJİNAL (çekilen tel, parlak kısmiler, kısa sönüm; 17. yüzyıl Hollanda ev çalgısı rengi) ve KANUN (mızrap, hafif tel titreşimi; İstanbul rengi).
Ezgiler bu dosyada yazıldı; bilinen bir dönem ezgisi kullanılmadı. Ney ya da dinî çağrışımlı çalgı/dizi yok.
  FLORA: sol majör dans (3/2 havası). Fiyat yükseldikçe hızlanır ve her tekrarda yukarı taşınır (balon); çöküşte tek alçak notayla kesilir.
  FLORA_MIN: aynı ezgi mi minörde ve yavaş (çöküş, efsane).
  LALE (İstanbul): re hicaz renkli ezgi (mi bemol – fa diyez artık ikilisi), kanunda; 1730'da yarıda kalır.
  Sonda iki ezgi aynı anda: virjinalde FLORA, kanunda LALE.
Her olay bir cümleye ya da sözcüğe bağlı (timeline.js). Sessizlikler: E01 başı (alıcı yok) ve H03 sonu.
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

NOTA = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def midi(n):
    m = re.match(r'([A-G])([#b]?)(-?\d)', n); return 12 * (int(m.group(3)) + 1) + NOTA[m.group(1)] + {'#': 1, 'b': -1, '': 0}[m.group(2)]
def hz(m): return 440 * 2 ** ((m - 69) / 12)

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
_VC = {}
def virjinal(m, v=.6, d=1.0):
    """çekilen tel: parlak kısmiler (tüy kalemin çektiği nokta: 1/7), hızlı sönüm, kısa 'tık'"""
    key = (m, round(v * 4) / 4, round(min(d, 3) * 4) / 4)
    if key in _VC: return _VC[key]
    f0 = hz(m); n = int((key[2] + .6) * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for k in range(1, 18):
        fk = f0 * k * (1 + .00012 * k * k)
        if fk > 11000: break
        a = abs(np.sin(np.pi * k / 7)) / k ** .9
        dec = max(.6, 1.2 + .04 * (m - 55)) * (1 + k * .22)
        s += a * np.sin(2 * np.pi * fk * t + k * .7) * np.exp(-t * dec)
    tik = rng.standard_normal(int(.006 * SR)) * np.exp(-np.arange(int(.006 * SR)) / 40) * .25; s[:len(tik)] += tik
    rel = np.ones(n); r0 = int(key[2] * SR); rel[r0:] = np.exp(-np.arange(n - r0) / (.05 * SR))
    s *= rel * key[1]; s[:32] *= np.linspace(0, 1, 32)
    _VC[key] = (s / 3.0).astype(np.float32); return _VC[key]
_KC = {}
def kanun(m, v=.6, d=1.2):
    """mızraplı tel: sıcak, orta parlak; hafif başlangıç perde kayması ve tel titreşimi"""
    key = (m, round(v * 4) / 4, round(min(d, 3) * 4) / 4)
    if key in _KC: return _KC[key]
    f0 = hz(m); n = int((key[2] + .9) * SR); t = np.arange(n) / SR; s = np.zeros(n)
    bend = 1 + .004 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f0 * bend) / SR
    for k in range(1, 12):
        a = abs(np.sin(np.pi * k / 4.3)) / k ** 1.1
        dec = max(.5, .9 + .03 * (m - 57)) * (1 + k * .35)
        s += a * np.sin(k * ph * (1 + .0003 * k) + k) * np.exp(-t * dec)
    s *= (1 + .04 * np.sin(2 * np.pi * 5.2 * t) * (1 - np.exp(-t * 3)))
    tik = rng.standard_normal(int(.004 * SR)) * np.exp(-np.arange(int(.004 * SR)) / 30) * .2; s[:len(tik)] += tik
    rel = np.ones(n); r0 = int(key[2] * SR); rel[r0:] = np.exp(-np.arange(n - r0) / (.12 * SR))
    s *= rel * key[1]; s[:32] *= np.linspace(0, 1, 32)
    _KC[key] = (s / 2.8).astype(np.float32); return _KC[key]
_HC = {}
def armonyum(m, d, v=.5):
    key = (m, round(d * 4) / 4, round(v * 4) / 4)
    if key in _HC: return _HC[key]
    f0 = hz(m); n = int((key[1] + .8) * SR); t = np.arange(n) / SR
    s = sum((1 / k) * np.sin(2 * np.pi * f0 * k * t * (1 + .0015 * np.sin(2 * np.pi * 5.5 * t))) for k in (1, 2, 3, 4, 6)) + .3 * np.sin(2 * np.pi * f0 * .5 * t)
    e = np.minimum(1, t / .45) * np.where(t > key[1], np.exp(-(t - key[1]) / .25), 1)
    _HC[key] = (s * e * key[2] * .22 * (1 + .08 * np.sin(2 * np.pi * 4.8 * t))).astype(np.float32); return _HC[key]

CAL = {'p': piyano, 'v': virjinal, 'k': kanun}
def tr(n, st):   # aktar: st yarım ses
    return '+'.join('-' if x == '-' else _ad(midi(x) + st) for x in n.split('+'))
_AD = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']
def _ad(m): return _AD[m % 12] + str(m // 12 - 1)
def nota(n, t, d=1.0, v=.7, pan=0.0, g=1.0, cal='p'):
    for x in n.split('+'):
        if x == '-' or not x: continue
        m = midi(x)
        sig = armonyum(m, d, v) if cal == 'h' else CAL[cal](m, v, d)
        put(sig, t, pan + (m - 62) * .006, g)
def dizi(seq, t0, bpm=66, v=.7, pan=0.0, g=1.0, cal='p', leg=1.1, st=0, t1=None):
    t = t0; b = 60 / bpm
    for n, d in seq:
        if t >= DUR or (t1 and t >= t1): break
        if n != '-': nota(tr(n, st) if st else n, t, d * b * leg, v, pan, g, cal)
        t += d * b
    return t
def arpej(akorlar, t0, t1, bpm=66, v=.4, pan=-.15, g=1.0, desen=(0, 1, 2, 1), cal='p', st=0):
    t = t0; b = 60 / bpm; i = 0
    while t < t1:
        ak, vu = akorlar[i % len(akorlar)]; ns = ak.split(); k = 0
        for j in range(int(vu * 2)):
            if t >= t1: break
            n = ns[desen[k % len(desen)] % len(ns)]; nota(tr(n, st) if st else n, t, b * .9, v * (1.1 if j == 0 else .85), pan, g, cal); t += b / 2; k += 1
        i += 1
    return t
def dron(notalar, t0, t1, v=.5, g=1.0, pan=0.0):
    d = t1 - t0
    if d <= 0: return
    for n in notalar.split(): put(armonyum(midi(n), d, v), t0, pan, g)
def tremolo(a, b, t0, t1, hiz=12, v=.4, g=1.0, cal='p'):
    t = t0; k = 0
    while t < t1:
        u = (t - t0) / max(.1, t1 - t0); nota(a if k % 2 == 0 else b, t, .2, v * (.6 + .4 * u), -.2, g, cal); t += 1 / hiz; k += 1
def vurus(n, t, v=.9, g=1.0, cal='p'): nota(n, t, 3.0, v, 0, g, cal)

# ── temalar ──
FLORA = [('G4', 1), ('B4', .5), ('C5', .5), ('D5', 1), ('G5', 1), ('F#5', .5), ('E5', .5), ('D5', 1), ('B4', 1), ('C5', .5), ('A4', .5), ('B4', 1), ('G4', 2),
         ('D5', 1), ('E5', .5), ('F#5', .5), ('G5', 1), ('A5', 1), ('B5', .5), ('A5', .5), ('G5', 1), ('F#5', 1), ('E5', .5), ('C5', .5), ('D5', 1), ('G4', 2)]
FLORA_AK = [('G2 D3 G3 B3', 3), ('C3 G3 C4 E4', 3), ('D3 A3 D4 F#4', 3), ('G2 D3 G3 B3', 3)]
FLORA_MIN = [(n.replace('B4', 'Bb4').replace('B5', 'Bb5').replace('F#5', 'F5').replace('E5', 'Eb5'), d) for n, d in FLORA]
FLORA_MIN_AK = [('G2 D3 G3 Bb3', 4), ('Eb3 Bb3 Eb4 G4', 4), ('C3 G3 C4 Eb4', 4), ('D3 A3 D4 F#4', 4)]
LALE = [('D5', 1), ('Eb5', .5), ('F#5', .5), ('G5', 1), ('A5', 1.5), ('G5', .5), ('F#5', .5), ('Eb5', .5), ('F#5', 1), ('D5', 2),
        ('A5', 1), ('Bb5', .5), ('A5', .5), ('G5', 1), ('F#5', 1), ('Eb5', .5), ('D5', .5), ('C5', .5), ('D5', 2.5)]
LALE_AK = [('D3 A3 D4', 4), ('C3 G3 C4', 2), ('D3 A3 D4', 2), ('G2 D3 G3', 2), ('D3 A3 D4', 2)]

# ════════ beste ════════
# 0 · KANCA: terazi (tek virjinal notası, sorgulayan), mezat salonu (FLORA canlı), İstanbul (kanun), soru
nota('G4', S('A01') + .1, 1.2, .45, cal='v'); nota('A4+D5', W('A01', 'alır'), 1.4, .38, cal='v')
nota('G3+D4', S('A02') + .2, 1.8, .35, cal='v')
arpej(FLORA_AK, S('A03') - .1, S('A06') - .2, bpm=96, v=.24, cal='v'); dizi(FLORA, S('A03') + .5, bpm=96, v=.32, pan=.15, cal='v', t1=S('A06') - .3)
vurus('G2+D3+G3', W('A05', 'beş', 1), .45)
dron('D2 A2', S('A06'), S('A07'), .26)
dizi(LALE[:10], S('A06') + .6, bpm=72, v=.34, pan=.1, cal='k')
tremolo('D2', 'Eb2', W('A06', 'patrona'), S('A07'), hiz=8, v=.22)
nota('D3+A3+Eb4', W('A07', 'lale'), 3, .3, cal='k'); nota('G3+Bb3+D4', W('A07', 'kim'), 3, .36)
# I · YOL: kış, elçi: kanun ince, dron; Leiden: virjinal FLORA ilk kez sakin; hırsız: alçak
dron('D2 A2', S('B01') - .3, S('B05'), .2)
dizi(LALE, S('B01') + 1.2, bpm=66, v=.3, pan=.15, cal='k', t1=S('B04'))
nota('D4+A4', W('B03', 'tülbendin'), 2, .24, cal='k')
arpej([('G2 D3 G3 B3', 4), ('D3 A3 D4 F#4', 4)], S('B05'), S('B06'), bpm=76, v=.2, cal='v'); dizi(FLORA[:13], S('B05') + 1.5, bpm=76, v=.28, pan=.15, cal='v', t1=S('B06'))
tremolo('G2', 'Ab2', S('B06'), E('B06'), hiz=6, v=.2); nota('G2+D3', W('B06', 'çalınıyor'), 2.5, .35)
# II · ALEV: kırık lale: virjinal, kırılma anında yarım ses kayması; Semper Augustus: aynalar (yankılı tekrar)
arpej(FLORA_AK, S('C01') - .2, S('C03'), bpm=80, v=.22, cal='v'); dizi(FLORA, S('C01') + 1, bpm=80, v=.3, pan=.15, cal='v', t1=S('C02') + 1.5)
nota('G5+Ab5', W('C02', 'kırılacağını'), 1.5, .3, .3, cal='v')
dron('G2 D3', S('C03'), S('C05'), .2); nota('Bb4+D5', W('C03', 'virüsün'), 2.5, .26, cal='p'); nota('G3+Bb3+Eb4', W('C03', 'hastaydı'), 3, .3)
for k in range(3): dizi(FLORA[:5], S('C05') + 1 + k * 1.6, bpm=96, v=.26 - k * .06, pan=(-.4, .4, 0)[k], cal='v', st=12 * (k == 2))
nota('G4+B4+D5', W('C05', 'satmıyor'), 2, .3, cal='v'); nota('G4+C5+E5', W('C06', 'satmıyor'), 2, .3, cal='v')
# III · RÜZGÂR TİCARETİ: balon. Her bölümde FLORA hızlanır ve yarım/tam ses yukarı taşınır
t = S('D01') - .2
for i, (bpm, st, t1) in enumerate([(84, 0, S('D03')), (100, 2, S('D05')), (116, 4, S('D06')), (138, 7, S('D07'))]):
    arpej(FLORA_AK, t, t1, bpm=bpm, v=.2 + i * .03, cal='v', st=st); dizi(FLORA, t + .3, bpm=bpm, v=.28 + i * .03, pan=.15, cal='v', st=st, t1=t1); t = t1
arpej(FLORA_AK, S('D07') - .1, S('D09'), bpm=120, v=.28, cal='v', st=5); dizi(FLORA, S('D07') + .3, bpm=120, v=.36, pan=.15, cal='v', st=5, t1=S('D09'))
vurus('C3+G3+C4', W('D08', 'doksan'), .4, cal='p')
nota('C4+E4+A4', S('D09') + .2, 2.5, .3, cal='p'); nota('B3+D4+G4', W('D09', 'haziranda'), 3, .26)
# IV · ÇÖKÜŞ: "kimse el kaldırmıyor": tek alçak nota, sonra sessizlik; FLORA minörde, yavaş
vurus('G1+G2', W('E01', 'kimse'), .55)
sus_a = (W('E01', 'kimse') + 1.6, S('E02') + .2)
dron('G1 D2', S('E02') + .2, S('E05'), .22)
dizi(FLORA_MIN[:13], S('E02') + 1.5, bpm=58, v=.26, pan=.15, cal='p', t1=S('E05'))
tremolo('G2', 'Ab2', S('E05'), S('E06'), hiz=5, v=.2)
nota('C4+Eb4+G4', W('E06', 'yüzde'), 3, .22); dron('G2 D3', S('E07'), E('E07') + 1, .22); nota('G3+Bb3+D4', W('E07', 'bilen'), 3.5, .3)
# V · EFSANE: broşür (virjinal alay), denizci (oyunlu), Mackay (piyano ağır), Goldgar (sakin arpej), tutulmayan söz
arpej(FLORA_MIN_AK, S('F01'), S('F04'), bpm=70, v=.2, cal='v'); dizi(FLORA_MIN, S('F01') + 1, bpm=70, v=.26, pan=.15, cal='v', t1=S('F03') + 2)
nota('G3+Bb3+Eb4', W('F03', 'çılgınlıktı'), 3, .3)
arpej([('C3 G3 C4 E4', 4), ('A2 E3 A3 C4', 4), ('F2 C3 F3 A3', 4), ('G2 D3 G3 B3', 4)], S('F04'), S('F05'), bpm=60, v=.22, cal='p')
dizi([('E5', .5), ('G5', .5), ('C6', 1), ('B5', .5), ('G5', .5), ('E5', 1)], W('F05', 'denizci'), bpm=120, v=.26, pan=.3, cal='v'); nota('C5+F#5', W('F05', 'semper'), 1.2, .3, .3, cal='v')
dizi([('C5', .5), ('E5', .5), ('G5', 1), ('F5', .5), ('D5', .5), ('B4', 1)], S('F06'), bpm=110, v=.22, pan=.3, cal='v')
dron('C2 G2', S('F07'), S('F08'), .2)
arpej([('A2 E3 A3 C4', 4), ('F2 C3 F3 A3', 4), ('C3 G3 C4 E4', 4), ('G2 D3 G3 B3', 4)], S('F08'), S('F11'), bpm=56, v=.2, cal='p')
nota('A3+C4+E4', W('F09', 'bulamıyor'), 3, .26)
nota('D3+F#3+C4', W('F11', 'tutulmayan'), 3.5, .3); nota('G2+D3+B3', W('F11', 'büyüttü'), 4, .3)
# VI · İSTANBUL: kanun LALE ezgisi; çırağan gecesi yumuşak; narh: ölçülü vuruş; tavan dört katı: yukarı taşınır
dron('D2 A2', S('G01') - .3, S('G06'), .22)
arpej(LALE_AK, S('G01'), S('G06'), bpm=72, v=.2, cal='k'); dizi(LALE, S('G01') + 1.5, bpm=72, v=.32, pan=.15, cal='k', t1=S('G03'))
dizi(LALE, S('G03') + .5, bpm=60, v=.28, pan=-.1, cal='k', t1=S('G05'))
nota('D4+Eb4+A4', W('G04', 'nizeyi'), 2.5, .3, cal='k')
for k in range(8): nota('D3', S('G06') + k * 1.2, .5, .26, cal='k')
nota('D3+A3+D4', W('G07', 'sürülecek'), 2.5, .3)
dizi(LALE[:10], S('G08') + .3, bpm=66, v=.28, pan=.15, cal='k', t1=S('G09'))
dizi(LALE[:10], S('G09') + .3, bpm=80, v=.32, pan=.15, cal='k', st=5, t1=E('G09') + 1)
# VII · 1730: alçak tremolo, kalabalık büyür; 1 Ekim: kesik; köşkler: LALE yarıda kalır
dron('D1 A1', S('H01'), S('H03'), .26); tremolo('D2', 'Eb2', S('H02'), S('H03'), hiz=10, v=.3)
vurus('D1+A1+D2', W('H03', 'öldürülüyor'), .5)
sus_b = (W('H03', 'öldürülüyor') + 1.4, S('H04') + .4)
dron('D2 A2', S('H04') + .4, E('H06') + .5, .2)
dizi(LALE[:7] + [('-', 2)], S('H05') + .5, bpm=56, v=.24, pan=.15, cal='k')
nota('D2+A2', W('H06', 'öldürülecek'), 4, .3)
# VIII · AD: gazete 1913 (piyano), "bin altın" (virjinal-kanun karışık ironik), Aktepe (sakin), kitap 2025, etiket düşer
arpej([('G2 D3 G3 Bb3', 4), ('Eb3 Bb3 Eb4 G4', 4), ('C3 G3 C4 Eb4', 4), ('D3 A3 D4 F#4', 4)], S('I02') - .2, S('I04'), bpm=60, v=.2, cal='p')
dizi(LALE[:5], W('I04', 'beş'), bpm=110, v=.3, pan=.2, cal='k', st=12)
nota('D3+Ab3+D4', W('I05', 'bulamadığını'), 3, .3)
arpej([('D3 A3 D4 F#4', 4), ('G2 D3 G3 B3', 4), ('A2 E3 A3 C#4', 4), ('D3 A3 D4 F#4', 4)], S('I06'), S('I07'), bpm=60, v=.2, cal='p')
dron('D2 A2', S('I07'), E('I08'), .2); nota('D3+A3+F#4', W('I07', 'lale'), 3.5, .32)
dizi(LALE, S('I08') + .5, bpm=64, v=.26, pan=-.1, cal='k', t1=E('I08'))
# IX · SON: iki ezgi aynı anda (virjinal FLORA + kanun LALE), soru, bitiş ekranı
dron('G2 D3', S('J02'), S('J04'), .2)
dizi(FLORA[:13], S('J02') + .3, bpm=72, v=.26, pan=-.25, cal='v', t1=S('J04'))
dizi([(tr(n, -7), d) for n, d in LALE[:10]], S('J02') + 1.4, bpm=72, v=.24, pan=.3, cal='k', t1=S('J04'))
nota('G4', S('J04') + .1, 1.2, .4, cal='v'); nota('A4+D5', W('J04', 'alır'), 1.6, .36, cal='v')
nota('G3+D4+G4', W('J05', 'kim'), 3, .3)
arpej(FLORA_AK, S('J06') - .2, DUR, bpm=84, v=.22, cal='v'); dizi(FLORA, S('J06') + .8, bpm=84, v=.3, pan=-.15, cal='v')
dizi([(tr(n, -7), d) for n, d in LALE], S('J06') + 6, bpm=84, v=.26, pan=.3, cal='k')

# ── oda yankısı ──
def yanki(x, sure=2.0, kuru=.82, islak=.28):
    n = int(sure * SR); t = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-t / .42); ir[:int(.02 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
    B = 1 << 20; F = 1 << int(np.ceil(np.log2(B + n))); H = np.fft.rfft(ir, F); y = np.zeros(len(x) + n, np.float32)
    for s in range(0, len(x), B):
        seg = x[s:s + B]; c = np.fft.irfft(np.fft.rfft(seg, F) * H, F)[:len(seg) + n]; y[s:s + len(c)] += c.astype(np.float32)
    return x * kuru + y[:len(x)] * islak
L = yanki(L); R = yanki(R)
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
    a, b = int(sus0 * SR), int(sus1 * SR); f = int(.6 * SR); mask[a:b] = 0; mask[max(0, a - f):a] *= np.linspace(1, 0, a - max(0, a - f)); mask[b:b + f] *= np.linspace(0, 1, min(f, N - b))
endf = np.ones(N, np.float32); g0 = int((DUR - 4) * SR); endf[g0:] = np.linspace(1, 0, N - g0)
L *= duck * mask * endf; R *= duck * mask * endf
pk = max(np.abs(L).max(), np.abs(R).max()); L /= pk / .7; R /= pk / .7
st_ = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'music.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st_.tobytes())
# düzey eğrisi (Dorian dersi: her müzik üretiminden sonra)
x = (np.abs(L) + np.abs(R)) / 2; sec = int(DUR)
db = np.array([20 * np.log10(np.sqrt(np.mean(x[i * SR:(i + 1) * SR] ** 2)) + 1e-9) for i in range(sec)])
print('audio/music.wav', round(DUR, 2), 'sn; sessizlikler', [tuple(round(v, 2) for v in s) for s in (sus_a, sus_b)])
print('düzey: medyan %.1f dBFS; -60 dB üstü saniye %d / %d' % (np.median(db), (db > -60).sum(), sec))
open(HERE / 'muzik_duzey.txt', 'w').write('\n'.join('%d %.1f' % (i, v) for i, v in enumerate(db)))
