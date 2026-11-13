#!/usr/bin/env python3
"""
CUMHURİYET ("Tek bir dâhinin değil, bir kuşağın hikâyesi"): original score, fully synthesized with
numpy/scipy (no samples, nothing downloaded). The instrument and DSP library is the channel's own, inherited
from sisifos/audio/score.py.

    python3 audio/score.py          (from the film folder or anywhere; paths are relative to this file)
    -> audio/music.wav              48 kHz, stereo, 16-bit, exactly window.DUR long
    -> audio/cues.md                regenerated: section boundaries and musical intentions at the current timing

Inputs
    timeline.js     window.CUES {id: {s, e}}, window.WORDS [{id, w, s, e}], window.DUR, parsed at runtime.
                    Every event in the score is anchored to a sentence (S/E) or to a word inside it (W/WE).
                    When the real voice-over arrives, tools/build_vo.py rewrites timeline.js with the same ids
                    and a plain rerun re-times the whole score.
    senaryo.json    which sentence belongs to which section (bolum)
    vo/vo.wav       optional; only *analysed* to find where speech is. Never mixed in.

Palette
    kanun / lyre     Karplus-Strong, two detuned strings per note, wooden body resonance
    ney / reed       additive reed or breathy flute: vibrato, breath noise, tonguing (Uşşak, Hicaz)
    strings, horns   band-limited (polyBLEP) detuned saw ensembles; horns get a cheap filter envelope
    choir "aah/ooh"  saw glottal source + vibrato + formant banks
    felt piano       slightly inharmonic partials as recursive resonators, two strings per note
    percussion       frame drum (modal membrane), timpani, booms, cymbal, wall-clock tick, hand bell, bells
    brass band       cornet / trumpet / trombone / tuba lines (tongued, brightness follows each note's envelope,
                     mouthpiece formant), snare drum, marching bass drum, clarinet (reed engine), glockenspiel
    one shared stereo convolution hall (one FFT per channel; 16 kHz twin for the low-rate buses)

Harmony   home D. Night D minor -> D Uşşak (segâh ~160 cents) for the Hamidian schools -> G Mixolydian
          harbour -> D minor/Phrygian secrets -> rising to a Bb-major 1908 -> D Phrygian/Hicaz war ->
          D Dorian Anatolia (B natural: hope) -> D major Republic.
Motif     "kuşak" (the generation), scale steps 1 3 2 5 4 8, rhythm 1 1 ½ 1½ 1 3 beats: it climbs by
          stepping forward and leaning back, like people standing on each other's shoulders.
          fragile   1 3 2 5        minor piano (A02 -> A04), F major lift (A05), lyre (C02), Bb major (D02)
          growing   1 3 2 5 4      Uşşak ney on 'sorgulamayı' (C03) and D04, minor cello (C06, E04)
          stronger  1 3 2 5 4 6    D Dorian strings + horns, ends on the hopeful B natural (F05)
          complete  1 3 2 5 4 8    D major: strings, horns, trumpets, choir, bells (G01)
          band      1 3 2 5 4 8 + its mirror 8 6 7 5 4 2 1: an original 2/4 brass-band march for the end screen
                    (soft under G06, open after it); a 1908 street band plays the first major glimpse (D02)
          It quotes no anthem or march (İstiklal, İzmir, Onuncu Yıl, Ceddin Deden, Harbiye, mehter).

Mix       Everything is ducked spectrally under the narration (STFT dynamic EQ: lows -3 dB,
          220 Hz-3.8 kHz -9 dB, highs -5 dB; the narrator's own comments and the whispered C03 duck deeper,
          see PRIORITY), driven by timeline.js and vo/vo.wav, so the music swells into the gaps.
          Hits are ducked about half as much. A near-silence holds "Yaşasın Cumhuriyet!"; the climax answers it.
          Peak-normalised to -1 dBFS; overall loudness balance is set later, in tools/mix.py.
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
rng = np.random.default_rng(1923)


# =============================================================================== timeline
def norm1(w):
    """Word normalisation, identical to tools/build_vo.py and tools/fake_timeline.py."""
    return re.sub(r"[^\wçğıöşüâî]+", '', w.lower().replace('İ', 'i').replace('I', 'ı').replace("'", '')
                  .replace('’', '').replace('â', 'a').replace('î', 'i').replace('û', 'u'))


def load_timeline(path):
    txt = path.read_text(encoding='utf-8')
    dec = json.JSONDecoder()

    def grab(name):
        m = re.search(r'window\.' + name + r'\s*=\s*', txt)
        if not m:
            raise SystemExit(f'{path}: window.{name} not found')
        return dec.raw_decode(txt, m.end())[0]

    cues = {k: (float(v['s']), float(v['e'])) for k, v in grab('CUES').items()}
    return float(grab('DUR')), cues, grab('WORDS'), 'fake_timeline' in txt.split('\n', 1)[0]


DUR, CUE, WORDS, PROVISIONAL = load_timeline(FILM / 'timeline.js')
N = int(round(DUR * SR))                 # exactly DUR long (tools/mix.py uses the same length)
ORDER = sorted(CUE, key=lambda c: CUE[c][0])
SENT = np.array([CUE[c] for c in ORDER])
WBY = {}
for _w in WORDS:
    WBY.setdefault(_w['id'], []).append(_w)
try:
    BOLUM = {s['id']: s['bolum'] for s in
             json.loads((FILM / 'senaryo.json').read_text(encoding='utf-8'))['segments']}
except (OSError, ValueError, KeyError):
    BOLUM = {}
SECTIONS = []                            # [(letter, bolum, [ids])] in film order
for _c in ORDER:
    if not SECTIONS or SECTIONS[-1][0] != _c[0]:
        SECTIONS.append((_c[0], BOLUM.get(_c, _c[0]), []))
    SECTIONS[-1][2].append(_c)
GROUP = {L: ids for L, _, ids in SECTIONS}
_WARNED = set()


def S(c): return CUE[c][0]
def E(c): return CUE[c][1]


def W(c, word, k=0, end=False):
    """Start (end=True: end) of the k-th word of sentence c equal to `word` (else: starting with it).
    A missing word falls back to the sentence start/end with a warning, so a script edit never breaks a run."""
    q = norm1(word)
    ws = WBY.get(c, [])
    hits = [w for w in ws if w['w'] == q] or [w for w in ws if w['w'].startswith(q)]
    if len(hits) > k:
        return float(hits[k]['e' if end else 's'])
    if (c, word, k) not in _WARNED:
        _WARNED.add((c, word, k))
        print(f'  ! word "{word}" #{k} not found in {c}; using the sentence {"end" if end else "start"}')
    return E(c) if end else S(c)


def WE(c, word, k=0): return W(c, word, k, end=True)


def sec_span(L):
    """(start of the section's first sentence, start of the next section's first sentence | DUR)."""
    i = [x[0] for x in SECTIONS].index(L)
    return S(GROUP[L][0]), (S(SECTIONS[i + 1][2][0]) if i + 1 < len(SECTIONS) else DUR)


def cue_at(t):
    """The sentence that is current at time t (the last one started; the first one before the film starts)."""
    c = ORDER[0]
    for k in ORDER:
        if CUE[k][0] <= t:
            c = k
        else:
            break
    return c


def speaking(t, pre=0.15, post=0.1):
    return bool(np.any((SENT[:, 0] - pre <= t) & (t <= SENT[:, 1] + post)))


def fit(t0, t1, beats, lo, hi):
    """Beat length that makes `beats` beats fill [t0, t1], kept within [lo, hi] seconds (elastic phrases)."""
    return float(np.clip((t1 - t0) / max(beats, 1e-6), lo, hi))


# =============================================================================== basics
_PC = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)


_ACC = {'#': 1, 'b': -1, 'q': -0.4}     # q: koma-flat (about 40 cents), e.g. 'Eq4' = segâh in D Uşşak


def note(s):
    if not isinstance(s, str):
        return s
    pc, i = _PC[s[0]], 1
    while s[i] in _ACC:
        pc += _ACC[s[i]]
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


LYRE = Bus('lyre', SR, gain=0.62, send=0.30, own=True)          # lyre, kanun, pizzicato
AULOS = Bus('reed', SR, gain=0.34, send=0.36)            # ney, reed
PERC = Bus('perc', SR, gain=0.52, send=0.22)
HITS = Bus('hits', SR, gain=0.62, send=0.18, duck='hits')
FX = Bus('fx', SR, gain=0.34, send=0.40)
STR = Bus('strings', SRL, gain=0.62, send=0.28)
DRONE = Bus('drone', SRL, gain=0.42, send=0.12)
CHOIR = Bus('choir', SRL, gain=0.40, send=0.55)
PIANO = Bus('piano', SRL, gain=0.62, send=0.34)
RUMB = Bus('rumble', SRL, gain=0.60, send=0.10, duck='hits')
BRASS = Bus('horns', SRL, gain=0.55, send=0.32)
BANDB = Bus('band', SR, gain=0.5, send=0.3)         # brass band at full rate: cornets and trumpets need the top


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
    items = [(nn(it[0]), max(it[1], 0.0), it[2] if len(it) > 2 else 1.0) for it in phrase]
    total = sum(d for _, d, _ in items)
    if total < 0.05 or all(m is None for m, _, _ in items):
        return
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
    a = smooth(np.concatenate([[0.0], amp]), att, fs)[1:] * (1 + accent * decays(acc, 0.13, fs))
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
    if n < int(0.05 * fs):
        return
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


def aulos(t0, phrase, gain=0.3, vib=16.0, glide=0.03, breath=0.05, pan=0.0, drone=None, att=0.04, rel=0.3,
          tilt=0.8, bright=0.12, hmax=9000.0, top=9500.0):
    """Reed: additive double-reed melody pipe (+ optional drone pipe), vibrato, breath, tonguing.
    A higher tilt / lower bright / more breath turns it into a ney (see ney())."""
    fs = AULOS.fs
    items = [(nn(it[0]), max(it[1], 0.0), it[2] if len(it) > 2 else 1.0) for it in phrase]
    total = sum(d for _, d, _ in items)
    if total < 0.05:
        return
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
    a = smooth(np.concatenate([[0.0], amp]), att, fs)[1:]
    a[i_end:] *= rc(n - i_end)[::-1]
    vz = smooth(vibz, 0.2, fs)
    vr = 5.3 + 0.25 * np.sin(2 * np.pi * 0.6 * tt)
    cents = vib * vz * np.sin(2 * np.pi * np.cumsum(vr) / fs) + wobble(n, fs, 3.0, (0.5, 2.0))
    f = mtof(p) * 2 ** (cents / 1200)
    y = reed(f, a, fs, hmax=hmax, tilt=tilt, bright=bright)
    y *= 1 + 0.03 * noise(n, None, 40, fs)
    y /= np.abs(y).max() + 1e-9
    y += breath * noise(n, 1200, 5500, fs) * a / (a.max() + 1e-9)
    y += 0.25 * noise(n, 2000, 7000, fs) * decays(acc, 0.018, fs) * a / (a.max() + 1e-9)
    if drone is not None:
        fd = np.full(n, float(mtof(note(drone)))) * 2 ** (wobble(n, fs, 2.5, (0.2, 1.0)) / 1200)
        da = smooth(np.where(a > 0.05 * a.max(), 1.0, 0.0), 0.15, fs) * env_ar(n, fs, 0.05, rel)
        d = reed(fd, da, fs, tilt=0.95, bright=0.0)
        y += 0.32 * d / (np.abs(d).max() + 1e-9)
    y = lp(y, top, fs, 4)
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
    """Deep cinematic boom settling on f1 (A1 by default): falling sine + low noise knock, saturated."""
    fs = SR
    f0 = max(f0, 75)
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
    """Thunder / distant artillery: a crack, a rolling low rumble and a deep boom."""
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
    boom(t, vel=0.85 * vel, f0=50, f1=36.7, decay=2.0)


def thud(t, vel=0.5, f0=55):
    fs = SRL
    n = int(0.5 * fs)
    tt = np.arange(n) / fs
    y = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 0.4 * np.exp(-tt / 0.02))) / fs) * np.exp(-tt / 0.1)
    y += 0.5 * noise(n, None, 250, fs) * np.exp(-tt / 0.03)
    place(RUMB, y * np.minimum(1, tt / 0.001), t, gain=vel, pan=rng.uniform(-0.4, 0.4))






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



# =============================================================================== more instruments
def kanun(t, m, vel=0.4, pan=-0.25):
    """Kanun: a bright, short plucked course (lyre engine, light damping, wider detune)."""
    f = float(mtof(note(m)))
    lyre(t, m, vel=vel, t60=float(np.clip(2.2 * (110 / f) ** 0.45, 0.5, 2.6)), bright=0.72, damp=0.3, pan=pan,
         detune=3.0)


def ney(t0, phrase, gain=0.45, pan=0.2, vib=9.0, breath=0.13):
    """Ney: the reed engine as an end-blown flute: few harmonics, breath, slow vibrato, a soft top."""
    aulos(t0, phrase, gain=gain, vib=vib, glide=0.05, breath=breath, pan=pan, att=0.09, rel=0.45,
          tilt=1.7, bright=0.03, hmax=5000.0, top=5200.0)


def hz(s):
    """Hicaz intonation: the augmented second is a little narrower (Eb/Bb a bit high, F#/C# a bit low)."""
    if s is None:
        return None
    m = note(s)
    pc = int(round(m)) % 12
    return m + (0.1 if pc in (3, 10) else -0.1 if pc in (1, 6) else 0.0)


TIMP = [(1.0, 1.0, 1.0), (1.504, 0.55, 0.6), (1.742, 0.25, 0.4), (2.0, 0.35, 0.45), (2.245, 0.15, 0.3),
        (2.494, 0.18, 0.3), (2.8, 0.08, 0.2), (2.98, 0.08, 0.2)]          # (ratio, amplitude, decay factor)


def timp(t, m, vel=0.6, pan=0.0, dur=3.0, decay=1.6):
    """Timpani: tuned membrane modes with a small pitch drop after the stroke, felt-mallet thump."""
    fs = SR
    f = float(mtof(note(m)))
    n = int(dur * fs)
    tt = np.arange(n) / fs
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.012 * vel * np.exp(-tt / 0.08))) / fs
    y = sum(a * np.sin(r * ph + rng.uniform(0, 6.3)) * np.exp(-tt / (decay * d)) for r, a, d in TIMP)
    y += 0.35 * noise(n, None, 500, fs) * np.exp(-tt / 0.012)
    y *= np.minimum(1, tt / 0.0015)
    fo = min(int(0.05 * fs), n)
    y[-fo:] *= rc(fo)[::-1]
    place(PERC, y / (np.abs(y).max() + 1e-9), t, gain=vel, pan=pan)


