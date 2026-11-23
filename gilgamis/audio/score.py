#!/usr/bin/env python3
"""GILGAMIŞ: özgün müzik, numpy ile sentez (örnek ses yok, indirme yok, ücretli üretim yok).
Çalgılar: lir (Ur lirlerini anımsatan telli; toplamsal sentez), bas dron, çerçeve davul, kil davul (darbuka benzeri tık), rüzgâr.
Ses dizisi: Re Frig (D Eb F G A Bb C). Ağıt motifi: A G F Eb D. Sur motifi (yalnız VII. bölümde tam): D F G A C D.
    python3 audio/score.py  → audio/music.wav (48 kHz stereo, timeline.js DUR) + saniye saniye düzey özeti (Dorian dersi: müzik gerçekten var mı?)
Her vuruş bir cümleye ya da kelimeye bağlı (timeline.js); çizelge değişince yeniden çalıştırmak yeter.
"""
import json, re, wave
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; FILM = HERE.parent
SR = 48000
rng = np.random.default_rng(7)
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

def lir(n, dur=3.0, v=.5, parlak=1.0):
    """Telli lir: harmonikler, yüksekler hızlı söner, hafif uyumsuzluk, çekme gürültüsü."""
    f = hz(n) if isinstance(n, str) else n; t = np.arange(int(dur * SR)) / SR; s = np.zeros_like(t)
    for k in range(1, 9):
        fk = f * k * (1 + .0006 * k * k)
        if fk > 9000: break
        a = (1 / k ** (1.3 / parlak)) * np.exp(-t * (1.6 + .9 * k) / max(.5, dur / 3))
        s += a * np.sin(2 * np.pi * fk * t + rng.random() * 6)
    s += np.exp(-t * 220) * rng.normal(0, .25, len(t))   # tırnak
    env = np.minimum(1, t / .004); return s * env * v * .35

def dron(n, dur, v=.25, acik=.6):
    f = hz(n); t = np.arange(int(dur * SR)) / SR; s = np.zeros_like(t)
    for k in range(1, 7): s += (acik ** k) * np.sin(2 * np.pi * f * k * t * (1 + .0015 * np.sin(.3 * t + k)) + k)
    lfo = .75 + .25 * np.sin(2 * np.pi * .07 * t)
    a = np.minimum(1, t / 2.5) * np.minimum(1, (dur - t) / 2.5)
    return s * lfo * a * v * .3

def davul(v=.6, ton=70):
    t = np.arange(int(.9 * SR)) / SR
    f = ton * (1 + 1.6 * np.exp(-t * 30)); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    s += rng.normal(0, 1, len(t)) * np.exp(-t * 60) * .25; return s * v * .5

def tik(v=.3):
    t = np.arange(int(.15 * SR)) / SR; return (np.sin(2 * np.pi * 380 * t) * np.exp(-t * 60) + rng.normal(0, 1, len(t)) * np.exp(-t * 120) * .4) * v * .3

def ruzgar(dur, v=.15):
    n = int(dur * SR); x = rng.normal(0, 1, n)
    # basit alçak geçiren (birinci derece) + yavaş genlik
    y = np.empty(n); a = .985; acc = 0.0
    for i in range(0, n, 4096):
        seg = x[i:i + 4096]; out = np.empty_like(seg)
        for j, v_ in enumerate(seg): acc = a * acc + (1 - a) * v_; out[j] = acc
        y[i:i + 4096] = out
    t = np.arange(n) / SR
    return y * 8 * (.6 + .4 * np.sin(2 * np.pi * .05 * t)) * np.minimum(1, t / 2) * np.minimum(1, (dur - t) / 2) * v

def motif(t0, notes, aralik=.55, v=.45, pan=0, dur=3.0):
    for k, n in enumerate(notes):
        if n: put(t0 + k * aralik, lir(n, dur, v), pan + (.15 if k % 2 else -.15))

