"""
Zaman Kuryesi · Zanzibar — ses tasarımı (numpy + scipy), 42.000 sn, 48 kHz stereo → out/audio.wav

Tüm zamanlamalar events.py'den gelir (görselle aynı). Kurallar:
  * tüm video boyunca saat tıkırtısı; sahne 6'da hızlanır, sahne 7'de (28–32) durur
  * 16.0–20.0 TAM sessizlik (sıfır örnek), 20.0'da büyük vuruş
  * bombardımanda top sesleri (filtrelenmiş gürültü + düşük frekanslı patlama)
  * sahne 9'da at nalları + esprili melodi
  * final: kısa "ding"; 42.0'daki tıkırtı 0.0'daki tıkırtıyla birebir bağlanır (döngü)
  * sonunda -14 LUFS (BS.1770) normalizasyonu, -1 dBFS tavan
"""
import os
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

import events as E
from engine import clamp, lerp, prog

SR = 48000
DUR = 42.0
N = int(round(SR * DUR))
rng = np.random.default_rng(1896)


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


def expd(d, tau):
    return np.exp(-tt(d) / tau)


def norm(x, peak=1.0):
    m = np.max(np.abs(x))
    return x * (peak / m) if m > 0 else x


dry = np.zeros((N, 2))
wet = np.zeros((N, 2))  # yankılı gönderim


def place(sig, at, gain=1.0, pan=0.0, send=0.0, buf=None):
    i = int(round(at * SR))
    if i >= N or i < -len(sig):
        return
    s = sig
    if i < 0:
        s, i = s[-i:], 0
    s = s[: N - i]
    l = np.cos((pan + 1) * np.pi / 4) * 1.414
    r = np.sin((pan + 1) * np.pi / 4) * 1.414
    dry[i:i + len(s), 0] += s * gain * l
    dry[i:i + len(s), 1] += s * gain * r
    if send > 0:
        wet[i:i + len(s), 0] += s * gain * l * send
        wet[i:i + len(s), 1] += s * gain * r * send


# ───────────────────────── sesler ─────────────────────────
def tick(kind=0):
    """Duvar saati 'tık' (kind 0) / 'tok' (kind 1)"""
    d = 0.09
    t = tt(d)
    f = 2100 if kind == 0 else 1500
    click = hp(noise(d), 2500) * np.exp(-t / 0.0012)
    ping = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.010)
    wood = np.sin(2 * np.pi * (700 if kind == 0 else 520) * t) * np.exp(-t / 0.022)
    s = 0.55 * click + 0.45 * ping + 0.55 * wood
    return s / np.max(np.abs(s))


def boom(strength=1.0, dur=1.8, low=34.0):
    t = tt(dur)
    f = low + (lerp(low, 110, 0.9) - low + 40) * np.exp(-t / 0.13)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.34 * strength + 0.1))
    body = lp(noise(dur), 300 + 60 * strength) * np.exp(-t / (0.22 * strength + 0.06))
    mid = bp(noise(dur), 300, 1500) * np.exp(-t / 0.09) * 0.35
    crack = hp(noise(dur), 1800) * np.exp(-t / 0.012) * 0.55
    s = 1.0 * sub + 0.9 * body + mid + crack
    s = np.tanh(1.3 * s) / 1.3
    fade = np.minimum(1, (dur - t) / 0.2)
    return s * fade


def explosion(size=1.0, dur=2.2):
    t = tt(dur)
    f = 28 + 40 * np.exp(-t / 0.2)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.5 * size))
    body = lp(noise(dur), 380) * np.exp(-t / (0.45 * size))
    deb = np.zeros_like(t)
    for k in range(10):
        a = 0.08 + rng.random() * 0.9
        n = int(0.012 * SR)
        i = int(a * SR)
        if i + n < len(deb):
            deb[i:i + n] += hp(noise(0.012), 3000) * np.exp(-np.arange(n) / SR / 0.004) * (0.4 + 0.5 * rng.random()) * (1 - a / 1.2)
    s = sub * 0.9 + body * 0.8 + deb * 0.35 + hp(noise(dur), 1200) * np.exp(-t / 0.02) * 0.3
    s = np.tanh(1.2 * s)
    return s * np.minimum(1, (dur - t) / 0.3)


def thud(strength=1.0):
    d = 0.9
    t = tt(d)
    f = 42 + 60 * np.exp(-t / 0.05)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.22) + 0.7 * lp(noise(d), 700) * np.exp(-t / 0.07) + 0.3 * hp(noise(d), 2000) * np.exp(-t / 0.01)
    return np.tanh(1.4 * s * strength) * np.minimum(1, (d - t) / 0.1)


