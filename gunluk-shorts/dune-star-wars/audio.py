"""
Dune × Star Wars — ses: heyecanlı seslendirme (tts.py) + sentezlenmiş müzik yatağı ve efektler, -14 LUFS.
Tüm efekt zamanları cues.py'den (görselle aynı veri). Konuşma sırasında müzik otomatik kısılır (ducking).
Çıktı: out/audio.wav (48 kHz stereo, tam T sn). Son 0.1 sn sessiz → döngüde kesintisiz bağlanır.
"""
import os
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

import cues
from engine import clamp, lerp, prog

SR = 48000
T = cues.T
N = int(round(SR * T))
rng = np.random.default_rng(1965)


def tt(d):
    return np.arange(int(SR * d)) / SR


def lp(x, fc, o=2):
    return sosfilt(butter(o, fc, "low", fs=SR, output="sos"), x)


def hp(x, fc, o=2):
    return sosfilt(butter(o, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)


def noise(d):
    n = rng.standard_normal(int(SR * d))
    return n / np.std(n)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


voice_buf = np.zeros((N, 2))
music_buf = np.zeros((N, 2))
sfx_buf = np.zeros((N, 2))
wet_buf = np.zeros((N, 2))


def place(buf, sig, at, gain=1.0, pan=0.0, send=0.0):
    i = int(round(at * SR))
    if i >= N or i < -len(sig):
        return
    s = sig
    if i < 0:
        s, i = s[-i:], 0
    s = s[: N - i]
    l = np.cos((pan + 1) * np.pi / 4) * 1.414
    r = np.sin((pan + 1) * np.pi / 4) * 1.414
    buf[i:i + len(s), 0] += s * gain * l
    buf[i:i + len(s), 1] += s * gain * r
    if send > 0:
        wet_buf[i:i + len(s), 0] += s * gain * l * send
        wet_buf[i:i + len(s), 1] += s * gain * r * send


# ───────────────────────── sesler ─────────────────────────
def whoosh(dur=0.4, up=True, bright=1.0):
    n = int(SR * dur)
    x = noise(dur)
    t = np.arange(n) / n
    fc = (300 + 4200 * bright * t ** 1.5) if up else (3500 * bright * (1 - t) ** 1.2 + 250)
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty(n)
    z = 0.0
    for i in range(n):
        z = (1 - a[i]) * x[i] + a[i] * z
        y[i] = z
    y = y - lp(y, 120)
    y = y * np.sin(np.pi * t) ** 1.5
    return y / (np.max(np.abs(y)) + 1e-9)


def thud(strength=1.0, d=0.8):
    t = tt(d)
    f = 48 + 70 * np.exp(-t / 0.05)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.2) + 0.7 * lp(noise(d), 700) * np.exp(-t / 0.06) + 0.3 * hp(noise(d), 2000) * np.exp(-t / 0.01)
    return np.tanh(1.4 * s * strength) * np.minimum(1, (d - t) / 0.1)


def pop(f0=650, f1=1100, d=0.12):
    t = tt(d)
    f = np.linspace(f0, f1, len(t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035)


def bell(f, d=0.9, tau=0.3):
    t = tt(d)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t / tau) + 0.5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / (tau * 0.5))
         + 0.25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / (tau * 0.25)))
    return s * np.minimum(1, (d - t) / 0.05)


def marimba(f, d=0.5):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.20) + 0.35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.05) + 0.1 * np.sin(2 * np.pi * 10 * f * t) * np.exp(-t / 0.02)
    return s * np.minimum(1, (d - t) / 0.05)


def pluck(f, d=0.4):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(4 * np.pi * f * t) + 0.15 * np.sin(6 * np.pi * f * t)
    return s * np.exp(-t / 0.16) * np.minimum(1, (d - t) / 0.04)


def uke(f, d=0.45):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(4 * np.pi * f * t) + 0.3 * np.sin(6 * np.pi * f * t) + 0.12 * np.sin(8 * np.pi * f * t)
    return s * np.exp(-t / 0.13) * np.minimum(1, (d - t) / 0.04)


