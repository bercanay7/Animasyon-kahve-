#!/usr/bin/env python3
"""
İKAROS: özgün müzik ve efektler, tamamen numpy/scipy ile sentez (örnek ses yok, indirme yok, ücretli üretim yok).
Motor (çalgılar, efektler, miks) milton/audio/score.py'den alındı; beste bölümleri (a_..h_) bu filme özgü.
    python3 audio/score.py  -> audio/music.wav (48 kHz stereo, timeline.js DUR), audio/motifler.txt
Her vuruş bir cümleye ya da kelimeye bağlı (timeline.js); çizelge değişince yeniden çalıştırmak yeter.
"""
import json
import re
import time
import wave
from functools import lru_cache
from pathlib import Path

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
import sys as _sys; _sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from scipy.ndimage import binary_closing, binary_dilation, maximum_filter1d, minimum_filter1d
    from scipy import fft as sfft
    from scipy.signal import butter, lfilter, sosfilt
except ImportError:   # bu kapta scipy yok: numpy uyum katmanı (audio/dsp_shim.py)
    from dsp_shim import binary_closing, binary_dilation, maximum_filter1d, minimum_filter1d, butter, lfilter, sosfilt
    from dsp_shim import fft as sfft

T_START = time.time()
HERE = Path(__file__).resolve().parent
FILM = HERE.parent
OUT = HERE / 'music.wav'
VO_PATH = FILM / 'vo' / 'vo.wav'
SR, SRL = 48000, 16000          # tam hız: tel/vurmalı/efekt; düşük hız: ped, koro, org, dron
rng = np.random.default_rng(1667)

# =============================================================================== cues (timeline.js)
_TL = (FILM / 'timeline.js').read_text(encoding='utf-8')
TCUE = json.loads(re.search(r'window\.CUES = (\{.*?\});', _TL, re.S).group(1))
TWORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', _TL, re.S).group(1))
DUR = float(re.search(r'window\.DUR\s*=\s*([\d.]+)', _TL).group(1))
CUE = {k: (v['s'], v['e']) for k, v in TCUE.items()}
ORDER = sorted(TCUE, key=lambda k: TCUE[k]['s'])
N = int(round(DUR * SR))
if VO_PATH.exists():
    with wave.open(str(VO_PATH)) as _w:
        if _w.getframerate() == SR and abs(_w.getnframes() - N) < SR // 20:
            N = _w.getnframes()          # anlatım izine örnek düzeyinde eşit
SENT = np.array(sorted(CUE.values()))


def speaking(t, pre=0.15, post=0.1):
    return bool(np.any((SENT[:, 0] - pre <= t) & (t <= SENT[:, 1] + post)))



# =============================================================================== basics (engine)
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


LYRE = Bus('lute', SR, gain=0.6, send=0.30, own=True)      # lavta + klavsen (tahta gövde)
LEAD = Bus('lead', SR, gain=0.5, send=0.36, duck='lead')       # solo viol: konuşmada daha derin kısma
PERC = Bus('perc', SR, gain=0.52, send=0.22)
HITS = Bus('hits', SR, gain=0.62, send=0.18, duck='hits')
FX = Bus('fx', SR, gain=0.34, send=0.30)
STR = Bus('strings', SRL, gain=0.62, send=0.30)
DRONE = Bus('drone', SRL, gain=0.55, send=0.12)
CHOIR = Bus('choir', SRL, gain=0.40, send=0.55)
ORGAN = Bus('organ', SRL, gain=0.55, send=0.60)                # uzak org: bol salon
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
    """Deep cinematic boom settling on G1: falling sine + low noise knock, saturated."""
    fs = SR
    f0, f1 = max(f0, 70), f1           # İkaros: f1 parametre (re tonik: D1≈36,7 / D2≈73,4)
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



def debris(t, vel=0.5, dur=1.0):
    for _ in range(9):
        dt = rng.uniform(0.02, dur) ** 1.5
        n = int(0.08 * SR)
        tt = np.arange(n) / SR
        y = noise(n, 200, 2500) * np.exp(-tt / rng.uniform(0.008, 0.025))
        place(HITS, y, t + dt, gain=vel * rng.uniform(0.2, 0.6) * (1 - dt / (dur + 0.2)),
              pan=rng.uniform(-0.6, 0.6))


# =============================================================================== patterns
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
    chord = [note(x) for x in (chord.split() if isinstance(chord, str) else chord)]
    t, i = t0, 0
    while t < t1 - 1e-6:
        sp = thin and speaking(t)
        if not (sp and i % 2):
            m = chord[pattern[i % len(pattern)] % len(chord)]
            v = vel * (0.7 if sp else 1.0) * rng.uniform(0.85, 1.0)
            if inst == 'hpsi':
                hpsi(t, m, vel=v, **kw)
            else:
                lute(t, m, vel=v, **kw)
        t += step
        i += 1



# =============================================================================== new instruments (this film)
def organ(notes, t0, t1, gain=0.15, att=0.35, rel=0.9, stops=(1.0, 0.42, 0.22, 0.12, 0.05), chiff=0.08,
          width=0.5, trem=0.0, bus=None):
    """Soft, distant flue organ (8'+4'+mixture hint): additive pipes, slow speech, a breath of chiff.
    Kept low and labial: no reeds, no hymn voicing (sustained modal chords and pedal points only)."""
    bus = bus or ORGAN
    fs = bus.fs
    n = int((t1 - t0) * fs)
    if n <= 0:
        return
    tt = np.arange(n) / fs
    L = np.zeros(n)
    R = np.zeros(n)
    for j, m in enumerate(M(notes) if isinstance(notes, str) else [note(x) for x in notes]):
        f = float(mtof(m))
        dr = 2 ** (wobble(n, fs, 1.2, (0.05, 0.2)) / 1200)
        ph = 2 * np.pi * np.cumsum(f * dr) / fs + rng.uniform(0, 6.3)
        y = np.zeros(n)
        for k, a in enumerate(stops, 1):
            if f * k < fs * 0.42:
                y += a * np.sin(k * ph + rng.uniform(0, 6.3)) * (1.0 if f * k < 2500 else 0.4)
        if chiff:
            c = noise(n, min(3 * f, fs * 0.4) * 0.8, min(3 * f, fs * 0.4) * 1.2 + 10, fs) * np.exp(-tt / 0.05)
            y += chiff * c
        if trem:
            y *= 1 - trem * (0.5 + 0.5 * np.sin(2 * np.pi * 5.2 * tt))
        p = (width if m >= 50 else 0.0) * (1 if j % 2 else -1)
        L += y * np.cos((p + 1) * np.pi / 4)
        R += y * np.sin((p + 1) * np.pi / 4)
    x = np.stack([L, R], 1) * np.sqrt(2) / np.sqrt(max(1, len(notes) if not isinstance(notes, str) else len(M(notes))))
    x = lp(x, 3200, fs, 2) * env_ar(n, fs, att, rel)[:, None]
    place(bus, x, t0, gain=gain)


def hpsi(t, m, vel=0.3, pan=0.15):
    """Harpsichord: bright quill pluck (KS string, little damping) + the jack's click."""
    lyre(t, m, vel=vel, t60=1.7, bright=0.92, damp=0.12, pan=pan, detune=0.8)
    tick(t, vel=0.05 * vel / 0.3, pitch=0.8, pan=pan)


