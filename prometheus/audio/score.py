#!/usr/bin/env python3
"""
PROMETHEUS — original score, fully synthesized with numpy/scipy (no samples, nothing downloaded).
The instrument engine (lyre, aulos, strings, choir, frame drum, felt piano, hall, spectral ducking)
is carried over from the Sisifos score; the arrangement, motifs and sound effects are new.

    python3 audio/score.py          (run from the film folder)
    -> audio/music.wav              48 kHz, stereo, 16-bit, exactly the film's length

Inputs
    audio/cues.md   film length and every narration sentence (tools/cues.py)
    timeline.js     word timings: every hit is bound to a sentence or a word, so the score follows the voice
    vo/vo.wav       optional; only *analysed* to find where speech is. Never mixed in.

Colour by layer (the picture changes vase technique with the source)
    Hesiodos, black-figure   lyre and frame drum, D Dorian: the rhapsode's epic
    Aiskhylos, red-figure    aulos (the tragic chorus' pipe), low drone, chain metal, D Phrygian
    Erhat, white-ground      felt piano and soft strings; D minor -> F, and D major for "özgürdür"

Motifs
    fire (Prometheus)   D A C D'        a fifth leap, then the minor seventh up to the octave: forethought
    chain (tyranny)     D C# C B Bb A   the chromatic lament bass
    three thrones       a heavy hit per fall; the third is withheld (D11, I03, I06) until J04,
                        where the chain motif turns over into the fire motif: "Zeus köle, Prometheus özgür"
Sound effects (hammer, chains, wings, eagle cry, wind, fire, storm, typewriter, gadfly) are synthesized
here too, so no generation credits are spent; they sit on the hits bus (ducked half as much).
"""
import json
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
rng = np.random.default_rng(1967)


# =============================================================================== cues
def read_cues(path):
    txt = path.read_text(encoding='utf-8')
    total = float(re.search(r'Toplam süre:\s*([\d.]+)', txt).group(1))
    sent = {m[1]: (float(m[2]), float(m[3]))
            for m in re.finditer(r'^- ([A-Z]\d\d[a-z]?) ([\d.]+)\s*[–-]\s*([\d.]+):', txt, re.M)}
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
    """Shared mix arrays: (rate, 'full' | 'hits' | 'lead' | 'send')."""
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
AULOS = Bus('aulos', SR, gain=0.34, send=0.36, duck='lead')   # solo çalgı: konuşmada daha derin kısma (ses kurulu tur 1)
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
        wd = 0.0 if note(m) < 50 else width      # D3 altı mono (ses kurulu tur 2)
        for v in range(voices * 2):
            c = rng.uniform(-detune, detune) + wobble(n, fs, 4.0)
            if vib:
                c = c + vib * np.sin(2 * np.pi * rng.uniform(4.6, 5.6) * tt + rng.uniform(0, 6.3))
            fr = f * 2 ** (c / 1200)
            y = blep_saw(fr, fs)
            if sine:
                y = (1 - sine) * y + sine * 1.4 * np.sin(2 * np.pi * np.cumsum(fr) / fs + rng.uniform(0, 6.3))
            if v % 2 == 0:
                L += y * (1 + wd) / 2
                R += y * (1 - wd) / 2
            else:
                L += y * (1 - wd) / 2
                R += y * (1 + wd) / 2
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
        pad([m], t0, t1, gain=gain * w, att=att, rel=rel, cutoff=cutoff, sine=0.5, voices=1, bus=DRONE, width=0.0, detune=2.0)


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



# =============================================================================== timing (timeline.js)
_TL = (FILM / 'timeline.js').read_text(encoding='utf-8')
TCUE = json.loads(re.search(r'window\.CUES = (.*?);\n', _TL, re.S).group(1))
TWORDS = json.loads(re.search(r'window\.WORDS = (.*?);\n', _TL, re.S).group(1))
ORDER = list(TCUE)
MISSING = []


def S(i): return TCUE[i]['s']
def Se(i): return TCUE[i]['e']
def nxt(i): return S(ORDER[ORDER.index(i) + 1]) if ORDER.index(i) + 1 < len(ORDER) else DUR


def _nw(w):
    w = w.replace('İ', 'i').replace('I', 'ı').lower().replace('â', 'a').replace('î', 'i').replace('û', 'u')
    return re.sub(r'[^\wçğıöşü]', '', w)


def W(i, w, n=0, end=False):
    """Time of the n-th word in sentence i starting with w (tts spelling); falls back to the sentence start."""
    k = 0
    for x in TWORDS:
        if x['id'] == i and x['w'].startswith(_nw(w)):
            if k == n:
                return x['e'] if end else x['s']
            k += 1
    MISSING.append(f'{i}@{w}#{n}')
    return S(i)


# =============================================================================== sound effects (synthesized)
def hammer(t, vel=1.0, pan=0.15):
    """Hephaistos' hammer on the chain stake: iron ring + body thud + rattling links."""
    metal(t, f0=740, vel=0.55 * vel, decay=0.55, ratios=(1, 2.41, 3.9, 5.6, 8.1), click=1.0, pan=pan)
    metal(t, f0=212, vel=0.35 * vel, decay=0.35, pan=pan)
    thud(t, vel=0.55 * vel, f0=58)
    clinks(t + 0.04, count=5, spread=0.45, vel=0.10 * vel, pan=pan)


def chain_rattle(t, vel=0.3, dur=0.8, pan=0.2):
    clinks(t, count=int(6 + 8 * dur), spread=dur, vel=0.14 * vel / 0.3, pan=pan)


def whoosh(t, vel=0.3, dur=0.45, lo=180, hi=900, pan=0.0):
    """One wing beat: band-passed air, fast swell and decay."""
    n = int(dur * SR)
    tt = np.arange(n) / SR
    env = np.sin(np.pi * np.clip(tt / dur, 0, 1)) ** 2
    y = noise(n, lo, hi, SR, 2) * env
    place(FX, y, t, gain=vel, pan=pan)


def wings(t0, t1, period=0.62, vel=0.22, pan=0.0):
    t = t0
    while t < t1:
        whoosh(t, vel=vel * rng.uniform(0.8, 1.05), pan=pan)
        t += period * rng.uniform(0.95, 1.05)


def eagle_cry(t, vel=0.25, pan=-0.2):
    """A raptor's scream: a falling, rough, fast-vibrato whistle with a breathy edge."""
    dur = 0.75
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = 2700 - 900 * (tt / dur) ** 0.7 + 90 * np.sin(2 * np.pi * 38 * tt)
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.minimum(1, tt / 0.03) * np.exp(-tt / 0.32)
    y = (np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)) * env
    y += 0.25 * noise(n, 2000, 6000, SR) * env
    place(FX, y * 0.5, t, gain=vel, pan=pan)


def wind(t0, t1, vel=0.12, lo=150, hi=1100, gust=0.5):
    """Wind on the cliff at the end of the world: slow gusts, low-rate noise bed."""
    fs = SRL
    n = int((t1 - t0) * fs)
    if n <= 0:
        return
    tt = np.arange(n) / fs
    g = 0.6 + gust * (0.5 + 0.5 * np.sin(2 * np.pi * 0.11 * tt + rng.uniform(0, 6))) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.29 * tt))
    y = np.stack([noise(n, lo, hi, fs, 2), noise(n, lo, hi, fs, 2)], 1) * (g * env_ar(n, fs, 1.5, 1.5))[:, None]
    place(DRONE, y, t0, gain=vel)


def crackle(t0, t1, vel=0.1, density=9.0):
    """Fire: sparse sharp crackles over a soft hiss (the gift, never louder than the voice)."""
    n = int((t1 - t0) * SR)
    if n <= 0:
        return
    hiss = noise(n, 900, 4000, SR, 2) * 0.12 * env_ar(n, SR, 0.4, 0.4)
    place(FX, hiss, t0, gain=vel)
    k = int((t1 - t0) * density)
    for dt in rng.uniform(0, t1 - t0, k):
        m = int(0.012 * SR)
        tm = np.arange(m) / SR
        place(FX, noise(m, 1500, 8000) * np.exp(-tm / 0.002), t0 + dt, gain=vel * rng.uniform(0.3, 1.0), pan=rng.uniform(-0.5, 0.5))


def typewriter(t0, t1, rate=9.0, vel=0.18):
    t = t0
    while t < t1:
        tick(t, vel=vel * rng.uniform(0.7, 1.0), pitch=rng.uniform(0.75, 0.9), pan=0.15)
        thud(t, vel=0.06, f0=140)
        t += rng.uniform(0.6, 1.4) / rate


def gadfly(t0, t1, vel=0.06):
    """Io's gadfly: a thin buzzing that swoops around the stereo field."""
    n = int((t1 - t0) * SR)
    if n <= 0:
        return
    tt = np.arange(n) / SR
    f = 215 + 25 * np.sin(2 * np.pi * 0.7 * tt) + 10 * np.sin(2 * np.pi * 9 * tt)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sign(np.sin(ph)) * 0.5 + 0.5 * np.sin(2 * ph)
    y = bp(y, 300, 3000, SR, 2) * env_ar(n, SR, 0.3, 0.4) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.37 * tt))
    pan = np.sin(2 * np.pi * 0.23 * tt)
    st = np.stack([y * np.cos((pan + 1) * np.pi / 4), y * np.sin((pan + 1) * np.pi / 4)], 1) * np.sqrt(2)
    place(FX, st, t0, gain=vel)