def block(d=0.08):
    t = tt(d)
    return (bp(noise(d), 1500, 3500) * np.exp(-t / 0.012) + 0.8 * np.sin(2 * np.pi * 1000 * t) * np.exp(-t / 0.02)) * 0.8


def snare(d=0.14):
    t = tt(d)
    return (hp(noise(d), 1200) * np.exp(-t / 0.045) + 0.5 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.03))


def gunshot(d=0.16):
    t = tt(d)
    s = bp(noise(d), 700, 4200) * np.exp(-t / 0.022) + 0.8 * np.sin(2 * np.pi * (140 - 60 * t / d) * t) * np.exp(-t / 0.04) + 0.3 * hp(noise(d), 3000) * np.exp(-t / 0.006)
    return np.tanh(1.6 * s) / 1.2


def tick(f=3200, d=0.03):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.5 * hp(noise(d), 2500)) * np.exp(-t / 0.004)


def slide(f0, f1, d, wave="saw", cut=1400):
    t = tt(d)
    f = np.linspace(f0, f1, len(t))
    ph = np.cumsum(f) / SR
    s = 2 * (ph % 1) - 1 if wave == "saw" else np.sin(2 * np.pi * ph)
    s = lp(s, cut if wave == "saw" else 4000)
    return s * np.sin(np.pi * np.linspace(0, 1, len(t))) ** 0.5


def engine_loop(d, f=52):
    t = tt(d)
    wob = 1 + 0.35 * np.sin(2 * np.pi * 9 * t)
    ph = np.cumsum(f * wob) / SR
    s = 2 * (ph % 1) - 1
    s = lp(s, 520) + 0.4 * lp(noise(d), 300)
    return s * np.minimum(np.minimum(1, t / 0.1), np.minimum(1, (d - t) / 0.2))


def crash(d=1.0):
    t = tt(d)
    return hp(noise(d), 1500) * np.exp(-t / 0.3) * 0.7 + 0.6 * lp(noise(d), 300) * np.exp(-t / 0.15)


def make_ir(d=1.2):
    t = tt(d)
    ir = lp(noise(d) * np.exp(-t / 0.28), 5500)
    ir[:int(0.01 * SR)] = 0
    return ir / np.sqrt(np.sum(ir ** 2))


def crinkle(d=1.0, rate=60):
    s = np.zeros(int(SR * d))
    n = int(0.0065 * SR)
    for k in range(int(rate * d)):
        i = int(rng.random() * (len(s) - n - 10))
        s[i:i + n] += hp(noise(0.0065), 3500) * np.exp(-np.arange(n) / SR / 0.0015) * (0.4 + 0.6 * rng.random())
    return s * np.sin(np.pi * np.linspace(0, 1, len(s))) ** 0.7


# ───────────────────────── titanik'e özgü sesler ─────────────────────────
def sonar(d=1.6, f=1180):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.09) + 0.3 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / 0.05)
    return s * np.minimum(1, t / 0.004)


def key_tick(d=0.05):
    t = tt(d)
    return (hp(noise(d), 1800) * np.exp(-t / 0.006) + 0.5 * np.sin(2 * np.pi * 420 * t) * np.exp(-t / 0.012)) * 0.8


def tink(f=1568, d=0.5):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.18) + 0.4 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t / 0.08)
    return s * np.minimum(1, t / 0.003) * np.minimum(1, (d - t) / 0.05)


def ice_crack(d=1.1):
    t = tt(d)
    s = hp(noise(d), 2500) * np.exp(-t / 0.05) * 0.8
    for k in range(7):
        i = int(SR * (0.03 + 0.05 * k + 0.02 * rng.random()))
        n = int(0.012 * SR)
        if i + n < len(s):
            s[i:i + n] += hp(noise(0.012), 3000) * np.exp(-np.arange(n) / SR / 0.003) * 0.8
    s += 0.9 * lp(noise(d), 260) * np.exp(-t / 0.22) + 0.7 * np.sin(2 * np.pi * (55 - 20 * t) * t) * np.exp(-t / 0.4)
    return np.tanh(1.3 * s) * np.minimum(1, (d - t) / 0.1)