def timp_roll(t0, t1, m, v0=0.1, v1=0.6, rate=0.065):
    t = t0
    while t < t1:
        k = (t - t0) / max(t1 - t0, 1e-3)
        timp(t, m, vel=(v0 + (v1 - v0) * k ** 1.5) * rng.uniform(0.85, 1.0), dur=0.9, pan=rng.uniform(-0.2, 0.2))
        t += rate * rng.uniform(0.9, 1.1)


def cymbal(t, vel=0.3, decay=2.5, pan=0.0):
    """Suspended cymbal crash: bright stereo noise with a fast sizzle and a long wash."""
    n = int(decay * 3 * SR)
    tt = np.arange(n) / SR
    y = np.stack([noise(n, 3500, 12000), noise(n, 3500, 12000)], 1) * np.exp(-tt / decay)[:, None]
    y += 0.5 * np.stack([noise(n, 6000, 14000), noise(n, 6000, 14000)], 1) * np.exp(-tt / 0.15)[:, None]
    y *= np.minimum(1, tt / 0.002)[:, None]
    place(FX, y, t, gain=vel, pan=pan)


def brass(notes, t0, t1, gain=0.2, att=0.3, rel=0.8, bright=0.6, voices=2, detune=5.0, pan=0.0, width=0.5):
    """Horn section chord: detuned saws through a dark and a bright low-pass, cross-faded by the amplitude
    envelope (a cheap filter envelope: louder = brighter), with a small pitch scoop into the attack."""
    fs = BRASS.fs
    n = int((t1 - t0) * fs)
    if n < int(0.05 * fs):
        return
    tt = np.arange(n) / fs
    e = env_ar(n, fs, att, rel)
    L = np.zeros(n)
    R = np.zeros(n)
    nv = 0
    scoop = -30.0 * np.exp(-tt / 0.05)
    for m in notes:
        f = float(mtof(note(m)))
        for v in range(voices):
            c = rng.uniform(-detune, detune) + wobble(n, fs, 3.0) + scoop
            y = blep_saw(f * 2 ** (c / 1200), fs)
            w = (1 + width) / 2 if v % 2 == 0 else (1 - width) / 2
            L += y * w
            R += y * (1 - w)
            nv += 1
    x = np.stack([L, R], 1) / np.sqrt(nv)
    b = (bright * e ** 1.5)[:, None]
    y = lp(x, 450, fs, 2) * (1 - b) + lp(x, 2800, fs, 2) * b
    place(BRASS, hp(y, 55, fs, 2) * e[:, None], t0, gain=gain, pan=pan)


# ------------------------------------------------------------------------------- brass band
BAND = dict(    # mouthpiece formants (Hz, gain), dark / bright low-pass corners, vibrato and attack-scoop cents
    trumpet=dict(form=((1250, 1.1), (2600, 0.5)), dark=900, bright=6500, vib=8.0, scoop=-30.0, hp=120),
    cornet=dict(form=((1050, 0.9),), dark=700, bright=4200, vib=7.0, scoop=-22.0, hp=110),
    trombone=dict(form=((520, 0.9), (1150, 0.45)), dark=380, bright=3000, vib=5.0, scoop=-28.0, hp=50),
    tuba=dict(form=((240, 0.7),), dark=200, bright=1100, vib=2.0, scoop=-15.0, hp=28),
)
BANDCH = dict(D=('D2', 'A1', 'F#3 A3 D4'), A=('A1', 'E2', 'E3 A3 C#4'), G=('G1', 'D2', 'G3 B3 D4'),
              A7=('A1', 'E2', 'E3 G3 C#4'), Bb=('Bb1', 'F2', 'F3 Bb3 D4'), F=('F1', 'C2', 'F3 A3 C4'),
              Bm=('B1', 'F#2', 'F#3 B3 D4'))     # (tuba root, tuba fifth, off-beat voicing)


def band_line(t0, phrase, kind='cornet', gain=0.3, pan=0.0, voices=2, detune=6.0, gap=0.05, bright=0.85):
    """A brass-band line: tongued notes (fast attack, a small scoop up into the pitch, a brief brassy edge),
    brightness that follows each note's envelope (dark / mid / bright low-passes cross-faded), a mouthpiece
    formant, late vibrato, and a short release before the next note (march articulation; `gap` seconds).
    phrase items: (note | None, seconds[, vel]). Peak-normalised, so `gain` is the level."""
    P = BAND[kind]
    fs = SR
    items = [(nn(it[0]), max(it[1], 0.0), it[2] if len(it) > 2 else 1.0) for it in phrase]
    total = sum(d for _, d, _ in items)
    if total < 0.05 or all(m is None for m, _, _ in items):
        return
    n = int((total + 0.3) * fs)
    pitch = np.full(n, np.nan)
    amp = np.zeros(n)
    edge = np.zeros(n)
    cents = np.zeros(n)
    t = 0.0
    for m, d, v in items:
        i0, i1 = int(t * fs), int((t + d) * fs)
        if m is not None and i1 > i0:
            x = np.arange(i1 - i0) / fs
            g = float(np.clip(gap, 0.015, 0.45 * d))
            e = np.minimum(1, x / 0.016) * (0.82 + 0.18 * np.exp(-x / 0.07))
            amp[i0:i1] = v * e * np.clip((d - x) / g, 0, 1) ** 0.7
            pitch[i0:i1] = m
            edge[i0:i1] = np.exp(-x / 0.06)
            vz = np.clip((x - 0.28) / 0.3, 0, 1) * (d > 0.45)
            cents[i0:i1] = P['scoop'] * np.exp(-x / 0.035) + P['vib'] * vz * np.sin(2 * np.pi * 5.4 * x)
        t += d
    valid = ~np.isnan(pitch)
    idx = np.where(valid, np.arange(n), 0)
    np.maximum.accumulate(idx, out=idx)
    pitch = pitch[idx]
    pitch[np.isnan(pitch)] = pitch[valid][0]
    p = smooth(pitch, 0.008, fs)
    x = sum(blep_saw(mtof(p) * 2 ** ((cents + rng.uniform(-detune, detune) + wobble(n, fs, 2.0)) / 1200), fs)
            for _ in range(voices)) / np.sqrt(voices)
    a = amp / (amp.max() + 1e-9)
    b = np.clip(bright * a ** 1.2 + 0.35 * edge * a, 0, 1)
    mid = np.sqrt(P['dark'] * P['bright'])
    y = lp(x, P['dark'], fs, 2) * (1 - b) ** 2 + 2 * lp(x, mid, fs, 2) * b * (1 - b) + lp(x, P['bright'], fs, 2) * b ** 2
    for f, gf in P['form']:
        y = y + gf * bp(y, f / 1.3, min(f * 1.3, fs * 0.45), fs, 1)
    y = hp(y, P['hp'], fs, 2) * amp
    place(BANDB, y / (np.abs(y).max() + 1e-9), t0, gain=gain, pan=pan)


def oompah(t0, q, plan, vel=1.0, tuba=0.3, stabs=0.16):
    """March accompaniment: tuba on the beats (root, fifth), trombones on the off-beats.
    plan: [(beats, BANDCH key)]."""
    tb, st = [], [[], [], []]
    k = 0
    for nb, key in plan:
        root, fifth, upper = BANDCH[key]
        ups = upper.split()
        for _ in range(nb):
            tb.append((root if k % 2 == 0 else fifth, q, vel * (1.0 if k % 2 == 0 else 0.85)))
            for j in range(3):
                st[j] += [(None, q / 2), (ups[j], q / 2, vel)]
            k += 1
    band_line(t0, tb, 'tuba', gain=tuba, gap=0.16)
    for j in range(3):
        band_line(t0, st[j], 'trombone', gain=stabs, pan=(-0.35, 0.05, 0.35)[j], gap=0.09, bright=0.7)


def snare(t, vel=0.3, pan=0.12):
    """Snare drum (trampet): two shell modes + the snare wires' rattle."""
    n = int(0.3 * SR)
    tt = np.arange(n) / SR
    y = 0.55 * np.sin(2 * np.pi * 190 * tt + rng.uniform(0, 6.3)) * np.exp(-tt / 0.045)
    y += 0.3 * np.sin(2 * np.pi * 335 * tt + rng.uniform(0, 6.3)) * np.exp(-tt / 0.03)
    y += 0.8 * noise(n, 1800, 9500, SR, 2) * np.exp(-tt / 0.085)
    y += 0.4 * noise(n, 4000, 11000) * np.exp(-tt / 0.01)
    y *= np.minimum(1, tt / 0.0006)
    place(PERC, y / (np.abs(y).max() + 1e-9), t + rng.normal(0, 0.002), gain=vel, pan=pan)


def snare_roll(t0, t1, v0=0.05, v1=0.3, rate=0.042):
    t, k = t0, 0
    while t < t1:
        x = (t - t0) / max(t1 - t0, 1e-3)
        snare(t, vel=(v0 + (v1 - v0) * x ** 1.4) * (1.0 if k % 2 else 0.85))
        t += rate * rng.uniform(0.93, 1.07)
        k += 1


def snare_bar(t, q, vel=0.2, pat='A . t t a . t .'):
    """One 2/4 bar in sixteenths: A accent, a tap, t ghost, '.' rest."""
    for i, tok in enumerate(pat.split()):
        if tok != '.':
            snare(t + i * q / 4, vel=vel * {'A': 1.0, 'a': 0.7, 't': 0.4}[tok])


def bassdrum(t, vel=0.4, pan=0.0):
    """Marching bass drum: a felt beater on a big, loose head."""
    n = int(0.7 * SR)
    tt = np.arange(n) / SR
    y = np.sin(2 * np.pi * np.cumsum(50 + 45 * np.exp(-tt / 0.02)) / SR) * np.exp(-tt / 0.25)
    y += 0.35 * noise(n, None, 350) * np.exp(-tt / 0.012)
    y *= np.minimum(1, tt / 0.001)
    place(PERC, y / (np.abs(y).max() + 1e-9), t, gain=vel, pan=pan)


def woodtick(t, vel=0.1, pitch=1.0, pan=0.3):
    """A wooden tick (wall clock, school clock, telegraph sounder): a click with two small body resonances."""
    n = int(0.06 * SR)
    tt = np.arange(n) / SR
    y = noise(n, 1800 * pitch, 7000, SR, 2) * np.exp(-tt / 0.004)
    y += 0.6 * np.sin(2 * np.pi * 2400 * pitch * tt) * np.exp(-tt / 0.012)
    y += 0.5 * np.sin(2 * np.pi * 780 * pitch * tt) * np.exp(-tt / 0.02)
    place(PERC, y * np.minimum(1, tt / 0.0004), t + rng.normal(0, 0.002), gain=vel, pan=pan)


def clock(t0, t1, period=1.0, vel=0.1, fade=None, pan=0.3):
    """A wall clock: tick-tock, the tock a little lower and softer. fade=([times], [gains])."""
    t, k = t0, 0
    while t < t1:
        g = 1.0 if fade is None else float(np.interp(t, fade[0], fade[1]))
        woodtick(t, vel=vel * g * (1.0 if k % 2 == 0 else 0.8), pitch=1.0 if k % 2 == 0 else 0.84, pan=pan)
        t += period
        k += 1


def telegraph(t, vel=0.09, pan=0.5):
    for dt, p in [(0, 1.0), (0.09, 0.85), (0.27, 1.0), (0.36, 0.85), (0.6, 1.0), (0.66, 0.85), (0.75, 1.0), (0.84, 0.85)]:
        woodtick(t + dt, vel=vel, pitch=1.3 * p, pan=pan)


def handbell(t, m, vel=0.12, strikes=3, rate=0.17, pan=0.35):
    """A school hand bell, rung a few times."""
    f = float(mtof(note(m)))
    for i in range(strikes):
        metal(t + i * rate * rng.uniform(0.9, 1.1), f0=f, vel=vel * (1 - 0.12 * i), decay=1.3,
              ratios=(1, 2.0, 2.66, 3.43, 4.25, 5.4), click=0.15, pan=pan, bus=FX)