def quake(t, vel=0.8, dur=3.0):
    """Earthquake: sub rumble + debris."""
    fs = SRL
    n = int(dur * fs)
    tt = np.arange(n) / fs
    env = np.minimum(1, tt / 0.2) * np.exp(-tt / (dur * 0.5))
    r = np.stack([noise(n, 18, 90, fs), noise(n, 18, 90, fs)], 1) * env[:, None]
    place(RUMB, r, t, gain=vel)
    debris(t + 0.1, vel=0.35 * vel, dur=dur * 0.6)


def throne_hit(t, vel=1.0, pan=0.0):
    """A throne falls: the revolution hit (wood crash + deep boom)."""
    boom(t, vel=0.95 * vel, f0=72, f1=55, decay=1.6, knock=0.7, pan=pan)
    fdrum(t, 'dum', vel=0.75 * vel, f0=64, pan=pan)
    debris(t + 0.03, vel=0.3 * vel, dur=0.7)


def swell_into(t, dur=1.6, vel=0.3, kind='swell'):
    riser(t, dur, vel=vel, kind=kind)


# =============================================================================== motifs and beds
FIRE = [(0, 1.0), (7, 0.5), (10, 0.5), (12, 2.0)]                       # D A C D'
FIRE_Q = [(0, 1.0), (7, 0.5), (10, 0.5), (9, 1.5)]                      # the question: ends on the sixth, unresolved
FIRE_DONE = [(0, 1.0), (7, 0.5), (9, 0.5), (11, 0.5), (12, 2.5)]       # D A B C# D': completed in D major
CHAIN = [(0, 1.0), (-1, 1.0), (-2, 1.0), (-3, 1.0), (-4, 1.0), (-5, 2.0)]   # D C# C B Bb A


def mot(root, items, beat, vel=1.0):
    root = note(root)
    return [(root + o, d * beat, vel) for o, d in items]


def fire_motif(t, root='D5', beat=0.42, inst='aulos', vel=1.0, kind=FIRE, **kw):
    ph = mot(root, kind, beat, vel)
    if inst == 'aulos':
        aulos(t, ph, gain=kw.pop('gain', 0.9), **kw)
    elif inst == 'bowed':
        bowed(t, ph, gain=kw.pop('gain', 0.45), **kw)
    elif inst == 'lyre':
        lyre_line(t, [(m, d, v) for m, d, v in ph], vel=kw.pop('lvel', 0.45), **kw)
    elif inst == 'piano':
        tt = t
        for m, d, v in ph:
            piano(tt, m, vel=0.45 * v, **kw)
            tt += d


def chain_motif(t, root='D3', beat=0.5, vel=1.0, **kw):
    bowed(t, mot(root, CHAIN, beat, vel), gain=kw.pop('gain', 0.42), stack=kw.pop('stack', (0, -12)),
          cutoff=kw.pop('cutoff', 700), vib=kw.pop('vib', 3), **kw)


def bed(t0, t1, chords, gain=0.18, cutoff=750, att=1.6, rel=1.6, ov=0.8, **kw):
    """Lay a chord progression evenly over [t0, t1] with overlapping crossfades."""
    if t1 <= t0:
        return
    k = len(chords)
    d = (t1 - t0) / k
    for i, ch in enumerate(chords):
        a = t0 + i * d - (ov if i else 0)
        b = t0 + (i + 1) * d + (ov if i < k - 1 else 0)
        pad(M(ch), max(0.0, a), b, gain=gain, att=att, rel=rel, cutoff=cutoff, **kw)


def piano_arp(t0, t1, chords, step=0.36, vel=0.22, pattern=(0, 1, 2, 3, 2, 1)):
    k = len(chords)
    d = (t1 - t0) / k
    for i, ch in enumerate(chords):
        arp(t0 + i * d, t0 + (i + 1) * d, M(ch), list(pattern), step, inst='piano', vel=vel)


def lyre_ost(t0, t1, bars, eighth=0.3, vel=0.36, ticks=False, drum=True):
    """Repeat a plucked ostinato (list of 8-token bars) over [t0, t1]."""
    seq, t = [], t0
    while t + 8 * eighth <= t1 + 1e-6:
        seq.append((bars[len(seq) % len(bars)], ticks, vel))
        t += 8 * eighth
    if seq:
        play_bars(t0, seq, eighth)
        if drum:
            for k in range(len(seq)):
                fdrum(t0 + k * 8 * eighth, 'dum', vel=0.2, f0=82)


# Hesiodos ostinatos (D Dorian), Mekone's cunning (with ticks), Hermes' quick pizzicato
OST_H = ['D2 . A2 . C3 . A2 .', 'D2 . A2 . B2 . G2 .', 'C2 . G2 . E2 . G2 .', 'A1 . E2 . A2 . C#3 .']
OST_M = ['D2 . F2 A2 B2 . A2 .', 'G2 . E2 F2 A2 . . .', 'D2 . F2 A2 B2 . D3 C3', 'B2 A2 G2 . E2 . C#2 .']
OST_HERMES = ['D3 F3 A3 F3 D3 F3 A3 C4', 'Bb2 D3 F3 D3 Bb2 D3 F3 A3', 'C3 Eb3 G3 Eb3 C3 Eb3 G3 Bb3', 'A2 C#3 E3 C#3 A2 C#3 E3 G3']
PHRY = ['D3 F3 A3', 'Eb3 G3 Bb3', 'C3 Eb3 G3', 'D3 F3 A3']
DOR = ['D3 F3 A3 C4', 'G2 B2 D3 F3', 'C3 E3 G3', 'A2 C#3 E3']
ERHAT = ['D3 F3 A3 E4', 'Bb2 D3 F3 A3', 'F2 A2 C3 E3', 'C3 E3 G3 D4']


# =============================================================================== the score
def s00_opening():
    """0 - 46: the theft (cover image), the chaining, the eagle (kylix), the title, Erhat's claim."""
    crackle(0.0, S('A02') - 0.3, vel=0.12)
    chain_rattle(0.05, vel=0.22, dur=0.55)    # the very first sound, before the voice: a chain
    drone('D1 D2 A2', 0.2, S('A03'), gain=0.30, att=1.2, rel=1.0, cutoff=300)
    # A01: the fire motif on the aulos, answering "bile bile"
    fire_motif(W('A01', 'bile') - 0.1, 'D5', beat=0.36, gain=0.32, vib=14, drone='D4')
    fire_motif(Se('A01') + 0.05, 'A4', beat=0.24, gain=0.45, kind=FIRE_Q, vib=10)
    # A02 the hammer locks the chain; the lament bass climbs down under "asıl tutsak"
    TH = Se('A01') + 0.24                    # the hammer falls in the silence before A02 (picture: P004 at + .12)
    hammer(TH, vel=1.0)
    boom(TH, vel=0.6, f0=60, decay=1.2)
    chain_rattle(TH + 0.15, vel=0.3, dur=0.9)
    hammer(W('A02', 'mıhlatan'), vel=0.55)     # second blow on "mıhlatan" (picture: P004)
    chain_rattle(W('A02', 'mıhlatan') + 0.15, vel=0.25, dur=0.7)
    chain_motif(W('A02', 'zeusun') - 0.3, 'D3', beat=0.42, gain=0.38)
    pad(M('Eb3 G3 Bb3'), W('A02', 'asıl') - 0.4, Se('A02') + 1.2, gain=0.14, cutoff=600)
    # A03 the kylix eagle: tremolo strings, wing beats, the cry, night, and the dawn returning
    bowed(S('A03') - 0.2, [('D3', W('A03', 'gece') - S('A03') + 0.2, 0.6)], gain=0.3, stack=(0, 3, 7), trem=0.5, cutoff=900, vib=0)
    wings(W('A03', 'kartal'), W('A03', 'karaciğerini') + 0.6, vel=0.2)
    eagle_cry(W('A03', 'iner'), vel=0.22)
    boom(W('A03', 'parçalar'), vel=0.45, f0=55, decay=1.0)
    pad(M('Bb2 D3 F3'), W('A03', 'gece') - 0.3, W('A03', 'sabah') + 0.3, gain=0.17, cutoff=520)
    for i, m in enumerate(['A4', 'D5', 'F5']):
        bell(W('A03', 'yeniden') + i * 0.35, m, vel=0.07)
    swell_into(W('A03', 'kartal', 1), dur=1.3, vel=0.22)
    wings(W('A03', 'kartal', 1), Se('A03') + 0.8, vel=0.18)
    # A04 TITLE
    T = W('A04', 'prometeus')
    riser(T, 1.4, vel=0.3, kind='cym')
    boom(T, vel=1.0, f0=62, decay=1.8)
    fdrum(T, 'dum', vel=0.85, f0=72)
    strum(T + 0.01, M('D2 A2 D3 F3 A3 D4'), vel=0.6, spread=0.016, bright=0.5)
    choir(M('D3 A3 D4 F4'), T, T + 4.2, gain=0.32, att=0.7, rel=1.4)
    drone('D1 D2', T, S('A05') + 2, gain=0.26, att=0.3, rel=2.0)
    fire_motif(Se('A04') + 0.05, 'D5', beat=0.45, gain=0.85, drone='D4', vib=16)
    # A06 Erhat: the felt piano enters, 1967 rings once
    piano_arp(S('A06'), Se('A06') + 1.0, ['D3 F3 A3 E4', 'Bb2 F3 A3 D4'], step=0.4, vel=0.2)
    bell(W('A06', 'bin'), 'A5', vel=0.08)
    # A05 the two questions: suspended
    pad(M('D3 G3 A3'), S('A05') - 0.3, W('A05', 've') + 0.5, gain=0.15, cutoff=700)
    pad(M('Bb2 Eb3 F3'), W('A05', 've'), Se('A05') + 2.0, gain=0.15, cutoff=650)
    lyre_line(Se('A05') + 0.15, [('A4', 0.28), ('C5', 0.28), ('D5', 0.6), ('E5', 0.9)], vel=0.38)
    crackle(W('A05', 'avuç') - 0.2, Se('A05') + 1.4, vel=0.09)


