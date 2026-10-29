"""
29 Ekim · Cumhuriyet 103 yaşında — ses tasarımı, 35.2 sn, 48 kHz stereo → audio.wav

Müzik ve efektler tamamen sentezlenir (marş ya da hazır müzik yok). Seslendirme ses/seslendirme.mp3'ten gelir
(ElevenLabs, eleven_v4, "Hebun Tuna" sesi); VO listesi kaydın parçalarını videodaki yerlerine koyar, müzik konuşma
sırasında kısılır. Zamanlamalar animation.html ile senkrondur.
  0.0  Re minör: yaylı halı, saat tıkırtısı. "Efendiler… yarın Cumhuriyet'i ilan edeceğiz."
  4.8  Flaşla kesme, timpani. "29 Ekim 1923. Saat 20.30… Cumhuriyet ilan edildi."; 10.6'dan top atışları, Re majör
 12.0  Işık sızıntısı parıltısı; Gençliğe Hitabe seslendirmesi, altında yaylılar ve seyrek piyano
 22.8  Kalp atışı gibi timpani, 24.8'den timpani tremolosu ve ters zil ile yükseliş; imza sırasında kalem hışırtısı
 26.4  Doruk: Re majör, bakır + yaylı + timpani + zil; bayrak dalgalanma sesi
 29.6  Geri çekiliş; havai fişekler; "Cumhuriyetimizin yüz üçüncü yılı kutlu olsun!"; son Re majör akoru
Bayraktan sonraki olaylar ilk sürümün saatleriyle yazılıdır (doruk 13.6) ve SH kadar kaydırılır (animation.html ile aynı).
Çalıştırma: python3 audio.py   (numpy + scipy + ffmpeg gerekir)
"""
import subprocess
import wave
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000
DUR = 35.2
SH = 26.4 - 13.6  # bayrak doruğunun kayması
N = int(SR * DUR)
BEAT = 0.8
rng = np.random.default_rng(1923)

# animation.html ile aynı liste: (patlama anı, x, y, tür, boyut)
BURSTS = [(t + SH, x, k, s) for t, x, k, s in [
    (18.0, 175, 'red', 1.0), (18.4, 900, 'white', 0.95), (18.8, 890, 'gold', 0.7),
    (19.2, 165, 'gold', 0.9), (19.6, 200, 'white', 0.7), (20.0, 880, 'red', 1.05),
    (20.4, 540, 'gold', 1.2), (20.8, 180, 'red', 0.9), (21.2, 910, 'white', 0.9),
    (21.6, 250, 'gold', 0.85), (22.0, 860, 'red', 0.8),
]]


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


def env_adsr(n, a, r, total):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.clip((total - t) / max(r, 1e-4), 0, 1)


def reverb(dry, seconds=2.6, decay=2.4, seed=5, lp=5000):
    r = np.random.default_rng(seed)
    t = tt(seconds)
    ir = r.standard_normal((len(t), 2)) * np.exp(-t * decay)[:, None]
    ir[: int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))[:, None]
    for c in range(2):
        ir[:, c] = lowpass(ir[:, c], lp)
    ir /= np.sqrt((ir ** 2).sum(axis=0)).max()
    out = np.zeros_like(dry)
    for c in range(2):
        out[:, c] = fftconvolve(dry[:, c], ir[:, c])[:len(dry)]
    return out


# ---------------- çalgılar ----------------
def saw(f, t, voices=5, spread=0.12, seed=0):
    r = np.random.default_rng(seed)
    out = np.zeros_like(t)
    for v in range(voices):
        det = (v - (voices - 1) / 2) / max(1, voices - 1) * spread
        ff = f * 2 ** (det / 12) * (1 + 0.0025 * np.sin(2 * np.pi * (4.6 + v * 0.3) * t + r.random() * 6))
        ph = 2 * np.pi * np.cumsum(ff) / SR + r.random() * 6
        hmax = int(min(40, 16000 / f))
        for h in range(1, hmax + 1):
            out += np.sin(ph * h) / h
    return out / voices


def strings(notes, d, att=0.5, rel=0.5, bright=2400):
    t = tt(d + rel)
    sig = sum(saw(note(n), t, 5, 0.14, seed=n) for n in notes) / len(notes)
    sig = lowpass(sig, bright, 2)
    return sig * env_adsr(len(t), att, rel, d + rel)


