"""
sfx.py — "ŞARLKEN" için tamamen sentezlenmiş SFX kütüphanesi (numpy/scipy; harici ses dosyası YOK).

    sfx(name, seed=0, dur=None, loop=False, **kw) -> np.ndarray float32 (n, 2), 48 kHz, tepe = −3 dBFS

* Hepsi deterministik (aynı ad+seed → aynı örnekler). dur: istenen uzunluk (sn); verilmezse varsayılan.
* Döngü sesleri (crowd_murmur, sea_waves, wind, rain, fire_crackle): varsayılan 8 sn ve DİKİŞSİZ
  (dur verilirse döngü o uzunluğa dek tekrarlanır; loop=True bayrağı miks.py'de aynı anlama gelir).
* Her ses fiziksel olarak modellenir: filtrelenmiş gürültü + gövde sinüsleri/modlar + zarflar (düz 'bip' yok).
* chapter_stinger / title_hit / church_bell / bell_toll_low: root=<Hz> ile müziğin ana sesine akort edilebilir.

CLI: python3 sfx.py --list | --render ad [--out dosya.wav] | --all --out klasör
"""
import argparse
import os
import sys
from functools import lru_cache

import numpy as np

import ses_dsp as D
from ses_dsp import SR, rng_for

PEAK_DB = -3.0
LOOP_SEC = 8.0


# ═══════════════════════════ ortak yardımcılar ═══════════════════════════
def _n(sec):
    return int(round(sec * SR))


