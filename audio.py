"""
Dünya Kahve Günü — ses tasarımı (20 sn, 48 kHz stereo) → audio.wav

Tamamen sentezlenir, telif sorunu yoktur. Zamanlamalar animation.html ile senkrondur.
  Müzik : D majör, sahne geçişlerinde akor değişimi
          Dmaj7 (0) → Bm9 (3.0, koyu sahne) → Gmaj7 (6.95) → Em9 (10.3, fal)
          → Asus2 (12.6, fal açılır) → D6/9 (15.0, final)
  Efekt : damla, geri sıçrama, whoosh + kapanış darbesi, panel whoosh,
          kahve dökülmesi, sayaç tıkları, fincan kapatma + porselen tıkı,
          bekleme tıkları, fincan kalkar, telve hışırtısı, fal parıltısı,
          tabağın rozete uçuşu, final çanı, rozet tıkı
Çalıştırma: python3 audio.py   (numpy + scipy gerekir)
"""
import wave
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000
DUR = 20.0
N = int(SR * DUR)
rng = np.random.default_rng(3)


def tt(d):
    return np.arange(int(SR * d)) / SR


def place(buf, sig, at, gain=1.0, pan=0.0):
    """sig'i at (sn) anında stereo tampona ekle; pan -1 (sol) .. 1 (sağ)."""
    i = int(at * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:i + len(sig), 0] += sig * l * 1.414
    buf[i:i + len(sig), 1] += sig * r * 1.414


def note(n):  # MIDI → Hz
    return 440.0 * 2 ** ((n - 69) / 12)


def lowpass(x, fc, order=2):
    return sosfilt(butter(order, fc, 'low', fs=SR, output='sos'), x)


def bandpass(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], 'band', fs=SR, output='sos'), x)


def sweep_lowpass(x, f0, f1, curve=1.0):
    """Zamanla kesim frekansı değişen tek kutuplu alçak geçiren filtre."""
    n = len(x)
    f = f0 + (f1 - f0) * (np.linspace(0, 1, n) ** curve)
    a = np.exp(-2 * np.pi * f / SR)
    y = np.empty(n)
    z = 0.0
    for i in range(n):
        z = (1 - a[i]) * x[i] + a[i] * z
        y[i] = z
    return y


def reverb_ir(seconds=2.2, seed=5):
    r = np.random.default_rng(seed)
    t = tt(seconds)
    ir = r.standard_normal((len(t), 2)) * np.exp(-t * 3.2)[:, None]
    ir[:, 0] = lowpass(ir[:, 0], 5000)
    ir[:, 1] = lowpass(ir[:, 1], 5000)
    return ir / np.abs(ir).sum(axis=0).max() * 6


def with_reverb(dry, wet=0.3):
    ir = reverb_ir()
    out = dry.copy()
    for c in range(2):
        out[:, c] += fftconvolve(dry[:, c], ir[:, c])[:N] * wet
    return out


# ---------------- müzik ----------------
music = np.zeros((N, 2))
CHORDS = [  # (başlangıç, bitiş, notalar)
    (0.0, 3.0, [50, 54, 57, 61]),          # Dmaj7
    (3.0, 6.95, [47, 50, 54, 57, 61]),     # Bm9 (B D F# A C#)
    (6.95, 10.3, [43, 47, 50, 54, 59]),    # Gmaj7 (+B)
    (10.3, 12.6, [40, 47, 50, 54, 55]),    # Em9 (E B D F# G) — gizemli
    (12.6, 15.0, [45, 52, 57, 59, 64]),    # Asus2 — fal açılır, merak
    (15.0, DUR, [50, 54, 57, 59, 64]),     # D6/9 — final
]


def pad_voice(freq, d):
    t = tt(d)
    sig = np.zeros_like(t)
    for det in (-0.12, 0.0, 0.11):  # hafif detune ile sıcak koro
        f = freq * 2 ** (det / 12)
        for h in range(1, 7):
            sig += np.sin(2 * np.pi * f * h * t + h) / h ** 1.6
    return lowpass(sig, 1600) / 3


for start, end, notes in CHORDS:
    d = end - start + 0.9  # sonraki akora yumuşak geçiş
    t = tt(d)
    env = np.minimum(1, t / 0.7) * np.clip((d - t) / 0.9, 0, 1)
    chord = sum(pad_voice(note(n), d) for n in notes) * env
    place(music, chord, max(0, start - 0.15), gain=0.035)
    # yumuşak bas
    bt = tt(d)
    bass = np.sin(2 * np.pi * note(notes[0] - 12) * bt) * np.minimum(1, bt / 0.05) * np.exp(-bt * 0.6)
    place(music, bass, start, gain=0.11)