def lute(t, m, vel=0.35, pan=-0.15, **kw):
    """Lute / theorbo: warm gut pluck (KS, soft, damped), through the wooden body of the LUTE bus."""
    kw.setdefault('bright', 0.32)
    kw.setdefault('damp', 0.62)
    lyre(t, m, vel=vel, pan=pan, **kw)


def timp(t, m='G2', vel=0.5, pan=0.0, dur=3.0):
    """Timpani: near-harmonic kettle modes, slight pitch drop, felt mallet."""
    fs = SR
    f = float(mtof(note(m)))
    n = int(dur * fs)
    tt = np.arange(n) / fs
    fdrop = f * (1 + 0.025 * vel * np.exp(-tt / 0.05))
    ph = 2 * np.pi * np.cumsum(fdrop) / fs
    y = np.zeros(n)
    for r, a, tau in [(1.0, 1.0, 1.1), (1.5, 0.55, 0.75), (1.98, 0.35, 0.55), (2.44, 0.22, 0.4), (2.9, 0.12, 0.3)]:
        y += a * np.sin(r * ph + rng.uniform(0, 6.3)) * np.exp(-tt / tau)
    y += 0.5 * noise(n, None, 700, fs) * np.exp(-tt / 0.012)
    y += 0.25 * noise(n, 40, 160, fs) * np.exp(-tt / 0.18)
    y *= np.minimum(1, tt / 0.002)
    place(PERC, y / (np.abs(y).max() + 1e-9), t, gain=vel, pan=pan)


def timp_roll(t0, t1, m='G2', vel=0.3, cresc=1.0):
    t = t0
    while t < t1:
        k = (t - t0) / max(t1 - t0, 1e-3)
        timp(t, m, vel=vel * (0.35 + 0.65 * k ** cresc) * rng.uniform(0.8, 1.0), dur=1.2, pan=rng.uniform(-0.2, 0.2))
        t += rng.uniform(0.065, 0.085)


def toll(t, m='G3', vel=0.35, decay=7.0, pan=0.0):
    """One stroke of a large bronze bell (hum, prime, minor tierce, quint, nominal...). A single toll, never a peal."""
    fs = SR
    f = float(mtof(note(m)))
    n = int(decay * 1.6 * fs)
    tt = np.arange(n) / fs
    y = np.zeros(n)
    for r, a, dk in [(0.5, 0.7, 1.0), (1.0, 0.8, 0.55), (1.19, 0.55, 0.42), (1.5, 0.3, 0.32), (2.0, 0.6, 0.28),
                     (2.51, 0.25, 0.16), (2.66, 0.22, 0.14), (3.01, 0.15, 0.1), (4.16, 0.08, 0.07)]:
        fk = f * r
        if fk < 9000:
            beat = 1 + 0.004 * rng.standard_normal()
            y += a * np.exp(-tt / (decay * dk)) * (np.sin(2 * np.pi * fk * tt + rng.uniform(0, 6.3))
                                                   + 0.5 * np.sin(2 * np.pi * fk * beat * tt + rng.uniform(0, 6.3)))
    y /= np.abs(y).max() + 1e-9
    y += 0.25 * noise(n, 300, 4000, fs) * np.exp(-tt / 0.01)
    y *= np.minimum(1, tt / 0.001)
    place(HITS, y, t, gain=vel, pan=pan)


def choir_line(t, items, gain=0.25, vowel='u', voices=3):
    for m, d, v in items:
        if m is not None:
            choir([m], max(0.0, t - 0.06), t + d + 0.45, gain=gain * v, att=0.16, rel=0.4, vowel=vowel, voices=voices, vib=14)
        t += d


def organ_line(t, items, gain=0.2, **kw):
    for m, d, v in items:
        if m is not None:
            organ([m], t, t + d + 0.25, gain=gain * v, att=0.06, rel=0.3, chiff=0.12, **kw)
        t += d


def viol(t0, phrase, gain=0.3, solo=True, **kw):
    """Viol (bass/treble viol): bowed, little vibrato, slightly nasal; solo lines go on the LEAD bus (ducked deeper)."""
    kw.setdefault('vib', 6.0)
    kw.setdefault('cutoff', 2200 if solo else 1500)
    kw.setdefault('voices', 1 if solo else 2)
    kw.setdefault('detune', 3.0 if solo else 6.0)
    kw.setdefault('accent', 0.25)
    bowed(t0, phrase, gain=gain, bus=LEAD if solo else STR, **kw)


def consort(notes, t0, t1, gain=0.12, cutoff=1300, att=1.4, rel=1.6, **kw):
    """Viol consort / string pad chord."""
    pad(M(notes) if isinstance(notes, str) else notes, t0, t1, gain=gain, att=att, rel=rel, cutoff=cutoff,
        voices=2, detune=5.0, vib=kw.pop('vib', 3.0), **kw)


# =============================================================================== timing helpers
def S(i): return TCUE[i]['s']
def Se(i): return TCUE[i]['e']
def nxt(i): return S(ORDER[ORDER.index(i) + 1]) if ORDER.index(i) + 1 < len(ORDER) else DUR


MISSING = []


def _nw(w):
    w = w.replace('İ', 'i').replace('I', 'ı').lower().replace('â', 'a').replace('î', 'i').replace('û', 'u')
    return re.sub(r'[^\wçğıöşü]', '', w)


def W(i, w, n=0, end=False):
    """n-th word of sentence i starting with w (tts spelling); falls back to the sentence start (and is reported)."""
    k = 0
    for x in TWORDS:
        if x['id'] == i and x['w'].startswith(_nw(w)):
            if k == n:
                return x['e'] if end else x['s']
            k += 1
    MISSING.append(f'{i}@{w}#{n}')
    return S(i)


def We(i, w, n=0): return W(i, w, n, end=True)


# =============================================================================== sound effects (synthesized)
def whoosh(t, vel=0.3, dur=0.45, lo=180, hi=900, pan=0.0):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    env = np.sin(np.pi * np.clip(tt / dur, 0, 1)) ** 2
    place(FX, noise(n, lo, hi, SR, 2) * env, t, gain=vel, pan=pan)


def wings(t0, t1, period=0.7, vel=0.2, pan=0.0, lo=150, hi=800):
    t = t0
    while t < t1:
        whoosh(t, vel=vel * rng.uniform(0.8, 1.05), dur=0.5, lo=lo, hi=hi, pan=pan + rng.uniform(-0.1, 0.1))
        t += period * rng.uniform(0.92, 1.08)


def whoosh_down(t, dur=1.6, vel=0.25):
    """A long fall through air: high noise sliding down into low rush."""
    n = int(dur * SR)
    x = np.linspace(0, 1, n)
    hi = np.stack([noise(n, 1500, 6000, SR, 2), noise(n, 1500, 6000, SR, 2)], 1)
    lo = np.stack([noise(n, 120, 700), noise(n, 120, 700)], 1)
    c = (x ** 0.8)[:, None]
    env = (np.sin(np.pi * np.clip(x * 1.15, 0, 1)) ** 1.5)[:, None]
    place(FX, (hi * (1 - c) + lo * c) * env, t, gain=vel)