AGIT = ['A4', 'G4', 'F4', 'Eb4', 'D4']
SUR = ['D4', 'F4', 'G4', 'A4', 'C5', 'D5']
ARP = ['D3', 'A3', 'D4', 'F4', 'A3', 'Eb4']

# ---------------------------------------------------------------- A: kanca
put(0.0, dron('D2', S('A03') + 1, .22))
motif(S('A01') + .3, AGIT, .6, .4)
put(W('A01', 'kaptırdı'), lir('Eb5', 2.5, .5, 1.6), -.3)              # yılan: tek uyumsuz tel
put(W('A01', 'kaptırdı') + .05, lir('D5', 2.5, .4, 1.6), .3)
put(S('A02'), dron('A1', Ee('A02') - S('A02') + 1.5, .18, .4))
for k in range(7): put(W('A02', 'altı') + k * .32, tik(.25), .2)           # altı gün yedi gece: yedi tık
put(S('A03'), dron('D2', Ee('A05') - S('A03') + 2, .2))
motif(W('A03', 'çık'), ['D4', 'F4', 'G4', 'A4'], .45, .35, .2)              # sur motifinin yarısı (tamamlanmaz)
put(S('A05'), lir('D3', 5, .4))

# ---------------------------------------------------------------- B: yabani adam (sıcak, akan arpej)
def arpej(t0, t1, notes=ARP, aralik=.42, v=.28, pan=0):
    t = t0; k = 0
    while t < t1: put(t, lir(notes[k % len(notes)], 2.2, v), pan + (.25 if k % 2 else -.25)); t += aralik; k += 1
put(S('B01') - 2, dron('D2', Ee('B11') - S('B01') + 3, .16))
arpej(S('B01'), Ee('B02'), ['D3', 'A3', 'D4', 'A3'], .5, .22)
put(W('B03', 'doğdu'), lir('D5', 3, .45, 1.3))
arpej(S('B04'), Ee('B05'), ['D3', 'A3', 'F4', 'A3', 'G4', 'A3'], .45, .22)
arpej(S('B06'), W('B06', 'kaçtı'), ['F3', 'C4', 'F4', 'A4'], .55, .2)
motif(Ee('B07') - 1, ['A4', 'G4', 'F4'], .5, .3)
arpej(S('B08'), Ee('B09'), ['D3', 'A3', 'D4', 'F4', 'A4', 'F4'], .38, .24)
for k in range(10): put(W('B10', 'boğuştular') + k * .45, davul(.55 if k % 2 == 0 else .35, 65), .1)
put(W('B10', 'sarstılar'), davul(.9, 50))
motif(S('B11') + .3, ['D4', 'F4', 'A4', 'D5'], .5, .35)

# ---------------------------------------------------------------- C: orman (gerilim, davul)
put(S('C01') - 1, dron('D2', Ee('C11') - S('C01') + 2, .2, .7))
arpej(S('C01'), Ee('C01'), ['D3', 'A3', 'Eb4', 'A3'], .48, .2)
for k in range(8): put(S('C02') + k * .9, davul(.5, 55), 0)
arpej(S('C03'), Ee('C04'), ['D3', 'D4', 'A3', 'D4'], .32, .2)
for k in range(int((Ee('C05') - S('C05')) / .25)): put(S('C05') + k * .25, lir(['D6', 'F6', 'A5', 'C6'][k % 4], .4, .06 + .04 * (k % 3 == 0), 2), (k % 5 - 2) / 3)   # kuş gibi tıngırtılar
for k in range(6): put(S('C07') + k * .6, davul(.6, 60), 0)
put(W('C07', 'öldürdüler'), davul(1.0, 45))
for k in range(8): put(W('C09', 'öldürdüler') - 3 + k * .38, davul(.5, 70), .1)
put(S('C10'), dron('A1', Ee('C11') - S('C10') + 2, .2, .5))
motif(S('C11'), ['A4', 'G4', 'F4', 'Eb4', 'D4'], .7, .35)