def metal_groan(d=1.4, f=70):
    t = tt(d)
    fm = f * (1 + 0.04 * np.sin(2 * np.pi * 3.5 * t) + 0.25 * t / d)
    ph = np.cumsum(fm) / SR
    s = lp(2 * (ph % 1) - 1, 380) * np.sin(np.pi * t / d) ** 0.8
    return s


def dark_pad(f, d):
    t = tt(d)
    s = 0
    for r, g in ((1.0, 1.0), (1.5, 0.5), (2.0, 0.35), (2.996, 0.15)):
        ph = np.cumsum(f * r * (1 + 0.003 * np.sin(2 * np.pi * 0.3 * t * r))) / SR
        s = s + g * (2 * (ph % 1) - 1)
    s = lp(s, 650)
    return s * np.minimum(np.minimum(1, t / 0.8), np.minimum(1, (d - t) / 0.8))


def heart(d=0.35):
    t = tt(d)
    f = 52 + 40 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.09)


def sting(f=311, d=2.0):
    t = tt(d)
    s = sum(g * np.sin(2 * np.pi * f * r * t) for r, g in ((1, 1), (1.19, 0.6), (1.68, 0.5), (2, 0.4))) * np.exp(-t / 0.7)
    return s * np.minimum(1, t / 0.01) * np.minimum(1, (d - t) / 0.1)


def load_voice():
    w = wave.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "voice.wav"))
    x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768
    y = np.zeros(N)
    y[:min(N, len(x))] = x[:N]
    return y


def buzz(d=0.9, f=520, ramp=False):
    """Sivrisinek vızıltısı: titreyen yüksek ton + genlik modülasyonu"""
    t = tt(d)
    wob = f * (1 + 0.035 * np.sin(2 * np.pi * 6 * t) + 0.02 * np.sin(2 * np.pi * 13.7 * t))
    ph = 2 * np.pi * np.cumsum(wob) / SR
    s_ = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.28 * np.sin(3 * ph)
    am = 0.62 + 0.38 * np.sin(2 * np.pi * 36 * t)
    env = np.minimum(1, t / 0.06) * np.minimum(1, (d - t) / 0.18)
    if ramp:
        env = env * (0.15 + 0.85 * (t / d) ** 1.6)
    return bp(s_ * am * env, 280, 2600) * 0.5


def hiss(d=0.9):
    t = tt(d)
    return hp(noise(d), 3500) * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.2) * 0.5


def burst_pops(t0, t1, n, gain=0.14, seed=3):
    r = np.random.default_rng(seed)
    for i in range(n):
        at = t0 + (t1 - t0) * (i / max(1, n - 1)) ** 0.8
        place(sfx_buf, pop(500 + 900 * r.random(), 900 + 900 * r.random(), 0.09), at, gain * (0.6 + 0.6 * r.random()), pan=-0.8 + 1.6 * r.random(), send=0.1)


def wind(d=12.0):
    """Çöl rüzgârı: bant geçiren gürültü + yavaş dalgalanma"""
    t = tt(d)
    y = bp(noise(d), 240, 1500)
    lfo = 0.55 + 0.45 * np.sin(2 * np.pi * 0.11 * t + 1.3) * np.sin(2 * np.pi * 0.047 * t + 0.4)
    return y * lfo * np.minimum(1, t / 1.5) * np.minimum(1, (d - t) / 1.5)


def rumble(d=2.5, f=38):
    """Kum kurdu: çok alçak gümbürtü"""
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.06 * np.sin(2 * np.pi * 0.7 * t))) / SR
    s = np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.8 * lp(noise(d), 110)
    return s * np.sin(np.pi * t / d) ** 1.4


def chalk(d=0.07):
    t = tt(d)
    return hp(noise(d), 2400) * np.exp(-t / 0.025) * (0.6 + 0.4 * np.sin(2 * np.pi * 70 * t)) * 0.8