def whoosh(dur=0.5, up=True, bright=1.0):
    n = int(SR * dur)
    x = noise(dur)
    t = np.arange(n) / n
    fc = (300 + 4200 * bright * t ** 1.5) if up else (3500 * bright * (1 - t) ** 1.2 + 250)
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty(n)
    z = 0.0
    for i in range(n):  # tek kutuplu, zamanla değişen alçak geçiren
        z = (1 - a[i]) * x[i] + a[i] * z
        y[i] = z
    y = y - lp(y, 120)
    env = np.sin(np.pi * t) ** 1.5
    return norm(y * env)


def pop(f0=650, f1=1100, d=0.12):
    t = tt(d)
    f = np.linspace(f0, f1, len(t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035)


def hoof(low=1.0):
    d = 0.12
    t = tt(d)
    s = bp(noise(d), 700, 3000) * np.exp(-t / 0.014) + 0.9 * np.sin(2 * np.pi * (150 * low) * t) * np.exp(-t / 0.03)
    return s / np.max(np.abs(s))


def bell(f, d=0.9, tau=0.3):
    t = tt(d)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t / tau) + 0.5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / (tau * 0.5))
         + 0.25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / (tau * 0.25)) + 0.3 * np.sin(2 * np.pi * f * 0.5 * t) * np.exp(-t / (tau * 1.4)))
    return s * np.minimum(1, (d - t) / 0.05)


def marimba(f, d=0.5):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.20) + 0.35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / 0.05) + 0.1 * np.sin(2 * np.pi * 10 * f * t) * np.exp(-t / 0.02)
    return s * np.minimum(1, (d - t) / 0.05)


def pluck_bass(f, d=0.4):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(4 * np.pi * f * t) + 0.15 * np.sin(6 * np.pi * f * t)
    return s * np.exp(-t / 0.16) * np.minimum(1, (d - t) / 0.04)


def block(d=0.08):
    t = tt(d)
    return (bp(noise(d), 1500, 3500) * np.exp(-t / 0.012) + 0.8 * np.sin(2 * np.pi * 1000 * t) * np.exp(-t / 0.02)) * 0.8


def slide(f0, f1, d, wave="saw"):
    t = tt(d)
    f = np.linspace(f0, f1, len(t))
    ph = np.cumsum(f) / SR
    s = 2 * (ph % 1) - 1 if wave == "saw" else np.sin(2 * np.pi * ph)
    s = lp(s, 1400 if wave == "saw" else 4000)
    return s * np.sin(np.pi * np.linspace(0, 1, len(t))) ** 0.5


def crinkle(d=1.0, rate=60):
    s = np.zeros(int(SR * d))
    for k in range(int(rate * d)):
        i = int(rng.random() * (len(s) - 400))
        n = int(0.0065 * SR)
        s[i:i + n] += hp(noise(0.0065), 3500) * np.exp(-np.arange(n) / SR / 0.0015) * (0.4 + 0.6 * rng.random())
    return s * np.sin(np.pi * np.linspace(0, 1, len(s))) ** 0.7


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def make_ir(d=1.6):
    t = tt(d)
    ir = noise(d) * np.exp(-t / 0.38)
    ir = lp(ir, 5000)
    ir[:int(0.012 * SR)] = 0
    return ir / np.sqrt(np.sum(ir ** 2))


