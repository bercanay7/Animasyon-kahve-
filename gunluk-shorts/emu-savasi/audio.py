"""
Emu Savaşı — ses: heyecanlı seslendirme (tts.py) + sentezlenmiş müzik yatağı ve efektler, -14 LUFS.
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
rng = np.random.default_rng(1932)


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


# ───────────────────────── miks ─────────────────────────
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
    # ducking zarfı (50 ms RMS → yumuşatma)
    hop = int(0.01 * SR)
    env = np.array([np.sqrt(np.mean(v[i:i + 4 * hop] ** 2)) for i in range(0, N - 4 * hop, hop)])
    env = np.minimum(1, env / 0.12)
    env = np.convolve(env, np.ones(12) / 12, mode="same")
    duck = np.interp(np.arange(N) / SR, np.arange(len(env)) * hop / SR, 1 - 0.6 * env)

    # ---- müzik yatağı: neşeli ukulele "oom-pah" (132 BPM), C–F–G–C
    B = 60.0 / 132
    chords = [([60, 64, 67], 36), ([65, 69, 72], 41), ([67, 71, 74], 43), ([60, 64, 67], 36)]
    nb = int(T / B) + 1
    for k in range(nb):
        tm = k * B
        notes, root = chords[(k // 4) % 4]
        if k % 2 == 0:
            place(music_buf, pluck(midi(root), 0.4), tm, 0.55, pan=-0.15)
        else:
            for n in notes:
                place(music_buf, uke(midi(n), 0.3), tm, 0.12, pan=0.2)
        if k % 4 in (1, 3):
            place(music_buf, snare(), tm, 0.10, pan=0.1)
        place(music_buf, block(), tm + B / 2, 0.06, pan=0.3)
    mel = [76, 79, 76, 72, 74, 77, 74, 71]
    for k in range(int(nb / 2)):
        tm = k * B * 2
        place(music_buf, marimba(midi(mel[k % 8] - 12 * (k % 3 == 2)), 0.5), tm + 0.0, 0.10, pan=0.1)

    # ---- geçişler
    for tb, kind in cues.TRANS:
        if kind in ("whip", "up"):
            place(sfx_buf, whoosh(0.4, True, 1.0), tb - 0.17, 0.55, pan=0.0, send=0.1)
        else:
            place(sfx_buf, whoosh(0.34, False, 1.1), tb - 0.17, 0.5, send=0.1)
            place(sfx_buf, thud(0.7), tb, 0.45)
    # ---- skor tabelası düşer, sayaç geri sarar
    place(sfx_buf, whoosh(0.55, False, 1.0), 0.5, 0.45)
    place(sfx_buf, crash(0.9), 1.1, 0.25)
    for k in range(18):  # geri sayım tıkları
        place(sfx_buf, tick(2400 + 80 * k), lerp(cues.RESET0, cues.RESET1, k / 18), 0.18)
    place(sfx_buf, whoosh(0.5, True, 0.8), cues.RESET0, 0.25)
    # ---- vurgular
    place(sfx_buf, thud(0.9), cues.wt("A", 8), 0.7, send=0.2)
    place(sfx_buf, slide(220, 110, 0.5, "saw"), cues.wt("A", 8) + 0.1, 0.08)
    for k, tm in enumerate(cues.POPS):
        place(sfx_buf, pop(600 + 60 * k, 1100 + 80 * k), tm, 0.30)
    for tm, s in cues.STAMPS:
        place(sfx_buf, thud(s), tm, 0.55 * min(1.1, s), send=0.25)
    # GİZLİ, sona kadar izle
    place(sfx_buf, bell(988, 0.6, 0.2), cues.wt("B", 2), 0.10, send=0.2)
    # harita çizimi: kalem hışırtısı
    n = 1.0
    place(sfx_buf, bp(noise(n), 1500, 5200) * np.sin(np.pi * tt(n) / n) ** 2, cues.st("C") + 0.1, 0.10)
    place(sfx_buf, pop(900, 1200, 0.1), cues.wt("C", 4), 0.3)
    # D: kemirme/yeme "çıt çıt" + sayaç tıkları
    for k in range(10):
        place(sfx_buf, tick(1200 + 100 * (k % 3), 0.05), cues.st("D") + 1.2 + k * 0.23, 0.16)
    td = cues.wt("D", 2)
    for k in range(24):
        place(sfx_buf, tick(3000 + 40 * k), td + k * 0.04, 0.10)
    # E: askerler, tüfek slayt, kasa düşer
    place(sfx_buf, pop(500, 800), cues.wt("E", 2), 0.3)
    place(sfx_buf, thud(0.8), cues.wt("E", 3) + 0.25, 0.5)
    place(sfx_buf, thud(1.0), cues.wt("E", 6) + 0.35, 0.55)
    # F: ampul "ding", zikzak "bip bip"
    place(sfx_buf, bell(1760, 0.7, 0.2), cues.wt("F", 3), 0.16, send=0.3)
    for k in range(8):
        place(sfx_buf, pop(500 + 90 * (k % 4), 700 + 90 * (k % 4), 0.1), cues.wt("F", 7) + k * 0.16, 0.12, pan=-0.4 + 0.2 * k * 0.5)
    # atışlar
    for k, s0 in enumerate(cues.SHOTS):
        place(sfx_buf, gunshot(), s0, 0.26 if s0 < cues.st("F") else 0.2, pan=(-0.4 if k % 2 else 0.2), send=0.1)
    # G: kamyon motoru + pat
    g0, g1 = cues.st("G"), cues.wt("G", 7) + 0.3
    place(sfx_buf, engine_loop(g1 - g0, 52), g0, 0.30, pan=-0.2)
    place(sfx_buf, slide(260, 70, 0.7, "saw", 700), cues.wt("G", 7), 0.12)
    place(sfx_buf, crash(0.5), cues.wt("G", 7) + 0.1, 0.10)
    # H: yağan mermi çıngırtıları ve sayaç dönüşü
    for k in range(60):
        place(sfx_buf, tick(2000 + 30 * (k % 20), 0.04), cues.st("H") + k * (cues.en("H") - cues.st("H")) / 60, 0.10, pan=(-0.5 + (k * 0.37) % 1.0))
    place(sfx_buf, whoosh(cues.en("H") - cues.st("H"), True, 0.7), cues.st("H"), 0.2)
    # I: kilit (ka-ching), emu üzerinden sekme
    tl = cues.wt("I", 1) + 0.18
    place(sfx_buf, bell(1318, 0.9, 0.25), tl, 0.20, send=0.3)
    place(sfx_buf, bell(2093, 0.6, 0.18), tl + 0.08, 0.14, send=0.3)
    place(sfx_buf, thud(1.0), tl, 0.5, send=0.2)
    for j in range(10):
        tj = cues.wt("I", 9) + j * 0.09 + 0.22
        place(sfx_buf, tick(1800 + 90 * (j % 4), 0.06), tj, 0.28)
        place(sfx_buf, pop(1100, 700, 0.07), tj, 0.10)
    # J: üzgün trombon
    j0 = cues.st("J") + 0.1
    for k, (f0, f1) in enumerate(((310, 296), (296, 278), (278, 205))):
        d = 0.42 if k < 2 else 1.0
        place(sfx_buf, slide(f0, f1, d, "saw", 1100), j0 + k * 0.5, 0.11, pan=-0.2, send=0.2)
    place(sfx_buf, bell(1568, 0.8, 0.2), cues.wt("J", 7) + 0.2, 0.08, send=0.3)
    for j in range(5):
        place(sfx_buf, snare(0.1), cues.wt("J", 7) + 0.4 + j * 0.22, 0.12)
    # K: skor — fanfar + ding
    tk = cues.wt("K", 4)
    for k, n in enumerate((60, 64, 67, 72)):
        place(sfx_buf, slide(midi(n), midi(n) * 1.003, 0.5, "saw", 2400), tk - 0.12 + k * 0.07, 0.07, send=0.3)
    place(sfx_buf, bell(1318.5, 0.95, 0.3), tk, 0.22, send=0.3)
    place(sfx_buf, bell(2637, 0.5, 0.12), tk, 0.08)
    place(sfx_buf, crash(0.9), tk, 0.18)

    # ---- yankı ve ducking
    ir = make_ir()
    for ch in range(2):
        sfx_buf[:, ch] += fftconvolve(wet_buf[:, ch], ir)[:N] * 0.5
    music = music_buf * 0.34
    for ch in range(2):
        music[:, ch] *= duck
    # motor/sürekli efektlere hafif ducking yok; kısa vuruşlar zaten kısa
    sfx = sfx_buf * 0.85
    mix = voice_buf * 1.0 + music + sfx
    return mix


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