def epiano(freq, d=1.8):
    t = tt(d)
    env = np.exp(-t * 2.6) * np.minimum(1, t / 0.004)
    sig = (np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(2 * np.pi * freq * 2 * t) * np.exp(-t * 6)
           + 0.06 * np.sin(2 * np.pi * freq * 3.01 * t) * np.exp(-t * 9))
    return sig * env


# arpej: 3. saniyeden itibaren, 92 BPM sekizlikler, seyrek
BEAT = 60 / 92
ARP = {0: [62, 66, 69, 73], 1: [59, 62, 66, 69, 73], 2: [55, 59, 62, 66, 71],
       3: [64, 67, 71, 74, 78], 4: [69, 71, 76, 81, 83], 5: [62, 66, 69, 71, 76]}
k = 0
t_note = 3.0
while t_note < 19.3:
    ci = max(i for i, c in enumerate(CHORDS) if c[0] <= t_note + 1e-6)
    pattern = ARP[ci]
    n = pattern[[0, 2, 1, 3, 2, 4, 3, 1][k % 8] % len(pattern)]
    accent = 1.0 if k % 2 == 0 else 0.6
    quiet = 0.35 if 11.6 <= t_note < 12.6 else 1.0  # fincan kapalıyken nefes
    place(music, epiano(note(n)), t_note, gain=0.05 * accent * quiet, pan=(-0.35 if k % 2 else 0.35))
    k += 1
    t_note += BEAT if ci in (0, 1, 3) else BEAT / 2

# final: iki oktav yukarıda kısa melodi
for i, (n, at) in enumerate([(78, 15.05), (81, 15.4), (83, 15.75), (81, 16.3), (78, 17.0), (76, 17.7)]):
    place(music, epiano(note(n), 2.2), at, gain=0.045, pan=0.2 * (-1) ** i)

# genel müzik zarfı: hızlı giriş, sonda kısılma
mt = np.arange(N) / SR
music *= (np.minimum(1, mt / 0.25) * np.clip((DUR - mt) / 0.9, 0, 1))[:, None]

# ---------------- efektler ----------------
sfx = np.zeros((N, 2))


def plip(f0=650, f1=1700, d=0.16):
    t = tt(d)
    f = f0 + (f1 - f0) * (1 - np.exp(-t * 60))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 32) * np.minimum(1, t / 0.002)


def thump(f=110, d=0.35, decay=12):
    t = tt(d)
    fr = f * (1 + 1.5 * np.exp(-t * 40))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * decay)


def whoosh(d, f0, f1, peak=0.85, curve=1.5):
    x = rng.standard_normal(int(SR * d))
    y = sweep_lowpass(x, f0, f1, curve)
    t = np.linspace(0, 1, len(y))
    env = np.where(t < peak, (t / peak) ** 2.2, np.clip((1 - t) / (1 - peak), 0, 1) ** 1.5)
    return y * env


def tick(f=2200, d=0.03):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) * 0.6 + rng.standard_normal(len(t)) * 0.4) * np.exp(-t * 220)


def bell(freq, d=2.6):
    t = tt(d)
    sig = sum(a * np.sin(2 * np.pi * freq * r * t) * np.exp(-t * dk)
              for r, a, dk in [(1, 1, 1.6), (2.0, 0.35, 2.5), (2.76, 0.25, 3.5), (5.4, 0.08, 6)])
    return sig * np.minimum(1, t / 0.003)


# S1: damla düşer (0.95) ve geri sıçrayan damlacık iner (1.75)
place(sfx, plip(), 0.95, gain=0.55)
place(sfx, thump(120, 0.3), 0.95, gain=0.35)
place(sfx, plip(900, 2200, 0.12), 1.75, gain=0.28, pan=0.1)
# daire ekranı kaplar: yükselen whoosh + koyu sahneye iniş darbesi
place(sfx, bandpass(whoosh(0.9, 300, 3200), 120, 9000), 2.12, gain=0.22)
place(sfx, thump(58, 1.0, 4.5), 2.98, gain=0.5)
# başlık satırları: çok hafif tıklar
for i, at in enumerate([2.75, 2.85, 2.98, 3.11]):
    place(sfx, tick(1400 + i * 120, 0.02), at, gain=0.06, pan=-0.3)