def _expd(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def _bpn(rng, n, lo, hi, order=2):
    return D.bp(rng.standard_normal(n), lo, hi, order)


def _place(buf, sig, t, gain=1.0, pan=0.0):
    """sig (mono) → buf (n,2) içine t sn'den itibaren ekler (sabit güç pan)."""
    i = int(round(t * SR))
    if i >= len(buf) or i + len(sig) <= 0:
        return
    if i < 0:
        sig, i = sig[-i:], 0
    m = min(len(sig), len(buf) - i)
    gl, gr = D.pan_gains(pan)
    buf[i:i + m, 0] += sig[:m] * gain * gl
    buf[i:i + m, 1] += sig[:m] * gain * gr


def _place_wrap(buf, sig, t, gain=1.0, pan=0.0):
    """Döngü tamponu için: taşan kısım başa sarar (dikişsiz)."""
    n = len(buf)
    i = int(round(t * SR)) % n
    gl, gr = D.pan_gains(pan)
    first = min(len(sig), n - i)
    buf[i:i + first, 0] += sig[:first] * gain * gl
    buf[i:i + first, 1] += sig[:first] * gain * gr
    rest = len(sig) - first
    if rest > 0:
        rest = min(rest, n)
        buf[:rest, 0] += sig[first:first + rest] * gain * gl
        buf[:rest, 1] += sig[first:first + rest] * gain * gr


def _stereo_noise(rng, n):
    return np.stack([rng.standard_normal(n), rng.standard_normal(n)], axis=1)


def _periodic_noise(rng, n, shape_fn):
    """FFT şekillendirmeli, n örnekte DÖNGÜSEL (dikişsiz) gürültü; shape_fn(freq_hz) genlik. Birim std."""
    X = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    X *= shape_fn(np.maximum(f, 1.0))
    X[0] = 0
    y = np.fft.irfft(X, n)
    return y / (np.std(y) + 1e-12)


def _pinkshape(lo=60.0, hi=9000.0):
    def fn(f):
        g = 1.0 / np.sqrt(f)
        g = g * (1 / (1 + (lo / f) ** 4)) * (1 / (1 + (f / hi) ** 4))
        return g
    return fn


def _bandshape(lo, hi, slope=4):
    def fn(f):
        return (1 / (1 + (lo / f) ** slope)) * (1 / (1 + (f / hi) ** slope))
    return fn


@lru_cache(maxsize=8)
def _room_ir(rt60, seed=21):
    return D.hall_ir(rt60, seed=seed, predelay=0.012)


def _room(x, wet=0.25, rt60=1.4):
    """x (n,2) → x + wet·reverb(x) (kuyruk eklenir). Küçük oda/salon rötuşu."""
    ir = _room_ir(float(rt60))
    w = D.reverb_wet(x, ir)
    out = np.zeros((len(w), 2))
    out[:len(x)] += x
    out += wet * w
    return out


def _fit(x, dur, loop=False):
    """x (n,2) → dur sn'ye kırp/uzat. Döngü ise dikişsiz tekrar; değilse kırpmada 40 ms sönüm, kısaysa sıfır doldur."""
    n = _n(dur)
    if loop:
        return D.tile_to(x, n)
    if len(x) >= n:
        y = x[:n].copy()
        return D.fade_edges(y, 0.0, min(0.04, dur / 3))
    return np.concatenate([x, np.zeros((n - len(x), 2))])


def _tame(x, crest_db):
    """Yumuşak tepe sınırlama: RMS'e göre crest_db üstünü tanh ile kıvırır (tek vuruşlu tepe diğer her şeyi bastırmasın)."""
    r = np.sqrt(np.mean(x ** 2)) + 1e-12
    T = r * 10 ** (crest_db / 20.0)
    return T * np.tanh(x / T)


CREST = {"tick": 26, "coin_clink": 24, "coin_pile": 22, "page_turn": 22, "paper_rustle": 20, "wax_seal_stamp": 24, "quill_scratch": 20,
         "sword_clash": 20, "heartbeat": 18, "horse_hooves": 20, "fire_crackle": 20}


def _finish(x, loop=False, name=None):
    """DC temizliği, kenar yumuşatma, tepe sınırlama, tepe −3 dBFS, float32 stereo."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    if not loop:
        x = D.sosfilt(D.biquad("hp", 18, 0, 0.7), x, axis=0)
        x = D.fade_edges(x, 0.0006, 0.012)
    x = _tame(x, CREST.get(name, 16))
    return D.peak_norm(x, PEAK_DB)


# ═══════════════════════════ kâğıt / yazı / mühür ═══════════════════════════
def _crinkles(rng, dur, rate, env_fn, lo=2200, hi=9500, amp=1.0):
    """Kâğıt buruşma tıkırtıları: Poisson olaylar × zarf; her biri kısa bantlı gürültü patlaması. (n,2)"""
    n = _n(dur)
    buf = np.zeros((n, 2))
    bank = []
    for c in np.exp(rng.uniform(np.log(lo), np.log(hi), 24)):
        L = int(rng.uniform(0.0015, 0.007) * SR)
        b = D.bp(rng.standard_normal(L + 64), c / 1.6, min(c * 1.6, 15000), 2)[:L] * np.exp(-np.arange(L) / (L * 0.28))
        bank.append(b / (np.max(np.abs(b)) + 1e-9))
    t = 0.0
    while t < dur:
        t += rng.exponential(1.0 / rate)
        e = env_fn(t)
        if rng.random() < e:
            b = bank[int(rng.integers(len(bank)))]
            _place(buf, b, t, amp * e * rng.lognormal(-0.2, 0.35), float(rng.uniform(-0.6, 0.6)))
    return buf


def _paper_rustle(rng, dur, **kw):
    dur = dur or 1.4
    n = _n(dur)
    ng = int(rng.integers(3, 6))
    cs = rng.uniform(0.1, 0.9, ng) * dur
    wd = rng.uniform(0.07, 0.18, ng) * dur

    def env(t):
        return float(min(1.0, sum(np.exp(-0.5 * ((t - c) / w) ** 2) for c, w in zip(cs, wd)) + 0.05))

    x = _crinkles(rng, dur, 170, env, amp=1.0)
    t = np.arange(n) / SR
    envc = np.array([env(tt) for tt in t[::480]])
    envf = np.interp(t, t[::480], envc)
    bed = _stereo_noise(rng, n)
    bed = D.bp(bed, 2500, 9000, 2) * (envf[:, None] ** 1.3) * 0.22
    x = x + bed
    return D.lp(x, 12000)


def _page_turn(rng, dur, **kw):
    dur = dur or 1.1
    n = _n(dur)
    t = np.arange(n) / SR
    mv = np.exp(-0.5 * ((t - 0.30) / 0.11) ** 2)
    sw = D.bp(_stereo_noise(rng, n), 1100, 5200, 2) * (mv[:, None] ** 1.2) * 0.9
    pan = np.clip((t - 0.15) / 0.3, 0, 1) * 1.2 - 0.6   # sol → sağ
    gl, gr = D.pan_gains(pan)
    sw = np.stack([sw[:, 0] * gl, sw[:, 1] * gr], axis=1)
    x = sw + _crinkles(rng, dur, 220, lambda tt: float(0.9 * np.exp(-0.5 * ((tt - 0.28) / 0.13) ** 2) + 0.04), amp=0.7)
    # kâğıt kenarı çırpma
    fl = D.hp(rng.standard_normal(int(0.02 * SR)), 1500, 2) * _expd(int(0.02 * SR), 0.004)
    _place(x, fl, 0.36, 1.3, 0.2)
    # sayfa iner: kısa tok ses
    th = D.lp(rng.standard_normal(int(0.08 * SR)), 450, 2) * _expd(int(0.08 * SR), 0.018)
    th = th + 0.6 * np.sin(D.PI2 * 105 * np.arange(len(th)) / SR) * _expd(len(th), 0.02)
    _place(x, th, 0.62, 0.55, 0.3)
    _place(x, D.bp(rng.standard_normal(int(0.03 * SR)), 1500, 4500, 2) * _expd(int(0.03 * SR), 0.006), 0.615, 0.35, 0.3)
    return D.lp(x, 11000)


def _wax_seal_stamp(rng, dur, **kw):
    dur = dur or 1.0
    n = _n(dur)
    x = np.zeros((n, 2))
    t = np.arange(int(0.5 * SR)) / SR
    thunk = (np.sin(D.PI2 * 150 * t) * np.exp(-t / 0.028) + 0.6 * np.sin(D.PI2 * 95 * t) * np.exp(-t / 0.05)
             + D.lp(rng.standard_normal(len(t)), 900, 2) * np.exp(-t / 0.015) * 0.9)
    _place(x, thunk, 0.0, 1.0, 0.0)
    nsq = int(0.45 * SR)
    ts = np.arange(nsq) / SR
    sq = D.bp(rng.standard_normal(nsq), 220, 1300, 2) * (1 - np.exp(-ts / 0.04)) * np.exp(-ts / 0.16)
    sq *= 1 + 0.4 * D.lp(rng.standard_normal(nsq), 60, 2) / 0.1
    _place(x, sq, 0.03, 0.55, 0.0)
    smack = D.bp(rng.standard_normal(int(0.02 * SR)), 900, 3400, 2) * _expd(int(0.02 * SR), 0.005)
    _place(x, smack, 0.045, 0.5, 0.0)
    rel = D.bp(rng.standard_normal(int(0.06 * SR)), 300, 1100, 2) * _expd(int(0.06 * SR), 0.02)
    _place(x, rel, 0.50, 0.25, 0.0)
    tck = D.bp(rng.standard_normal(int(0.012 * SR)), 1800, 4800, 2) * _expd(int(0.012 * SR), 0.003)
    _place(x, tck, 0.505, 0.5, 0.0)
    return D.lp(x, 9000)


def _quill_scratch(rng, dur, **kw):
    dur = dur or 2.4
    n = _n(dur)
    x = np.zeros((n, 2))
    t = 0.12
    while t < dur - 0.2:
        L = float(rng.uniform(0.09, 0.28))
        m = _n(L)
        ts = np.arange(m) / SR
        env = np.minimum(1.0, ts / 0.012) * np.minimum(1.0, (L - ts) / 0.03) * rng.uniform(0.5, 1.0)
        fc = rng.uniform(2300, 3400) * (1 + 0.18 * np.sin(np.pi * ts / L * rng.choice([1, -1])))
        w = rng.standard_normal(m)
        a = D.resonator_tv(w, fc, 900) * 1.3 + D.resonator_tv(w, fc * 1.65, 1400) * 0.8 + D.hp(w, 5200, 2) * 0.25
        grain = 0.55 + 0.45 * (D.lp(rng.standard_normal(m), 140, 2) / 0.12)
        _place(x, a * env * np.clip(grain, 0.1, 2.0), t, 1.0, float(rng.uniform(-0.15, 0.15)))
        t += L + float(rng.uniform(0.03, 0.2))
        if rng.random() < 0.18:
            t += float(rng.uniform(0.25, 0.5))
    return D.lp(x, 9500)


# ═══════════════════════════ metal / para ═══════════════════════════
def _coin_ring(rng, f0=None, tau=None):
    f0 = f0 or float(rng.uniform(2600, 4700))
    d = float(rng.uniform(0.08, 0.20)) if tau is None else tau
    n = int(min(d * 8.0, 1.2) * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for r, a, tf in [(1.0, 1.0, 1.0), (1.52, 0.6, 0.7), (2.39, 0.42, 0.45), (3.07, 0.3, 0.3), (4.13, 0.16, 0.2)]:
        fr = f0 * r * (1 + rng.uniform(-0.01, 0.01))
        if fr < 17000:
            y += a * np.sin(D.PI2 * fr * t + rng.uniform(0, D.PI2)) * np.exp(-t / (d * tf))
    y += 0.8 * D.bp(rng.standard_normal(n), 3000, 9000, 2) * np.exp(-t / 0.0025)
    return y


def _coin_clink(rng, dur, **kw):
    dur = dur or 0.9
    n = _n(dur)
    x = np.zeros((n, 2))
    k = int(rng.integers(2, 4))
    t = 0.0
    for i in range(k):
        _place(x, _coin_ring(rng), t, (1.0 - 0.25 * i) * rng.uniform(0.8, 1.0), float(rng.uniform(-0.5, 0.5)))
        t += float(rng.uniform(0.07, 0.22))
    return D.lp(x, 14000)


def _coin_pile(rng, dur, **kw):
    dur = dur or 2.8
    n = _n(dur)
    x = np.zeros((n, 2))
    nev = int(18 * dur + 30)
    ts = np.sort(dur * 0.9 * rng.beta(0.8, 2.2, nev))
    for t in ts:
        _place(x, _coin_ring(rng, tau=float(rng.uniform(0.04, 0.22))), float(t), float(rng.lognormal(-1.0, 0.7)) * (1.0 - 0.4 * t / dur), float(rng.uniform(-0.8, 0.8)))
    sl = D.bp(_stereo_noise(rng, n), 2500, 7500, 2) * np.exp(-np.arange(n) / (0.9 * SR))[:, None] * 0.06
    x += sl
    th = D.bp(rng.standard_normal(int(0.05 * SR)), 350, 1000, 2) * _expd(int(0.05 * SR), 0.015)
    _place(x, th, 0.0, 0.5, 0.0)
    return D.lp(x, 14000)


def _sword_clash(rng, dur, **kw):
    dur = dur or 1.8
    n = _n(dur)
    x = np.zeros((n, 2))
    hits = max(1, int(dur / 0.55))
    t = 0.0
    for h in range(min(hits, 4)):
        f0 = float(rng.uniform(750, 1350))
        m = int(1.2 * SR)
        ts = np.arange(m) / SR
        y = np.zeros(m)
        for r, a, tau in [(1.0, 1.0, 0.30), (2.76, 0.8, 0.20), (5.40, 0.55, 0.12), (8.93, 0.35, 0.07), (13.3, 0.18, 0.04)]:
            if f0 * r < 18000:
                y += a * np.sin(D.PI2 * f0 * r * ts + rng.uniform(0, 6.28)) * np.exp(-ts / tau)
        y += 1.4 * D.bp(rng.standard_normal(m), 1800, 9500, 2) * np.exp(-ts / 0.012)
        y += 0.9 * D.bp(rng.standard_normal(m), 600, 2500, 2) * np.exp(-ts / 0.03)
        sc = int(0.22 * SR)
        tsc = np.arange(sc) / SR
        sweep = np.zeros(sc)
        fcs = np.linspace(2500, 7500, 12)
        for i, c in enumerate(fcs):
            g = np.exp(-0.5 * ((tsc - (i + 0.5) / 12 * 0.2) / 0.03) ** 2)
            sweep += D.resonator(rng.standard_normal(sc), c, 600) * g
        _place(x, y, t, (1.0 - 0.18 * h) * rng.uniform(0.85, 1.0), float(rng.uniform(-0.3, 0.3)))
        _place(x, sweep, t + 0.012, 0.55, float(rng.uniform(-0.3, 0.3)))
        t += float(rng.uniform(0.28, 0.55))
        if t > dur - 0.5:
            break
    return _room(D.lp(x, 15000), 0.18, 0.7)[:n]


# ═══════════════════════════ patlama / gök / hava ═══════════════════════════
def _cannon_boom(rng, dur, **kw):
    dur = dur or 6.0
    n = _n(dur)
    x = np.zeros((n, 2))
    m = _n(min(dur, 3.0))
    t = np.arange(m) / SR
    f = 30 + 55 * np.exp(-t / 0.12)
    body = np.sin(D.PI2 * np.cumsum(f) / SR) * np.exp(-t / 0.28)
    blast = D.lp(rng.standard_normal(m), 2200, 2) * np.exp(-t / 0.07) * 1.5
    blast += D.hp(rng.standard_normal(m), 2500, 2) * np.exp(-t / 0.012) * 0.8
    mid = D.bp(rng.standard_normal(m), 140, 1100, 2) * np.exp(-t / 0.13) * 2.2
    rum = D.bp(rng.standard_normal(m), 60, 260, 2) * np.exp(-t / 0.9) * (1.0 + 0.5 * np.sin(D.PI2 * 7 * t)) * 2.6
    core = body * 0.9 + blast + mid + rum
    core = np.tanh(1.2 * core)
    _place(x, core, 0.02, 1.0, 0.0)
    for _ in range(int(rng.integers(5, 10))):
        tt = float(rng.uniform(0.3, 1.6))
        b = D.bp(rng.standard_normal(int(0.02 * SR)), 600, 3500, 2) * _expd(int(0.02 * SR), 0.005)
        _place(x, b, tt, float(rng.uniform(0.05, 0.18)), float(rng.uniform(-0.7, 0.7)))
    for dt, g, fc, pn in [(0.85, 0.40, 900, -0.6), (1.75, 0.26, 600, 0.6), (2.9, 0.16, 420, -0.3)]:
        if dt + 0.5 >= dur:
            continue
        e = D.lp(core[:int(2.2 * SR)], fc, 2)
        e = e * np.exp(-np.arange(len(e)) / (0.9 * SR))
        _place(x, e, dt, g, pn)
    return _room(x, 0.12, 2.0)[:n]


def _thunder(rng, dur, **kw):
    dur = dur or 7.0
    n = _n(dur)
    t = np.arange(n) / SR
    nz = _stereo_noise(rng, n)
    # yuvarlanan gürleme zarfı: art arda tümsekler + yavaş sönüm
    env = np.zeros(n)
    k = int(rng.integers(6, 10))
    for i in range(k):
        t0 = 0.25 + (i / max(k - 1, 1)) ** 1.3 * dur * 0.55 + rng.uniform(-0.1, 0.25)
        a = rng.uniform(0.35, 1.0) * (1 - 0.6 * t0 / dur)
        env += a * np.exp(-np.maximum(t - t0, 0) / rng.uniform(0.45, 1.5)) * (t >= t0) * (1 - np.exp(-np.maximum(t - t0, 0) / rng.uniform(0.06, 0.25)))
    env += 0.5 * np.exp(-t / 2.2) * (1 - np.exp(-t / 0.15))
    env = env / env.max()
    sub = D.bp(nz, 28, 120, 2) * (env[:, None] ** 0.8) * 2.0
    low = D.bp(nz, 100, 420, 2) * env[:, None] * 2.4
    mid = D.bp(nz, 400, 1600, 2) * (env[:, None] ** 2.2) * 1.2 * (1 - D.smoothstep((t - 2.8) / 2.0))[:, None]
    crack = D.hp(_stereo_noise(rng, n), 700, 2) * (np.exp(-np.maximum(t - 0.12, 0) / 0.05) * (t >= 0.12))[:, None] * 0.9
    cr2 = D.bp(_stereo_noise(rng, n), 1500, 6000, 2) * (np.exp(-np.maximum(t - 0.35, 0) / 0.08) * (t >= 0.35))[:, None] * 0.35
    out = sub + low + mid + crack + cr2
    return _room(out, 0.12, 2.2)[:n]


def _whoosh(rng, dur, long=False, **kw):
    dur = dur or (2.6 if long else 0.9)
    n = _n(dur)
    t = np.arange(n) / SR
    u = t / dur
    nz = _stereo_noise(rng, n)
    out = np.zeros((n, 2))
    nb = 16
    fc0, fc1 = (250, 5200) if long else (350, 4200)
    cs = np.exp(np.linspace(np.log(fc0), np.log(fc1), nb))
    for i, c in enumerate(cs):
        pos = ((i + 0.5) / nb) ** (1.2 if long else 1.0) * 0.55 + 0.08
        g = np.exp(-0.5 * ((u - pos) / (0.12 if long else 0.17)) ** 2)
        out += D.bp(nz, c / 1.3, min(c * 1.3, 15000), 2) * g[:, None]
    env = np.sin(np.pi * np.clip(u, 0, 1)) ** (1.4 if long else 1.0)
    out *= env[:, None]
    pan = (np.clip(u, 0, 1) * 2 - 1) * 0.85
    gl, gr = D.pan_gains(pan)
    out = np.stack([out[:, 0] * gl, out[:, 1] * gr], axis=1)
    if long:
        sub = np.sin(D.PI2 * np.cumsum(45 + 40 * u ** 1.5) / SR) * env * 0.35
        out += np.stack([sub, sub], axis=1)
    return D.hp(out, 90, 2)


def _church_bell(rng, dur, root=None, **kw):
    dur = dur or 7.0
    f = float(root or 392.0)
    y = D.bell_tone(f, min(dur + 1.0, 9.0), 1.0, rng, ring=1.1, strike=0.55)
    x = np.stack([y * 0.95, y * 1.0], axis=1)
    return _room(x, 0.35, 1.8)[:_n(dur)]


def _bell_toll_low(rng, dur, root=None, **kw):
    dur = dur or 7.5
    f = float(root or 110.0)
    y = D.bell_tone(f, min(dur + 1.0, 9.0), 1.0, rng, ring=2.2, strike=0.7)
    x = np.stack([y, y * 0.97], axis=1)
    x[:, 0] += 0.25 * np.roll(y, int(0.0006 * SR))
    return _room(x, 0.4, 2.2)[:_n(dur)]


def _gong_hit(rng, dur, root=None, **kw):
    dur = dur or 7.0
    f = float(root or 110.0)
    y = D.gong_tone(f, min(dur + 1.0, 9.5), 1.0, rng)
    y2 = D.gong_tone(f, min(dur + 1.0, 9.5), 1.0, rng_for("gong2", rng.integers(1 << 30)))
    x = np.stack([y, 0.6 * y + 0.4 * y2], axis=1)
    return _room(x, 0.28, 2.0)[:_n(dur)]


def _drum_hit(rng, dur, **kw):
    dur = dur or 1.6
    n = _n(dur)
    t = np.arange(n) / SR
    f = 46 + 40 * np.exp(-t / 0.05)
    body = np.sin(D.PI2 * np.cumsum(f) / SR) * np.exp(-t / 0.40)
    body += 0.55 * np.sin(D.PI2 * np.cumsum(f * 1.5) / SR) * np.exp(-t / 0.20)
    mid = np.sin(D.PI2 * np.cumsum(120 + 60 * np.exp(-t / 0.04)) / SR) * np.exp(-t / 0.16) * 0.9
    slap = D.bp(rng.standard_normal(n), 250, 2400, 2) * np.exp(-t / 0.025) * 1.7
    skin = D.hp(rng.standard_normal(n), 1800, 2) * np.exp(-t / 0.008) * 0.6
    y = np.tanh(1.1 * (body * 0.8 + mid + slap + skin))
    x = np.stack([y, y], axis=1)
    return _room(x, 0.22, 1.2)[:n]


def _heartbeat(rng, dur, bpm=64, **kw):
    dur = dur or 4.0
    n = _n(dur)
    x = np.zeros((n, 2))
    per = 60.0 / bpm
    t = 0.05
    while t < dur - 0.4:
        for dt, a, f0 in [(0.0, 1.0, 66.0), (0.29, 0.72, 58.0)]:
            m = _n(0.35)
            ts = np.arange(m) / SR
            f = f0 * (1 + 0.5 * np.exp(-ts / 0.03))
            y = np.sin(D.PI2 * np.cumsum(f) / SR) * np.exp(-ts / 0.075)
            y += D.bp(rng.standard_normal(m), 90, 420, 2) * np.exp(-ts / 0.035) * 1.4
            y += 0.5 * np.sin(D.PI2 * 2.0 * f0 * ts) * np.exp(-ts / 0.04)
            _place(x, y * np.minimum(1.0, ts / 0.004), t + dt, a * rng.uniform(0.92, 1.0), 0.0)
        t += per
    return D.lp(x, 900)


def _gate_thud(rng, dur, **kw):
    dur = dur or 2.6
    n = _n(dur)
    x = np.zeros((n, 2))
    t = np.arange(n) / SR
    body = np.sin(D.PI2 * np.cumsum(48 + 40 * np.exp(-t / 0.06)) / SR) * np.exp(-t / 0.36)
    wood = D.bp(rng.standard_normal(n), 120, 900, 2) * np.exp(-t / 0.10) * 2.4
    wood += D.resonator(rng.standard_normal(n), 230, 90) * np.exp(-t / 0.14) * 2.4
    wood += D.resonator(rng.standard_normal(n), 420, 130) * np.exp(-t / 0.08) * 1.5
    imp = D.bp(rng.standard_normal(int(0.03 * SR)), 500, 3500, 2) * _expd(int(0.03 * SR), 0.006) * 1.0
    y = body * 0.9 + wood
    _place(x, y, 0.0, 1.0, 0.0)
    _place(x, imp, 0.0, 0.8, 0.0)
    for k in range(int(rng.integers(4, 8))):   # demir halka/zincir şıngırtısı
        c = float(rng.uniform(1500, 4200))
        m = int(0.25 * SR)
        ts = np.arange(m) / SR
        ring = np.sin(D.PI2 * c * ts) * np.exp(-ts / rng.uniform(0.03, 0.1)) * rng.uniform(0.08, 0.3)
        _place(x, ring, float(rng.uniform(0.04, 0.45)), 1.0, float(rng.uniform(-0.5, 0.5)))
    lat = D.bp(rng.standard_normal(int(0.04 * SR)), 800, 4000, 2) * _expd(int(0.04 * SR), 0.008)
    _place(x, lat, 0.33, 0.45, 0.2)
    ru = D.lp(_stereo_noise(rng, n), 130, 2) * np.exp(-t / 0.9)[:, None] * 0.8
    x += ru
    return _room(x, 0.3, 1.6)[:n]


def _tick(rng, dur, **kw):
    dur = dur or 0.3
    n = _n(dur)
    t = np.arange(n) / SR
    f = float(rng.uniform(1900, 2500))
    y = np.sin(D.PI2 * f * t) * np.exp(-t / 0.012) + 0.5 * np.sin(D.PI2 * f * 2.43 * t) * np.exp(-t / 0.007)
    y += D.bp(rng.standard_normal(n), 2500, 9000, 2) * np.exp(-t / 0.0018) * 1.6
    y += 0.5 * np.sin(D.PI2 * 410 * t) * np.exp(-t / 0.02)
    x = np.stack([y, y], axis=1)
    return _room(x, 0.10, 0.5)[:n]


# ═══════════════════════════ ritimli / müzikal vurgular ═══════════════════════════
def _horse_hooves(rng, dur, kind="gallop", **kw):
    dur = dur or 4.0
    n = _n(dur)
    x = np.zeros((n, 2))
    P = 0.40 if kind == "gallop" else 0.55
    offs, amps = ([0.0, 0.10, 0.19, 0.30], [0.9, 0.7, 0.8, 1.0]) if kind == "gallop" else ([0.0, 0.27], [1.0, 0.85])
    t = 0.08
    while t < dur - 0.3:
        u = t / dur
        dist = 0.25 + 0.75 * np.sin(np.pi * np.clip(u * 0.9 + 0.05, 0, 1)) ** 1.2   # yaklaş-uzaklaş
        pan = (u * 2 - 1) * 0.8
        for o, a in zip(offs, amps):
            tt = t + o + rng.normal(0, 0.005)
            m = int(0.25 * SR)
            ts = np.arange(m) / SR
            thud = np.sin(D.PI2 * 135 * ts * (1 + 0.3 * np.exp(-ts / 0.02))) * np.exp(-ts / 0.03)
            thud += D.bp(rng.standard_normal(m), 180, 1000, 2) * np.exp(-ts / 0.022) * 1.2
            clack = D.bp(rng.standard_normal(m), 1500, 4500, 2) * np.exp(-ts / 0.004) * 0.9
            clack += 0.5 * np.sin(D.PI2 * rng.uniform(3000, 3600) * ts) * np.exp(-ts / 0.015)
            y = thud + clack * (0.5 + 0.5 * dist)
            _place(x, D.lp(y, 3000 + 5000 * dist), tt, a * dist * rng.uniform(0.85, 1.0), pan)
        t += P * rng.uniform(0.97, 1.03)
    return _room(x, 0.2, 0.9)[:n]


def _chime_tone(f, dur, rng, bright=1.0):
    n = _n(dur)
    t = np.arange(n) / SR
    y = np.sin(D.PI2 * f * t) * np.exp(-t / (dur * 0.30))
    y += 0.35 * bright * np.sin(D.PI2 * f * 2.0 * t + 0.3) * np.exp(-t / (dur * 0.18))
    y += 0.2 * bright * np.sin(D.PI2 * f * 2.76 * t) * np.exp(-t / (dur * 0.10))
    y += 0.08 * bright * np.sin(D.PI2 * f * 5.4 * t) * np.exp(-t / (dur * 0.05))
    y += 0.25 * np.sin(D.PI2 * (f + 0.6) * t) * np.exp(-t / (dur * 0.26))
    return y * np.minimum(1.0, t / 0.003)


def _magic_chime(rng, dur, root=None, **kw):
    dur = dur or 2.6
    n = _n(dur)
    f = float(root or 587.33)    # D5
    notes = [f, f * 2 ** (4 / 12) * 1.0, f * 2 ** (9 / 12)]  # D, F#, B → yumuşak, parlak majör altılı
    x = np.zeros((n, 2))
    for i, nf in enumerate(notes):
        _place(x, _chime_tone(nf, 2.0, rng), 0.0 + 0.2 * i, 1.0 - 0.1 * i, (-0.3, 0.0, 0.3)[i])
    sh = np.zeros(n)
    t = np.arange(n) / SR
    for k, nf in enumerate((f * 2, f * 2 * 1.26, f * 2 * 1.68)):
        sh += np.sin(D.PI2 * nf * t + rng.uniform(0, 6)) * np.exp(-t / 1.1) * (1 - np.exp(-t / 0.25)) * 0.07
    x[:, 0] += sh
    x[:, 1] += sh * 0.8
    return _room(x, 0.35, 1.8)[:n]


def _golden_chord(rng, root_hz, dur, organ=1.0, gong=0.5, bell=0.5, attack=0.05, release=1.3, voicing=(0, 7, 12, 16, 19)):
    """Org akoru (+ gong + çan): D majör açık dizilim (kök, beşli, oktav, majör üçlü, beşli+8)."""
    n = _n(dur)
    x = np.zeros((n, 2))
    pans = [-0.15, 0.15, -0.3, 0.3, 0.0]
    for i, st in enumerate(voicing):
        f = root_hz * 2 ** (st / 12)
        tab = D.additive_table(f, lambda ff: (f / ff) ** 1.3 / (1 + (ff / 4800.0) ** 4), rng, phase="random")
        y = D.wt_osc(tab, f * (1 + rng.uniform(-0.0004, 0.0004)), n, phase0=rng.random())
        tab2 = D.additive_table(f * 2, lambda ff: (f * 2 / ff) ** 1.8, rng, phase="random")
        y += 0.35 * D.wt_osc(tab2, f * 2, n, phase0=rng.random())
        y *= D.adsr(n, attack, 0.2, 0.85, release)
        gl, gr = D.pan_gains(pans[i % 5])
        x[:, 0] += y * gl * organ * (1.0 if i else 1.3)
        x[:, 1] += y * gr * organ * (1.0 if i else 1.3)
    if gong > 0:
        g = D.gong_tone(root_hz * 1.0, dur, 1.0, rng, bloom=1.1)
        x += gong * np.stack([g, g * 0.85], axis=1) * 0.9
    if bell > 0:
        for k, (st, dt, a) in enumerate([(24, 0.12, 1.0), (31, 0.30, 0.6), (28, 0.5, 0.5)]):
            b = D.bell_tone(root_hz * 2 ** (st / 12), dur - dt, 1.0, rng, ring=1.2, strike=0.4)
            _place(x, b / (np.max(np.abs(b)) + 1e-9), dt, bell * a * 0.5, (-0.3, 0.3, 0.1)[k])
    return x


def _chapter_stinger(rng, dur, root=None, **kw):
    dur = dur or 2.5
    r = float(root or 146.83)
    x = _golden_chord(rng, r, dur, organ=1.0, gong=0.45, bell=0.55, attack=0.07, release=1.2)
    return _room(x, 0.25, 1.8)[:_n(dur)]


def _title_hit(rng, dur, root=None, **kw):
    dur = dur or 5.0
    n = _n(dur)
    r = float(root or 73.42)
    x = np.zeros((n, 2))
    sb = D.sub_boom(r * 1.06, r * 0.42, dur, 1.0)
    x += np.stack([sb, sb], axis=1) * 0.55
    g = D.gong_tone(r * 2, dur, 1.0, rng, bloom=1.3)
    g2 = D.gong_tone(r * 2, dur, 1.0, rng_for("title", int(rng.integers(1 << 30))), bloom=1.3)
    x += np.stack([g, 0.55 * g + 0.45 * g2], axis=1) * 1.0
    tm = D.timpani_hit(r, 1.0, rng, dur=min(dur, 3.2))
    _place(x, tm, 0.0, 0.9, 0.0)
    for k, (st, dt, a) in enumerate([(36, 0.05, 1.0), (43, 0.18, 0.7), (40, 0.30, 0.6), (48, 0.46, 0.4), (52, 0.62, 0.3)]):
        d0 = min(dur - dt, 4.2)
        b = D.bell_tone(r * 2 ** (st / 12), d0, 1.0, rng, ring=1.6, strike=0.3)
        _place(x, b / (np.max(np.abs(b)) + 1e-9), dt, a * 0.40, ((-1) ** k) * 0.35)
    t = np.arange(n) / SR
    sh = np.zeros(n)
    for st in (48, 52, 55, 60):
        sh += np.sin(D.PI2 * r * 2 ** (st / 12) * t + rng.uniform(0, 6)) * (1 - np.exp(-t / 0.4)) * np.exp(-t / 1.6) * 0.05
    x[:, 0] += sh
    x[:, 1] += sh
    return _room(x, 0.18, 2.2)[:n]


# ═══════════════════════════ döngüsel dokular (8 sn, dikişsiz) ═══════════════════════════
def _crowd_murmur(rng, dur, **kw):
    n = _n(dur)
    x = np.zeros((n, 2))
    vowels = [(700, 1100, 2600), (450, 800, 2500), (350, 700, 2400), (500, 1700, 2500), (400, 1900, 2700), (600, 1000, 2500)]
    nv = 22
    for v in range(nv):
        f0 = float(rng.uniform(95, 250))
        pan = float(rng.uniform(-0.9, 0.9))
        amp = float(rng.uniform(0.4, 1.0))
        t = float(rng.uniform(0, 0.3))
        while t < dur:
            L = float(rng.uniform(0.08, 0.24))
            m = _n(L) + 400
            ts = np.arange(m) / SR
            fr = f0 * (1 + 0.07 * np.sin(D.PI2 * 3.2 * ts + rng.uniform(0, 6)) + float(rng.uniform(-0.12, 0.12)))
            ph = np.cumsum(fr) / SR
            src = (2 * (ph % 1) - 1) * 0.6 + 0.4 * rng.standard_normal(m) * 0.15
            f1, f2, f3 = vowels[int(rng.integers(len(vowels)))]
            y = D.resonator(src, f1, 110) + 0.7 * D.resonator(src, f2, 140) + 0.3 * D.resonator(src, f3, 220)
            env = np.sin(np.pi * np.clip(np.arange(m) / (m - 400), 0, 1)) ** 1.5
            y = y[:m] * env
            _place_wrap(x, y, t, amp * float(rng.uniform(0.5, 1.0)), pan)
            t += L + float(rng.exponential(0.12)) + (float(rng.uniform(0.3, 0.9)) if rng.random() < 0.10 else 0.0)
    bed = np.stack([_periodic_noise(rng, n, _bandshape(160, 1800, 4)), _periodic_noise(rng, n, _bandshape(160, 1800, 4))], axis=1)
    x = x / (np.std(x) + 1e-9) + 0.35 * bed / (np.std(bed) + 1e-9)
    x = D.periodic_filter(np.concatenate([D.biquad("lp", 3800, 0, 0.7), D.biquad("lp", 3800, 0, 0.7)]), x)
    return x


def _sea_waves(rng, dur, **kw):
    n = _n(dur)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    centers = [0.22 * dur + rng.uniform(-0.1, 0.1), 0.68 * dur + rng.uniform(-0.1, 0.1)]
    amps = [1.0, 0.65]
    for ch in range(2):
        low = _periodic_noise(rng, n, _bandshape(40, 380, 2))
        mid = _periodic_noise(rng, n, _bandshape(350, 2200, 2))
        hi = _periodic_noise(rng, n, _bandshape(2000, 8000, 3))
        env_l = np.zeros(n)
        env_m = np.zeros(n)
        env_h = np.zeros(n)
        for c, a in zip(centers, amps):
            d = ((t - c + dur / 2) % dur) - dur / 2     # dairesel zaman farkı
            rise = np.exp(-0.5 * (d / 1.1) ** 2) * (d < 0) + np.exp(-0.5 * (d / 1.9) ** 2) * (d >= 0)
            wash = np.where(d >= -0.15, np.exp(-np.maximum(d, 0) / 1.6) * (1 - np.exp(-np.maximum(d + 0.15, 0) / 0.2)), 0.0)
            env_l += a * rise
            env_m += a * (rise ** 1.4)
            env_h += a * (wash * 0.9 + rise ** 3 * 0.35)
        out[:, ch] = low * (0.08 + env_l) * 0.9 + mid * (0.03 + env_m) * 0.8 + hi * env_h * 0.5
    return out


def _wind(rng, dur, **kw):
    n = _n(dur)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    gust = 0.55 + 0.25 * np.sin(D.PI2 * t / dur + 0.7) + 0.15 * np.sin(D.PI2 * 3 * t / dur + 2.0) + 0.1 * np.sin(D.PI2 * 5 * t / dur)
    base = np.stack([_periodic_noise(rng, n, _bandshape(90, 1100, 2)), _periodic_noise(rng, n, _bandshape(90, 1100, 2))], axis=1)
    hi = np.stack([_periodic_noise(rng, n, _bandshape(900, 4200, 2)), _periodic_noise(rng, n, _bandshape(900, 4200, 2))], axis=1)
    out = base * (gust[:, None] ** 1.3) + hi * (gust[:, None] ** 3) * 0.35
    # ıslık: dar rezonans, yavaş kayan
    fc = 1050 + 280 * np.sin(D.PI2 * 2 * t / dur) + 120 * np.sin(D.PI2 * 3 * t / dur + 1)
    wh = np.zeros(n)
    blk = 480
    z = np.zeros(2)
    w0 = rng.standard_normal(3 * n)
    # 3 kopya üzerinde süz → ortası dikişsiz
    fc3 = np.tile(fc, 3)
    y = np.zeros(3 * n)
    zi = np.zeros(2)
    for i in range(0, 3 * n, blk):
        f = fc3[i]
        r = np.exp(-np.pi * 50.0 / SR)
        th = D.PI2 * f / SR
        a = [1.0, -2 * r * np.cos(th), r * r]
        b = [(1 - r) * 0.6]
        seg, zi = D.lfilter(b, a, w0[i:i + blk], zi=zi)
        y[i:i + blk] = seg
    wh = y[n:2 * n] * (gust ** 2.2)
    out[:, 0] += wh * 0.55
    out[:, 1] += np.roll(wh, int(0.011 * SR)) * 0.55
    return out


def _rain(rng, dur, **kw):
    n = _n(dur)
    out = np.zeros((n, 2))
    for ch in range(2):
        hiss = _periodic_noise(rng, n, _bandshape(1800, 11000, 2))
        mid = _periodic_noise(rng, n, _bandshape(350, 1400, 2))
        mod = 1 + 0.12 * D.lp(rng.standard_normal(n), 6, 1) / 0.05
        out[:, ch] = hiss * 0.8 * np.clip(mod, 0.5, 1.5) + mid * 0.25
    drops = np.zeros((n, 2))
    bank = []
    for c in np.exp(rng.uniform(np.log(1800), np.log(7500), 20)):
        L = int(0.006 * SR)
        b = D.bp(rng.standard_normal(L + 32), c / 1.4, min(c * 1.4, 14000), 2)[:L] * np.exp(-np.arange(L) / (0.0016 * SR))
        bank.append(b / (np.max(np.abs(b)) + 1e-9))
    for _ in range(int(dur * 260)):
        _place_wrap(drops, bank[int(rng.integers(len(bank)))], float(rng.uniform(0, dur)), float(rng.lognormal(-1.2, 0.8)), float(rng.uniform(-0.9, 0.9)))
    big = []
    for c in (420, 560, 760):
        L = int(0.03 * SR)
        ts = np.arange(L) / SR
        big.append(np.sin(D.PI2 * c * ts * (1 + 0.5 * np.exp(-ts / 0.006))) * np.exp(-ts / 0.007))
    for _ in range(int(dur * 14)):
        _place_wrap(drops, big[int(rng.integers(3))], float(rng.uniform(0, dur)), float(rng.uniform(0.15, 0.4)), float(rng.uniform(-0.8, 0.8)))
    return out + drops * 0.5


def _fire_crackle(rng, dur, **kw):
    n = _n(dur)
    out = np.zeros((n, 2))
    for ch in range(2):
        bed = _periodic_noise(rng, n, _bandshape(70, 420, 2))
        t = np.arange(n) / SR
        flick = 0.6 + 0.25 * np.sin(D.PI2 * 3 * t / dur + rng.uniform(0, 6)) + 0.15 * np.sin(D.PI2 * 7 * t / dur + rng.uniform(0, 6))
        rush = _periodic_noise(rng, n, _bandshape(250, 1600, 2)) * 0.25
        out[:, ch] = bed * flick * 0.7 + rush * flick ** 2
    for _ in range(int(dur * 28)):
        c = float(np.exp(rng.uniform(np.log(1200), np.log(7000))))
        L = int(rng.uniform(0.001, 0.004) * SR) + 40
        b = D.bp(rng.standard_normal(L + 32), c / 1.5, min(c * 1.5, 14000), 2)[:L] * np.exp(-np.arange(L) / (L * 0.3))
        _place_wrap(out, b / (np.max(np.abs(b)) + 1e-9), float(rng.uniform(0, dur)), float(rng.lognormal(-1.8, 0.7)), float(rng.uniform(-0.8, 0.8)))
    for _ in range(int(dur * 1.6)):
        L = int(0.012 * SR)
        ts = np.arange(L) / SR
        b = D.bp(rng.standard_normal(L + 32), 500, 3000, 2)[:L] * np.exp(-ts / 0.003) + 0.6 * np.sin(D.PI2 * rng.uniform(180, 320) * ts) * np.exp(-ts / 0.006)
        _place_wrap(out, b / (np.max(np.abs(b)) + 1e-9), float(rng.uniform(0, dur)), float(rng.uniform(0.15, 0.45)), float(rng.uniform(-0.6, 0.6)))
    for _ in range(int(dur * 0.35)):
        L = int(0.02 * SR)
        b = D.hp(rng.standard_normal(L + 32), 3000, 2)[:L] * np.exp(-np.arange(L) / (0.004 * SR))
        _place_wrap(out, b / (np.max(np.abs(b)) + 1e-9), float(rng.uniform(0, dur)), float(rng.uniform(0.3, 0.6)), float(rng.uniform(-0.7, 0.7)))
    return out


def _ship_creak(rng, dur, **kw):
    dur = dur or 3.2
    n = _n(dur)
    t = np.arange(n) / SR
    x = np.zeros((n, 2))
    nc = int(rng.integers(2, 4))
    for k in range(nc):
        t0 = float(rng.uniform(0.0, max(dur - 1.4, 0.1)))
        L = float(rng.uniform(0.7, 1.4))
        m = _n(L)
        ts = np.arange(m) / SR
        u = ts / L
        f0 = float(rng.uniform(150, 260))
        fr = f0 * (1 + 0.35 * np.sin(np.pi * u) + 0.08 * D.lp(rng.standard_normal(m), 12, 1) / 0.03)
        # taş-kayma: darbe katarı
        rate = 22 + 14 * np.sin(np.pi * u) + 6 * D.lp(rng.standard_normal(m), 5, 1) / 0.03
        pulse = (np.cumsum(rate) / SR) % 1.0
        saw = 2 * (np.cumsum(fr) / SR % 1.0) - 1
        gate = np.clip(1.0 - pulse * 1.6, 0, 1) ** 0.7
        y = saw * gate
        y = D.resonator_tv(y, 620 + 380 * u, 220) * 3.0 + D.resonator_tv(y, 1250 + 500 * u, 300) * 1.4 + 0.5 * D.lp(y, 400, 2)
        env = np.sin(np.pi * np.clip(u, 0, 1)) ** 0.8 * (0.6 + 0.4 * D.lp(rng.standard_normal(m), 9, 1) / 0.04)
        gr = np.sin(D.PI2 * 74 * ts) * np.sin(np.pi * u) ** 2 * 0.25
        _place(x, (y * 0.35 + gr) * env, t0, rng.uniform(0.7, 1.0), float(rng.uniform(-0.4, 0.4)))
    kn = int(rng.integers(2, 5))
    for _ in range(kn):
        c = float(rng.uniform(180, 420))
        m = int(0.12 * SR)
        ts = np.arange(m) / SR
        kk = np.sin(D.PI2 * c * ts) * np.exp(-ts / 0.025) + D.bp(rng.standard_normal(m), 400, 1600, 2) * np.exp(-ts / 0.01) * 0.6
        _place(x, kk, float(rng.uniform(0.1, dur - 0.3)), float(rng.uniform(0.12, 0.35)), float(rng.uniform(-0.5, 0.5)))
    return _room(D.lp(x, 6000), 0.2, 0.8)[:n]


# ═══════════════════════════ kayıt defteri ═══════════════════════════
REGISTRY = {
    "paper_rustle": _paper_rustle, "page_turn": _page_turn, "wax_seal_stamp": _wax_seal_stamp, "quill_scratch": _quill_scratch,
    "coin_clink": _coin_clink, "coin_pile": _coin_pile, "sword_clash": _sword_clash, "cannon_boom": _cannon_boom,
    "crowd_murmur": _crowd_murmur, "sea_waves": _sea_waves, "ship_creak": _ship_creak, "wind": _wind, "rain": _rain,
    "thunder": _thunder, "church_bell": _church_bell, "horse_hooves": _horse_hooves, "fire_crackle": _fire_crackle,
    "gate_thud": _gate_thud, "whoosh": lambda rng, dur, **kw: _whoosh(rng, dur, False), "whoosh_long": lambda rng, dur, **kw: _whoosh(rng, dur, True),
    "gong_hit": _gong_hit, "heartbeat": _heartbeat, "chapter_stinger": _chapter_stinger, "title_hit": _title_hit,
    "tick": _tick, "bell_toll_low": _bell_toll_low, "drum_hit": _drum_hit, "magic_chime": _magic_chime,
}
LOOPABLE = {"crowd_murmur", "sea_waves", "wind", "rain", "fire_crackle"}
# varsayılan kuyruklu sesler için "doğal" uzunluklar (dur=None)
SFX_NAMES = sorted(REGISTRY)


def sfx(name, seed=0, dur=None, loop=False, **kw):
    """SFX üretir → float32 (n,2) @48 kHz, tepe −3 dBFS. Döngü sesleri: dur=None → 8 sn dikişsiz döngü."""
    if name not in REGISTRY:
        raise KeyError(f"bilinmeyen SFX: {name}  (mevcut: {', '.join(SFX_NAMES)})")
    rng = rng_for("sfx", name, int(seed))
    if name in LOOPABLE:
        x = REGISTRY[name](rng, LOOP_SEC)
        x = _finish(x, loop=True, name=name)
        if dur is not None and abs(dur - LOOP_SEC) > 1e-6:
            x = _fit(x.astype(np.float64), dur, loop=True)
            x = D.peak_norm(D.fade_edges(x, 0.0, 0.0), PEAK_DB)
        return x.astype(np.float32)
    x = REGISTRY[name](rng, dur, **kw)
    if dur is not None:
        x = _fit(np.asarray(x, dtype=np.float64), dur, loop=False)
    return _finish(x, name=name)


# ═══════════════════════════ CLI ═══════════════════════════
def main():
    ap = argparse.ArgumentParser(description="SFX kütüphanesi")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--render")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--dur", type=float, default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.list:
        for k in SFX_NAMES:
            print(k + ("  [döngü]" if k in LOOPABLE else ""))
        return
    if a.all:
        out = a.out or "sfx_out"
        os.makedirs(out, exist_ok=True)
        for k in SFX_NAMES:
            x = sfx(k, a.seed)
            D.write_wav(os.path.join(out, k + ".wav"), x, SR)
            print(f"{k:16s} {len(x) / SR:5.2f} sn  tepe {20 * np.log10(np.abs(x).max()):.1f} dBFS")
        return
    if a.render:
        x = sfx(a.render, a.seed, a.dur)
        D.write_wav(a.out or f"{a.render}.wav", x, SR)
        print(len(x) / SR, "sn")


if __name__ == "__main__":
    main()