def wind(t0, t1, vel=0.12, lo=150, hi=1100, gust=0.5, att=1.5, rel=1.5):
    fs = SRL
    n = int((t1 - t0) * fs)
    if n <= 0:
        return
    tt = np.arange(n) / fs
    g = 0.6 + gust * (0.5 + 0.5 * np.sin(2 * np.pi * 0.11 * tt + rng.uniform(0, 6))) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.29 * tt + rng.uniform(0, 6)))
    y = np.stack([noise(n, lo, hi, fs, 2), noise(n, lo, hi, fs, 2)], 1) * (g * env_ar(n, fs, att, rel))[:, None]
    place(DRONE, y, t0, gain=vel)


def crackle(t0, t1, vel=0.1, density=9.0, hiss=0.12):
    """Fire: sparse sharp crackles over a soft hiss."""
    n = int((t1 - t0) * SR)
    if n <= 0:
        return
    if hiss:
        place(FX, noise(n, 900, 4000, SR, 2) * hiss * env_ar(n, SR, 0.4, 0.4), t0, gain=vel)
    k = int((t1 - t0) * density)
    m = int(0.012 * SR)
    tm = np.arange(m) / SR
    for dt in rng.uniform(0, t1 - t0, k):
        place(FX, noise(m, 1500, 8000) * np.exp(-tm / 0.002), t0 + dt, gain=vel * rng.uniform(0.3, 1.0), pan=rng.uniform(-0.5, 0.5))


def fire_bed(t0, t1, vel=0.12, crack=0.5, att=1.2, rel=1.5, density=6.0):
    """The burning lake: low roar with slow flicker (dron bus) + crackles."""
    fs = SRL
    n = int((t1 - t0) * fs)
    if n <= 0:
        return
    fl = noise(n, None, 3.0, fs)
    fl = 0.65 + 0.35 * np.tanh(fl)
    roar = np.stack([noise(n, 60, 380, fs, 2) + 0.35 * noise(n, 380, 1300, fs, 2),
                     noise(n, 60, 380, fs, 2) + 0.35 * noise(n, 380, 1300, fs, 2)], 1)
    place(DRONE, roar * (fl * env_ar(n, fs, att, rel))[:, None], t0, gain=vel)
    if crack:
        crackle(t0, t1, vel=vel * crack, density=density, hiss=0.08)


def chain_rattle(t, vel=0.3, dur=0.8, pan=0.2):
    clinks(t, count=int(5 + 8 * dur), spread=dur, vel=0.14 * vel / 0.3, pan=pan)


def chain_lock(t, vel=0.4, pan=0.1):
    """One heavy link closing: iron clank + short rattle."""
    metal(t, f0=640, vel=0.5 * vel, decay=0.45, ratios=(1, 2.41, 3.9, 5.6), click=0.9, pan=pan)
    metal(t, f0=230, vel=0.3 * vel, decay=0.3, pan=pan)
    clinks(t + 0.03, count=4, spread=0.25, vel=0.12 * vel, pan=pan)


def sword_draw(t, vel=0.3, pan=0.0):
    """Blade leaving the scabbard: rising metallic scrape, then a ring."""
    n = int(0.62 * SR)
    tt = np.arange(n) / SR
    env = np.minimum(1, tt / 0.45) ** 1.5 * np.where(tt < 0.5, 1.0, np.exp(-(tt - 0.5) / 0.03))
    grain = 0.6 + 0.4 * np.sin(2 * np.pi * (60 + 120 * tt / 0.62) * tt)
    y = noise(n, 2600, 8500, SR, 2) * env * grain
    place(FX, y, t, gain=0.5 * vel, pan=pan)
    metal(t + 0.5, f0=rng.uniform(1150, 1400), vel=0.35 * vel, decay=1.1, ratios=(1, 2.62, 4.13, 5.9), click=0.1, pan=pan)


def sword_clash(t, vel=0.6, pan=0.0):
    metal(t, f0=rng.uniform(980, 1100), vel=0.6 * vel, decay=0.8, ratios=(1, 2.31, 3.53, 4.9, 6.7), click=1.0, pan=pan)
    metal(t, f0=rng.uniform(1550, 1700), vel=0.35 * vel, decay=0.5, ratios=(1, 2.2, 3.1), click=0.5, pan=-pan)
    thud(t, vel=0.35 * vel, f0=70)


def footsteps(t0, t1, count=10, vel=0.2):
    for k, t in enumerate(np.linspace(t0, t1, count)):
        thud(t, vel=vel * (0.6 + 0.4 * k / max(count - 1, 1)), f0=rng.uniform(60, 80))
        clinks(t + 0.01, count=2, spread=0.06, vel=0.04 * vel / 0.2, pan=0.1)


def cannon(t, vel=0.7, pan=0.0):
    boom(t, vel=0.8 * vel, f0=95, decay=0.9, knock=1.0, pan=pan)
    n = int(0.6 * SR)
    tt = np.arange(n) / SR
    place(HITS, noise(n, None, 1600, SR, 2) * np.exp(-tt / 0.12) * np.minimum(1, tt / 0.002), t, gain=0.4 * vel, pan=pan)
    fs = SRL
    n2 = int(2.5 * fs)
    t2 = np.arange(n2) / fs
    place(RUMB, np.stack([noise(n2, 25, 160, fs), noise(n2, 25, 160, fs)], 1) * (np.exp(-t2 / 0.8) * np.minimum(1, t2 / 0.05))[:, None], t, gain=0.5 * vel)


def quake(t, vel=0.8, dur=3.0):
    fs = SRL
    n = int(dur * fs)
    tt = np.arange(n) / fs
    env = np.minimum(1, tt / 0.2) * np.exp(-tt / (dur * 0.5))
    place(RUMB, np.stack([noise(n, 18, 90, fs), noise(n, 18, 90, fs)], 1) * env[:, None], t, gain=vel)
    debris(t + 0.1, vel=0.35 * vel, dur=dur * 0.6)


def rumble(t0, t1, vel=0.4, lo=25, hi=140):
    """Long rolling rumble (the chariot, the world's wound)."""
    fs = SRL
    n = int((t1 - t0) * fs)
    if n <= 0:
        return
    tt = np.arange(n) / fs
    mod = 0.6 + 0.4 * np.tanh(noise(n, None, 2.0, fs))
    place(RUMB, np.stack([noise(n, lo, hi, fs), noise(n, lo, hi, fs)], 1) * (mod * env_ar(n, fs, 0.8, 1.2))[:, None], t0, gain=vel)


def quill(t0, t1, vel=0.08, pan=0.25):
    """Quill pen on paper: short scratchy strokes with tiny gaps."""
    t = t0
    while t < t1:
        d = rng.uniform(0.08, 0.32)
        n = int(d * SR)
        tt = np.arange(n) / SR
        grain = 0.55 + 0.45 * np.sin(2 * np.pi * rng.uniform(25, 45) * tt + rng.uniform(0, 6))
        env = np.minimum(1, tt / 0.01) * np.exp(-tt / (0.6 * d))
        y = noise(n, 2600, 7500, SR, 2) * grain * env
        place(FX, y, t, gain=vel * rng.uniform(0.6, 1.0), pan=pan + rng.uniform(-0.05, 0.05))
        t += d + rng.uniform(0.04, 0.22)