# panel siler
place(sfx, bandpass(whoosh(0.8, 500, 4000, 0.8), 150, 10000), 6.18, gain=0.2, pan=0.2)
# kahve dökülmesi (7.95–8.8): gurul gurul, dolarken tınısı yükselir
pd = 1.05
x = rng.standard_normal(int(SR * pd))
pour = sweep_lowpass(x, 500, 1500, 1.0)
pt = tt(pd)
gurgle = 0.6 + 0.4 * np.sin(2 * np.pi * (9 + 5 * pt) * pt) * np.sin(2 * np.pi * 3.3 * pt)
pour *= gurgle * np.minimum(1, pt / 0.08) * np.clip((pd - pt) / 0.25, 0, 1)
place(sfx, pour, 7.9, gain=0.45, pan=-0.05)
# sayaç tıkları: animation.html'deki odometer ile aynı hesap
def ease_out_expo(x):
    return np.where(x >= 1, 1, 1 - 2 ** (-10 * x))


for di, ch in enumerate([1, 5, 0, 0]):
    d0 = 8.45 + di * 0.1
    ts = np.linspace(d0, d0 + 0.9, 2000)
    v = (ch - 2) - 1 + ease_out_expo(np.clip((ts - d0) / 0.9, 0, 1)) * 3
    steps = np.where(np.diff(np.floor(v + 0.06)) > 0)[0]  # görsel oturma anı
    for s in steps:
        place(sfx, tick(2600 - di * 150), ts[s + 1], gain=0.12, pan=-0.45 + di * 0.3)
# fal: kahve içilir (yumuşak alçalan hışırtı)
place(sfx, bandpass(whoosh(0.8, 1800, 400, 0.3, 1.0), 150, 4000), 10.0, gain=0.07)


def clink(f=3100, d=0.5):
    t = tt(d)
    return sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * dk)
               for r, a, dk in [(1, 1, 14), (1.52, 0.6, 18), (2.31, 0.35, 24), (3.1, 0.2, 30)])


# fincan havada döner ve tabağa kapanır
place(sfx, bandpass(whoosh(0.7, 400, 2600, 0.7), 150, 9000), 10.9, gain=0.14, pan=-0.1)
place(sfx, clink(), 11.6, gain=0.16, pan=0.05)
place(sfx, thump(180, 0.2, 25), 11.6, gain=0.18)
# bekleme: saat gibi üç yumuşak tık
for i, at in enumerate([11.85, 12.15, 12.45]):
    place(sfx, tick(1500, 0.025), at, gain=0.07, pan=-0.2 + i * 0.2)
# fincan kalkar
place(sfx, clink(3600, 0.3), 12.6, gain=0.08, pan=-0.1)
place(sfx, bandpass(whoosh(0.6, 600, 4500, 0.85), 200, 10000), 12.6, gain=0.13, pan=0.15)
# telve beliriyor: kum gibi hışırtı taneleri
grains = np.zeros(int(SR * 1.2))
gt = np.arange(len(grains)) / SR
for _ in range(260):
    at = rng.uniform(0, 1.1) ** 1.4
    i = int(at * SR)
    g = rng.standard_normal(int(SR * 0.004)) * np.exp(-np.arange(int(SR * 0.004)) / SR * 900)
    grains[i:i + len(g)] += g * rng.uniform(0.3, 1)
grains = bandpass(grains, 1800, 9000) * np.clip((1.2 - gt) / 0.4, 0, 1)
place(sfx, grains, 13.1, gain=0.22, pan=0.1)
# fal okunur: parıltı
for i, (n, at) in enumerate([(81, 13.45), (85, 13.6), (88, 13.75)]):
    place(sfx, bell(note(n), 1.8), at, gain=0.05, pan=-0.3 + i * 0.3)
# tabak rozete uçar
place(sfx, bandpass(whoosh(0.8, 700, 3500, 0.75), 200, 9000), 14.6, gain=0.13, pan=0.4)
# final: "Kahveler bizden." çanı + rozet
place(sfx, bell(note(74)), 15.0, gain=0.16, pan=-0.15)
place(sfx, bell(note(81)), 15.15, gain=0.10, pan=0.2)
place(sfx, tick(1800, 0.04), 15.6, gain=0.1, pan=0.5)

# ---------------- miks ----------------
mix = with_reverb(music, 0.35) + with_reverb(sfx, 0.18)
peak = np.abs(mix).max()
mix = mix / peak * 0.89  # ~ -1 dBFS tepe
pcm = (np.clip(mix, -1, 1) * 32767).astype('<i2')
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('audio.wav yazıldı')