def drum_bars(t0, t1, e, pats, vel=0.5, f0=70, grow=0.0):
    """Frame-drum patterns, one token per eighth `e`: D dum, d soft dum, T tek, t soft tek, '.' rest."""
    t, k = t0, 0
    while t < t1 - 1e-6:
        for i, tok in enumerate(pats[k % len(pats)].split()):
            tt = t + i * e
            if tok == '.' or tt >= t1:
                continue
            g = vel * (1 + grow * (tt - t0) / max(t1 - t0, 1e-3))
            if tok in 'Dd':
                fdrum(tt, 'dum', vel=g * (1.0 if tok == 'D' else 0.6) * rng.uniform(0.9, 1.05), f0=f0)
            else:
                fdrum(tt, 'tek', vel=g * (0.45 if tok == 'T' else 0.28) * (0.6 if speaking(tt) else 1.0), f0=210)
        t += len(pats[k % len(pats)].split()) * e
        k += 1


def pulse_line(t0, t1, beat, roots, v0=0.5, v1=0.8, gain=0.3, stack=(0, 12), cutoff=800, timp_every=2, tek=None):
    """Steady détaché beats in the low strings (one bowed call). roots: [(time, note)], the line follows them;
    crescendo v0 -> v1; timpani every `timp_every` beats; frame-drum 'tek' on the off-beats from time `tek`."""
    roots = sorted((t, note(m)) for t, m in roots)
    nb = int((t1 - t0) / beat)
    if nb < 1:
        return
    items = []
    for k in range(nb):
        t = t0 + k * beat
        r = roots[0][1]
        for a, m in roots:
            if a <= t + 0.05:
                r = m
        v = v0 + (v1 - v0) * k / max(nb - 1, 1)
        items.append((r, beat, v * (1.0 if k % 2 == 0 else 0.85)))
        if timp_every and k % timp_every == 0:
            timp(t, r + 12 if r < note('C2') else r, vel=0.32 * v)
        if tek is not None and t >= tek:
            fdrum(t + beat / 2, 'tek', vel=0.13 * v * (0.7 if speaking(t + beat / 2) else 1.0), f0=210)
    bowed(t0, items, gain=gain, stack=stack, cutoff=cutoff, vib=0, att=0.02, accent=0.6, rel=0.3, legato=False)


def chords(seq, t_end, gain=0.15, ov=0.9, lead=0.3, bass=None, **kw):
    """Pad progression. seq: [(anchor, 'notes')] or [(anchor, 'notes', {pad overrides})]; each chord arrives
    `lead` s before its anchor and cross-fades (ov) into the next; the last one lasts until t_end.
    bass: bowed() keywords -> the lowest notes also become a legato bass line."""
    seq = sorted(seq, key=lambda x: x[0])
    for i, it in enumerate(seq):
        o = dict(kw, gain=gain)
        o.update(it[2] if len(it) > 2 else {})
        t1 = seq[i + 1][0] - lead + ov if i + 1 < len(seq) else t_end
        pad(M(it[1]), it[0] - lead, t1, **o)
    if bass:
        ph = []
        for i, it in enumerate(seq):
            t1 = seq[i + 1][0] - lead if i + 1 < len(seq) else t_end - bass.get('rel', 0.6)
            ph.append((M(it[1])[0], t1 - (it[0] - lead), 1.0))
        bowed(seq[0][0] - lead, ph, **bass)


# =============================================================================== the kuşak motif
# (scale step, beats): 1 3 2 5 4 8. Climbs by stepping forward and leaning back; fragments end open.
KUSAK = [(0, 1.0), (2, 1.0), (1, 0.5), (4, 1.5), (3, 1.0), (7, 3.0)]
SCALES = dict(major=[0, 2, 4, 5, 7, 9, 11, 12], minor=[0, 2, 3, 5, 7, 8, 10, 12],
              dorian=[0, 2, 3, 5, 7, 9, 10, 12], ussak=[0, 1.6, 3, 5, 7, 8, 10, 12],
              hicaz=[0, 1.1, 3.9, 5, 7, 8, 10, 12])


def kusak(root, beat, scale='major', n=6, vel=1.0, hold=None, sixth=False):
    """The motif as phrase items [(midi, seconds, vel)]. n=4: 1 3 2 5 (fragile, open); n=5: + 4 (hangs);
    n=6: + 8 (complete) or, sixth=True, + 6 (hopeful, not home). hold: length of the last note in beats."""
    sc = SCALES[scale]
    r = note(root)
    out = []
    for i, (st, b) in enumerate(KUSAK[:n]):
        if i == 5 and sixth:
            st = 5
        out.append((r + sc[st], b * beat, vel * (0.9 + 0.02 * i)))
    if hold is not None:
        out[-1] = (out[-1][0], hold * beat, out[-1][2])
    return out


def kbeats(n=6, hold=None):
    b = [d for _, d in KUSAK[:n]]
    if hold is not None:
        b[-1] = hold
    return sum(b)


def onsets(t, items):
    out = []
    for _, d, _ in items:
        out.append(t)
        t += d
    return out


def play(t, items, inst, vel=1.0, oct=0, **kw):
    """Phrase on a struck or plucked instrument: inst(t, midi, vel=..., **kw) per note."""
    for m, d, v in items:
        if m is not None:
            inst(t, m + oct, vel=vel * v, **kw)
        t += d
    return t


# =============================================================================== the score
def sec_acilis():
    """Açılış (A01-A05): Ankara, the night of 28 October 1923, a small dinner. Felt piano, low strings, a wall
    clock. The motif, fragile and in D minor, follows "Yarın Cumhuriyet ilan edeceğiz!" into the cadre who
    founded it (A04); a small lift into F major on '...değil… bir kuşağın hikâyesi' (A05)."""
    _, t_end = sec_span('A')
    lift = WE('A05', 'değil')                          # the breath before "bir kuşağın hikâyesi"
    q0 = E('A02') + 0.1                                # after "Yarın Cumhuriyet ilan edeceğiz!"
    clock(0.35, lift - 0.25, period=1.0, vel=0.12, fade=([S('A04'), lift], [1.0, 0.4]))
    seq = [(0.55, 'D2 A2 F3 E4'), (W('A02', 'yarın'), 'Bb1 F2 D3 A3'), (q0, 'D2 A2 F3 E4'),
           (W('A04', 'otuz'), 'Bb1 F2 D3 F3'), (W('A04', 'sultanın'), 'G1 D2 Bb2 E3'),
           (W('A04', 'abdülhamidin'), 'A1 E2 D3 E3'), (S('A05'), 'D2 A2 F3 A3')]
    chords(seq, lift + 1.0, gain=0.14, att=1.5, rel=1.3, cutoff=620, sine=0.35,
           bass=dict(gain=0.2, stack=(0, 12), cutoff=520, vib=4, att=0.6, rel=1.0, accent=0.15))
    zone = (q0 - 0.2, W('A04', 'otuz') + 0.6)
    for t0, c in seq:                                  # the felt piano, sparse broken chords
        if zone[0] <= t0 <= zone[1]:
            continue
        for i, m in enumerate(M(c)[1:4]):
            t = t0 + 0.05 + 0.62 * i
            piano(t, m + 12 if m < note('C3') else m, vel=0.2 * (0.8 if speaking(t) else 1.0), pan=-0.15 + 0.15 * i)
    b = fit(q0, W('A04', 'otuz') + 0.3, 4.0, 0.46, 0.7)
    play(q0, kusak('D4', b, 'minor', n=4, hold=3), piano, vel=0.4)
    piano(q0, 'D3', vel=0.2)
    piano(q0 + 2.5 * b, 'A2', vel=0.17)
    # the lift: F major, the motif in major for the first time (still only four notes)
    pad(M('F2 C3 A3 E4 G4'), lift - 0.15, t_end + 1.4, gain=0.13, att=0.9, rel=1.7, cutoff=1250, sine=0.3)
    bowed(lift - 0.1, [('F2', t_end - lift + 0.6, 0.9)], gain=0.2, stack=(0, 12), cutoff=600, vib=4, att=0.5, rel=1.2)
    piano(lift + 0.02, 'F3', vel=0.24)
    piano(lift + 0.04, 'C4', vel=0.2)
    t = lift + 0.14
    bl = fit(t, E('A05') + 0.1, 2.5, 0.36, 0.6)     # the held 4th note answers after "hikâyesi"
    play(t, kusak('F4', bl, 'major', n=4, hold=4), piano, vel=0.26)
    piano(t + 2.5 * bl, 'C6', vel=0.09)


def sec_okullar():
    """Sultanın okulları (B01-B06): D Uşşak. Kanun ostinato, ney, a school-clock tick and a soft bendir; a hand
    bell opens the school. Darker and sparse where the sultan shuts the Meclis (B01), thinner under the
    narrator's own comment (B05). After 'Kemal' the ney walks down to G, the harbour's tonic."""
    b0, b1 = sec_span('B')
    e8 = 0.30
    t0 = b0 - 0.45
    tstop = E('B06') + 0.1
    dark = W('B01', 'meclisi')
    drone('D2 A2', t0 - 0.4, b1 + 0.6, gain=0.2, att=2.0, rel=1.4, cutoff=300)
    seq = [(b0, 'D3 A3'), (dark, 'G2 D3 Bb3', dict(cutoff=480)), (S('B02'), 'D3 A3'), (S('B03'), 'D3 A3 F4 C5'),
           (S('B04'), 'D3 A3 F4'), (S('B05'), 'Bb2 F3 D4', dict(gain=0.08)), (S('B06'), 'F3 C4 A4'),
           (W('B06', 'kendi'), 'D3 A3 F4'), (E('B06'), 'G2 D3 G3', dict(cutoff=900))]
    chords(seq, b1 + 0.8, gain=0.11, cutoff=650, att=1.4, rel=1.2, sine=0.3)
    handbell(b0 - 0.4, 'A5', vel=0.1, strikes=4)
    PAT = dict(D1='D3 A3 D4 A3 Eq4 D4 A3 D4', D2='D3 A3 D4 A3 F4 Eq4 D4 A3', C='C3 G3 C4 G3 D4 C4 Bb3 A3',
               Bb='Bb2 F3 Bb3 F3 A3 G3 F3 Eq3', s1='D3 . . A3 . . D4 .', s2='C3 . . G3 . . Bb3 .',
               s3='D3 . . A2 . . . .')
    PLAN = dict(B01=['s1', 's1', 'D1', 'D2'], B02=['D1', 'D2', 'C', 'Bb'], B03=['D1', 'D2', 'C', 'Bb'],
                B04=['D1', 'D2', 'D1', 'Bb'], B05=['s1', 's2'], B06=['D1', 'D2', 'C', 'Bb'])
    VEL = dict(B01=0.34, B02=0.38, B03=0.44, B04=0.36, B05=0.3, B06=0.4)
    used = {}
    t = t0
    while t < tstop - 0.2:
        c = cue_at(t + 4 * e8)
        c = c if c in PLAN else 'B01'
        key = 's3' if c == 'B01' and t + 4 * e8 >= dark else PLAN[c][used.get(c, 0) % len(PLAN[c])]
        used[c] = used.get(c, 0) + 1
        sparse = key.startswith('s')
        for i, tok in enumerate(PAT[key].split()):
            tt = t + i * e8
            if tok == '.' or tt > tstop - 0.15:
                continue
            v = VEL[c] * (1.12 if i in (0, 4) else 1.0) * (0.92 if i % 2 else 1.0) * (0.85 if speaking(tt) else 1.0)
            kanun(tt, note(tok), vel=v)
            if i == 0 and not sparse:
                kanun(tt + 0.012, note(tok) + 12, vel=v * 0.35, pan=-0.1)
        if c in ('B02', 'B03', 'B04', 'B06'):                 # the school clock
            for i in range(0, 8, 2):
                if t + i * e8 < tstop:
                    woodtick(t + i * e8, vel=0.07 if i % 4 else 0.085, pitch=1.15 if i % 4 else 1.25, pan=0.35)
        if c in ('B03', 'B04', 'B06'):                        # a soft bendir
            fdrum(t, 'dum', vel=0.2, f0=82)
            fdrum(t + 5 * e8, 'tek', vel=0.08, f0=220)
            fdrum(t + 6 * e8, 'dum', vel=0.12, f0=82)
        t += 8 * e8
    ney(E('B01') + 0.05, [('A4', 0.55), ('Bb4', 0.18), ('A4', 0.18), ('G4', 0.22), ('F4', 0.25), ('Eq4', 0.35),
                          ('D4', 1.3)], gain=0.32)
    ney(E('B03') + 0.02, [('D5', 0.12), ('Eq5', 0.12), ('F5', 0.12), ('G5', 0.14),
                          ('A5', max(S('B04') - E('B03') - 0.62, 0.25))], gain=0.42)
    tg = E('B06') + 0.05                                   # down to G: the harbour's tonic
    ney(tg, [('D5', 0.3), ('C5', 0.22), ('Bb4', 0.22), ('A4', 0.4), ('G4', max(b1 - tg - 1.0, 0.6) + 0.5)],
        gain=0.4)
    kanun(tg + 1.14, 'G3', vel=0.3)
    kanun(tg + 1.15, 'D4', vel=0.22)