# ───────────────────────── MİKS ─────────────────────────
def build():
    # --- saat tıkırtısı ---
    for k, tm in enumerate(E.tick_times()):
        fast = 20.0 <= tm < 28.0
        g = 1.35 if not fast else 1.0
        place(tick(k % 2), tm, g, pan=0.0)
    # sahne 1: dönen ibre vızıltısı (0–3)
    sw = whoosh(3.0, up=True, bright=0.35) * 0.0
    ws = bp(noise(2.9), 700, 2600) * np.sin(np.pi * tt(2.9) / 2.9) ** 2
    place(ws, 0.05, 0.05)
    # --- geçiş vınlamaları ---
    for i, w in enumerate(E.WHOOSH):
        place(whoosh(0.42 if i else 0.7, up=(i != 0), bright=1.0), w if i else 3.0, 0.55 if i else 0.35,
              pan=0.0, send=0.15)
    # pop'lar
    place(pop(500, 900), 3.78, 0.35)
    place(pop(700, 1300, 0.16), 4.55, 0.30)
    place(thud(0.6), 3.80, 0.35)
    place(pop(900, 1200, 0.1), 6.97, 0.25)  # iğne
    place(bell(1568, 0.8, 0.25), 10.1, 0.14, send=0.3)  # taç
    place(pop(300, 200, 0.2), 8.9, 0.2)  # sultan portresi söner
    for tm, s in E.STAMPS:
        place(thud(s), tm, 0.95 * min(1.0, s), send=0.25)
    # liman: gemiler kayar, parşömen açılır
    place(crinkle(1.3, 70), 12.0, 0.10)
    place(bp(noise(2.0), 150, 900) * np.sin(np.pi * tt(2.0) / 2.0), 11.2, 0.12)
    # --- 16–20 sessizlik (sonra sıfırlanır) ---
    # --- büyük vuruş ---
    place(boom(1.8, 2.6, 30), E.BIG_HIT, 0.85, send=0.5)
    place(explosion(1.8, 2.8), E.BIG_HIT + 0.02, 0.35, send=0.4)
    # --- bombardıman ---
    for s in E.SHOTS:
        x = E.SHIPS[s["ship"]][0]
        pan = clamp((x - 540) / 540.0, -1, 1) * 0.7
        big = 1.0 if s["t"] < 20.5 else 0.75
        place(boom(0.6 + 0.4 * rng.random(), 1.3, 36 + 10 * rng.random()), s["t"], 0.42 * big, pan=pan, send=0.35)
        # mermi vınlaması
        wh = slide(2000, 650, s["flight"], wave="sine")
        place(wh, s["t"] + 0.05, 0.035, pan=0.2 * pan)
    for im in E.IMPACTS:
        pan = clamp((im["x"] - 540) / 540.0, -1, 1) * 0.5
        place(explosion(im["size"] * 0.8, 2.0), im["t"], 0.30 * min(1.3, im["size"]), pan=pan, send=0.3)
    # batan gemi: metal gıcırtısı + su
    place(bp(noise(3.0), 80, 400) * np.sin(np.pi * tt(3.0) / 3.0), 24.5, 0.22)
    place(slide(380, 90, 2.4, "saw"), 24.8, 0.10, send=0.2)
    # bayrak iniyor: alçalan hüzünlü ton
    place(slide(260, 130, 1.5, "saw"), 28.5, 0.10, send=0.3)
    # saat donması: ağır "klak"
    place(thud(0.7), E.T_FREEZE, 0.5)
    place(bell(880, 0.7, 0.2), E.T_FREEZE, 0.10, send=0.3)
    # --- sahne 8: gerilim ---
    rise = bp(noise(3.0), 200, 2400) * (tt(3.0) / 3.0) ** 2
    place(rise, 32.0, 0.14)
    for b in (32.6, 33.3, 34.0, 34.55):
        place(thud(0.55), b, 0.55, send=0.2)
    place(whoosh(0.5, True, 1.4), 34.45, 0.2)
    # --- sahne 9: at nalları + melodi ---
    cyc = 0.4
    for k in range(int((E.HORSE_T1 + 0.4 - E.HORSE_T0) / cyc)):
        for o in (0.0, 0.085, 0.19, 0.30):
            tm = E.HORSE_T0 + k * cyc + o
            if tm > E.HORSE_T1 + 0.2:
                continue
            u = prog(tm, 35.0, 37.6)
            pan = lerp(-0.85, 0.85, u)
            vol = 0.55 * (0.45 + 0.55 * min(1, (tm - 35.0) / 0.5)) * (1 - prog(tm, 37.0, 37.8))
            place(hoof(1.0 if o in (0.0, 0.19) else 0.8), tm, vol, pan=pan, send=0.1)
    place(slide(380, 1500, 0.28, "sine"), 36.52, 0.10)  # zarf atışı: kaydırmalı düdük
    place(thud(0.35), 37.05, 0.35)  # zarf düşer
    place(bell(1760, 0.7, 0.18), 37.25, 0.12, send=0.3)
    place(crinkle(1.1, 90), 38.25, 0.12)
    for j, tm in enumerate((38.60, 38.82, 39.04, 39.26)):
        place(bell(2637, 0.5, 0.10), tm, 0.09, pan=0.0, send=0.2)
    # melodi (150 BPM = 0.4 sn vuruş)
    B = 0.4
    t0 = 35.0
    lead = [
        (0, 76), (.5, 79), (1, 76), (1.5, 79), (2, 81), (2.5, 79), (3, 76), (3.5, 74),
        (4, 72), (4.5, 76), (5, 72), (5.5, 76), (6, 77), (6.5, 76), (7, 74), (7.5, 71),
        (8, 72), (8.5, 76), (9, 79), (9.5, 76), (10, 81), (10.5, 79), (11, 77), (11.5, 74),
        (12, 72),
    ]
    for b, n in lead:
        place(marimba(midi(n), 0.45), t0 + b * B, 0.22 * (0.8 if (b % 1) else 1.0), pan=0.15)
    bass = [(0, 48), (2, 55), (4, 53), (6, 48), (8, 48), (10, 55), (12, 48)]
    for b, n in bass:
        place(pluck_bass(midi(n), 0.5), t0 + b * B, 0.30, pan=-0.2)
    for b in range(1, 13, 2):
        place(block(), t0 + b * B, 0.12, pan=0.3)
    for b in (0, 4, 8):  # akor vuruşları (off-beat)
        for n in (60, 64, 67):
            place(marimba(midi(n), 0.2), t0 + (b + 1) * B, 0.07, pan=-0.1)
    # komik final: trombon kayması
    place(slide(330, 165, 0.42, "saw"), 39.52, 0.16, pan=-0.1)
    place(slide(330, 120, 0.5, "saw"), 39.94 - 0.0, 0.0)
    # --- final: geri sarma + ding ---
    n_rw = 14
    for k in range(n_rw):
        u = k / (n_rw - 1)
        tm = lerp(40.40, 41.22, u ** 0.8)
        place(tick(k % 2), tm, 0.55, pan=0.0)
    place(whoosh(0.9, True, 1.2), 40.35, 0.25, send=0.2)
    d = bell(1318.5, 0.95, 0.30)
    d = d * np.minimum(1, np.maximum(0, (E.DING_T + 0.95 - (E.DING_T + tt(0.95))) / 0.2))  # 42.0'dan önce tamamen sönsün
    # (ding 41.42 + 0.58 = 42.0) — son 0.2 sn'de sönümle
    cut = int((DUR - E.DING_T) * SR)
    d = d[:cut] * np.minimum(1, (cut - np.arange(cut)) / (0.25 * SR))
    place(d, E.DING_T, 0.28, send=0.25)
    place(bell(2637, 0.4, 0.1)[:cut], E.DING_T, 0.06)

    # --- yankı gönderimi ---
    ir = make_ir()
    for ch in range(2):
        w = fftconvolve(wet[:, ch], ir)[:N]
        dry[:, ch] += w * 0.55
    return dry