def brass(notes, d, att=0.18, rel=0.6):
    t = tt(d + rel)
    sig = sum(saw(note(n), t, 3, 0.06, seed=n + 100) for n in notes) / len(notes)
    e = np.minimum(1, t / att) ** 1.5
    dark, bright = lowpass(sig, 700, 2), lowpass(sig, 3600, 2)
    br = np.clip(e * (1 - 0.35 * np.minimum(1, t / 1.6)), 0, 1)       # açılıp hafifçe kapanan filtre
    return (dark * (1 - br) + bright * br) * env_adsr(len(t), att, rel, d + rel)


def piano(f, d=3.0, vel=1.0):
    t = tt(d)
    B = 0.0004
    sig = np.zeros_like(t)
    for h, a in enumerate([1, 0.5, 0.28, 0.16, 0.1, 0.06, 0.035], start=1):
        fh = f * h * np.sqrt(1 + B * h * h)
        sig += a * np.sin(2 * np.pi * fh * t) * np.exp(-t * (1.1 + h * 0.55))
    hammer = highpass(rng.standard_normal(len(t)), 1500) * np.exp(-t * 300) * 0.08
    return (sig + hammer) * np.minimum(1, t / 0.002) * vel


def bell(freq, d=3.0):
    t = tt(d)
    return sum(a * np.sin(2 * np.pi * freq * r * t) * np.exp(-t * dk)
               for r, a, dk in [(1, 1, 1.0), (2.0, 0.4, 1.8), (2.76, 0.28, 2.6), (5.4, 0.1, 4.5), (8.9, 0.05, 7)]) * np.minimum(1, t / 0.002)


def timpani(f=note(38), d=2.2, vel=1.0):
    t = tt(d)
    ff = f * (1 + 0.12 * np.exp(-t * 18))
    body = np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t * 2.2)
    body += 0.35 * np.sin(2 * np.pi * np.cumsum(ff * 1.5) / SR) * np.exp(-t * 3.5)
    skin = lowpass(rng.standard_normal(len(t)), 1200) * np.exp(-t * 40) * 0.5
    return np.tanh((body + skin) * 1.3) * vel


def crash(d=3.5):
    t = tt(d)
    n = highpass(rng.standard_normal(len(t)), 3500) * np.exp(-t * 2.0)
    metal = sum(np.sin(2 * np.pi * f * t + i) for i, f in enumerate([3203, 4157, 5371, 6789, 7411])) * 0.05 * np.exp(-t * 2)
    return (n * 0.6 + metal) * np.minimum(1, t / 0.002)


def reverse_swell(d=1.2):
    return crash(d + 0.4)[::-1][-int(SR * d):] * np.linspace(0, 1, int(SR * d)) ** 2


def cannon(d=3.0, far=0.0):
    t = tt(d)
    f = 36 * (1 + 3.0 * np.exp(-t * 14))
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (2.2 + far * 2))
    crack = bandpass(rng.standard_normal(len(t)), 120, 4000 * (1 - far * 0.7)) * np.exp(-t * (22 + far * 20))
    rumble = lowpass(rng.standard_normal(len(t)), 220) * np.exp(-t * 1.6) * 0.8
    return np.tanh((sub * 0.8 + crack * 1.6 + rumble * 0.6) * 1.6)


def tick(f=3200, d=0.06):
    t = tt(d)
    return (highpass(rng.standard_normal(len(t)), 2500) * np.exp(-t * 900) * 0.5
            + np.sin(2 * np.pi * f * t) * np.exp(-t * 160)) * np.minimum(1, t / 0.0005)


def flutter(d, rate=7.0):
    t = tt(d)
    n = bandpass(rng.standard_normal(len(t)), 180, 1600)
    am = 0.55 + 0.45 * np.sin(2 * np.pi * rate * t + 2 * np.sin(2 * np.pi * 0.7 * t))
    return n * am * env_adsr(len(t), 0.4, 0.8, d)


def whoosh(d, lo, hi, peak=0.8):
    t = np.linspace(0, 1, int(SR * d))
    n = rng.standard_normal(len(t))
    a, b = bandpass(n, lo, lo * 3), bandpass(n, hi / 3, hi)
    env = np.where(t < peak, (t / peak) ** 2.2, np.clip((1 - t) / (1 - peak), 0, 1) ** 1.4)
    return (a * (1 - t) + b * t) * env


def pen(d):
    t = tt(d)
    n = bandpass(rng.standard_normal(len(t)), 2200, 7000)
    jit = np.abs(np.sin(2 * np.pi * 5.3 * t) * np.sin(2 * np.pi * 2.1 * t + 1)) ** 0.6
    return n * jit * env_adsr(len(t), 0.05, 0.15, d)


