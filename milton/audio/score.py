#!/usr/bin/env python3
"""
KAYIP CENNET — Şeytan'ın iç yolculuğu: özgün müzik ve efektler, tamamen numpy/scipy ile sentez
(örnek ses yok, indirme yok, ücretli üretim yok).

    python3 audio/score.py          (film klasöründen)
    -> audio/music.wav              48 kHz, stereo, 16 bit, tam film süresi (timeline.js DUR)
    -> audio/motifler.txt           motiflerin çaldığı anlar ve notaları (doğrulama listesi)

Girdiler
    timeline.js   cümle (CUES) ve kelime (WORDS) zamanları: her vuruş bir cümleye ya da kelimeye bağlı,
                  hiçbir zaman sabit yazılmaz; çizelge değişince yeniden çalıştırmak yeter
    vo/vo.wav     yalnız konuşmanın nerede olduğunu bulmak için analiz edilir; miksine girmez

Çalgı motoru (Karplus-Strong telli, yaylı topluluğu, sözsüz koro, salon yankısı, konuşmaya göre spektral
kısma) Sisifos/Prometheus filmlerinden devralındı. Düzenleme, motifler, org, klavsen, timpani, büyük çan
ve bütün efektler bu filme özgüdür.

Palet  17. yüzyıl İngiltere'si x karanlık destan
    viol topluluğu (yaylı)  ·  uzak, yumuşak borulu org (labial)  ·  lavta ve klavsen (Milton'ın odası)
    sözsüz koro "a/u" (cennet, iç ışık)  ·  alçak dron, timpani (cehennem, savaş)  ·  tek büyük çan (kırılmalar)

Motifler (ton merkezi Sol)
    IŞIK      Si4 Re5 La5 Sol5          (Sol majör; üçlü, beşli sıçrama, inen ikili ile çözülür)
              eksilerek döner:  minör  Sib4 Re5 La5 Sol5  ->  kırık (Frig)  Sib4 Re5 Lab5 Sol5
              ->  yarım  Sib4 Re5 (sıçrama hiç gelmez)  ;  umut (G09)  Si4 Re5 La5 (çözülmeden asılı)
              L09'da ilk kez Milton için tam ve çözülerek: Si4 Re5 La5 Sol5 Fa#5 Sol5
    DÜŞÜŞ     Sol2 Fa#2 Fa2 Mi2 Mib2 Re2  (aksak uzun-kısa adımlarla inen kromatik bas)
              D09: dokuz gün = dokuz yarım ses (Sol2 -> Sib1), her adımda bir timpani
    İÇ CEHENNEM (G07)  kırık IŞIK tiz viol + koroda, DÜŞÜŞ basta: ikisi "Ben cehennemim"de buluşur
    ABDİEL    Sol4 Re5 Mi5 Re5          (dik duran, süssüz çizgi; K16'da geri gelir)
    ADEN      Re5 Si4 Do5 La4 Si4 Sol4  (klavsen/lavta pastorali; K01'de çıkışta umut)
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
    f0, f1 = max(f0, 70), 49.0          # settles on G1 (the film's tonic)
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
    chord = [note(x) for x in chord]
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



# =============================================================================== the score
# Harmonic colours (all centred on G):
HEAVEN = ['G2 D3 B3 D4', 'C3 G3 B3 E4', 'D3 A3 D4 F#4', 'E2 B2 G3 D4']          # G major, open voicings, no cadences
HELL = ['G1 D2 G2 Bb2', 'Ab1 Eb2 Ab2 C3', 'G1 D2 G2 Bb2', 'F1 C2 Ab2 C3']          # G Phrygian / C minor colour
ROOM = ['G2 D3 Bb3', 'Eb2 Bb2 G3', 'C3 G3 Eb4', 'D2 A2 F#3']                     # Milton's room: G minor, lute
OPEN = ['G2 D3 A3 D4', 'C3 G3 D4 E4', 'G2 D3 B3 D4', 'D3 A3 E4 F#4']              # hope (K01, L11)
SUSP = 'C3 G3 D4 G4'                                                          # the question chord (C12, K16, L10)


def a_hook():
    """A: 'Ben cehennemim' (cold open, Nifates silhouette with the lake inside), the brightest angel, the lake."""
    # A01: wind + inner fire; the fall bass under the line; one high broken sigh as 'cehennemim' lands (G07 preview)
    wind(0.0, S('A02') + 0.5, vel=0.07, lo=200, hi=900)
    fire_bed(0.15, Se('A01') + 0.8, vel=0.07, crack=0.4)
    drone('G1 D2', 0.1, S('A02') + 0.6, gain=0.22, att=0.6, rel=0.8)
    span = W('A01', 'ben') - W('A01', 'hangi') + 0.6
    fall(W('A01', 'hangi') - 0.25, 'G2', beat=span / 9.0, gain=0.3)
    choir_line(W('A01', 'cehennemim'), [(note('Ab5'), 0.7, 1.0), (note('G5'), 1.4, 0.8)], gain=0.16, vowel='u')
    boom(We('A01', 'cehennemim') + 0.05, vel=0.3, f0=70, decay=1.0, knock=0.2)   # after the word, never on it
    # A02: match-cut to the archangel in light: the LIGHT motif, complete, G major (the only time before heaven)
    T = S('A02') - 0.15
    riser(T + 0.1, 0.9, vel=0.12, kind='cym')
    choir(M('G3 B3 D4 G4'), T, Se('A02') + 1.0, gain=0.24, att=0.5, rel=1.0)
    organ('G2 D3 B3', T, Se('A02') + 1.0, gain=0.12, att=0.6, rel=1.0)
    light(W('A02', 'cennetin'), 'full', beat=0.42, inst='viol', gain=0.28)
    light(W('A02', 'cennetin') + 0.02, 'full', beat=0.42, inst='hpsi', gain=0.16)
    shimmer(W('A02', 'parlak'), dur=1.6, vel=0.035)
    # A03: the escape (small winged figure rising from hell's mouth): wings, wind, low tremolo; the question hangs
    wings(S('A03') + 0.1, W('A03', 'ama') + 0.3, period=0.75, vel=0.13)
    wind(S('A03'), nxt('A03') + 0.5, vel=0.08, lo=180, hi=1200, gust=0.8)
    bowed(S('A03'), [('G2', W('A03', 'onu') - S('A03'), 0.6)], gain=0.2, stack=(0, 3, 7), trem=0.5, cutoff=800, vib=0)
    consort('Eb3 Bb3 F4', W('A03', 'onu') - 0.2, nxt('A03') + 0.8, gain=0.11, cutoff=900, att=0.6, rel=1.0)
    # A04: eyes open on the burning lake; nine days; chains
    T = S('A04')
    fire_bed(T - 0.6, Se('A04') + 1.2, vel=0.13, crack=0.6, att=1.5)
    drone('G1 D2 Ab2', T - 0.3, Se('A04') + 1.0, gain=0.24, att=1.5, rel=1.2)
    timp(W('A04', 'dokuz'), 'G2', vel=0.22)
    timp(W('A04', 'gün'), 'G2', vel=0.16)
    organ('G1 D2 Ab2 Eb3', W('A04', 'görünür') - 0.3, Se('A04') + 1.0, gain=0.09, att=1.0, rel=1.0, chiff=0.0)
    chain_rattle(W('A04', 'zincirlerle'), vel=0.26, dur=1.0)
    chain_lock(W('A04', 'bağlı') + 0.05, vel=0.25)
    # A05: the title page of the epic (ink appears): page, then the lute — Milton's world
    page(S('A05') - 0.35, vel=0.14)
    T = W('A05', 'kayıp')
    timp(T, 'G2', vel=0.35)
    boom(T, vel=0.3, f0=70, decay=1.2, knock=0.2)
    choir(M('G2 D3 Bb3 D4'), T - 0.05, W('A05', 'buradaki') + 0.3, gain=0.2, att=0.3, rel=1.0, vowel='o')
    lute_arp(W('A05', 'buradaki'), Se('A05') + 0.6, ['G2 D3 G3 Bb3', 'Eb2 Bb2 Eb3 G3', 'C3 G3 C4 Eb4', 'D3 A3 D4 F#4'], step=0.45, vel=0.2)
    # A06: 'hiçbir şey göremiyordu': everything thins to one low viol note; the candle
    viol(S('A06') - 0.2, [('G2', Se('A06') - S('A06') + 1.5, 0.7)], gain=0.16, solo=False, cutoff=900)
    lute(Se('A06') + 0.2, 'D4', vel=0.25)
    lute(Se('A06') + 0.65, 'G3', vel=0.2)


def b_poet():
    """B: the blind poet (London, night): lute and a soft viol consort; quill, pages; the burning books."""
    card(S('B01') - 0.1)
    lute(S('B01') - 0.05, 'G2', vel=0.3)
    consort('G2 D3 Bb3', S('B01'), S('B02') + 0.5, gain=0.08, cutoff=900)
    # B02-B03: night room: G minor lute broken chords, thinned under the words; quill when he dictates
    lute_arp(S('B02') - 0.2, Se('B03') + 0.6, ROOM * 3, step=0.46, vel=0.19)
    bed(S('B02'), Se('B03') + 1.0, ['G2 D3 Bb3', 'Eb2 G3 Bb3', 'C3 G3 Eb4', 'D2 F#3 A3'] * 2, gain=0.07, cutoff=900)
    quill(W('B02', 'yazdırırdı'), W('B02', 'yazdırırdı') + 3.0, vel=0.07)
    quill(W('B02', 'kırk'), Se('B02') + 0.4, vel=0.06)
    page(W('B03', 'okurdu') - 0.2, vel=0.1)
    consort('C3 G3 Eb4 Ab4', W('B03', 'dayanılmaz') - 0.3, nxt('B03') + 0.6, gain=0.08, cutoff=900)
    # B04: the revolutionary; the hangman burns his books (crowd, flames); then 'sekiz yıldır kördü': fire gone
    timp(W('B04', 'devrimciydi'), 'G2', vel=0.25)
    timp(W('B04', 'idamını'), 'G2', vel=0.2)
    drone('G1 D2', S('B04'), Se('B04') + 1.5, gain=0.16)
    timp(W('B04', 'devrim'), 'D2', vel=0.22)
    T = W('B04', 'cellat')
    whoosh(T + 0.1, vel=0.12, lo=300, hi=2000)
    crowd(T - 0.3, W('B04', 'sekiz') + 0.3, vel=0.05, att=1.0, rel=0.6)
    fire_bed(T - 0.2, W('B04', 'sekiz') + 0.4, vel=0.11, crack=1.3, density=14, att=0.5, rel=0.5)
    for k in range(3):
        page(T + 0.6 + k * 0.9, vel=0.06, pan=rng.uniform(-0.6, 0.6))
    stab(W('B04', 'sekiz') - 0.05, 'G2 D3 G3', vel=0.12, cutoff=900, rel=2.0)
    viol(W('B04', 'kördü'), [('G3', 1.6, 0.8), ('F#3', 1.2, 0.6)], gain=0.14)
    # B05: he finished it in defeat: manuscript pages pile up
    for k, t in enumerate(np.linspace(S('B05') + 0.3, Se('B05') - 0.3, 3)):
        page(t, vel=0.07)
    lute_arp(S('B05'), Se('B05') + 0.4, ['Eb2 Bb2 Eb3 G3', 'D2 A2 D3 F#3'], step=0.48, vel=0.17)
    # B06: 'Mevsimler döner; ama bana gün dönmez': seasons pass in the window; slow organ chords, far away
    bed(S('B06') - 0.3, Se('B06') + 1.0, ['Eb3 Bb3 G4', 'C3 G3 Eb4', 'Ab2 Eb3 C4', 'G2 D3 Bb3'], kind='organ', gain=0.1, att=1.2, rel=1.2, chiff=0.03)
    viol(W('B06', 'mevsimler'), [('D4', 1.8, 0.7), ('Eb4', 1.8, 0.7), ('D4', 1.4, 0.6), ('C4', 1.6, 0.5), ('Bb3', 3.0, 0.5)], gain=0.12)
    # B08: a poet who lost the light, an angel who lost the light: the LIGHT (minor) on lute, viol answers
    light(W('B08', 'şair') - 0.1, 'min', beat=0.38, inst='lute', gain=0.26)
    light(W('B08', 'meleği') - 0.05, 'min', beat=0.42, inst='viol', gain=0.2)
    consort('G2 D3 Bb3', S('B08'), nxt('B08') + 0.8, gain=0.07, cutoff=900)
    # B09: an old draft (a sun on the page): page turn, the sun glows (choir, Eb), it was a confession
    page(S('B09') - 0.3, vel=0.12)
    lute_arp(S('B09'), W('B09', 've') - 0.2, ['G2 D3 G3 Bb3', 'Eb2 Bb2 Eb3 G3'], step=0.5, vel=0.15)
    choir(M('Eb3 Bb3 G4'), W('B09', 'zafer') - 0.3, Se('B09') + 1.0, gain=0.14, att=1.2, rel=1.0, vowel='u')
    # B10 -> C: the sun on the page grows into heaven's light
    consort('D3 A3 D4', S('B10'), S('C01') + 0.5, gain=0.07, cutoff=1200)
    riser(S('C01') - 0.05, (S('C01') - S('B10')) * 0.8, vel=0.16, kind='cym')


def c_light():
    """C: heaven (light, organ far away, wordless choir 'a'); the revolt; Abdiel alone."""
    t0, t1 = S('C01') - 0.2, Se('C09') + 0.5
    card(S('C01') - 0.1, vel=0.6)
    choir(M('G3 D4 G4 B4'), t0, S('C02') + 1.2, gain=0.24, att=0.6, rel=1.4)
    organ('G2 D3 G3', t0, Se('C04'), gain=0.1, att=1.0, rel=1.5)
    bed(S('C02') - 0.5, Se('C03') + 0.5, HEAVEN, gain=0.08, cutoff=1500)
    bed(S('C02'), Se('C03') + 0.5, ['G3 B3 D4', 'C4 E4 G4', 'D4 F#4 A4', 'B3 D4 G4'], kind='choir', gain=0.11, att=1.5, rel=1.5)
    arp(S('C02'), Se('C03'), M('G4 B4 D5 A5'), [0, 1, 2, 3, 2, 1], 0.32, inst='hpsi', vel=0.06)
    light(W('C02', 'parlak') - 0.1, 'full', beat=0.44, inst='choir', gain=0.2)
    light(W('C03', 'lüsifer') - 0.05, 'full', beat=0.42, inst='viol', gain=0.28)
    shimmer(W('C03', 'ışık') - 0.2, dur=1.8, vel=0.04)
    # C04: the Son exalted (brighter D), then 'diz çökecek': a low Eb creeps in; 'karanlığa düşecektir': the fall foreshadowed
    choir(M('D3 A3 D4 F#4'), W('C04', 'oğulu') - 0.2, W('C04', 'diz') + 0.5, gain=0.2, att=0.6, rel=1.0)
    organ('D2 A2 D3', W('C04', 'oğulu') - 0.2, W('C04', 'diz') + 0.5, gain=0.1, att=0.6, rel=1.0)
    bowed(W('C04', 'diz') - 0.1, [('Eb2', Se('C04') - W('C04', 'diz') + 1.0, 0.6)], gain=0.2, stack=(0, 12), cutoff=700, vib=2, att=0.8)
    consort('G2 Eb3 Bb3', W('C04', 'diz'), Se('C04') + 0.8, gain=0.08, cutoff=900)
    fall(W('C04', 'karanlığa') - 0.1, 'G2', beat=0.3, kind=FALL[:3], gain=0.22)
    # C05: midnight conspiracy: quiet low pizzicato pulse, darker chords
    t = S('C05')
    while t < Se('C05'):
        lute(t, 'G2', vel=0.14 * (0.7 if speaking(t) else 1.0), t60=0.8, damp=0.85, bright=0.25)
        t += 0.5
    bed(S('C05'), Se('C05') + 0.6, ['E2 B2 G3', 'C3 G3 Eb4'], gain=0.07, cutoff=850)
    # C06: 'özgürlük': the word lands on a drum and a bright, slightly off chord
    T = W('C06', 'özgürlük')
    timp(T, 'G2', vel=0.4)
    choir(M('Bb2 F3 Bb3 D4'), T - 0.05, T + 3.0, gain=0.2, att=0.15, rel=1.6)
    consort('Bb2 F3 D4', T - 0.05, Se('C07') + 0.6, gain=0.08, cutoff=1100)
    # C07: his speech: pull back to a low pedal, tremolo
    bowed(S('C07'), [('D2', Se('C07') - S('C07') + 0.5, 0.5)], gain=0.13, stack=(0, 7), trem=0.35, cutoff=700, vib=0)
    # C08: a third of heaven follows him (points of light flow): the FALL motif, first full statement
    fall(W('C08', 'üçte') - 0.2, 'G2', beat=0.42, gain=0.3)
    for k, t in enumerate(np.linspace(W('C08', 'ordularının'), Se('C08') + 1.0, 9)):
        hpsi(t, ['A5', 'G5', 'F#5', 'E5', 'D5', 'C5', 'B4', 'A4', 'G4'][k], vel=0.08)
    # C09: two answers: 'özgürlük için' (major) / 'kıskançlık ve gurur' (the light, minor)
    consort('G2 D3 B3', W('C09', 'özgürlük') - 0.1, W('C09', 'miltona') + 0.2, gain=0.08)
    consort('G2 D3 Bb3', W('C09', 'kıskançlık') - 0.1, Se('C09') + 0.8, gain=0.08)
    light(W('C09', 'kıskançlık'), 'min', beat=0.36, inst='hpsi', gain=0.14)
    # C10-C11: Abdiel stands up: everything thins; one plain upright line, alone; a pedal
    organ('G2 D3', S('C10') - 0.2, Se('C11') + 1.0, gain=0.08, att=1.0, rel=1.4, chiff=0.0)
    abdiel(W('C10', 'abdiyeldir'), beat=0.55, gain=0.24)
    viol(W('C11', 'tek'), [('G4', 1.0, 0.7), ('A4', 1.0, 0.7), ('B4', 1.0, 0.7), ('D5', 2.4, 0.8)], gain=0.16)
    abdiel(Se('C11') - 0.2, beat=0.45, gain=0.18)
    # C12: who is the real rebel? the question chord; two plucks, unresolved
    consort(SUSP, S('C12') - 0.2, Se('C12') + 1.5, gain=0.08, cutoff=1000)
    hpsi(Se('C12') + 0.1, 'D5', vel=0.14)
    hpsi(Se('C12') + 0.5, 'A4', vel=0.12)


def d_war():
    """D: the war in heaven, the wound, the chariot, nine days of falling."""
    card(S('D01') - 0.1, vel=0.7)
    T = W('D01', 'kılıçlar')
    for k in range(4):
        sword_draw(T - 0.35 + k * 0.17, vel=0.22 * (1 - 0.15 * k), pan=-0.6 + 0.4 * k)
    timp_roll(T, T + 1.6, 'G2', vel=0.16)
    drone('G1 D2', S('D01'), Se('D03') + 1.0, gain=0.18)
    bed(S('D01'), Se('D03') + 0.6, ['G2 D3 Bb3', 'Ab2 Eb3 C4', 'G2 D3 Bb3'], gain=0.08, cutoff=900)
    war_drums(Se('D01') + 0.05, nxt('D01') + 0.2, beat=0.5, vel=0.3)
    light(W('D01', 'acının') - 0.2, 'min', beat=0.4, inst='viol', gain=0.14)
    # D02-D03: Abdiel's answer (quote): pull back; 'zincir bekle': a link closes
    abdiel(W('D02', 'abdiyel'), beat=0.5, gain=0.16)
    chain_lock(W('D03', 'zincir'), vel=0.22)
    # D04: the sword falls; ten steps back; knee on the ground
    T = W('D04', 'kılıç')
    sword_clash(T, vel=0.55)
    boom(T, vel=0.4, f0=80, decay=0.8, knock=0.4)
    footsteps(W('D04', 'geriler'), W('D04', 'çöker'), count=10, vel=0.16)
    thud(W('D04', 'çöker') + 0.05, vel=0.35, f0=55)
    stab(W('D04', 'çöker'), 'G2 D3 Ab3', vel=0.14, cutoff=900)
    # D05: a blade through his right side: the first pain = the LIGHT broken for the first time
    sword_clash(W('D05', 'yarar') - 0.05, vel=0.4, pan=0.3)
    whoosh(W('D05', 'kılıcı'), vel=0.12, dur=0.35, lo=600, hi=3000)
    light(W('D05', 'acıyı') - 0.1, 'broken', beat=0.4, inst='viol', gain=0.2)
    consort('G2 D3 Bb3 Eb4', S('D05'), Se('D06') + 0.8, gain=0.07, cutoff=900)
    # D07: gunpowder and cannon; mountains torn up
    cannon(W('D07', 'barutu'), vel=0.45, pan=-0.4)
    cannon(W('D07', 'topu'), vel=0.55, pan=-0.2)
    cannon(We('D07', 'eder') + 0.1, vel=0.4, pan=-0.5)
    quake(W('D07', 'dağları'), vel=0.45, dur=3.0)
    debris(W('D07', 'atar'), vel=0.3, dur=1.0)
    war_drums(S('D07'), Se('D07') + 0.5, beat=0.48, vel=0.22)
    # D08: the chariot of light (no figure): choir and organ in D major, rolling wheels; they leap into the void
    T = W('D08', 'oğul')
    choir(M('D3 A3 D4 F#4 A4'), T - 0.3, W('D08', 'asiler') + 0.5, gain=0.26, att=0.5, rel=1.0)
    organ('D2 A2 D3 F#3', T - 0.3, W('D08', 'asiler') + 0.5, gain=0.12, att=0.5, rel=1.0)
    rumble(T, We('D08', 'sürülür'), vel=0.35)
    shimmer(T, dur=2.0, vel=0.04, notes=('A6', 'D7', 'F#6', 'A5'))
    whoosh_down(W('D08', 'boşluğa'), dur=1.8, vel=0.16)
    # D09: nine days of falling: nine semitones down in the bass, a timpani on each; Chaos roars; hell closes
    a, b = S('D09') - 0.1, W('D09', 'kapandı')
    step = (b - a) / 10.0
    fall(a, 'G2', beat=step, kind=FALL9, gain=0.36, stack=(0, 12, -12))
    for k in range(9):
        timp(a + (k + 1) * step, 'G2', vel=0.18 + 0.03 * k)
    thunder(W('D09', 'kaos') + 0.05, vel=0.55)
    wind(S('D09'), Se('D09') + 0.5, vel=0.08, lo=100, hi=900, gust=1.0)
    T = We('D09', 'kapandı')
    boom(T + 0.05, vel=0.65, f0=70, decay=1.6, knock=0.7)
    door(T - 1.6, vel=0.2, dur=1.6)
    # D10: back to the lake
    fire_bed(Se('D09') + 0.4, nxt('D10') + 1.0, vel=0.12, crack=0.5)
    drone('G1 D2', Se('D09') + 0.2, nxt('D10') + 1.0, gain=0.2)


def e_king():
    """E: the burning lake and the shore; the king of hell; Pandemonium; the council."""
    t0, t1 = S('E01') - 0.5, Se('E08') + 1.5
    card(S('E01') - 0.1, vel=0.7)
    fire_bed(t0, S('E05'), vel=0.1, crack=0.45)
    fire_bed(S('E05'), t1, vel=0.12, crack=0.55)
    drone('G1 D2', t0, Se('E04') + 1.0, gain=0.2)
    organ('G1 D2 G2 Bb2', S('E01') - 0.1, S('E02') + 1.0, gain=0.11, att=0.3, rel=1.4)
    # E02: Beelzebub. 'ne kadar düşmüş' (a fall fragment) / 'ışık diyarında' (the light remembered, minor, far)
    bed(S('E02'), Se('E02') + 0.5, ['G2 D3 Bb3', 'Eb2 Bb2 G3'], gain=0.06, cutoff=800)
    fall(W('E02', 'düşmüş') - 0.1, 'G2', beat=0.3, kind=FALL[:4], gain=0.2)
    light(W('E02', 'ışık') - 0.1, 'min', beat=0.42, inst='choir', gain=0.12)
    # E03: four words appear one by one (irade · intikam · nefret · yüreklilik): rising timpani + low strokes
    for w, m in [('irade', 'G2'), ('intikam', 'Ab2'), ('nefret', 'Bb2'), ('yüreklilik', 'C3')]:
        timp(W('E03', w), m, vel=0.28)
        stab(W('E03', w), m, vel=0.1, cutoff=800, rel=0.8)
    # E04: proud outline, a curled-up small figure inside (despair): thin high viol; the poet (ODA) bows his head
    viol(W('E04', 'umutsuzlukla') - 0.3, [('D5', 1.6, 0.5), ('Eb5', 1.0, 0.5), ('D5', 2.0, 0.4)], gain=0.1, vib=3)
    lute(W('E04', 'destan'), 'G3', vel=0.2)
    lute(W('E04', 'destan') + 0.45, 'D3', vel=0.18)
    # E05: he rises from the lake: wings open, released chains fall
    T = W('E05', 'kalkar')
    riser(T, 1.2, vel=0.14)
    whoosh(T, vel=0.22, dur=0.9, lo=120, hi=700)
    whoosh(T + 0.6, vel=0.18, dur=0.8, lo=120, hi=700)
    chain_rattle(T + 0.2, vel=0.3, dur=1.4, pan=-0.2)
    bowed(T - 0.2, [('G2', 0.8), ('Bb2', 0.8), ('D3', 0.8), ('G3', 2.0)], gain=0.2, stack=(0, 12), cutoff=900, vib=2)
    # E06: 'Elveda mutlu ovalar' = the light, minor, on the far organ; 'dehşetler' = low Ab major accent
    light(W('E06', 'elveda') - 0.05, 'min', beat=0.45, inst='organ', gain=0.16)
    stab(W('E06', 'dehşetler'), 'Ab1 Eb2 Ab2 C3', vel=0.14, cutoff=800, rel=1.6)
    drone('Ab1 Eb2', W('E06', 'dehşetler'), Se('E06') + 0.5, gain=0.14)
    consort('G2 D3 Bb3', W('E06', 'zihin') - 0.3, Se('E06') + 0.8, gain=0.06, cutoff=800)
    # E07-E08: the most famous line; the spear is planted; a dark Phrygian organ, held
    T = W('E07', 'cehennemde')
    boom(T, vel=0.5, f0=75, decay=1.2, knock=0.5)
    metal(T, f0=180, vel=0.15, decay=0.5, click=0.7)
    timp(T, 'G2', vel=0.35)
    organ('G1 D2 G2 Ab2 D3', T - 0.1, Se('E08') + 1.5, gain=0.13, att=0.4, rel=1.6, chiff=0.05)
    choir(M('G2 D3 G3 Ab3'), T - 0.05, Se('E07') + 0.8, gain=0.14, att=0.4, rel=1.2, vowel='o')
    timp(W('E08', 'kral'), 'G2', vel=0.3)
    # E09: scale: the shield like a moon, the spear beside a mast: low drum steps rising
    for k, w in enumerate(['kalkanı', 'ay', 'mızrağı', 'geminin', 'değnek']):
        lute(W('E09', w), ['G1', 'D2', 'G2', 'D3', 'G3'][k], vel=0.18, t60=1.2, damp=0.8)
    drone('G1 D2', S('E09'), Se('E11') + 1.0, gain=0.16)
    # E10: the face: 'gurur' (G minor, organ) / 'pişmanlık' (Eb major, choir): two chords that return in L05
    organ('G2 D3 Bb3', W('E10', 'gurur') - 0.1, W('E10', 'gözlerinde') + 0.3, gain=0.12, att=0.2, rel=0.8)
    choir(M('Eb3 Bb3 G4'), W('E10', 'pişmanlık') - 0.1, Se('E10') + 1.5, gain=0.16, att=0.25, rel=1.2, vowel='u')
    # E11: his army, scorched but standing; three attempts to speak; the tears (the light, minor, soft)
    bed(S('E11'), Se('E11') + 0.6, ['G2 D3 Bb3', 'Eb2 Bb2 G3', 'C3 G3 Eb4'], gain=0.07, cutoff=900)
    for k in range(3):
        consort('D3 A3', W('E11', 'dener') + 0.6 * k, W('E11', 'dener') + 0.6 * k + 0.8, gain=0.05, att=0.3, rel=0.4)
    choir_line(W('E11', 'gözlerinden'), [(note('D5'), 0.8, 1.0), (note('C5'), 0.8, 0.9), (note('Bb4'), 0.8, 0.8), (note('A4'), 1.6, 0.7)], gain=0.13, vowel='u')
    drop(W('E11', 'yaşlar') + 0.2, vel=0.08)
    light(Se('E11') + 0.05, 'min', beat=0.42, inst='viol', gain=0.18)
    # E12: gold dug from hell's soil; the palace rises: Pandemonium
    t = W('E12', 'altın')
    while t < W('E12', 'saray'):
        metal(t, f0=rng.uniform(800, 1100), vel=0.06, decay=0.2, ratios=(1, 2.7, 4.1), click=0.6, pan=rng.uniform(-0.6, 0.6), bus=PERC)
        t += rng.uniform(0.25, 0.4)
    T = W('E12', 'saray')
    organ('G1 D2 Ab2 D3 G3', T - 0.5, W('E12', 'pandemonyum') + 2.0, gain=0.12, att=1.5, rel=1.4)
    rumble(T - 0.5, W('E12', 'pandemonyum'), vel=0.3)
    timp(W('E12', 'pandemonyum'), 'G2', vel=0.4)
    boom(W('E12', 'pandemonyum'), vel=0.35, f0=70, decay=1.0)
    choir(M('G2 D3 Ab3 D4'), W('E12', 'pandemonyum') - 0.05, Se('E12') + 1.0, gain=0.16, att=0.2, rel=1.2, vowel='o')
    # E13: the council (sustained low strings); 'insana saldırmak': a drum
    bowed(S('E13') - 0.2, [('G2', Se('E13') - S('E13') + 0.8, 0.5)], gain=0.13, stack=(0, 7, 12), cutoff=700, vib=2)
    timp(W('E13', 'insana'), 'G2', vel=0.25)
    # E14: only he volunteers: a solo low viol
    viol(W('E14', 'yalnızca') - 0.1, [('D3', 0.8, 0.8), ('G3', 0.8, 0.8), ('Bb3', 2.2, 0.8)], gain=0.17, cutoff=1600)
    # E15: all hell bows (a grand, hollow Eb major), then 'diz çökmeyi reddeden...': it drains to a low unison
    T = W('E15', 'eğilir')
    organ('Eb2 Bb2 Eb3 G3 Bb3', T - 0.3, W('E15', 'diz') + 0.2, gain=0.14, att=0.6, rel=0.6)
    choir(M('Eb3 Bb3 G4'), T - 0.3, W('E15', 'diz') + 0.2, gain=0.18, att=0.6, rel=0.6)
    bowed(W('E15', 'diz'), [('G2', Se('E15') - W('E15', 'diz') + 1.5, 0.6)], gain=0.16, stack=(0, -12), cutoff=600, vib=0)
    light(Se('E15') + 0.1, 'half', beat=0.5, inst='viol', gain=0.13)


def f_gates():
    """F: Sin and Death at the gate; the door; Chaos; the flight; the sun (Uriel); Niphates."""
    card(S('F01') - 0.1, vel=0.6)
    drone('G1 Db2 G2', S('F01') - 0.2, S('F05') + 0.5, gain=0.16)
    consort('G2 Ab2 D3', S('F01'), Se('F01') + 1.2, gain=0.06, cutoff=700)
    hiss(W('F02', 'yılan'), W('F02', 'yılan') + 1.2, vel=0.05)
    bowed(W('F02', 'gölge') - 0.1, [('Db2', 3.0, 0.5)], gain=0.13, stack=(0, 1, 6), cutoff=600, vib=0, att=0.8)
    # F03: Sin: 'born from your head': the light, broken and veiled, on the choir
    light(W('F03', 'yarıldı') - 0.1, 'broken', beat=0.42, inst='choir', gain=0.12, vowel='u')
    consort('G2 D3 Bb3', W('F03', 'beni'), Se('F03') + 0.6, gain=0.05, cutoff=800)
    # F04: 'Ölüm. Kendi oğlu.'
    T = W('F04', 'ölüm')
    boom(T, vel=0.4, f0=60, decay=1.4, knock=0.3)
    stab(T, 'G1 Db2 G2', vel=0.12, cutoff=700, rel=2.0)
    # F05: Sin opens the gate: creak + boom; the ocean of Chaos (wind, swirling glissandi)
    door(W('F05', 'kapıyı') - 0.2, vel=0.45, dur=2.0)
    T = W('F05', 'kaos')
    wind(T - 1.0, S('F07') + 1.0, vel=0.12, lo=90, hi=1400, gust=1.0)
    for k in range(4):
        a = T + 0.3 + k * 1.3
        bowed(a, [(('G3', 'Db3') if k % 2 else ('Db3', 'Ab3'), 1.6, 0.5)], gain=0.08, voices=2, cutoff=900, vib=0, glide=0.4)
    rumble(T, Se('F06'), vel=0.2)
    # F06: wings, then a fall thousands of fathoms down, then a gust throws him up
    wings(W('F06', 'kanatlarını'), W('F06', 'boşluğa') - 0.2, period=0.6, vel=0.18)
    whoosh_down(W('F06', 'düşer') - 0.1, dur=2.0, vel=0.18)
    bowed(W('F06', 'düşer'), [(('G4', 'G2'), 2.0, 0.6)], gain=0.1, voices=2, cutoff=1200, vib=0)
    riser(W('F06', 'fırlatmasa') + 0.4, 1.6, vel=0.16)
    # F07: far away, a little world hung from heaven by a golden chain
    shimmer(W('F07', 'altın') - 0.1, dur=2.0, vel=0.035, notes=('G6', 'D7', 'B6'))
    clinks(W('F07', 'zincirle'), count=4, spread=0.6, vel=0.05, pan=0.3)
    consort('G3 D4 B4', W('F07', 'altın'), Se('F07') + 1.0, gain=0.07, cutoff=1800)
    hpsi(W('F07', 'dünya'), 'B5', vel=0.12)
    hpsi(W('F07', 'dünya') + 0.25, 'G5', vel=0.1)
    # F08: the sun, Uriel; he disguised as a young angel: the light FULL, but thin and too bright (a false radiance)
    choir(M('G3 D4 G4 B4'), S('F08') - 0.2, Se('F08') + 1.0, gain=0.18, att=0.8, rel=1.0)
    light(W('F08', 'genç') - 0.1, 'full', beat=0.32, inst='hpsi', gain=0.13)
    shimmer(W('F08', 'kılığında'), dur=1.2, vel=0.03)
    # F09: he glides down onto Niphates
    whoosh_down(W('F09', 'süzülür') - 0.2, dur=1.5, vel=0.12)
    wind(S('F09'), nxt('F09') + 1.0, vel=0.1, lo=150, hi=1000)


def g_confession():
    """G: Niphates. The emotional summit: the sparest, closest music in the film (wind, one viol, an organ pedal)."""
    t0, t1 = S('G01') - 0.5, Se('G16') + 2.0
    wind(t0, t1, vel=0.07, lo=180, hi=900, gust=0.35, att=2.0, rel=3.0)
    card(S('G01') - 0.1, vel=0.45)
    organ('G1 G2', S('G01') - 0.2, S('G03'), gain=0.08, att=1.5, rel=2.0, chiff=0.0)
    choir([note('D5')], S('G01'), Se('G01') + 1.5, gain=0.07, att=1.0, rel=1.2, vowel='u')
    # G02: he carries hell inside (the lake glows in his chest)
    fire_bed(W('G02', 'cehennemi') - 0.2, Se('G02') + 1.0, vel=0.045, crack=0.25, att=1.0, rel=1.2)
    drone('G1 D2', W('G02', 'cehennemi'), Se('G02') + 0.8, gain=0.1)
    # G02b: young Milton writing by day, with sight: G major lute, quill, light comes in
    lute_arp(S('G02b') - 0.1, Se('G02b') + 0.6, ['G2 D3 G3 B3', 'C3 G3 C4 E4'], step=0.42, vel=0.18)
    quill(S('G02b') + 0.5, S('G02b') + 2.5, vel=0.05)
    # G03: to the sun: high soft choir (G major) -> 'nefret' turns it to G minor
    choir(M('G3 B3 D4 G4'), W('G03', 'ey') - 0.3, W('G03', 'nefret') + 0.3, gain=0.13, att=1.0, rel=0.6, vowel='a')
    choir(M('G3 Bb3 D4 G4'), W('G03', 'nefret'), Se('G03') + 1.0, gain=0.11, att=0.6, rel=1.0, vowel='u')
    organ('G1 D2', W('G03', 'ey'), Se('G06') + 1.0, gain=0.07, att=2.0, rel=2.0, chiff=0.0)
    # G04-G05: tenderness for God; 'Keşke... mutlu kalırdım' (the light, minor, very soft: what might have been)
    viol(W('G04', 'benden') - 0.2, [('Bb3', 2.4, 0.5), ('C4', 1.6, 0.5), ('Bb3', 2.0, 0.45), ('G3', 3.0, 0.4)], gain=0.12, solo=False, cutoff=1100)
    light(W('G05', 'mutlu') - 0.15, 'min', beat=0.4, inst='viol', gain=0.15)
    # G06: 'Vardı.'
    lute(W('G06', 'vardı'), 'G2', vel=0.25, t60=1.5)
    # G07 (DORUK): 'Ben cehennemim'. FALL in the bass and the broken LIGHT on top, arriving together
    a, b = W('G07', 'vay') - 0.2, We('G07', 'cehennemim')
    fall(a, 'G2', beat=(b - a + 1.0) / 9.0, gain=0.3, stack=(0, 12))
    organ_line(a, mot('G1', FALL, (b - a + 1.0) / 9.0), gain=0.1)
    c = W('G07', 'hangi') - 0.15
    bl = (b + 1.3 - c) / 5.5
    light(c, 'broken', beat=bl, inst='viol', gain=0.26)
    light(c, 'broken', beat=bl, inst='choir', gain=0.12, vowel='u')
    boom(We('G07', 'cehennemim') + 0.05, vel=0.26, f0=65, decay=1.6, knock=0.15)
    consort('G2 D3 Ab3 D4', W('G07', 'ben'), nxt('G07') + 1.5, gain=0.08, cutoff=800)
    # G08: the deeper deep: the drone sinks an octave
    drone('G0 G1', S('G08') - 0.2, Se('G08') + 1.0, gain=0.16, cutoff=180)
    rumble(W('G08', 'dip'), Se('G08') + 0.5, vel=0.12)
    # G09: 'Pişmanlığa hiç yer kalmadı mı?' The first G major since heaven; the light reaches A5... and hangs
    T = W('G09', 'pişmanlığa')
    organ('G2 D3 B3', T - 0.5, Se('G09') + 1.8, gain=0.08, att=1.0, rel=1.0, chiff=0.0)
    choir(M('G3 B3 D4'), T - 0.3, Se('G09') + 1.6, gain=0.09, att=1.0, rel=1.0, vowel='a')
    light(T - 0.05, 'hope', beat=0.5, inst='viol', gain=0.18)
    # G09b: 'boyun eğmek' = a chain link locks; 'gururum yasaklıyor' = it collapses to a bare low G minor
    chain_lock(W('G09b', 'boyun'), vel=0.2)
    T = W('G09b', 'gururum')
    bowed(T - 0.1, [('G2', Se('G09b') - T + 2.0, 0.5)], gain=0.13, stack=(0, 12), cutoff=600, vib=0, att=0.4)
    viol(T + 0.2, [('Bb3', 1.4, 0.5), ('A3', 2.5, 0.4)], gain=0.1)
    # G10: the eyes of the army he left behind: slow soft pulses
    t = W('G10', 'ordunun')
    while t < Se('G10'):
        timp(t, 'G2', vel=0.08)
        t += 1.1
    # G11: crown and sceptre rise, he sinks: contrary motion
    T = W('G11', 'tacım') - 0.1
    viol(T, [('G4', 0.7), ('A4', 0.7), ('Bb4', 0.7), ('C5', 1.5)], gain=0.12)
    bowed(T, [('G2', 0.7), ('F#2', 0.7), ('F2', 0.7), ('E2', 1.5)], gain=0.13, stack=(0, 12), cutoff=700, vib=2)
    # G12: the cycle (kneel, rise, dizzy, fall): a turning four-note ring on the lute
    t = W('G12', 'diyelim')
    k = 0
    while t < Se('G12'):
        lute(t, ['G3', 'Bb3', 'D4', 'A3'][k % 4], vel=0.12 * (0.7 if speaking(t) else 1.0), pan=-0.3 + 0.2 * (k % 4))
        t += 0.55
        k += 1
    # G13: the distance opens: a high and a low note drift apart
    viol(S('G13'), [('D4', 2.0, 0.4), ('G4', 2.0, 0.4), ('D5', 3.0, 0.35)], gain=0.08)
    bowed(S('G13'), [('G2', 2.0, 0.4), ('D2', 2.0, 0.4), ('G1', 3.5, 0.35)], gain=0.1, cutoff=600, vib=0)
    # G14: three farewells (descending plucks); 'Kötülük: sen benim iyiliğim ol' = the toll; he turns from the sun
    for n_, m in enumerate(['D3', 'Bb2', 'G2']):
        lute(W('G14', 'elveda', n_), m, vel=0.2, t60=2.0)
    T = W('G14', 'kötülük')
    toll(T, 'G3', vel=0.3, decay=6.0)
    organ('G1 D2 Ab2', T, Se('G14') + 2.5, gain=0.1, att=0.4, rel=2.0, chiff=0.0)
    drone('G1 D2', T, Se('G15') + 1.0, gain=0.12)
    # G15: three faces (anger, envy, despair); the eye of Uriel in the sun
    for w, ch in [('öfkeyle', 'C3 G3 Eb4'), ('kıskançlıkla', 'Ab2 Eb3 C4'), ('umutsuzlukla', 'G2 D3 Bb3')]:
        consort(ch, W('G15', w) - 0.05, W('G15', w) + 1.6, gain=0.07, att=0.15, rel=0.8, cutoff=900)
    bell(W('G15', 'uriyel'), 'D6', vel=0.05, decay=1.5)
    # G16: no crowd, no mask; for the first time we pity him: the light, minor, alone; then a long breath
    light(W('G16', 'acıyoruz') - 0.1, 'min', beat=0.5, inst='viol', gain=0.15)
    consort('Eb3 Bb3 G4', W('G16', 'maskesiz'), Se('G16') + 2.0, gain=0.06, cutoff=900, rel=2.0)


def h_eden():
    """H: Eden. Harpsichord pastoral, birds; love and envy; the toad; the spear's touch; shame."""
    card(S('H01') - 0.1, vel=0.4)
    birds(S('H01') - 1.0, S('H05'), vel=0.03)
    bed(S('H01'), Se('H04') + 0.8, ['G3 D4 B4', 'C4 G4 E5', 'D3 A3 F#4', 'G3 D4 B4'], gain=0.07, cutoff=1800)
    arp(S('H02'), S('H04'), M('G4 B4 D5 G5'), [0, 2, 1, 3, 2, 1], 0.34, inst='hpsi', vel=0.07)
    whoosh(W('H02', 'atlar') - 0.15, vel=0.16, dur=0.55, lo=200, hi=1200)
    thud(We('H02', 'atlar') + 0.1, vel=0.12, f0=80)
    wings(W('H03', 'karabatak') - 0.3, W('H03', 'karabatak') + 1.0, period=0.35, vel=0.1, lo=300, hi=1500)
    # H04: Adam and Eve: the EDEN motif
    eden(W('H04', 'adem') - 0.1, beat=0.36, vel=0.22)
    eden(Se('H04') + 0.1, beat=0.36, vel=0.15, inst='lute')
    # H05: 'Onları sevebilirim bile': the light, minor, tender
    light(W('H05', 'sevebilirim') - 0.1, 'min', beat=0.45, inst='viol', gain=0.16)
    consort('Eb3 Bb3 G4', S('H05'), Se('H05') + 0.6, gain=0.06, cutoff=1100)
    # H06: 'intikamı': the inner flame grows back
    fire_bed(W('H06', 'krallığının'), Se('H06') + 0.8, vel=0.04, crack=0.3, att=1.5, rel=0.8)
    consort('G2 Db3 Ab3', W('H06', 'ama') - 0.1, Se('H06') + 0.8, gain=0.07, cutoff=800)
    # H07: the poet's margin note
    page(S('H07') - 0.25, vel=0.1)
    quill(W('H07', 'zorbaların'), W('H07', 'zorbaların') + 2.0, vel=0.04)
    # H08: 'Nefret edilesi manzara!' a dissonant sting; 'cehenneme itildim' a fall fragment
    stab(W('H08', 'nefret'), 'G2 Ab2 D3 Eb3', vel=0.16, cutoff=900, rel=1.6)
    fall(W('H08', 'cehenneme') - 0.1, 'G2', beat=0.32, kind=FALL[:4], gain=0.2)
    # H09: night; a toad at Eve's ear; dreams whispered
    croak(W('H09', 'kurbağa') + 0.15, vel=0.1)
    choir([note('D5'), note('Ab5')], W('H09', 'rüyalar'), Se('H09') + 1.5, gain=0.06, att=1.0, rel=1.0, vowel='u', vib=30)
    # H10: the spear touches him; he springs back into his own shape
    T = W('H10', 'dokunur')
    metal(T, f0=2100, vel=0.12, decay=0.9, ratios=(1, 2.76, 5.4), click=0.4)
    riser(W('H10', 'gerçek'), 0.8, vel=0.12)
    boom(W('H10', 'biçimine'), vel=0.3, f0=70, decay=0.9)
    # H11: the bright guards (choir) vs him; 'günahına benziyorsun'
    choir(M('G3 D4 G4 B4'), S('H11') - 0.2, W('H11', 'günahına'), gain=0.11, att=0.8, rel=0.5)
    bowed(W('H11', 'günahına') - 0.1, [('G2', 3.0, 0.5)], gain=0.12, stack=(0, 13), cutoff=700, vib=0)
    # H12: shame: the fall (slow), the dimmed light (only half of it)
    fall(W('H12', 'utanç') - 0.1, 'G2', beat=0.55, gain=0.24)
    light(W('H12', 'sönükleşen') - 0.1, 'half', beat=0.5, inst='viol', gain=0.14)


