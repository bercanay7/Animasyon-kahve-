"""
Navitas · Öğretmenler Günü · hareketli Story sesi, 10 sn, 48 kHz stereo → ses.wav
Tamamen sentezlenir (telif yok); yalnız numpy. Zamanlamalar animasyon.html ile aynı.
  Müzik : keçeli piyano + yumuşak pad. D (0) → G (2.35, elma konar) → Bm (3.7, "öğretmenim") → A (4.7) → D (5.7, ışık)
  Efekt : tebeşir sürtmesi (kitaplar çizilirken), elmanın "tok"u, kalemin kayması ve dokunuşu, pırıltı çanları, ışık parıltısı
Çalıştırma: python3 ses.py
"""
import wave
import numpy as np

SR, DUR = 48000, 10.0
N = int(SR * DUR)
rng = np.random.default_rng(24)
L = np.zeros(N); R = np.zeros(N)


def tt(d): return np.arange(int(SR * d)) / SR
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)


def place(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N: return
    s = sig[: N - i] * gain
    L[i:i + len(s)] += s * np.sqrt((1 - pan) / 2)
    R[i:i + len(s)] += s * np.sqrt((1 + pan) / 2)


def bandpass(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= np.exp(-((np.log(np.maximum(f, 1) / np.sqrt(lo * hi))) / np.log(hi / lo) * 2) ** 2)
    return np.fft.irfft(X, len(x))


def piano(m, d=2.6, vel=1.0):
    t = tt(d); f = hz(m); s = np.zeros_like(t)
    for k, a in enumerate([1, .45, .22, .12, .06], 1):          # keçeli piyano: az üst ses, hızlı sönen tını
        s += a * np.sin(2 * np.pi * f * k * t * (1 + 0.0004 * k * k)) * np.exp(-t * (1.6 + 1.3 * k))
    att = np.minimum(1, t / 0.006)
    thump = np.sin(2 * np.pi * f * 0.5 * t) * np.exp(-t * 30) * 0.2
    return (s + thump) * att * vel * 0.22


def pad(ms, d, at):
    t = tt(d); s = np.zeros_like(t)
    for m in ms:
        for det in (-0.06, 0.06):
            s += np.sin(2 * np.pi * hz(m + det) * t + rng.random() * 6) * 0.5
    env = np.minimum(1, t / 0.9) * np.minimum(1, (d - t) / 0.9)
    place(s * env * 0.028, at, pan=-0.2); place(s * env * 0.028, at, pan=0.2)


def bell(m, at, g=0.12, pan=0.0):
    t = tt(2.2); f = hz(m)
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * dcy) for a, r, dcy in
            [(1, 1, 3), (.5, 2.76, 5), (.3, 5.4, 8), (.2, 8.9, 12)])
    place(s * np.minimum(1, t / 0.002), at, g, pan)


def chalk(at, d, g=0.18, pan=0.0):
    """tebeşir sürtmesi: bant geçiren gürültü, düzensiz basınçla"""
    n = int(SR * d); x = rng.standard_normal(n)
    x = bandpass(x, 1800, 6500)
    t = np.arange(n) / SR
    press = 0.6 + 0.4 * np.sin(2 * np.pi * 9 * t + rng.random() * 6) * np.sin(2 * np.pi * 3.3 * t)
    grit = (rng.random(n) < 0.004) * rng.standard_normal(n) * 6           # tebeşir taneleri
    env = np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.06)
    place((x * press + bandpass(grit, 2500, 9000)) * env, at, g / np.std(x), pan)


def whoosh(at, d, lo, hi, g=0.1, pan=0.0):
    n = int(SR * d); t = np.arange(n) / SR
    x = bandpass(rng.standard_normal(n), lo, hi)
    env = np.sin(np.pi * np.minimum(1, t / d)) ** 2
    place(x / np.std(x) * env, at, g, pan)