def sec_selanik():
    """Selanik ve yasak kitaplar (C01-C06): an open harbour in G Mixolydian (7/8 plucks, light pad, water,
    a flick of colour for each language), the motif sprouting after 'filizlendi' (C02). C03: the ney asks
    with the motif in Uşşak on 'sorgulamayı'; from 'Manastır'da' whispers - low D drone, sparse pizzicato,
    a muted heartbeat, the forbidden words glow. C04 darker (Eb, tremolo); four plucks for the four students
    (C05); exile in Hicaz and the motif in the cellos 'arkadaşlarıyla' - with friends (C06)."""
    c0, c1 = sec_span('C')
    q = W('C03', 'sorgulamayı')
    wh = W('C03', 'manastırda')                       # the [softly] turn: secrets
    e8 = 0.19
    H = dict(G='G3 D4 B3 D4 G4 D4 B3', F='F3 C4 A3 C4 F4 C4 A3', C='C3 G3 C4 G3 E4 G3 C4', Dm='D3 A3 D4 A3 F4 A3 D4')
    BASS = dict(G='G2', F='F2', C='C2', Dm='D2')
    prog = ['G', 'G', 'F', 'G', 'C', 'G', 'F', 'Dm']
    t, k = c0 - 0.3, 0
    while t + 7 * e8 <= S('C03') - 0.2:
        c = cue_at(t + 3 * e8)
        thin = c == 'C02'
        ch = prog[k % 8]
        for i, tok in enumerate(H[ch].split()):
            if thin and i not in (0, 2, 4):
                continue
            tt = t + i * e8
            v = (0.3 if i in (0, 2, 4) else 0.21) * (0.8 if speaking(tt) else 1.0)
            lyre(tt, note(tok), vel=v, bright=0.62, damp=0.45, t60=1.4, pan=0.3 if i % 2 else -0.2)
        pizz(t, BASS[ch], vel=0.22, t60=0.9, dur=0.9, pan=0.0)
        t += 7 * e8
        k += 1
    lyre(t, 'G2', vel=0.32, bright=0.4)
    pad(M('G2 D3 A3 D4'), c0 - 0.7, S('C03') + 0.6, gain=0.12, att=2.0, rel=1.6, cutoff=1500, sine=0.4)
    pad(M('A4 D5'), c0 - 0.2, S('C03') + 0.4, gain=0.035, att=2.5, rel=1.6, cutoff=3200, voices=1, sine=0.8, detune=3)
    ripples(c0 + 0.5, S('C03') - 0.6, M('G5 A5 B5 D6 E6'), rate=0.6, vel=0.07, bright=0.6)
    tl = W('C01', 'ladino') + 0.05                      # Ladino, Rumca, Bulgarca, Türkçe
    for i in range(8):
        lyre(tl + 0.055 * i, 'B4', vel=0.13 * (1 - 0.06 * i), bright=0.6, t60=0.8, pan=-0.45)
    lyre_line(W('C01', 'rumca') + 0.05, [('D5', 0.09), ('C5', 0.09), ('B4', 0.3)], vel=0.18, bright=0.7, pan=0.45)
    aulos(W('C01', 'bulgarca') + 0.05, [('A4', 0.12), ('G4', 0.1), ('A4', 0.5)], gain=0.28, vib=7, pan=-0.3)
    play(W('C01', 'türkçe') + 0.05, [(note('G4'), 0.1, 1), (note('F4'), 0.1, 1), (note('G4'), 0.4, 1)], kanun,
         vel=0.22, pan=0.3)
    ts = WE('C02', 'filizlendi') + 0.06                 # the ideas sprout: the motif, small and high
    play(ts, kusak('G5', 0.3, 'major', n=4, hold=3), lyre, vel=0.3, bright=0.55, pan=0.2)
    bell(ts + 0.75, 'D6', vel=0.05)
    # C03 "Mektep ... öğretti: sorgulamayı." - the school's ney asks, in Uşşak
    ney(WE('C03', 'sorgulamayı') + 0.05, kusak('D5', 0.4, 'ussak', n=5, vel=0.95, hold=2.2), gain=0.25)
    # --- secrets
    drone('D1 D2', S('C03') - 0.3, c1 + 0.8, gain=0.19, att=2.5, rel=1.2, cutoff=260)
    seq = [(S('C03'), 'G2 D3 Bb3'), (wh, 'D2 A2 F3'), (S('C04'), 'D2 Eb3 A3'), (S('C05'), 'D2 A2 F3'),
           (W('C05', 'ittihat'), 'Bb1 F2 D3'), (S('C06'), 'D2 A2 F3'), (W('C06', 'tutuklanıp'), 'G1 D2 Bb2 Eb3'),
           (W('C06', 'suriyeye'), 'D2 A2 C3 F#3'), (W('C06', 'şamda'), 'D2 A2 F3'), (W('C06', 'vatan'), 'F2 C3 A3')]
    chords(seq, c1 + 0.6, gain=0.1, cutoff=420, att=1.3, rel=1.0)
    SP = dict(C03=['D2 . . A1 . . . .', '. . D2 . . . F2 .'], C04=['D2 . Eb2 . . . D2 .', '. . A1 . Eb2 . . .'],
              C05=['D2 . . A1 . . F2 .', 'D2 . . . . . A1 .'], C06=['D2 . . A1 . . . .', '. . D2 . . . A1 .'])
    t, k = wh + 0.1, 0
    while t < c1 - 0.6:
        for i, tok in enumerate(SP.get(cue_at(t + 1.0), SP['C03'])[k % 2].split()):
            tt = t + i * 0.3
            if tok != '.' and tt < c1 - 0.4:
                pizz(tt, note(tok), vel=0.3, pan=-0.2, t60=0.8, dur=0.8)
        t += 2.4
        k += 1
    heartbeat(wh + 0.3, S('C04'), period=0.95, vel=0.15)
    heartbeat(S('C04'), S('C05'), period=0.78, vel=0.19)
    heartbeat(S('C05'), c1 - 0.5, period=0.88, vel=0.15)
    for wd, ch in [('vatan', 'A4 E5'), ('hürriyet', 'D5 A5')]:          # the forbidden words glow
        t = W('C03', wd)
        pad(M(ch), t - 0.1, t + 2.4, gain=0.05, att=0.5, rel=1.6, cutoff=3200, voices=1, sine=0.75, detune=3)
    bowed(S('C04') - 0.2, [('D2', E('C04') - S('C04') + 0.5, 0.8)], gain=0.2, stack=(0, 1), trem=0.7, att=1.2,
          rel=0.8, cutoff=600, vib=0)
    td = W('C05', 'dört')
    for i, m in enumerate(M('D3 F3 A3 C4')):
        pizz(td + 0.17 * i, m, vel=0.3, t60=0.9, dur=0.9, pan=-0.3 + 0.2 * i)
    brass(M('Bb1 F2 D3'), W('C05', 'ittihat') - 0.3, E('C05') + 0.8, gain=0.12, att=1.5, rel=1.0, bright=0.3)
    ta = W('C06', 'tutuklanıp')
    boom(ta, vel=0.34, f0=60, f1=49.0, decay=0.9)
    fdrum(ta, 'dum', vel=0.36, f0=60)
    ney(W('C06', 'suriyeye') + 0.05, [('A4', 0.45), (hz('Bb4'), 0.2), (hz('C#5'), 0.3), ('D5', 0.3),
                                      (hz('C#5'), 0.2), (hz('Bb4'), 0.25), ('A4', 0.9)], gain=0.22, pan=0.45)
    tv = W('C06', 'arkadaşlarıyla')
    bv = fit(tv, c1 + 0.3, 4.0, 0.42, 0.62)
    bowed(tv, kusak('D3', bv, 'minor', n=4, vel=0.85, hold=2.5), gain=0.24, cutoff=750, vib=5, rel=1.0, accent=0.3)


def sec_1908():
    """1908 (D01-D04): rising energy - string ostinato and frame drum climbing D-F-G-A to 'Meşrutiyet'; the
    dominant holds under '...yeniden ilan edildi' and a bright Bb-major hit answers it: a street band out of a
    'Hürriyet' postcard plays the motif's first major glimpse; a wry pizzicato as the Meclis deposes the sultan
    (D03); D04 reflective: the ney remembers the schools, the informers darken."""
    d0, d1 = sec_span('D')
    peak = W('D02', 'meşrutiyet')                    # the build stops; the dominant holds under the words
    hit = E('D02') + 0.08                            # ...and the Bb-major hit answers "ilan edildi"
    e = 0.25
    t0 = d0 - 0.25
    roots = sorted([(t0, 'D2'), (W('D01', 'ya'), 'Bb1'), (W('D01', 'ya', 1), 'A1'), (S('D02'), 'D2'),
                    (W('D02', 'dağa'), 'F2'), (W('D02', 'sultan'), 'G1'), (W('D02', 'geri'), 'A1')])
    OFF = [12, 12, 0, 12, 12, 0, 12, 7]
    items = []
    for k in range(max(int((peak - 0.08 - t0) / e), 0)):
        tt = t0 + k * e
        r = [note(m) for a, m in roots if a <= tt + 0.05][-1]
        x = (tt - t0) / max(peak - t0, 1.0)
        items.append((r + OFF[k % 8], e, 0.45 + 0.55 * x ** 1.3))
    bowed(t0, items, gain=0.3, stack=(0, 12), cutoff=950, vib=0, att=0.015, accent=0.7, rel=0.15, legato=False)
    mid = t0 + round((S('D02') - t0) / (8 * e)) * 8 * e
    drum_bars(t0, mid, e, ['D . . . D . t .'], vel=0.24, grow=0.4)
    drum_bars(mid, peak - 0.1, e, ['D . . T D . T T'], vel=0.36, grow=0.6)
    timp_roll(peak - 1.6, peak - 0.03, 'A2', 0.08, 0.5)
    timp(peak, 'A2', vel=0.45)
    riser(hit, max(hit - peak, 1.0) + 0.4, vel=0.24, kind='cym')
    bowed(peak - 0.05, [('A3', hit - peak + 0.05, 0.6)], gain=0.16, stack=(0, 4, 7, 12), trem=0.5, att=0.15,
          rel=0.05, cutoff=1800, vib=0)
    seq = [(t0 + 0.3, 'D2 A2 F3 A3'), (W('D01', 'ya'), 'Bb1 F2 D3 F3'), (W('D01', 'ya', 1), 'A1 E2 C#3 E3'),
           (S('D02'), 'D2 A2 F3 A3', dict(cutoff=850)), (W('D02', 'dağa'), 'F2 C3 A3 C4', dict(cutoff=1000)),
           (W('D02', 'sultan'), 'G1 D2 Bb2 D3 G3', dict(cutoff=1150)),
           (W('D02', 'geri'), 'A1 E2 C#3 E3 A3', dict(cutoff=1300))]
    chords(seq, hit + 0.05, gain=0.13, cutoff=700, att=1.0, rel=0.3, sine=0.2)
    # "...ilan edildi." answered by a street band out of a 1908 "Hürriyet" postcard: the motif's first major
    # glimpse (Bb D C F) on a slightly out-of-tune cornet, clarinet, oom-pah, snare and bass drum
    boom(hit, vel=0.55, f0=72, f1=58.27, decay=1.1)
    timp(hit, 'Bb1', vel=0.65)
    bassdrum(hit, vel=0.42)
    cymbal(hit, vel=0.24, decay=1.6)
    strum(hit, M('Bb2 F3 Bb3 D4 F4 Bb4'), vel=0.34, spread=0.018, bright=0.6)
    pad(M('Bb1 F2 Bb2 D3 F3 Bb3 D4'), hit - 0.02, hit + 4.0, gain=0.13, att=0.04, rel=2.6, cutoff=1900, vib=4)
    qb = 0.4
    tune = kusak('Bb4', qb, 'major', n=4, hold=2.5) + [(None, qb, 1.0)]
    band_line(hit, tune, 'cornet', gain=0.3, voices=3, detune=11.0, pan=-0.1)
    aulos(hit, [(None if m is None else m + 12, d, v) for m, d, v in tune], gain=0.1, vib=4, breath=0.03, tilt=0.9,
          bright=0.1, pan=0.3)
    oompah(hit, qb, [(2, 'Bb'), (2, 'F'), (2, 'Bb')], vel=0.9, tuba=0.24, stabs=0.12)
    for k in range(3):
        snare_bar(hit + 2 * k * qb, qb, vel=0.12)
        bassdrum(hit + (2 * k + 1) * qb, vel=0.16)
    # D03 wry pizzicato
    t3 = hit + 6 * qb + 0.1
    e3 = 0.22
    WRY = ['D3 . A2 . D3 C#3 D3 .', 'F3 . C3 . F3 E3 F3 .', 'G3 . D3 . Bb3 A3 G3 .', 'A3 . E3 . A2 . C#3 .']
    run, wink = W('D03', 'tahttan'), W('D03', 'meclis')
    t, k = t3, 0
    while t < S('D04') - 0.4:
        for i, tok in enumerate(WRY[k % 4].split()):
            tt = t + i * e3
            if tok == '.' or tt > S('D04') - 0.4 or run - 0.1 <= tt <= run + 0.9:
                continue
            pizz(tt, note(tok), vel=0.3 * (0.85 if speaking(tt) else 1.0) * (1.1 if i == 0 else 1.0), pan=-0.15,
                 t60=0.5, dur=0.5, bright=0.35)
        t += 8 * e3
        k += 1
    for i, m in enumerate(M('A3 G3 F3 E3 D3')):                     # "tahttan indirdi": down the steps
        pizz(run + 0.09 * i, m, vel=0.3, pan=0.3 - 0.12 * i)
    pizz(run + 0.55, 'D2', vel=0.42, t60=0.9, dur=0.9)
    pizz(wink, 'A4', vel=0.22, bright=0.5)                           # the Meclis he shut deposes him: a wink
    pizz(wink + 0.09, 'D5', vel=0.2, bright=0.5)
    woodtick(wink + 0.09, vel=0.08)
    for wd, m in [('mustafa', 'D4'), ('kazım', 'A4')]:               # two young officers
        pizz(W('D03', wd), m, vel=0.26, bright=0.45, t60=0.9, dur=0.9)
    chords([(t3, 'D3 A3'), (wink, 'G2 D3 Bb3'), (W('D03', 'ordunun'), 'A2 E3 C#4'), (W('D03', 'mustafa'), 'D3 F3 A3')],
           S('D04') + 0.6, gain=0.07, cutoff=700, att=0.8, rel=0.8, sine=0.4)
    # D04 "Okulları açan da, jurnalleri okuyan da aynı sultandı. Bu kuşak, ikisinin arasında yetişti."
    chords([(S('D04'), 'F2 C3 A3 C4'), (W('D04', 'jurnalleri'), 'Eb2 Bb2 G3'), (W('D04', 'aynı'), 'D2 A2 F3'),
            (W('D04', 'bu'), 'Bb1 F2 D3 F3'), (W('D04', 'yetişti'), 'A1 E2 D3 E3')], d1 + 0.4, gain=0.13, cutoff=750,
           att=1.2, rel=1.0, sine=0.4, bass=dict(gain=0.18, stack=(0, 12), cutoff=520, vib=4, att=0.5, rel=0.8))
    ney(WE('D04', 'okulları') + 0.05, kusak('D5', 0.42, 'ussak', n=4, vel=0.9, hold=2.6), gain=0.2)