def whistle(d=0.45):
    t = tt(d)
    f = 1100 + 1500 * (t / d) ** 0.7 + 40 * np.sin(2 * np.pi * 23 * t)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    hiss = bandpass(rng.standard_normal(len(t)), 3000, 9000) * 0.4
    return (tone * 0.5 + hiss) * np.minimum(1, t / 0.05) * (0.4 + 0.6 * t / d)


def burst(size=1.0):
    t = tt(2.2)
    f = 55 * (1 + 2 * np.exp(-t * 25))
    thump = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6)
    crack = bandpass(rng.standard_normal(len(t)), 400, 6000) * np.exp(-t * 30)
    tail = lowpass(rng.standard_normal(len(t)), 900) * np.exp(-t * 2.5) * 0.25
    return np.tanh((thump + crack * 1.3 + tail) * 1.4) * size


def crackle(d=1.4, density=90):
    out = np.zeros(int(SR * d))
    k = int(density * d)
    for _ in range(k):
        i = int(rng.uniform(0.15, 1) ** 0.6 * (len(out) - 600))
        c = highpass(rng.standard_normal(500), 2000) * np.exp(-np.arange(500) / 50) * rng.uniform(0.3, 1)
        out[i:i + 500] += c
    return out * np.linspace(1, 0.3, len(out))


