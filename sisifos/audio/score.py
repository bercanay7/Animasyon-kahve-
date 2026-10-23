#!/usr/bin/env python3
"""
SİSİFOS — original score, fully synthesized with numpy/scipy (no samples, nothing downloaded).

    python3 audio/score.py          (run from the film folder)
    -> audio/music.wav              48 kHz, stereo, 16-bit, exactly the film's length

Inputs
    audio/cues.md   film length and every narration sentence (parsed at runtime)
    vo/vo.wav       optional; only *analysed* to find where speech is. Never mixed in.

Palette
    lyre / kithara   Karplus-Strong, two detuned strings per note, wooden body resonance
    strings          band-limited (polyBLEP) detuned saw ensembles, 24 dB/oct low-passed, drifting
    choir "aah/ooh"  saw glottal source + vibrato + formant banks (bass/tenor/alto/soprano)
    aulos            additive reed with formant, vibrato, breath noise, and a drone pipe
    frame drum       modal membrane (Bessel ratios) + skin slap; booms tuned to A1; chain metal
    felt piano       slightly inharmonic partials as recursive resonators, two strings per note
    one shared stereo convolution hall (one FFT per channel; 16 kHz twin for the low-rate buses)

Harmony   D Phrygian (dark) / D Dorian (cunning, mythic) -> D major + Lydian G# (Camus).
Motif     the boulder:  D E F A | G -> D       rises four steps, slips, falls back
          completed:    D E F# A B -> D'       reaches the summit (Camus, outro)

Sections  0 cold open + title (aulos states the motif) · I cunning king (plucked Dorian ostinato,
          ticks) · II eagle and spring, thunder · III Death chained, Ares' war drums · IV underworld,
          sunlight, dragged back · V punishment (motif climbs word by word, silence, slip, crash,
          four relentless cycles) · VI Camus (felt piano; Dorian -> D major; motif completed on
          "mutlu") · outro + end screen (lyre; the motif asks, then completes).

Mix       Everything is ducked spectrally under the narration (STFT dynamic EQ: lows -3 dB,
          220 Hz-3.8 kHz -9 dB, highs -5 dB; key lines deeper, see PRIORITY), driven by cues.md
          and vo.wav, so the music swells into the gaps. Hits are ducked about half as much.
          Peak-normalised to -1 dBFS; overall loudness balance is set later, in the final mix.
"""
import re
import time
import wave
from functools import lru_cache
from pathlib import Path

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from scipy.ndimage import binary_closing, binary_dilation, maximum_filter1d, minimum_filter1d
from scipy import fft as sfft
from scipy.signal import butter, lfilter, sosfilt

T_START = time.time()
HERE = Path(__file__).resolve().parent
FILM = HERE.parent
OUT = HERE / 'music.wav'
VO_PATH = FILM / 'vo' / 'vo.wav'
SR, SRL = 48000, 16000          # full rate for plucks/percussion, low rate for pads/choir/piano
rng = np.random.default_rng(1942)


# =============================================================================== cues
def read_cues(path):
    txt = path.read_text(encoding='utf-8')
    total = float(re.search(r'Toplam süre:\s*([\d.]+)', txt).group(1))
    sent = {m[1]: (float(m[2]), float(m[3]))
            for m in re.finditer(r'^- ([A-Z]\d\d) ([\d.]+)\s*[–-]\s*([\d.]+):', txt, re.M)}
    return total, sent


DUR, CUE = read_cues(HERE / 'cues.md')
N = int(round(DUR * SR))
if VO_PATH.exists():
    with wave.open(str(VO_PATH)) as _w:
        if _w.getframerate() == SR and abs(_w.getnframes() - N) < SR // 20:
            N = _w.getnframes()          # sample-exact with the narration track
SENT = np.array(sorted(CUE.values()))


def speaking(t, pre=0.15, post=0.1):
    return bool(np.any((SENT[:, 0] - pre <= t) & (t <= SENT[:, 1] + post)))


# =============================================================================== basics
_PC = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)


def note(s):
    if not isinstance(s, str):
        return s
    pc, i = _PC[s[0]], 1
    while s[i] in 'b#':
        pc += 1 if s[i] == '#' else -1
        i += 1
    return 12 * (int(s[i:]) + 1) + pc


def M(s): return [note(x) for x in s.split()]


def nn(x):
    if x is None or isinstance(x, (int, float, np.integer)):
        return x
    if isinstance(x, tuple):
        return tuple(nn(v) for v in x)
    return note(x)


def mtof(m): return 440.0 * 2.0 ** ((np.asarray(m, float) - 69.0) / 12.0)


@lru_cache(maxsize=None)
def _sos(kind, f, fs, order):
    return butter(order, f, kind, fs=fs, output='sos')


def lp(x, f, fs=SR, order=2): return sosfilt(_sos('lowpass', float(f), fs, order), x, axis=0)
def hp(x, f, fs=SR, order=2): return sosfilt(_sos('highpass', float(f), fs, order), x, axis=0)
def bp(x, lo, hi, fs=SR, order=2): return sosfilt(_sos('bandpass', (float(lo), float(hi)), fs, order), x, axis=0)


def smooth(x, tau, fs):
    a = np.exp(-1.0 / (max(tau, 1e-5) * fs))
    y, _ = lfilter([1 - a], [1, -a], x, zi=[a * x[0]])
    return y


def decays(impulses, tau, fs):
    return lfilter([1.0], [1.0, -np.exp(-1.0 / (tau * fs))], impulses)


def rc(n):
    return 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, max(int(n), 1)))


def env_ar(n, fs, att, rel):
    e = np.ones(n)
    a = min(int(att * fs), n)
    r = min(int(rel * fs), n - a)
    if a:
        e[:a] = rc(a)
    if r:
        e[n - r:] *= rc(r)[::-1]
    return e


def noise(n, lo=None, hi=None, fs=SR, order=2):
    x = rng.standard_normal(n)
    if lo and hi:
        x = bp(x, lo, hi, fs, order)
    elif hi:
        x = lp(x, hi, fs, order)
    elif lo:
        x = hp(x, lo, fs, order)
    return x / (np.sqrt(np.mean(x ** 2)) + 1e-12)