def s01_question():
    """46 - 94: Erhat's question (white-ground, piano)."""
    t0, t1 = S('B01') - 0.6, S('C01') - 0.4
    piano_arp(t0, S('B06'), ['D3 F3 A3 E4', 'Bb2 D3 F3 A3', 'F2 A2 C3 E3', 'C3 E3 G3 D4', 'D3 F3 A3 E4', 'G2 Bb2 D3 F3'], step=0.42, vel=0.18)
    bed(t0, t1, ['D3 F3 A3', 'Bb2 D3 F3', 'F2 A2 C3', 'C3 E3 G3', 'G2 Bb2 D3', 'A2 C#3 E3'], gain=0.12, cutoff=650)
    # B02 three scrolls, two crumble: two soft dust hits, one held note
    for k, w in enumerate(['tek', 'ulaştı']):
        debris(W('B02', w), vel=0.12, dur=0.6)
    bell(W('B02', 'zincire'), 'D6', vel=0.07)
    # B04 "insanlığın dramıdır": warm major lift
    pad(M('F3 A3 C4 E4'), W('B04', 'oynanan'), Se('B04') + 1.0, gain=0.13, cutoff=900)
    # B06 the big question: swell, then NASIL? rings
    swell_into(W('B06', 'nasıl'), 1.8, vel=0.2)
    bowed(W('B06', 'nasıl'), [('A3', 2.4, 0.7), ('Bb3', 2.0, 0.8), ('A3', 3.0, 0.9)], gain=0.24, stack=(0, -12), cutoff=900)
    for i, m in enumerate(['D5', 'A5', 'E6']):
        bell(W('B06', 'yaratabildi') + 0.5 + i * 0.22, m, vel=0.08)
    # B07 rewind into myth: reverse swell into the lyre
    whoosh(W('B07', 'geriye') - 0.35, vel=0.22, dur=1.0, lo=400, hi=3000)   # the page rewinds (P024)
    riser(W('B07', 'taht'), 2.2, vel=0.24, kind='swell')
    strum(W('B07', 'taht') + 0.02, M('D3 A3 D4 F4 A4'), vel=0.4, spread=0.05)


def s02_thrones():
    """94 - 238: the gods' war for the throne (Hesiodos, black-figure lyre)."""
    lyre_ost(S('C01') - 0.3, S('C04') - 0.4, OST_H, eighth=0.31, vel=0.30, drum=False)
    bed(S('C01') - 0.3, S('C04'), DOR, gain=0.12, cutoff=700)
    throne_hit(W('C02', 'darbesi'), vel=0.45)
    # C04 genealogy: Khaos (low cluster) -> Gaia (warm) -> Uranos (high, starry) -> disgust
    drone('D1 Eb2 A2', S('C04'), W('C04', 'toprak') + 0.5, gain=0.26, att=1.0, rel=1.0, cutoff=240)
    pad(M('D3 F3 A3 C4'), W('C04', 'toprak'), W('C04', 'gaya', 1) + 0.6, gain=0.16, cutoff=800)
    pad(M('F4 A4 C5 E5'), W('C04', 'gaya', 1), W('C04', 'ama') + 0.5, gain=0.10, cutoff=2200, sine=0.4)
    ripples(W('C04', 'gaya', 1), W('C04', 'ama'), M('A5 C6 E6 G6'), rate=0.6, vel=0.06)
    pad(M('D3 Eb3 A3'), W('C04', 'ama'), Se('C04') + 0.8, gain=0.16, cutoff=500)
    for k in range(4):
        thud(W('C04', 'geri') + k * 0.32, vel=0.22, f0=52)
    # C06 the sickle; nobody dares... except Kronos
    metal(W('C06', 'tırpan'), f0=1320, vel=0.22, decay=1.4, ratios=(1, 2.1, 3.3, 4.9), click=0.2, pan=-0.2)
    pad(M('D3 F3 A3'), S('C06'), W('C06', 'en') + 0.4, gain=0.13, cutoff=650)
    bell(W('C06', 'kronos'), 'D5', vel=0.1)
    # C07 ambush: heartbeat, the swing, the first revolution
    heartbeat(S('C07'), W('C07', 'tırpanı') - 0.2, period=0.8, vel=0.24, accel=0.96)
    bowed(S('C07'), [('D3', W('C07', 'tırpanı') - S('C07'), 0.6)], gain=0.24, stack=(0, 1), trem=0.4, cutoff=800, vib=0)
    whoosh(W('C07', 'tırpanı') - 0.1, vel=0.35, dur=0.35, lo=500, hi=3000)
    boom(W('C07', 'savurdu'), vel=0.7, f0=70, decay=1.2)
    throne_hit(W('C07', 'devrim'), vel=1.0)
    # C09 the revolution eats its children: five gulps
    pad(M('D3 F3 Ab3'), S('C09'), Se('C09') + 0.5, gain=0.15, cutoff=520)
    for k in range(5):
        thud(W('C09', 'yuttu') + k * 0.42, vel=0.3 - 0.03 * k, f0=48)
    # C10 Rheia to Crete (aulos), the stone, Zeus' childhood, the vomiting, the second throne
    aulos(S('C10'), [('A4', 0.4), ('D5', 0.4), ('E5', 0.4), ('F5', 0.8), ('E5', 0.4), ('D5', 1.0)], gain=0.5, vib=10)
    thud(W('C10', 'taş'), vel=0.4, f0=60)
    choir(M('F3 A3 D4'), W('C10', 'çocuk') - 0.2, W('C10', 'büyüyünce'), gain=0.26, att=0.6, rel=0.8, vowel='o')
    for i, m in enumerate(M('A3 G3 F3 E3 D3 C3')):
        pizz(W('C10', 'kusturdu') + 0.14 * i, m, vel=0.32)
    throne_hit(W('C10', 'indirdi'), vel=0.4)
    # C12 Erhat distinguishes the two revolutions (piano)
    piano_arp(S('C12'), Se('C12') + 0.6, ERHAT, step=0.4, vel=0.18)
    bed(S('C12'), Se('C12') + 0.6, ['D3 F3 A3', 'Bb2 D3 F3', 'F2 A2 C3', 'C3 E3 G3'], gain=0.1, cutoff=600)
    bell(W('C12', 'akılla'), 'A5', vel=0.08)
    # C14 Prometheus had a role: a hint of the fire motif on lyre
    fire_motif(W('C14', 'prometeus'), 'D4', beat=0.3, inst='lyre', lvel=0.32)
    pad(M('D3 G3 A3'), W('C14', 'hangi'), Se('C14') + 0.6, gain=0.12, cutoff=700)
    # C17 Titanomachy: war drums, the gate of Tartaros, then only reason remains, Zeus enthroned
    war_drums(S('C17'), W('C17', 'tartarosa') + 0.2, beat=0.48, vel=0.6)
    bed(S('C17'), W('C17', 'tartarosa'), ['D2 A2 D3', 'C2 G2 C3', 'Bb1 F2 Bb2', 'A1 E2 A2'], gain=0.2, cutoff=600)
    boom(W('C17', 'yüz'), vel=0.6, f0=60, decay=1.0)
    boom(W('C17', 'kapatıldı'), vel=0.6, f0=58, decay=1.6)    # the bronze gate shuts (P051)
    metal(W('C17', 'kapatıldı') + 0.05, f0=150, vel=0.3, decay=1.3, pan=0.1)
    piano(W('C17', 'akıldan'), 'D4', vel=0.3)
    piano(W('C17', 'akıldan') + 0.5, 'A4', vel=0.25)
    thunder(W('C17', 'yıldırım'), vel=0.55)
    choir(M('Bb2 F3 Bb3 D4'), W('C17', 'yıldırım') + 0.2, W('C17', 'paylaştırmaya'), gain=0.3, att=0.6, rel=1.0)
    lyre_ost(W('C17', 'paylaştırmaya') - 0.2, S('C18'), OST_H[:2], eighth=0.28, vel=0.26, drum=False)
    # C18 the one obstacle: silence, then the fire motif on "Prometheus"
    pad(M('D3 Eb3 A3'), S('C18'), W('C18', 'prometeus'), gain=0.14, cutoff=500)
    fire_motif(Se('C18') + 0.05, 'D5', beat=0.46, gain=0.7, drone='D4', vib=14)   # adın arkasından (önünde 2 sn boşluk)
    boom(W('C18', 'prometeus'), vel=0.2, f0=62, decay=1.3)


