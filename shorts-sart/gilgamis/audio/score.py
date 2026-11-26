#!/usr/bin/env python3
"""ŞART SHORTS'U · GILGAMIŞ: bu Shorts için yazılan müzik (filmin müziği kesilip yapıştırılmadı).
Motor ve motifler gilgamis/audio/score.py'nin kopyası (lir, dron, kil davul; Re Frig; ağıt motifi A G F Eb D). Beste bu Shorts'a özgü.
    python3 shorts-sart/gilgamis/audio/score.py → audio/music.wav (timeline.js ve zaman.js tools/ses.py'den)
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

# ================================================================ ŞART SHORTS'U: beste
# İlk karede müzik çalıyor. 'altı gün yedi gece'de filmdeki yedi tık; 'uyku'da ağıt motifi aşağı iner (düşüş);
# ekmekler gün gün yedi tel; tablette her sıra bir basamak (Re Frig yukarı), yedincisi közde: Re'ye varır; son cümlede tek davul.
KES = json.loads(re.search(r'window\.SZ = (\{.*\});', (FILM / 'zaman.js').read_text(encoding='utf-8'), re.S).group(1))['KESIT']
KS = lambda i: KES[i]['t0']
put(0.0, lir('D3', 4, .35)); put(.01, lir('A3', 4, .22), .2)
def dron_hizli(n, dur, v=.25, acik=.6):   # filmin dronu 2,5 sn'de açılıyor; Shorts'ta ilk saniyede duyulsun
    x = dron(n, dur + 2.5, v, acik)[int(2.5 * SR):]; return x * np.minimum(1, np.arange(len(x)) / (.05 * SR))
put(0.0, dron_hizli('D2', KS(1) + .5, .2))
for k in range(7): put(W('F06', 'altı') + k * .2, tik(.22), .2)
put(KS(1) - .2, dron_hizli('A1', KS(4) - KS(1) + 1.5, .16, .4))
motif(W('F07', 'uyku') - .1, AGIT, .55, .32, dur=3.5)
for k in range(7): put(KS(2) + .25 + k * .3, lir('A5', 1.2, .12, 1.5), .4)
put(W('F09', 'uyandığında'), lir('D4', 4, .3)); put(W('F09', 'gözüm'), lir('A4', 3, .2), .2)
put(KS(4) - .3, dron('D2', KS(5) - KS(4) + 2.5, .14, .55))
for n, w in zip(['D4', 'Eb4', 'F4', 'G4', 'A4', 'Bb4', 'C5'], ['birincisi', 'ikincisi', 'üçüncüsü', 'dördüncüsü', 'beşincisi', 'altıncısı', 'yedincisi']):
    put(W('F10', w), lir(n, 2.6, .3), -.1)
put(W('F10', 'közdeydi'), lir('D5', 4, .38, 1.3), .15); put(W('F10', 'közdeydi') + .02, lir('A4', 4, .25), -.15)
put(KS(5) - .2, dron('D2', DUR - KS(5) + 1, .16, .5))
motif(S('F11') + .2, ['A4', 'G4', 'F4'], .6, .28)
put(W('F11', 'yenememişti'), davul(.7, 48))
put(W('F11', 'yenememişti') + .3, lir('D3', 3, .3))

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
i_ = np.arange(N); fade = np.minimum(1, i_ / (.02 * SR)) * np.clip((DUR - i_ / SR) / .8, 0, 1); L *= fade; Rr *= fade   # döngü: 20 ms açılış, son 0,8 sn söner
out = (np.clip(np.stack([L, Rr], 1), -1, 1) * 32767).astype(np.int16)
with wave.open(str(HERE / 'music.wav'), 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
# düzey özeti (Dorian dersi)
rms = np.sqrt(np.mean(L[:len(L) // SR * SR].reshape(-1, SR) ** 2, 1)) + 1e-9; db = 20 * np.log10(rms)
print(f'music.wav {DUR:.1f} sn | medyan {np.median(db):.1f} dBFS | -60 dB üstü saniye: {(db > -60).sum()}/{len(db)} | -40 dB üstü: {(db > -40).sum()}')
print('saniye saniye:', ' '.join(f'{d:.0f}' for d in db))