# ---------------- seslendirme ----------------
# (kayıttaki başlangıç, bitiş, videodaki başlangıç) — kelime zamanları animation.html'deki yazılarla aynı
VO = [(0.0, 3.6, 0.5),       # Efendiler… yarın Cumhuriyet'i ilan edeceğiz.
      (4.4, 10.3, 4.8),      # 29 Ekim 1923. Saat 20.30… Cumhuriyet ilan edildi.
      (11.0, 24.1, 12.21),   # Gençliğe Hitabe
      (24.4, None, 31.05)]   # Cumhuriyetimizin yüz üçüncü yılı kutlu olsun!
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'ses/seslendirme.mp3', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                     capture_output=True, check=True).stdout
rec = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
rec = highpass(rec, 70)
vo = np.zeros((N, 2))
for i, (a, b, at) in enumerate(VO):
    seg = rec[int(a * SR): int(b * SR) if b else len(rec)].copy()
    f = int(0.03 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    act = np.abs(seg) > np.abs(seg).max() * 0.05                     # parçaları eşit yüksekliğe getir
    rms = np.sqrt((seg[act] ** 2).mean())
    place(vo, seg / rms * (0.71 if i == 0 else 1.0), at, gain=0.1)  # ilk cümle fısıltıya yakın: 3 dB alçak
vo_mono = vo[:, 0] / 1.414
# hafif sıkıştırma: yavaş RMS izleyici, -6 dB üstünde 2:1
env = np.sqrt(np.maximum(lowpass(vo_mono ** 2, 8), 1e-10))
thr = np.abs(vo_mono).max() * 0.25
comp = np.where(env > thr, (thr + (env - thr) / 2) / env, 1.0)
vo *= comp[:, None]
vo = vo / np.abs(vo).max() * 0.8
# konuşma zarfı: müziği kısmak için (hızlı atak, yavaş bırakma)
speech = (np.convolve(np.abs(vo_mono) > np.abs(vo_mono).max() * 0.04, np.ones(int(0.35 * SR)), 'same') > 0).astype(float)
duck_env = lowpass(speech, 3, 1)
duck_env = np.clip(duck_env / max(duck_env.max(), 1e-6), 0, 1)


# ---------------- müzik ----------------
music = np.zeros((N, 2))
CHORDS = [  # başlangıç, bitiş, akor, bas
    (0.0, 4.8, [50, 53, 57, 62], 38),          # Re minör
    (4.8, 6.4, [53, 58, 62, 65], 34),          # Si♭
    (6.4, 8.0, [53, 57, 60, 65], 45),          # Fa / La
    (8.0, 9.0, [55, 58, 62, 67], 43),          # Sol minör
    (9.0, 10.6, [57, 61, 64, 69], 45),         # La — "Cumhuriyet ilan edildi."
    (10.6, 12.0, [50, 54, 57, 62, 66], 38),    # Re majör — top atışları
    (12.0, 14.8, [53, 57, 62, 64], 38),        # Re minör 9 — Gençliğe Hitabe
    (14.8, 16.4, [53, 58, 62, 65], 46),        # Si♭
    (16.4, 18.0, [55, 60, 64, 67], 48),        # Do
    (18.0, 19.6, [53, 57, 60, 65], 41),        # Fa
    (19.6, 21.1, [55, 58, 62, 67], 43),        # Sol minör
    (21.1, 22.8, [53, 58, 62, 65], 46),        # Si♭
    (22.8, 24.8, [57, 62, 64, 69], 45),        # La sus4
    (24.8, 26.4, [57, 61, 64, 67], 45),        # La 7
] + [(a + SH, b + SH, c, d) for a, b, c, d in [
    (13.6, 15.2, [50, 54, 57, 62, 66], 38),    # Re majör (doruk)
    (15.2, 16.0, [55, 59, 62, 67], 43),        # Sol
    (16.0, 16.8, [57, 61, 64, 69], 45),        # La
    (16.8, 18.4, [54, 57, 62, 66, 69], 38),    # Re
    (18.4, 19.2, [55, 59, 62, 67], 38),        # Sol / Re
    (19.2, 20.0, [57, 61, 64, 69], 38),        # La / Re
    (20.0, DUR - SH, [50, 54, 57, 62, 66, 69], 38),  # Re
]]
for s, e, ch, bass in CHORDS:
    d = e - s
    soft = s < 4.8
    place(music, strings(ch, d, att=0.9 if soft else 0.35, rel=0.6, bright=1800 if soft else 2800), s, gain=0.22 if soft else 0.26)
    place(music, highpass(strings([bass, bass + 12], d, att=0.5, rel=0.6, bright=900), 45), s, gain=0.09)
    if s >= 13.6 + SH - 1e-6 or s == 10.6:
        o = s - SH
        place(music, brass([n + 12 for n in ch[-3:]] if (o < 16.8 and s != 10.6) else ch[-3:], d,
                           att=0.12 if (round(o, 1) in (13.6, 16.8, 20.0) or s == 10.6) else 0.3), s, gain=0.26 if s != 10.6 else 0.18)

# alçak yaylı ostinato (sekizlikler) 4.8 – 26.4
k = 4.8
while k < 26.4 - 1e-6:
    bass = [c for c in CHORDS if c[0] <= k + 1e-6][-1][3]
    nt = tt(0.36)
    o = saw(note(bass + 12), nt, 3, 0.08, seed=int(k * 10))
    o = lowpass(o, 1100) * np.exp(-nt * 5) * np.minimum(1, nt / 0.015)
    place(music, o, k, gain=0.1 if 10.6 <= k < 12.0 or k >= 22.8 else 0.07, pan=-0.2)
    k = round(k + BEAT / 2, 3)

# piyano: cümle başlarında ve vurgulu kelimelerde, seslendirmenin altında yumuşak
MEL = [(0.0, 62, 0.5), (0.5, 69, 0.6), (1.9, 74, 0.55), (3.2, 69, 0.5),
       (5.0, 70, 0.55), (7.3, 72, 0.5), (9.05, 73, 0.6), (10.6, 74, 0.8), (11.15, 78, 0.6), (11.7, 81, 0.6),
       (12.29, 74, 0.6), (13.7, 77, 0.65), (14.88, 74, 0.55), (16.33, 72, 0.45), (17.35, 70, 0.5),
       (18.2, 72, 0.55), (19.16, 76, 0.65), (19.84, 77, 0.55), (21.15, 74, 0.6), (22.76, 70, 0.5),
       (23.52, 74, 0.65), (24.34, 76, 0.6), (24.85, 73, 0.6)] + [(a + SH, n, v) for a, n, v in [
       (13.6, 74, 1.0), (14.4, 76, 0.8), (15.2, 74, 0.85), (16.0, 73, 0.8), (16.8, 74, 0.9), (18.4, 79, 0.6), (19.2, 76, 0.6), (20.0, 74, 0.8)]]
for at, n, v in MEL:
    place(music, piano(note(n), 3.2, v) + 0.3 * piano(note(n - 12), 3.2, v), at, gain=0.28, pan=0.15)

# ---------------- vurmalılar ----------------
perc = np.zeros((N, 2))
for i, at in enumerate(np.arange(0, 4.8, BEAT)):                                 # saat
    place(perc, tick(3300 if i % 2 == 0 else 2500), at, gain=0.08, pan=0.25)
place(perc, timpani(note(34), 2.2, 0.9), 4.8, gain=0.42)                          # kesme
for at in (22.8, 23.6, 24.4):                                                      # kalp atışı
    place(perc, timpani(note(38), 1.6, 0.8), at, gain=0.24)
    place(perc, timpani(note(38), 1.2, 0.5), at + 0.22, gain=0.2)
roll = np.arange(24.8, 26.35, 0.055)                                              # timpani tremolosu
for j, at in enumerate(roll):
    place(perc, timpani(note(45), 0.5, 0.25 + 0.75 * (j / len(roll)) ** 2), at, gain=0.22)
place(perc, reverse_swell(1.4), 26.4 - 1.4, gain=0.35)
place(perc, timpani(note(38), 2.6, 1.0), 26.4, gain=0.48)                         # doruk
place(perc, timpani(note(38), 2.0, 0.9), 26.4 + 0.4, gain=0.4)
place(perc, crash(4.0), 26.4, gain=0.24, pan=0.2)
place(perc, timpani(note(45), 1.8, 0.7), 16.0 + SH, gain=0.35)
place(perc, timpani(note(38), 2.6, 0.9), 16.8 + SH, gain=0.5)
place(perc, crash(3.0), 16.8 + SH, gain=0.18, pan=-0.2)
place(perc, timpani(note(38), 3.0, 1.0), 20.0 + SH, gain=0.5)
place(perc, crash(3.5), 20.0 + SH, gain=0.2)

# ---------------- efektler ----------------
sfx = np.zeros((N, 2))
place(sfx, reverse_swell(0.9), 4.8 - 0.9, gain=0.25)
place(sfx, cannon(3.2), 10.6, gain=0.85)                                           # top atışları
place(sfx, cannon(3.0, far=0.4), 11.15, gain=0.55, pan=-0.35)
place(sfx, cannon(3.0, far=0.8), 11.7, gain=0.4, pan=0.35)
for i, n in enumerate([86, 93, 98, 102]):                                         # ışık sızıntısı parıltısı
    place(sfx, bell(note(n), 2.0), 11.7 + i * 0.07, gain=0.03, pan=-0.4 + i * 0.27)
place(sfx, pen(1.1), 24.85, gain=0.05, pan=0.1)                                   # imza
place(sfx, whoosh(0.5, 120, 3000, 0.9), 13.1 + SH, gain=0.5)                       # bayrak inişi
place(sfx, flutter(4.0, 6.5), 13.4 + SH, gain=0.07)                                # dalgalanma
place(sfx, whoosh(1.4, 200, 2500, 0.5), 16.8 + SH, gain=0.18)                      # geri çekiliş
for i, n in enumerate([93, 98, 100, 105]):                                        # "29 EKİM" harfleri
    place(sfx, bell(note(n), 1.6), 17.75 + SH + i * 0.12, gain=0.03, pan=-0.3 + i * 0.2)
place(sfx, bell(note(86), 3.5), 20.6 + SH, gain=0.09, pan=-0.1)                   # logo çanı
place(sfx, bell(note(93), 3.2), 20.8 + SH, gain=0.06, pan=0.15)
for tb, x, kind, size in BURSTS:                                                  # havai fişekler
    pan = (x - 540) / 540 * 0.75
    place(sfx, whistle(0.45), tb - 0.45, gain=0.035 * size, pan=pan)
    place(sfx, burst(size), tb, gain=0.32 * size, pan=pan)
    if kind != 'red':
        place(sfx, crackle(1.5 if kind == 'gold' else 1.1, 120 if kind == 'white' else 70), tb + 0.25, gain=0.07 * size, pan=pan)

# ---------------- miks ----------------
bed = music + perc
bed = bed * 0.82 + reverb(music + perc * 0.6, 3.0, 2.0) * 0.38
fx = sfx * 0.82 + reverb(sfx, 2.2, 2.6, seed=9) * 0.25
bed *= (1 - 0.6 * duck_env)[:, None]                 # konuşurken müzik ~ -8 dB
fx *= (1 - 0.45 * duck_env)[:, None]
# seslendirme seviyesi: konuşulan yerlerde yatağın RMS'inin ~9 dB üstü
on = duck_env > 0.5
bed_rms = np.sqrt(((bed + fx)[on] ** 2).mean())
vo_rms = np.sqrt((vo[on] ** 2).mean())
vo *= bed_rms * 10 ** (9 / 20) / vo_rms
mix = bed + fx + vo + reverb(vo, 1.2, 4.0, seed=3, lp=4000) * 0.12
mt = np.arange(N) / SR
mix *= (np.minimum(1, mt / 0.02) * np.clip((DUR - mt) / 0.8, 0, 1))[:, None]
mix = highpass(mix.T, 35).T
mix = mix - 0.45 * lowpass(mix.T, 130).T  # telefon hoparlörü için alçak frekansları biraz kıs
mix = np.tanh(mix / np.abs(mix).max() * 1.4) / np.tanh(1.4) * 0.89  # yumuşak limit, ~ -1 dBFS
pcm = (np.clip(mix, -1, 1) * 32767).astype('<i2')
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('audio.wav yazıldı')