def i_serpent():
    """I: seven nights; into the serpent; the 'stupid goodness'; the fruit; 'Kazanmıştır.'"""
    card(S('I01') - 0.1, vel=0.5)
    consort('G2 Db3 F3', S('I01'), Se('I01') + 1.5, gain=0.07, cutoff=800)
    # I02: seven nights circling the earth: seven low pulses; wind
    wind(S('I02'), Se('I02') + 1.0, vel=0.07)
    for t in np.linspace(W('I02', 'yedi'), W('I02', 'sekizinci') - 0.3, 7):
        timp(t, 'G2', vel=0.1)
    drone('G1 D2', S('I02'), Se('I05') + 1.0, gain=0.13)
    # I04: the sleeping serpent; disgust
    hiss(W('I04', 'yılan'), W('I04', 'yılan') + 1.5, vel=0.025)
    stab(W('I04', 'iğrenç'), 'G2 Ab2 Db3', vel=0.12, cutoff=800, rel=1.5)
    # I05: 'yükseldiği kadar alçalmak': a line up, then the fall; he flows into the snake's mouth
    T = W('I05', 'yükseldiği')
    viol(T - 0.3, [('G3', 0.4), ('Bb3', 0.4), ('D4', 0.4), ('G4', 1.0)], gain=0.14)
    fall(W('I05', 'alçalmak') - 0.1, 'G2', beat=0.38, gain=0.24)
    whoosh(W('I05', 'ağzından') - 0.2, vel=0.12, dur=1.0, lo=100, hi=600)
    hiss(W('I05', 'içine'), W('I05', 'içine') + 1.0, vel=0.03)
    # I06: morning; Eve alone in the garden; the 'stupid goodness': the drone stops, a pure G major, the light tries (2 notes)
    birds(S('I06') - 0.5, W('I06', 'havvanın'), vel=0.025)
    eden(W('I06', 'havvayı') - 0.1, beat=0.4, vel=0.13)
    T = W('I06', 'sersem')
    choir(M('G3 B3 D4 G4'), T - 0.6, Se('I06') + 1.8, gain=0.1, att=1.2, rel=1.4, vowel='a')
    consort('G3 B3 D4', T - 0.6, Se('I06') + 1.8, gain=0.06, cutoff=1800)
    hpsi(T + 0.3, 'B4', vel=0.12)
    hpsi(T + 0.8, 'D5', vel=0.1)
    _log(T + 0.3, 'IŞIK/ilk iki nota (hpsi)', [(note('B4'), 0, 0), (note('D5'), 0, 0)])
    # I07: the hell inside ends the joy: the flame and the drone return
    fire_bed(W('I07', 'cehennem') - 0.3, Se('I07') + 1.0, vel=0.05, crack=0.35, att=0.4)
    drone('G1 D2 Ab2', W('I07', 'cehennem') - 0.3, Se('I09') + 0.5, gain=0.13, att=0.6)
    # I08: the fruit: torn, bitten; then Adam too
    snap(W('I08', 'koparır') + 0.1, vel=0.3)
    crunch(W('I08', 'yer') + 0.05, vel=0.22)
    crunch(W('I08', 'adem') + 0.35, vel=0.15)
    # I09: the earth feels the wound; nature sighs; the serpent slinks into the thicket
    rumble(W('I09', 'dünya') - 0.1, W('I09', 'haber') + 0.5, vel=0.28, lo=20, hi=100)
    thunder(W('I09', 'yarayı'), vel=0.25)
    wind(W('I09', 'iç') - 0.3, Se('I09') + 1.0, vel=0.1, gust=1.0, att=0.6)
    hiss(W('I09', 'yılan'), Se('I09') + 0.6, vel=0.03, lo=1500, hi=6000)
    # I10: 'Kazanmıştır.' one deep blow, a hollow open fifth, then black
    T = Se('I10') + 0.05                  # the blow falls just after the word
    boom(T, vel=0.5, f0=65, decay=1.6, knock=0.3)
    timp(T, 'G2', vel=0.28)
    organ('G1 D2 G2', T - 0.05, Se('I10') + 2.2, gain=0.1, att=0.05, rel=1.8, chiff=0.0)