def page(t, vel=0.15, pan=-0.2):
    """A heavy page turning: air swish + paper crinkle."""
    n = int(0.75 * SR)
    tt = np.arange(n) / SR
    env = np.exp(-((tt - 0.22) / 0.08) ** 2) + 0.7 * np.exp(-((tt - 0.46) / 0.06) ** 2)
    y = noise(n, 500, 5000, SR, 2) * env
    for dt in rng.uniform(0.05, 0.55, 22):
        i = int(dt * SR)
        m = min(int(0.01 * SR), n - i)
        y[i:i + m] += 0.6 * noise(m, 2000, 7000) * np.exp(-np.arange(m) / (0.0015 * SR))
    place(FX, y * 0.6, t, gain=vel, pan=pan)


def drop(t, vel=0.12, pan=0.1):
    """A single tear-drop: tiny rising pitch blip (water)."""
    n = int(0.12 * SR)
    tt = np.arange(n) / SR
    f = 1300 + 1100 * (1 - np.exp(-tt / 0.012))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.025) * np.minimum(1, tt / 0.001)
    place(FX, y, t, gain=vel, pan=pan)


def puff(t, vel=0.12):
    """Candle blown out."""
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    place(FX, noise(n, 150, 1500) * np.sin(np.pi * np.clip(tt / 0.35, 0, 1)) ** 2, t, gain=vel)


def door(t, vel=0.5, dur=2.2):
    """The nine-fold gate: long iron/wood creak (stick-slip through body resonances), then the boom of the leaves."""
    fs = SR
    n = int(dur * fs)
    tt = np.arange(n) / fs
    rate = 22 + 30 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.45 * tt + 1.0)) + 6 * noise(n, None, 4, fs)
    ph = np.cumsum(rate) / fs
    imp = np.zeros(n)
    imp[np.nonzero(np.diff(np.floor(ph)) > 0)[0]] = 1.0
    imp *= rng.uniform(0.5, 1.0, n)
    y = np.zeros(n)
    for f0, r in [(420, 0.995), (780, 0.993), (1350, 0.99), (2300, 0.985)]:
        w = 2 * np.pi * f0 / fs
        y += lfilter([1.0], [1, -2 * r * np.cos(w), r * r], imp) * (1 - r)
    y *= env_ar(n, fs, 0.15, 0.3)
    y /= np.abs(y).max() + 1e-9
    place(FX, y, t, gain=0.5 * vel, pan=-0.1)
    boom(t + dur - 0.1, vel=0.7 * vel, f0=60, decay=1.4, knock=0.8)
    metal(t + dur - 0.08, f0=190, vel=0.25 * vel, decay=0.6, click=0.6)
    rumble(t + dur - 0.1, t + dur + 2.5, vel=0.35 * vel)


def hiss(t0, t1, vel=0.12, voices=1, swell=None, att=0.25, rel=0.5, lo=2600, hi=9000, pan=0.0):
    """Serpent hiss. voices>1: a hall of many hissing mouths (decorrelated, stereo-spread).
    swell: exponent for a slow rise across [t0, t1] (J05)."""
    fs = SR
    n = int((t1 - t0) * fs)
    if n <= 0:
        return
    tt = np.arange(n) / fs
    out = np.zeros((n, 2))
    for v in range(voices):
        sh = 0.55 + 0.45 * np.tanh(1.5 * noise(n, None, rng.uniform(0.6, 2.0), fs))
        a = rng.uniform(0, 0.25) * (t1 - t0) if voices > 1 else 0.0
        e = np.clip((tt - a) / 0.4, 0, 1) if voices > 1 else 1.0
        y = noise(n, lo * rng.uniform(0.85, 1.15), hi, fs, 2) * sh * e
        p = pan if voices == 1 else rng.uniform(-0.9, 0.9)
        out[:, 0] += y * np.cos((p + 1) * np.pi / 4)
        out[:, 1] += y * np.sin((p + 1) * np.pi / 4)
    out *= np.sqrt(2) / np.sqrt(voices)
    g = env_ar(n, fs, att, rel)
    if swell:
        g = g * (0.08 + 0.92 * np.clip(tt / (t1 - t0), 0, 1) ** swell)
    place(FX, out * g[:, None], t0, gain=vel)


def snap(t, vel=0.3):
    """Fruit torn from the branch: twig crack + leaf rustle."""
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    y = noise(n, 1500, 9000) * np.exp(-tt / 0.0015)
    y += 0.6 * np.roll(noise(n, 1200, 7000) * np.exp(-tt / 0.002), int(0.018 * SR))
    y += 0.4 * np.sin(2 * np.pi * 950 * tt) * np.exp(-tt / 0.012)
    y += 0.15 * noise(n, 1500, 6000) * np.exp(-tt / 0.12)
    place(FX, y, t, gain=vel, pan=0.15)


def crunch(t, vel=0.25):
    """A bite into fruit."""
    for dt in np.sort(rng.uniform(0, 0.16, 6)):
        n = int(0.04 * SR)
        tt = np.arange(n) / SR
        place(FX, noise(n, 700, 4500) * np.exp(-tt / 0.007), t + dt, gain=vel * rng.uniform(0.5, 1.0), pan=0.1)
    thud(t, vel=0.08, f0=150)


def croak(t, vel=0.12):
    """A toad by Eve's ear: two low pulsed croaks."""
    for k in range(2):
        n = int(0.32 * SR)
        tt = np.arange(n) / SR
        pul = (np.sin(2 * np.pi * 27 * tt) > 0.2).astype(float)
        y = np.sin(2 * np.pi * (330 - 40 * tt) * tt) * pul
        y = bp(y, 200, 1400) * np.sin(np.pi * np.clip(tt / 0.32, 0, 1))
        place(FX, y, t + k * 0.45, gain=vel, pan=-0.3)


def birds(t0, t1, vel=0.04, rate=1.2):
    """Eden: sparse little chirps, only where nobody speaks."""
    t = t0
    while t < t1:
        if not speaking(t, pre=0.3, post=0.3):
            for c in range(rng.integers(1, 4)):
                n = int(0.07 * SR)
                tt = np.arange(n) / SR
                f0 = rng.uniform(2800, 4200)
                f = f0 + rng.uniform(600, 1500) * np.sin(np.pi * tt / 0.07)
                y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / 0.07) ** 2
                place(FX, y, t + c * 0.11, gain=vel * rng.uniform(0.5, 1.0), pan=rng.uniform(-0.8, 0.8))
        t += rate * rng.uniform(0.6, 1.6)