def wobble(n, fs, cents, rates=(0.08, 0.4)):
    """Slow random pitch/amplitude drift (three slow sines), computed coarsely and interpolated."""
    step = 64
    t = np.arange(n // step + 2) * (step / fs)
    r = rng.uniform(rates[0], rates[1], 3)
    p = rng.uniform(0, 2 * np.pi, 3)
    w = cents * (0.5 * np.sin(2 * np.pi * r[0] * t + p[0]) + 0.3 * np.sin(2 * np.pi * r[1] * t + p[1])
                 + 0.2 * np.sin(2 * np.pi * r[2] * t + p[2]))
    return np.interp(np.arange(n, dtype=float), np.arange(len(t)) * float(step), w)


def blep_saw(freq, fs):
    """Band-limited sawtooth (polyBLEP) for a per-sample frequency array."""
    dt = np.asarray(freq, float) / fs
    ph = np.cumsum(dt) + rng.random()
    ph -= np.floor(ph)
    y = 2.0 * ph - 1.0
    m = ph < dt
    t = ph[m] / dt[m]
    y[m] -= 2 * t - t * t - 1
    m = ph > 1 - dt
    t = (ph[m] - 1) / dt[m]
    y[m] -= t * t + 2 * t + 1
    return y


# =============================================================================== buses
_ARR = {}


def arr(fs, key):
    """Shared mix arrays: (rate, 'full' | 'hits' | 'send')."""
    if (fs, key) not in _ARR:
        _ARR[(fs, key)] = np.zeros((N * fs // SR + fs, 2), np.float32)
    return _ARR[(fs, key)]


class Bus:
    """Routing for one instrument family: level, reverb send, ducking class, sample rate.
    own=True keeps a private array for post-processing (the lyre's wooden body)."""
    def __init__(self, name, fs=SR, gain=1.0, send=0.25, duck='full', own=False):
        self.name, self.fs, self.gain, self.send, self.duck = name, fs, gain, send, duck
        self.x = np.zeros((N * fs // SR + fs, 2), np.float32) if own else None


def place(bus, sig, t, gain=1.0, pan=0.0):
    sig = np.asarray(sig, float)
    a = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    pl, pr = np.cos(a) * np.sqrt(2), np.sin(a) * np.sqrt(2)
    if sig.ndim == 1:
        sig = np.stack([sig * pl, sig * pr], 1)
    elif pan:
        sig = sig * np.array([pl, pr])
    i = int(round(t * bus.fs))
    if i < 0:
        sig, i = sig[-i:], 0
    n = min(len(sig), N * bus.fs // SR + bus.fs - i)
    if n <= 0:
        return
    sig = (sig[:n] * (gain * bus.gain)).astype(np.float32)
    if bus.x is not None:
        bus.x[i:i + n] += sig
    else:
        arr(bus.fs, bus.duck)[i:i + n] += sig
        arr(bus.fs, 'send')[i:i + n] += sig * np.float32(bus.send)


LYRE = Bus('lyre', SR, gain=0.62, send=0.30, own=True)
AULOS = Bus('aulos', SR, gain=0.34, send=0.36)
PERC = Bus('perc', SR, gain=0.52, send=0.22)
HITS = Bus('hits', SR, gain=0.62, send=0.18, duck='hits')
FX = Bus('fx', SR, gain=0.34, send=0.40)
STR = Bus('strings', SRL, gain=0.62, send=0.28)
DRONE = Bus('drone', SRL, gain=0.55, send=0.12)
CHOIR = Bus('choir', SRL, gain=0.40, send=0.55)
PIANO = Bus('piano', SRL, gain=0.62, send=0.34)
RUMB = Bus('rumble', SRL, gain=0.60, send=0.10, duck='hits')


# =============================================================================== instruments
def ks_string(f, dur, t60=3.0, bright=0.5, damp=0.5, pos=0.17):
    """Karplus-Strong string: one-period noise pluck, damped 3-tap loop filter, fractional tuning."""
    fs = SR
    L = max(int(dur * fs), 1)
    D = fs / f - 1.0                      # the symmetric loop filter adds one sample of delay
    Nd = int(D)
    fr = D - Nd
    g = 10.0 ** (-3.0 / (t60 * f))        # loop gain per period for the requested T60
    s = 0.25 * float(np.clip(damp, 0, 1))
    taps = g * np.convolve([s, 1 - 2 * s, s], [1 - fr, fr])
    ex = rng.standard_normal(Nd)
    a = np.exp(-2 * np.pi * (250 + 8000 * bright ** 2) / fs)
    ex = lfilter([1 - a], [1, -a], lfilter([1 - a], [1, -a], ex))
    k = max(1, int(pos * Nd))
    ex = ex - np.concatenate([np.zeros(k), ex[:-k]])   # pluck position
    ex -= ex.mean()
    P = Nd + 3
    y = np.zeros(P + L)
    m = min(Nd, L)
    y[P:P + m] = ex[:m]
    for st in range(P + Nd, P + L, Nd):
        en = min(st + Nd, P + L)
        y[st:en] = (taps[0] * y[st - Nd:en - Nd] + taps[1] * y[st - Nd - 1:en - Nd - 1]
                    + taps[2] * y[st - Nd - 2:en - Nd - 2] + taps[3] * y[st - Nd - 3:en - Nd - 3])
    y = y[P:]
    return y / (np.abs(y[:3 * Nd]).max() + 1e-9)


def lyre(t, m, vel=0.5, dur=None, t60=None, bright=0.45, damp=0.55, pan=0.0, detune=1.8, bus=None):
    m = note(m)
    f = float(mtof(m))
    if t60 is None:
        t60 = float(np.clip(3.4 * (110 / f) ** 0.45, 0.7, 4.5))
    if dur is None:
        dur = min(t60 * 1.15, 5.0)
    c = 2 ** (detune / 1200)
    a = ks_string(f * c, dur, t60, bright, damp, rng.uniform(0.11, 0.2))
    b = ks_string(f / c, dur, t60 * 0.9, bright * 0.9, damp, rng.uniform(0.11, 0.2))
    n = min(len(a), len(b))
    x = np.stack([0.65 * a[:n] + 0.35 * b[:n], 0.35 * a[:n] + 0.65 * b[:n]], 1) * 0.5
    fo = min(int(0.04 * SR), n)
    x[-fo:] *= rc(fo)[::-1, None]
    place(bus or LYRE, x, t + rng.normal(0, 0.003), gain=vel, pan=pan)


def pizz(t, m, vel=0.45, pan=-0.1, bright=0.3, t60=0.6, dur=0.55):
    lyre(t, m, vel=vel, dur=dur, t60=t60, bright=bright, damp=0.85, pan=pan)


def strum(t, notes, vel=0.5, spread=0.022, up=True, **kw):
    notes = [note(x) for x in notes]
    order = notes if up else notes[::-1]
    k = max(len(order) - 1, 1)
    for i, m in enumerate(order):
        lyre(t + i * spread * (1 + 0.15 * rng.standard_normal()), m, vel=vel * rng.uniform(0.85, 1.0),
             pan=-0.4 + 0.8 * i / k, **kw)


def lyre_line(t, items, vel=0.4, **kw):
    for it in items:
        v = it[2] if len(it) > 2 else 1.0
        lyre(t, it[0], vel=vel * v, **kw)
        t += it[1]
    return t


def body_ir():
    """Wooden sound-box of the lyre: a handful of damped modes added to the direct sound."""
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    ir = np.zeros(n)
    ir[0] = 1.0
    for f, g, tau in [(98, 0.9, 0.05), (196, 1.1, 0.045), (300, 0.8, 0.035), (450, 0.6, 0.03),
                      (680, 0.45, 0.022), (950, 0.35, 0.018), (1350, 0.25, 0.012), (2200, 0.15, 0.008)]:
        ir += (2 * g / (tau * SR)) * np.cos(2 * np.pi * f * t) * np.exp(-t / tau)
    return ir


def pad(notes, t0, t1, gain=0.2, att=1.5, rel=2.0, cutoff=900, voices=2, detune=7.0, sine=0.0,
        bus=None, width=0.8, breathe=0.0, vib=0.0):
    """Sustained ensemble chord (strings or drone): drifting, detuned band-limited saws, low-passed."""
    bus = bus or STR
    fs = bus.fs
    n = int((t1 - t0) * fs)
    if n <= 0:
        return
    tt = np.arange(n) / fs
    L = np.zeros(n)
    R = np.zeros(n)
    nv = 0
    for m in notes:
        f = float(mtof(note(m)))
        for v in range(voices * 2):
            c = rng.uniform(-detune, detune) + wobble(n, fs, 4.0)
            if vib:
                c = c + vib * np.sin(2 * np.pi * rng.uniform(4.6, 5.6) * tt + rng.uniform(0, 6.3))
            fr = f * 2 ** (c / 1200)
            y = blep_saw(fr, fs)
            if sine:
                y = (1 - sine) * y + sine * 1.4 * np.sin(2 * np.pi * np.cumsum(fr) / fs + rng.uniform(0, 6.3))
            if v % 2 == 0:
                L += y * (1 + width) / 2
                R += y * (1 - width) / 2
            else:
                L += y * (1 - width) / 2
                R += y * (1 + width) / 2
            nv += 1
    x = np.stack([L, R], 1) / np.sqrt(nv)
    x = hp(lp(x, cutoff, fs, 4), 38, fs, 2)
    e = env_ar(n, fs, att, rel)
    if breathe:
        e *= 1 - breathe * (0.5 - 0.5 * np.cos(2 * np.pi * tt / 4.4))
    place(bus, x * e[:, None], t0, gain=gain)


def drone(notes, t0, t1, gain=0.3, att=2.0, rel=1.5, cutoff=280):
    """Low drone, one pad per note; the sub octave (below A1) is kept as a quiet shadow."""
    for m in M(notes):
        w = 0.3 if m < 33 else (0.75 if m > 40 else 1.0)
        pad([m], t0, t1, gain=gain * w, att=att, rel=rel, cutoff=cutoff, sine=0.5, voices=1, bus=DRONE)


def bowed(t0, phrase, gain=0.3, stack=(0,), voices=2, detune=6.0, cutoff=900, vib=8.0, glide=0.045,
          att=0.07, rel=0.6, accent=0.4, trem=0.0, bus=None, pan=0.0, width=0.7, legato=True):
    """A bowed string section line. phrase items: (note | (from, to) glide | None rest, seconds, vel)."""
    bus = bus or STR
    fs = bus.fs
    items = [(nn(it[0]), it[1], it[2] if len(it) > 2 else 1.0) for it in phrase]
    total = sum(d for _, d, _ in items)
    n = int((total + rel + 0.05) * fs)
    tt = np.arange(n) / fs
    pitch = np.full(n, np.nan)
    amp = np.zeros(n)
    vibz = np.zeros(n)
    acc = np.zeros(n)
    t = 0.0
    for m, d, v in items:
        i0, i1 = int(t * fs), int((t + d) * fs)
        if m is not None:
            if isinstance(m, tuple):
                pitch[i0:i1] = np.linspace(m[0], m[1], i1 - i0)
            else:
                pitch[i0:i1] = m
                vibz[min(i0 + int(0.22 * fs), i1):i1] = 1.0
                acc[i0] = 1.0
            amp[i0:i1] = v
            if not legato:
                amp[max(i0, i1 - int(0.035 * fs)):i1] = 0
        t += d
    valid = ~np.isnan(pitch)
    idx = np.where(valid, np.arange(n), 0)
    np.maximum.accumulate(idx, out=idx)
    pitch = pitch[idx]
    pitch[np.isnan(pitch)] = pitch[valid][0]
    i_end = min(int(total * fs), n - 1)
    amp[i_end:] = amp[max(i_end - 1, 0)]
    p = smooth(pitch, glide, fs)
    a = smooth(amp, att, fs) * (1 + accent * decays(acc, 0.13, fs))
    a[i_end:] *= rc(n - i_end)[::-1]
    vz = smooth(vibz, 0.25, fs)
    L = np.zeros(n)
    R = np.zeros(n)
    nv = 0
    for s in stack:
        for v in range(voices * 2):
            c = (rng.uniform(-detune, detune) + wobble(n, fs, 3.0)
                 + vib * vz * np.sin(2 * np.pi * rng.uniform(4.6, 5.6) * tt + rng.uniform(0, 6.3)))
            y = blep_saw(mtof(p + s) * 2 ** (c / 1200), fs)
            if trem:
                y *= 1 - trem * (0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(11, 15) * tt + rng.uniform(0, 6.3)))
            w1, w2 = (1 + width) / 2, (1 - width) / 2
            if v % 2:
                w1, w2 = w2, w1
            L += y * w1
            R += y * w2
            nv += 1
    x = np.stack([L, R], 1) / np.sqrt(nv)
    x = hp(lp(x, cutoff, fs, 4), 35, fs, 2) * a[:, None]
    place(bus, x, t0, gain=gain, pan=pan)


FORMANTS = {
    ('a', 'bass'): [(600, 60, 0), (1040, 70, -7), (2250, 110, -9), (2450, 120, -9), (2750, 130, -20)],
    ('a', 'tenor'): [(650, 80, 0), (1080, 90, -6), (2650, 120, -7), (2900, 130, -8), (3250, 140, -22)],
    ('a', 'alto'): [(800, 80, 0), (1150, 90, -4), (2800, 120, -20), (3500, 130, -36)],
    ('a', 'sop'): [(800, 80, 0), (1150, 90, -6), (2900, 120, -32), (3900, 130, -20)],
    ('o', 'bass'): [(400, 40, 0), (750, 80, -11), (2400, 100, -21), (2600, 120, -20)],
    ('o', 'tenor'): [(400, 40, 0), (800, 80, -10), (2600, 100, -12), (2800, 120, -12)],
    ('o', 'alto'): [(450, 70, 0), (800, 80, -9), (2830, 100, -16), (3500, 130, -28)],
    ('o', 'sop'): [(450, 70, 0), (800, 80, -9), (2830, 100, -16), (3500, 130, -28)],
    ('u', 'bass'): [(350, 40, 0), (600, 80, -20), (2400, 100, -32)],
    ('u', 'tenor'): [(350, 40, 0), (600, 60, -20), (2700, 100, -17)],
    ('u', 'alto'): [(325, 50, 0), (700, 60, -12), (2530, 170, -30)],
    ('u', 'sop'): [(325, 50, 0), (700, 60, -16), (2700, 170, -35)],
}


def register(m): return 'bass' if m < 52 else 'tenor' if m < 60 else 'alto' if m < 67 else 'sop'


def choir(notes, t0, t1, gain=0.3, att=1.2, rel=1.5, vowel='a', voices=4, vib=22.0, width=0.9):
    """Wordless choir: per singer a vibrato saw 'glottis' + breath, through a vowel formant bank."""
    fs = CHOIR.fs
    n = int((t1 - t0) * fs)
    tt = np.arange(n) / fs
    groups = {}
    for m in notes:
        m = note(m)
        reg = register(m)
        f = float(mtof(m))
        acc = groups.setdefault(reg, [np.zeros(n), np.zeros(n)])
        for v in range(voices):
            ve = np.clip((tt - rng.uniform(0.15, 0.6)) / 0.8, 0, 1)
            c = (rng.uniform(-9, 9) + wobble(n, fs, 5.0, (0.2, 1.1))
                 + vib * ve * np.sin(2 * np.pi * rng.uniform(4.6, 5.8) * tt + rng.uniform(0, 6.3)))
            y = blep_saw(f * 2 ** (c / 1200), fs) * (1 + 0.15 * wobble(n, fs, 1.0, (0.1, 0.6)))
            acc[v % 2] += y
    out = np.zeros((n, 2))
    for reg, (L, R) in groups.items():
        for ch, sig in enumerate((L, R)):
            sig = sig + 0.12 * np.std(sig) * rng.standard_normal(n)
            y = np.zeros(n)
            for fc, bw, db in FORMANTS[(vowel, reg)]:
                bw *= 1.6
                y += 10 ** (db / 20) * bp(sig, fc - bw / 2, min(fc + bw / 2, fs * 0.45), fs, 1)
            out[:, ch] += y
    out = lp(out, 4500, fs, 2)
    out = out * ((1 + width) / 2) + out[:, ::-1] * ((1 - width) / 2)
    out *= 0.25 / (np.sqrt(np.mean(out ** 2)) + 1e-12)
    out *= env_ar(n, fs, att, rel)[:, None]
    place(CHOIR, out, t0, gain=gain)


AUL_F = np.array([0, 250, 600, 1000, 1400, 1900, 2600, 3600, 5000, 7000, 9500, 24000.0])
AUL_G = np.array([0.5, 0.7, 1.0, 1.5, 1.9, 1.6, 1.0, 0.6, 0.35, 0.15, 0.05, 0.0])


def reed(f, a, fs, hmax=9000.0, tilt=0.8, bright=0.12):
    ph = 2 * np.pi * np.cumsum(f) / fs
    H = max(1, int(hmax / f.max()))
    lg = np.log(np.maximum(a / (a.max() + 1e-9), 1e-4))
    y = np.zeros(len(f))
    for h in range(1, H + 1):
        g = np.interp(h * f, AUL_F, AUL_G) * h ** -tilt * (1.0 if h % 2 else 0.5)
        y += g * np.exp(lg * bright * (h - 1)) * np.sin(h * ph + rng.uniform(0, 6.3))
    return y * a


def aulos(t0, phrase, gain=0.3, vib=16.0, glide=0.03, breath=0.05, pan=0.0, drone=None, att=0.04, rel=0.3):
    """Aulos: additive double-reed melody pipe (+ optional drone pipe), vibrato, breath, tonguing."""
    fs = AULOS.fs
    items = [(nn(it[0]), it[1], it[2] if len(it) > 2 else 1.0) for it in phrase]
    total = sum(d for _, d, _ in items)
    n = int((total + rel + 0.05) * fs)
    tt = np.arange(n) / fs
    pitch = np.full(n, np.nan)
    amp = np.zeros(n)
    vibz = np.zeros(n)
    acc = np.zeros(n)
    t = 0.0
    for m, d, v in items:
        i0, i1 = int(t * fs), int((t + d) * fs)
        if m is not None:
            if isinstance(m, tuple):
                pitch[i0:i1] = np.linspace(m[0], m[1], i1 - i0)
            else:
                pitch[i0:i1] = m
                if d > 0.3:
                    vibz[i0 + int(0.18 * fs):i1] = 1.0
                acc[i0] = 1.0
            amp[i0:i1] = v
            if not isinstance(m, tuple):
                amp[i0:i0 + int(0.018 * fs)] *= 0.35          # tonguing
        t += d
    valid = ~np.isnan(pitch)
    idx = np.where(valid, np.arange(n), 0)
    np.maximum.accumulate(idx, out=idx)
    pitch = pitch[idx]
    pitch[np.isnan(pitch)] = pitch[valid][0]
    i_end = min(int(total * fs), n - 1)
    amp[i_end:] = amp[max(i_end - 1, 0)]
    p = smooth(pitch, glide, fs)
    a = smooth(amp, att, fs)
    a[i_end:] *= rc(n - i_end)[::-1]
    vz = smooth(vibz, 0.2, fs)
    vr = 5.3 + 0.25 * np.sin(2 * np.pi * 0.6 * tt)
    cents = vib * vz * np.sin(2 * np.pi * np.cumsum(vr) / fs) + wobble(n, fs, 3.0, (0.5, 2.0))
    f = mtof(p) * 2 ** (cents / 1200)
    y = reed(f, a, fs)
    y *= 1 + 0.03 * noise(n, None, 40, fs)
    y /= np.abs(y).max() + 1e-9
    y += breath * noise(n, 1200, 5500, fs) * a / (a.max() + 1e-9)
    y += 0.25 * noise(n, 2000, 7000, fs) * decays(acc, 0.018, fs) * a / (a.max() + 1e-9)
    if drone is not None:
        fd = np.full(n, float(mtof(note(drone)))) * 2 ** (wobble(n, fs, 2.5, (0.2, 1.0)) / 1200)
        da = smooth(np.where(a > 0.05 * a.max(), 1.0, 0.0), 0.15, fs) * env_ar(n, fs, 0.05, rel)
        d = reed(fd, da, fs, tilt=0.95, bright=0.0)
        y += 0.32 * d / (np.abs(d).max() + 1e-9)
    y = lp(y, 9500, fs, 2)
    place(AULOS, y, t0, gain=gain, pan=pan)


def piano(t, m, vel=0.5, dur=None, pan=0.0, bright=0.5):
    """Felt piano: slightly stretched partials, two strings per note, two-stage decay, soft hammer."""
    fs = PIANO.fs
    m = note(m)
    f = float(mtof(m))
    if dur is None:
        dur = float(np.clip(5.0 * (262 / f) ** 0.5, 1.6, 6.0))
    n = int(dur * fs)
    tt = np.arange(n) / fs
    B = 0.00012 * (f / 262)
    y = np.zeros(n)
    imp = np.zeros(n)
    imp[0] = 1.0
    for k in range(1, 15):
        fk = k * f * np.sqrt(1 + B * k * k)
        if fk > 6500:
            break
        a = k ** -1.1 * np.exp(-(k - 1) * (0.55 - 0.35 * bright * vel))
        t1 = 0.28 * (262 / f) ** 0.4 / (1 + 0.25 * (k - 1))
        t2 = 3.4 * (262 / f) ** 0.5 / (1 + 0.12 * (k - 1))
        for d in (-0.7, 0.6):                       # two slightly detuned strings
            w = 2 * np.pi * fk * (1 + d / 1731) / fs
            ph = rng.uniform(0, 6.3)
            for amp, tau in ((0.55 * a, t1), (0.45 * a, t2)):   # prompt + after-sound decay
                r = np.exp(-1.0 / (tau * fs))
                y += amp * lfilter([np.sin(ph), r * np.sin(w - ph)], [1, -2 * r * np.cos(w), r * r], imp)
    y /= np.abs(y[:int(0.05 * fs)]).max() + 1e-9
    y += 0.12 * noise(n, None, 900, fs) * np.exp(-tt / 0.006)
    y *= np.minimum(1, tt / 0.002)
    fo = min(int(0.3 * fs), n)
    y[-fo:] *= rc(fo)[::-1]
    place(PIANO, y, t, gain=vel, pan=pan)


FD_R = np.array([1.0, 1.594, 2.136, 2.296, 2.653, 2.918, 3.156, 3.501])


def fdrum(t, kind='dum', vel=0.6, f0=None, pan=0.0, dur=1.4):
    """Frame drum (tympanon): membrane modes with a pitch drop + skin slap. 'dum' centre / 'tek' rim."""
    fs = SR
    n = int(dur * fs)
    tt = np.arange(n) / fs
    if kind == 'dum':
        f0 = f0 or 78
        amps = [1, 0.5, 0.3, 0.22, 0.15, 0.1, 0.07, 0.05]
        taus = [0.42, 0.22, 0.16, 0.14, 0.11, 0.09, 0.07, 0.06]
        slap = noise(n, None, 1800, fs) * np.exp(-tt / 0.008) * 0.3
    else:
        f0 = f0 or 190
        amps = [0.2, 0.5, 0.6, 0.5, 0.45, 0.4, 0.35, 0.3]
        taus = [0.09, 0.07, 0.06, 0.05, 0.05, 0.04, 0.04, 0.035]
        slap = noise(n, 1800, 7000, fs) * np.exp(-tt / 0.004) * 0.45
    ph = 2 * np.pi * np.cumsum(f0 * (1 + 0.1 * vel * np.exp(-tt / 0.03))) / fs
    y = sum(a * np.sin(r * ph) * np.exp(-tt / tau) for r, a, tau in zip(FD_R, amps, taus))
    y = (y + slap) * np.minimum(1, tt / 0.001)
    place(PERC, y / (np.abs(y).max() + 1e-9), t, gain=vel, pan=pan)


def boom(t, vel=1.0, f0=80, f1=55, decay=0.8, knock=0.5, pan=0.0, sat=2.4):
    """Deep cinematic boom settling on A1 (the fifth of D): falling sine + low noise knock, saturated."""
    fs = SR
    f0, f1 = max(f0, 75), 55.0
    decay = min(decay, 0.9)
    n = int(decay * 4 * fs)
    tt = np.arange(n) / fs
    f = f1 + (f0 - f1) * np.exp(-tt / 0.09)
    y = np.sin(2 * np.pi * np.cumsum(f) / fs) * np.exp(-tt / decay)
    y += knock * noise(n, None, 300, fs) * np.exp(-tt / 0.05)
    y += 0.3 * knock * noise(n, None, 120, fs) * np.exp(-tt / 0.3)
    y = np.tanh(sat * y) / np.tanh(sat) * np.minimum(1, tt / 0.0015)
    place(HITS, y, t, gain=vel, pan=pan)


def metal(t, f0=587.0, vel=0.8, decay=0.9, ratios=(1, 2.756, 5.404, 8.933, 13.34), click=0.5,
          pan=0.0, bus=None):
    """Struck metal (chain, latch, iron): inharmonic beating partials + click transient."""
    fs = SR
    n = int(decay * 3 * fs) + int(0.05 * fs)
    tt = np.arange(n) / fs
    y = np.zeros(n)
    for k, r in enumerate(ratios):
        fk = f0 * r * (1 + rng.uniform(-0.004, 0.004))
        if fk > 10500:
            continue
        a = 1 / (1 + k) ** 0.7
        tau = decay / (1 + 0.8 * k)
        y += a * np.exp(-tt / tau) * (np.sin(2 * np.pi * fk * tt + rng.uniform(0, 6.3))
                                      + 0.6 * np.sin(2 * np.pi * fk * 1.0035 * tt + rng.uniform(0, 6.3)))
    y /= np.abs(y).max() + 1e-9
    y += click * noise(n, 1500, 9000, fs) * np.exp(-tt / 0.004)
    y *= np.minimum(1, tt / 0.0005)
    place(bus or HITS, y, t, gain=vel, pan=pan)


def clinks(t, count=6, spread=0.6, vel=0.15, pan=0.2):
    times = np.sort(rng.uniform(0, spread, count))
    for i, dt in enumerate(times):
        metal(t + dt, f0=rng.uniform(1700, 3200), vel=vel * (1 - 0.5 * i / count) * rng.uniform(0.6, 1),
              decay=rng.uniform(0.05, 0.12), ratios=(1, 2.41, 3.73, 5.1), click=0.3,
              pan=pan + rng.uniform(-0.3, 0.3), bus=PERC)


def tick(t, vel=0.15, pitch=1.0, pan=0.0):
    n = int(0.03 * SR)
    tt = np.arange(n) / SR
    y = noise(n, 4200 * pitch, 9000, SR, 4) * np.exp(-tt / 0.0025)
    y += 0.5 * np.sin(2 * np.pi * 5300 * pitch * tt) * np.exp(-tt / 0.005)
    place(PERC, y * np.minimum(1, tt / 0.0003), t, gain=vel, pan=pan)


def bell(t, m, vel=0.2, decay=2.4, pan=0.0):
    f = float(mtof(note(m)))
    n = int(decay * 2.5 * SR)
    tt = np.arange(n) / SR
    y = np.zeros(n)
    for r, a, dk in [(1, 1.0, 1.0), (2.0, 0.3, 0.6), (3.0, 0.12, 0.4), (4.17, 0.08, 0.25), (5.43, 0.05, 0.18)]:
        if f * r < 10500:
            y += a * np.sin(2 * np.pi * f * r * tt + rng.uniform(0, 6.3)) * np.exp(-tt / (decay * dk))
    place(FX, y * np.minimum(1, tt / 0.002), t, gain=vel, pan=pan)


def riser(t_end, dur, vel=0.4, kind='swell'):
    """Reverse-swell into a hit. 'cym' stays above the speech band (reverse cymbal)."""
    n = int(dur * SR)
    x = np.linspace(0, 1, n)
    if kind == 'cym':
        y = np.stack([noise(n, 4000, 9500, SR, 4), noise(n, 4000, 9500, SR, 4)], 1) * (x ** 3.5)[:, None]
    else:
        lo = np.stack([noise(n, 250, 900), noise(n, 250, 900)], 1)
        hi = np.stack([noise(n, 1500, 7000, SR, 4), noise(n, 1500, 7000, SR, 4)], 1)
        c = (x ** 1.6)[:, None]
        y = (lo * (1 - c) + hi * c) * (x ** 2.5)[:, None]
    fo = int(0.012 * SR)
    y[-fo:] *= rc(fo)[::-1, None]
    place(FX, y, t_end - dur, gain=vel)


def thunder(t, vel=1.0):
    n = int(1.4 * SR)
    tt = np.arange(n) / SR
    env = np.exp(-tt / 0.07) + 0.5 * np.exp(-((tt - 0.09) / 0.03) ** 2) + 0.3 * np.exp(-((tt - 0.24) / 0.05) ** 2)
    crack = np.stack([noise(n, 60, 2400), noise(n, 60, 2400)], 1) * (env * np.minimum(1, tt / 0.003))[:, None]
    place(HITS, crack, t, gain=0.2 * vel)
    fs = SRL
    n2 = int(7.5 * fs)
    t2 = np.arange(n2) / fs
    bumps = sum(a * np.exp(-((t2 - c) / w) ** 2)
                for c, w, a in [(0.08, 0.06, 1.0), (0.45, 0.2, 0.75), (1.0, 0.3, 0.8), (1.7, 0.35, 0.6),
                                (2.5, 0.45, 0.5), (3.4, 0.6, 0.35), (4.6, 0.8, 0.22)])
    env2 = bumps * np.exp(-t2 / 3.0) * np.minimum(1, t2 / 0.01)
    r = np.stack([noise(n2, 22, 200, fs), noise(n2, 22, 200, fs)], 1) * env2[:, None]
    place(RUMB, r, t, gain=0.9 * vel)
    boom(t, vel=0.85 * vel, f0=50, f1=28, decay=2.0)


def thud(t, vel=0.5, f0=55):
    fs = SRL
    n = int(0.5 * fs)
    tt = np.arange(n) / fs
    y = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 0.4 * np.exp(-tt / 0.02))) / fs) * np.exp(-tt / 0.1)
    y += 0.5 * noise(n, None, 250, fs) * np.exp(-tt / 0.03)
    place(RUMB, y * np.minimum(1, tt / 0.001), t, gain=vel, pan=rng.uniform(-0.4, 0.4))


def boulder_roll(t0, t1, vel=1.0, grow=1.4):
    """The boulder tumbling: low rolling rumble that grows, with irregular, quickening thuds."""
    fs = SRL
    dur = t1 - t0
    n = int((dur + 0.5) * fs)
    tt = np.arange(n) / fs
    x = np.clip(tt / dur, 0, 1)
    env = (0.25 + 0.75 * x ** grow) * np.where(tt < dur, 1.0, np.exp(-(tt - dur) / 0.12))
    env *= np.minimum(1, tt / 0.15)
    r = np.stack([noise(n, 25, 150, fs), noise(n, 25, 150, fs)], 1)
    r += 0.12 * np.stack([noise(n, 250, 800, fs), noise(n, 250, 800, fs)], 1)
    place(RUMB, r * env[:, None], t0, gain=0.5 * vel)
    t = t0 + 0.1
    while t < t1 - 0.12:
        k = (t - t0) / dur
        thud(t, vel=vel * (0.35 + 0.5 * k) * rng.uniform(0.6, 1.0), f0=rng.uniform(45, 75))
        t += (0.42 - 0.26 * k) * rng.uniform(0.7, 1.3)


def debris(t, vel=0.5, dur=1.0):
    for _ in range(9):
        dt = rng.uniform(0.02, dur) ** 1.5
        n = int(0.08 * SR)
        tt = np.arange(n) / SR
        y = noise(n, 200, 2500) * np.exp(-tt / rng.uniform(0.008, 0.025))
        place(HITS, y, t + dt, gain=vel * rng.uniform(0.2, 0.6) * (1 - dt / (dur + 0.2)),
              pan=rng.uniform(-0.6, 0.6))


# =============================================================================== patterns
def play_bars(t0, bars, eighth, vel=0.42, accent=0.08, ticks=False, pan=-0.12, **kw):
    """Plucked ostinato. bars: strings of 8 eighth-note tokens ('.' = rest)."""
    t = t0
    for bar, tk, v0 in bars:
        if bar:
            for i, tok in enumerate(bar.split()):
                if tok != '.':
                    v = v0 + (accent if i % 4 == 0 else 0) - (0.04 if i % 2 else 0)
                    if speaking(t + i * eighth):
                        v *= 0.85
                    pizz(t + i * eighth, note(tok), vel=v, pan=pan, **kw)
        if tk:
            for i in (1, 3, 5, 7):
                tick(t + i * eighth + rng.normal(0, 0.003), vel=0.14 * rng.uniform(0.8, 1.1),
                     pitch=1.0 if i % 4 == 1 else 1.12, pan=0.45 if i % 4 == 1 else -0.35)
        t += 8 * eighth
    return t


def ripples(t0, t1, notes, rate=0.4, vel=0.12, bright=0.55):
    """Spring water: scattered high lyre plinks, sparse under words, dense in the gaps."""
    t = t0
    while t < t1:
        sp = speaking(t)
        lyre(t, int(rng.choice(notes)), vel=vel * (0.6 if sp else 1.0) * rng.uniform(0.6, 1.0),
             bright=bright, t60=1.2, pan=rng.uniform(-0.7, 0.7))
        t += (rate if sp else 0.13) * rng.uniform(0.7, 1.35)


def heartbeat(t0, t1, period=0.92, vel=0.3, accel=1.0):
    t = t0
    while t < t1:
        fdrum(t, 'dum', vel=vel, f0=64)
        fdrum(t + 0.27 * period, 'dum', vel=vel * 0.6, f0=60)
        t += period
        period *= accel


def war_drums(t0, t1, beat=0.5, vel=0.7):
    e = beat / 2
    t = t0
    while t < t1 - 1e-6:
        for i, v in [(0, 0.75), (3, 0.55), (4, 0.68), (6, 0.5)]:
            if t + i * e < t1:
                fdrum(t + i * e, 'dum', vel=vel * v * rng.uniform(0.9, 1.05), f0=70)
        for i in (2, 5, 7):
            if t + i * e < t1:
                fdrum(t + i * e, 'tek', vel=vel * (0.12 if speaking(t + i * e) else 0.25), f0=210)
        t += 8 * e


def arp(t0, t1, chord, pattern, step, inst='lyre', vel=0.25, thin=True, **kw):
    """Arpeggiate chord tones; under narration every second note is dropped and the rest softened."""
    chord = [note(x) for x in chord]
    t, i = t0, 0
    while t < t1 - 1e-6:
        sp = thin and speaking(t)
        if not (sp and i % 2):
            m = chord[pattern[i % len(pattern)] % len(chord)]
            v = vel * (0.7 if sp else 1.0) * rng.uniform(0.85, 1.0)
            if inst == 'lyre':
                lyre(t, m, vel=v, **kw)
            else:
                piano(t, m, vel=v, **kw)
        t += step
        i += 1


# =============================================================================== the boulder motif
# (offset from root in semitones, length in beats)
MOTIF = [(0, 1.0), (2, 0.5), (3, 0.5), (7, 1.5), (5, 0.5), (0, 2.0)]          # D E F A | G -> D
MOTIF_MAJOR = [(0, 1.0), (2, 0.5), (4, 0.5), (7, 1.0), (9, 0.5), (12, 2.5)]    # D E F# A B -> D'


def motif(root, beat, vel=1.0, major=False, slip=0.0):
    """The boulder motif as phrase items. slip>0: the G slides down into the final D (the fall)."""
    out = [(root + o, d * beat, vel) for o, d in (MOTIF_MAJOR if major else MOTIF)]
    if slip and not major:
        g, d, v = out[4]
        out[4:5] = [(g, d * (1 - slip), v), ((g, root), d * slip, v)]
    return out


# =============================================================================== the score
def sec0_cold_open():
    """0 - 36: chained Death, the boulder rolls back, title card."""
    D1, D2, E2, F2, G2, A2, D3 = M('D1 D2 E2 F2 G2 A2 D3')
    drone('D1 D2 A2', 0.05, 23.2, gain=0.36, att=1.6, rel=0.5, cutoff=300)
    # 1.70 the chain locks
    metal(1.61, f0=1900, vel=0.30, decay=0.06, ratios=(1, 2.37, 3.91), click=0.9, pan=0.25)
    metal(1.70, f0=440, vel=0.6, decay=0.4, pan=0.1)
    boom(1.70, vel=0.75, f0=60, f1=36, decay=1.3)
    clinks(1.78, count=7, spread=0.7, vel=0.16, pan=0.2)
    bowed(1.70, [(D2, 2.6, 0.35)], gain=0.55, stack=(0, 12), accent=2.2, att=0.012, rel=1.6, cutoff=800, vib=0)
    # Phrygian shadows under "...iki kez kandırmış... sonsuza dek"
    pad(M('D3 F3 A3'), 2.3, 9.6, gain=0.20, att=2.0, rel=1.6, cutoff=650)
    pad(M('Bb2 D3 F3'), 8.1, 12.4, gain=0.20, att=1.4, rel=1.5, cutoff=650)
    pad(M('Eb3 G3 Bb3'), 10.8, 14.9, gain=0.18, att=1.3, rel=1.6, cutoff=600)
    pad(M('D3 F3 A3'), 13.8, 22.6, gain=0.15, att=1.6, rel=1.0, cutoff=560)
    # the motif in the low strings: "Zirveye her yaklaştığında, kaya geri yuvarlanır."
    bowed(13.75, [(D2, 0.70, 0.85), (E2, 0.35, 0.85), (F2, 0.35, 0.9), (A2, 1.14, 1.0),
                  (G2, 0.45, 0.9), ((G2, D2), 0.30, 0.85), (D2, 1.5, 0.8)],
          gain=0.55, stack=(0, 12), cutoff=950, vib=5, accent=0.5, rel=1.2)
    boulder_roll(16.97, 18.4, vel=0.3)
    # "O da aşağı iner..." walking down; "...ve yeniden başlar" the first two steps again
    for i, m in enumerate(M('D3 C3 Bb2 A2')):
        pizz(18.80 + 0.33 * i, m, vel=0.34, t60=0.9, dur=0.9)
    bowed(20.23, [(D2, 0.67, 0.7), (E2, 0.9, 0.75)], gain=0.42, stack=(0, 12), cutoff=800, rel=0.5)
    fdrum(20.23, 'dum', vel=0.32)
    riser(22.83, 1.75, vel=0.32, kind='cym')
    pad([D2, A2, D3], 21.2, 22.86, gain=0.24, att=1.6, rel=0.04, cutoff=900)
    # 22.85 TITLE: SİSİFOS — the motif, stated whole on the aulos
    T = 22.85
    boom(T, vel=1.0, f0=62, f1=33, decay=1.9)
    fdrum(T, 'dum', vel=0.9, f0=72)
    strum(T + 0.01, M('D2 A2 D3 F3 A3 D4'), vel=0.62, spread=0.016, bright=0.5)
    choir(M('D3 A3 D4 F4'), T, 27.9, gain=0.48, att=0.9, rel=1.4, vowel='a')
    pad(M('D2 A2 D3 F3 A3 E4'), T, 28.4, gain=0.18, att=0.5, rel=2.2, cutoff=1300)
    drone('D1 D2', T, 37.0, gain=0.30, att=0.3, rel=2.0)
    aulos(23.95, motif(note('D5'), 0.52, 0.9), gain=1.0, drone='D4', vib=18)
    for tt_, k, v in [(23.95, 'dum', 0.42), (24.45, 'tek', 0.2), (24.95, 'dum', 0.55), (26.08, 'dum', 0.45)]:
        fdrum(tt_, k, vel=v)
    # A06 "...neden 'mutlu' dedi?" — a first glimmer of D major on "mutlu"
    pad(M('D3 F3 A3 C4'), 27.6, 31.2, gain=0.14, att=1.5, rel=1.4, cutoff=700)
    pad(M('Bb2 D3 F3 A3'), 30.2, 33.6, gain=0.14, att=1.4, rel=1.2, cutoff=700)
    lyre(29.4, 'D2', vel=0.3)
    lyre(31.9, 'Bb1', vel=0.3)
    pad(M('D3 F#3 A3'), 32.6, 35.6, gain=0.14, att=0.5, rel=2.2, cutoff=1300)
    bell(33.62, 'F#5', vel=0.16, pan=-0.3)
    bell(33.86, 'A5', vel=0.14, pan=0.3)
    bell(34.12, 'D6', vel=0.12)


OST_A = ['D2 . F2 A2 B2 . A2 .', 'G2 . E2 F2 A2 . . .', 'D2 . F2 A2 B2 . D3 C3', 'B2 A2 G2 . E2 . C#2 .']
OST_B = ['D2 . . Eb2 D2 . . A1', 'D2 . . Eb2 D2 . F2 E2', 'D2 . . Eb2 D2 . . A1', 'Bb1 . A1 . . . C#2 .']
OST_C = ['D2 D2 . A2 D2 D2 . A2', 'C2 C2 . G2 C2 C2 . G2', 'Bb1 Bb1 . F2 Bb1 Bb1 . F2', 'A1 A1 . E2 A1 . C#2 E2']
E1 = 0.30   # chapter I: 100 BPM eighths


def sec1_cunning():
    """36 - 93: the cunning king, Autolykos and the lettered hooves (D Dorian, plucked ostinato)."""
    bars = ([(OST_A[0], False, 0.58), (OST_A[1], False, 0.62), (OST_A[2], True, 0.66), (OST_A[3], True, 0.66)]
            + [(b, True, 0.70) for b in OST_A] + [(OST_A[0], True, 0.70), (OST_A[1], True, 0.70), (None, True, 0)]
            + [(b, True, 0.66) for b in OST_B] + [(OST_B[0], True, 0.66)]
            + [(b, True, 0.72) for b in OST_C]
            + [(OST_A[0], True, 0.70), ('B2 A2 G2 . E2 . C#2 D2', False, 0.70)])
    play_bars(34.8, bars, E1)
    for k, (bar, _, _) in enumerate(bars):                 # a soft frame-drum downbeat under the ostinato
        if bar and not 16 <= k < 20:
            fdrum(34.8 + k * 8 * E1, 'dum', vel=0.24, f0=82)
    for k in range(4):                                    # hooves stamping letters in the earth
        for i in (0, 4):
            fdrum(73.2 + k * 2.4 + i * E1, 'dum', vel=0.22, f0=88)
    pad(M('D3 A3 C4 E4'), 35.0, 46.0, gain=0.21, att=3.0, rel=2.0, cutoff=700)
    pad(M('D3 F3 A3 C4'), 45.5, 53.3, gain=0.21, att=2.0, rel=1.5, cutoff=700)
    pad(M('G2 B2 D3 F3'), 52.8, 59.5, gain=0.21, att=1.5, rel=1.5, cutoff=700)
    pad(M('D3 F3 A3'), 59.0, 61.6, gain=0.21, att=0.8, rel=1.0, cutoff=800)
    pad(M('D3 Eb3 A3'), 61.2, 73.4, gain=0.21, att=1.5, rel=1.0, cutoff=500)
    for i, ch in enumerate(['D3 F3 A3', 'C3 E3 G3', 'Bb2 D3 F3', 'A2 C#3 E3']):
        pad(M(ch), 73.0 + i * 2.4, 73.2 + (i + 1) * 2.4 + 0.6, gain=0.16, att=0.5, rel=0.8, cutoff=800)
    pad(M('D3 F3 A3 E4'), 82.6, 88.0, gain=0.21, att=1.0, rel=1.5, cutoff=800)
    # winks in the gaps
    lyre_line(44.12, [('A4', 0.12), ('C5', 0.12), ('D5', 0.14), ('E5', 0.07), ('D5', 0.4)], vel=0.5, bright=0.55)
    lyre_line(52.30, [('F5', 0.15), ('E5', 0.15), ('D5', 0.4)], vel=0.42)
    aulos(59.28, [('A4', 0.11), ('B4', 0.09), ('A4', 0.16), ('F4', 0.2), ('E4', 0.1), ('D4', 0.5)], gain=0.7, vib=8)
    lyre_line(73.18, [('B4', 0.2), ('A4', 0.4)], vel=0.42)
    strum(83.40, M('D3 A3 D4 F4 A4 D5'), vel=0.5, spread=0.045, bright=0.6)        # "Beni Autolykos çaldı."
    fdrum(83.40, 'tek', vel=0.4)
    bell(83.75, 'D6', vel=0.12)
    # "Ne var ki bu zekâ... tanrıların hedefi yapacaktı."
    pad(M('D2 A2 Eb3'), 87.3, 93.9, gain=0.224, att=2.5, rel=1.6, cutoff=450)
    drone('D1 D2', 88.0, 94.2, gain=0.28, att=2.5, rel=1.4)
    boom(91.65, vel=0.45, f0=50, f1=30, decay=1.8)
    bowed(91.65, [('D2', 2.4, 0.8)], gain=0.32, stack=(0, -12), att=0.6, rel=1.2, cutoff=600, vib=4)


def sec2_eagle_spring():
    """93 - 144: the eagle (Zeus), the spring, the betrayal, thunder."""
    pad(M('D2 A2 E3 A3'), 92.8, 99.9, gain=0.213, att=2.2, rel=1.3, cutoff=900)
    pad(M('A4 E5'), 93.6, 99.8, gain=0.062, att=3.0, rel=1.4, cutoff=2600, voices=1)
    for tt_, m in [(93.62, 'D3'), (94.92, 'A3'), (96.2, 'E4'), (97.5, 'A3'), (98.96, 'D4')]:
        lyre(tt_, m, vel=0.42, bright=0.4)
    fdrum(98.95, 'dum', vel=0.45)
    # "Devasa bir kartal..." — Bb major, Zeus' colour; wing-beats
    pad(M('Bb1 F2 Bb2 D3 F3'), 99.3, 105.8, gain=0.25, att=2.6, rel=1.4, cutoff=1000)
    for tt_, v in [(100.55, 0.42), (100.82, 0.3), (101.62, 0.45), (101.89, 0.32), (102.7, 0.45), (102.97, 0.33)]:
        fdrum(tt_, 'dum', vel=v)
    boom(103.63, vel=0.55, f0=56, f1=34)
    for tt_, v in [(103.63, 0.8), (103.88, 0.6), (104.13, 0.85)]:
        fdrum(tt_, 'dum', vel=v)
    strum(103.64, M('Bb2 F3 Bb3 D4 F4'), vel=0.55, spread=0.02)
    choir(M('Bb2 F3 Bb3 D4'), 103.1, 106.4, gain=0.42, att=0.5, rel=1.6, vowel='a')
    aulos(103.72, [('A5', 0.08), (('A5', 'D6'), 0.16), ('D6', 0.45), (('D6', 'Bb5'), 0.22), ('Bb5', 0.15)],
          gain=0.75, vib=26)
    # "Kartal, kılık değiştirmiş Zeus'tu."
    pad(M('G1 D2 G2 Bb2'), 104.9, 108.6, gain=0.25, att=0.8, rel=1.4, cutoff=600)
    # "...ırmak tanrısı Asopos'un kızı, Egina."
    pad(M('F2 C3 F3 A3'), 107.9, 112.6, gain=0.175, att=1.5, rel=1.2, cutoff=800)
    ripples(108.2, 111.2, M('A4 C5 D5 E5 F5'), rate=0.45, vel=0.11)
    lyre_line(111.45, [('A4', 0.3), ('G4', 0.25), ('F4', 0.25), ('E4', 0.5)], vel=0.36)
    # Asopos wanders over mountains and plains
    for i, m in enumerate(M('D2 A2 C3 A2 Bb1 F2 A2 F2 A1 C#2')):
        pizz(112.7 + 0.8 * i, m, vel=0.5, t60=0.8, dur=0.8)
    pad(M('D3 F3 A3'), 112.4, 116.2, gain=0.15, att=1.2, rel=1.0, cutoff=700)
    pad(M('Bb2 D3 F3'), 115.7, 119.2, gain=0.15, att=1.0, rel=1.0, cutoff=700)
    pad(M('A2 C#3 E3'), 118.9, 120.8, gain=0.15, att=0.8, rel=0.8, cutoff=700)
    # "Sisifos gülümsedi..." the cunning tune again, then the bargain
    lyre_line(119.68, [('D5', 0.15), ('A4', 0.15), ('B4', 0.1), ('C#5', 0.1), ('D5', 0.3)], vel=0.4, bright=0.55)
    play_bars(120.6, [(OST_A[0], True, 0.52), ('G2 . E2 F2 . . . .', True, 0.52)], E1)
    pad(M('D3 A3 C4 E4'), 120.3, 126.8, gain=0.112, att=1.0, rel=1.0, cutoff=700)
    pizz(124.6, 'A1', vel=0.3)
    # the spring gushes from the rocks
    for i, m in enumerate(M('D4 E4 F4 G4 A4 B4 C5 D5 E5')):
        lyre(126.70 + 0.065 * i, m, vel=0.3, bright=0.6, t60=1.5, pan=-0.5 + 0.12 * i)
    pad(M('D3 G3 B3 D4'), 127.2, 131.0, gain=0.188, att=0.6, rel=1.4, cutoff=1300)
    pad(M('D3 A3 E4'), 130.5, 133.9, gain=0.175, att=1.2, rel=1.2, cutoff=1300)
    ripples(127.4, 133.9, M('D5 E5 G5 A5 B5 D6'), rate=0.42, vel=0.12)
    pad(M('G2 D3 G3 B3'), 133.0, 136.2, gain=0.2, att=0.5, rel=1.3, cutoff=1300)
    # "Ama Sisifos, tanrıların kralını ele vermişti." — Phrygian shadow
    pad(M('D2 Eb3 G3 Bb3'), 135.4, 141.3, gain=0.175, att=1.5, rel=0.4, cutoff=520)
    drone('D1 D2', 135.6, 146.0, gain=0.28, att=2.0, rel=2.0)
    bowed(138.0, [('D2', 3.2, 1.0)], gain=0.34, stack=(0, 1, 12), trem=0.7, att=2.5, rel=0.12, cutoff=800, vib=0)
    t, d = 138.6, 0.30
    while t < 141.12:
        k = (t - 138.6) / 2.6
        fdrum(t, 'dum', vel=0.18 + 0.4 * k, f0=66)
        t += d
        d = max(0.085, d * 0.9)
    # 141.21 "...unutmazdı." THUNDER
    thunder(141.21, vel=1.0)
    pad(M('D2 F2 Bb2 D3'), 141.21, 145.0, gain=0.3, att=0.03, rel=2.8, cutoff=900)
    choir(M('D2 Bb2 D3 F3'), 141.21, 145.2, gain=0.42, att=0.08, rel=2.6, vowel='o')


def sec3_death_chained():
    """144 - 199: Thanatos and the chains; Death is chained; Ares' fury (D Phrygian)."""
    drone('D1 D2', 142.0, 171.7, gain=0.28, att=2.0, rel=0.5)
    pad(M('A2 D3 Eb3'), 144.2, 152.2, gain=0.10, att=2.0, rel=1.5, cutoff=500)
    heartbeat(143.6, 157.0, period=0.92, vel=0.32)
    # "...Thanatos'u." — Death's own voice: low men, descending line
    choir(M('D2 A2'), 150.6, 157.8, gain=0.40, att=1.4, rel=1.6, vowel='o')
    bowed(150.9, [('D3', 1.2), ('C3', 1.0), ('Bb2', 1.2), ('A2', 2.4)], gain=0.32, stack=(0, -12), cutoff=700, vib=4)
    pad(M('Bb2 D3 Eb3'), 151.9, 157.6, gain=0.10, att=1.5, rel=1.5, cutoff=500)
    clinks(154.05, 5, 0.5, vel=0.12)
    boom(155.8, vel=0.35, f0=48)
    clinks(156.22, 8, 0.8, vel=0.2)
    # curiosity: "Sadece merakla zincirlere baktı."  "Bir gösterir misin?"
    pad(M('D3 A3'), 157.2, 167.4, gain=0.08, att=1.5, rel=1.0, cutoff=600)
    for tt_, m in [(158.5, 'A3'), (159.25, 'Bb3'), (160.0, 'A3'), (161.7, 'E4'), (162.5, 'F4')]:
        lyre(tt_, m, vel=0.22, bright=0.35)
    lyre_line(163.2, [('E4', 0.14), ('F4', 0.14), ('A4', 0.14), ('D5', 0.4)], vel=0.34)
    for i, m in enumerate(M('D2 A2 D2 A2')):
        pizz(164.0 + 0.6 * i, m, vel=0.3)
    aulos(166.12, [('D5', 0.07), ('Eb5', 0.07), ('D5', 0.22), ('A4', 0.38)], gain=0.6, vib=6)
    # the trick: tension rising under D05, then the lock
    bowed(167.0, [('D2', 4.45, 1.0)], gain=0.42, stack=(0, 1, 7), trem=0.75, att=3.5, rel=0.25, cutoff=750, vib=0)
    heartbeat(168.6, 171.1, period=0.55, vel=0.3, accel=0.94)
    metal(171.78, f0=1900, vel=0.32, decay=0.06, ratios=(1, 2.37, 3.91), click=0.9)
    metal(171.86, f0=440, vel=0.8, decay=0.55)
    boom(171.86, vel=0.45, f0=55, decay=0.7)
    # 173.13 "Ölüm, zincirlenmişti."
    boom(173.13, vel=0.9, f0=52, f1=30, decay=2.0)
    choir(M('D2 A2 D3 Eb3'), 173.13, 177.4, gain=0.45, att=0.06, rel=1.8, vowel='a')
    bowed(173.13, [('D2', 3.5, 0.45)], gain=0.5, stack=(0, -12), accent=2.0, att=0.01, rel=1.5, cutoff=800, vib=0)
    metal(173.13, f0=147, vel=0.32, decay=2.8, ratios=(1, 2.32, 3.87, 5.21, 6.98), click=0.1)
    drone('D1 D2', 173.1, 185.5, gain=0.26, att=0.2, rel=1.5)
    # nobody dies: time stands still
    pad(M('A4 Eb5'), 175.4, 184.4, gain=0.045, att=2.5, rel=1.4, cutoff=3200, voices=1, detune=3)
    # Ares
    for tt_, k, v in [(183.98, 'tek', 0.3), (184.13, 'tek', 0.35), (184.30, 'dum', 0.5), (184.5, 'dum', 0.6),
                      (184.68, 'dum', 0.7)]:
        fdrum(tt_, k, vel=v)
    war_drums(184.85, 197.0, beat=0.5, vel=0.62)
    agit = [('D2', 0.2), (None, 0.05), ('D2', 0.2), (None, 0.05), ('Eb2', 0.2), (None, 0.05), ('D2', 0.2), (None, 0.05),
            ('D2', 0.2), (None, 0.05), ('D2', 0.2), (None, 0.05), ('F2', 0.2), (None, 0.05), ('Eb2', 0.2), (None, 0.05)]
    bowed(184.85, agit * 3, gain=0.34, stack=(0, 12), cutoff=850, vib=0, att=0.02,
          accent=0.6, rel=0.3)
    bowed(191.03, agit * 3, gain=0.36, stack=(0, 12), cutoff=900, vib=0, att=0.02, accent=0.6, rel=0.3)
    pad(M('D2 A2 Eb3'), 184.6, 197.4, gain=0.12, att=3.0, rel=0.3, cutoff=700)
    pad(M('D2 A2 D3 Eb3 A3'), 190.25, 191.4, gain=0.30, att=0.03, rel=0.8, cutoff=1800)   # Ares' cry
    boom(190.25, vel=0.55)
    metal(193.5, f0=415, vel=0.55, decay=0.5)                                                 # chains fall
    clinks(193.55, 10, 0.9, vel=0.2)
    # 197.2 handed over to Death
    boom(197.2, vel=0.85, f0=50, decay=2.2)
    fdrum(197.2, 'dum', vel=0.8)
    choir(M('D2 A2 Eb3'), 197.2, 199.4, gain=0.4, att=0.05, rel=1.6, vowel='o')
    bowed(197.25, [('D3', 0.25, 0.9), (('D3', 'D2'), 1.5, 0.7), ('D2', 0.5, 0.4)], gain=0.34, stack=(0, -12),
          rel=0.8, cutoff=700, vib=0)


def sec4_second_trick():
    """199 - 243: the whisper, the underworld, sunlit freedom, dragged back."""
    pad(M('D3 A3 F4'), 199.0, 205.0, gain=0.168, att=1.5, rel=1.2, cutoff=500)
    for tt_, m in [(199.5, 'A3'), (201.2, 'F3'), (202.9, 'D4'), (204.5, 'E4'), (204.82, 'D4')]:
        lyre(tt_, m, vel=0.34, bright=0.3)
    pad(M('D3 A3'), 204.6, 210.0, gain=0.126, att=1.0, rel=1.0, cutoff=450)
    # descent to the underworld
    boom(209.5, vel=0.45, f0=45)
    choir(M('D2 A2'), 209.4, 217.6, gain=0.32, att=0.8, rel=1.6, vowel='u')
    for i, m in enumerate(M('A3 G3 F3 E3 D3')):
        lyre(209.5 + 0.22 * i, m, vel=0.4, bright=0.35)
    drone('D1 D2', 209.4, 228.4, gain=0.26, att=1.0, rel=1.4)
    pad(M('Bb2 D3 Eb3 G3'), 210.8, 225.8, gain=0.231, att=2.0, rel=1.5, cutoff=550)
    choir(M('A4 D5'), 213.5, 217.6, gain=0.18, att=1.5, rel=1.4, vowel='u', voices=3)       # Persephone
    # the sly plea, in the shadows
    play_bars(217.3, [(b, True, 0.56) for b in OST_B[:3]], E1)
    lyre_line(224.70, [('D5', 0.15), ('C#5', 0.15), ('D5', 0.4)], vel=0.34)
    pizz(225.4, 'D2', vel=0.45)
    # "Persefoni ona inandı." -> out into the sun
    aulos(226.95, [('A4', 0.1), ('B4', 0.08), ('C5', 0.08), ('D5', 0.35)], gain=0.6, vib=8)
    for i, m in enumerate(M('D4 E4 G4 A4 B4 D5 G5')):
        lyre(227.55 + 0.075 * i, m, vel=0.3, bright=0.6, t60=1.6, pan=-0.5 + 0.15 * i)
    riser(228.1, 1.2, vel=0.2, kind='cym')
    pad(M('G2 D3 G3 B3 D4'), 228.0, 230.6, gain=0.357, att=0.4, rel=1.0, cutoff=1500)
    pad(M('C3 G3 C4 E4'), 230.2, 232.1, gain=0.315, att=0.6, rel=0.8, cutoff=1500)
    pad(M('G2 B2 D3 G3'), 231.7, 236.6, gain=0.315, att=0.6, rel=1.4, cutoff=1400)
    arp(228.2, 232.4, M('G3 B3 D4 G4 C4 E4'), [0, 1, 2, 3, 2, 1], 0.25, vel=0.34, bright=0.55, thin=True)
    pizz(233.0, 'G2', vel=0.45)
    lyre_line(233.95, [('G4', 0.1), ('A4', 0.1), ('B4', 0.1), ('D5', 0.12), ('G5', 0.5)], vel=0.42, bright=0.6)
    strum(234.45, M('G3 B3 D4 G4'), vel=0.4, spread=0.03, bright=0.55)
    # "Ta ki tanrıların habercisi Hermes..." -> dragged back
    pad(M('Bb2 D3 F3'), 236.4, 238.9, gain=0.273, att=0.8, rel=0.8, cutoff=700)
    for i in range(12):
        tick(238.30 + 0.05 * i, vel=0.1 + 0.01 * i, pitch=1.1, pan=-0.6 + 0.1 * i)
    pad(M('D2 Eb3 G3 Bb3'), 238.6, 241.6, gain=0.294, att=0.8, rel=0.6, cutoff=500)
    bowed(239.4, [('D3', 0.3, 0.8), (('D3', 'D1'), 2.2, 0.85), ('D1', 0.4, 0.6)], gain=0.36, stack=(0, 12),
          cutoff=650, vib=0, rel=0.5)
    riser(242.9, 1.6, vel=0.26)


def sec5_punishment():
    """243 - 294: Tartaros. The push (motif rising word by word), the slip, the crash, the endless cycle."""
    D1, D2, E2, F2, G2, A2, Bb2 = M('D1 D2 E2 F2 G2 A2 Bb2')
    boom(242.9, vel=0.9, f0=50, f1=30, decay=2.0)
    drone('D1 D2 A2', 242.9, 266.0, gain=0.33, att=0.3, rel=0.6, cutoff=300)
    choir(M('D2 A2'), 243.0, 248.6, gain=0.32, att=1.5, rel=1.4, vowel='u')
    pad(M('D3 Eb3'), 243.4, 258.6, gain=0.08, att=3.0, rel=1.5, cutoff=450)
    boom(247.35, vel=0.4, f0=46)
    bowed(247.3, [(D2, 1.2, 0.7)], gain=0.3, stack=(0, 12), att=0.4, rel=0.6, cutoff=600, vib=0)
    pad(M('D2 A2 Eb3'), 248.0, 254.4, gain=0.12, att=1.5, rel=1.2, cutoff=450)
    # "Tepenin dibinde, dev bir kaya."
    boom(252.95, vel=0.65, f0=48, f1=29, decay=1.8)
    bowed(252.95, [(D2, 2.4, 0.7)], gain=0.4, stack=(0, -12), accent=1.0, att=0.05, rel=1.0, cutoff=600, vib=0)
    choir(M('D2 A2 D3'), 253.9, 256.0, gain=0.34, att=0.6, rel=1.2, vowel='o')
    fdrum(258.3, 'dum', vel=0.45, f0=62)
    bowed(258.3, [(D2, 1.0, 0.6)], gain=0.3, stack=(0, -12), att=0.8, rel=0.1, cutoff=600, vib=0)
    # F04 — the motif climbs with the words; cut to silence on "...kalmıştı ki"
    push = [(D2, 1.82, 0.75), (E2, 0.86, 0.82), (F2, 1.16, 0.88), (A2, 1.28, 0.95), (Bb2, 0.94, 1.0)]
    bowed(259.36, push, gain=0.55, stack=(0, -12, 12), cutoff=900, vib=4, accent=0.7, rel=0.06, att=0.06)
    bowed(263.2, [(A2 + 12, 1.28, 0.6), (Bb2 + 12, 0.94, 1.0)], gain=0.24, trem=0.8, cutoff=1400, vib=0,
          att=0.6, rel=0.06)
    for tt_, v in [(259.36, 0.7), (261.18, 0.75), (262.04, 0.78), (263.20, 0.85), (264.48, 0.9)]:
        fdrum(tt_, 'dum', vel=v, f0=62)
        boom(tt_, vel=0.28 + 0.1 * v, f0=48, decay=0.8)
    choir(M('A2 D3 E3'), 263.2, 265.45, gain=0.30, att=1.4, rel=0.05, vowel='a')
    riser(265.42, 1.0, vel=0.18, kind='cym')
    # 266.27 "Kaya elinden kurtuldu." — slip, fall, tumble; 271.09 crash
    boom(266.27, vel=0.9, f0=70, f1=34, decay=1.2)
    fdrum(266.27, 'dum', vel=0.9, f0=70)
    bowed(266.27, [(G2, 0.3, 1.0), ((G2, D1), 1.7, 0.85), (D1, 0.6, 0.5)], gain=0.5, stack=(0, 12), cutoff=800,
          vib=0, rel=0.6, accent=1.0, att=0.01)
    for i, m in enumerate(M('A3 G3 F3 E3 D3 C3 Bb2 A2 G2 F2 E2 D2')):
        lyre(266.33 + 0.1 * i, m, vel=0.3 * (1 - 0.04 * i), bright=0.35, t60=1.0, pan=0.5 - 0.08 * i)
    boulder_roll(266.4, 271.09, vel=1.0)
    t = 266.6
    while t < 270.9:
        fdrum(t, 'dum', vel=rng.uniform(0.15, 0.35), f0=rng.uniform(55, 80), pan=rng.uniform(-0.4, 0.4))
        t += rng.uniform(0.18, 0.45)
    T = 271.09
    boom(T, vel=1.25, f0=58, f1=27, decay=2.4, knock=0.8)
    fdrum(T, 'dum', vel=1.0, f0=60)
    debris(T + 0.02, vel=0.5)
    bowed(T, [(D2, 2.2, 0.4)], gain=0.55, stack=(0, -12, 7), accent=2.2, att=0.01, rel=1.4, cutoff=900, vib=0)
    choir(M('D2 A2 D3'), T, 273.4, gain=0.42, att=0.05, rel=1.8, vowel='a')
    drone('D1 D2', T, 294.6, gain=0.30, att=0.2, rel=1.5)
    # "Sisifos aşağı indi." walking down; "Ve yeniden başladı." the cycle
    for i, m in enumerate(M('A2 G2 F2 E2 D2')):
        pizz(273.45 + 0.4 * i, m, vel=0.3, t60=0.9, dur=0.9)
    b = (292.75 - 275.93) / 22.0
    cyc = []
    for k in range(4):                                     # D E F A | G -> D, four times, heavier each time
        cyc += motif(D2, b, 0.75 + 0.08 * k, slip=0.25)
    cyc[-1] = (D2, 0.6, cyc[-1][2])                        # the last fall dies away into Camus
    bowed(275.93, cyc, gain=0.58, stack=(0, -12), cutoff=950, vib=3, accent=0.8, rel=1.3)
    bowed(275.93 + 6 * b, cyc[7:], gain=0.18, stack=(12,), cutoff=1100, vib=3, accent=0.6, rel=1.1)
    for k in range(4):
        c0 = 275.93 + 6 * b * k
        boom(c0, vel=0.42 + 0.08 * k, f0=50, decay=1.0)
        for beat_, v in [(0, 0.75), (2, 0.8), (4, 0.7)]:
            fdrum(c0 + beat_ * b, 'dum', vel=v * (0.8 + 0.07 * k), f0=60)
        if k >= 1:
            for beat_ in (1, 3, 5):
                fdrum(c0 + beat_ * b, 'dum', vel=0.25 + 0.04 * k, f0=74)
    choir(M('D2 A2 D3'), 275.93 + 6 * b, 293.6, gain=0.30, att=2.5, rel=1.4, vowel='o')
    pad(M('D2 A2 Eb3'), 284.0, 293.0, gain=0.10, att=3.0, rel=0.8, cutoff=700)
    boom(292.75, vel=0.95, f0=52, f1=28, decay=2.2)
    fdrum(292.75, 'dum', vel=0.9, f0=58)


def sec6_camus():
    """294 - 384: Camus, 1942. Felt piano and warm pads; Dorian brightening to D major / Lydian."""
    BT = 60 / 70.0
    # 294.01 style change
    piano(294.01, 'D4', vel=0.45)
    piano(294.03, 'A4', vel=0.35)
    piano(294.05, 'D2', vel=0.3)
    chords = [(294.0, 300.2, 'D3 A3 C4 E4 F4'), (300.0, 303.6, 'Bb2 F3 A3 D4'), (303.4, 307.1, 'G2 D3 F3 Bb3 A3'),
              (306.9, 310.0, 'A2 E3 G3 C#4')]
    for a, b, ch in chords:
        pad(M(ch), a, b, gain=0.102, att=1.6, rel=1.5, cutoff=800, sine=0.6)
    arp(295.0, 309.6, M('D3 A3 E4 F4'), [0, 1, 2, 1, 3, 1], 2 * BT, inst='piano', vel=0.3)
    fdrum(299.3, 'dum', vel=0.18, f0=52)          # "...dünya yeniden savaştayken" — a far drum
    fdrum(299.75, 'dum', vel=0.14, f0=50)
    boom(300.7, vel=0.22, f0=45, decay=1.6)
    for tt_, m in [(309.8, 'F4'), (310.2, 'E4'), (310.6, 'D4')]:
        piano(tt_, m, vel=0.4)
    # G03 the daily round: a repeating piano figure; stops at "Bütün bunlar ne için?"
    rnd = [('D3 A3 E4 A3', 311.0), ('C3 G3 D4 G3', 314.43), ('Bb2 F3 C4 F3', 317.86)]
    for ch, t0 in rnd:
        notes = M(ch)
        for i in range(8):
            t = t0 + i * BT / 2
            piano(t, notes[i % 4], vel=(0.17 if speaking(t) else 0.3) * (1.1 if i % 4 == 0 else 1.0))
    for a, b, ch in [(310.8, 314.8, 'D3 A3 C4 E4'), (314.2, 318.2, 'C3 G3 B3 E4'), (317.6, 321.6, 'Bb2 F3 A3 D4'),
                     (321.2, 325.8, 'Bb2 F3 A3 E4')]:
        pad(M(ch), a, b, gain=0.093, att=1.2, rel=1.4, cutoff=800, sine=0.6)
    # G04 "Evren bu soruya cevap vermez." — almost nothing
    pad(M('A5'), 323.6, 333.4, gain=0.03, att=3.0, rel=2.0, cutoff=2500, sine=0.9, voices=1, detune=2)
    drone('D2', 323.8, 334.4, gain=0.08, att=3.0, rel=1.5, cutoff=300)
    piano(325.2, 'D5', vel=0.2)
    piano(328.2, 'A4', vel=0.18)
    piano(331.3, 'E4', vel=0.3)                    # "absürt": a semitone crack
    piano(331.32, 'F4', vel=0.28)
    piano(332.4, 'D2', vel=0.3)
    # G05 the way back down: heavy but steady steps
    steps = M('D3 C3 Bb2 A2 G2 F2 E2 D2')
    for i, m in enumerate(steps):
        t = 334.0 + 1.2 * i
        piano(t, m, vel=0.34)
        fdrum(t, 'dum', vel=0.16, f0=58)
    for a, b, ch in [(333.8, 336.6, 'D3 F3 A3'), (336.2, 339.0, 'Bb2 D3 F3 A3'), (338.6, 341.4, 'G2 Bb2 D3 F3'),
                     (341.0, 343.6, 'A2 C#3 E3 G3'), (343.3, 345.4, 'D3 F3 A3')]:
        pad(M(ch), a, b, gain=0.102, att=1.0, rel=1.0, cutoff=850, sine=0.5)
    piano(344.2, 'A4', vel=0.36)
    piano(344.6, 'D5', vel=0.34)
    # G06 "O dönüş, bir nefes gibidir." — breathing, brightening
    for a, b, ch in [(345.0, 348.7, 'F2 C3 F3 A3'), (348.3, 351.5, 'C3 G3 C4 E4'), (351.1, 354.3, 'G2 D3 G3 B3'),
                     (353.9, 356.0, 'A2 E3 A3 D4'), (355.6, 357.9, 'A2 E3 A3 C#4')]:
        pad(M(ch), a, b, gain=0.119, att=1.2, rel=1.0, cutoff=950, sine=0.5, breathe=0.25)
    for tt_, m in [(347.18, 'A4'), (350.2, 'E5'), (353.95, 'B4')]:       # in the narrator's breaths
        piano(tt_, m, vel=0.2)
    # 357.65 the first D major: the motif half-remembered (D E F#), not yet complete
    pad(M('D2 A2 D3 F#3 A3'), 357.5, 361.0, gain=0.145, att=0.5, rel=1.4, cutoff=1400, sine=0.4)
    for tt_, m in [(357.75, 'D4'), (358.15, 'E4'), (358.55, 'F#4')]:
        piano(tt_, m, vel=0.4)
    # G07 "Kaya onundur..." — D major, a warm pulse
    for a, b, ch in [(359.0, 360.7, 'B1 F#2 B2 D3'), (360.4, 362.1, 'G1 D2 G2 B2'), (361.8, 363.8, 'E2 B2 D3 G3'),
                     (363.5, 365.8, 'A1 E2 A2 C#3 E3'), (365.4, 367.3, 'D2 A2 D3 F#3')]:
        pad(M(ch), a, b, gain=0.128, att=0.9, rel=0.9, cutoff=1000, sine=0.45)
    for a, b, ch in [(366.9, 368.3, 'G2 D3 F#3 B3'), (367.9, 370.9, 'A2 D3 E3 A3')]:      # hush for G08
        pad(M(ch), a, b, gain=0.085, att=0.9, rel=0.9, cutoff=750, sine=0.5)
    for k in range(10):
        fdrum(359.15 + 2 * BT * k, 'dum', vel=0.09, f0=58)
    arp(359.2, 365.4, M('D4 F#4 A4 B4'), [0, 2, 1, 3], 2 * BT, inst='piano', vel=0.24)
    piano(365.6, 'F#4', vel=0.32)
    piano(366.0, 'A4', vel=0.32)
    # G08 / gap: rising arpeggio, strings swell
    for i, m in enumerate(M('A3 D4 E4 A4 D5')):
        piano(369.62 + 0.18 * i, m, vel=0.32)
    # G09 the quote: strings rise under it
    for a, b, ch in [(370.4, 372.5, 'G2 D3 B3'), (372.2, 374.1, 'A2 E3 C#4'), (373.8, 375.9, 'B2 F#3 D4'),
                     (375.6, 378.3, 'G2 D3 A3 B3')]:
        pad(M(ch), a, b, gain=0.145, att=0.9, rel=0.6, cutoff=1300, vib=4)
    # 375.73 - 378.19 the boulder motif rises in major ... and is completed at 378.19
    up = [('D4', 0.45, 0.8), ('E4', 0.30, 0.85), ('F#4', 0.35, 0.9), ('A4', 0.60, 0.95), ('B4', 0.64, 1.0),
          ('D5', 0.7, 0.9)]
    bowed(375.85, up, gain=0.36, stack=(0, -12), cutoff=1800, vib=10, accent=0.3, rel=1.0, glide=0.05)
    t = 375.85
    for m, d, v in up:
        piano(t, m, vel=0.42 * v)
        lyre(t + 0.005, m, vel=0.32 * v, bright=0.5)
        t += d
    choir(M('D3 A3 D4'), 376.0, 378.35, gain=0.22, att=1.8, rel=0.2, vowel='a')
    riser(378.17, 2.2, vel=0.22, kind='cym')
    t, d = 376.8, 0.24
    while t < 378.1:
        fdrum(t, 'dum', vel=0.12 + 0.25 * (t - 376.8) / 1.3, f0=60)
        t += d
        d = max(0.07, d * 0.85)
    # 378.19 "Sisifos'u mutlu hayal etmek gerekir." — D major blooms (Lydian light)
    T = 378.19
    boom(T, vel=0.5, f0=46, f1=32, decay=2.0, knock=0.25)
    strum(T, M('D2 A2 D3 F#3 A3 D4 F#4'), vel=0.34, spread=0.03, bright=0.3)
    pad(M('D2 A2 D3 F#3 A3'), T, 385.6, gain=0.153, att=0.3, rel=2.2, cutoff=900, vib=3)
    choir(M('D3 F#3 A3 D4'), 379.6, 384.9, gain=0.36, att=1.3, rel=2.0, vowel='a')
    bell(378.45, 'D6', vel=0.13, pan=-0.2)                # in the breath before "mutlu"
    bell(378.62, 'A6', vel=0.10, pan=0.25)
    # 380.85 - 384.3 luminous after-glow: the completed motif, high, with the Lydian G#
    hi = [('D5', 0.40), ('E5', 0.20), ('F#5', 0.20), ('A5', 0.55), ('B5', 0.25), ('D6', 1.6)]
    lyre_line(380.95, hi, vel=0.5, bright=0.6)
    bowed(380.95, [(m, d, 0.9) for m, d in hi], gain=0.30, stack=(0, -12), cutoff=2600, vib=12, accent=0.2,
          rel=1.6, glide=0.04)
    pad(M('D2 A2 F#3 C#4 E4 G#4'), 380.6, 386.2, gain=0.128, att=1.2, rel=2.0, cutoff=2400, vib=4)
    choir(M('D4 F#4 A4'), 381.0, 385.4, gain=0.26, att=1.0, rel=2.0, vowel='a')
    bell(382.6, 'D6', vel=0.14)
    bell(382.8, 'G#6', vel=0.08, pan=0.4)


def sec7_outro():
    """384 - 425: 'Senin kayan ne?' — warm, intimate; then the end-screen statement."""
    E = 60 / 72.0 / 2
    prog1 = [(384.3, 'D2 A2 F#3 A3'), (386.0, 'B1 F#2 D3 F#3'), (387.65, 'G1 D2 B2 D3'), (389.3, 'A1 E2 C#3 E3'),
             (391.0, 'D2 A2 F#3 A3'), (392.65, 'G1 D2 B2 D3'), (393.9, 'G1 D2 B2 D3'), (395.55, 'A1 E2 C#3 E3'),
             (397.2, 'B1 F#2 D3 F#3'), (398.85, 'G1 D2 B2 D3'), (400.5, 'A1 E2 A2 D3')]
    for i, (t0, ch) in enumerate(prog1):
        t1 = prog1[i + 1][0] if i + 1 < len(prog1) else 402.4
        arp(t0, t1, M(ch), [0, 1, 2, 3, 2, 1], E, vel=0.42, bright=0.33, thin=True)
        pad(M(ch)[1:], t0 - 0.3, t1 + 0.5, gain=0.21, att=0.8, rel=0.8, cutoff=850, sine=0.5)
    drone('D2', 384.0, 402.6, gain=0.10, att=2.0, rel=1.5, cutoff=240)
    lyre_line(392.9, [('F#4', 0.3), ('E4', 0.3), ('D4', 0.6)], vel=0.5)
    lyre_line(400.95, [('A4', 0.35), ('B4', 0.3), ('A4', 0.3), ('F#4', 0.6)], vel=0.5)
    # H03 "Peki ya sen? Senin kayan ne?" — almost alone; the motif asks, unresolved
    pad(M('G2 D3 A3 B3'), 402.3, 406.6, gain=0.21, att=1.0, rel=1.2, cutoff=900, sine=0.5)
    question = [('D4', 0.40), ('E4', 0.20), ('F#4', 0.20), ('A4', 0.40), ('B4', 1.2)]
    lyre_line(404.45, question, vel=0.52, bright=0.5)
    t = 404.45
    for m, d in question:
        piano(t + 0.01, m, vel=0.2)
        t += d
    # H04 back to warmth, cadence into the end screen
    for i, (t0, ch) in enumerate([(406.2, 'E2 B2 D3 G3'), (407.9, 'G1 D2 B2 D3'), (409.6, 'A1 E2 A2 C#3')]):
        arp(t0, t0 + 1.7, M(ch), [0, 1, 2, 3, 2, 1], E, vel=0.42, bright=0.33, thin=True)
        pad(M(ch)[1:], t0 - 0.3, t0 + 2.2, gain=0.21, att=0.8, rel=0.8, cutoff=850, sine=0.5)
    # 410.69 END SCREEN: the completed boulder motif, then the answer, then home
    B = 0.82
    T = 410.72
    strum(T, M('D2 A2 D3 F#3 A3'), vel=0.6, spread=0.03, bright=0.45)
    mel = motif(note('D5'), B, 1.0, major=True)                       # D E F# A B -> D', completed
    mel[-1] = (mel[-1][0], mel[-1][1] + 2 * B, 1.0)                   # ... and the summit is held
    mel += [(note(m), d * B, 0.9) for m, d in [('A5', 1.0), ('F#5', 0.5), ('E5', 0.5), ('D5', 2.0)]]
    t = T
    for m, d, v in mel:
        lyre(t, m, vel=0.68 * v, bright=0.55)
        t += d
    bowed(T, [(m, d, v) for m, d, v in mel], gain=0.34, stack=(-12,), cutoff=1800, vib=10, accent=0.2,
          rel=1.0, glide=0.05)
    harm = [(0, 2, 'D2 A2 D3 F#3 A3'), (2, 4, 'G1 D2 G2 B2 D3'), (4, 6, 'B1 F#2 B2 D3 F#3'),
            (6, 8, 'G1 D2 G2 B2 E3'), (8, 10, 'G1 D2 B2 D3'), (10, 12, 'A1 E2 A2 C#3 E3')]
    for b0, b1, ch in harm:
        arp(T + b0 * B, T + b1 * B, M(ch), [0, 1, 2, 3, 4, 3], B / 2, vel=0.34, bright=0.4, thin=False)
        pad(M(ch)[1:], T + b0 * B - 0.3, T + b1 * B + 0.6, gain=0.24, att=0.7, rel=0.9, cutoff=1100, sine=0.4)
    for k in range(6):
        fdrum(T + 2 * k * B, 'dum', vel=0.3, f0=56)
    F = T + 12 * B                                          # final chord ~420.6
    strum(F, M('D2 A2 D3 F#3 A3 D4 F#4'), vel=0.62, spread=0.04, bright=0.45)
    lyre(F + 0.35, 'D5', vel=0.32, bright=0.5)
    pad(M('D2 A2 D3 F#3 A3 E4'), F - 0.3, DUR + 0.5, gain=0.266, att=0.8, rel=3.5, cutoff=1300, sine=0.4)
    choir(M('D3 A3 F#4'), F, DUR + 0.5, gain=0.2, att=1.0, rel=3.5, vowel='a')
    drone('D1 D2', F - 0.2, DUR + 0.5, gain=0.16, att=0.6, rel=3.5, cutoff=240)
    fdrum(F, 'dum', vel=0.3, f0=54)
    bell(F + 0.05, 'D6', vel=0.12)
    bell(F + 0.9, 'A5', vel=0.09, pan=0.3)


# =============================================================================== mixing
def reverb_ir(fs=SR, length=4.0, pre=0.02, seed=7):
    """Stereo hall: decorrelated noise, frequency-dependent decay, soft build-up, return EQ baked in."""
    r = np.random.default_rng(seed)
    n = int(length * fs)
    t = np.arange(n) / fs
    out = np.zeros((n + int(pre * fs), 2))
    for c in range(2):
        w = r.standard_normal(n)
        acc = np.zeros(n)
        for lo, hi, t60 in [(None, 350, 3.1), (350, 1400, 2.8), (1400, 4200, 2.1), (4200, 7600, 1.3)]:
            b = lp(w, hi, fs, 4) if lo is None else bp(w, lo, hi, fs, 3)
            acc += b * np.exp(-6.9078 * t / t60)
        out[int(pre * fs):, c] = acc * (1 - np.exp(-t / 0.018))
    out = hp(out, 90, fs, 2)
    out /= np.sqrt((out ** 2).sum(0).mean() * fs / SR)     # same in-band gain at any rate
    return out


PRIORITY = {'A01': 1.3, 'A05': 1.3, 'C08': 1.6, 'D06': 1.3, 'F05': 1.2, 'G10': 2.0}   # lines that must cut through


def speech_mask():
    """Smoothed 'narration present' curve on a 10 ms grid (cues.md, refined with vo.wav).
    1.0 = normal duck; key lines (PRIORITY) duck deeper."""
    hop = 0.01
    tg = np.arange(0, DUR + 1.0, hop)
    act = np.zeros(len(tg), bool)
    weight = np.ones(len(tg))
    for c, (a, b) in CUE.items():
        on = (tg >= a - 0.06) & (tg <= b + 0.04)
        act |= on
        weight[on] = np.maximum(weight[on], PRIORITY.get(c, 1.0))
    used_vo = False
    if VO_PATH.exists():
        with wave.open(str(VO_PATH)) as w:
            vo = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0
            if w.getnchannels() > 1:
                vo = vo.reshape(-1, w.getnchannels()).mean(1)
        h = int(hop * SR)
        k = len(vo) // h
        rms = np.sqrt(np.mean(vo[:k * h].reshape(k, h) ** 2, 1) + 1e-12)
        db = 20 * np.log10(rms)
        on = binary_dilation(db > -48.0, np.ones(13, bool))
        act[:min(k, len(act))] |= on[:len(act)]
        used_vo = True
    act = binary_closing(act, np.ones(int(0.35 / hop), bool))
    x = act * weight
    ra, rr = np.exp(-hop / 0.10), np.exp(-hop / 0.38)
    fwd = np.empty_like(x)
    bwd = np.empty_like(x)
    y = 0.0
    for i in range(len(x)):
        y = max(x[i], y * rr)
        fwd[i] = y
    y = 0.0
    for i in range(len(x) - 1, -1, -1):
        y = max(x[i], y * ra)
        bwd[i] = y
    return tg, np.maximum(fwd, bwd), used_vo


def duck_depth(freqs, scale=1.0):
    """How many dB each frequency is pulled down while narration is present."""
    pts_f = np.log2([20, 110, 220, 3800, 6500, 24000])
    pts_d = np.array([3.0, 3.0, 9.0, 9.0, 5.0, 5.0]) * scale
    return np.interp(np.log2(np.maximum(freqs, 20)), pts_f, pts_d)


def master_eq(freqs):
    """Static master EQ applied inside the STFT: 35 Hz high-pass (removes DC) and 13.5 kHz low-pass."""
    f = np.maximum(freqs, 1e-3)
    return 1 / np.sqrt(1 + (35 / f) ** 8) / np.sqrt(1 + (f / 13500) ** 8)


def fftconv(x, h):
    """Linear convolution of a long signal with an impulse response in one multi-threaded FFT."""
    L = sfft.next_fast_len(len(x) + len(h) - 1, real=True)
    X = sfft.rfft(np.asarray(x, np.float32), L, workers=-1)
    X *= sfft.rfft(np.asarray(h, np.float32), L, workers=-1)
    return sfft.irfft(X, L, workers=-1)[:len(x)]


def spectral_duck(layers, mt, mv):
    """STFT dynamic EQ: while the narrator talks, cut the speech band (and a little of everything).
    layers: [(signal, depth_scale)]; each layer gets its own depth, the results are summed."""
    nfft = 2048
    hop = nfft // 4
    win = np.sqrt(0.5 - 0.5 * np.cos(2 * np.pi * np.arange(nfft) / nfft)).astype(np.float32)
    freqs = np.fft.rfftfreq(nfft, 1 / SR)
    n = len(layers[0][0])
    pads = [np.concatenate([np.zeros(nfft, np.float32), np.asarray(x, np.float32), np.zeros(2 * nfft, np.float32)])
            for x, _ in layers]
    views = [sliding_window_view(xp, nfft)[::hop] for xp in pads]
    depths = [duck_depth(freqs, d).astype(np.float32) for _, d in layers]
    eq = master_eq(freqs).astype(np.float32)
    nfr = len(views[0])
    out = np.zeros((nfr + 3, hop), np.float32)
    sv = np.interp((np.arange(nfr) * hop + nfft / 2 - nfft) / SR, mt, mv).astype(np.float32)
    for c0 in range(0, nfr, 8192):
        c1 = min(nfr, c0 + 8192)
        acc = 0
        for v, D in zip(views, depths):
            F = sfft.rfft(v[c0:c1] * win, axis=1, workers=-1)
            F *= np.power(np.float32(10.0), -(sv[c0:c1, None] * D[None, :]) / np.float32(20.0))
            acc = acc + F
        y = (sfft.irfft(acc * eq, nfft, axis=1, workers=-1) * win).reshape(c1 - c0, 4, hop)
        for q in range(4):
            out[c0 + q:c1 + q] += y[:, q, :]
    return out.reshape(-1)[nfft:nfft + n] * 0.5


def upsample(x, k):
    """Band-limited integer upsampling of a whole stereo track in one multi-threaded FFT."""
    n = len(x)
    L = sfft.next_fast_len(n, real=True)
    X = sfft.rfft(x, L, axis=0, workers=-1)
    Y = np.zeros((L * k // 2 + 1, x.shape[1]), X.dtype)
    Y[:len(X)] = X * k
    Y[len(X) - 1] *= 0.5
    return sfft.irfft(Y, L * k, axis=0, workers=-1)[:n * k].astype(np.float32)


def master_gain(n):
    """Dramatic near-silence before the slip, and the final fade; computed on a 5 ms grid."""
    tg = np.arange(0, n / SR + 0.01, 0.005)
    g = np.ones(len(tg))
    for a, b, lvl in [(265.42, 266.24, 0.006)]:
        g = np.minimum(g, np.interp(tg, [a, a + 0.07, b - 0.02, b], [1.0, lvl, lvl, 1.0], left=1.0, right=1.0))
    g *= np.interp(tg, [DUR - 2.6, DUR], [1.0, 0.0], left=1.0, right=0.0) ** 1.5
    return tg, g


def limiter_gain(mix, blk=240):
    """Gentle look-ahead limiter on a 5 ms block envelope: only the biggest hits get touched."""
    nb = len(mix) // blk
    pk = np.abs(mix[:nb * blk]).max(1).reshape(nb, blk).max(1)
    env = maximum_filter1d(pk, size=5)
    thr = np.percentile(env, 99.9) * 1.15
    g = minimum_filter1d(np.minimum(1.0, thr / (env + 1e-12)), size=7)
    k = np.hanning(9)
    g = np.convolve(g, k / k.sum(), mode='same')
    tb = (np.arange(nb) + 0.5) * blk
    return np.interp(np.arange(len(mix), dtype=float), tb, g)


def mixdown():
    t = time.time()
    lap = []

    def mark(what):
        nonlocal t
        lap.append(f'{what} {time.time() - t:.1f}s')
        t = time.time()

    # lyre: wooden body + gentle top cut, one FFT convolution per channel
    body = body_ir()
    body = lp(body, 9000, SR, 2)
    for c in range(2):
        y = fftconv(LYRE.x[:, c], body).astype(np.float32)
        arr(SR, 'full')[:, c] += y
        arr(SR, 'send')[:, c] += y * np.float32(LYRE.send)
    LYRE.x = None
    mark('lyre')
    # reverb, once per rate (low-rate buses get a 16 kHz version of the same hall)
    for fs in (SR, SRL):
        ir = reverb_ir(fs)
        snd = arr(fs, 'send')
        dst = arr(fs, 'full')
        for c in range(2):
            dst[:, c] += fftconv(snd[:, c], ir[:, c]).astype(np.float32)
        del _ARR[(fs, 'send')]
    mark('reverb')
    full = arr(SR, 'full')[:N]
    hits = arr(SR, 'hits')[:N]
    full += upsample(arr(SRL, 'full'), SR // SRL)[:N]
    hits += upsample(arr(SRL, 'hits'), SR // SRL)[:N]
    del _ARR[(SRL, 'full')], _ARR[(SRL, 'hits')]
    mark('upsample')
    mt, mv, used_vo = speech_mask()
    mix = np.stack([spectral_duck([(full[:, c], 1.0), (hits[:, c], 0.55)], mt, mv) for c in range(2)], 1)
    _ARR.clear()
    mark('duck+eq')
    tg, gg = master_gain(N)
    mix *= np.interp(np.arange(N, dtype=float) / SR, tg, gg).astype(np.float32)[:, None]
    mix *= limiter_gain(mix).astype(np.float32)[:, None]
    mix *= np.float32(10 ** (-1 / 20) / np.abs(mix).max())
    mark('master')
    print('  mix: ' + ', '.join(lap), flush=True)
    return mix, used_vo


def write_wav(path, mix):
    d = (rng.random(mix.shape, np.float32) - rng.random(mix.shape, np.float32)) / np.float32(32768.0)  # TPDF dither
    pcm = np.clip(np.round((mix + d) * 32767), -32768, 32767).astype('<i2')
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main():
    print(f'film {DUR:.2f} s, {N} samples, {len(CUE)} sentences', flush=True)
    for f in (sec0_cold_open, sec1_cunning, sec2_eagle_spring, sec3_death_chained, sec4_second_trick,
              sec5_punishment, sec6_camus, sec7_outro):
        t = time.time()
        f()
        print(f'  {f.__name__:22s} {time.time() - t:5.1f} s', flush=True)
    mix, used_vo = mixdown()
    write_wav(OUT, mix)
    print(f'wrote {OUT.relative_to(FILM)}  ({len(mix) / SR:.3f} s, speech mask from '
          f'{"cues.md + vo.wav" if used_vo else "cues.md"})  in {time.time() - T_START:.1f} s')


if __name__ == '__main__':
    main()