def sec_savas():
    """Ateşte dövülen kuşak (E01-E06): war, D Phrygian / Hicaz. 'savaş' is a dark hit; war drums and a Hicaz
    string ostinato (E02); a reed lament over a drone for Salonica lost (E03); the motif, minor, in the cellos
    as the narrator speaks of Rumeli lost and a homeland to come (E04); Gallipoli heavy - timpani, low choir,
    artillery, rising strings (E05); E06 empties out and ends on one soft major third: 've birbirleri'."""
    e0, e1 = sec_span('E')
    hit = max(WE('E01', 'savaş'), E('E01')) + 0.05   # the word is said (acoustic end), then the blow
    sel = W('E03', 'selanik')
    tc = WE('E05', 'çanakkale') + 0.08
    tb = W('E06', 'birbirleri')
    drone('D1 D2', e0 - 0.8, hit + 0.2, gain=0.2, att=2.5, rel=0.15)
    bowed(e0 - 0.5, [('D2', hit - e0 + 0.5, 0.9)], gain=0.28, stack=(0, 1), trem=0.75, att=max(hit - e0, 0.5) * 0.8,
          rel=0.06, cutoff=700, vib=0)
    riser(hit, 1.8, vel=0.26)
    boom(hit, vel=1.05, f0=64, f1=36.7, decay=2.0, knock=0.7)
    fdrum(hit, 'dum', vel=0.95, f0=62)
    timp(hit, 'D2', vel=0.9)
    bowed(hit, [('D2', 2.4, 0.5)], gain=0.5, stack=(0, -12, 1), accent=2.2, att=0.01, rel=1.4, cutoff=900, vib=0)
    metal(hit, f0=98, vel=0.3, decay=2.4, ratios=(1, 2.32, 3.87, 5.21, 6.98), click=0.1)
    choir(M('D2 A2 Eb3'), hit, hit + 3.2, gain=0.34, att=0.05, rel=2.2, vowel='o')
    drone('D1 D2 A2', hit, tb + 0.6, gain=0.22, att=0.3, rel=2.5, cutoff=280)
    # E02 Trablusgarp: drums and a Hicaz ostinato
    e = 0.25
    w0, w1 = hit + 1.5, sel - 0.12
    drum_bars(w0, w1, e, ['D . . t D . t .', 'D . . t D t D .'], vel=0.42, grow=0.25)
    HZ = ['D2', 'Eb2', 'F#2', 'Eb2', 'D2', None, 'A1', None]
    nb = max(int((w1 - w0) / e), 0)
    bowed(w0, [(hz(HZ[k % 8]), e, 0.6 + 0.25 * k / max(nb, 1)) for k in range(nb)], gain=0.26, stack=(0, 12),
          cutoff=800, vib=0, att=0.015, accent=0.6, rel=0.2, legato=False)
    chords([(S('E02'), 'D2 A2 F#3 C4'), (W('E02', 'genç'), 'Eb2 Bb2 G3'), (W('E02', 'halkla'), 'D2 A2 F#3 C4'),
            (S('E03'), 'D2 A2 F3 Bb3')], sel + 0.5, gain=0.1, cutoff=650, att=1.0, rel=0.8)
    # E03 the lament (Hicaz on D)
    LAMENT = [('A4', 0.9), (('A4', 'Bb4'), 0.15), ('Bb4', 0.35), ('A4', 0.3), ('G4', 0.4), ('F#4', 0.5), ('Eb4', 0.3),
              ('D4', 1.6), (None, 0.4), ('F#4', 0.4), ('G4', 0.3), ('A4', 0.6), ('Bb4', 0.3), ('A4', 0.25), ('G4', 0.25),
              ('F#4', 0.3), ('Eb4', 0.45), ('D4', 2.2)]
    sc = float(np.clip((S('E04') - 0.15 - sel) / sum(d for _, d in LAMENT), 0.8, 1.3))
    ph = [((hz(m[0]), hz(m[1])) if isinstance(m, tuple) else hz(m), d * sc) for m, d in LAMENT]
    aulos(sel + 0.1, ph, gain=0.22, vib=14, breath=0.05, pan=0.1, tilt=1.05, bright=0.08, att=0.07, rel=0.6,
          hmax=6000.0, top=4500.0)
    pad(M('D3 A3'), sel - 0.3, S('E04') + 1.0, gain=0.07, att=1.5, rel=1.2, cutoff=500, sine=0.5)
    # E04 the narrator's belief: a shared wound -> a homeland to come
    tr = W('E04', 'rumeliyi')
    chords([(S('E04'), 'D2 A2 F3'), (W('E04', 'ortak'), 'Bb1 F2 D3'), (tr, 'G1 D2 Bb2'),
            (W('E04', 'yeni'), 'D2 A2 F3 A3')], S('E05') - 0.2, gain=0.09, cutoff=520, att=1.3, rel=0.9, sine=0.4)
    by = fit(tr, E('E04'), kbeats(5, 2.5), 0.4, 0.62)
    bowed(tr, kusak('D3', by, 'minor', n=5, vel=0.85, hold=2.5), gain=0.28, cutoff=900, vib=6, rel=0.7, accent=0.3)
    # E05 Gallipoli
    riser(tc, min(1.6, max(tc - E('E04'), 0.6)), vel=0.24, kind='cym')
    boom(tc, vel=1.1, f0=60, f1=36.7, decay=2.2, knock=0.8)
    timp(tc, 'D2', vel=1.0)
    fdrum(tc, 'dum', vel=1.0, f0=60)
    choir(M('D2 A2 D3 Eb3'), tc, E('E05') + 1.4, gain=0.25, att=0.08, rel=1.6, vowel='o')
    bowed(tc, [('D2', 2.0, 0.5)], gain=0.48, stack=(0, -12, 7), accent=2.0, att=0.01, rel=1.2, cutoff=900, vib=0)
    e5 = 0.3
    g0, g1 = tc + 4 * e5, E('E05') + 0.3
    drum_bars(g0, g1, e5, ['D . t D D . t .', 'D . t D D t D T'], vel=0.47, grow=0.4)
    HV = ['D2', 'D2', None, 'D2', 'Eb2', None, 'D2', 'C2']
    nb = max(int((g1 - g0) / e5), 0)
    bowed(g0, [(HV[k % 8], e5, 0.65 + 0.3 * k / max(nb, 1)) for k in range(nb)], gain=0.3, stack=(0, 12, -12),
          cutoff=850, vib=0, att=0.015, accent=0.7, rel=0.2, legato=False)
    for wd in ('arıburnunda', 'anafartalarda'):
        thunder(W('E05', wd), vel=0.35)
    ta = W('E05', 'adı')
    s = max(E('E05') - ta, 1.0) / 6
    bowed(ta, [('D3', s), ('Eb3', s), ('F3', s), ('G3', s), ('A3', 2 * s)], gain=0.3, stack=(0, 12), trem=0.45,
          cutoff=1300, vib=6, att=0.2, rel=0.8)
    chords([(tc, 'D2 A2 Eb3'), (ta, 'Bb1 F2 D3'), (W('E05', 'ordunun'), 'C2 G2 Eb3'),
            (W('E05', 'komutana'), 'D2 A2 D3 F3')], E('E05') + 1.2, gain=0.13, cutoff=900, att=0.8, rel=1.0)
    boom(E('E05') + 0.45, vel=0.7, f0=60, f1=36.7, decay=1.8)     # "…komutana dönüştü." tamamen bittikten sonra
    timp(E('E05') + 0.45, 'D2', vel=0.8)
    fdrum(E('E05') + 0.45, 'dum', vel=0.7, f0=60)
    # E06 the fronts, the defeat, and what was left
    for i, wd in enumerate(['kafkasyada', 'irakta', 'filistinde']):
        t = W('E06', wd)
        boom(t, vel=0.36 - 0.06 * i, f0=60, f1=36.7, decay=1.4)
        timp(t, 'D2', vel=0.3 - 0.05 * i)
    ti = W('E06', 'imparatorluk')
    chords([(S('E06'), 'D2 A2 F3'), (W('E06', 'aynı'), 'F2 C3 A3'), (ti, 'Bb1 F2 D3'),
            (W('E06', 'ellerinde'), 'G1 D2 Bb2'), (W('E06', 'tecrübe'), 'A1 E2 A2')], tb + 0.6, gain=0.1, cutoff=600,
           att=1.2, rel=1.0, sine=0.4)
    tn = W('E06', 'aynı')
    k6 = float(np.clip((ti - tn) / 5.0, 0.5, 1.0))
    bowed(tn, [('A3', 1.4 * k6), ('F3', 1.0 * k6), ('E3', 0.8 * k6), ('D3', 1.8 * k6)], gain=0.2, cutoff=900, vib=6,
          rel=0.8)
    bowed(ti, [('D3', 0.8), ('C3', 0.8), ('Bb2', 0.8), ('A2', 2.2)], gain=0.24, stack=(0, -12), cutoff=700, vib=4,
          rel=0.8)
    piano(W('E06', 'tecrübe'), 'D2', vel=0.3)
    piano(W('E06', 'tecrübe') + 0.02, 'A2', vel=0.2)
    piano(E('E06') + 0.12, 'D4', vel=0.25)                                       # "ve birbirleri": a first major third
    piano(E('E06') + 0.46, 'F#4', vel=0.22)
    pad(M('D3 F#3 A3'), tb - 0.15, e1 + 0.2, gain=0.07, att=0.8, rel=1.8, cutoff=900, sine=0.6)
    pad(M('A5'), E('E06') + 0.1, e1 + 0.2, gain=0.022, att=1.0, rel=1.5, cutoff=3000, voices=1, sine=0.9, detune=2)


