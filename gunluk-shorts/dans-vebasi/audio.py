"""
Dans Salgını — ses: heyecanlı seslendirme (tts.py) + sentezlenmiş müzik yatağı ve efektler, -14 LUFS.
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


def crinkle(d=1.0, rate=60):
    s = np.zeros(int(SR * d))
    n = int(0.0065 * SR)
    for k in range(int(rate * d)):
        i = int(rng.random() * (len(s) - n - 10))
        s[i:i + n] += hp(noise(0.0065), 3500) * np.exp(-np.arange(n) / SR / 0.0015) * (0.4 + 0.6 * rng.random())
    return s * np.sin(np.pi * np.linspace(0, 1, len(s))) ** 0.7


# ───────────────────────── ortaçağ çalgıları ─────────────────────────
def ks_pluck(f, d=0.6, damp=0.996, bright=0.5):
    """Karplus-Strong: ud/lavta teli"""
    n = int(SR * d)
    p = max(2, int(SR / f))
    buf = (rng.random(p) * 2 - 1) * bright + (rng.random(p) * 2 - 1) * (1 - bright) * 0.3
    out = np.empty(n)
    for i in range(n):
        j = i % p
        out[i] = buf[j]
        buf[j] = damp * 0.5 * (buf[j] + buf[(j + 1) % p])
    out *= np.minimum(1, (n - np.arange(n)) / (0.05 * SR))
    return out / (np.max(np.abs(out)) + 1e-9) * 0.9


def drone(d, f=73.4, vib=0.0):
    t = tt(d)
    s = 0.0
    for k, (r, g) in enumerate(((1, 1.0), (1.5, 0.6), (2, 0.5))):
        ph = np.cumsum(f * r * (1 + vib * np.sin(2 * np.pi * 4.5 * t))) / SR
        s = s + g * (2 * (ph % 1) - 1)
    s = lp(s, 700)
    return s * np.minimum(np.minimum(1, t / 0.6), np.minimum(1, (d - t) / 0.4))


def shawm(f, d=0.5):
    """Gayda/zurna benzeri nazal ton"""
    t = tt(d)
    ph = np.cumsum(f * (1 + 0.006 * np.sin(2 * np.pi * 5.5 * t))) / SR
    s = 2 * (ph % 1) - 1 + 0.6 * (2 * ((2 * ph) % 1) - 1)
    s = bp(s, 400, 2600)
    return s * np.minimum(np.minimum(1, t / 0.03), np.minimum(1, (d - t) / 0.06))


def tabor_hit(kind=0):
    d = 0.3
    t = tt(d)
    if kind == 0:   # kick
        f = 62 + 70 * np.exp(-t / 0.04)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.11) + 0.3 * lp(noise(d), 600) * np.exp(-t / 0.02)
    return hp(noise(d), 1500) * np.exp(-t / 0.035) + 0.5 * np.sin(2 * np.pi * 220 * t) * np.exp(-t / 0.05)


def wood_tok(d=0.12, f=700):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.02) + 0.7 * bp(noise(d), 900, 2600) * np.exp(-t / 0.015))


def bubble():
    d = 0.12
    t = tt(d)
    f = 300 + 900 * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.03)


def bpm_at(t):
    pts = [(0, 96), (st_("D"), 104), (st_("E"), 140), (st_("F"), 160), (st_("H"), 176), (st_("I"), 168), (st_("J"), 112), (cues.SILENCE_T, 112)]
    for (t0, b0), (t1, b1) in zip(pts[:-1], pts[1:]):
        if t < t1:
            return lerp(b0, b1, prog(t, t0, t1))
    return pts[-1][1]


def st_(k):
    return cues.st(k)


# ───────────────────────── miks ─────────────────────────
DORIAN = [62, 64, 65, 67, 69, 71, 72, 74]   # D dorian
MOTIFS = [[0, 2, 4, 2, 3, 1, 2, 0], [4, 5, 4, 2, 3, 2, 1, 0], [0, 4, 3, 2, 4, 3, 1, 2], [7, 5, 4, 5, 3, 4, 2, 0]]


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

    Tm = cues.SILENCE_T
    # ---- müzik: sekizlik ızgara (tempo hızlanır)
    t = 0.0
    k = 0
    grid = []
    while t < Tm:
        grid.append(t)
        t += 60.0 / bpm_at(t) / 2
    for k, tm in enumerate(grid):
        inten = 0.35 + 0.65 * prog(tm, 0, cues.st("H"))
        if tm > cues.st("J"):
            inten = 0.45
        motif = MOTIFS[(k // 8) % len(MOTIFS)]
        n = DORIAN[motif[k % 8]] - (12 if (k // 16) % 3 == 2 else 0)
        place(music_buf, ks_pluck(midi(n), 0.45), tm, 0.28 * inten + 0.40, pan=-0.2)
        if k % 2 == 0:
            place(music_buf, ks_pluck(midi(DORIAN[0] - 24 if (k // 8) % 2 == 0 else DORIAN[4] - 24), 0.5, 0.997, 0.7), tm, 0.28 * inten + 0.08, pan=-0.05)
        if tm >= cues.st("D") - 0.1:
            place(music_buf, tabor_hit(0), tm, 0.55 * inten, send=0.1) if k % 4 == 0 else None
            place(music_buf, tabor_hit(1), tm, 0.28 * inten) if k % 4 == 2 else None
        if tm >= cues.st("F") and k % 2 == 1:
            place(music_buf, tabor_hit(1), tm, 0.12 * inten, pan=0.2)
    # drone (D2 + beşli) ve gayda
    place(music_buf, drone(Tm - 8.0, 73.4), 8.0, 0.16, pan=0.0)
    for j, tm in enumerate(np.arange(cues.st("G"), Tm, 1.6)):
        if tm > cues.st("J"):
            break
        note = [74, 72, 69, 71][j % 4]
        place(music_buf, shawm(midi(note), 1.3), tm, 0.28, pan=0.25, send=0.15)

    # ---- geçişler ve vurgular
    for tb, kind in cues.TRANS:
        if kind in ("whip", "up"):
            place(sfx_buf, whoosh(0.4, True, 1.0), tb - 0.17, 0.5, send=0.1)
        else:
            place(sfx_buf, whoosh(0.34, False, 1.1), tb - 0.17, 0.45, send=0.1)
            place(sfx_buf, thud(0.6), tb, 0.35)
    for tm, s in cues.STAMPS:
        place(sfx_buf, thud(s), tm, 0.45 * min(1.1, s), send=0.2)
    for k, tm in enumerate(cues.POPS):
        place(sfx_buf, pop(600 + 60 * k, 1100 + 80 * k), tm, 0.28)
    # kağıt hışırtısı: etiketler
    for tm in (cues.wt("B", 3), cues.wt("C", 1), cues.wt("D", 2), cues.wt("D", 7), cues.wt("F", 1), cues.wt("F", 6)):
        place(sfx_buf, crinkle(0.35, 60), tm - 0.05, 0.12)
    # gün-gece dönüşü: tiz çınlama (A)
    place(sfx_buf, whoosh(1.3, True, 0.8), cues.wt("A", 6) - 0.1, 0.25)
    # D: kalabalık ayak vuruşları (kitle büyüdükçe)
    for k in range(60):
        tm = cues.st("D") + k * 0.14
        if tm < cues.en("D"):
            place(sfx_buf, wood_tok(0.12, 120 + 60 * (k % 2)), tm, 0.10 + 0.25 * prog(tm, cues.st("D"), cues.en("D")), pan=(-0.6 + 1.2 * ((k * 0.37) % 1.0)))
    # E: yığılma tıkırtıları ve nefes
    for tm in (cues.wt("E", 1), cues.wt("E", 3)):
        place(sfx_buf, crash(0.4), tm, 0.10)
    for j in range(6):
        place(sfx_buf, thud(0.5), cues.wt("E", 5) + 0.15 * j, 0.20, pan=-0.5 + 0.2 * j)
    # F: şişe kaynaması
    for j in range(24):
        place(sfx_buf, bubble(), cues.wt("F", 1) + j * 0.07, 0.10, pan=0.4)
    place(sfx_buf, bell(988, 0.9, 0.3), cues.wt("F", 4), 0.12, send=0.3)
    # G: tahta tahta sahne (tok tok) + çekiç
    for j in range(6):
        place(sfx_buf, wood_tok(0.16, 520 + 40 * j), cues.st("G") + 0.15 + j * 0.28, 0.4, pan=-0.3 + 0.1 * j)
    for j in range(8):
        place(sfx_buf, wood_tok(0.1, 900), cues.st("G") + 0.1 + j * 0.25, 0.2, pan=0.5 if j % 2 else -0.5)
    place(sfx_buf, thud(1.0), cues.wt("G", 2), 0.5, send=0.2)
    # H: yayılma — yükselen ses
    place(sfx_buf, whoosh(cues.en("H") - cues.st("H"), True, 1.3), cues.st("H"), 0.2)
    # I: yasak ve araba gıcırtısı
    place(sfx_buf, slide(900, 120, 0.4, "saw", 2400), cues.wt("I", 1), 0.14)
    for j in range(14):
        place(sfx_buf, wood_tok(0.08, 300 + 20 * (j % 3)), cues.wt("I", 4) + j * 0.22, 0.2, pan=-0.4 + 0.06 * j)
    place(sfx_buf, bp(noise(2.4), 500, 1800) * np.sin(np.pi * tt(2.4) / 2.4) * 0.5, cues.wt("I", 4), 0.05)
    # J: gizemli çan
    for k, tm in enumerate((cues.wt("J", 5), cues.wt("J", 8), cues.wt("J", 10))):
        place(sfx_buf, bell(740 + 120 * k, 1.2, 0.35), tm, 0.12, send=0.5)
    # K: müzik kesilir — iğne sıyırma + yığılma sesleri
    tk = cues.SILENCE_T
    place(sfx_buf, slide(900, 80, 0.25, "saw", 3000), tk - 0.05, 0.16)
    for j in range(10):
        place(sfx_buf, thud(0.35), tk + 0.15 + j * 0.16, 0.14, pan=-0.6 + 0.13 * j)
    # L: tek bir yumuşak ud sesi (dansçı geri döner) — döngü başlangıcıyla bağlanır
    place(sfx_buf, ks_pluck(midi(62), 0.9, 0.998), cues.wt("L", 2) + 0.15, 0.30, send=0.3)

    ir = make_ir()
    for ch in range(2):
        sfx_buf[:, ch] += fftconvolve(wet_buf[:, ch], ir)[:N] * 0.5
    music = music_buf * 0.15
    for ch in range(2):
        music[:, ch] *= duck
    # müzik, SILENCE_T'de keskin biter (0.02 sn)
    ci = int(Tm * SR)
    fo = int(0.02 * SR)
    music[ci - fo:ci] *= np.linspace(1, 0, fo)[:, None]
    music[ci:] = 0.0
    sfx = sfx_buf * 0.7
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
