"""
Pellagra: Mikrop Değildi (TESLİMAT #7) — ses: kuru anlatıcı (tts.py) + ortak müzik yatağı + sahneye bağlı efektler, −14 LUFS.
Tüm efekt zamanları cues.py'den (görselle aynı veri). Konuşma sırasında müzik/efekt otomatik kısılır (ducking: müzik 0,85, efekt 0,40).
Kare 0'da tek imza vuruşu (≤0,25 sn), yatak 3. sn'de girer, son 0,1 sn sessiz → döngüde kesintisiz bağlanır.
Çıktı: out/audio.wav (48 kHz stereo, tam T sn).
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
rng = np.random.default_rng(1916)
HERE = os.path.dirname(os.path.abspath(__file__))


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


def tink(f=1568, d=0.5):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.18) + 0.4 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t / 0.08)
    return s * np.minimum(1, t / 0.003) * np.minimum(1, (d - t) / 0.05)


def block(d=0.08):
    t = tt(d)
    return (bp(noise(d), 1500, 3500) * np.exp(-t / 0.012) + 0.8 * np.sin(2 * np.pi * 1000 * t) * np.exp(-t / 0.02)) * 0.8


def snare(d=0.14):
    t = tt(d)
    return hp(noise(d), 1200) * np.exp(-t / 0.045) + 0.5 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.03)


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


def crash(d=1.0):
    t = tt(d)
    return hp(noise(d), 1500) * np.exp(-t / 0.3) * 0.7 + 0.6 * lp(noise(d), 300) * np.exp(-t / 0.15)


def rumble(d=2.5, f=38):
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.06 * np.sin(2 * np.pi * 0.7 * t))) / SR
    s = np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.8 * lp(noise(d), 110)
    return s * np.sin(np.pi * t / d) ** 1.4


def metal_groan(d=1.4, f=70):
    t = tt(d)
    fm = f * (1 + 0.04 * np.sin(2 * np.pi * 3.5 * t) + 0.25 * t / d)
    ph = np.cumsum(fm) / SR
    return lp(2 * (ph % 1) - 1, 380) * np.sin(np.pi * t / d) ** 0.8


def sting(f=311, d=2.0):
    t = tt(d)
    s = sum(g * np.sin(2 * np.pi * f * r * t) for r, g in ((1, 1), (1.19, 0.6), (1.68, 0.5), (2, 0.4))) * np.exp(-t / 0.7)
    return s * np.minimum(1, t / 0.01) * np.minimum(1, (d - t) / 0.1)


def dark_pad(f, d):
    t = tt(d)
    s = 0
    for r, g in ((1.0, 1.0), (1.5, 0.5), (2.0, 0.35), (2.996, 0.15)):
        ph = np.cumsum(f * r * (1 + 0.003 * np.sin(2 * np.pi * 0.3 * t * r))) / SR
        s = s + g * (2 * (ph % 1) - 1)
    s = lp(s, 650)
    return s * np.minimum(np.minimum(1, t / 0.8), np.minimum(1, (d - t) / 0.8))


def make_ir(d=1.2):
    t = tt(d)
    ir = lp(noise(d) * np.exp(-t / 0.28), 5500)
    ir[:int(0.01 * SR)] = 0
    return ir / np.sqrt(np.sum(ir ** 2))


def gulp(d=0.18):
    """Yutkunma: alçalan kısa 'glup' + boğaz gürültüsü."""
    t = tt(d)
    f = 230 * np.exp(-t / 0.045) + 70
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.07) + 0.35 * lp(noise(d), 500) * np.exp(-t / 0.05)
    return s * np.minimum(1, t / 0.004) * np.minimum(1, (d - t) / 0.03)


def plop(d=0.14):
    t = tt(d)
    f = 520 * np.exp(-t / 0.03) + 120
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05)


def chew(d=0.07):
    t = tt(d)
    return lp(noise(d), 900) * np.exp(-t / 0.02) * 0.7


def hiss(d=0.9, hi=3500):
    t = tt(d)
    return hp(noise(d), hi) * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.2) * 0.5


def rain(d=4.0):
    t = tt(d)
    return (hp(noise(d), 2600) * 0.5 + bp(noise(d), 600, 1800) * 0.25) * np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.6)


def buzz(d=0.9, f=520):
    t = tt(d)
    wob = f * (1 + 0.035 * np.sin(2 * np.pi * 6 * t) + 0.02 * np.sin(2 * np.pi * 13.7 * t))
    ph = 2 * np.pi * np.cumsum(wob) / SR
    s_ = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.28 * np.sin(3 * ph)
    am = 0.62 + 0.38 * np.sin(2 * np.pi * 36 * t)
    env = np.minimum(1, t / 0.06) * np.minimum(1, (d - t) / 0.18)
    return bp(s_ * am * env, 280, 2600) * 0.5


def load_voice():
    w = wave.open(os.path.join(HERE, "out", "voice.wav"))
    x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768
    y = np.zeros(N)
    y[:min(N, len(x))] = x[:N]
    return y


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
    We = cues.we
    Tm = T - 0.12

    # ---- müzik yatağı (ortak palet): Frig modu karanlık pad + yumuşak nabız; 0–3 sn arası yok, 3. sn'de girer
    roots = [73.4, 77.8, 65.4, 87.3, 73.4, 82.4]
    k, t0 = 0, 2.8
    while t0 < Tm - 2:
        f = roots[k % len(roots)]
        d = min(10.5, Tm - t0)
        place(music_buf, dark_pad(f, d), t0, 0.28, pan=-0.1)
        place(music_buf, dark_pad(f * 3, d), t0, 0.10, pan=0.3, send=0.2)
        k += 1
        t0 += 9.0
    tm = 3.2
    while tm < Tm - 2:
        inten = 0.40 + 0.60 * max(prog(tm, S("D2"), S("D4")) * (1 - prog(tm, E("D4"), E("D4") + 2.5)), prog(tm, S("F3"), E("F4b")))
        place(music_buf, thud(0.5), tm, 0.18 * inten, send=0.1)
        tm += 2.5                                  # 96 BPM: 1 ölçü = 2,5 sn
    place(sfx_buf, rain(E("F5") - S("F5") + 1.4), S("F5") - 0.5, 0.20)   # fırtına: yağmur

    # ---- geçişler
    for tb, kind in cues.TRANS:
        if kind in ("whip", "up"):
            place(sfx_buf, whoosh(0.4, True, 0.8), tb - 0.17, 0.34, send=0.1)
        else:
            place(sfx_buf, whoosh(0.34, False, 0.9), tb - 0.17, 0.30, send=0.1)
            place(sfx_buf, thud(0.5), tb, 0.24)

    # ---- kare 0: tek imza vuruşu (≤0,25 sn) + kanca
    place(sfx_buf, thud(0.22), 0.0, 0.55)
    place(sfx_buf, block(), 0.0, 0.25)
    place(sfx_buf, thud(0.7), W_("A2", 0) - 0.02, 0.30, send=0.2)
    place(sfx_buf, sting(196, 1.8), W_("A2", 0), 0.10, send=0.5)

    # ---- B: güney, belirtiler, mikrop arayan doktorlar
    place(sfx_buf, tink(1318, 0.6), W_("B1", 8) - 0.1, 0.18, send=0.4)
    place(sfx_buf, block(), W_("B1", 8) - 0.1, 0.30)
    place(sfx_buf, thud(0.6), W_("B1", 8) - 0.1, 0.24)
    for wi in (0, 2, 3, 4):
        place(sfx_buf, pop(600 + 80 * wi, 900 + 90 * wi, 0.12), W_("B2", wi) - 0.05, 0.22, pan=-0.5 + 0.33 * wi, send=0.2)
    place(sfx_buf, thud(0.9), W_("B2", 4), 0.30, send=0.3)
    place(sfx_buf, buzz(1.0, 330), W_("B2", 3), 0.06)
    place(sfx_buf, pop(500, 800, 0.1), W_("B3", 4) - 0.05, 0.22)
    place(sfx_buf, buzz(1.6, 520), W_("B3", 4), 0.10, send=0.2)
    place(sfx_buf, sting(207, 2.0), W_("B3", 4), 0.12, send=0.5)

    # ---- C: yetimhane
    t = W_("C1", 0) - 0.05
    place(sfx_buf, thud(0.8), t, 0.32, send=0.2)
    place(sfx_buf, block(), t, 0.28)
    for ts in (W_("C1", 8) - 0.12, W_("C1", 10) - 0.12, S("C2") - 0.08):
        place(sfx_buf, whoosh(0.26, True, 0.7), ts - 0.12, 0.26)
    place(sfx_buf, pop(600, 900, 0.12), W_("C1", 8) - 0.05, 0.22)
    place(sfx_buf, pop(700, 1100, 0.12), W_("C1", 10) - 0.05, 0.22)
    place(sfx_buf, tink(1568, 0.5), We("C1", 11) + 0.02, 0.22, send=0.4)          # kanıt 1
    place(sfx_buf, bell(988, 1.2, 0.5), We("C1", 11) + 0.04, 0.10, send=0.5)
    place(sfx_buf, pop(500, 800, 0.12), S("C2") + 0.1, 0.22)
    place(sfx_buf, buzz(1.4, 480), W_("C2", 0), 0.08, send=0.2)
    place(sfx_buf, thud(0.7), W_("C2", 4) + 0.2, 0.30, send=0.3)
    place(sfx_buf, crash(0.6), W_("C2", 4) + 0.2, 0.16)

    # ---- D: şüpheciler, kanıt 2 (kirli parti)
    place(sfx_buf, pop(450, 650, 0.14), W_("D0", 1) - 0.05, 0.26)
    for i, tz in enumerate((W_("D1", 0) - 0.1, W_("D1", 0) + 0.18, W_("D1", 0) + 0.46)):
        place(sfx_buf, thud(0.4), tz, 0.14, pan=0.2 * i)
    place(sfx_buf, tink(1760, 0.5), W_("D1", 3) + 0.3, 0.18, send=0.4)
    t = cues.STAMP_YEAR
    place(sfx_buf, thud(1.0), t, 0.40, send=0.3)
    place(sfx_buf, block(), t, 0.34)
    for i in range(5):                               # kadeh gibi kalkan haplar
        place(sfx_buf, pop(500 + 70 * i, 800 + 70 * i, 0.1), W_("D2", 1) + 0.15 * i + 0.1, 0.14, pan=-0.6 + 0.3 * i)
    tg = W_("D2", 11)
    for i in range(5):                               # yutkunma
        place(sfx_buf, gulp(), tg + 0.04 * i, 0.30, pan=-0.6 + 0.3 * i, send=0.15)
    place(sfx_buf, thud(0.9), tg + 0.1, 0.22, send=0.3)
    for i in range(5):                               # onay işaretleri
        place(sfx_buf, tink(1046 + 150 * i, 0.5), S("D3") + 0.18 * i, 0.20, pan=-0.6 + 0.3 * i, send=0.4)
    place(sfx_buf, bell(1318, 1.6, 0.6), We("D3", 2), 0.12, send=0.5)             # kanıt 2
    t = cues.STAMP_WARN
    place(sfx_buf, snare(), t - 0.02, 0.50)
    place(sfx_buf, thud(1.1), t, 0.50, send=0.3)
    place(sfx_buf, block(), t, 0.34)
    place(sfx_buf, sting(185, 2.4), t, 0.18, send=0.5)

    # ---- E: tabak, diyet, hapishane
    for wi in range(4):
        place(sfx_buf, pop(700 + 60 * wi, 1000 + 80 * wi, 0.1), W_("E0", wi) - 0.05, 0.18, pan=-0.5 + 0.33 * wi)
    t = W_("E0b", 1)
    place(sfx_buf, tink(1568, 0.6), t, 0.24, send=0.4)
    place(sfx_buf, whoosh(0.5, True, 0.6), t - 0.25, 0.22)
    for i, n_ in enumerate((1046, 1318, 1568, 2093)):
        place(sfx_buf, bell(n_, 1.2, 0.4), t + 0.05 * i, 0.07, pan=-0.4 + 0.27 * i, send=0.5)
    place(sfx_buf, plop(), W_("E1", 2), 0.22)
    place(sfx_buf, pop(560, 760, 0.1), W_("E1", 2) - 0.05, 0.16)
    place(sfx_buf, tink(1760, 0.4), W_("E2", 3), 0.20, send=0.4)                  # süt
    place(sfx_buf, block(), W_("E2", 4) + 0.05, 0.26)                              # yumurta
    place(sfx_buf, thud(0.5), W_("E2", 6) + 0.05, 0.24)                            # et
    tc = W_("E2b", 2)
    for i, n_ in enumerate((988, 1318, 1568, 1976)):
        place(sfx_buf, bell(n_, 1.3, 0.4), tc + 0.06 * i, 0.09, pan=-0.4 + 0.27 * i, send=0.5)
    place(sfx_buf, bell(1318, 1.6, 0.6), We("E2b", 2), 0.12, send=0.5)             # kanıt 3
    place(sfx_buf, whoosh(0.5, True, 0.5), W_("E3", 1) - 0.1, 0.22)
    place(sfx_buf, tink(1318, 0.6), W_("E3", 1) + 0.1, 0.20, send=0.4)
    for i in range(int((W_("E4", 0) - W_("E3", 5)) / 0.16)):
        place(sfx_buf, chew(), W_("E3", 5) + 0.16 * i, 0.12, pan=-0.6 + 1.2 * ((i * 7) % 10) / 10)
    for i in range(3):
        place(sfx_buf, slide(380, 200, 0.4, "sine", 2400), W_("E4", 1) + 0.12 * i, 0.10, pan=-0.3 + 0.3 * i)
        place(sfx_buf, plop(), W_("E4", 1) + 0.12 * i, 0.14, pan=-0.3 + 0.3 * i)
    place(sfx_buf, thud(0.9), W_("E4", 0), 0.30, send=0.3)
    place(sfx_buf, block(), W_("E4", 0), 0.22)
    place(sfx_buf, bell(1318, 1.6, 0.6), We("E4", 3), 0.12, send=0.5)              # kanıt 4

    # ---- F: niasin, mezar, mısır, kireç, gemi
    t = cues.gstart(10) + 0.05
    place(sfx_buf, sting(311, 2.4), t, 0.16, send=0.5)
    for i, n_ in enumerate((1046, 1318, 1568, 2093)):
        place(sfx_buf, bell(n_, 1.2, 0.4), W_("F1", 1) + 0.07 * i, 0.08, pan=-0.4 + 0.27 * i, send=0.5)
    t = W_("F2", 2) - 0.05
    place(sfx_buf, thud(1.0), t, 0.40, send=0.3)
    place(sfx_buf, block(), t, 0.32)
    place(sfx_buf, rumble(2.0, 42), W_("F2", 3) - 0.1, 0.22, send=0.2)
    place(sfx_buf, bell(330, 2.6, 0.9), W_("F2", 4), 0.10, send=0.5)
    t = cues.gstart(11) + 0.05
    place(sfx_buf, pop(500, 900, 0.12), t, 0.24)
    place(sfx_buf, tink(1760, 0.5), W_("F3", 5) - 0.05, 0.22, send=0.4)
    place(sfx_buf, thud(0.7), W_("F3", 5), 0.22)
    place(sfx_buf, whoosh(0.3, True, 0.6), S("F4") - 0.2, 0.22)
    tl = W_("F4", 5)
    place(sfx_buf, hiss(1.1, 4500), tl - 0.1, 0.16)
    for i in range(6):
        place(sfx_buf, plop(), tl + 0.12 * i, 0.12, pan=-0.2 + 0.1 * i)
    for i, n_ in enumerate((1318, 1568, 1976, 2349, 2637)):
        place(sfx_buf, bell(n_, 1.4, 0.45), W_("F4b", 2) + 0.09 * i, 0.08, pan=-0.4 + 0.2 * i, send=0.5)
    place(sfx_buf, tink(1760, 0.5), W_("F4b", 2) - 0.05, 0.20, send=0.4)
    place(sfx_buf, metal_groan(2.0, 60), S("F5") + 0.1, 0.14, send=0.3)
    t = W_("F5", 3) + 0.05
    place(sfx_buf, crash(1.0), t, 0.26, send=0.3)
    place(sfx_buf, rumble(2.6, 40), t + 0.1, 0.30, send=0.3)

    # ---- G: mikrop çarpı ve kart
    place(sfx_buf, pop(500, 800, 0.12), cues.gstart(13) + 0.05, 0.22)
    place(sfx_buf, buzz(1.0, 400), W_("G1", 0), 0.08)
    t = cues.GERM_X
    place(sfx_buf, snare(), t - 0.02, 0.5)
    place(sfx_buf, thud(1.1), t, 0.50, send=0.3)
    place(sfx_buf, crash(0.9), t, 0.22, send=0.2)
    place(sfx_buf, sting(220, 2.4), t, 0.18, send=0.5)
    for i, n_ in enumerate((1046, 1318, 1568, 1976)):
        place(sfx_buf, bell(n_, 1.4, 0.4), t + 0.2 + 0.06 * i, 0.07, pan=-0.4 + 0.27 * i, send=0.5)
    place(sfx_buf, whoosh(0.45, False, 0.9), cues.CARD_T - 0.05, 0.26)

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
    # Anayasa: kodlanmış mp4'te −14 LUFS ±1 ve ≤ −1 dBTP. İleri-bakışlı (lookahead) limiter: 10 ms pencerede minimum kazanç + hareketli ortalama.
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    ceil = 10 ** (CEIL_DB / 20)
    n = int(0.010 * SR)

    def limit(y):
        from scipy.signal import resample_poly
        y4 = resample_poly(y, 4, 1, axis=0)                      # 4x aşırı örnek: örnekler arası (true) tepe
        env = np.abs(y4).max(axis=1)[: len(y) * 4].reshape(-1, 4).max(axis=1)
        gain = np.minimum(1.0, ceil / (env + 1e-9))
        gain = uniform_filter1d(minimum_filter1d(gain, size=2 * n, mode="nearest"), size=n, mode="nearest")
        gain = np.minimum(gain, np.minimum(1.0, ceil / (env + 1e-9)))
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
    write_wav(os.path.join(HERE, "out", "audio.wav"), out)
    print(f"audio.wav: {len(out)/SR:.3f} sn, entegre {L:.2f} LUFS, tepe {20*np.log10(np.max(np.abs(out))):.2f} dBFS")
