"""Erdem Melih Reels için özgün müzik ve efekt (numpy sentezi; lisans sorunu yok).
96 BPM: 8 vuruş = 5,0 sn, logo vuruşu tam 5,0 sn'de. Çıktı: 48 kHz stereo WAV.
Kullanım: python3 audio/muzik.py <cikti.wav> [toplam_sn] [logodan_önceki_vuruş=8] [hışırtı_sn,hışırtı_sn...]
8 vuruşta ilk Reels'in müziği birebir üretilir; daha uzunda akorlar ölçü başına değişir (Lm–Fa–Rem–Lm … Mi)."""
import sys, wave
import numpy as np

SR = 48000
OUT = sys.argv[1]
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 8.5
BPM = 96.0
BEAT = 60.0 / BPM
NB = int(sys.argv[3]) if len(sys.argv) > 3 else 8
WHOOSH = [float(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 and sys.argv[4] else []
HIT = NB * BEAT  # 8 vuruşta 5,0 sn
N = int(DUR * SR)
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)

def t_(n): return np.arange(n) / SR
def add(buf, start, sig, gain=1.0):
    i = int(start * SR)
    if i >= N: return
    j = min(N, i + len(sig)); buf[i:j] += gain * sig[: j - i]
def addst(start, sig, gain=1.0, pan=0.0):
    add(L, start, sig, gain * np.sqrt((1 - pan) / 2)); add(R, start, sig, gain * np.sqrt((1 + pan) / 2))
def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
def lowpass(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))
def highpass(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR) + 1e-9
    return np.fft.irfft(X / np.sqrt(1 + (fc / f) ** 4), len(x))

# --- davul ---
def kick(dur=0.55):
    t = t_(int(dur * SR)); f = 46 + 110 * np.exp(-t * 32)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 6.5) + 0.25 * np.exp(-t * 300) * rng.standard_normal(len(t))
def hat(dur=0.06, dec=70):
    t = t_(int(dur * SR)); return highpass(rng.standard_normal(len(t)), 7000) * np.exp(-t * dec)
def snap(dur=0.25):
    t = t_(int(dur * SR)); n = highpass(rng.standard_normal(len(t)), 1500) * np.exp(-t * 22)
    return n + 0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)

# Giriş (0–5 sn): yumuşak davul; vuruş 2 ve 4'te parmak şıklatma
for b in range(NB):
    tb = b * BEAT
    if b % 4 in (0, 3) and b != NB - 1: addst(tb, kick(), 0.55)
    if b % 4 == 1: addst(tb, snap(), 0.16, 0.15)
    if b % 8 == 3: addst(tb + BEAT / 2, kick(), 0.35)
    for h in range(2):
        if b >= 2: addst(tb + h * BEAT / 2, hat(), 0.05 if h else 0.07, -0.3 + 0.6 * h)

# --- karanlık pad (La minör → Fa → La minör), yavaş açılan filtre ---
def pad(notes, dur, att=0.8, rel=1.0):
    t = t_(int(dur * SR)); s = np.zeros(len(t))
    for m in notes:
        for d in (-0.08, 0.0, 0.08):  # hafif detune
            s += np.sin(2 * np.pi * midi(m + d) * t + rng.uniform(0, 6)) + 0.3 * np.sin(4 * np.pi * midi(m + d) * t)
    env = np.minimum(1, t / att) * np.minimum(1, (dur - t) / rel)
    return lowpass(s * env, 900) / len(notes)
AKOR = {"Am": ([45, 52, 57, 60], 33), "F": ([41, 48, 57, 60], 29), "Dm": ([38, 50, 53, 57], 38), "E": ([40, 47, 56, 59], 28)}
BARS = NB // 4
PROG = ["Am"] * BARS if NB == 8 else [["Am", "F", "Dm", "Am"][i % 4] for i in range(BARS - 1)] + ["E"]
if NB == 8:
    addst(0.0, pad([45, 52, 57, 60], HIT + 0.3, att=1.5, rel=0.4), 0.10)
else:
    for i, c in enumerate(PROG):
        addst(i * 4 * BEAT, pad(AKOR[c][0], 4 * BEAT + 0.35, att=1.5 if i == 0 else 0.5, rel=0.4), 0.10)
addst(HIT, pad([41, 48, 57, 60, 64], DUR - HIT, att=0.05, rel=1.6), 0.12)

# --- alt bas ---
def sub(m, dur):
    t = t_(int(dur * SR)); env = np.minimum(1, t / 0.02) * np.exp(-t * 1.2)
    return np.tanh(1.5 * np.sin(2 * np.pi * midi(m) * t)) * env
for i, c in enumerate(PROG): addst(i * 4 * BEAT, sub(AKOR[c][1], 4 * BEAT), 0.20)
addst(HIT, sub(29, DUR - HIT), 0.26)

# --- çan/piyano arpej (dövme iğnesi gibi ince, metalik) ---
def bell(m, dur=1.6):
    t = t_(int(dur * SR)); f = midi(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 3) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6) \
        + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 9)
    return s * np.minimum(1, t / 0.004)
arp = [69, 72, 76, 72, 69, 72, 76, 79]
for st0 in range(2, NB - 3, 8):
    for i, m in enumerate(arp): addst(i * BEAT / 2 + st0 * BEAT, bell(m), 0.07, (-0.4, 0.4)[i % 2])
for i, m in enumerate([77, 76, 72, 69]): addst(HIT + 0.9 + i * BEAT, bell(m, 2.2), 0.06, (-0.3, 0.3)[i % 2])

# --- yükselen hışırtı (4,0 → 5,0) ve logo vuruşu ---
rl = 1.05; t = t_(int(rl * SR))
riser = highpass(rng.standard_normal(len(t)), 2500) * (t / rl) ** 2.5
addst(HIT - rl, riser, 0.10)
ti = t_(int(2.5 * SR))
boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-ti * 18)) / SR) * np.exp(-ti * 2.2)
crack = highpass(rng.standard_normal(len(ti)), 800) * np.exp(-ti * 25)
addst(HIT, boom, 0.7); addst(HIT, crack, 0.18)

# --- hızlanma geçişlerinde hışırtı (ortası verilen anda) ---
for wt in WHOOSH:
    d = 0.7; t = t_(int(d * SR)); env = np.sin(np.pi * t / d) ** 2
    w = lowpass(highpass(rng.standard_normal(len(t)), 400), 3500) * env
    addst(wt - d / 2, w, 0.12, -0.5); addst(wt - d / 2 + 0.05, w, 0.08, 0.5)

# --- yankı (üstel gürültü dürtüsü, FFT evrişimi) ---
def reverb(x, sec=2.2, mix=0.22, seed=1):
    r = np.random.default_rng(seed); n = int(sec * SR); tt = t_(n)
    ir = r.standard_normal(n) * np.exp(-tt * 6.9 / sec); ir = lowpass(ir, 5000); ir /= np.sqrt((ir ** 2).sum())
    m = len(x) + n; F = np.fft.rfft(x, m) * np.fft.rfft(ir, m)
    return x + mix * np.fft.irfft(F, m)[: len(x)]
L = reverb(L, seed=1); R = reverb(R, seed=2)
# Son 0,6 sn sönümlenme
fade = np.ones(N); k = int(0.6 * SR); fade[-k:] = np.linspace(1, 0, k) ** 2
L *= fade; R *= fade
pk = max(np.abs(L).max(), np.abs(R).max()); L, R = L / pk * 0.89, R / pk * 0.89
st = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print("ok", OUT, DUR, "sn; logo vuruşu", HIT)