def typed(t0, t1, n, gain=0.12, seed=1):
    r = np.random.default_rng(seed)
    for i in range(n):
        place(sfx_buf, key_tick(), t0 + (t1 - t0) * i / max(1, n - 1), gain * (0.7 + 0.5 * r.random()), pan=-0.2 + 0.4 * r.random())


def build():
    v = load_voice()
    voice_buf[:, 0] = v
    voice_buf[:, 1] = v
    hop = int(0.01 * SR)
    env = np.array([np.sqrt(np.mean(v[i:i + 4 * hop] ** 2)) for i in range(0, N - 4 * hop, hop)])
    env = np.minimum(1, env / 0.12)
    env = np.convolve(env, np.ones(12) / 12, mode="same")
    duck = np.interp(np.arange(N) / SR, np.arange(len(env)) * hop / SR, 1 - 0.85 * env)
    duck_sfx = np.interp(np.arange(N) / SR, np.arange(len(env)) * hop / SR, 1 - 0.40 * env)
    S, E, W_ = cues.st, cues.en, cues.wt
    Tm = T - 0.12

    # ---- müzik yatağı: Frig modu pad + rüzgâr + yumuşak davul nabzı
    roots = [73.4, 77.8, 65.4, 87.3, 73.4, 82.4]
    k, t0 = 0, 0.0
    while t0 < Tm - 2:
        f = roots[k % len(roots)]
        d = min(10.5, Tm - t0)
        place(music_buf, dark_pad(f, d), t0, 0.28, pan=-0.1)
        place(music_buf, dark_pad(f * 3, d), t0, 0.10, pan=0.3, send=0.2)
        k += 1
        t0 += 9.0
    for t0 in np.arange(0.0, Tm, 11.0):
        place(music_buf, wind(13.0), t0, 0.30, pan=(-0.3 if int(t0 / 11) % 2 else 0.3))
    tm = 14.0
    while tm < Tm - 2:
        inten = 0.45 + 0.55 * max(prog(tm, S("D0"), S("D3")) * (1 - prog(tm, E("D5"), E("D5") + 3)), prog(tm, S("G1"), E("G2")))
        place(music_buf, thud(0.5), tm, 0.20 * inten, send=0.1)
        tm += 2.3

    # ---- geçişler
    for tb, kind in cues.TRANS:
        if kind in ("whip", "up"):
            place(sfx_buf, whoosh(0.4, True, 0.8), tb - 0.17, 0.34, send=0.1)
        else:
            place(sfx_buf, whoosh(0.34, False, 0.9), tb - 0.17, 0.30, send=0.1)
            place(sfx_buf, thud(0.5), tb, 0.24)
    # ---- açılış kartı
    place(sfx_buf, thud(1.0), 0.0, 0.5, send=0.2)
    place(sfx_buf, sting(220, 1.8), 0.02, 0.16, send=0.4)
    place(sfx_buf, whoosh(0.5, False, 1.0), 0.85, 0.3)
    # ---- A1–A3
    place(sfx_buf, tink(1318), W_("A1", 7), 0.2, send=0.4)
    place(sfx_buf, metal_groan(1.8, 58), W_("A1", 11), 0.18, send=0.3)
    t = W_("A2", 2)
    place(sfx_buf, block(), t, 0.35)
    place(sfx_buf, thud(0.6), t, 0.28)
    place(sfx_buf, whoosh(0.9, True, 0.6), W_("A2", 5), 0.24)
    t = W_("A2", 11)
    place(sfx_buf, thud(0.7), t, 0.28)
    place(sfx_buf, crinkle(0.4, 40), t, 0.18)
    place(sfx_buf, slide(500, 1100, 0.5, "sine", 3000), W_("A3", 6), 0.12)
    place(sfx_buf, tink(1568, 0.5), W_("A3", 8), 0.25, send=0.4)
    place(sfx_buf, whoosh(0.5, True, 0.6), W_("A3", 9), 0.24)
    t = W_("A3", 13)
    place(sfx_buf, thud(1.0), t, 0.5, send=0.3)
    place(sfx_buf, block(), t, 0.4)
    # ---- B: roman
    t = W_("B1", 2)
    place(sfx_buf, thud(0.9), t, 0.4, send=0.3)
    place(sfx_buf, sting(196, 2.0), t, 0.15, send=0.5)
    place(sfx_buf, pop(500, 800, 0.1), W_("B1", 3), 0.2)
    place(sfx_buf, rumble(3.2, 40), W_("B1", 11) - 0.1, 0.22, send=0.2)
    for i, wi in enumerate((11, 12, 13)):
        place(sfx_buf, bell(880 + 110 * i, 1.2, 0.5), W_("B1", wi), 0.10, pan=-0.3 + 0.3 * i, send=0.5)
    n = 9
    for i in range(n):
        place(sfx_buf, crinkle(0.35, 50), S("B2") + 0.1 + i * (E("B2") + 0.5 - S("B2") - 0.1) / n * 0.9, 0.16, pan=-0.6 + 1.2 * rng.random())
    typed(S("B2"), E("B2") + 0.2, 20, 0.11, 2)
    t = W_("B3", 2)
    place(sfx_buf, sting(330, 2.4), t, 0.2, send=0.5)
    for i in range(5):
        place(sfx_buf, bell(1318 * (1 + 0.25 * i), 1.0, 0.4), t + 0.06 * i, 0.08, pan=-0.4 + 0.2 * i, send=0.5)
    # ---- C: Star Wars 1977
    for i in range(int((W_("C2", 0) - S("C1")) / 0.25)):
        place(sfx_buf, tick(2400, 0.02), S("C1") + i * 0.25, 0.10)
    place(sfx_buf, thud(0.8), S("C1") + 0.45, 0.35, send=0.2)
    for ts in (W_("C2", 5), W_("C2", 9), W_("C2", 13)):
        place(sfx_buf, whoosh(0.3, True, 0.7), ts - 0.1, 0.22)
        place(sfx_buf, tink(1760, 0.4), ts + 0.3, 0.16, send=0.4)
    place(sfx_buf, slide(900, 120, 0.3, "saw", 2000), W_("C3", 2), 0.12)
    place(sfx_buf, thud(0.9), W_("C3", 8), 0.4, send=0.3)
    # ---- D: beş benzerlik
    for i in range(5):
        place(sfx_buf, tink(1046 + 130 * i, 0.4), W_("D0", 2) + 0.1 * i, 0.16, send=0.4)
    rv = {1: (W_("D1", 6), W_("D1", 8), W_("D1", 8)), 2: (W_("D2", 3), W_("D2", 5), W_("D2", 8)), 3: (W_("D3", 2), W_("D3", 3), W_("D3", 3)),
          4: (W_("D4", 1), W_("D4", 2), W_("D4", 6)), 5: (W_("D5", 2), W_("D5", 4), W_("D5", 4))}
    popi = {1: 8, 2: 10, 3: 4, 4: 8, 5: 9}
    for k in range(1, 6):
        sid = f"D{k}"
        place(sfx_buf, tink(1568, 0.4), W_(sid, 0) + 0.25, 0.20, send=0.4)
        place(sfx_buf, whoosh(0.35, True, 0.5), S(sid) - 0.06, 0.22)
        a_, s_, b_ = rv[k]
        place(sfx_buf, pop(600, 900, 0.12), a_, 0.22, pan=-0.5, send=0.2)
        place(sfx_buf, pop(500, 800, 0.12), s_, 0.22, pan=0.5, send=0.2)
        if b_ > max(a_, s_) - 0.01 and k in (2, 5):
            place(sfx_buf, whoosh(0.5, True, 0.5), b_ - 0.05, 0.18)
        tp = cues.we(sid, popi[k])
        place(sfx_buf, thud(0.7), tp, 0.34, send=0.2)
        place(sfx_buf, tink(2093, 0.5), tp + 0.03, 0.18, send=0.4)
    place(sfx_buf, rumble(2.4, 40), rv[3][0] - 0.1, 0.22, send=0.2)
    for i in range(6):
        place(sfx_buf, bell(1568 * (1 + 0.2 * i), 0.9, 0.35), rv[4][0] + 0.05 * i, 0.07, pan=-0.4 + 0.16 * i, send=0.5)
    typed(rv[4][2], rv[4][2] + 0.5, 26, 0.10, 3)
    # ---- E: Herbert, Lucas
    place(sfx_buf, whoosh(0.5, True, 0.5), S("E1"), 0.24)
    typed(W_("E1", 9), cues.we("E1", 14), 46, 0.11, 4)
    place(sfx_buf, thud(0.8), W_("E1", 4), 0.30, send=0.2)
    place(sfx_buf, block(), W_("E1", 4), 0.25)
    place(sfx_buf, thud(1.0), S("E2") + 0.2, 0.34, send=0.3)
    for i in range(16):
        place(sfx_buf, chalk(), W_("E2", 5) + (cues.we("E2", 8) - W_("E2", 5)) * i / 15, 0.18, pan=-0.3 + 0.1 * (i % 5))
    place(sfx_buf, tink(1318, 0.5), cues.we("E2", 8), 0.22, send=0.4)
    place(sfx_buf, pop(600, 900, 0.12), W_("E2", 11), 0.2)
    place(sfx_buf, whoosh(0.4, True, 0.5), S("E3") + 0.1, 0.2)
    place(sfx_buf, pop(500, 800, 0.12), W_("E3", 3), 0.2)
    typed(W_("E3", 4), cues.we("E3", 10), 33, 0.10, 5)
    place(sfx_buf, thud(0.8), W_("E3", 9), 0.32, send=0.3)
    # ---- F: atalar, uyarı
    place(sfx_buf, slide(300, 900, 1.6, "sine", 2400), W_("F1", 4) - 0.1, 0.10)
    for ts in (W_("F1", 8), W_("F1", 11)):
        place(sfx_buf, thud(0.5), ts, 0.22)
        place(sfx_buf, tink(1318, 0.4), ts + 0.05, 0.16, send=0.4)
    place(sfx_buf, thud(0.8), S("F2") + 0.15, 0.30, send=0.3)
    place(sfx_buf, wind(5.0), S("F2"), 0.20)
    t = W_("F2", 4)
    place(sfx_buf, tink(1760, 0.5), t, 0.24, send=0.4)
    place(sfx_buf, metal_groan(1.6, 55), t, 0.18, send=0.3)
    t = W_("F2", 12)
    place(sfx_buf, crash(0.8), t, 0.20, send=0.2)
    for i in range(6):
        place(sfx_buf, tick(900, 0.03), t + 0.15 + 0.11 * i, 0.12)
    # ---- G: teklif
    place(sfx_buf, whoosh(0.5, True, 0.5), W_("G1", 5) - 0.1, 0.22)
    for i in range(3):
        place(sfx_buf, block(), W_("G1", 9) + 0.28 * i, 0.38)
    t = W_("G2", 2)
    place(sfx_buf, thud(1.0), t, 0.42, send=0.3)
    place(sfx_buf, block(), t, 0.35)
    place(sfx_buf, whoosh(0.5, True, 0.6), W_("G2", 5) - 0.5, 0.22)
    t = W_("G2", 5)
    place(sfx_buf, snare(), t - 0.02, 0.5)
    place(sfx_buf, thud(1.1), t, 0.5, send=0.3)
    place(sfx_buf, sting(207, 2.4), t, 0.2, send=0.5)
    place(sfx_buf, slide(300, 800, 0.5, "sine", 2400), W_("G3", 1), 0.10)
    place(sfx_buf, slide(300, 700, 0.5, "sine", 2400), W_("G3", 2), 0.10)
    place(sfx_buf, thud(1.0), W_("G3", 3), 0.44, send=0.3)
    place(sfx_buf, pop(600, 900, 0.12), W_("G4", 2), 0.2)
    place(sfx_buf, block(), W_("G4", 5), 0.25)
    place(sfx_buf, whoosh(0.4, True, 0.5), W_("G4", 10) - 0.1, 0.22)
    typed(W_("G4", 10), cues.we("G4", 16), 50, 0.10, 6)
    # ---- H: hüküm ve kart
    for tt_ in (W_("H1", 5), W_("H1", 8)):
        place(sfx_buf, thud(0.9), tt_, 0.38, send=0.3)
        place(sfx_buf, block(), tt_, 0.28)
    for i in range(26):
        place(sfx_buf, tick(700, 0.03), W_("H1", 6) + (cues.we("H1", 8) + 0.6 - W_("H1", 6)) * i / 25, 0.08, pan=-0.3 + 0.6 * (i % 2))
    for wi in (1, 3, 6):
        place(sfx_buf, pop(600, 900, 0.12), W_("H2", wi) - 0.05, 0.18)
    card_t = W_("H2", 5) - 0.15
    place(sfx_buf, whoosh(0.5, False, 0.9), card_t - 0.1, 0.3)
    place(sfx_buf, thud(0.9), card_t + 0.35, 0.45, send=0.3)
    place(sfx_buf, sonar(1.4, 880), card_t + 0.5, 0.2, send=0.5)

    ir = make_ir()
    for ch in range(2):
        sfx_buf[:, ch] += fftconvolve(wet_buf[:, ch], ir)[:N] * 0.5
    music = music_buf * 0.15
    for ch in range(2):
        music[:, ch] *= duck
    sfx = sfx_buf * 0.7
    for ch in range(2):
        sfx[:, ch] *= duck_sfx
    return voice_buf * 1.0 + music + sfx