def j_hiss():
    """J: the return; the expected applause; SILENCE (J04); the hiss; the transformation (the film's break)."""
    card(S('J01') - 0.1, vel=0.5)
    drone('G1 D2', S('J01') - 0.2, S('J02') + 1.0, gain=0.12)
    # J02: in disguise across the hall; suddenly on the throne in a false radiance; cheering
    T = W('J02', 'birden')
    riser(T, 0.7, vel=0.1, kind='cym')
    shimmer(T, dur=2.4, vel=0.045, notes=('Ab5', 'Eb6', 'C6', 'Ab6'))
    choir(M('Ab2 Eb3 Ab3 C4'), T - 0.05, Se('J02') + 1.0, gain=0.14, att=0.3, rel=1.0, vowel='o')
    organ('Ab1 Eb2 Ab2', T - 0.05, Se('J03') + 0.3, gain=0.09, att=0.3, rel=0.4)
    crowd(W('J02', 'sevinç') - 0.3, Se('J03') + 0.1, vel=0.09, att=1.2, rel=0.4)
    # J03: 'Hem de bir elmayla!' a drum
    timp(W('J03', 'elmayla'), 'Ab2', vel=0.25)
    # J04: silence (master gain closes; see master_gain) — nothing is placed here.
    # J05: 'kasvetli, ortak bir tıslama': the hiss swells slowly from 'tek bir ses' and peaks in the gap
    a = W('J05', 'tek') - 0.2
    b = nxt('J05') + 0.6
    hiss(a, b, vel=0.13, voices=12, swell=1.7, att=0.5, rel=0.8)
    # J07: transformation: sharpening face, arms glued, legs entwined, he falls flat: a giant serpent (the toll)
    hiss(S('J07'), Se('J07') + 0.5, vel=0.045, voices=6, att=0.6, rel=0.8)
    bowed(W('J07', 'yüzünün') - 0.1, [(('G3', 'Db3'), 2.4, 0.5), (('D3', 'Ab2'), 2.4, 0.5)], gain=0.1, voices=2, cutoff=900, vib=0, glide=0.3)
    thud(W('J07', 'yığılır') + 0.1, vel=0.4, f0=60)
    boom(W('J07', 'yığılır') + 0.1, vel=0.25, f0=60, decay=0.8)
    T = W('J07', 'devasa')
    toll(T, 'G3', vel=0.32, decay=6.5)
    fall(T + 0.1, 'G2', beat=0.45, gain=0.26, stack=(0, 12, -12))
    hiss(W('J07', 'karnının'), W('J07', 'karnının') + 1.6, vel=0.05, lo=1800, hi=7000)
    # J08: only a hiss comes out; every devil a serpent: the hall of hissing swells in the gap
    hiss(W('J08', 'tıslama') - 0.05, W('J08', 'tıslama') + 0.9, vel=0.06)
    hiss(W('J08', 'bütün'), nxt('J08') + 0.4, vel=0.1, voices=14, swell=1.2, att=0.4, rel=1.0)
    # J06: Niphates vs. the hissing hall: pull back to a sustained low
    bowed(S('J06') - 0.2, [('G2', Se('J06') - S('J06') + 1.0, 0.5)], gain=0.12, stack=(0, 7), cutoff=700, vib=0)
    # J09: the rule (sin's shape = punishment's shape)
    consort('G2 D3 Bb3', S('J09'), Se('J09') + 0.8, gain=0.06, cutoff=800)
    stab(W('J09', 'utanca'), 'G2 Db3 G3', vel=0.1, cutoff=800, rel=1.5)
    # J10: fruit trees; the fruit turns to bitter ash in their mouths
    hiss(W('J10', 'saldırırlar') - 0.2, W('J10', 'saldırırlar') + 1.0, vel=0.04, voices=5)
    ash(W('J10', 'küle') - 0.2, W('J10', 'küle') + 2.2, vel=0.12)
    # J11: he leaves the epic; the empty dark hall; the opening question returns
    wind(S('J11'), Se('J11') + 1.0, vel=0.05)
    fall(W('J11', 'baştaki') - 0.2, 'G2', beat=0.38, gain=0.18)
    light(W('J11', 'onu') - 0.05, 'half', beat=0.5, inst='viol', gain=0.14)