def s03_rage():
    """238 - 336: Zeus' unappeasable rage; the four brothers; the third revolution is prepared."""
    drone('D1 D2', S('D01') - 0.5, Se('D01') + 1.2, gain=0.26, att=0.8, rel=1.0)
    pad(M('D3 F3 Ab3'), S('D01') - 0.5, S('D02'), gain=0.15, cutoff=500)
    # D02 the four names: one pluck each
    for w, m in [('atlas', 'D4'), ('menoitios', 'F4'), ('prometeus', 'A4'), ('epimeteus', 'C5')]:
        lyre(W('D02', w), m, vel=0.4)
    bed(S('D02'), Se('D04') + 0.5, DOR, gain=0.12, cutoff=650)
    # D03 Atlas' weight; Menoitios struck
    bowed(W('D03', 'atlas'), [('D2', 2.2, 0.8), ('C2', 1.8, 0.7)], gain=0.32, stack=(0, 7, 12), cutoff=600)
    thunder(W('D03', 'yıldırımla'), vel=0.55)
    # D04 the column and the eagle; the "gift" (wry)
    chain_rattle(W('D04', 'zincirlendi'), vel=0.25, dur=0.6)
    eagle_cry(W('D04', 'kartala'), vel=0.14)
    lyre_line(W('D04', 'armağan') + 0.1, [('E5', 0.18), ('D5', 0.18), ('B4', 0.5)], vel=0.32)
    # D05 Erhat's question and his "Hayır"
    piano_arp(S('D05'), Se('D05') + 0.4, ERHAT[:2], step=0.42, vel=0.18)
    piano(W('D05', 'hayır'), 'D3', vel=0.45)
    piano(W('D05', 'hayır'), 'A3', vel=0.35)
    # D07 monopoly on reason; the rage boils
    pad(M('D2 A2 D3'), S('D07'), W('D07', 've'), gain=0.17, cutoff=420)
    bowed(W('D07', 've'), [('D3', 1.2, 0.5), ('Eb3', 1.2, 0.7), ('E3', 1.0, 0.9), ('F3', 1.6, 1.0)], gain=0.3, stack=(0, -12, 1), cutoff=900, trem=0.3)
    quake(W('D07', 'öfke'), vel=0.3, dur=2.0)
    # D08 deceive / unsettle / ridicule: three wry plucks
    for w, ch in [('aldatır', 'D4 F4 A4'), ('tedirgin', 'C#4 E4 G4'), ('gülünç', 'D4 G4 Bb4')]:
        strum(W('D08', w), M(ch), vel=0.3, spread=0.03)
    # D09 the seer
    for i, m in enumerate(['A5', 'E6', 'A6']):
        bell(W('D09', 'kâhin') + i * 0.25, m, vel=0.07)
    pad(M('D3 G3 A3 E4'), S('D09'), Se('D09') + 0.4, gain=0.12, cutoff=900)
    # D10 "üçüncü devrimin hazırlanması": low choir
    choir(M('D2 A2 D3 F3'), S('D10'), Se('D10') + 1.5, gain=0.3, att=0.8, rel=1.2, vowel='o')
    # D11 two thrones fall; the third hit is withheld (master gain dips into silence)
    throne_hit(W('D11', 'uranos'), vel=0.6, pan=-0.3)
    throne_hit(W('D11', 'kronos'), vel=0.6, pan=0.3)
    bowed(W('D11', 'sıra'), [('A5', Se('D11') + 0.3 - W('D11', 'sıra'), 0.5)], gain=0.12, cutoff=3000, vib=0)


def s04_mekone():
    """336 - 494: the trick at Mekone, the fire, Pandora (Hesiodos)."""
    lyre_ost(S('E01') - 0.2, S('E07') - 0.3, OST_M, eighth=0.3, vel=0.33, ticks=True)
    bed(S('E01') - 0.2, S('E07'), ['D3 A3 C4 E4', 'D3 F3 A3 C4', 'G2 B2 D3 F3', 'D3 F3 A3', 'D3 Eb3 A3'], gain=0.14, cutoff=700)
    crackle(S('E01'), W('E01', 'yakardı') + 1.0, vel=0.07)
    thud(W('E03', 'öküz'), vel=0.3, f0=55)
    metal(W('E03', 'ikiye'), f0=1500, vel=0.15, decay=0.3, click=0.6)
    lyre_line(W('E04', 'çıplak') + 0.1, [('B4', 0.2), ('A4', 0.2), ('G4', 0.2), ('E4', 0.6)], vel=0.3)
    strum(W('E05', 'beyaz'), M('D3 G#3 D4'), vel=0.32, spread=0.03)
    # E07 - E08 Erhat (piano)
    piano_arp(S('E07'), Se('E08') + 0.5, ERHAT, step=0.4, vel=0.18)
    bed(S('E07'), Se('E08') + 0.5, ['D3 F3 A3', 'Bb2 D3 F3', 'F2 A2 C3', 'C3 E3 G3'], gain=0.1, cutoff=650)
    # E09 Zeus withholds fire: the music drains to a drone, the hearths go out (crackles stop)
    lyre_line(S('E09'), [('A4', 0.25), ('C5', 0.25), ('B4', 0.6)], vel=0.28)
    drone('D1 D2', W('E09', 'gururu'), S('E10') + 0.5, gain=0.26, att=0.6, rel=0.6)
    for k in range(4):
        thud(W('E09', 'esirger') + k * 0.4, vel=0.12, f0=90)
    # E10 the fennel stalk: the fire motif whole (aulos + lyre), then Zeus bitten to the heart
    crackle(W('E10', 'rezene'), W('E10', 'hesiodosun'), vel=0.11)
    fire_motif(W('E10', 'götürür', end=True) + 0.05, 'D5', beat=0.42, gain=0.4, drone='D4', vib=16)
    strum(W('E10', 'götürür', end=True) + 0.05, M('D3 A3 D4 F4 A4'), vel=0.45, spread=0.03)
    bed(W('E10', 'rezene'), W('E10', 'hesiodosun'), ['D3 F3 A3 C4', 'G2 B2 D3 F3'], gain=0.15, cutoff=900)
    pad(M('D2 Eb3 A3'), W('E10', 'hesiodosun'), Se('E10') + 1.0, gain=0.17, cutoff=450)
    boom(W('E10', 'ısırır'), vel=0.55, f0=58, decay=1.2)
    # E12 Pandora (delicate lyre and choir), Epimetheus thinks too late (wry)
    ripples(S('E12'), W('E12', 'prometeus'), M('D5 F5 A5 C6'), rate=0.55, vel=0.07)
    choir(M('F4 A4 C5'), W('E12', 'tanrılar'), W('E12', 'prometeus'), gain=0.2, att=0.8, rel=0.8, vowel='u')
    bell(W('E12', 'pandoradır'), 'F5', vel=0.09)
    pad(M('D3 F3 A3'), W('E12', 'prometeus'), Se('E12') + 0.6, gain=0.12, cutoff=700)
    lyre_line(W('E12', 'sonradan'), [('C5', 0.22), ('B4', 0.22), ('Bb4', 0.22), ('A4', 0.6)], vel=0.3)
    # E14 the jar opens: swarm cluster, then a single bell: Hope
    swell_into(W('E14', 'kapağını'), 1.2, vel=0.25)
    bowed(W('E14', 'kapağını'), [('D3', 3.0, 0.8)], gain=0.28, stack=(0, 1, 6, 13), trem=0.6, cutoff=1400, vib=0)
    for k in range(10):
        whoosh(W('E14', 'hastalıklar') + k * 0.18, vel=0.07, dur=0.25, lo=1200, hi=4000, pan=rng.uniform(-0.8, 0.8))
    bell(W('E14', 'umut'), 'A5', vel=0.12, decay=3.4)
    # E11 two deceits: only brute force remains
    piano(W('E11', 'iki'), 'D3', vel=0.3)
    boom(W('E11', 'kaba'), vel=0.7, f0=60, decay=1.3)
    # E15 Hesiodos praises Zeus (lyre) / Erhat reads between the lines (piano)
    strum(S('E15'), M('D3 F#3 A3 D4'), vel=0.32, spread=0.05)
    piano_arp(W('E15', 'ama'), Se('E15') + 0.5, ['D3 F3 A3 E4', 'G2 Bb2 D3 F3', 'Bb2 D3 F3 A3', 'A2 C#3 E3 G3'], step=0.38, vel=0.18)
    # E16 the third and last revolution has happened: human consciousness (rising choir, D major)
    choir(M('D3 A3 D4 F#4'), W('E16', 'üçüncü'), Se('E16') + 1.5, gain=0.3, att=1.2, rel=1.4)
    pad(M('D3 F#3 A3 E4'), W('E16', 'insan'), Se('E16') + 1.6, gain=0.14, cutoff=1100)
    # E16b towards the other poet: the aulos turns Phrygian
    fire_motif(S('E16b') + 0.2, 'A4', beat=0.3, inst='lyre', kind=FIRE_Q, lvel=0.3)
    aulos(W('E16b', 'zincirin'), [('D5', 0.8), ('Eb5', 0.8), ('D5', 1.6)], gain=0.5, vib=10, drone='D4')
    drone('D1 D2 A2', W('E16b', 'zincirin'), S('F01') + 1.0, gain=0.24, att=1.0, rel=1.0)