def sec_anadolu():
    """Anadolu (F01-F06): determination. A steady pulse in D Dorian (low strings, timpani, later frame drum).
    'yalnız değildi' brings in the first held voice, and every name of the cadre adds one more to the chord -
    not one genius, a generation - with a telegraph for Kâzım Karabekir and a solo violin for Halide Edib.
    F05 builds stab by stab (Kongreler, Meclis, Sakarya, Büyük Taarruz), then the motif returns stronger
    (strings + horns) and lands on the hopeful B natural on 'birbirine güvenmeyi'. F06 noble and warm,
    ending on the dominant A."""
    f0, f1 = sec_span('F')
    q = 0.6
    tk = W('F05', 'kongreler')
    tb = W('F05', 'bu')
    pulse_line(f0 - 0.15, tk - 0.2, q, [(f0 - 0.15, 'D2'), (W('F04', 'halide'), 'Bb1'), (W('F04', 'sonra'), 'C2')],
               v0=0.4, v1=0.8, gain=0.3, timp_every=2, tek=S('F03'))
    pad(M('D2 A2 D3'), f0 - 0.4, tk, gain=0.09, att=2.0, rel=0.6, cutoff=500, sine=0.5)
    end = tk + 0.1
    ROLL = [('F01', 'yalnız', 'A3', 'str'), ('F02', 'ali', 'D4', 'horn'), ('F02', 'kazım', 'F4', 'str'),
            ('F03', 'ismet', 'A4', 'reed'), ('F03', 'fevzi', 'D3', 'horn'), ('F04', 'halide', 'C5', 'str')]
    for c, wd, m, kind in ROLL:
        t = W(c, wd)
        if kind == 'str':
            pad([m], t - 0.05, end, gain=0.075, att=0.3, rel=0.5, cutoff=1600, voices=1, vib=5, detune=4)
        elif kind == 'horn':
            brass([m], t - 0.05, end, gain=0.11, att=0.3, rel=0.5, bright=0.5)
        else:
            aulos(t, [(m, end - t, 0.7)], gain=0.16, vib=7, breath=0.06, pan=0.4, att=0.25, rel=0.5)
    # telegraph: ses efektinde, "katıldı"dan sonra (audio/sfx_events.json)
    th = W('F04', 'halide')
    bowed(th, [('E5', 1.0), ('F5', 0.5), ('G5', 0.5), ('A5', 2.0), ('G5', 0.6), ('E5', 1.6)], gain=0.13, voices=1,
          detune=3, cutoff=3400, vib=13, pan=0.3, rel=0.8)
    chords([(W('F04', 'binlerce'), 'Bb2 F3 D4 F4'), (W('F04', 'sonra'), 'C3 G3 E4 G4')], tk + 0.05, gain=0.12,
           cutoff=1300, att=1.0, rel=0.4)
    t = tk - 1.1
    while t < tk - 0.08:                                             # a tek roll into the build
        fdrum(t, 'tek', vel=0.08 + 0.3 * (t - tk + 1.1) / 1.1, f0=230)
        t += 0.065
    # F05 the build: one stab per word
    for wd, ch, v in [('kongreler', 'D2 A2 D3 F3 A3', 0.5), ('meclis', 'F2 C3 F3 A3 C4', 0.6),
                      ('sakarya', 'G2 D3 G3 B3 D4', 0.72), ('büyük', 'A1 E2 A2 C#3 E3 A3', 0.9)]:
        t = WE('F05', 'taarruz') + 0.03 if wd == 'büyük' else W('F05', wd)
        ns = M(ch)
        timp(t, ns[0] if ns[0] >= note('C2') else ns[0] + 12, vel=v)
        fdrum(t, 'dum', vel=0.8 * v, f0=66)
        brass(ns[1:], t - 0.02, t + 1.5, gain=0.24 * v, att=0.03, rel=1.0, bright=0.85)
        pad(ns, t - 0.02, t + 1.7, gain=0.2 * v, att=0.03, rel=1.1, cutoff=1700)
        boom(t, vel=0.55 * v, f0=66, f1=float(mtof(24 + ns[0] % 12)), decay=1.0)
    ta = WE('F05', 'taarruz') + 0.03
    pad(M('A1 E2 A2 C#3 E3'), ta, tb + 0.1, gain=0.15, att=0.05, rel=0.3, cutoff=1300)
    timp_roll(ta + 0.3, tb - 0.03, 'A2', 0.1, 0.45)
    riser(tb, min(1.6, max(tb - ta, 0.6)), vel=0.22, kind='cym')
    # the motif, stronger: its last note (B natural) on "birbirine güvenmeyi"
    tg = E('F05') + 0.05
    bm = 0.58
    tm = tg - 5 * bm
    if tm < tb:
        tm, bm = tb, fit(tb, tg, 5.0, 0.42, 0.62)
    mel = kusak('D4', bm, 'dorian', n=6, vel=0.95, sixth=True, hold=1.3)
    on = onsets(tm, mel)
    tail = on[5] + 1.3 * bm
    if tm - tb > 0.8:                                                # the cadre at work before the tune
        pulse_line(tb, tm, bm, [(tb, 'D2')], v0=0.6, v1=0.75, gain=0.28, timp_every=2, tek=tb)
        pad(M('D2 A2 D3 F3'), tb - 0.05, tm + 0.3, gain=0.14, att=0.2, rel=0.4, cutoff=1100)
    bowed(tm, mel[:5], gain=0.36, stack=(0,), cutoff=1400, vib=8, accent=0.35, rel=0.3)
    bowed(on[5], mel[5:], gain=0.42, stack=(0, 12), cutoff=1900, vib=8, accent=0.35, rel=0.6)
    bowed(tm, mel, gain=0.26, stack=(-12,), cutoff=1300, vib=4, accent=0.5, rel=1.0, bus=BRASS)
    seq = [(on[0], 'D2 A2 D3 F3'), (on[2], 'C2 G2 C3 E3'), (on[3], 'F2 C3 F3 A3'), (on[4], 'C2 G2 C3 E3'),
           (on[5], 'G2 D3 G3 B3')]
    chords(seq, tail + 0.3, gain=0.17, cutoff=1500, att=0.3, rel=0.6, lead=0.05, ov=0.3)
    pulse_line(tm, tail, bm, [(o, M(c)[0]) for o, c in seq], v0=0.75, v1=0.95, gain=0.3, timp_every=2, tek=tm)
    cymbal(on[5], vel=0.15, decay=1.8)
    # F06 "Kuşak hazırdı. Onu tek bir hedefte birleştiren ise Mustafa Kemal'in dehası oldu."
    seq = [(S('F06'), 'F2 C3 A3 C4'), (W('F06', 'onu'), 'Bb1 F2 D3 F3'), (W('F06', 'mustafa'), 'G1 D2 Bb2 F3'),
           (W('F06', 'dehası'), 'A1 E2 D3 E3'), (WE('F06', 'oldu'), 'A1 E2 C#3 E3')]
    chords(seq, f1 + 0.7, gain=0.15, cutoff=1000, att=1.0, rel=1.2, sine=0.3,
           bass=dict(gain=0.22, stack=(0, 12), cutoff=620, vib=5, att=0.5, rel=1.0))
    brass(M('F3 A3 C4'), S('F06') - 0.3, W('F06', 'onu') + 0.5, gain=0.1, att=1.2, rel=0.9, bright=0.45)
    brass(M('F3 Bb3 D4'), W('F06', 'onu') - 0.3, W('F06', 'dehası') + 0.4, gain=0.1, att=0.9, rel=0.9, bright=0.45)
    pulse_line(S('F06') - 0.2, W('F06', 'onu'), 2 * q, [(S('F06'), 'F2')], v0=0.55, v1=0.4, gain=0.22, timp_every=1)