def crowd(t0, t1, vel=0.12, att=0.6, rel=1.2):
    """Hell's cheering host, far away: formant-shaped noise voices with random swells."""
    fs = SR
    n = int((t1 - t0) * fs)
    if n <= 0:
        return
    out = np.zeros((n, 2))
    for v in range(8):
        src = noise(n, 150, 3500, fs)
        y = 0.0
        for fc, bw, g in [(700, 200, 1.0), (1150, 220, 0.6), (2600, 400, 0.25)]:
            fc *= rng.uniform(0.85, 1.15)
            y = y + g * bp(src, fc - bw / 2, fc + bw / 2, fs, 1)
        sw = np.clip(0.5 + 0.8 * noise(n, None, rng.uniform(1.0, 3.0), fs), 0, 1.6)
        p = rng.uniform(-0.8, 0.8)
        out[:, 0] += y * sw * np.cos((p + 1) * np.pi / 4)
        out[:, 1] += y * sw * np.sin((p + 1) * np.pi / 4)
    out = lp(out, 2800, fs, 2) * env_ar(n, fs, att, rel)[:, None]
    place(FX, out / np.sqrt(8), t0, gain=vel)


def ash(t0, t1, vel=0.12):
    """Fruit crumbling to ash: falling grains, thinning out."""
    for dt in (rng.uniform(0, 1, int(60 * (t1 - t0))) ** 1.8) * (t1 - t0):
        n = int(0.02 * SR)
        tt = np.arange(n) / SR
        place(FX, noise(n, 400, 3000) * np.exp(-tt / 0.004), t0 + dt, gain=vel * rng.uniform(0.2, 0.8), pan=rng.uniform(-0.4, 0.4))
    n = int((t1 - t0) * SR)
    place(FX, noise(n, 200, 1500) * 0.15 * env_ar(n, SR, 0.1, (t1 - t0) * 0.7), t0, gain=vel)


def shimmer(t, dur=1.5, vel=0.06, notes=('D6', 'G6', 'A6', 'B6', 'D7')):
    """Glitter (the morning star, the false radiance): fast high bell plinks."""
    k = int(dur * 9)
    for dt in np.sort(rng.uniform(0, dur, k)):
        bell(t + dt, rng.choice(list(notes)), vel=vel * rng.uniform(0.4, 1.0) * (1 - 0.5 * dt / dur), decay=0.8,
             pan=rng.uniform(-0.7, 0.7))


def stab(t, notes, vel=0.3, cutoff=1600, rel=1.2):
    """String-section sting (short, accented chord)."""
    for m in M(notes):
        bowed(t, [(m, 0.4)], gain=vel / np.sqrt(len(M(notes))), voices=2, cutoff=cutoff, vib=0, accent=1.0, att=0.01, rel=rel)


# =============================================================================== motifs
NOTELOG = []
_NM = ['Do', 'Do#', 'Re', 'Mib', 'Mi', 'Fa', 'Fa#', 'Sol', 'Lab', 'La', 'Sib', 'Si']


def nname(m): return f'{_NM[int(m) % 12]}{int(m) // 12 - 1}'


def nearest_cue(t):
    best = ORDER[0]
    for k in ORDER:
        if S(k) <= t + 0.5:
            best = k
    return best


LIGHT = {
    'full': [(4, 1.0), (7, 0.5), (14, 1.5), (12, 2.5)],          # B4 D5 A5 G5
    'min': [(3, 1.0), (7, 0.5), (14, 1.5), (12, 2.5)],           # Bb4 D5 A5 G5
    'broken': [(3, 1.0), (7, 0.5), (13, 1.5), (12, 2.5)],        # Bb4 D5 Ab5 G5 (Phrygian)
    'half': [(3, 1.0), (7, 2.5)],                                # Bb4 D5 ... the leap never comes
    'hope': [(4, 1.0), (7, 0.5), (14, 3.0)],                     # B4 D5 A5, left hanging
    'home': [(4, 1.0), (7, 0.5), (14, 1.5), (12, 1.0), (11, 0.5), (12, 3.0)],   # ... G5 F#5 G5: resolved
}
FALL = [(0, 1.5), (-1, 0.5), (-2, 1.5), (-3, 0.5), (-4, 2.0), (-5, 3.0)]       # G F# F E Eb D, limping
FALL9 = [(-k, 1.0) for k in range(10)]                                        # G2 .. Bb1: nine semitone steps
ABDIEL = [(0, 1.0), (7, 1.0), (9, 1.0), (7, 2.0)]                               # G4 D5 E5 D5
EDEN = [(7, 0.5), (4, 0.5), (5, 0.5), (2, 0.5), (4, 0.5), (0, 1.5)]             # D5 B4 C5 A4 B4 G4


def mot(root, items, beat, vel=1.0):
    root = note(root)
    return [(root + o, d * beat, vel) for o, d in items]


def _log(t, name, ph):
    NOTELOG.append((t, name, ' '.join(nname(m) for m, _, _ in ph)))


def light(t, kind='full', root='G4', beat=0.45, inst='viol', gain=None, **kw):
    ph = mot(root, LIGHT[kind], beat)
    _log(t, f'IŞIK/{kind} ({inst})', ph)
    if inst == 'viol':
        viol(t, ph, gain=gain or 0.32, **kw)
    elif inst == 'choir':
        choir_line(t, ph, gain=gain or 0.3, vowel=kw.pop('vowel', 'a'))
    elif inst == 'organ':
        organ_line(t, ph, gain=gain or 0.22)
    elif inst == 'hpsi':
        for m, d, v in ph:
            hpsi(t, m, vel=gain or 0.3)
            t += d
    elif inst == 'lute':
        for m, d, v in ph:
            lute(t, m, vel=gain or 0.35, pan=0.1)
            t += d
    return sum(d for _, d, _ in ph)


def fall(t, root='G2', beat=0.45, kind=FALL, gain=0.34, inst='bowed', **kw):
    ph = mot(root, kind, beat)
    _log(t, 'DÜŞÜŞ' + ('/9' if kind is FALL9 else '') + f' ({inst})', ph)
    if inst == 'bowed':
        bowed(t, ph, gain=gain, stack=kw.pop('stack', (0, 12)), cutoff=kw.pop('cutoff', 900), vib=kw.pop('vib', 3),
              voices=2, **kw)
    elif inst == 'organ':
        organ_line(t, ph, gain=gain, stops=(1.0, 0.5, 0.2))
    elif inst == 'pizz':
        for m, d, v in ph:
            lute(t, m, vel=gain, t60=0.9, damp=0.85)
            t += d
    return sum(d for _, d, _ in ph)


def abdiel(t, beat=0.6, gain=0.3):
    ph = mot('G4', ABDIEL, beat)
    _log(t, 'ABDİEL (viol)', ph)
    viol(t, ph, gain=gain, vib=4.0)


def eden(t, beat=0.36, vel=0.28, inst='hpsi'):
    ph = mot('G4', EDEN, beat)
    _log(t, f'ADEN ({inst})', ph)
    for m, d, v in ph:
        (hpsi if inst == 'hpsi' else lute)(t, m, vel=vel)
        t += d


def bed(t0, t1, chords, gain=0.12, cutoff=1200, att=1.6, rel=1.6, ov=0.8, kind='consort', **kw):
    """Chord progression laid evenly over [t0, t1], overlapping crossfades. kind: consort | organ | choir."""
    if t1 <= t0:
        return
    k = len(chords)
    d = (t1 - t0) / k
    for i, ch in enumerate(chords):
        a = max(0.0, t0 + i * d - (ov if i else 0))
        b = t0 + (i + 1) * d + (ov if i < k - 1 else 0)
        if kind == 'consort':
            consort(ch, a, b, gain=gain, cutoff=cutoff, att=att, rel=rel, **kw)
        elif kind == 'organ':
            organ(ch, a, b, gain=gain, att=att, rel=rel, **kw)
        else:
            choir(M(ch), a, b, gain=gain, att=att, rel=rel, **kw)