def s05_trial():
    """494 - 676: the trial (Aiskhylos: aulos, drone, chain metal)."""
    drone('D1 D2 A2', S('F01') - 0.4, S('F03'), gain=0.24, att=1.2, rel=1.2)
    aulos(Se('F01') + 0.05, [('D5', 0.3), ('Eb5', 0.2), ('F5', 0.4), ('D5', 0.3)], gain=0.45, vib=10, drone='D4')
    bed(S('F02'), Se('F02') + 0.4, PHRY, gain=0.12, cutoff=650)
    # F03 Kafka: a single low piano note like a ticking clock, an eerie cluster
    for k in range(int((Se('F03') - W('F03', 'oyunu')) / 0.9) + 1):
        piano(W('F03', 'oyunu') + k * 0.9, 'D2', vel=0.16, dur=1.0)
    pad(M('D3 Eb3 Ab3'), W('F03', 'erhat'), Se('F03') + 1.2, gain=0.12, cutoff=600)
    # F05 the trial opens: gavel knocks
    for k in range(3):
        fdrum(S('F05') + k * 0.28, 'tek', vel=0.4, f0=170)
    pad(M('D3 F3 A3'), S('F05'), Se('F05b') + 0.6, gain=0.13, cutoff=600)
    bowed(S('F05b'), [('Bb5', Se('F05b') - S('F05b') + 1.0, 0.5)], gain=0.1, stack=(0, 1), cutoff=3000, vib=0)
    # F06 Scythia: wind; Kratos and Bia march the prisoner in
    wind(S('F06') - 0.5, Se('F14') + 2.0, vel=0.10)
    for k in range(int((W('F06', 'kratos') - W('F06', 'zeusun')) / 0.6)):
        fdrum(W('F06', 'zeusun') + k * 0.6, 'dum', vel=0.32, f0=60)
        chain_rattle(W('F06', 'zeusun') + k * 0.6 + 0.05, vel=0.12, dur=0.3)
    drone('D1 A1', S('F06'), Se('F08') + 0.5, gain=0.22, att=0.8, rel=0.8, cutoff=220)
    # F08 the purpose of the punishment; F07 Hephaistos unwilling, then the hammer
    pad(M('D3 Eb3 G3'), S('F08'), Se('F08') + 0.5, gain=0.13, cutoff=550)
    bowed(S('F07'), [('A3', 2.0, 0.6), ('Bb3', 1.4, 0.7), ('A3', 2.4, 0.6)], gain=0.24, stack=(0, -12), cutoff=800)
    hammer(W('F07', 'kendi', 1) + 1.1, vel=0.6)   # picture: P117 hit = F07@kendi#1 + 1.1
    # F09 "Ah, nefret ettiğim zanaatım!" lament; Kratos' icy line over the chain motif
    aulos(W('F09', 'ah'), [('F5', 0.5), ('E5', 0.5), ('Eb5', 0.6), ('D5', 1.2)], gain=0.45, vib=14)
    chain_motif(W('F09', 'güçün'), 'D3', beat=0.55, gain=0.34)
    # F10 freedom and slavery (Erhat): piano, two notes in conflict
    piano_arp(S('F10'), Se('F10a') + 0.5, ['D3 F3 A3 E4', 'Bb2 D3 F3 A3', 'G2 Bb2 D3 F3', 'A2 C#3 E3 G3'], step=0.42, vel=0.17)
    bed(S('F10'), Se('F10a') + 0.5, ['D3 F3 A3', 'Bb2 D3 F3', 'G2 Bb2 D3', 'A2 C#3 E3'], gain=0.1, cutoff=600)
    # F10b he said not a word: the hammer twice, then silence
    hammer(W('F10b', 'indi'), vel=0.6)        # picture: P132–P133 hits on both "indi"
    hammer(W('F10b', 'indi', 1), vel=0.6)
    pad(M('D2 A2'), W('F10b', 'zincire'), Se('F10b') + 1.0, gain=0.15, cutoff=300)
    # F13 alone, he speaks to the sky: choir, the "countless laughter" of the waves, Earth
    choir(M('D3 A3 D4 F4'), W('F13', 'ey'), W('F13', 'bakın'), gain=0.26, att=1.6, rel=1.0, vowel='a')
    whoosh(W('F13', 'hızlı'), vel=0.2, dur=1.2, lo=300, hi=2500)
    ripples(W('F13', 'ırmakların'), W('F13', 've'), M('D6 E6 F6 A6 C7'), rate=0.42, vel=0.07)
    ripples(W('F13', 'deniz'), W('F13', 've'), M('A5 C6 D6 F6'), rate=0.18, vel=0.06)
    pad(M('D2 A2 D3'), W('F13', 'sen'), W('F13', 'bakın'), gain=0.18, cutoff=400)
    bowed(W('F13', 'bakın'), [('D4', 1.0, 0.8), ('Eb4', 1.2, 0.9), ('D4', 2.0, 0.7)], gain=0.3, stack=(0, -12), cutoff=1000)
    # F14 he breaks off ("Ama ne diyorum?"): almost silence; necessity; neither silent nor speaking
    pad(M('D2 A2'), W('F14', 'olacak'), W('F14', 'yine'), gain=0.12, cutoff=300)
    bowed(W('F14', 'zorunluluğun'), [('A2', 3.0, 0.6)], gain=0.2, stack=(0, 12), cutoff=600)
    aulos(W('F14', 'yine'), [('D5', 0.8), ('Eb5', 1.0), ('D5', 0.6), ('C5', 0.6), ('D5', 1.0), (('D5', 'Eb5'), 0.6), ('Eb5', 1.0)], gain=0.4, vib=12)


def s06_defence():
    """676 - 835: the defence ("bile bile yaptım")."""
    for k in range(2):
        fdrum(S('G01') + k * 0.3, 'tek', vel=0.35, f0=170)
    piano_arp(S('G02'), Se('G02') + 0.4, ['D3 F3 A3 E4', 'F2 A2 C3 E3', 'Bb2 D3 F3 A3'], step=0.42, vel=0.17)
    # G03 the Oceanids rise from the sea: ripples and a female choir
    ripples(S('G03'), Se('G03b'), M('D5 F5 A5 C6 D6'), rate=0.5, vel=0.06)
    choir(M('F4 A4 D5'), S('G03'), W('G03', 'prometeus'), gain=0.18, att=1.2, rel=1.0, vowel='u')
    bed(S('G03'), Se('G03b') + 0.6, ['D3 F3 A3', 'Bb2 D3 F3', 'C3 E3 G3', 'A2 C#3 E3'], gain=0.12, cutoff=750)
    # G03b Themis: "not force but cunning" -> a lyre wink
    lyre_line(W('G03b', 'kurnazlığın'), [('A4', 0.2), ('D5', 0.2), ('E5', 0.2), ('F5', 0.6)], vel=0.32)
    # G05 the war remembered (soft drums), Kronos buried by his counsel
    war_drums(S('G05'), W('G05', 'erhatın'), beat=0.5, vel=0.32)
    boom(W('G05', 'tartarosa'), vel=0.45, f0=60, decay=1.0)
    # G06 tyranny's disease: the chain motif
    chain_motif(W('G06', 'zorbalığın') - 0.2, 'D3', beat=0.5, gain=0.3)
    # G07 Zeus would wipe humanity out; Prometheus alone opposes
    pad(M('D3 F3 Ab3'), S('G07'), W('G07', 'buna'), gain=0.14, cutoff=500)
    fire_motif(W('G07', 'buna'), 'D4', beat=0.34, inst='lyre', lvel=0.34)
    # G07b "Ölümlülere acıdım": the solo aulos lament
    aulos(W('G07b', 'ölümlülere'), [('A4', 0.6), ('Bb4', 0.6), ('A4', 0.8), ('G4', 0.6), ('F4', 0.6), ('E4', 0.8), ('D4', 1.4)], gain=0.25, vib=12, drone='D4')
    # G08 blind hopes (pale bells), then the fire (warm)
    for k in range(5):
        bell(W('G08', 'kör') + k * 0.4, ['D6', 'F6', 'A6', 'E6', 'C6'][k], vel=0.04)
    fire_motif(Se('G08') + 0.05, 'D5', beat=0.24, gain=0.55, vib=12, drone='D4')
    crackle(W('G08', 'ateşi'), Se('G08') + 1.2, vel=0.08)
    # G09 what does giving fire mean? (piano)
    piano_arp(S('G09'), Se('G09') + 0.4, ERHAT, step=0.4, vel=0.17)
    # G10b the history of civilisation: an accelerating lyre ostinato, a hit on each gift
    lyre_ost(S('G10b'), W('G10b', 'tek'), OST_H, eighth=0.24, vel=0.3, drum=False)
    for w, m in [('yıldızları', 'A5'), ('sayıları', 'C6'), ('harfleri', 'D6'), ('hayvanları', 'E5'), ('gemiyi', 'F5'), ('ilacı', 'G5'), ('madenleri', 'A5')]:
        bell(W('G10b', w), m, vel=0.06)
        fdrum(W('G10b', w), 'tek', vel=0.22, f0=200)
    metal(W('G10b', 'madenleri') + 0.05, f0=900, vel=0.15, decay=0.4)
    strum(W('G10b', 'tek'), M('D3 A3 D4 F#4 A4 D5'), vel=0.5, spread=0.02)
    choir(M('D3 A3 D4 F#4'), W('G10b', 'tek'), Se('G10b') + 1.4, gain=0.28, att=0.4, rel=1.2)
    # G11 "isteyerek, isteyerek": two drum strokes; the typed testimony
    fdrum(W('G11', 'isteyerek'), 'dum', vel=0.6, f0=62)
    fdrum(W('G11', 'isteyerek', 1), 'dum', vel=0.7, f0=60)
    typewriter(W('G11', 'ne'), Se('G11') + 0.2, vel=0.14)
    # G13 pride and endurance; G12b "eriyip gideceğimi... düşünmemiştim": thin, falling
    bowed(S('G13'), [('D3', 2.0, 0.7), ('A3', 2.0, 0.8)], gain=0.26, stack=(0, -12, 7), cutoff=700)
    bowed(W('G12b', 'böyle'), [('A5', 1.4, 0.5), ('G5', 1.4, 0.45), ('F5', 1.4, 0.4), ('E5', 2.4, 0.35)], gain=0.12, cutoff=3000, vib=4)
    pad(M('D2 A2'), W('G12b', 'böyle'), Se('G12b') + 0.8, gain=0.12, cutoff=300)
    # G13b knowing is not living; yet he does not step back: the fire motif, low and firm
    fire_motif(W('G13b', 'yine'), 'D3', beat=0.5, inst='bowed', gain=0.36, stack=(0, 12))