def lufs(x):
    import pyloudnorm as pyln
    return pyln.Meter(SR).integrated_loudness(x)


def master(x):
    # sessizlik penceresi: tam sıfır (16.0–20.0), kenarlarda 8 ms yumuşatma
    a, b = int(E.SILENCE[0] * SR), int(E.SILENCE[1] * SR)
    fo = int(0.008 * SR)
    x[a - fo:a] *= np.linspace(1, 0, fo)[:, None]
    x[a:b] = 0.0
    # dönüş noktası: son 4 ms'de yumuşak sönüm (başlangıçtaki tıkın hemen öncesi sessiz)
    fo2 = int(0.004 * SR)
    x[-fo2:] *= np.linspace(1, 0, fo2)[:, None]
    x = hp_stereo(x, 28)
    ceil = 10 ** (-6.0 / 20)
    g = 1.0
    y = x
    for _ in range(6):
        y = np.tanh(x * g / ceil * 0.9) * ceil / 0.9 if False else x * g
        # yumuşak sınırlayıcı: tepe > tavan ise tanh ile bük
        over = np.abs(y) > ceil * 0.8
        z = np.where(over, np.sign(y) * (ceil * 0.8 + (ceil - ceil * 0.8) * np.tanh((np.abs(y) - ceil * 0.8) / (ceil - ceil * 0.8))), y)
        z[a:b] = 0.0
        L = lufs(z)
        if abs(L - (-14.0)) < 0.05:
            break
        g *= 10 ** ((-14.0 - L) / 20)
    return np.clip(z, -ceil, ceil), lufs(z)


def hp_stereo(x, fc):
    sos = butter(2, fc, "high", fs=SR, output="sos")
    return np.stack([sosfilt(sos, x[:, 0]), sosfilt(sos, x[:, 1])], axis=1)


def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    mix = build()
    out, L = master(mix)
    write_wav("out/audio.wav", out)
    print(f"audio.wav yazıldı: {len(out)/SR:.3f} sn, entegre {L:.2f} LUFS, tepe {20*np.log10(np.max(np.abs(out))):.2f} dBFS")