def lute_arp(t0, t1, chords, step=0.42, vel=0.22, pattern=(0, 1, 2, 3, 2, 1), inst='lute'):
    k = len(chords)
    if t1 <= t0:
        return
    d = (t1 - t0) / k
    for i, ch in enumerate(chords):
        arp(t0 + i * d, t0 + (i + 1) * d, M(ch), list(pattern), step, inst=inst, vel=vel)


def card(t, notes='G1 D2 G2', vel=0.5):
    """Chapter card: a low soft stroke (timpani + boom), the same colour every time."""
    timp(t, M(notes)[-1], vel=0.45 * vel)
    boom(t, vel=0.35 * vel, f0=75, decay=1.0, knock=0.3)



# =============================================================================== İKAROS: beste
# Ton: re (D). Ege rengi: dorian (Si doğal) ve miksolidyen (Do doğal); gökte majör, düşüşte minör.
SABAH = ['D2 A2 D3 F#3', 'G2 D3 G3 B3', 'A2 E3 A3 C#4', 'D2 A2 E3 F#3']
DORYA = ['D2 A2 D3 F3', 'C3 G3 C4 E4', 'G2 D3 G3 B3', 'A2 E3 A3 C4']
GECE = ['D2 A2 F3 A3', 'Bb1 F2 D3 F3', 'G1 D2 Bb2 D3', 'A1 E2 C#3 E3']
UCUS = [(0, .5), (2, .5), (4, .5), (7, .5), (9, 1.0), (7, .5), (12, 1.5)]      # D E F# A B A D: uçuş (yükselen)
UYARI_ALT, UYARI_UST, UYARI_ORTA = 'A2', 'A5', 'D4'                               # deniz, güneş, orta
KEKLIK = ['C6', 'A5', 'C6']

def mel(t, items, inst='lyre', vel=.3, **kw):
    """Ezgi: items (midi, sn, vel). lyre için tek tek çalınır, bowed için ifade."""
    if inst == 'bowed': bowed(t, items, gain=vel, **kw); return sum(d for _, d, _ in items)
    for m, d, v in items: lyre(t, m, vel=vel * v, **kw); t += d
    return sum(d for _, d, _ in items)

def ucus(t, root='D4', beat=.38, inst='lyre', vel=.3, **kw):
    ph = mot(root, UCUS, beat); _log(t, f'UÇUŞ ({inst})', ph); return mel(t, ph, inst, vel, **kw)

def deniz(t0, t1, vel=.08, period=5.5):
    """Dalgalar: alçak geçiren gürültü, yavaş genlik dalgası (dalga boyu ~period sn)."""
    n = int(max(0, t1 - t0) * SR)
    if n <= 0: return
    tt = np.arange(n) / SR
    env = (.55 + .45 * np.sin(2 * np.pi * tt / period + 1.3)) * np.clip(tt / 1.5, 0, 1) * np.clip((t1 - t0 - tt) / 1.5, 0, 1)
    place(FX, noise(n, 120, 900, SR, 2) * env, t0, gain=vel)

def keklik_otus(t, vel=.05):
    for k, m in enumerate(KEKLIK): bell(t + k * .13, m, vel=vel * (1 - .2 * k), decay=.25, pan=.3)

def a_kanca():
    """A: 'İki uyarı' — güneş (yüksek koro, parıltı) ve deniz (dalga) arasında asılı soru."""
    wind(0.0, S('B02'), vel=.06, lo=300, hi=1400)
    pad(M('D3 A3 E4'), .2, Se('A01') + 1.0, gain=.1, att=.8, rel=1.0, cutoff=1100)
    lyre(W('A01', 'iki'), 'A4', vel=.25); lyre(W('A01', 'uyarı'), 'D5', vel=.22)
    choir(M('A4 E5'), W('A02', 'güneşe') - .2, Se('A02') + .6, gain=.14, att=.4, rel=.8, vowel='a')
    shimmer(W('A02', 'güneşe'), dur=1.4, vel=.04, notes=('A6', 'D7', 'E7', 'F#7'))
    deniz(S('A03') - .3, S('B02') + .8, vel=.07)
    drone('D2 A2', S('A03'), S('B02') + .5, gain=.16, att=.8, rel=1.0)
    bowed(W('A03', 'oysa'), [('E3', Se('A03') - W('A03', 'oysa') + 1.0, .6)], gain=.12, stack=(0, 5), cutoff=900, vib=4)

def b_girit():
    """B: Girit afişi, labirent, sürgün, 'gök açık'."""
    T = S('B02') - .3
    toll(T, 'D3', vel=.18, decay=5.0)
    arp(S('B02'), Se('B02') + .5, 'D3 A3 D4 F4'.split(), (0, 1, 2, 3, 2, 1), .36, vel=.16)
    for k in range(6): lyre(W('B02', 'labirent') + k * .18, ['D4', 'F4', 'E4', 'C4', 'D4', 'A3'][k], vel=.12, pan=-.2)
    deniz(S('B03'), Se('B03') + .6, vel=.08)
    bed(S('B03'), Se('B03') + .4, DORYA[:2], gain=.09, cutoff=900)
    bowed(W('B03', 'özlüyordu') - .2, [('A3', 1.0, .7), ('G3', 1.2, .6), ('F3', 1.6, .5)], gain=.14, cutoff=1000)
    wind(S('B04'), Se('B04') + 1.0, vel=.06, lo=500, hi=2200, gust=.8)
    riser(W('B04', 'gök') - .05, 1.0, vel=.08, kind='cym')
    pad(M('D3 A3 D4 F#4 A4'), W('B04', 'gök'), Se('B04') + 1.2, gain=.12, att=.3, rel=1.0, cutoff=1500)
    birds(W('B04', 'gök') + .4, Se('B04') + .6, vel=.02, rate=.8)