def s07_witnesses():
    """835 - 958: witnesses and the "cow's crossing"."""
    lyre_line(S('H01'), [('D5', 0.3), ('E5', 0.3), ('F5', 0.3), ('A5', 0.9)], vel=0.3)
    pad(M('D3 G3 A3'), S('H01'), Se('H01') + 0.6, gain=0.12, cutoff=800)
    piano_arp(S('H02'), Se('H02') + 0.3, ['D3 F3 A3 E4', 'G2 Bb2 D3 F3', 'Bb2 D3 F3 A3', 'A2 C#3 E3 G3'], step=0.4, vel=0.17)
    piano(W('H02', 'tek'), 'D3', vel=0.4)
    # H04 Okeanos on his winged beast: dignified-comic lyre
    wings(S('H04'), S('H04') + 2.0, period=0.8, vel=0.12)
    lyre_ost(S('H04'), Se('H04'), ['D3 . F3 A3 . F3 . .', 'C3 . E3 G3 . E3 . .'], eighth=0.26, vel=0.26, drum=False)
    bed(S('H04'), Se('H04') + 0.4, ['D3 F3 A3', 'C3 E3 G3', 'Bb2 D3 F3', 'A2 C#3 E3'], gain=0.1, cutoff=700)
    wings(W('H04', 'kendi', 1), Se('H04') + 1.2, period=0.8, vel=0.1)
    # H05 "agan eleutherostomeis", consciousness grants freedom
    piano_arp(S('H05'), Se('H05') + 0.3, ERHAT, step=0.42, vel=0.16)
    # H05b he allowed himself no hope: a single low note, nearly nothing
    piano(W('H05b', 'kendisi'), 'D2', vel=0.3, dur=4.0)
    pad(M('D2 A2'), W('H05b', 'kendisi'), Se('H05b') + 1.2, gain=0.1, cutoff=280)
    # H06 Io and the gadfly: aulos chase
    gadfly(S('H06'), Se('H07') - 2.0, vel=0.05)
    aulos(W('H06', 'adı'), [('A4', 0.2), ('C5', 0.2), ('D5', 0.2), ('E5', 0.2), ('F5', 0.4), ('E5', 0.2), ('D5', 0.2), ('C5', 0.4), ('A4', 0.6)], gain=0.4, vib=8)
    bed(S('H06'), Se('H06') + 0.4, ['D3 F3 A3', 'Eb3 G3 Bb3'], gain=0.12, cutoff=700)
    # H07 the journey and the Bosporus: travelling lyre, warmth for Istanbul
    lyre_ost(S('H07'), W('H07', 'ama'), ['D3 A3 D4 A3 F3 A3 D4 A3', 'C3 G3 C4 G3 E3 G3 C4 G3'], eighth=0.25, vel=0.22, drum=False)
    bell(W('H07', 'bosporos'), 'D6', vel=0.08)
    pad(M('F3 A3 C4 E4'), W('H07', 'ama'), Se('H07') + 1.2, gain=0.14, cutoff=1100)
    strum(W('H07', 'istanbul'), M('F3 C4 F4 A4'), vel=0.32, spread=0.04)
    # H09 "Ben ölemem bile": the chain motif
    pad(M('D3 F3 A3'), S('H09'), W('H09', 'prometeusun'), gain=0.12, cutoff=600)
    chain_motif(W('H09', 'ölemem'), 'D3', beat=0.48, gain=0.3)
    # H10 an archer will be born: rising fourths, a hint of hope
    bowed(W('H10', 'okçu') - 0.6, [('D3', 0.8, 0.6), ('G3', 0.8, 0.7), ('C4', 0.8, 0.8), ('F4', 1.8, 0.9)], gain=0.24, stack=(0, -12), cutoff=1100)


def s08_secret():
    """958 - 1058: the secret that shakes the throne; Hermes."""
    bowed(S('I01') - 0.3, [('D4', 4.0, 0.5)], gain=0.16, stack=(0, 1), trem=0.3, cutoff=1200, vib=0)
    drone('D1 D2', S('I01'), Se('I04') + 0.5, gain=0.2, att=1.0, rel=1.0)
    pad(M('A4 E5'), S('I02'), W('I02', 've'), gain=0.08, cutoff=3000, sine=0.5)
    bowed(W('I02', 'babasından'), [('D2', 1.2, 0.6), ('E2', 1.2, 0.7), ('F2', 1.2, 0.8), ('G2', 1.6, 0.9)], gain=0.28, stack=(0, 12), cutoff=700)
    # I03 the two fallen thrones echo; the third withheld again
    throne_hit(W('I03', 'uranosun'), vel=0.5, pan=-0.3)
    throne_hit(W('I03', 'kronosun'), vel=0.5, pan=0.3)
    choir(M('D2 A2 D3'), W('I03', 'erhat'), Se('I03') + 0.6, gain=0.22, att=0.8, rel=1.0, vowel='o')
    bowed(W('I03', 'ayshilosun'), [('Ab4', 3.0, 0.4)], gain=0.1, stack=(0, 1), trem=0.5, cutoff=2400, vib=0)
    piano(S('I04'), 'D4', vel=0.25)
    # I05 Hermes flies in: quick, sly pizzicato
    wings(S('I05') - 0.4, S('I05') + 1.0, period=0.35, vel=0.12)
    lyre_ost(S('I05'), Se('I07'), OST_HERMES, eighth=0.16, vel=0.22, drum=False)
    bed(S('I05'), Se('I07') + 0.5, ['D3 F3 A3', 'Bb2 D3 F3', 'C3 Eb3 G3', 'A2 C#3 E3'], gain=0.1, cutoff=700)
    stinger = W('I05', 'sırrı')
    fdrum(stinger, 'tek', vel=0.4, f0=210)
    # I06 the mocking: two tyrants fell (two booms), the third as a far echo
    aulos(S('I06'), [('D5', 0.3), ('F5', 0.3), ('E5', 0.3), ('D5', 0.6)], gain=0.4, vib=8)
    boom(W('I06', 'iki'), vel=0.4, f0=60, decay=1.0, pan=-0.3)
    boom(W('I06', 'iki') + 0.6, vel=0.4, f0=60, decay=1.0, pan=0.3)
    boom(W('I06', 'üçüncüsünün'), vel=0.18, f0=60, decay=2.0)
    # I07 "senin uşaklığına değişmem"
    strum(W('I07', 'bu'), M('D3 A3 D4'), vel=0.35, spread=0.02)
    # I08 "Eyvah!" (the music cuts), Hermes pounces, "Yaşlanan zaman" (a slow bell)
    boom(W('I08', 'eyvah'), vel=0.35, f0=70, decay=0.6)
    eagle_cry(W('I08', 'eyvah') + 0.1, vel=0.08)
    lyre_line(W('I08', 'hermes'), [('F5', 0.15), ('E5', 0.15), ('D5', 0.4)], vel=0.28)
    bell(W('I08', 'yaşlanan'), 'D5', vel=0.12, decay=3.2)
    pad(M('D3 A3 E4'), W('I08', 'yaşlanan'), Se('I08') + 1.0, gain=0.12, cutoff=900)
    # I07b his terms: fire motif against the chain motif
    chain_motif(S('I07b'), 'D3', beat=0.5, gain=0.26)
    fire_motif(W('I07b', 'ne'), 'D5', beat=0.42, gain=0.6, vib=12, drone='D4')