def k_readings():
    """K01-K04: the way out of Eden (hope). K05-K16: the two readings (plain, thoughtful)."""
    # K01: sunrise, the flaming sword at the gate, two small figures walk on: open G, lute, choir, EDEN
    t0 = S('K01') - 0.5
    bed(t0, Se('K02') + 0.6, OPEN, gain=0.08, cutoff=1600)
    lute_arp(S('K01'), Se('K02') + 0.4, ['G2 D3 G3 B3', 'C3 G3 C4 E4', 'G2 D3 G3 B3', 'D3 A3 D4 F#4'], step=0.44, vel=0.16)
    crackle(S('K01'), W('K01', 'milton'), vel=0.025, density=4, hiss=0.05)
    eden(W('K01', 'adem') - 0.1, beat=0.4, vel=0.14, inst='lute')
    drop(W('K01', 'damla') + 0.1, vel=0.05)
    T = W('K01', 'bütün')
    choir(M('G3 D4 A4 D5'), T - 0.4, nxt('K01') + 1.2, gain=0.14, att=1.0, rel=1.4, vowel='a')
    organ('G2 D3 A3', T - 0.4, nxt('K01') + 1.2, gain=0.07, att=1.0, rel=1.4, chiff=0.0)
    # K02 -> K03: two columns: mercy (major) / none (minor)
    page(S('K03') - 0.3, vel=0.1)
    consort('G2 D3 B3', W('K03', 'insan') - 0.1, W('K03', 'asi') + 0.2, gain=0.07, cutoff=1300)
    consort('G2 D3 Bb3', W('K03', 'asi'), Se('K03') + 0.6, gain=0.07, cutoff=900)
    hpsi(W('K03', 'merhamet'), 'B4', vel=0.1)
    hpsi(W('K03', 'bulamayacak'), 'Bb4', vel=0.1)
    # K04: the candle goes out (1674)
    puff(W('K04', 'öldükten'), vel=0.1)
    lute(W('K04', 'başladı') + 0.3, 'G2', vel=0.18, t60=2.0)
    # K05-K16: TWO READINGS: harpsichord and viol consort, steady and plain
    card(S('K05') - 0.1, vel=0.4)
    page(S('K05') - 0.3, vel=0.08)
    a, b = S('K06') - 0.2, Se('K16') + 0.5
    chords = ['G2 D3 Bb3', 'D3 A3 F4', 'Eb3 Bb3 G4', 'C3 G3 Eb4', 'G2 D3 Bb3', 'D3 A3 F#4']
    nb = max(1, int((b - a) / 9.0))
    bed(a, b, [chords[i % len(chords)] for i in range(nb)], gain=0.055, cutoff=1100)
    k = 0
    t = a
    while t < b:
        ch = M(chords[int((t - a) / ((b - a) / nb)) % len(chords)])
        if not speaking(t) or k % 2 == 0:
            hpsi(t, ch[k % len(ch)] + 12, vel=0.05 if speaking(t) else 0.08, pan=0.3)
        t += 0.5
        k += 1
    page(S('K06') - 0.2, vel=0.07)
    # K07 Blake: 'zincirliydi' (a link) / 'özgür' (a free rising line); Blake's Satan is the hero: the LIGHT, full
    chain_lock(W('K07', 'zincirliydi'), vel=0.12)
    viol(W('K07', 'özgür') - 0.1, [('D4', 0.4), ('E4', 0.4), ('G4', 0.4), ('B4', 1.2)], gain=0.12)
    light(W('K07', 'tarafındaydı') - 0.6, 'full', beat=0.4, inst='viol', gain=0.15)
    # K08: most of the remembered lines are his: an echo of E07's dark organ
    organ('G1 D2 G2 Ab2', S('K08'), Se('K08') + 0.8, gain=0.06, att=0.6, rel=0.8, chiff=0.0)
    # K11 Lewis: the ladder down: hero -> general -> politician -> spy -> toad -> snake = the FALL, one step per rung
    rungs = [('kahramandan', 0), ('generale', -1), ('politikacıya', -2), ('casusa', -3), ('kurbağaya', -4), ('yılana', -5)]
    for w, o in rungs:
        T = W('K11', w)
        lute(T, note('G3') + o, vel=0.2, t60=1.4)
        lute(T, note('G2') + o, vel=0.16, t60=1.6)
    _log(W('K11', 'kahramandan'), 'DÜŞÜŞ (Lewis basamakları, lavta)', [(note('G3') + o, 0, 0) for _, o in rungs])
    timp(W('K11', 'yılana'), 'D2', vel=0.2)
    # K12: rises, falls
    viol(W('K12', 'yükselmeye') - 0.1, [('G3', 0.4), ('Bb3', 0.4), ('D4', 0.8), ('C4', 0.4), ('Bb3', 0.4), ('G3', 1.2)], gain=0.12)
    # K13: 'Blake mi haklı, Lewis mi?' (light fragment / fall fragment); the jewelled throne (hollow organ)
    light(W('K13', 'bleyk') - 0.1, 'half', beat=0.35, inst='hpsi', gain=0.12)
    fall(W('K13', 'luis'), 'G2', beat=0.3, kind=FALL[:3], gain=0.15)
    organ('G1 D2 Ab2 D3', W('K13', 'görkemli') - 0.2, Se('K13') + 0.8, gain=0.07, att=0.5, rel=0.8)
    # K15: a broken chain re-forms into a throne; K15b: the crown pushed back
    chain_rattle(W('K15', 'özgürlükleri'), vel=0.16, dur=0.5)
    clinks(W('K15', 'taht') - 0.2, count=6, spread=1.0, vel=0.06)
    metal(W('K15b', 'tacı'), f0=1500, vel=0.04, decay=0.6, click=0.2)
    # K16: the question of C12 returns: the same suspended chord, Abdiel's line
    consort(SUSP, S('K16') - 0.2, Se('K16') + 1.6, gain=0.07, cutoff=1000)
    abdiel(W('K16', 'abdiyelin') - 0.1, beat=0.5, gain=0.16)
    hpsi(Se('K16') + 0.15, 'D5', vel=0.12)
    hpsi(Se('K16') + 0.55, 'A4', vel=0.1)