# ---------------------------------------------------------------- D: yatağın başı (az nota, uzun sessizlik)
put(S('D01'), dron('D2', Ee('D06') - S('D01'), .12, .45))
for i in ['D02', 'D03']: put(S(i), lir('D3', 4, .3))
put(S('D04'), dron('A2', Ee('D04') - S('D04') + 1, .14, .7))
motif(S('D04') + 1, ['D4', '', 'F4', '', 'A4', '', 'D5'], .7, .25)
motif(S('D05') + .5, ['D5', 'A4', 'F4', 'D4'], .8, .32)
put(S('D06'), lir('D4', 5, .35)); put(S('D06') + .02, lir('A4', 5, .25))
for k, i in enumerate(['D07', 'D08', 'D09']): put(S(i) + .4, lir(['A3', 'F3', 'D3'][k], 5, .3))
put(S('D10'), dron('D2', Ee('D12') - S('D10'), .1, .4))
motif(S('D10') + .5, AGIT, .9, .3, dur=4)
for k in range(7): put(W('D12', 'altı') + k * .9, lir('D3', 3, .2), 0)          # yedi gece
put(Ee('D13') + .2, lir('D2', 6, .3, .6))                                        # kurt: sessizlikten sonra tek bas
put(S('D14'), ruzgar(Ee('D15') - S('D14') + 1, .12))
motif(S('D14') + 2, ['Eb4', 'D4', 'C4', 'D4'], .9, .25)

# ---------------------------------------------------------------- E: dünyanın ucu (yürüyüş, karanlık, Siduri)
put(S('E01') - 1, dron('D2', Ee('E02') - S('E01') + 2, .16))
for k in range(int((Ee('E02') - S('E01')) / .8)): put(S('E01') + k * .8, davul(.32, 75), 0)
put(S('E03'), dron('D1', Ee('E03') - S('E03') + 1.5, .2, .3))                    # karanlık: yalnız dip dron
arpej(S('E04'), Ee('E04'), ['A4', 'D5', 'F5', 'A5', 'Eb5'], .25, .14)
put(S('E05'), dron('F2', Ee('E08') - S('E05') + 1, .14, .5))
arpej(S('E06'), Ee('E07'), ['F3', 'C4', 'F4', 'A4', 'C4', 'G4'], .5, .22)        # Siduri: sıcak, F majöre yakın
put(S('E09'), dron('D2', Ee('E11') - S('E09') + 2, .16, .6))
for k in range(int((Ee('E11') - S('E10')) / 1.2)): put(S('E10') + k * 1.2, davul(.3, 60), -.2)

# ---------------------------------------------------------------- F: tufandan kurtulan adam
put(S('F01') - 1, dron('A1', Ee('F02') - S('F01') + 2, .16))
arpej(S('F03'), Ee('F03'), ['D3', 'Eb3', 'D3', 'A2'], .6, .2)
for k in range(int((Ee('F04') - S('F04')) / .22)): put(S('F04') + k * .22, davul(.35 + .3 * (k % 4 == 0), 48 + 10 * (k % 2)), (k % 3 - 1) * .3)
put(S('F04'), ruzgar(Ee('F04') - S('F04') + 1, .25))
put(W('F04', 'kile'), davul(1.0, 40))
motif(S('F05'), ['D4', 'A4', 'D5'], .7, .3)
put(S('F06'), dron('D2', Ee('F12') - S('F06') + 2, .13, .5))
for k in range(7): put(W('F08', 'her') + k * .8, lir('A5', 1.5, .12, 1.5), .4)   # ekmek, gün gün
put(S('F10'), lir('D4', 4, .25))
motif(S('F12'), AGIT, .8, .3, dur=4)