def s09_other_end():
    """1058 - 1127: the other end of the chain. Freeze, then the climax (J04)."""
    drone('D1 D2', S('J01') - 0.5, S('J04') + 0.5, gain=0.24, att=0.4, rel=0.6)
    bowed(S('J01'), [('A4', Se('J01') - S('J01') + 1.0, 0.4)], gain=0.1, cutoff=2500, vib=0)
    chain_motif(W('J02', 'zeustan'), 'D3', beat=0.42, gain=0.28)
    pad(M('D3 G3 A3'), W('J02', 'erhat'), Se('J02') + 0.8, gain=0.13, cutoff=800)
    # J04 the camera climbs the chain to Zeus' wrist: rising strings; "köle" on the chain motif,
    # "özgürdür": the chain turns over into the fire motif, D major, full
    t0 = S('J04') - 0.5
    riser(W('J04', 'köle'), W('J04', 'köle') - t0, vel=0.3)
    bowed(t0, [('D3', 0.8, 0.6), ('E3', 0.8, 0.7), ('F3', 0.8, 0.8), (('F3', 'A3'), W('J04', 'köle') - t0 - 2.4, 0.9)], gain=0.32, stack=(0, -12, 12), cutoff=1000)
    boom(W('J04', 'köle'), vel=0.7, f0=60, decay=1.5)
    chain_motif(W('J04', 'köle'), 'D3', beat=0.22, gain=0.3, legato=False)
    T = W('J04', 'prometeus')
    boom(T, vel=0.6, f0=64, decay=2.0)
    fdrum(T, 'dum', vel=0.8, f0=70)
    strum(T + 0.01, M('D2 A2 D3 F#3 A3 D4'), vel=0.6, spread=0.016)
    choir(M('D3 A3 D4 F#4 A4'), W('J04', 'özgürdür', end=True), Se('J05') + 0.5, gain=0.4, att=0.3, rel=1.8)
    pad(M('D3 F#3 A3 E4'), T, Se('J05') + 0.5, gain=0.16, cutoff=1300)
    fire_motif(W('J04', 'özgürdür', end=True) + 0.05, 'D5', beat=0.27, gain=0.9, kind=FIRE_DONE, vib=16, drone='D4')
    boom(W('J04', 'özgürdür', end=True) + 0.05, vel=0.8, f0=64, decay=2.0)
    # J06 roles reversed: an inverted arpeggio; J10 one man's great work
    piano_arp(S('J06'), Se('J06') + 0.5, ['D3 F#3 A3 E4', 'B2 D3 F#3 A3'], step=0.4, vel=0.18, pattern=(3, 2, 1, 0, 1, 2))
    piano_arp(S('J10'), Se('J10') + 1.2, ['G2 B2 D3 F#3', 'D3 F#3 A3 E4'], step=0.44, vel=0.16)
    pad(M('D3 F#3 A3'), S('J10'), Se('J10') + 1.4, gain=0.12, cutoff=900)


def s10_storm():
    """1127 - 1226: the eagle, the storm and the last word."""
    drone('D1 D2 A2', S('I08a') - 0.5, S('I10'), gain=0.24, att=0.8, rel=1.0)
    pad(M('D3 Eb3 A3'), S('I08a'), Se('I08a') + 0.8, gain=0.15, cutoff=500)
    # I08b Hermes' last threat: thunder, the long dark, the winged hound, the feast
    thunder(W('I08b', 'yıldırımla'), vel=0.6)
    pad(M('D2 Ab2 D3'), W('I08b', 'uzun'), W('I08b', 'zeusun'), gain=0.15, cutoff=350)
    wings(W('I08b', 'kanatlı'), W('I08b', 'çağrılmamış'), period=0.7, vel=0.18)
    eagle_cry(W('I08b', 'kartal'), vel=0.18)
    bowed(W('I08b', 'çağrılmamış'), [('D3', 1.5, 0.6), ('Eb3', 1.5, 0.7), ('D3', 2.0, 0.6)], gain=0.24, stack=(0, 6), cutoff=800, trem=0.4)
    # I08c the opening's eagle: the price of saying no; "beni öldüremez"
    wings(S('I08c'), W('I08c', 'prometeus'), period=0.62, vel=0.16)
    fire_motif(W('I08c', 'bedeli'), 'D3', beat=0.4, inst='bowed', gain=0.3, stack=(0, 12))
    strum(W('I08c', 'öldüremez'), M('D3 A3 D4'), vel=0.4, spread=0.02)
    # I09 the Oceanids stay: female choir
    choir(M('D4 F4 A4'), W('I09', 'ama'), Se('I09') + 0.8, gain=0.26, att=0.6, rel=1.0, vowel='a')
    # I10 brute force: the storm (drums, thunder, rumble), sky and sea mixed
    t0 = S('I10')
    war_drums(t0, Se('I10') + 0.3, beat=0.42, vel=0.55)
    bed(t0, Se('I10') + 0.5, ['D2 A2 D3', 'Eb2 Bb2 Eb3', 'C2 G2 C3', 'D2 A2 D3'], gain=0.22, cutoff=700)
    quake(W('I10', 'yer'), vel=0.7, dur=3.0)
    thunder(W('I10', 'gök'), vel=0.6)
    thunder(W('I10', 'şimşekler'), vel=0.8)
    wind(W('I10', 'rüzgârlar'), Se('I10') + 1.0, vel=0.22, lo=200, hi=2400, gust=0.9)
    boom(W('I10', 'gök', 1), vel=0.6, f0=55, decay=2.0)
    riser(W('I10', 'gök', 1), 1.8, vel=0.35)
    # I11 in the chaos a stillness: the solo aulos to his mother
    aulos(W('I11', 'görüyor') - 0.2, [('A4', 0.6), ('Bb4', 0.8), ('A4', 0.6), ('G4', 0.6), ('A4', 1.4)], gain=0.4, vib=12, drone='D4')
    pad(M('D2 A2'), S('I11'), Se('I11') + 0.6, gain=0.12, cutoff=300)
    # I12 the last word is his: silence, the fire motif alone, then the strings in D major
    fire_motif(W('I12', 'onundur', end=True) + 0.05, 'D5', beat=0.44, gain=0.35, vib=14)
    choir(M('D3 A3 D4 F#4'), W('I12', 'kıyamet'), Se('I12') + 2.4, gain=0.34, att=1.2, rel=1.8)
    bowed(W('I12', 'kıyamet'), [('A3', 1.6, 0.7), ('B3', 1.0, 0.8), ('C#4', 1.0, 0.9), ('D4', 3.4, 1.0)], gain=0.32, stack=(0, -12), cutoff=1300)
    boom(W('I12', 'özgür'), vel=0.6, f0=62, decay=1.8)


def s11_legacy():
    """1226 - 1295: from Herakles to Oppenheimer; the torch relay."""
    pad(M('D3 G3 A3'), S('L01') - 0.4, Se('L01') + 0.6, gain=0.12, cutoff=800)
    # L02 Herakles shoots the eagle
    lyre_ost(S('L02'), W('L02', 'tabii'), ['D3 A3 D4 A3 D3 A3 D4 F#4', 'G3 D4 G4 D4 A3 E4 A4 E4'], eighth=0.24, vel=0.28, drum=True)
    whoosh(W('L02', 'kartalı') - 0.2, vel=0.3, dur=0.25, lo=1500, hi=6000)
    boom(W('L02', 'öldürdü'), vel=0.6, f0=62, decay=1.0)
    eagle_cry(W('L02', 'öldürdü') - 0.1, vel=0.14)
    lyre_line(W('L02', 'tabii'), [('E5', 0.2), ('D5', 0.2), ('B4', 0.6)], vel=0.3)
    debris(W('L02', 'kayıp'), vel=0.12, dur=0.5)
    bell(W('L02', 'kayıp') + 0.4, 'D6', vel=0.06)
    # L03 the chained image endures
    bowed(S('L03'), [('D3', 2.0, 0.6), ('A3', 2.4, 0.7)], gain=0.22, stack=(0, -12), cutoff=800)
    # L04 Goethe (romantic piano)
    piano_arp(S('L04'), Se('L04') + 0.3, ['D3 F3 A3 D4', 'Bb2 D3 F3 Bb3', 'G2 Bb2 D3 G3', 'A2 C#3 E3 A3'], step=0.3, vel=0.2, pattern=(0, 1, 2, 3, 2, 1, 2, 3))
    # L05 Frankenstein (lightning crackle), Oppenheimer (rumble, a blinding white noise, cut)
    thunder(W('L05', 'frankenştayn'), vel=0.35)
    pad(M('D3 Eb3 Ab3'), W('L05', 'frankenştayn'), W('L05', 'atom'), gain=0.12, cutoff=700)
    riser(W('L05', 'openhaymırın') + 1.2, 2.0, vel=0.3, kind='swell')
    boom(W('L05', 'openhaymırın') + 1.2, vel=0.45, f0=50, decay=1.5)
    # L06 the torch relay: running drums, the fire motif passed hand to hand
    t0, t1 = S('L06'), Se('L06') + 1.0
    for k in range(int((t1 - t0) / 0.3)):
        fdrum(t0 + k * 0.3, 'dum' if k % 2 == 0 else 'tek', vel=(0.24 if k % 2 == 0 else 0.12) * (0.5 if t0 + k * 0.3 < Se('L06') else 1.0), f0=80)
    fire_motif(t0, 'D4', beat=0.26, inst='lyre', lvel=0.3)
    fire_motif(Se('L06') + 0.05, 'D5', beat=0.26, gain=0.45, vib=10)
    fire_motif(t0 + 3.2, 'D4', beat=0.26, inst='piano')
    pad(M('D3 A3 D4 F4'), t0, t1, gain=0.12, cutoff=1000)