def sec_kapanis():
    """Kapanış (G01-G06) + end screen. 29 October, evening: a hush on an A pedal and the clock of the first
    scene; one chime for half past eight; the hall rises (choir, tremolo strings, timpani roll); a breath
    holds 'Yaşasın Cumhuriyet!'; the climax answers it: the motif complete in D major (strings, horns, choir,
    bells, trumpets; D-A-G-D). G02 the parade passes (soft oom-pah), G03-G04 reflective piano (a tick for the
    school desk, a far drum for the trench), G05 the motif asks again and hangs on the dominant seventh, G06
    solemn, then a warm IV-V-I with a brass band approaching under the words; the end screen is an original
    brass-band march made of the motif and closes on D major."""
    g0, _ = sec_span('G')
    ya = W('G01', 'yaşasın')
    top = WE('G01', 'cumhuriyet')
    tmc = W('G01', 'meclis')
    drone('A1 A2', g0 - 0.7, ya + 0.05, gain=0.15, att=1.5, rel=0.08, cutoff=280)
    pad(M('A2 E3 A3'), g0 - 0.5, tmc + 0.6, gain=0.07, att=1.5, rel=1.0, cutoff=600, sine=0.4)
    clock(g0 + 0.15, tmc - 0.1, period=1.0, vel=0.1)
    tbu = WE('G01', 'buçukta')
    bell(W('G01', 'mecliste') - 0.75, 'A5', vel=0.12, decay=3.0, pan=0.35)
    bell(W('G01', 'mecliste') - 0.75, 'A4', vel=0.07, decay=3.5, pan=0.35)
    build = max(ya - tmc + 0.25, 0.8)
    choir(M('A2 E3 A3 C#4 E4'), ya - build, ya + 0.05, gain=0.34, att=build * 0.9, rel=0.07, vowel='a')
    bowed(ya - build, [('A2', build, 1.0)], gain=0.34, stack=(0, 7, 12, 16), trem=0.6, att=build * 0.85, rel=0.05,
          cutoff=1500, vib=0)
    timp_roll(ya - min(1.8, build), ya - 0.03, 'A2', 0.08, 0.5)
    snare_roll(ya - min(1.6, build), ya - 0.03, 0.03, 0.2)
    riser(ya, min(2.0, build + 0.3), vel=0.3, kind='cym')
    # the climax (master_gain() holds the breath before it)
    T = max(top, E('G01')) + 0.05                   # after the acoustic end of "Cumhuriyet!"
    B = fit(T, S('G02') - 0.85, 5.0, 0.46, 0.54)     # the summit (D') lands before G02 when the gap allows
    mel = kusak('D4', B, 'major', n=6, vel=1.0, hold=4)
    on = onsets(T, mel)
    L = kbeats(6, 4) * B
    boom(T, vel=1.0, f0=72, f1=36.7, decay=2.0, knock=0.45)
    timp(T, 'D2', vel=1.0)
    timp(T + 0.012, 'A2', vel=0.55)
    fdrum(T, 'dum', vel=0.65, f0=70)
    cymbal(T, vel=0.42, decay=3.2)
    strum(T, M('D2 A2 D3 F#3 A3 D4 F#4'), vel=0.55, spread=0.02, bright=0.6)
    seq = [(on[0], 'D2 A2 D3 F#3 A3'), (on[2], 'A1 E2 A2 C#3 E3'), (on[4], 'G1 D2 G2 B2 D3'),
           (on[5], 'D2 A2 D3 F#3 A3 D4')]
    chords(seq, T + L + 2.8, gain=0.23, cutoff=3200, att=0.06, rel=1.5, lead=0.03, ov=0.3, vib=4)
    CH = ['D3 A3 D4 F#4', 'C#3 A3 C#4 E4', 'B2 G3 B3 D4', 'D3 A3 D4 F#4 A4']
    for i, (t0, _) in enumerate(seq):
        last = i + 1 == len(seq)
        t1 = T + L + 2.8 if last else seq[i + 1][0] + 0.25
        choir(M(CH[i]), t0 - 0.03, t1, gain=0.4, att=0.12 if i == 0 else 0.25, rel=1.5 if last else 0.4, vowel='a')
        brass(M(CH[i])[:3], t0 - 0.02, t1, gain=0.12, att=0.08, rel=1.4 if last else 0.4, bright=0.7)
    bowed(T, mel, gain=0.5, stack=(0, 12), cutoff=3400, vib=10, accent=0.35, rel=1.6)
    bowed(T, mel, gain=0.34, stack=(-12,), cutoff=1500, vib=4, accent=0.5, rel=1.3, bus=BRASS)
    band_line(T, mel, 'trumpet', gain=0.32, voices=2, pan=0.15, gap=0.04)
    bassdrum(T, vel=0.4)
    play(T, mel, bell, vel=0.15, oct=12)
    play(T, mel, lyre, vel=0.42, bright=0.6)
    for i, (t0, c) in enumerate(seq[:3]):
        arp(t0, seq[i + 1][0], M(c)[1:], [0, 1, 2, 3, 2, 1], B / 2, vel=0.22, thin=False, bright=0.5)
    timp(on[2], 'A2', vel=0.65)
    timp(on[4], 'G2', vel=0.65)
    timp(on[5], 'D2', vel=0.75)
    boom(on[5], vel=0.4, f0=70, f1=36.7, decay=1.4, knock=0.25)
    cymbal(on[5], vel=0.18, decay=3.0)
    for dt, m, v in [(0.0, 'D5', 0.18), (0.03, 'A5', 0.13), (0.06, 'D6', 0.11), (0.7, 'F#5', 0.07), (1.4, 'A5', 0.06)]:
        bell(on[5] + dt, m, vel=v, decay=4.0, pan=rng.uniform(-0.4, 0.4))
    # G02 the parade passes under the facts: a soft oom-pah on the climax's beat, receding before G03
    after = T + L
    CHD = dict(D='D2 A2 D3 F#3 A3', G='G1 D2 B2 D3 G3', Bm='B1 F#2 B2 D3 F#3', A='A1 E2 A2 C#3 E3')
    bed = [(after, 'D')] + [(t, c) for t, c in [(W('G02', 'ertesi'), 'G'), (W('G02', 'genelkurmayda'), 'Bm'),
                                                (W('G02', 'üçü'), 'A')] if t > after + 0.8]
    end_bed = S('G03') - 0.3
    beats = []                                       # chord per beat on the climax's grid
    t = after
    while t < end_bed - B:
        beats.append([c for t0, c in bed if t0 <= t + 0.1][-1])
        t += B
    if beats:
        plan = []
        for c in beats:
            if plan and plan[-1][1] == c:
                plan[-1][0] += 1
            else:
                plan.append([1, c])
        nb = len(beats)
        oompah(after, B, plan, vel=0.8, tuba=0.15, stabs=0.07)
        for k in range(0, nb, 2):
            bassdrum(after + k * B, vel=0.12 * (1 - 0.6 * k / nb))
    for i, (t0, c) in enumerate(bed):
        t1 = bed[i + 1][0] if i + 1 < len(bed) else S('G03')
        if t1 - t0 >= 0.4:
            pad(M(CHD[c])[1:], t0 - 0.2, t1 + 0.7, gain=0.11, att=0.8, rel=0.9, cutoff=1100, sine=0.3)
    tu = W('G02', 'üçü')                                            # "Üçü de...": three small bells
    for i, m in enumerate(['D6', 'F#6', 'A6']):
        bell(tu + 0.18 * i, m, vel=0.07, decay=2.2, pan=-0.3 + 0.3 * i)
    # G03-G04 reflective piano
    PV = dict(Bm='B2 F#3 B3 D4', Gm='G2 D3 Bb3 D4', D='D3 A3 D4 F#4', G='G2 D3 G3 B3', A='A2 E3 A3 C#4',
              DF='F#2 D3 A3 D4', Em='E2 B2 D3 G3', As='A2 E3 A3 D4')
    PD = dict(Bm='B1 F#2 B2 D3', Gm='G1 D2 G2 Bb2', D='D2 A2 D3 F#3', G='G1 D2 G2 B2', A='A1 E2 A2 C#3',
              DF='F#1 D2 A2 D3', Em='E2 B2 D3 G3', As='A1 E2 A2 D3')
    g5 = S('G05')
    plan = [(S('G03'), 'Bm', 0.36), (W('G03', 'muhalefete'), 'Gm', 0.36), (W('G03', 'ama'), 'D', 0.36),
            (W('G03', 'bir'), 'G', 0.36), (W('G03', 'siperden'), 'A', 0.36), (S('G04'), 'G', 0.72),
            (W('G04', 'otuz'), 'DF', 0.72), (W('G04', 'bugün'), 'Em', 0.72), (W('G04', 'yazılır'), 'As', 0.72)]
    plan.sort(key=lambda x: x[0])
    for i, (t0, c, st) in enumerate(plan):
        t1 = plan[i + 1][0] if i + 1 < len(plan) else g5
        arp(t0, t1, M(PV[c]), [0, 1, 2, 3, 2, 1], st, inst='piano', vel=0.26 if st < 0.5 else 0.21, thin=True)
    chords([(t, PD[c]) for t, c, _ in plan], g5 + 0.5, gain=0.08, cutoff=800, att=1.2, rel=1.0, sine=0.5, lead=0.2)
    woodtick(W('G03', 'okul'), vel=0.07, pitch=0.9)                 # "bir okul sırasından"
    fdrum(W('G03', 'siperden'), 'dum', vel=0.16, f0=58)              # "ve bir siperden"
    # G05 the question: the motif hangs on G over A7
    t5 = S('G05') + 0.25
    bq = fit(t5, W('G05', 'yorumlara') - 0.25, 4.0, 0.5, 0.85)
    qm = kusak('D4', bq, 'major', n=5, hold=3)
    on = onsets(t5, qm)
    play(t5, qm, piano, vel=0.28)
    piano(t5, 'G2', vel=0.2)
    piano(on[2], 'A2', vel=0.18)
    chords([(S('G05'), 'G2 D3 B3'), (on[2], 'A2 E3 C#4'), (on[4], 'A2 E3 G3 C#4')], S('G06') + 0.6, gain=0.1,
           cutoff=850, att=1.0, rel=0.9, sine=0.5, lead=0.2)
    # G06 "Atatürk'ü ve onun kuşağını saygıyla anıyoruz." solemn; "Cumhuriyetimizin ... kutlu olsun." warm cadence
    tcm, ty = W('G06', 'cumhuriyetimizin'), W('G06', 'yılı')
    chords([(S('G06'), 'B1 F#2 A2 D3'), (W('G06', 'kuşağını'), 'E2 B2 D3 G3'), (tcm, 'G1 D2 G2 B2 D3'),
            (ty, 'A1 E2 A2 C#3 G3')], E('G06') + 0.4, gain=0.14, cutoff=1000, att=0.9, rel=0.6, sine=0.35)
    choir(M('B2 D3 F#3'), S('G06') - 0.2, tcm + 0.2, gain=0.1, att=1.2, rel=0.5, vowel='u')
    choir(M('G3 B3 D4'), tcm - 0.3, ty + 0.2, gain=0.13, att=0.8, rel=0.4, vowel='a')
    choir(M('A3 C#4 E4 G4'), ty - 0.1, E('G06') + 0.25, gain=0.14, att=0.4, rel=0.35, vowel='a')
    # end screen: the kuşak motif becomes an original brass-band march (2/4, D major): soft under
    # "Cumhuriyetimizin yüz üçüncü yılı kutlu olsun", open after it. Strain = the complete motif (4 bars) and
    # its mirror falling home (4 bars: 8 6 7 5 | 4 2 1); then the whole band holds D major.
    T2 = E('G06') + 0.05
    tail = DUR - T2
    if tail > 8.0:
        q = float(np.clip((DUR - 4.8 - T2) / 16, 0.46, 0.58))
        nb = 2 * int((T2 - tcm) / (2 * q))           # whole bars of lead-in under the words
        if nb >= 2:
            t0 = T2 - nb * q
            tub = []
            for k in range(nb):
                key = 'G' if t0 + k * q < ty else 'A7'
                tub.append((BANDCH[key][k % 2], q, 0.7 + 0.3 * k / nb))
            band_line(t0, tub, 'tuba', gain=0.16, gap=0.16)
            for k in range(0, nb - 2, 2):
                snare_bar(t0 + k * q, q, vel=0.05 + 0.08 * k / nb, pat='a . t . a . t t')
                bassdrum(t0 + k * q, vel=0.1)
            snare_roll(T2 - 2 * q, T2 - 0.02, 0.04, 0.2)
        mel = kusak('D4', q, 'major', n=6, hold=3) + [(None if m is None else note(m), d * q, 1.0) for m, d in
               [('D5', 1), ('B4', 1), ('C#5', 0.5), ('A4', 1.5), ('G4', 1), ('E4', 1), ('D4', 1), (None, 1)]]
        band_line(T2, mel, 'cornet', gain=0.38, voices=3, detune=5.0, pan=-0.12)
        band_line(T2, mel, 'trumpet', gain=0.18, voices=2, pan=0.12, gap=0.04)
        aulos(T2, [(None if m is None else m + 12, d, v) for m, d, v in mel], gain=0.11, vib=3, breath=0.03,
              tilt=0.9, bright=0.1, pan=0.3)                                    # clarinets, an octave up
        play(T2, mel, bell, vel=0.05, oct=24, decay=1.2)                     # glockenspiel
        oompah(T2, q, [(2, 'D'), (2, 'A'), (1, 'G'), (3, 'D'), (2, 'G'), (2, 'A'), (2, 'A7'), (2, 'D')],
               vel=1.0, tuba=0.38, stabs=0.19)
        for k in range(8):
            tb_ = T2 + 2 * k * q
            if k in (3, 7):
                snare_bar(tb_, q, vel=0.19, pat='A . t t . . . .')
                snare_roll(tb_ + q, tb_ + 2 * q - 0.02, 0.06, 0.24 if k == 7 else 0.15)
            else:
                snare_bar(tb_, q, vel=0.19)
            bassdrum(tb_, vel=0.36)
            bassdrum(tb_ + q, vel=0.24)
        cymbal(T2, vel=0.22, decay=0.9)
        cymbal(T2 + 8 * q, vel=0.17, decay=0.9)
        pad(M('D3 A3 D4 F#4'), T2 - 0.1, T2 + 16 * q, gain=0.07, att=0.6, rel=1.0, cutoff=1200, sine=0.4)
        F = T2 + 16 * q
        for kind, ns, gn in [('trumpet', 'D5 F#5', 0.12), ('cornet', 'A4 D5', 0.17), ('trombone', 'D3 A3 F#4', 0.15),
                             ('tuba', 'D2', 0.32)]:
            for m in ns.split():
                band_line(F, [(m, 2.8, 1.0)], kind, gain=gn, gap=1.1, voices=2)
        bassdrum(F, vel=0.46)
        cymbal(F, vel=0.28, decay=1.8)
        timp(F, 'D2', vel=0.45)
    else:                                            # too short a tail for the march: a plain cadence
        timp(T2, 'D2', vel=0.35)
        F = T2 + 0.3
        strum(F, M('D2 A2 D3 F#3 A3 D4 F#4'), vel=0.4, spread=0.04, bright=0.45)
    pad(M('D2 A2 D3 F#3 A3 E4'), F - 0.2, DUR + 0.3, gain=0.15, att=0.6, rel=max(DUR - F, 1.0) * 0.6, cutoff=1300,
        sine=0.4)
    choir(M('D3 A3 F#4'), F, DUR + 0.3, gain=0.15, att=1.0, rel=max(DUR - F, 1.0) * 0.6, vowel='a')
    drone('D1 D2', F - 0.2, DUR + 0.3, gain=0.11, att=0.6, rel=max(DUR - F, 1.0) * 0.6, cutoff=240)
    bell(F + 0.05, 'D6', vel=0.1, decay=3.5)
    bell(F + 0.6, 'A5', vel=0.09, decay=3.5, pan=0.3)
    bell(F + 1.2, 'F#5', vel=0.07, decay=3.5, pan=-0.3)


SECTION_FUNCS = [('A', sec_acilis), ('B', sec_okullar), ('C', sec_selanik), ('D', sec_1908), ('E', sec_savas),
                 ('F', sec_anadolu), ('G', sec_kapanis)]


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


# lines that must cut through: the thesis, the narrator's own comments ("Bana kalırsa", "Bence"), the whisper
PRIORITY = {'A05': 1.5, 'B05': 1.25, 'C02': 1.2, 'C03': 1.4, 'E04': 1.25, 'G04': 1.3, 'G05': 1.35, 'G06': 1.15,
            'D02': 1.2, 'E05': 1.4, 'G02': 1.7, 'F05': 1.3, 'E03': 1.3, 'G01': 1.25, 'E01': 1.3, 'C06': 1.2, 'D03': 1.25,
            'F04': 1.2, 'D04': 1.2}       # + the hottest musical moments that run under words (ses kurulu: kelime başına ölçüm)
HUSH = 0.16                     # music level while "Yaşasın Cumhuriyet!" is spoken (the climax answers it)
TAIL_DB = 0.0                   # end-screen trim (dB); the march is composed to sit below the climax


def speech_mask():
    """Smoothed 'narration present' curve on a 10 ms grid (timeline.js CUES, refined with vo.wav).
    1.0 = normal duck; key lines (PRIORITY) duck deeper."""
    hop = 0.01
    tg = np.arange(0, DUR + 1.0, hop)
    act = np.zeros(len(tg), bool)
    weight = np.ones(len(tg))
    for c, (a, b) in CUE.items():
        on = (tg >= a - 0.06) & (tg <= b + 0.2)          # cümle sonu kuyruğu korunur
        act |= on
        weight[on] = np.maximum(weight[on], PRIORITY.get(c, 1.0))
    used_vo = False
    if VO_PATH.exists():
        vo, vsr = read_vo(VO_PATH)
        h = int(hop * vsr)
        k = len(vo) // h
        rms = np.sqrt(np.mean(vo[:k * h].reshape(k, h) ** 2, 1) + 1e-12)
        db = 20 * np.log10(rms)
        on = binary_dilation(db > -48.0, np.ones(13, bool))
        act[:min(k, len(act))] |= on[:len(act)]
        used_vo = True
    act = binary_closing(act, np.ones(int(0.6 / hop), bool))
    x = act * weight
    ra, rr = np.exp(-hop / 0.10), np.exp(-hop / 0.5)
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


def read_vo(path):
    """Mono float narration and its sample rate (16/24/32-bit PCM wav; soundfile for anything else)."""
    try:
        with wave.open(str(path)) as w:
            ch, sw, fs = w.getnchannels(), w.getsampwidth(), w.getframerate()
            raw = w.readframes(w.getnframes())
        if sw == 2:
            x = np.frombuffer(raw, '<i2').astype(np.float32) / 32768.0
        elif sw == 3:
            b = np.frombuffer(raw, np.uint8).reshape(-1, 3)
            x = ((b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int32) << 16))
                 << 8 >> 8).astype(np.float32) / 8388608.0
        elif sw == 4:
            x = np.frombuffer(raw, '<i4').astype(np.float32) / 2147483648.0
        else:
            raise wave.Error(f'{sw * 8}-bit')
    except wave.Error:
        import soundfile as sf
        x, fs = sf.read(str(path), dtype='float32', always_2d=True)
        return x.mean(1), fs
    return (x.reshape(-1, ch).mean(1) if ch > 1 else x), fs


def duck_depth(freqs, scale=1.0):
    """How many dB each frequency is pulled down while narration is present."""
    pts_f = np.log2([20, 110, 220, 3800, 6500, 24000])
    pts_d = np.array([3.0, 3.0, 9.0, 9.0, 5.0, 5.0]) * scale
    return np.interp(np.log2(np.maximum(freqs, 20)), pts_f, pts_d)