def tok(at, g=0.5):
    t = tt(0.5)
    body = np.sin(2 * np.pi * (180 * np.exp(-t * 6) + 70) * t) * np.exp(-t * 14)   # elmanın kitaba konuşu
    knock = bandpass(rng.standard_normal(len(t)), 400, 2500) * np.exp(-t * 60) * 0.15
    place(body + knock, at, g)


# ---- müzik ----
D, G, Bm, A = 62, 55, 59, 57
CH = [(0.0, [50, 57, 62, 66, 69]), (2.35, [43, 55, 59, 62, 66]), (3.7, [47, 54, 59, 62, 66]),
      (4.7, [45, 52, 57, 61, 64]), (5.7, [50, 57, 62, 66, 69, 76])]
for i, (at, ms) in enumerate(CH):
    end = CH[i + 1][0] + 0.6 if i + 1 < len(CH) else DUR
    pad(ms[1:4], end - at, at)
    place(piano(ms[0], 3.5, 0.9), at, pan=-0.1)                     # bas
# melodi: vurgu anlarına oturur (logo, etiket, kitaplar, elma, yaprak, pırıltı, yazı, ışık)
MEL = [(0.15, 74), (0.45, 78), (0.80, 76), (1.10, 74), (1.40, 71), (1.70, 69),
       (2.35, 74), (2.50, 78), (2.95, 81), (3.25, 79), (3.70, 78), (4.05, 74),
       (4.70, 76), (5.05, 73), (5.70, 74), (6.10, 78), (6.50, 81), (7.30, 86)]
for at, m in MEL:
    place(piano(m, 2.8, 0.75), at, pan=0.15 * np.sin(at * 3))
    if at >= 5.7: place(piano(m - 12, 2.8, 0.35), at)

# ---- efektler ----
for i, (s, d) in enumerate([(0.80, .55), (1.02, .4), (1.10, .55), (1.32, .4), (1.40, .55), (1.62, .4)]):
    chalk(s, d, 0.16 if d > .5 else 0.1, pan=-0.3 + 0.12 * i)        # kitapların dış ve iç çizgileri
chalk(0.35, 1.0, 0.035, 0.0)                                         # çerçeve: çok hafif
whoosh(1.90, 0.45, 300, 2000, 0.05)                                  # elmanın düşüşü
tok(2.35, 0.55)
chalk(2.36, 0.25, 0.08)                                              # toz
whoosh(2.42, 0.35, 2000, 7000, 0.04, 0.2)                            # yaprak
whoosh(2.55, 0.5, 600, 4000, 0.07, 0.6)                              # kalem gelir
tok(2.98, 0.12)                                                      # kalem dokunur
for i, (at, m) in enumerate([(2.95, 93), (3.03, 98), (3.11, 90)]):
    bell(m, at, 0.05, pan=[-0.5, 0.4, -0.2][i])
for i in range(3): whoosh(3.25 + i * 0.09, 0.25, 3000, 9000, 0.02)  # kelimeler
for i in range(11): bell(96 + (i % 3) * 2, 3.7 + i * 0.055, 0.006, pan=-0.6 + i * 0.12)  # harfler: fısıltı gibi
chalk(4.95, 0.5, 0.12, 0.1)                                          # vurgu çizgisi
whoosh(5.75, 0.9, 4000, 12000, 0.03)                                 # ışık süpürmesi
for i, m in enumerate([86, 90, 93, 98]): bell(m, 5.85 + i * 0.12, 0.025, pan=-0.4 + i * 0.27)

# ---- miks: oda yankısı, son karartma, düzey ----
ir_t = tt(1.6)
ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 3.2); ir[0] = 0
def conv(x):
    n = len(x) + len(ir)
    y = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:len(x)]
    return y / np.max(np.abs(ir)) * 0.012
L, R = L + conv(L), R + conv(np.roll(R, 240))
fade = np.minimum(1, (DUR - np.arange(N) / SR) / 1.2)
L *= fade; R *= fade
pk = max(np.abs(L).max(), np.abs(R).max())
L, R = L / pk * 0.8, R / pk * 0.8
out = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open('ses.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
print('Hazır: ses.wav')