# ---------------------------------------------------------------- G: yılan
put(S('G01') - 1, dron('D2', Ee('G05') - S('G01') + 2, .14, .6))
arpej(S('G02'), Ee('G03'), ['D4', 'A4', 'D5', 'F5'], .3, .15)
motif(S('G04'), ['D4', 'F4', 'G4', 'A4', 'C5'], .45, .35)                       # sur motifi neredeyse tamam (son nota yok)
arpej(S('G05'), Ee('G06'), ['D3', 'A3', 'F4', 'A3'], .5, .2)
put(W('G07', 'aldı', 1), lir('Eb5', 3, .45, 1.6), -.3)                            # A01'in aynısı
put(W('G07', 'aldı', 1) + .05, lir('D5', 3, .35, 1.6), .3)
put(S('G08'), dron('D2', Ee('G10') - S('G08') + 2, .14, .4))
motif(S('G08') + .4, AGIT, 1.0, .35, dur=4.5)
put(Ee('G10') + .3, lir('D3', 4, .25))

# ---------------------------------------------------------------- H: surlar (sur motifi ilk kez tam)
put(S('H01') - 1, dron('D2', DUR - S('H01') + 1, .16, .7))
arpej(S('H01'), Ee('H01'), ['D3', 'A3', 'D4', 'A3'], .5, .2)
motif(W('H02', 'çık'), SUR, .5, .4)
arpej(S('H03'), Ee('H04'), ['D3', 'A3', 'D4', 'F4', 'G4', 'A4', 'C5', 'A4'], .36, .24)
put(S('H05'), lir('D4', 5, .35))
motif(W('H05', 'çık'), ['D4', 'F4', 'G4', 'A4'], .5, .3)
put(W('H07', 'tableti'), lir('A5', 4, .35, 1.4))
arpej(S('H08'), Ee('H08'), ['D3', 'A3', 'D4', 'G4', 'A4', 'D4'], .42, .2)
motif(W('H09', 'sensin'), SUR, .55, .45, dur=5)
arpej(S('H10'), DUR - 2, ['D3', 'A3', 'D4', 'F4', 'A4', 'C5', 'D5', 'A4'], .45, .2)
motif(DUR - 9, SUR, .7, .35, dur=6)

# ---------------------------------------------------------------- yankı + anlatım altında kısma + son
def yanki(x, sure=2.6, kuru=.65):
    n = int(sure * SR); t = np.arange(n) / SR; ir = rng.normal(0, 1, n) * np.exp(-t * 3.2) * .018; ir[0] = 0
    m = 1 << int(np.ceil(np.log2(len(x) + n)))
    return kuru * x + np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[:len(x)]
L = yanki(L); Rr = yanki(Rr)
# anlatım altında 5 dB kısma (cümle aralarında geri gelir)
g = np.ones(N); hop = SR // 100
for c in CUES.values():
    a, b = int((c['s'] - .15) * SR), int((c['e'] + .1) * SR); g[max(0, a):min(N, b)] = 10 ** (-5 / 20)
k = np.ones(25) / 25; gs = np.repeat(np.convolve(g[::hop], k, 'same'), hop)[:N]; gs = np.pad(gs, (0, N - len(gs)), 'edge')
L *= gs; Rr *= gs
pk = max(np.abs(L).max(), np.abs(Rr).max()); L /= pk / .8; Rr /= pk / .8
fade = np.minimum(1, (N - np.arange(N)) / (3 * SR)); L *= fade; Rr *= fade
out = (np.clip(np.stack([L, Rr], 1), -1, 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'music.wav'), 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
# düzey özeti (Dorian dersi)
rms = np.sqrt(np.mean(L[:len(L) // SR * SR].reshape(-1, SR) ** 2, 1)) + 1e-9; db = 20 * np.log10(rms)
print(f'music.wav {DUR:.1f} sn | medyan {np.median(db):.1f} dBFS | -60 dB üstü saniye: {(db > -60).sum()}/{len(db)} | -40 dB üstü: {(db > -40).sum()}')
print('bölüm başı düzeyleri:', ' '.join(f"{i}:{db[int(S(i))]:.0f}" for i in ['A01', 'B01', 'C01', 'D01', 'D13', 'E03', 'F04', 'G07', 'H03']))