def l_tear():
    """L: Cabanel's fallen angel; the two chords; the self-forged chain; the toll; the poet's inner light; the end."""
    card(S('L01') - 0.1, vel=0.4)
    t0 = S('L01') - 0.3
    bed(t0, Se('L05') + 0.6, ['Eb3 Bb3 G4', 'C3 G3 Eb4', 'Ab2 Eb3 C4', 'Bb2 F3 D4', 'Eb3 Bb3 G4', 'G2 D3 Bb3'], gain=0.07, cutoff=1100)
    organ('Eb2 Bb2', t0, Se('L03') + 1.0, gain=0.06, att=1.5, rel=1.5, chiff=0.0)
    # L03: the eye fills: a drop; the light, minor
    drop(W('L03', 'dolu') + 0.3, vel=0.08)
    light(Se('L03') - 0.1, 'min', beat=0.42, inst='viol', gain=0.16)
    # L04: the E11 tears, echoed on the choir
    choir_line(W('L04', 'ağlar') - 0.1, [(note('D5'), 0.8, 1.0), (note('C5'), 0.8, 0.9), (note('Bb4'), 0.8, 0.8), (note('A4'), 1.6, 0.7)], gain=0.11, vowel='u')
    # L05: 'pişmanlık mıydı, gurur mu?' the two chords of E10
    choir(M('Eb3 Bb3 G4'), W('L05', 'pişmanlık') - 0.1, W('L05', 'gurur') + 0.1, gain=0.13, att=0.2, rel=0.5, vowel='u')
    organ('G2 D3 Bb3', W('L05', 'gurur') - 0.05, W('L05', 'milton') + 0.4, gain=0.11, att=0.2, rel=0.6)
    # L06: the opening question returns: the A01 fall; 'içinde taşıyordu' (the inner flame); 'bir çıkış var mıydı?'
    fall(W('L06', 'cehennemden') - 0.2, 'G2', beat=0.4, gain=0.22)
    fire_bed(W('L06', 'cehennemi') - 0.2, W('L06', 'peki') + 0.5, vel=0.04, crack=0.3, att=0.6, rel=0.8)
    consort(SUSP, W('L06', 'çıkış') - 0.3, Se('L06') + 1.2, gain=0.07, cutoff=1000)
    # L07: a chain drawn link by link — and he struck it himself: 'gururu'
    drone('G1 D2', S('L07'), Se('L08') + 0.5, gain=0.12)
    for w in ['zincir', 'zinciri', 'zincirleri']:
        chain_lock(W('L07', w) + 0.05, vel=0.14)
    T = W('L07', 'gururu')
    chain_lock(T, vel=0.3)
    boom(T, vel=0.25, f0=65, decay=1.0, knock=0.2)
    viol(W('L07', 'nifates') - 0.2, [('Bb3', 1.6, 0.5), ('A3', 1.6, 0.5), ('Ab3', 1.6, 0.5), ('G3', 3.0, 0.45)], gain=0.1, solo=False, cutoff=900)
    # L08: a closed door of light above, his back turned below
    consort('G2 D3 Ab3', S('L08'), Se('L08') + 0.6, gain=0.06, cutoff=800)
    thud(W('L08', 'kapı') + 0.05, vel=0.2, f0=55)
    # L08b: 'Belki herkesin, söylemeyi kendine yasakladığı bir söz vardır.' — one toll, then quiet
    toll(S('L08b') - 0.2, 'G3', vel=0.24, decay=7.0)
    # L09: the blind poet; light rises inside his silhouette. The LIGHT, for the first time for Milton, whole and resolved
    t0 = S('L09') - 0.3
    organ('G2 D3', t0, Se('L09') + 2.0, gain=0.06, att=2.0, rel=1.6, chiff=0.0)
    T = W('L09', 'sen')
    choir(M('G3 B3 D4'), T - 0.6, Se('L09') + 2.4, gain=0.1, att=1.6, rel=1.4, vowel='a')
    light(T - 0.05, 'home', beat=0.5, inst='viol', gain=0.2)
    light(T - 0.05, 'home', beat=0.5, inst='organ', gain=0.1)
    consort('G2 D3 B3 D4', W('L09', 'belki') - 0.5, Se('L09') + 2.4, gain=0.06, cutoff=1500)
    light(Se('L09') + 0.05, 'home', beat=0.4, inst='choir', gain=0.12)
    # L10: the question to the viewer: suspended
    consort(SUSP, S('L10') - 0.3, Se('L10') + 1.2, gain=0.06, cutoff=1100)
    hpsi(W('L10', 'gurur'), 'D5', vel=0.08)
    hpsi(W('L10', 'gurur') + 0.4, 'A4', vel=0.07)
    # L11 + tail: end screen; warm and open (lute + consort), the subscribe call lifts; the film closes on the LIGHT
    a = S('L11') - 0.4
    bed(a, DUR, OPEN + ['G2 D3 B3 D4'], gain=0.07, cutoff=1500, rel=3.0)
    lute_arp(S('L11'), Se('L11') + 0.5, ['G2 D3 G3 B3', 'C3 G3 C4 E4', 'E2 B2 E3 G3', 'D3 A3 D4 F#4'], step=0.44, vel=0.15)
    choir(M('G3 D4 G4'), W('L11', 'abone') - 0.5, DUR, gain=0.1, att=1.0, rel=3.0, vowel='a')
    organ('G2 D3 G3', Se('L11') - 0.5, DUR, gain=0.06, att=1.0, rel=3.5, chiff=0.0)
    light(Se('L11') + 0.15, 'home', beat=min(0.5, max(0.3, (DUR - Se('L11') - 1.8) / 7.5)), inst='viol', gain=0.2)
    lute(DUR - 2.6, 'G2', vel=0.2, t60=3.0)
    lute(DUR - 2.6, 'D3', vel=0.15, t60=3.0)


SECTIONS = [a_hook, b_poet, c_light, d_war, e_king, f_gates, g_confession, h_eden, i_serpent, j_hiss, k_readings, l_tear]


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


PRIORITY = {'A01': 1.3, 'A02': 1.15, 'G07': 1.4, 'G09': 1.35, 'G09b': 1.35, 'G14': 1.3, 'I10': 1.4, 'J05': 1.2, 'L08b': 1.35, 'L09': 1.25, 'L10': 1.3, 'L11': 1.15}   # lines that must cut through


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
    a = We('J03', 'mi') + 0.35                 # the laugh's question dies away
    b = W('J05', 'tek') - 0.25                 # the hiss is the first thing heard again
    g = np.minimum(g, np.interp(tg, [a, a + 0.6, b, b + 0.05], [1.0, 0.0, 0.0, 1.0], left=1.0, right=1.0))
    g *= np.interp(tg, [DUR - 4.0, DUR - 0.05], [1.0, 0.0], left=1.0, right=0.0) ** 2
    return tg, g


def room_tone():
    """A barely audible empty hall under the J04 silence (so it is silence, not a dropout)."""
    a, b = We('J03', 'mi') + 0.35, W('J05', 'tek') + 0.6
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