def master_eq(freqs):
    """Static master EQ applied inside the STFT: 35 Hz high-pass (removes DC), a gentle low shelf (-5 dB at
    40 Hz, -1.5 dB at 150 Hz: the drones stay felt but leave room under the voice) and a 13.5 kHz low-pass."""
    f = np.maximum(freqs, 1e-3)
    shelf = 0.5 + 0.5 * f ** 2 / (f ** 2 + 110.0 ** 2)
    return shelf / np.sqrt(1 + (35 / f) ** 8) / np.sqrt(1 + (f / 13500) ** 8)


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
    """The held breath under "Yaşasın Cumhuriyet!", the end-screen trim and the final fade (5 ms grid)."""
    tg = np.arange(0, n / SR + 0.01, 0.005)
    g = np.ones(len(tg))
    a, b = W('G01', 'yaşasın') - 0.06, max(WE('G01', 'cumhuriyet'), E('G01')) + 0.01
    if b - a > 0.3:
        g = np.minimum(g, np.interp(tg, [a, a + 0.09, b - 0.04, b], [1.0, HUSH, HUSH, 1.0], left=1.0, right=1.0))
    g *= np.interp(tg, [E(ORDER[-1]) - 0.6, E(ORDER[-1]) + 0.6], [1.0, 10 ** (TAIL_DB / 20)])
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




# =============================================================================== cues.md
INTENT = {
    'A': 'Ankara, 28 Ekim 1923 gecesi. Keçe piyano, alçak yaylılar, duvar saati (A04 boyunca azalır). "Yarın '
         'Cumhuriyet ilan edeceğiz!"den sonra kuşak motifi piyanoda kırılgan: Re minör, 1-3-2-5, açık biter, '
         'Cumhuriyet\'i kuran kadroya bağlanır. A05 "…değil" nefesinde Fa majöre küçük yükseliş; motif ilk kez '
         'majörde (yine 4 nota).',
    'B': 'Re Uşşak (segâh ≈ 160 cent). Kanun ostinatosu, ney cümleleri, okul saati tıkırtısı, el zili, hafif bendir; '
         'B03 en canlı yer. B01 "Meclis\'i süresiz tatil etti" kararır ve seyrekleşir. B05 (anlatıcının yorumu) '
         'inceltilir: seyrek kanun, tıkırtı/davul yok. "Kemal"den sonra ney Sol\'e iner: limanın tonu.',
    'C': 'C01-C02 açık liman: Sol miksolidyen, 7/8 (2+2+3) çekme telli, hafif pad, su damlaları; dört dile birer '
         'küçük renk. C02 (anlatıcının yorumu) inceltilir; "filizlendi"den sonra motif küçük ve yüksek filizlenir. '
         'C03 "sorgulamayı": okulun neyi motifle sorar (Uşşak, 1-3-2-5-4). "Manastır\'da"dan itibaren sır: alçak '
         'Re drone, seyrek pizzicato, boğuk kalp atışı; fısıltıdaki "vatan… hürriyet…" parlar. C04 hafiyeler: Mi '
         'bemol, tremolo, daha hızlı nabız. C05 dört öğrenciye dört nota. C06 tutuklanma (boğuk vuruş), sürgün '
         '(Hicaz ney), "arkadaşlarıyla"da motif viyolonsellerde (minör).',
    'D': 'Yükselen enerji: yaylı ostinato + def, bas Re-Fa-Sol-La tırmanır, timpani tremolosu ve ters zil. '
         '"Meşrutiyet"te yükseliş durur, La asılı kalır; "ilan edildi"nin ardından parlak Si bemol majör vuruş (henüz '
         '"ev" değil): '
         '"Hürriyet" kartpostalından çıkmış bir sokak bandosu (hafif akortsuz kornet, klarnet, tuba, trampet) '
         'motifin ilk majör görünüşünü çalar. D03 alaycı pizzicato: "Meclis" göz kırpar, "tahttan indirdi"de basamak basamak iniş, iki subaya iki nota. '
         'D04 düşünceli: "Okulları" ney motifi hatırlar, "jurnalleri" kararır.',
    'E': '"savaş" söylenir, ardından karanlık vuruş (boom, timpani, Frigyen yaylılar, alçak koro). E02 savaş davulları + Hicaz '
         'ostinatosu. E03 "Selanik": davullar susar; drone üstünde kamış ağıt (Hicaz). E04 anlatıcının inancı, '
         'ince; "Rumeli\'yi kaybeden"de motif minörde viyolonsellerde. E05 "Çanakkale." sözünün ardından ağır ve yoğun (timpani, '
         'alçak koro "o", top sesleri, yükselen yaylılar). E06 cepheler uzak gümbürtüler; yenilgi; "tecrübe…" tek '
         'piyano notası; "ve birbirleri" tek, yumuşak bir majör üçlü ile sessizce biter.',
    'F': 'Kararlılık: Re dorian sabit nabız (alçak yaylılar, timpani, F03\'ten itibaren def). "yalnız değildi" ilk '
         'tutulan sesi getirir; kadrodaki her isim akora bir ses daha ekler (Ali Fuat, Kâzım Karabekir [telgraf], '
         'İsmet, Fevzi Paşa; Halide Edib için solo keman): tek dâhi değil, bir kuşak. F05 her kelimede büyüyen '
         'vuruşlar (Kongreler, Meclis, Sakarya, Büyük Taarruz), sonra motif güçlenerek döner (yaylılar + kornolar), '
         'son notası umutlu Si natürel "birbirine güvenmeyi" üstüne. F06 "Kuşak hazırdı": asil ve sıcak; La '
         '(dominant) üstünde biter.',
    'G': 'G01: La pedalında sessizlik, ilk sahnenin saati; "buçukta" tek saat çanı; "Meclis\'te sesler yükseldi" '
         'koro, tremolo ve timpani ile yükselir; "Yaşasın Cumhuriyet!" nefes tutulmuş bir sessizlikte duyulur; doruk '
         'ona cevap verir: motif ilk kez TAM, Re majör (yaylılar, kornolar, trompet, koro, çanlar; Re-La-Sol-Re). G02 bayram '
         'yatağı: bando geçip gider (yumuşak tuba ve trombon "um-pa"; "Üçü de" üç küçük çan). G03-G04 düşünceli piyano ("muhalefete" kararır; okul sırası için bir '
         'tıkırtı, siper için uzak bir davul). G05 soru: motif La7 üstünde Sol\'de asılı kalır. G06 önce saygı '
         '(Si minör, koro "u"), sonra "Cumhuriyetimizin…" sıcak IV-V-I; sözün altında bando uzaktan yaklaşır '
         '(kısık trampet ve tuba). Bitiş ekranı: motiften türeyen ÖZGÜN bando marşı (2/4, Re majör; kornet, '
         'trompet, klarnet, trombon, tuba, trampet, büyük davul, zil, glokenşpil): motif tam (4 ölçü) + aynası '
         '(8-6-7-5 | 4-2-1, 4 ölçü), sonra bütün bando Re majörde tutar ve söner. Hiçbir marştan alıntı ya da '
         'benzetme yoktur.',
}


def write_cues_md(path):
    def ts(t):
        return f'{int(t // 60)}:{t % 60:05.2f} ({t:.2f})'

    L = ['# Müzik işaretleri (cumhuriyet)', '',
         f'Bu dosyayı `audio/score.py` her çalıştığında `timeline.js`ten yeniden yazar; elle düzenleme kaybolur.',
         f'Zaman çizelgesi: {"GEÇİCİ tahmin (fake_timeline.py)" if PROVISIONAL else "gerçek seslendirme (build_vo.py)"}. '
         f'Toplam süre {ts(DUR)}; anlatım {ts(E(ORDER[-1]))} sn\'de biter, sonrası bitiş ekranı müziği.', '',
         '## Kuşak motifi', '',
         'Gam basamakları 1-3-2-5-4-8, ritim 1-1-½-1½-1-3 vuruş: ileri adım, geri yaslanma, yine ileri. Hiçbir marşı '
         '(İstiklal, İzmir, Onuncu Yıl, Ceddin Deden, Harbiye, mehter) alıntılamaz.', '',
         '| Biçim | Notalar | Nerede |', '|---|---|---|',
         '| kırılgan | 1-3-2-5 | A02 sonu (Re minör, piyano), A05 (Fa majör, piyano), C02 (Sol majör, lir), D02 (Si♭ majör), C06 (minör, viyolonsel), D04 (Uşşak, ney) |',
         '| büyüyen | 1-3-2-5-4 | C03 "sorgulamayı" (Re Uşşak, ney), E04 (minör, viyolonsel), G05 (majör, piyano; soru) |',
         '| güçlü | 1-3-2-5-4-6 | F05 (Re dorian, yaylılar + kornolar; Si natürel) |',
         '| tam | 1-3-2-5-4-8 | G01 doruk (Re majör; yaylılar, kornolar, trompet, koro, çanlar) |',
         '| bando | 1-3-2-5-4-8 + 8-6-7-5-4-2-1 | bitiş ekranı marşı (2/4, Re majör); D02 sonrası 1908 sokak bandosu (Si♭, 4 nota) |', '',
         '## Bölümler', '', '| Bölüm | Cümleler | Başlangıç - bitiş | Müzik |', '|---|---|---|---|']
    for letter, name, ids in SECTIONS:
        a, b = sec_span(letter)
        if letter == SECTIONS[0][0]:
            a = 0.0
        L.append(f'| {name} | {ids[0]}-{ids[-1]} | {ts(a)} - {ts(b)} | {INTENT.get(letter, "")} |')
    L += ['', '## Vuruş anları (kelimeye bağlı)', '']
    for t, what in sorted([
            (E('A02') + 0.1, 'A02 sonu: motif piyanoda kırılgan (Re minör)'),
            (WE('A05', 'değil'), 'A05 "…değil" nefesi: Fa majöre yükseliş'),
            (S('B01') - 0.4, 'B başı: okul el zili, kanun'),
            (W('C01', 'ladino'), 'C01 diller: Ladino, Rumca, Bulgarca, Türkçe'),
            (WE('C02', 'filizlendi'), 'C02 "filizlendi": motif filizlenir'),
            (W('C03', 'sorgulamayı'), 'C03 "sorgulamayı": ney motifle sorar (Uşşak)'),
            (W('C03', 'manastırda'), 'C03 "Manastır\'da": sırlar başlar'),
            (W('D02', 'meşrutiyet'), 'D02 "Meşrutiyet": yükseliş durur, La (dominant) asılı kalır'),
            (E('D02'), 'D02 "ilan edildi" biter: Si♭ majör vuruş + 1908 sokak bandosu'),
            (WE('E01', 'savaş'), 'E01 "savaş" biter: karanlık vuruş'),
            (W('E03', 'selanik'), 'E03 "Selanik": davullar susar, ağıt'),
            (WE('E05', 'çanakkale'), 'E05 "Çanakkale." biter: ağır vuruş'),
            (W('E06', 'birbirleri'), 'E06 "birbirleri": tek majör üçlü, sessizlik'),
            (W('F05', 'kongreler'), 'F05 vuruşlar: Kongreler / Meclis / Sakarya / Büyük Taarruz'),
            (W('F05', 'birbirine'), 'F05 "birbirine güvenmeyi": motifin Si natürel notası'),
            (WE('G01', 'buçukta'), 'G01 "buçukta": saat çanı'),
            (W('G01', 'yaşasın'), 'G01 "Yaşasın": müzik nefesini tutar'),
            (WE('G01', 'cumhuriyet'), 'G01 "Cumhuriyet!" biter: DORUK, motif tam (Re majör)'),
            (W('G06', 'cumhuriyetimizin'), 'G06 "Cumhuriyetimizin": bando uzaktan yaklaşır (kısık)'),
            (E('G06'), 'G06 biter: bitiş ekranı bando marşı (motif + aynası), Re majör final')]):
        L.append(f'- {ts(t)}: {what}')
    L += ['', '## Seslendirme planı için not', '',
          f'- Doruk "Yaşasın Cumhuriyet!" biter bitmez başlar ve ~5 sn sürer; şu an G01 ile G02 arası '
          f'{S("G02") - E("G01"):.1f} sn. `vo/plan.json` içinde `gap.G01` 2.5-3 sn olursa doruğun çoğu boşlukta duyulur.',
          '- Bölüm araları (`secGap`) ve cümle araları müziğin yükseldiği yerlerdir; ne kadar uzunsa müzik o kadar nefes alır.',
          '- Seslendirme ya da senaryo değişirse: `python3 tools/build_vo.py` → `python3 audio/score.py` → '
          '`python3 tools/mix.py --stems` → `python3 audio/ses_rapor.py` (board/ses/ kanıtları).', '']
    path.write_text('\n'.join(L), encoding='utf-8')


# =============================================================================== main
def main():
    print(f'film {DUR:.2f} s, {N} samples, {len(CUE)} sentences, {len(WORDS)} words'
          f'{" (PROVISIONAL timeline)" if PROVISIONAL else ""}', flush=True)
    for letter, f in SECTION_FUNCS:
        if letter not in GROUP:
            print(f'  ! section {letter} missing from timeline.js, skipped')
            continue
        t = time.time()
        f()
        print(f'  {f.__name__:14s} {sec_span(letter)[0]:7.2f} s  {time.time() - t:5.1f} s', flush=True)
    mix, used_vo = mixdown()
    write_wav(OUT, mix)
    write_cues_md(HERE / 'cues.md')
    print(f'wrote {OUT.relative_to(FILM)} + audio/cues.md  ({len(mix) / SR:.3f} s, speech mask from '
          f'{"timeline.js + vo.wav" if used_vo else "timeline.js"})  in {time.time() - T_START:.1f} s')


if __name__ == '__main__':
    main()