def c_mum():
    """C: atölye (lir), uyarı motifi (alçak / yüksek / orta), sır, öpücük."""
    arp(S('C01'), Se('C02') + .3, 'D3 A3 D4 E4'.split(), (0, 2, 1, 3, 2, 1), .3, vel=.13, pan=-.15)
    for k in range(8): tick(W('C01', 'dizdi') - 1.2 + k * .16, vel=.05, pitch=1 + k * .06)
    for k in range(4): drop(W('C01', 'mumla') + k * .14, vel=.05)
    bell(W('C03', 'tehlikesiyle'), 'A5', vel=.06, decay=2.0)
    bowed(S('C03') - .1, [('D4', 2.2, .5)], gain=.1, stack=(0, 6), cutoff=900, vib=3)          # tritone: tehlike
    ucus(W('C04', 'denedi'), 'D4', beat=.3, vel=.18)
    T = S('C05')
    pad(M('D3 A3'), T - .3, Se('C05') + .6, gain=.08, att=.6, rel=.6, cutoff=700)
    drone(UYARI_ALT, W('C05', 'alçalırsan') - .1, W('C05', 'yükselirsen'), gain=.18, att=.15, rel=.5); deniz(W('C05', 'alçalırsan'), W('C05', 'yükselirsen') + .5, vel=.06, period=2.2)
    choir([note(UYARI_UST)], W('C05', 'yükselirsen') - .1, W('C05', 'arasından'), gain=.12, att=.15, rel=.5, vowel='a'); shimmer(W('C05', 'güneş'), dur=.8, vel=.03)
    lyre(W('C05', 'arasından'), UYARI_ORTA, vel=.3); lyre(W('C05', 'arasından') + .3, 'A4', vel=.22)
    drone(UYARI_ALT, W('C06', 'çok') - .1, W('C06', 'üstelik'), gain=.2, att=.1, rel=.4)
    boom(W('C06', 'sırrı') + .35, vel=.18, f0=90, f1=36.7, decay=1.2, knock=.1)
    pad(M('D2 G#2 D3'), W('C06', 'ama') - .1, Se('C06') + .8, gain=.1, att=.4, rel=.8, cutoff=500)
    lyre(W('C07', 'izle'), 'D4', vel=.25)
    bowed(S('C08'), [('F#4', 2.0, .5), ('E4', 1.6, .55), ('D4', 1.2, .6), ('A3', 2.4, .5)], gain=.14, cutoff=1200)
    pad(M('D3 A3 F#4'), W('C08', 'öptü') - .2, Se('C08') + 1.4, gain=.08, att=.6, rel=1.2, cutoff=1000)

def d_ucus():
    """D: kalkış, tanıklar, sevinç, öğleye tırmanış; 'kibir değil'."""
    T = S('D01')
    riser(T, .9, vel=.14, kind='swell')
    wings(T + .1, Se('D01') + .5, period=.6, vel=.14); wind(T, Se('D05') + .8, vel=.08, lo=300, hi=2400, gust=.7)
    bed(T, Se('D02') + .5, SABAH, gain=.1, cutoff=1500)
    ucus(T + .05, 'D4', beat=.36, inst='bowed', vel=.2); ucus(T + .05, 'D5', beat=.36, vel=.18)
    arp(W('D01', 'daidalos'), Se('D01'), 'D4 F#4 A4 D5', (0, 1, 2, 3, 2, 1), .24, vel=.12)
    deniz(S('D02') - .5, Se('D03') + .5, vel=.05)
    for w, m in (('balıkçı', 'A4'), ('çoban', 'B4'), ('çiftçi', 'D5')): lyre(W('D02', w), m, vel=.16)
    choir(M('D4 F#4 A4 D5'), W('D03', 'tanrı') - .2, Se('D03') + 1.0, gain=.16, att=.4, rel=.9, vowel='a')
    T = S('D04')
    bed(T, Se('D04') + .6, ['G2 D3 G3 B3', 'A2 E3 A3 C#4', 'B2 F#3 B3 D4', 'D3 A3 D4 F#4'], gain=.1, cutoff=1800)
    ucus(W('D04', 'sevincine'), 'D5', beat=.3, vel=.2)
    bowed(W('D04', 'yükseğe') - .3, [('A4', .6, .6), ('B4', .6, .65), ('D5', .9, .7), ('F#5', 1.8, .75)], gain=.16, cutoff=2400)
    shimmer(W('D04', 'yükseğe'), dur=1.6, vel=.05, notes=('A6', 'B6', 'D7', 'E7', 'F#7'))
    pad(M('D3 A3 E4 F#4'), S('D05'), Se('D05') + .8, gain=.08, att=.3, rel=.8, cutoff=1400)
    for w in ('kibir', 'cüretten', 'sevinçten', 'arzudan'): lyre(W('D05', w), 'D5' if w != 'kibir' else 'G#4', vel=.15)

def e_dusus():
    """E: mum erir (yüksek tel gerilir), çırpınış, düşüş (sessizlik), çağrı, tüyler, İkarya."""
    T = S('E01')
    bowed(T - .2, [((note('A5'), note('G#5')), 3.2, .5)], gain=.1, stack=(0, 1), cutoff=3000, vib=2, trem=.3)
    for k in range(6): drop(W('E01', 'mum') + k * .45, vel=.05, pan=.1 * k - .2)
    wings(S('E02'), Se('E02'), period=.32, vel=.12)
    bowed(S('E02'), [('D3', 1.5, .6), ('C#3', 1.5, .6), ('C3', 1.5, .6)], gain=.12, stack=(0, 6), cutoff=900, trem=.6)
    whoosh_down(W('E03', 'düşerken') - .2, dur=2.0, vel=.16)
    drop(W('E03', 'yuttu'), vel=.12); boom(W('E03', 'yuttu') + .05, vel=.14, f0=80, f1=36.7, decay=1.4, knock=.1)
    deniz(W('E03', 'yuttu'), Se('E05') + 1.0, vel=.06)
    bowed(S('E04'), [('D4', 1.2, .4), ('A3', 2.6, .5)], gain=.12, cutoff=900)
    toll(W('E04', 'neredesin') + .7, 'D3', vel=.14, decay=6.0)
    bed(S('E05'), Se('E05') + 1.2, ['D2 A2 D3 F3', 'Bb1 F2 D3 F3', 'G1 D2 Bb2 D3', 'A1 E2 C#3 E3'], gain=.1, cutoff=800)
    bowed(W('E05', 'ikarya') - .3, [('F4', 1.0, .5), ('E4', 1.0, .5), ('D4', 2.4, .55)], gain=.12, cutoff=1200)

def f_keklik():
    """F: alacakaranlık; keklik ötüşü (sevinç), çocuğun hikâyesi, kale, Athena'nın ışığı, alçaktan uçuş."""
    T = S('F01')
    drone('D2 A2', T - .3, Se('F02') + .5, gain=.12, att=1.0, rel=.8)
    for k in range(3): keklik_otus(W('F02', 'öttü') + k * .55, vel=.06)
    wings(W('F02', 'kanatlarını'), W('F02', 'kanatlarını') + .8, period=.18, vel=.06, lo=400, hi=1800)
    pad(M('D3 G#3 C4'), S('F03') - .1, Se('F03') + .6, gain=.09, att=.3, rel=.6, cutoff=700)
    boom(W('F03', 'çocuktu') + .25, vel=.12, f0=85, f1=36.7, decay=1.0, knock=.1)
    arp(S('F04'), Se('F04') + .3, 'D3 A3 D4 E4'.split(), (0, 2, 1, 3), .3, vel=.11)
    for k in range(5): tick(W('F04', 'testereyi') + k * .12, vel=.05, pitch=1.4)
    timp(W('F05', 'kıskandı'), 'D2', vel=.22)
    drone('D2 Eb2', S('F05'), Se('F05') + .4, gain=.12, att=.3, rel=.6)
    whoosh_down(W('F05', 'attı') - .1, dur=1.1, vel=.09)
    bowed(W('F05', 'yalan') - .2, [('Eb4', 1.2, .5), ('D4', 1.8, .5)], gain=.1, cutoff=900)
    riser(W('F06', 'yakalayıp') - .1, .8, vel=.06, kind='cym'); shimmer(W('F06', 'yakalayıp'), dur=1.6, vel=.05, notes=('D6', 'A6', 'D7', 'E7'))
    choir(M('D4 A4 E5'), W('F06', 'yakalayıp') - .1, Se('F06') + .8, gain=.11, att=.3, rel=.8, vowel='o')
    birds(S('F07'), Se('F07'), vel=.02, rate=.6)
    for k in range(3): keklik_otus(S('F07') + 1 + k * 2.6, vel=.035)
    bed(S('F07'), Se('F07') + .4, DORYA[:2], gain=.08, cutoff=800)
    lyre(W('F08', 'ortadan'), UYARI_ORTA, vel=.22); drone(UYARI_ALT, W('F08', 'atmıştı') - .2, Se('F08') + 1.2, gain=.16, att=.2, rel=1.0)
    boom(W('F08', 'atmıştı') + .4, vel=.16, f0=90, f1=36.7, decay=1.4, knock=.15)

