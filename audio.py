"""
Dünya Kahve Günü (Story) — ses tasarımı, 9 sn, 48 kHz stereo → audio.wav

Tamamen sentezlenir, telif sorunu yoktur. Zamanlamalar animation.html ile senkrondur.
120 BPM, vuruş = 0.5 sn, ızgara 0'dan başlar. İlk karede güçlü bir vuruşla açılır.
  Akorlar: D (0) → Bm7 (1.0, espresso) → Gmaj7 (2.5, köpüğe dalış) → A (4.0, şeritler) → D6/9 (6.0, kapanış)
  Davul  : kick her vuruşta, clap 2. ve 4. vuruşlarda, hi-hat sekizliklerde; kapanışta sakinleşir
  Efekt  : açılış darbesi, geçiş whoosh'ları, çekirdek patlaması, harf "pop"ları, parıltı, kapanış çanı
Çalıştırma: python3 audio.py   (numpy + scipy gerekir)
"""
import wave
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000
DUR = 9.0
N = int(SR * DUR)
BEAT = 0.5
rng = np.random.default_rng(11)


def tt(d):
    return np.arange(int(SR * d)) / SR


def place(buf, sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N or i < 0:
        return
    sig = sig[: N - i] * gain
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:i + len(sig), 0] += sig * l * 1.414
    buf[i:i + len(sig), 1] += sig * r * 1.414


def note(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def lowpass(x, fc, order=2):
    return sosfilt(butter(order, fc, 'low', fs=SR, output='sos'), x)


def highpass(x, fc, order=2):
    return sosfilt(butter(order, fc, 'high', fs=SR, output='sos'), x)


def bandpass(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], 'band', fs=SR, output='sos'), x)


def sweep_lowpass(x, f0, f1, curve=1.0):
    n = len(x)
    f = f0 + (f1 - f0) * (np.linspace(0, 1, n) ** curve)
    a = np.exp(-2 * np.pi * f / SR)
    y = np.empty(n)
    z = 0.0
    for i in range(n):
        z = (1 - a[i]) * x[i] + a[i] * z
        y[i] = z
    return y


def with_reverb(dry, wet, seconds=1.4):
    r = np.random.default_rng(5)
    t = tt(seconds)
    ir = r.standard_normal((len(t), 2)) * np.exp(-t * 4.5)[:, None]
    for c in range(2):
        ir[:, c] = lowpass(ir[:, c], 6000)
    ir /= np.abs(ir).sum(axis=0).max() / 6
    out = dry.copy()
    for c in range(2):
        out[:, c] += fftconvolve(dry[:, c], ir[:, c])[:N] * wet
    return out


# ---------------- sesler ----------------
def kick(d=0.45, f0=55, punch=4.0):
    t = tt(d)
    f = f0 * (1 + punch * np.exp(-t * 35))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    click = highpass(rng.standard_normal(len(t)), 3000) * np.exp(-t * 400) * 0.3
    return np.tanh((body + click) * 1.6)


def clap(d=0.25):
    t = tt(d)
    n = bandpass(rng.standard_normal(len(t)), 900, 5000)
    env = np.zeros_like(t)
    for o in (0, 0.011, 0.022):
        env += np.where(t >= o, np.exp(-(t - o) * 90), 0)
    env += np.exp(-t * 18) * 0.35
    return n * env


def hat(open_=False):
    t = tt(0.22 if open_ else 0.06)
    return highpass(rng.standard_normal(len(t)), 7000) * np.exp(-t * (18 if open_ else 70))


def boom(d=1.4):
    t = tt(d)
    f = 42 * (1 + 2.5 * np.exp(-t * 20))
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.6)
    noise = lowpass(rng.standard_normal(len(t)), 900) * np.exp(-t * 9) * 0.6
    return np.tanh((sub + noise) * 1.4)


def whoosh(d, f0, f1, peak=0.9, curve=1.5):
    x = rng.standard_normal(int(SR * d))
    y = sweep_lowpass(x, f0, f1, curve)
    t = np.linspace(0, 1, len(y))
    env = np.where(t < peak, (t / peak) ** 2.4, np.clip((1 - t) / (1 - peak), 0, 1) ** 1.5)
    return y * env


def pop(f0=500, f1=1400, d=0.09):
    t = tt(d)
    f = f0 + (f1 - f0) * (1 - np.exp(-t * 70))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45) * np.minimum(1, t / 0.0015)


def epiano(freq, d=1.2, decay=3.0):
    t = tt(d)
    env = np.exp(-t * decay) * np.minimum(1, t / 0.003)
    return (np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2 * t) * np.exp(-t * 7)
            + 0.08 * np.sin(2 * np.pi * freq * 3.01 * t) * np.exp(-t * 10)) * env


def bell(freq, d=2.4):
    t = tt(d)
    return sum(a * np.sin(2 * np.pi * freq * r * t) * np.exp(-t * dk)
               for r, a, dk in [(1, 1, 1.4), (2.0, 0.35, 2.4), (2.76, 0.25, 3.4), (5.4, 0.08, 6)]) * np.minimum(1, t / 0.003)


def pad(notes, d):
    t = tt(d)
    sig = np.zeros_like(t)
    for n in notes:
        for det in (-0.1, 0.1):
            f = note(n) * 2 ** (det / 12)
            for h in range(1, 6):
                sig += np.sin(2 * np.pi * f * h * t + h) / h ** 1.7
    env = np.minimum(1, t / 0.12) * np.clip((d - t) / 0.2, 0, 1)
    return lowpass(sig, 2200) * env / len(notes)