def wood_tok_():
    d = 0.05
    t = tt(d)
    return (np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.008) + 0.5 * hp(noise(d), 2000) * np.exp(-t / 0.004)) * 0.8


# ───────────────────────── mastering ─────────────────────────
def lufs(x):
    import pyloudnorm as pyln
    return pyln.Meter(SR).integrated_loudness(x)


CEIL_DB = -2.5   # örnek tepe tavanı (dBFS); AAC sonrası true peak ≤ −1 dBTP hedefi


def master(x):
    # son 0.1 sn tam sessiz (döngüde kesintisiz bağlanır); ilk örnekte yumuşak giriş
    tail = int(0.10 * SR)
    fo = int(0.03 * SR)
    x[-tail - fo:-tail] *= np.linspace(1, 0, fo)[:, None]
    x[-tail:] = 0.0
    x[:int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))[:, None]
    sos = butter(2, 30, "high", fs=SR, output="sos")
    x = np.stack([sosfilt(sos, x[:, 0]), sosfilt(sos, x[:, 1])], axis=1)
    # Anayasa: kodlanmış mp4'te −14 LUFS ±1 ve ≤ −1 dBTP. Sert kırpma yerine ileri-bakışlı (lookahead) limiter:
    # tepe, 10 ms pencerede minimum kazanç + hareketli ortalama ile yumuşatılır (bozulma/pompalama düşük).
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    ceil = 10 ** (CEIL_DB / 20)
    n = int(0.010 * SR)

    def limit(y):
        from scipy.signal import resample_poly
        y4 = resample_poly(y, 4, 1, axis=0)                      # 4x aşırı örnek: örnekler arası (true) tepe
        env = np.abs(y4).max(axis=1)[: len(y) * 4].reshape(-1, 4).max(axis=1)
        gain = np.minimum(1.0, ceil / (env + 1e-9))
        gain = uniform_filter1d(minimum_filter1d(gain, size=2 * n, mode="nearest"), size=n, mode="nearest")
        gain = np.minimum(gain, np.minimum(1.0, ceil / (env + 1e-9)))   # güvenlik: asla tavanı aşma
        z = y * gain[:, None]
        z[-tail:] = 0.0
        return z

    g = 1.0
    z = x
    for _ in range(12):
        z = limit(x * g)
        L = lufs(z)
        if abs(L + 14.0) < 0.05:
            break
        g *= 10 ** ((-14.0 - L) / 20)
    return z, lufs(z)


def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    out, L = master(build())
    write_wav(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "audio.wav"), out)
    print(f"audio.wav: {len(out)/SR:.3f} sn, entegre {L:.2f} LUFS, tepe {20*np.log10(np.max(np.abs(out))):.2f} dBFS")
