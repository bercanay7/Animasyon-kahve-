"""
Titanik'in Kehaneti — ses: heyecanlı seslendirme (tts.py) + sentezlenmiş müzik yatağı ve efektler, -14 LUFS.
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
rng = np.random.default_rng(1912)


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


def build():
    v = load_voice()
    voice_buf[:, 0] = v
    voice_buf[:, 1] = v
    hop = int(0.01 * SR)
    env = np.array([np.sqrt(np.mean(v[i:i + 4 * hop] ** 2)) for i in range(0, N - 4 * hop, hop)])
    env = np.minimum(1, env / 0.12)
    env = np.convolve(env, np.ones(12) / 12, mode="same")
    duck = np.interp(np.arange(N) / SR, np.arange(len(env)) * hop / SR, 1 - 0.70 * env)

    Tm = T - 0.12
    # ---- müzik: karanlık pad (D minör: D, F, A, Bb) + kalp atışı + sonar
    chords = [(73.4, 0.0), (58.3, 6.0), (87.3, 12.0), (73.4, 18.0), (65.4, 24.0), (73.4, 30.0)]
    for f, t0 in chords:
        d = min(6.6, Tm - t0)
        if d > 1:
            place(music_buf, dark_pad(f, d), t0, 0.30, pan=-0.1)
            place(music_buf, dark_pad(f * 1.5 * 2, d), t0, 0.12, pan=0.3, send=0.2)
    # kalp atışı: tempo hızlanır
    tm = 2.0
    while tm < Tm - 1.0:
        inten = 0.4 + 0.6 * prog(tm, 2.0, cues.st("I"))
        place(music_buf, heart(), tm, 0.55 * inten, send=0.05)
        place(music_buf, heart(), tm + 0.2, 0.32 * inten)
        tm += 1.05 - 0.45 * prog(tm, 4.0, cues.st("I"))
    # sonar
    for tm in np.arange(0.6, Tm - 2, 3.2):
        place(music_buf, sonar(1.4), tm, 0.18, pan=0.4, send=0.5)

    # ---- geçişler
    for tb, kind in cues.TRANS:
        if kind in ("whip", "up"):
            place(sfx_buf, whoosh(0.4, True, 1.0), tb - 0.17, 0.5, send=0.1)
        else:
            place(sfx_buf, whoosh(0.34, False, 1.1), tb - 0.17, 0.45, send=0.1)
            place(sfx_buf, thud(0.6), tb, 0.35)
    # açılış: sinyal darbesi + kart düşüşü
    place(sfx_buf, thud(1.0), 0.0, 0.6, send=0.2)
    place(sfx_buf, sting(311, 1.6), 0.02, 0.18, send=0.4)
    place(sfx_buf, whoosh(0.5, False, 1.2), 0.85, 0.4)
    # A: yıl sayacı tik tak
    for k in range(14):
        place(sfx_buf, key_tick(), 1.3 + k * (cues.wt("A", 9) + 0.1 - 1.3) / 14, 0.25)
    # B: satır tıkları
    for i in range(6):
        place(sfx_buf, key_tick(), cues.st("B") + 0.12 + i * 0.16, 0.35)
    # C: daktilo
    for ch in range(8):
        place(sfx_buf, key_tick(), cues.wt("C", 3) - 0.35 + ch / 11.0, 0.3)
    for ch in range(4):
        place(sfx_buf, key_tick(), cues.wt("C", 0) + ch / 6.0, 0.3)
    place(sfx_buf, bell(880, 1.0, 0.35), cues.wt("C", 3) + 0.3, 0.10, send=0.4)
    # benzerlik tink'leri + damgalar
    for k, tm in enumerate(cues.SIM_T):
        place(sfx_buf, tink(1318 + 110 * k), tm, 0.30, pan=-0.2 + 0.08 * k, send=0.3)
    for tm, s in cues.STAMPS:
        place(sfx_buf, thud(s), tm, 0.45 * min(1.1, s), send=0.2)
    # E: buzdağı yaklaşır, çarpar
    place(sfx_buf, metal_groan(2.4, 62), cues.st("E") + 0.9, 0.22, send=0.3)
    place(sfx_buf, ice_crack(1.2), cues.wt("E", 5) - 0.02, 0.7, send=0.3)
    place(sfx_buf, crash(1.0), cues.wt("E", 5), 0.35, send=0.2)
    # F: kırmızı çizgi cızırtısı
    place(sfx_buf, slide(300, 1500, 0.45, "saw", 3000), cues.wt("F", 3) - 0.1, 0.14)
    # G: bot tıkırtıları
    for i in range(44):
        tm = cues.st("G") + 0.3 + (i % 24) * 0.045 + (0.0 if i < 24 else 0.0)
        if i < 24:
            place(sfx_buf, wood_tok_(), tm, 0.12, pan=-0.5)
        else:
            place(sfx_buf, wood_tok_(), cues.st("G") + 0.3 + (i - 24) * 0.045, 0.12, pan=0.5)
    # H: ölçü çizgileri
    for k in (4, 7):
        place(sfx_buf, whoosh(0.35, True, 0.8), cues.wt("H", k) - 0.05, 0.25)
    # I/J: büyük darbe + çan
    place(sfx_buf, sting(233, 2.4), cues.wt("I", 5), 0.35, send=0.5)
    place(sfx_buf, metal_groan(1.6, 55), cues.wt("I", 5) + 0.2, 0.25, send=0.3)
    place(sfx_buf, thud(1.2), cues.wt("J", 4), 0.65, send=0.3)
    place(sfx_buf, sting(207, 2.8), cues.wt("J", 4), 0.38, send=0.5)
    # K: çarpı ve onay
    place(sfx_buf, slide(900, 120, 0.3, "saw", 2400), cues.wt("K", 2), 0.2)
    place(sfx_buf, tink(1760), cues.wt("K", 7) - 0.1, 0.3, send=0.4)
    # L: kart dönüşü
    place(sfx_buf, thud(0.9), cues.st("L") - 0.04 + 0.17, 0.5, send=0.3)
    place(sfx_buf, sonar(1.2, 880), cues.st("L") + 0.4, 0.22, send=0.5)

    ir = make_ir()
    for ch in range(2):
        sfx_buf[:, ch] += fftconvolve(wet_buf[:, ch], ir)[:N] * 0.5
    music = music_buf * 0.15
    for ch in range(2):
        music[:, ch] *= duck
    sfx = sfx_buf * 0.7
    return voice_buf * 1.0 + music + sfx


def wood_tok_():
    d = 0.05
    t = tt(d)
    return (np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.008) + 0.5 * hp(noise(d), 2000) * np.exp(-t / 0.004)) * 0.8


# ───────────────────────── mastering ─────────────────────────
def lufs(x):
    import pyloudnorm as pyln
    return pyln.Meter(SR).integrated_loudness(x)


def master(x):
    # son 0.1 sn tam sessiz (döngüde kesintisiz bağlanır); ilk örnekte yumuşak giriş
    tail = int(0.10 * SR)
    fo = int(0.03 * SR)
    x[-tail - fo:-tail] *= np.linspace(1, 0, fo)[:, None]
    x[-tail:] = 0.0
    x[:int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))[:, None]
    sos = butter(2, 30, "high", fs=SR, output="sos")
    x = np.stack([sosfilt(sos, x[:, 0]), sosfilt(sos, x[:, 1])], axis=1)
    ceil = 10 ** (-6.0 / 20)
    g = 1.0
    z = x
    for _ in range(8):
        y = x * g
        knee = ceil * 0.75
        z = np.where(np.abs(y) > knee, np.sign(y) * (knee + (ceil - knee) * np.tanh((np.abs(y) - knee) / (ceil - knee))), y)
        z[-tail:] = 0.0
        L = lufs(z)
        if abs(L + 14.0) < 0.05:
            break
        g *= 10 ** ((-14.0 - L) / 20)
    return np.clip(z, -ceil, ceil), lufs(z)


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