def g_ucuslar():
    """G: gece, üç uçuş; en iyisi ya da hiç; batan tüyler; şafakla 'ama önce uçtu'; Bruegel; soru; bitiş."""
    T = S('G01')
    bed(T, Se('G02') + .5, GECE, gain=.09, cutoff=900)
    lyre(W('G01', 'güneşe'), 'A5', vel=.14); lyre(W('G01', 'keklik'), 'A3', vel=.16); lyre(W('G01', 'usta'), 'D4', vel=.16)
    timp(W('G03', 'en'), 'A2', vel=.14); timp(W('G03', 'hiç'), 'D2', vel=.18)
    pad(M('D3 F3 A3'), S('G04'), Se('G04') + .5, gain=.07, att=.5, rel=.6, cutoff=800)
    deniz(S('G05') - .3, Se('G05') + .8, vel=.05, period=7.0)
    bowed(S('G05'), [('A3', 2.0, .5), ('G3', 2.0, .5), ('F3', 2.0, .5), ('E3', 3.0, .5)], gain=.11, cutoff=800)
    T = S('G06')
    riser(T, 1.0, vel=.1, kind='swell'); wind(T, Se('G07') + .8, vel=.06, lo=300, hi=2400)
    bed(T, Se('G07') + .8, SABAH, gain=.1, cutoff=1600)
    ucus(W('G06', 'önce') - .1, 'D4', beat=.4, inst='bowed', vel=.2); ucus(W('G06', 'önce') - .1, 'D5', beat=.4, vel=.18)
    choir(M('D4 A4 D5 F#5'), W('G07', 'babasının') - .2, Se('G07') + 1.0, gain=.12, att=.6, rel=1.0, vowel='a')
    T = S('G08')
    arp(T, Se('G08') + .3, 'G3 D4 G4 B4'.split(), (0, 1, 2, 3, 2, 1), .3, vel=.12, pan=.2)               # pastoral (sol)
    birds(T + .5, Se('G08'), vel=.018, rate=.7); deniz(T, Se('G08') + .5, vel=.04)
    drop(W('G08', 'bacak'), vel=.06)
    pad(M('G3 D4 A4'), S('G09') - .2, Se('G09') + 1.4, gain=.1, att=.6, rel=1.2, cutoff=1300)        # soru akoru (çözülmez)
    T = S('H01')
    bed(T, DUR - .2, SABAH, gain=.09, cutoff=1400, att=1.2, rel=2.5)
    ucus(T + .8, 'D4', beat=.45, vel=.2); ucus(W('H01', 'milton') - .2, 'A4', beat=.42, inst='bowed', vel=.14)
    arp(W('H01', 'abone') - 1.0, DUR - 1.0, 'D4 F#4 A4 D5', (0, 1, 2, 3, 2, 1), .3, vel=.1)

SECTIONS = [a_kanca, b_girit, c_mum, d_ucus, e_dusus, f_keklik, g_ucuslar]


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


PRIORITY = {'A01': 1.3, 'C05': 1.3, 'C06': 1.2, 'E04': 1.3, 'F03': 1.2, 'F08': 1.3, 'G06': 1.2, 'G09': 1.35}   # lines that must cut through


def speech_mask():
    """Smoothed 'narration present' curve on a 10 ms grid (timeline.js, refined with vo.wav).
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
    """J04: real silence (the applause that never comes) from the end of J03's last word to the hiss in J05;
    the final close after the end screen. Computed on a 5 ms grid."""
    tg = np.arange(0, n / SR + 0.01, 0.005)
    g = np.ones(len(tg))
    a = We('E03', 'yuttu') + 0.9               # İkaros: su sesi yuttu; kısa gerçek sessizlik
    b = S('E04') - 0.15                        # babanın çağrısından hemen önce ses döner
    g = np.minimum(g, np.interp(tg, [a, a + 0.6, b, b + 0.05], [1.0, 0.0, 0.0, 1.0], left=1.0, right=1.0))
    g *= np.interp(tg, [DUR - 4.0, DUR - 0.05], [1.0, 0.0], left=1.0, right=0.0) ** 2
    return tg, g


def room_tone():
    """A barely audible empty hall under the J04 silence (so it is silence, not a dropout)."""
    a, b = We('E03', 'yuttu') + 0.9, S('E04') + 0.4
    n = int((b - a) * SR)
    x = np.stack([noise(n, 40, 700, SR, 2), noise(n, 40, 700, SR, 2)], 1) * env_ar(n, SR, 0.8, 0.8)[:, None]
    return a, (x * 10 ** (-58 / 20)).astype(np.float32)


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
    mix = np.stack([spectral_duck([(full[:, c], 1.0), (hits[:, c], 0.8), (lead[:, c], 1.5)], mt, mv) for c in range(2)], 1)
    _ARR.clear()
    mark('duck+eq')
    tg, gg = master_gain(N)
    mix *= np.interp(np.arange(N, dtype=float) / SR, tg, gg).astype(np.float32)[:, None]
    mix *= limiter_gain(mix).astype(np.float32)[:, None]
    mix *= np.float32(10 ** (-1 / 20) / np.abs(mix).max())
    ra, rt = room_tone()
    i = int(ra * SR)
    m = min(len(rt), N - i)
    mix[i:i + m] += rt[:m]
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


def write_notelog(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('# Motiflerin çaldığı anlar (audio/score.py üretir; zaman = film saniyesi)\n')
        for t, name, notes in sorted(NOTELOG):
            f.write(f'{int(t // 60):02d}:{t % 60:05.2f}  {nearest_cue(t):5s} {name:34s} {notes}\n')


def main():
    print(f'film {DUR:.2f} s, {N} samples, {len(CUE)} sentences', flush=True)
    for f in SECTIONS:
        t = time.time()
        f()
        print(f'  {f.__name__:22s} {time.time() - t:5.1f} s', flush=True)
    if MISSING:
        print('  KELİME BULUNAMADI:', ', '.join(sorted(set(MISSING))), flush=True)
    write_notelog(HERE / 'motifler.txt')
    mix, used_vo = mixdown()
    write_wav(OUT, mix)
    print(f'wrote {OUT.relative_to(FILM)}  ({len(mix) / SR:.3f} s, speech mask from '
          f'{"timeline.js + vo.wav" if used_vo else "timeline.js"})  in {time.time() - T_START:.1f} s')


if __name__ == '__main__':
    main()