# ---------------- müzik ----------------
music = np.zeros((N, 2))
drums = np.zeros((N, 2))
CHORDS = [  # başlangıç, bitiş, akor, bas kökü
    (0.0, 1.0, [62, 66, 69, 74], 38),      # D
    (1.0, 2.5, [59, 62, 66, 69], 35),      # Bm7
    (2.5, 4.0, [55, 59, 62, 66], 31),      # Gmaj7
    (4.0, 6.0, [57, 61, 64, 69], 33),      # A
    (6.0, DUR, [62, 66, 69, 71, 76], 38),  # D6/9
]
for start, end, ch, root in CHORDS:
    place(music, pad(ch, end - start + 0.15), start, gain=0.10)
    stab = sum(epiano(note(n), 1.4, 2.4) for n in ch) / len(ch)  # sahne başında akor vuruşu
    place(music, stab, start, gain=0.55)
    k = start
    while k < min(end, 8.0) - 1e-6:                                  # bas: her vuruşta kök
        bt = tt(0.42)
        b = np.sin(2 * np.pi * note(root) * bt) + 0.3 * np.sin(2 * np.pi * note(root) * 2 * bt)
        b *= np.exp(-bt * 6) * np.minimum(1, bt / 0.004)
        place(music, np.tanh(b * 1.3), k, gain=0.32)
        k += BEAT

# arpej: köpüğe dalıştan itibaren onaltılıklar, kapanışta sekizlik
k, tn = 0, 2.5
while tn < 8.3:
    ci = max(i for i, c in enumerate(CHORDS) if c[0] <= tn + 1e-6)
    ch = CHORDS[ci][2]
    n = ch[[0, 2, 1, 3, 2, 1][k % 6] % len(ch)] + 12
    place(music, epiano(note(n), 0.8, 5), tn, gain=0.12, pan=0.35 if k % 2 else -0.35)
    k += 1
    tn += 0.25 if tn < 6.0 else 0.5

# davul
for i in range(int(8.0 / BEAT) + 1):
    t0 = i * BEAT
    if t0 < 6.0 or t0 in (6.0, 7.0, 8.0):
        place(drums, kick(), t0, gain=0.9 if t0 <= 6.0 else 0.55)
    if t0 < 6.0 and i % 2 == 1:
        place(drums, clap(), t0, gain=0.45)
for i in range(20):
    t0 = 1.0 + i * 0.25
    place(drums, hat(open_=(i % 4 == 1)), t0, gain=0.11 if i % 2 else 0.07, pan=0.3)

# ---------------- efektler ----------------
sfx = np.zeros((N, 2))
place(sfx, boom(), 0.0, gain=0.7)                                                         # açılış darbesi
place(sfx, pop(700, 1600), 0.5, gain=0.25)                                                 # etiket
place(sfx, bandpass(whoosh(0.5, 500, 5000), 200, 10000), 0.62, gain=0.35)                  # espresso daire
for i in range(11):                                                                         # çekirdek patlaması
    place(sfx, pop(380 + i * 60, 1100 + i * 90, 0.08), 1.5 + i * 0.012, gain=0.13, pan=np.sin(i * 2.1) * 0.7)
place(sfx, bandpass(whoosh(0.45, 300, 6000, 0.95, 2.0), 150, 11000), 2.06, gain=0.45)      # köpüğe dalış
place(sfx, boom(1.0), 2.5, gain=0.5)
for i in range(7):                                                                          # "bizden!" harfleri
    place(sfx, pop(900 + i * 110, 2000 + i * 120, 0.06), 2.6 + i * 0.04, gain=0.12, pan=-0.5 + i * 0.16)
for i, n in enumerate([86, 90, 93, 98]):                                                    # parıltı
    place(sfx, bell(note(n), 1.2), 3.0 + i * 0.06, gain=0.05, pan=-0.4 + i * 0.27)
place(sfx, bandpass(whoosh(0.4, 600, 5000, 0.9), 200, 10000), 3.62, gain=0.3, pan=0.3)     # şeritler
place(sfx, bandpass(whoosh(0.45, 400, 5500, 0.92, 2.0), 150, 11000), 5.58, gain=0.35)      # krem ekran
place(sfx, boom(1.2), 6.0, gain=0.45)
for i in range(7):                                                                          # "bizden." harfleri
    place(sfx, pop(900 + i * 110, 2000 + i * 120, 0.06), 6.3 + i * 0.04, gain=0.1, pan=-0.5 + i * 0.16)
place(sfx, bell(note(74), 2.6), 6.0, gain=0.2, pan=-0.1)                                    # kapanış çanı
place(sfx, bell(note(81), 2.4), 6.3, gain=0.12, pan=0.2)
place(sfx, pop(800, 1500), 6.95, gain=0.18)                                                 # etiket

# ---------------- miks ----------------
mix = with_reverb(music, 0.25) + drums + with_reverb(sfx, 0.15)
mt = np.arange(N) / SR
mix *= np.clip((DUR - mt) / 0.6, 0, 1)[:, None]
mix = np.tanh(mix / np.abs(mix).max() * 1.5) / np.tanh(1.5) * 0.89  # yumuşak limit, ~ -1 dBFS
pcm = (np.clip(mix, -1, 1) * 32767).astype('<i2')
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('audio.wav yazıldı')