def s12_rebel():
    """1295 - 1397: the creature who rebels; the final name."""
    # K08a the question returns (same bells as B06), Erhat's answer
    for i, m in enumerate(['D5', 'A5', 'E6']):
        bell(S('K08a') + 0.2 + i * 0.22, m, vel=0.08)
    piano_arp(S('K08a'), Se('K08a') + 0.4, ['D3 F3 A3 E4', 'Bb2 D3 F3 A3', 'F2 A2 C3 E3', 'C3 E3 G3 D4', 'G2 Bb2 D3 F3', 'A2 C#3 E3 G3'], step=0.42, vel=0.17)
    bed(S('K08a'), Se('K08a') + 0.4, ['D3 F3 A3', 'Bb2 D3 F3', 'F2 A2 C3', 'C3 E3 G3'], gain=0.1, cutoff=650)
    # K08c reason above force; thought cannot be bridled: a rising line
    bowed(W('K08c', 'düşünceye'), [('D4', 0.8, 0.6), ('E4', 0.8, 0.7), ('F4', 0.8, 0.8), ('A4', 2.0, 0.9)], gain=0.2, stack=(0, -12), cutoff=1200)
    pad(M('D3 F3 A3 C4'), W('K08c', 'belki'), Se('K08c') + 0.8, gain=0.12, cutoff=800)
    # K01 - K02 what is man? the rebellious creature (choir swell)
    piano_arp(S('K01'), W('K02', 'insan'), ['D3 F3 A3 E4', 'G2 Bb2 D3 F3'], step=0.44, vel=0.16)
    choir(M('D3 A3 D4 F4'), W('K02', 'başkaldıran') - 0.4, Se('K02') + 0.6, gain=0.28, att=1.0, rel=1.2)
    bed(W('K02', 'başkaldıran'), Se('K02') + 0.6, ['D3 F3 A3', 'F3 A3 C4', 'G2 B2 D3', 'A2 C#3 E3'], gain=0.13, cutoff=900)
    # K04 they shed tradition; "Umuda karşı da ayaklandık" (firm strings)
    piano_arp(S('K04'), W('K04', 'erhat', 1), ['D3 F3 A3 E4', 'C3 E3 G3 D4'], step=0.4, vel=0.16)
    bowed(W('K04', 'umuda'), [('D3', 1.2, 0.8), ('F3', 1.2, 0.85), ('A3', 1.2, 0.9), ('D4', 2.4, 1.0)], gain=0.3, stack=(0, -12), cutoff=1100)
    # K06 the build to the name: the fire motif completed in D major, everything
    bed(S('K06'), W('K06', 've'), ['D3 F3 A3', 'Bb2 D3 F3', 'G2 B2 D3', 'A2 C#3 E3'], gain=0.15, cutoff=900)
    arp(S('K06'), W('K06', 'prometeus'), M('D4 F4 A4 D5'), [0, 1, 2, 3, 2, 1], 0.24, vel=0.18)
    riser(W('K06', 'prometeus'), 2.4, vel=0.35, kind='cym')
    T = W('K06', 'prometeus')
    boom(T, vel=0.7, f0=62, decay=2.0)
    fdrum(T, 'dum', vel=0.9, f0=70)
    strum(T + 0.01, M('D2 A2 D3 F#3 A3 D4 F#4'), vel=0.62, spread=0.016, bright=0.55)
    choir(M('D3 A3 D4 F#4 A4'), T, T + 6.0, gain=0.46, att=0.4, rel=2.2)
    pad(M('D2 A2 D3 F#3 A3 E4'), T, T + 6.4, gain=0.18, att=0.4, rel=2.4, cutoff=1400)
    fire_motif(T + 0.4, 'D5', beat=0.5, gain=0.95, kind=FIRE_DONE, vib=16, drone='D4')
    crackle(T, T + 6.0, vel=0.1)


def s13_coda():
    """1397 - end: the translators' wish, the question to the viewer, the end screen (Sisifos' motif)."""
    piano_arp(S('M00'), Se('M00') + 0.6, ['D3 F#3 A3 E4', 'G2 B2 D3 F#3', 'B2 D3 F#3 A3', 'A2 C#3 E3 G3'], step=0.4, vel=0.18)
    lyre_line(W('M00', 'coşmuşlar'), [('D5', 0.18), ('E5', 0.18), ('F#5', 0.18), ('A5', 0.6)], vel=0.32)
    pad(M('D3 F#3 A3 E4'), W('M00', 'dilekleri'), Se('M00') + 1.0, gain=0.13, cutoff=1100)
    # M02 the question to the viewer: the fire motif as a question (unresolved)
    fire_motif(Se('M02') + 0.05, 'D5', beat=0.4, gain=0.55, kind=FIRE_Q, vib=12)
    crackle(S('M02'), DUR - 0.5, vel=0.08, density=6)
    # M03 + end screen: lyre; Sisifos' boulder motif quoted once (the series), then a soft close
    t0 = S('M03')
    arp(t0, DUR - 3.0, M('D3 A3 D4 F#4'), [0, 1, 2, 3, 2, 1], 0.36, vel=0.16)
    bed(t0, DUR - 1.0, ['D3 F#3 A3', 'G2 B2 D3', 'D3 F#3 A3 E4', 'A2 C#3 E3', 'D3 F#3 A3'], gain=0.12, cutoff=900)
    lyre_line(W('M03', 'sisifosun'), [('D4', 0.42), ('E4', 0.21), ('F4', 0.21), ('A4', 0.62), ('G4', 0.21), ('D4', 0.84)], vel=0.34)
    fire_motif(Se('M03') + 1.0, 'D5', beat=0.5, kind=FIRE_DONE, gain=0.5, vib=12)
    drone('D1 D2', t0, DUR, gain=0.2, att=1.0, rel=2.5)


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


PRIORITY = {'A01': 1.3, 'A02': 1.2, 'A04': 1.3, 'F14': 1.7, 'G07b': 1.7, 'H05b': 1.3, 'J04': 1.7, 'I12': 1.3, 'K06': 1.3, 'L06': 1.5, 'M02': 1.2}   # lines that must cut through


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
    act = binary_closing(act, np.ones(int(1.0 / hop), bool))   # ≤ 1 sn'lik aralarda müzik kabarmaz
    x = act * weight
    ra, rr = np.exp(-hop / 0.10), np.exp(-hop / 0.9)
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
    # breaths of near-silence: the withheld third throne (D11), the whisper (F14), the freeze (J01), "Son söz onundur" (I12)
    dips = [(Se('D11') + 0.1, nxt('D11') - 0.4, 0.35), (W('F14', 'ama') - 0.2, W('F14', 'olacak') - 0.1, 0.18),
            (S('J01') - 0.3, W('J02', 'zeustan') - 0.2, 0.55)]
    for a, b, lvl in dips:
        g = np.minimum(g, np.interp(tg, [a, a + 0.07, b - 0.35, b], [1.0, lvl, lvl, 1.0], left=1.0, right=1.0))
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
    lead = arr(SR, 'lead')[:N]
    full += upsample(arr(SRL, 'full'), SR // SRL)[:N]
    hits += upsample(arr(SRL, 'hits'), SR // SRL)[:N]
    del _ARR[(SRL, 'full')], _ARR[(SRL, 'hits')]
    mark('upsample')
    mt, mv, used_vo = speech_mask()
    mix = np.stack([spectral_duck([(full[:, c], 1.0), (hits[:, c], 0.55), (lead[:, c], 1.5)], mt, mv) for c in range(2)], 1)
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
    for f in (s00_opening, s01_question, s02_thrones, s03_rage, s04_mekone, s05_trial, s06_defence,
              s07_witnesses, s08_secret, s09_other_end, s10_storm, s11_legacy, s12_rebel, s13_coda):
        t = time.time()
        f()
        print(f'  {f.__name__:22s} {time.time() - t:5.1f} s', flush=True)
    if MISSING:
        print('  KELİME BULUNAMADI:', ', '.join(sorted(set(MISSING))), flush=True)
    mix, used_vo = mixdown()
    write_wav(OUT, mix)
    print(f'wrote {OUT.relative_to(FILM)}  ({len(mix) / SR:.3f} s, speech mask from '
          f'{"cues.md + vo.wav" if used_vo else "cues.md"})  in {time.time() - T_START:.1f} s')


if __name__ == '__main__':
    main()
