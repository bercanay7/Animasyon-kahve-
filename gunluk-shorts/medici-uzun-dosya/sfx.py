"""
sfx.py — "MEDICI" için tamamen sentezlenmiş SFX kütüphanesi + geçiş→ses eşlemesi + JSON sözleşmesi (numpy/scipy; harici ses dosyası YOK).

    sfx(name, seed=0, dur=None, loop=False, **kw) -> np.ndarray float32 (n, 2), 48 kHz, tepe = −3 dBFS

* Hepsi deterministik (aynı ad+seed → aynı örnekler). dur: istenen uzunluk (sn); verilmezse doğal uzunluk.
* Döngü sesleri (crowd_murmur, sea_waves, wind, rain, fire_crackle, church_ambience, water_lap, candle_flame): varsayılan 8 sn ve DİKİŞSİZ.
* Fiziksel modelleme: filtrelenmiş gürültü + gövde sinüsleri/modlar + zarflar (düz 'bip' yok).
* KATALOG (python3 sfx.py --list): kâğıt/yazı (sayfa, kâğıt, kalem, mühür, damga, mektup, defter kapanışı, harf dizimi, baskı, harita iğnesi, fırça),
  para (sikke, yığın, yuvarlanma), kapı/metal (sürgü, TUNÇ KAPI, kilit, tahta/metal vuruş, klavye mekanizması, lens/cam tınısı, taş oyma),
  kalabalık/mekân (SÖZSÜZ uğultu, ritmik haykırış, uzak alkış, kilise oda tonu, adımlar, nal, uzaklaşan at, uzak trompet),
  doğa (ateş, mum alevi/sönmesi, deniz, liman suyu, halat, gemi, rüzgâr), çan/gong/vuruş (YALNIZ kaynaklı olay), geçişler (yıkama, sıva, dip, ışık, zum, şerit, kayma, iris, mum).
* ÇAN KURALI: church_bell / bell_toll_low / gong_hit c7, c10, c13'te OLAY sesi olarak kullanılamaz (resolve_cues atlar ve uyarır).
* Geçiş türü → ses eşlemesi: TRANSITION_MAP + transition_cues(); ses köprüsü / J-kesme kancaları: j_cut, l_cut, ses_koprusu.
* JSON sözleşmesi (sfx_cues_pN.json): bkz. normalize_cue / resolve_cues ve notlar_ses.md.

CLI: python3 sfx.py --list | --render ad [--out dosya.wav] | --all --out klasör | --katalog
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


# ═══════════════════════════ MEDICI: kapı / kilit / metal ═══════════════════════════
def _door_bolt(rng, dur, **kw):
    """Sürgü: demir sürtünmesi (pürüzlü kayma) + demir-ahşap çarpma + küçük sıçrama."""
    dur = dur or 1.3
    n = _n(dur)
    x = np.zeros((n, 2))
    L = _n(0.28)
    ts = np.arange(L) / SR
    env = np.minimum(1.0, ts / 0.03) * np.minimum(1.0, (0.28 - ts) / 0.05)
    w = rng.standard_normal(L)
    scr = D.bp(w, 700, 3600, 2) * env * (0.6 + 0.4 * np.sin(D.PI2 * 38 * ts + rng.uniform(0, 6)))
    scr += 0.5 * D.resonator(w, 1300, 500) * env
    _place(x, scr, 0.02, 0.9, -0.1)
    t0 = 0.31
    m = _n(0.5)
    tm = np.arange(m) / SR
    hit = np.zeros(m)
    for fr, a, tau in [(820, 1.0, 0.045), (1630, 0.6, 0.03), (2450, 0.4, 0.02), (310, 0.9, 0.06)]:
        hit += a * np.sin(D.PI2 * fr * tm * (1 + rng.uniform(-0.01, 0.01))) * np.exp(-tm / tau)
    hit += 1.1 * D.bp(rng.standard_normal(m), 400, 3000, 2) * np.exp(-tm / 0.012)
    hit += 0.8 * np.sin(D.PI2 * 95 * tm) * np.exp(-tm / 0.05)
    _place(x, hit, t0, 1.0, 0.05)
    _place(x, hit[:_n(0.15)] * 0.25, t0 + 0.07, 1.0, 0.1)
    return _room(x, 0.18, 0.8)[:n]


def _door_bronze(rng, dur, **kw):
    """Tunç kapı çarpması: alçak gövde darbesi + büyük metal levhanın uzun, hafif uyumsuz kipleri (sessizliğe uzanan kuyruk) + zincir/halka şıngırtısı."""
    dur = dur or 6.5
    n = _n(dur)
    t = np.arange(n) / SR
    x = np.zeros((n, 2))
    body = np.sin(D.PI2 * np.cumsum(55 + 75 * np.exp(-t / 0.06)) / SR) * np.exp(-t / 0.35)
    imp = D.bp(rng.standard_normal(n), 200, 5000, 2) * np.exp(-t / 0.018) * 1.8
    ring = np.zeros(n)
    for fr, a, tau in [(96, 1.0, 2.6), (143, 0.8, 2.2), (231, 0.7, 1.8), (318, 0.55, 1.5), (472, 0.5, 1.2), (655, 0.4, 0.9), (930, 0.3, 0.6), (1380, 0.2, 0.4)]:
        fr = fr * (1 + rng.uniform(-0.012, 0.012))
        for sgn in (-1, 1):
            ring += 0.5 * a * np.sin(D.PI2 * (fr + sgn * rng.uniform(0.2, 1.1)) * t + rng.uniform(0, 6.28)) * np.exp(-t / tau)
    y = np.tanh(1.1 * (body * 0.9 + imp + ring))
    _place(x, y, 0.0, 1.0, 0.0)
    for _ in range(int(rng.integers(3, 6))):
        c = float(rng.uniform(1800, 4800))
        m = _n(0.3)
        ts = np.arange(m) / SR
        _place(x, np.sin(D.PI2 * c * ts) * np.exp(-ts / rng.uniform(0.04, 0.12)) * rng.uniform(0.05, 0.2), float(rng.uniform(0.05, 0.5)), 1.0, float(rng.uniform(-0.5, 0.5)))
    return _room(x, 0.3, 2.4)[:n]


def _lock_click(rng, dur, **kw):
    """Kilit: anahtar dönüşü (iki küçük tık) + sürgü/dil 'klak' + kısa metal tınısı."""
    dur = dur or 0.9
    n = _n(dur)
    x = np.zeros((n, 2))
    for t0, a in ((0.0, 0.6), (0.17, 0.7)):
        m = _n(0.05)
        ts = np.arange(m) / SR
        c = D.bp(rng.standard_normal(m), 1800, 6000, 2) * np.exp(-ts / 0.004) + 0.4 * np.sin(D.PI2 * 2300 * ts) * np.exp(-ts / 0.01)
        _place(x, c, t0, a, 0.05)
    m = _n(0.45)
    ts = np.arange(m) / SR
    k = np.zeros(m)
    for fr, a, tau in [(640, 1.0, 0.05), (1280, 0.6, 0.04), (2100, 0.4, 0.03)]:
        k += a * np.sin(D.PI2 * fr * ts) * np.exp(-ts / tau)
    k += D.bp(rng.standard_normal(m), 500, 3500, 2) * np.exp(-ts / 0.01) * 1.2
    _place(x, k, 0.40, 1.0, 0.0)
    return _room(D.lp(x, 9000), 0.15, 0.6)[:n]


def _knock(rng, dur, kind="wood", n_hits=1, **kw):
    """Tahta/metal vuruş: kind='wood' (tok) | 'metal' (parlak tık)."""
    dur = dur or 0.5
    n = _n(dur)
    x = np.zeros((n, 2))
    t = 0.02
    for _ in range(int(n_hits)):
        m = _n(0.25)
        ts = np.arange(m) / SR
        if kind == "metal":
            y = sum(a * np.sin(D.PI2 * f * ts) * np.exp(-ts / tau) for f, a, tau in [(2400, 1.0, 0.03), (3900, 0.6, 0.02), (5300, 0.3, 0.012)]) + D.hp(rng.standard_normal(m), 3000, 2) * np.exp(-ts / 0.002)
        else:
            y = D.bp(rng.standard_normal(m), 180, 1100, 2) * np.exp(-ts / 0.012) * 1.6 + np.sin(D.PI2 * 240 * ts) * np.exp(-ts / 0.03) * 0.8
        _place(x, y, t, rng.uniform(0.8, 1.0), float(rng.uniform(-0.2, 0.2)))
        t += float(rng.uniform(0.16, 0.30))
    return _room(x, 0.12, 0.5)[:n]


# ═══════════════════════════ kalabalık / mekân (SÖZSÜZ) ═══════════════════════════
def _crowd_chant(rng, dur, **kw):
    """Ritmik kalabalık haykırışı (SÖZSÜZ): iki heceli ('pal-le') ünlü patlamaları a–e; 24 ses, hafif eşgüdümsüz. Medici: 'palle, palle' alayı (c7)."""
    dur = dur or 5.0
    n = _n(dur)
    x = np.zeros((n, 2))
    period = float(kw.get("period", 0.66))
    forms = {"a": (700, 1100, 2600), "e": (430, 1750, 2600)}
    for v in range(24):
        f0 = float(rng.uniform(105, 230))
        pan = float(rng.uniform(-0.9, 0.9))
        amp = float(rng.uniform(0.5, 1.0))
        t = float(rng.uniform(0.0, 0.08))
        while t < dur - 0.1:
            for off, vow, L in ((0.0, "a", 0.22), (0.30, "e", 0.20)):
                jit = float(rng.normal(0, 0.035))
                m = _n(L) + 600
                ts = np.arange(m) / SR
                fr = f0 * (1 + 0.05 * np.sin(D.PI2 * 4.0 * ts + rng.uniform(0, 6)) + (0.08 if vow == "e" else 0.0) * (ts / L))
                src = (2 * ((np.cumsum(fr) / SR) % 1) - 1) * 0.7 + 0.25 * rng.standard_normal(m)
                f1, f2, f3 = forms[vow]
                y = D.resonator(src, f1, 120) + 0.7 * D.resonator(src, f2, 150) + 0.3 * D.resonator(src, f3, 230)
                env = np.sin(np.pi * np.clip(np.arange(m) / (m - 600), 0, 1)) ** 1.3
                _place(x, y[:m] * env, t + off + jit, amp * float(rng.uniform(0.6, 1.0)), pan)
            t += period * float(rng.uniform(0.97, 1.03))
    x = x / (np.std(x) + 1e-9)
    x = D.lp(x, 4200, 2)
    x = D.fade_edges(x, 0.5, 0.9)
    return _room(x, 0.25, 1.4)[:n]


def _applause_far(rng, dur, **kw):
    """Uzak alkış: yoğunluğu yükselip sönen küçük el çırpma patlamaları + mesafe süzgeci ve reverb."""
    dur = dur or 6.0
    n = _n(dur)
    x = np.zeros((n, 2))
    t = 0.0
    while t < dur:
        u = t / dur
        rate = 90 * (np.clip(u / 0.2, 0, 1) ** 1.2) * (1 - np.clip((u - 0.55) / 0.45, 0, 1) ** 1.5) + 4
        t += float(rng.exponential(1.0 / rate))
        m = _n(float(rng.uniform(0.007, 0.016)))
        ts = np.arange(m) / SR
        c = D.bp(rng.standard_normal(m + 64), 1200, 4800, 2)[:m] * np.exp(-ts / (m / SR * 0.3))
        _place(x, c, t, float(rng.lognormal(-0.8, 0.5)), float(rng.uniform(-0.9, 0.9)))
    x = D.lp(x, 3800, 2)
    x = D.fade_edges(x, 0.35, 1.2)
    return _room(x, 0.5, 1.8)[:n]


def _circ_reverb(x, rt60, wet=0.9, dry=0.35, seed=31):
    """Döngüsel (dikişsiz) reverb: periyodik x (n,2) ile IR'nin dairesel evrişimi (FFT). IR < n olmalı."""
    n = len(x)
    ir = D.hall_ir(rt60, seed=seed)
    ir = ir[:min(len(ir), n - 1)]
    out = np.zeros_like(x)
    for ch in range(2):
        h = np.zeros(n)
        h[:len(ir)] = ir[:, ch]
        out[:, ch] = np.fft.irfft(np.fft.rfft(x[:, ch]) * np.fft.rfft(h), n)
    return dry * x + wet * out * (np.std(x) / (np.std(out) + 1e-12))


def _church_ambience(rng, dur, **kw):
    """Kilise içi oda tonu (DÖNGÜ): uzak, sözsüz kalabalık uğultusu + uzun reverb + çok alçak oda uğultusu. 'Ayin yankısı' olarak: müzik değil, doku."""
    n = _n(dur)
    base = _crowd_murmur(rng, dur)
    base = base / (np.std(base) + 1e-9)
    x = _circ_reverb(base, 3.4, wet=1.0, dry=0.28)
    hum = np.stack([_periodic_noise(rng, n, _bandshape(55, 190, 3)), _periodic_noise(rng, n, _bandshape(55, 190, 3))], axis=1)
    x = x + 0.28 * hum
    sos = np.concatenate([D.biquad("lp", 2300, 0, 0.7), D.biquad("lp", 2300, 0, 0.7)])
    return D.periodic_filter(sos, x)


def _hoof_far(rng, dur, **kw):
    """Tek atın uzaklaşan nal sesi (yürüyüş): adım adım sönen, giderek donuklaşan, sağa/sola kayan."""
    dur = dur or 3.8
    n = _n(dur)
    x = np.zeros((n, 2))
    pan0 = float(kw.get("pan0", -0.2))
    for k in range(7):
        t = 0.15 + k * 0.52 * float(rng.uniform(0.97, 1.03))
        for o, a in ((0.0, 1.0), (0.26, 0.8)):
            dist = 0.85 ** (k + o)
            m = _n(0.25)
            ts = np.arange(m) / SR
            thud = np.sin(D.PI2 * 135 * ts * (1 + 0.3 * np.exp(-ts / 0.02))) * np.exp(-ts / 0.03)
            thud += D.bp(rng.standard_normal(m), 180, 1000, 2) * np.exp(-ts / 0.022) * 1.2
            clack = D.bp(rng.standard_normal(m), 1500, 4500, 2) * np.exp(-ts / 0.004) * 0.9
            y = D.lp(thud + clack * (0.3 + 0.7 * dist), 5500 * dist + 900)
            _place(x, y, t + o, a * dist, np.clip(pan0 + 0.12 * k, -1, 1))
    return _room(x, 0.35, 1.4)[:n]


def _footsteps(rng, dur, kind="stone", n_steps=6, pace=0.62, **kw):
    """Adımlar (taş/ahşap zemin, yankılı mekân): ağır topuk darbesi + tık; hafif sağ-sol."""
    dur = dur or (0.3 + n_steps * pace + 1.2)
    n = _n(dur)
    x = np.zeros((n, 2))
    t = 0.12
    for k in range(int(n_steps)):
        m = _n(0.3)
        ts = np.arange(m) / SR
        if kind == "wood":
            y = D.bp(rng.standard_normal(m), 150, 900, 2) * np.exp(-ts / 0.03) * 1.4 + np.sin(D.PI2 * 120 * ts) * np.exp(-ts / 0.04)
        else:
            y = D.lp(rng.standard_normal(m), 600, 2) * np.exp(-ts / 0.025) * 1.2 + np.sin(D.PI2 * 90 * ts) * np.exp(-ts / 0.035)
            y += D.bp(rng.standard_normal(m), 1500, 3800, 2) * np.exp(-ts / 0.004) * 0.45
        _place(x, y, t, float(rng.uniform(0.75, 1.0)), (-0.15 if k % 2 else 0.15))
        t += pace * float(rng.uniform(0.94, 1.07))
    return _room(x, 0.55 if kind == "stone" else 0.3, 2.2 if kind == "stone" else 0.9)[:n]


def _distant_trumpet(rng, dur, **kw):
    """Uzaktan trompet: iki nota (boş beşli), nefesli ataklı pirinç tınısı, güçlü mesafe süzgeci + uzun reverb. (c10: 9 Kasım → Capponi köprüsü)"""
    dur = dur or 4.4
    n = _n(dur)
    x = np.zeros((n, 2))
    for f, t0, L in ((392.0, 0.0, 1.15), (587.33, 1.35, 1.9)):
        m = _n(L)
        tm = np.arange(m) / SR
        tab = D.additive_table(f, lambda ff: (f / ff) ** 0.9 * (1 + 2.2 * np.exp(-((ff - 1500.0) / 800.0) ** 2)) / (1 + (ff / 3500.0) ** 4), rng, phase="random", max_hz=8000)
        y = D.wt_osc(tab, f * (1 + 0.004 * np.sin(D.PI2 * 5.2 * tm)), m, phase0=rng.random())
        y *= np.minimum(1.0, tm / 0.07) * np.minimum(1.0, (L - tm) / 0.25) * (0.85 + 0.15 * np.sin(D.PI2 * 4.0 * tm))
        y += 0.05 * D.bp(rng.standard_normal(m), 3000, 6500, 2) * np.minimum(1.0, tm / 0.05) * np.exp(-tm / 0.3)
        _place(x, y, t0, 1.0, 0.1)
    x = D.lp(x, 2600, 2)
    return _room(x, 0.9, 2.2)[:n]


# ═══════════════════════════ deniz / halat / su / ateş / mum ═══════════════════════════
def _rope_creak(rng, dur, **kw):
    """Halat gerilimi: ince, yüksek perdeli sürtünme gıcırtısı (stick-slip) + alçak gerilme homurtusu."""
    dur = dur or 2.6
    n = _n(dur)
    x = np.zeros((n, 2))
    for k in range(int(rng.integers(2, 4))):
        t0 = float(rng.uniform(0.0, max(dur - 1.3, 0.1)))
        L = float(rng.uniform(0.6, 1.2))
        m = _n(L)
        ts = np.arange(m) / SR
        u = ts / L
        f0 = float(rng.uniform(420, 760))
        fr = f0 * (1 + 0.25 * np.sin(np.pi * u) + 0.05 * D.lp(rng.standard_normal(m), 10, 1) / 0.03)
        rate = 52 + 18 * np.sin(np.pi * u)
        gate = np.clip(1.0 - ((np.cumsum(rate) / SR) % 1.0) * 1.7, 0, 1) ** 0.8
        saw = 2 * ((np.cumsum(fr) / SR) % 1.0) - 1
        y = D.resonator_tv(saw * gate, 1100 + 700 * u, 260) * 2.4 + 0.3 * D.lp(saw * gate, 500, 2)
        env = np.sin(np.pi * np.clip(u, 0, 1)) ** 0.9
        _place(x, y * env * 0.35, t0, float(rng.uniform(0.7, 1.0)), float(rng.uniform(-0.4, 0.4)))
    return _room(D.lp(x, 6500), 0.2, 0.9)[:n]


def _water_lap(rng, dur, **kw):
    """Liman suyu (DÖNGÜ): yumuşak yalama, küçük baloncuk 'plip'leri, düşük hışırtı."""
    n = _n(dur)
    out = np.zeros((n, 2))
    t = np.arange(n) / SR
    for ch in range(2):
        low = _periodic_noise(rng, n, _bandshape(60, 520, 2))
        swell = 0.55 + 0.45 * np.sin(D.PI2 * 2 * t / dur + rng.uniform(0, 6)) * np.sin(D.PI2 * 3 * t / dur + rng.uniform(0, 6))
        hi = _periodic_noise(rng, n, _bandshape(1800, 6500, 2))
        out[:, ch] = low * swell * 0.9 + hi * (swell ** 2) * 0.12
    for _ in range(int(dur * 6)):
        m = _n(0.025)
        ts = np.arange(m) / SR
        f = float(rng.uniform(300, 800))
        y = np.sin(D.PI2 * np.cumsum(f * (1 + 2.0 * ts / 0.025)) / SR) * np.exp(-ts / 0.007)
        _place_wrap(out, y, float(rng.uniform(0, dur)), float(rng.uniform(0.05, 0.2)), float(rng.uniform(-0.8, 0.8)))
    return out


def _candle_flame(rng, dur, **kw):
    """Mum alevi (DÖNGÜ): çok yumuşak titreşim (alçak gürültü + 6–12 Hz kıpırtı), seyrek minik çıtırtı, ara sıra hafif 'fış'."""
    n = _n(dur)
    out = np.zeros((n, 2))
    t = np.arange(n) / SR
    for ch in range(2):
        bed = _periodic_noise(rng, n, _bandshape(90, 800, 2))
        flick = 0.65 + 0.2 * np.sin(D.PI2 * 3 * t / dur + rng.uniform(0, 6)) + 0.15 * np.sin(D.PI2 * 8 * t / dur + rng.uniform(0, 6))
        flut = _periodic_noise(rng, n, _bandshape(3, 14, 2))
        flut = 1 + 0.35 * np.clip(flut / (np.std(flut) + 1e-9), -2, 2) / 2
        mid = _periodic_noise(rng, n, _bandshape(400, 1800, 2)) * 0.22
        out[:, ch] = bed * flick * 0.6 + mid * flick * np.clip(flut, 0.3, 1.7)
    for _ in range(int(dur * 1.1)):
        c = float(np.exp(rng.uniform(np.log(1500), np.log(6500))))
        L = int(rng.uniform(0.001, 0.003) * SR) + 40
        b = D.bp(rng.standard_normal(L + 32), c / 1.5, min(c * 1.5, 14000), 2)[:L] * np.exp(-np.arange(L) / (L * 0.3))
        _place_wrap(out, b / (np.max(np.abs(b)) + 1e-9), float(rng.uniform(0, dur)), float(rng.lognormal(-2.3, 0.6)), float(rng.uniform(-0.6, 0.6)))
    for _ in range(max(1, int(dur / 3.0))):
        L = int(0.4 * SR)
        ts = np.arange(L) / SR
        b = D.lp(rng.standard_normal(L), 700, 2) * np.sin(np.pi * ts / 0.4) ** 2 * 0.5
        _place_wrap(out, b, float(rng.uniform(0, dur)), 0.4, float(rng.uniform(-0.5, 0.5)))
    return out


def _candle_snuff(rng, dur, **kw):
    """Mum sönmesi: nefes/üfleme + fitil çızırtısı ve kısa duman fışırtısı."""
    dur = dur or 1.8
    n = _n(dur)
    t = np.arange(n) / SR
    puff = D.bp(rng.standard_normal(n), 500, 3500, 2) * np.exp(-t / 0.05) * (1 - np.exp(-t / 0.012)) * 1.0
    hiss = D.hp(rng.standard_normal(n), 2200, 2) * np.exp(-t / 0.35) * (1 - np.exp(-t / 0.05)) * 0.22
    poof = np.sin(D.PI2 * 70 * t) * np.exp(-t / 0.06) * 0.3
    x = np.stack([puff + hiss + poof, (puff + hiss + poof) * 0.95], axis=1)
    for _ in range(int(rng.integers(3, 7))):
        c = float(rng.uniform(2500, 6000))
        L = _n(0.004)
        ts = np.arange(L) / SR
        _place(x, np.sin(D.PI2 * c * ts) * np.exp(-ts / 0.0012), float(rng.uniform(0.1, 0.9)), float(rng.uniform(0.05, 0.15)), float(rng.uniform(-0.4, 0.4)))
    x = np.stack([D.lp(x[:, 0], 7000, 2), D.lp(x[:, 1], 7000, 2)], axis=1)      # yumuşatma: tiz çıtırtı/tıslama 7 kHz üstünde kesik
    return _room(x, 0.1, 0.5)[:n]


def _candle_out_in(rng, dur, **kw):
    """Mum sönmesi + karanlık + yeni mum yanışı (geçiş 'candle'): snuff, ~1 sn sessizlik, hafif 'fış' + alev titremesi yükselir."""
    dur = dur or 3.0
    n = _n(dur)
    x = np.zeros((n, 2))
    sn = _candle_snuff(rng, 1.4)
    _place(x, sn[:, 0], 0.0, 1.0, -0.1)
    t0 = 1.15
    m = _n(0.35)
    ts = np.arange(m) / SR
    ig = D.lp(rng.standard_normal(m), 900, 2) * np.sin(np.pi * ts / 0.35) ** 1.5
    _place(x, ig, t0, 0.5, 0.1)
    fl = _candle_flame(rng_for("cof", int(rng.integers(1 << 30))), 4.0)
    L = min(len(fl), n - _n(t0 + 0.2))
    env = np.minimum(1.0, np.arange(L) / (0.8 * SR))[:, None]
    x[_n(t0 + 0.2):_n(t0 + 0.2) + L] += fl[:L] * env * 0.7
    return x


# ═══════════════════════════ mekanizma / yazı / kâğıt / taş ═══════════════════════════
def _keyboard_action(rng, dur, kind="harpsichord", n_keys=6, **kw):
    """Klavye mekanizması: tuş 'tok'u + (klavsen) çubuk-pena çıtlaması / (piyano) çekiç darbesi + sönümleyici. Telsiz: yalnız mekanizma sesi (nota yok)."""
    dur = dur or (0.4 + 0.4 * n_keys + 0.8)
    n = _n(dur)
    x = np.zeros((n, 2))
    t = 0.1
    for k in range(int(n_keys)):
        m = _n(0.22)
        ts = np.arange(m) / SR
        key = D.lp(rng.standard_normal(m), 900, 2) * np.exp(-ts / 0.012) + np.sin(D.PI2 * 180 * ts) * np.exp(-ts / 0.02) * 0.8
        if kind == "piano":
            ham = D.lp(rng.standard_normal(m), 1800, 2) * np.exp(-ts / 0.02) * 0.9 + np.sin(D.PI2 * 120 * ts) * np.exp(-ts / 0.03) * 0.7
            y = key * 0.8 + ham
        else:
            jack = D.hp(rng.standard_normal(m), 3500, 2) * np.exp(-ts / 0.004) * 0.9 + D.resonator(rng.standard_normal(m), 2300, 800) * np.exp(-ts / 0.008) * 0.6
            y = key + jack
        _place(x, y, t, float(rng.uniform(0.6, 1.0)), float(rng.uniform(-0.25, 0.25)))
        if rng.random() < 0.6:        # tuş bırakma
            _place(x, D.bp(rng.standard_normal(m), 400, 2500, 2) * np.exp(-ts / 0.01) * 0.3, t + float(rng.uniform(0.12, 0.3)), 0.5, 0.0)
        t += float(rng.uniform(0.22, 0.52))
    return _room(x, 0.15, 0.7)[:n]


def _glass_chime(rng, dur, root=None, **kw):
    """Lens/cam tınısı: cam kadeh benzeri uyumsuz kısmiler (hafif vurma çiftleri), uzun parlak sönüm. root: Hz."""
    dur = dur or 3.6
    n = _n(dur)
    t = np.arange(n) / SR
    f = float(root or 1568.0)
    y = np.zeros(n)
    for r, a, tau in [(1.0, 1.0, 2.6), (2.32, 0.5, 1.9), (4.25, 0.32, 1.3), (6.63, 0.18, 0.9), (9.38, 0.1, 0.55)]:
        fr = f * r
        if fr > 17000:
            continue
        for sgn in (-1, 1):
            y += 0.5 * a * np.sin(D.PI2 * (fr + sgn * rng.uniform(1.0, 3.2)) * t + rng.uniform(0, 6.28)) * np.exp(-t / tau)
    y += 0.4 * D.hp(rng.standard_normal(n), 4000, 2) * np.exp(-t / 0.003)
    y *= np.minimum(1.0, t / 0.0012)
    x = np.stack([y, y * 0.92], axis=1)
    return _room(x, 0.3, 1.5)[:n]


def _stamp_thud(rng, dur, **kw):
    """Damga çarpması (mürekkepli ahşap damga): tok darbe + kâğıt tokadı + kısa mürekkep 'cık'."""
    dur = dur or 0.9
    n = _n(dur)
    t = np.arange(n) / SR
    thump = D.lp(rng.standard_normal(n), 600, 2) * np.exp(-t / 0.03) * 1.3 + np.sin(D.PI2 * 105 * t * (1 + 0.25 * np.exp(-t / 0.02))) * np.exp(-t / 0.055) * 1.0
    slap = D.hp(rng.standard_normal(n), 1500, 2) * np.exp(-t / 0.008) * 0.45
    ink = D.bp(rng.standard_normal(n), 250, 1300, 2) * (1 - np.exp(-t / 0.02)) * np.exp(-t / 0.15) * 0.25
    y = thump + slap + ink
    x = np.stack([y, y], axis=1)
    return _room(x, 0.1, 0.5)[:n]


def _coin_roll(rng, dur, **kw):
    """Sikke yuvarlanıp yerleşir: hızlanan sallantı (wobble) + sönen halka tınısı, sonda 3 hızlı tık."""
    dur = dur or 2.5
    n = _n(dur)
    t = np.arange(n) / SR
    f = float(rng.uniform(3000, 3600))
    rate = 5.0 + 26.0 * (t / 1.9) ** 2.2
    wob = 0.5 + 0.5 * np.cos(D.PI2 * np.cumsum(rate) / SR)
    env = np.exp(-t / 1.4) * np.clip((1.95 - t) / 0.2, 0, 1) * np.minimum(1.0, t / 0.01)
    y = (np.sin(D.PI2 * f * t) + 0.5 * np.sin(D.PI2 * f * 2.39 * t)) * wob * env * 0.5
    y += D.bp(rng.standard_normal(n), 250, 900, 2) * wob * env * 0.12
    x = np.stack([y, y], axis=1)
    for dt, a in ((1.93, 1.0), (2.01, 0.7), (2.07, 0.5)):
        _place(x, _coin_ring(rng, f0=f, tau=0.05) * 0.5, dt, a, 0.05)
    return D.lp(x, 14000)[:n]


def _type_set(rng, dur, **kw):
    """Matbaa harf dizimi: harf kalıplarının dizgi çubuğuna tek tek yerleşen metal tıkları; sonda büyük 'klak'."""
    dur = dur or 2.6
    n = _n(dur)
    x = np.zeros((n, 2))
    t = 0.1
    while t < dur - 0.5:
        m = _n(0.06)
        ts = np.arange(m) / SR
        y = sum(a * np.sin(D.PI2 * f * ts * (1 + rng.uniform(-0.02, 0.02))) * np.exp(-ts / tau)
                for f, a, tau in [(rng.uniform(3200, 4200), 1.0, 0.012), (rng.uniform(5200, 7000), 0.5, 0.008)])
        y += D.hp(rng.standard_normal(m), 3500, 2) * np.exp(-ts / 0.0025) * 0.8
        _place(x, y, t, float(rng.uniform(0.35, 0.9)), float(rng.uniform(-0.4, 0.4)))
        t += float(rng.uniform(0.11, 0.26))
    m = _n(0.2)
    ts = np.arange(m) / SR
    big = D.bp(rng.standard_normal(m), 600, 3500, 2) * np.exp(-ts / 0.015) * 1.2 + np.sin(D.PI2 * 420 * ts) * np.exp(-ts / 0.04) * 0.8
    _place(x, big, t + 0.05, 0.9, 0.0)
    return _room(D.lp(x, 11000), 0.12, 0.6)[:n]


def _press_thud(rng, dur, **kw):
    """Vidalı baskı: yükselen ahşap gıcırtısı + ağır tok baskı darbesi + kâğıt soyulma hışırtısı."""
    dur = dur or 2.6
    n = _n(dur)
    x = np.zeros((n, 2))
    L = _n(0.95)
    ts = np.arange(L) / SR
    u = ts / 0.95
    saw = 2 * ((np.cumsum(150 + 90 * u) / SR) % 1.0) - 1
    gate = np.clip(1.0 - ((np.cumsum(30 + 20 * u) / SR) % 1.0) * 1.6, 0, 1) ** 0.8
    cr = D.resonator_tv(saw * gate, 420 + 300 * u, 200) * 1.4 * np.sin(np.pi * np.clip(u, 0, 1)) ** 0.7
    _place(x, cr * 0.5, 0.0, 0.8, -0.1)
    t0 = 1.0
    m = _n(0.6)
    tm = np.arange(m) / SR
    th = D.lp(rng.standard_normal(m), 400, 2) * np.exp(-tm / 0.05) * 1.4 + np.sin(D.PI2 * 70 * tm) * np.exp(-tm / 0.12) * 1.1
    _place(x, th, t0, 1.0, 0.0)
    m = _n(0.35)
    tm = np.arange(m) / SR
    pe = D.hp(rng.standard_normal(m), 2000, 2) * np.sin(np.pi * tm / 0.35) ** 1.5 * 0.35
    _place(x, pe, t0 + 0.4, 0.6, 0.2)
    return _room(D.lp(x, 9000), 0.2, 0.9)[:n]


def _book_close(rng, dur, **kw):
    """Defter kapanışı: ağır cilt darbesi + hava üflemesi + kâğıt kıpırtısı (c9: şubeler tek tek kapanır). pitch: 1.0 = varsayılan (alçalan seri için <1)."""
    dur = dur or 1.5
    n = _n(dur)
    t = np.arange(n) / SR
    p = float(kw.get("pitch", 1.0))
    thump = np.sin(D.PI2 * np.cumsum((100 * p) * (0.6 + 0.4 * np.exp(-t / 0.05))) / SR) * np.exp(-t / 0.09) * 1.3
    thump += D.lp(rng.standard_normal(n), 500, 2) * np.exp(-t / 0.03) * 1.1
    puff = D.bp(rng.standard_normal(n), 300, 2500, 2) * np.exp(-t / 0.12) * (1 - np.exp(-t / 0.01)) * 0.5
    x = np.stack([thump + puff, (thump + puff) * 0.97], axis=1)
    cr = _crinkles(rng, dur, 140, lambda tt: float(0.5 * np.exp(-tt / 0.3) + 0.03), lo=1500, hi=6000, amp=0.4)
    x[:len(cr)] += cr[:n]
    return _room(x, 0.15, 0.7)[:n]


def _letter_open(rng, dur, **kw):
    """Mektup açılışı: mühür mumunun çatlaması + kâğıdın açılıp düzleşmesi."""
    dur = dur or 1.8
    n = _n(dur)
    x = np.zeros((n, 2))
    m = _n(0.05)
    ts = np.arange(m) / SR
    cr = D.hp(rng.standard_normal(m), 2000, 2) * np.exp(-ts / 0.006) * 1.2 + np.sin(D.PI2 * 2800 * ts) * np.exp(-ts / 0.004) * 0.5
    _place(x, cr, 0.05, 0.9, 0.0)
    pa = _crinkles(rng, 1.3, 190, lambda tt: float(0.9 * np.exp(-0.5 * ((tt - 0.45) / 0.22) ** 2) + 0.04), amp=0.8)
    _place(x, pa[:, 0], 0.18, 0.7, -0.15)
    _place(x, pa[:, 1], 0.18, 0.7, 0.15)
    return D.lp(x, 11000)[:n]


def _pin_stick(rng, dur, **kw):
    """Harita iğnesi dikme: küçük ahşap 'tak' + ince metal tınısı."""
    dur = dur or 0.4
    n = _n(dur)
    t = np.arange(n) / SR
    y = D.bp(rng.standard_normal(n), 800, 2600, 2) * np.exp(-t / 0.008) * 1.2 + np.sin(D.PI2 * 4300 * t) * np.exp(-t / 0.06) * 0.25 + np.sin(D.PI2 * 260 * t) * np.exp(-t / 0.02) * 0.5
    x = np.stack([y, y], axis=1)
    return _room(x, 0.1, 0.4)[:n]


def _chisel_tap(rng, dur, **kw):
    """Sert taş atölyesi: kalemle taş oyma vuruşları (parlak tık + kısa alçak gövde), düzensiz aralık."""
    dur = dur or 2.2
    n = _n(dur)
    x = np.zeros((n, 2))
    t = 0.1
    while t < dur - 0.4:
        m = _n(0.12)
        ts = np.arange(m) / SR
        y = np.sin(D.PI2 * float(rng.uniform(1500, 2200)) * ts) * np.exp(-ts / 0.012) + D.bp(rng.standard_normal(m), 1000, 5000, 2) * np.exp(-ts / 0.004) * 0.9 + np.sin(D.PI2 * 300 * ts) * np.exp(-ts / 0.015) * 0.4
        _place(x, y, t, float(rng.uniform(0.6, 1.0)), float(rng.uniform(-0.3, 0.3)))
        t += float(rng.uniform(0.17, 0.42))
    return _room(x, 0.2, 0.9)[:n]


def _brush_stroke(rng, dur, **kw):
    """Fırça darbesi (duvara yazı): yumuşak ataklı sürtünme hışırtısı."""
    dur = dur or 0.7
    n = _n(dur)
    t = np.arange(n) / SR
    y = D.bp(rng.standard_normal(n), 800, 6000, 2) * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.6 * (0.7 + 0.3 * np.sin(D.PI2 * 30 * t))
    return np.stack([y, y * 0.95], axis=1)


# ═══════════════════════════ MEDICI geçiş sesleri ═══════════════════════════
def _wash_swell(rng, dur, **kw):
    """Pigment yıkama ('yikama'): ıslak boyanın yayılması — yumuşak, bantlı gürültü kabarması + hafif damlama dokusu."""
    dur = dur or 1.1
    n = _n(dur)
    t = np.arange(n) / SR
    u = t / dur
    env = np.sin(np.pi * np.clip(u, 0, 1)) ** 1.6
    nz = _stereo_noise(rng, n)
    y = D.bp(nz, 250, 2600, 2) * (env * (0.75 + 0.25 * np.sin(D.PI2 * 3.1 * t + 0.5)))[:, None]
    y += D.bp(nz, 80, 300, 2) * (env ** 1.5)[:, None] * 0.5
    for _ in range(int(dur * 9)):
        m = _n(0.02)
        ts = np.arange(m) / SR
        f = float(rng.uniform(500, 1400))
        _place(y, np.sin(D.PI2 * np.cumsum(f * (1 + 1.5 * ts / 0.02)) / SR) * np.exp(-ts / 0.006), float(rng.uniform(0.1, dur - 0.1)), float(rng.uniform(0.03, 0.1)) * float(env[min(int(rng.uniform(0.1, dur - 0.1) * SR), n - 1)]), float(rng.uniform(-0.7, 0.7)))
    return D.lp(y, 9000)


def _plaster_scrape(rng, dur, **kw):
    """Fresko günlüğü ('giornata'): sıva yamalarının mala ile sürülmesi — kısa, taneli kazıma vuruşları."""
    dur = dur or 1.0
    n = _n(dur)
    x = np.zeros((n, 2))
    k = int(rng.integers(3, 5))
    for i in range(k):
        L = float(rng.uniform(0.14, 0.26))
        m = _n(L)
        ts = np.arange(m) / SR
        env = np.sin(np.pi * ts / L) ** 1.2
        g = 0.55 + 0.45 * (D.lp(rng.standard_normal(m), 160, 2) / 0.1)
        y = D.bp(rng.standard_normal(m), 900, 5500, 2) * env * np.clip(g, 0.1, 2.0)
        _place(x, y, 0.04 + i * dur / (k + 0.5) * float(rng.uniform(0.8, 1.1)), float(rng.uniform(0.6, 1.0)), float(rng.uniform(-0.5, 0.5)))
    return D.lp(x, 8500)


def _dip_drop(rng, dur, **kw):
    """'dip' (siyaha iniş): alçalan alt-bas + havanın çekilmesi (düşen bantlı gürültü) + uzun reverb kuyruğu."""
    dur = dur or 2.6
    n = _n(dur)
    t = np.arange(n) / SR
    f = 32 + 58 * np.exp(-t / 0.55)
    sub = np.sin(D.PI2 * np.cumsum(f) / SR) * np.exp(-t / 0.9) * np.minimum(1.0, t / 0.02)
    nz = rng.standard_normal(n)
    sweep = np.zeros(n)
    for c in np.exp(np.linspace(np.log(3000), np.log(220), 12)):
        pos = np.log(3000 / c) / np.log(3000 / 220) * 0.7
        g = np.exp(-0.5 * ((t - pos) / 0.12) ** 2)
        sweep += D.bp(nz, c / 1.3, min(c * 1.3, 12000), 2) * g
    sweep *= 0.5
    th = D.lp(rng.standard_normal(n), 250, 2) * np.exp(-t / 0.06) * 0.8
    y = sub * 1.1 + sweep + th
    x = np.stack([y, y * 0.98], axis=1)
    return _room(x, 0.4, 2.2)[:n]


def _light_swell(rng, dur, root=None, **kw):
    """'light' (sıcak ışık huzmesi): yavaş kabaran uyumlu harmonik örtü (add9) + havadar parıltı. root: Hz (müziğin ana sesine akort)."""
    dur = dur or 2.6
    n = _n(dur)
    t = np.arange(n) / SR
    f = float(root or 392.0)
    y = np.zeros(n)
    for r, a in [(1.0, 1.0), (1.5, 0.7), (2.0, 0.6), (2.5, 0.35), (3.0, 0.3)]:
        for dt_ in (-0.7, 0.7):
            y += 0.5 * a * np.sin(D.PI2 * (f * r + dt_) * t + rng.uniform(0, 6.28)) * (1 - np.exp(-t / 0.7)) * np.exp(-np.maximum(t - 0.8, 0) / 1.1)
    air = D.bp(rng.standard_normal(n), 3500, 9500, 2) * (1 - np.exp(-t / 0.6)) * np.exp(-np.maximum(t - 0.8, 0) / 0.9) * 0.05
    x = np.stack([y + air, y * 0.94 - air], axis=1)
    return _room(x, 0.3, 1.8)[:n]


def _zoom_rush(rng, dur, long=False, **kw):
    """'zoom' / 'zoomthru': hızlanan hava hücumu (yükselen bantlı gürültü) + yükselen alt-bas, sonda yumuşak oturma darbesi."""
    dur = dur or (1.5 if long else 0.9)
    n = _n(dur)
    t = np.arange(n) / SR
    u = t / dur
    nz = _stereo_noise(rng, n)
    out = np.zeros((n, 2))
    nb = 14
    cs = np.exp(np.linspace(np.log(260), np.log(5200), nb))
    for i, c in enumerate(cs):
        pos = ((i + 0.5) / nb) ** 1.3 * 0.82
        g = np.exp(-0.5 * ((u - pos) / 0.14) ** 2)
        out += D.bp(nz, c / 1.3, min(c * 1.3, 14000), 2) * g[:, None]
    out *= (u ** 1.5 * np.clip((1.0 - u) / 0.12, 0, 1))[:, None]
    sub = np.sin(D.PI2 * np.cumsum(40 + 80 * u ** 2) / SR) * u ** 2 * np.clip((1 - u) / 0.1, 0, 1) * 0.35
    out += np.stack([sub, sub], axis=1)
    m = _n(0.25)
    tm = np.arange(m) / SR
    th = D.lp(rng.standard_normal(m), 260, 2) * np.exp(-tm / 0.05) * 0.5 + np.sin(D.PI2 * 70 * tm) * np.exp(-tm / 0.08) * 0.5
    _place(out, th, max(dur - 0.12, 0.1), 0.8, 0.0)
    return D.hp(out, 60, 2)


def _cloth_sweep(rng, dur, dir="r", **kw):
    """'carry' (öne gelen şerit ekranı süpürür): kumaş/kâğıt şeridin hışırtılı süpürüşü; dir: şeridin gittiği yön ('r' soldan sağa)."""
    dur = dur or 1.0
    n = _n(dur)
    t = np.arange(n) / SR
    u = t / dur
    env = np.sin(np.pi * np.clip(u, 0, 1)) ** 1.3
    y = D.bp(rng.standard_normal(n), 500, 3800, 2) * env * (0.8 + 0.2 * np.sin(D.PI2 * 9 * t))
    pan = (np.clip(u, 0, 1) * 2 - 1) * 0.8 * (1 if dir == "r" else -1)
    gl, gr = D.pan_gains(pan)
    x = np.stack([y * gl, y * gr], axis=1)
    m = _n(0.05)
    fl = D.hp(rng.standard_normal(m), 1500, 2) * np.exp(-np.arange(m) / (0.01 * SR))
    _place(x, fl, dur * 0.8, 0.35, 0.8 * (1 if dir == "r" else -1))
    return D.lp(x, 10000)


def _slide_glide(rng, dur, dir="r", **kw):
    """'slide' (iki çekim birlikte kayar): alçak, yumuşak ahşap-kâğıt kayma + hava; dir: kameranın yönü ('r': içerik sola akar → pan sağdan sola)."""
    dur = dur or 1.0
    n = _n(dur)
    t = np.arange(n) / SR
    u = t / dur
    env = np.sin(np.pi * np.clip(u, 0, 1)) ** 1.2
    nz = rng.standard_normal(n)
    y = D.bp(nz, 150, 1300, 2) * env * 1.0 + D.resonator(nz, 380, 200) * env * 0.6
    pan = (np.clip(u, 0, 1) * 2 - 1) * 0.6 * (-1 if dir == "r" else 1)
    gl, gr = D.pan_gains(pan)
    return np.stack([y * gl, y * gr], axis=1)


def _iris_ring(rng, dur, obj="florin", root=None, **kw):
    """'iris' (yuvarlak nesne ekranı doldurur): nesneye göre — florin: sikke halkası; palle: oyuk ahşap top 'tok'; sun/moon: ışık kabarması; dome: alçak kubbe rezonansı;
    lens: cam tınısı; seal: mühür darbesi."""
    dur = dur or 1.2
    if obj == "florin":
        n = _n(dur)
        x = np.zeros((n, 2))
        _place(x, _coin_ring(rng, f0=float(rng.uniform(3000, 3800)), tau=0.16), 0.0, 0.8, 0.0)
        _place(x, _coin_ring(rng, f0=float(rng.uniform(2600, 3300)), tau=0.12), 0.09, 0.5, 0.2)
        sw = _whoosh(rng_for("iris", int(rng.integers(1 << 30))), dur, False) * 0.35
        x[:len(sw)] += sw[:n]
        return D.lp(x, 14000)[:n]
    if obj == "palle":
        n = _n(dur)
        t = np.arange(n) / SR
        y = D.resonator(rng.standard_normal(n), 320, 70) * np.exp(-t / 0.14) * 1.4 + np.sin(D.PI2 * 190 * t) * np.exp(-t / 0.09) * 0.8
        y += D.bp(rng.standard_normal(n), 900, 3200, 2) * np.exp(-t / 0.008) * 0.5
        x = np.stack([y, y], axis=1)
        return _room(x, 0.15, 0.7)[:n]
    if obj in ("sun", "moon"):
        return _light_swell(rng, dur + 0.8, root=float(root or (392.0 if obj == "sun" else 329.63)))
    if obj == "dome":
        n = _n(dur + 0.8)
        t = np.arange(n) / SR
        y = (np.sin(D.PI2 * 82.4 * t) + 0.6 * np.sin(D.PI2 * 123.5 * t) + 0.4 * np.sin(D.PI2 * 165 * t)) * (1 - np.exp(-t / 0.35)) * np.exp(-np.maximum(t - 0.5, 0) / 0.9) * 0.6
        y += D.bp(rng.standard_normal(n), 150, 900, 2) * (1 - np.exp(-t / 0.3)) * np.exp(-np.maximum(t - 0.4, 0) / 0.6) * 0.25
        return _room(np.stack([y, y], axis=1), 0.5, 2.4)[:n]
    if obj == "lens":
        return _glass_chime(rng, dur + 1.5)
    if obj == "seal":
        return _wax_seal_stamp(rng, dur)
    return _whoosh(rng, dur, False)


def _whoosh_dir(rng, dur, dir="l", soft=False, **kw):
    """Yönlü whoosh (whip/wipe): dir KAMERA yönüdür; içerik tersine akar → 'r' için ses sağdan sola kayar. soft=True: wipe (daha yumuşak, parıltılı)."""
    x = _whoosh(rng, dur or (0.9 if soft else 0.7), False)
    pan_sign = -1.0 if dir == "r" else 1.0
    # _whoosh varsayılanı soldan sağa; ters yön için kanalları çevir
    if pan_sign < 0:
        x = x[:, ::-1].copy()
    return D.lp(x, 6500) if soft else x


def _chapter_stinger_flavor(rng, dur, root=None, flavor="altin", **kw):
    """Bölüm kartı vurgusu — perde rengine göre: altin (P1: sıcak org + lavta/çan parıltısı), bedel (P2: koyu — alçak org beşlisi + gamba + hafif gong, çan yok),
    miras (P3: sakin — yumuşak org + üç notalık lavta hücresi)."""
    dur = dur or 2.6
    r = float(root or 146.83)
    n = _n(dur)
    x = np.zeros((n, 2))
    if flavor == "bedel":
        for i, st in enumerate((0, 7, 12)):
            f = r * 2 ** (st / 12)
            tab = D.additive_table(f, lambda ff: (f / ff) ** 1.6 / (1 + (ff / 3200.0) ** 4), rng, phase="random")
            y = D.wt_osc(tab, f * (1 + rng.uniform(-0.0004, 0.0004)), n, phase0=rng.random()) * D.adsr(n, 0.25, 0.2, 0.8, 1.4)
            gl, gr = D.pan_gains((-0.2, 0.2, 0.0)[i])
            x[:, 0] += y * gl
            x[:, 1] += y * gr
        g = D.gong_tone(r * 0.5, dur, 1.0, rng, bloom=1.0)
        x += 0.22 * np.stack([g, g * 0.85], axis=1)
        return _room(x, 0.3, 2.0)[:n]
    if flavor == "miras":
        xo = _golden_chord(rng, r, dur, organ=0.7, gong=0.0, bell=0.0, attack=0.25, release=1.4, voicing=(0, 7, 12, 16))
        x += xo
        for k, (dt, st) in enumerate(((0.35, 7), (0.75, 7), (1.2, 4))):     # üç nota: tekrar eden iki + düşen üçlü
            f = r * 4 * 2 ** (st / 12)
            y = D.ks_string(f, 1.6, rng, S=0.5, t60=2.0, bright=0.5, pick=0.15, damp=0.3, vel=1.0)
            y = D.fade_edges(y, 0.0004, 0.05)
            _place(x, y / (np.max(np.abs(y)) + 1e-9) * 0.5, dt, 1.0, 0.15)
        return _room(x, 0.25, 1.8)[:n]
    xo = _golden_chord(rng, r, dur, organ=1.0, gong=0.4, bell=0.45, attack=0.07, release=1.2)
    return _room(xo, 0.25, 1.8)[:n]


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
    """SFX üretir → float32 (n,2) @48 kHz, tepe −3 dBFS. Döngü sesleri: dur=None → 8 sn dikişsiz döngü.
    dur: istenen uzunluk (sn). Üreteç çok kısa dur'u desteklemezse doğal uzunlukta üretilip dur'a kırpılır (40 ms sönümle)."""
    if name not in REGISTRY:
        raise KeyError(f"bilinmeyen SFX: {name}  (mevcut: {', '.join(SFX_NAMES)})")
    if name in LOOPABLE:
        rng = rng_for("sfx", name, int(seed))
        x = REGISTRY[name](rng, LOOP_SEC)
        x = _finish(x, loop=True, name=name)
        if dur is not None and abs(dur - LOOP_SEC) > 1e-6:
            x = _fit(x.astype(np.float64), dur, loop=True)
            x = D.peak_norm(x, PEAK_DB)
        return x.astype(np.float32)
    x = None
    if dur is not None:
        try:
            x = np.asarray(REGISTRY[name](rng_for("sfx", name, int(seed)), dur, **kw), dtype=np.float64)
            if not np.isfinite(x).all() or np.max(np.abs(x)) < 1e-6:
                x = None
        except Exception:      # noqa — çok kısa/uygunsuz dur: doğal uzunluğa dön
            x = None
    if x is None:
        x = np.asarray(REGISTRY[name](rng_for("sfx", name, int(seed)), None, **kw), dtype=np.float64)
    if dur is not None:
        x = _fit(x, dur, loop=False)
    return _finish(x, name=name)


# ═══════════════════════════ MEDICI kayıt defteri ek girişleri ═══════════════════════════
REGISTRY.update({
    # kapı / kilit / metal / tahta
    "door_bolt": _door_bolt, "door_bronze": _door_bronze, "lock_click": _lock_click,
    "knock_wood": lambda rng, dur, **kw: _knock(rng, dur, "wood", **kw), "knock_metal": lambda rng, dur, **kw: _knock(rng, dur, "metal", **kw),
    # kalabalık / mekân (sözsüz)
    "crowd_chant": _crowd_chant, "applause_far": _applause_far, "church_ambience": _church_ambience,
    "hoof_far": _hoof_far, "footsteps": _footsteps, "distant_trumpet": _distant_trumpet,
    # deniz / halat / su / ateş / mum
    "rope_creak": _rope_creak, "water_lap": _water_lap, "candle_flame": _candle_flame, "candle_snuff": _candle_snuff, "candle_out_in": _candle_out_in,
    # mekanizma / yazı / kâğıt / taş
    "keyboard_action": _keyboard_action, "glass_chime": _glass_chime, "stamp_thud": _stamp_thud, "coin_roll": _coin_roll,
    "type_set": _type_set, "press_thud": _press_thud, "book_close": _book_close, "letter_open": _letter_open,
    "pin_stick": _pin_stick, "chisel_tap": _chisel_tap, "brush_stroke": _brush_stroke,
    # geçiş sesleri
    "wash_swell": _wash_swell, "plaster_scrape": _plaster_scrape, "dip_drop": _dip_drop, "light_swell": _light_swell,
    "zoom_rush": _zoom_rush, "zoom_rush_long": lambda rng, dur, **kw: _zoom_rush(rng, dur, True), "cloth_sweep": _cloth_sweep,
    "slide_glide": _slide_glide, "iris_ring": _iris_ring, "whoosh_dir": _whoosh_dir,
    # perde rengine göre bölüm vurgusu (flavor=altin|bedel|miras); eski ad korunur
    "chapter_stinger": _chapter_stinger_flavor,
})
LOOPABLE |= {"church_ambience", "water_lap", "candle_flame"}
CREST.update({"door_bolt": 22, "door_bronze": 20, "lock_click": 22, "knock_wood": 22, "knock_metal": 22, "crowd_chant": 16, "applause_far": 16,
              "hoof_far": 20, "footsteps": 20, "distant_trumpet": 16, "rope_creak": 18, "candle_snuff": 18, "candle_out_in": 18,
              "keyboard_action": 24, "glass_chime": 20, "stamp_thud": 22, "coin_roll": 20, "type_set": 24, "press_thud": 20,
              "book_close": 20, "letter_open": 20, "pin_stick": 22, "chisel_tap": 22, "brush_stroke": 16, "dip_drop": 18, "zoom_rush": 18,
              "zoom_rush_long": 18, "cloth_sweep": 16, "slide_glide": 16, "iris_ring": 20, "plaster_scrape": 18, "wash_swell": 16})
SFX_NAMES = sorted(REGISTRY)

# ───────────────────────── katalog meta: Türkçe ad, tür, doğal süre, not ─────────────────────────
CATALOG = {   # ad: (Türkçe, grup)
    "page_turn": ("sayfa çevirme", "kâğıt/yazı"), "paper_rustle": ("kâğıt hışırtısı", "kâğıt/yazı"), "quill_scratch": ("kalem/tüy çiziği", "kâğıt/yazı"),
    "wax_seal_stamp": ("mühür", "kâğıt/yazı"), "stamp_thud": ("damga çarpması", "kâğıt/yazı"), "letter_open": ("mektup açılışı", "kâğıt/yazı"),
    "book_close": ("defter kapanışı", "kâğıt/yazı"), "type_set": ("harf dizimi (matbaa)", "kâğıt/yazı"), "press_thud": ("baskı presi", "kâğıt/yazı"),
    "pin_stick": ("harita iğnesi", "kâğıt/yazı"), "brush_stroke": ("fırça darbesi", "kâğıt/yazı"),
    "coin_clink": ("sikke şıngırtısı", "para"), "coin_pile": ("sikke yığını", "para"), "coin_roll": ("sikke yuvarlanır", "para"),
    "door_bolt": ("kapı sürgüsü", "kapı/metal"), "door_bronze": ("tunç kapı çarpması", "kapı/metal"), "lock_click": ("kilit/anahtar", "kapı/metal"),
    "gate_thud": ("ağır kapı çarpması (ahşap+zincir)", "kapı/metal"), "knock_wood": ("tahta vuruş", "kapı/metal"), "knock_metal": ("metal tık", "kapı/metal"),
    "keyboard_action": ("klavye mekanizması (klavsen/piyano)", "kapı/metal"), "glass_chime": ("lens/cam tınısı", "kapı/metal"), "chisel_tap": ("sert taş oyma", "kapı/metal"),
    "crowd_murmur": ("kalabalık uğultusu (sözsüz)", "kalabalık/mekân"), "crowd_chant": ("ritmik kalabalık haykırışı (sözsüz)", "kalabalık/mekân"),
    "applause_far": ("uzak alkış", "kalabalık/mekân"), "church_ambience": ("kilise içi oda tonu", "kalabalık/mekân"), "footsteps": ("adımlar (taş/ahşap)", "kalabalık/mekân"),
    "horse_hooves": ("nal sesi (dörtnala/yürüyüş)", "kalabalık/mekân"), "hoof_far": ("uzaklaşan tek at", "kalabalık/mekân"), "distant_trumpet": ("uzak trompet", "kalabalık/mekân"),
    "fire_crackle": ("ateş çıtırtısı", "doğa"), "candle_flame": ("mum alevi (döngü)", "doğa"), "candle_snuff": ("mum sönmesi", "doğa"),
    "sea_waves": ("deniz dalgaları", "doğa"), "water_lap": ("liman suyu (döngü)", "doğa"), "ship_creak": ("gemi ahşap gıcırtısı", "doğa"), "rope_creak": ("halat gerilimi", "doğa"),
    "wind": ("rüzgâr", "doğa"), "rain": ("yağmur", "doğa"), "thunder": ("gök gürültüsü", "doğa"),
    "church_bell": ("kilise çanı (YALNIZ kaynaklı olay)", "çan/gong/vuruş"), "bell_toll_low": ("alçak çan (YALNIZ kaynaklı olay)", "çan/gong/vuruş"), "gong_hit": ("gong", "çan/gong/vuruş"),
    "title_hit": ("ana başlık vuruşu", "çan/gong/vuruş"), "chapter_stinger": ("bölüm kartı vurgusu (flavor=altin|bedel|miras)", "çan/gong/vuruş"),
    "drum_hit": ("çerçeve davulu vuruşu", "çan/gong/vuruş"), "heartbeat": ("kalp atışı", "çan/gong/vuruş"), "tick": ("kuru tık", "çan/gong/vuruş"),
    "cannon_boom": ("top (uzak, YALNIZ kuşatma)", "çan/gong/vuruş"), "sword_clash": ("kılıç (kullanma: şiddet gösterilmez)", "çan/gong/vuruş"), "magic_chime": ("büyülü çınlama (Şarlken'den; Medici'de kullanılmaz)", "çan/gong/vuruş"),
    "whoosh": ("whoosh (soldan sağa)", "geçiş"), "whoosh_long": ("uzun whoosh", "geçiş"), "whoosh_dir": ("yönlü whoosh (whip/wipe)", "geçiş"),
    "wash_swell": ("pigment yıkama", "geçiş"), "plaster_scrape": ("fresko sıva", "geçiş"), "dip_drop": ("siyaha iniş", "geçiş"), "light_swell": ("ışık huzmesi", "geçiş"),
    "zoom_rush": ("zum hücumu", "geçiş"), "zoom_rush_long": ("uzun zum-geçiş", "geçiş"), "cloth_sweep": ("şerit süpürüşü", "geçiş"), "slide_glide": ("kayma", "geçiş"),
    "iris_ring": ("iris (obj=florin|palle|sun|moon|dome|lens|seal)", "geçiş"), "candle_out_in": ("mum söner-yanar (candle)", "geçiş"),
}

# ───────────────────────── kaynak politikası: olay sesi olarak YASAK adlar (bölüm → ad kümesi) ─────────────────────────
_BELLS = {"church_bell", "bell_toll_low", "gong_hit"}
POLICY_FORBID = {
    "c7": _BELLS,       # 26 Nisan 1478: çan çalma iddiası kaynakta yok ("SAAT/HAVA/KOKU/ÇAN YOK")
    "c10": _BELLS,      # 9 Kasım 1494: saat/ışık/ÇAN yok (Capponi'nin 'çanlarla yanıt' sözü anlatıda söylenir; olay sesi DEĞİL)
    "c13": _BELLS,      # 24 Ağustos 1572: şiddet yok, çan yok
}
POLICY_NOTE = {"c7": "c7: çan olay sesi yasak (kaynakta yok)", "c10": "c10: çan olay sesi yasak (kaynakta yok)", "c13": "c13: çan olay sesi yasak (1572: şiddet yok, çan yok)"}
ALWAYS_AVOID = {"sword_clash": "şiddet gösterilmez (hançer/kılıç sesi yok)", "magic_chime": "Şarlken sesi; Medici paletinde yok"}

# ───────────────────────── JSON sözleşmesi: sfx_cues_pN.json ─────────────────────────
"""
Biçim (UTF-8 JSON; kökte nesne ya da doğrudan liste):
{ "surum": 1, "parca": 2,
  "ayar": { "varsayilan_stinger": true, "gecis_sesleri": true },
  "cues": [ { "id": "c7-oda", "ad": "church_ambience", "capa": ["c7s2", "katedralinde", -0.4], "bitis_capa": ["c7s3", "end", -1.5],
              "seviye": -26, "pan": 0.0, "tohum": 3, "dongu": true, "gir": 1.0, "cik": 1.5, "bastir_db": -4, "parametre": {}, "bolum": "c7",
              "not": "J-kesme: ayin yankısı görüntüden 0,4 sn önce", "kaynak": "scenes_c7.py V1" }, ... ] }
Alanlar (Türkçe birincil, İngilizce Şarlken adı eşdeğerdir):
  t | capa (anchor)     başlangıç: parça ses ekseninde saniye YA DA zaman çizelgesi çapası ["c7s17"] | ["c7s17", 0.3] | ["c7s17","sözcük",-0.1] | ["c7s17","end",0]
  erken (lead)           sesi çapadan X sn ÖNCE başlat (J-kesme / ses köprüsü); varsayılan 0
  ad (name)              sfx.py adı (python3 sfx.py --list)           seviye (gain_db)  dB (tepe −3 dBFS'e göre; ambiyans −24…−30, olay −14…−22)
  sure (dur)             sn | null (doğal)                            dongu (loop)      true + sure (ya da bitis_capa) → dikişsiz döngü
  bitis_capa (end_anchor) döngü/yatak bitişi (sure yerine)             gir/cik (fade_in/fade_out) yumuşatma sn
  bastir_db (duck_db)    konuşma altında kısma (döngüde varsayılan −4)  parametre (params)  {"root": Hz, "obj": "florin", "dir": "r", "flavor": "bedel"...}
  tohum (seed)           tekrarlanabilirlik                           bolum (ch)         yalnız kaynak-politikası denetimi için ipucu
  kapali                 true → atlanır (silmeden devre dışı)          not / kaynak       serbest metin
"""
CUE_ALIASES = {"capa": "anchor", "ad": "name", "seviye": "gain_db", "tohum": "seed", "sure": "dur", "dongu": "loop", "erken": "lead",
               "bitis_capa": "end_anchor", "gir": "fade_in", "cik": "fade_out", "bastir_db": "duck_db", "parametre": "params", "bolum": "ch",
               "not": "note", "kapali": "off"}


def normalize_cue(raw):
    """Ham (Türkçe/İngilizce anahtarlı) cue → kanonik sözlük (İngilizce anahtarlar). Bilinmeyen anahtarlar 'extra'da saklanır."""
    c = {}
    for k, v in raw.items():
        c[CUE_ALIASES.get(k, k)] = v
    if "name" not in c:
        raise ValueError(f"cue'da 'ad' yok: {raw}")
    if c["name"] not in REGISTRY:
        raise KeyError(f"bilinmeyen SFX adı '{c['name']}' (python3 sfx.py --list)")
    if "t" not in c and "anchor" not in c:
        raise ValueError(f"cue'da 't' ya da 'capa' yok: {raw}")
    c.setdefault("gain_db", -20.0)
    c.setdefault("pan", 0.0)
    c.setdefault("seed", 0)
    c.setdefault("dur", None)
    c.setdefault("loop", False)
    c.setdefault("lead", 0.0)
    c.setdefault("params", {})
    return c


def load_cue_file(path):
    """sfx_cues_pN.json → (cue listesi [ham], ayar sözlüğü). Dosya yoksa ([], {})."""
    import json
    if not path or not os.path.exists(path):
        return [], {}
    d = json.load(open(path, encoding="utf-8"))
    if isinstance(d, list):
        return d, {}
    return d.get("cues", []), d.get("ayar", {})


def resolve_cues(raw_cues, sent, chapters=None, quiet_zones=(), warn=print):
    """Ham cue'ları mutlak zamana çözer. Döner: (cues [miks.render_sfx_bus biçimi], uyarılar).
    - t / capa(+erken) → 't' (sn); bitis_capa → 'dur'. Çözülemeyen çapa: cue ATLANIR ve uyarılır (ses yamalanınca yeniden çözülür).
    - kaynak politikası: POLICY_FORBID (bölüme göre yasak adlar) ve ALWAYS_AVOID → cue atlanır, uyarı verilir.
    - quiet_zones (müzik sessizlik kapıları): bu aralıklarda başlayan cue için bilgi uyarısı (atlanmaz)."""
    import ses_dsp as DD
    out, warns = [], []
    ch_spans = [(c["id"], c["t0"], c["t1"]) for c in (chapters or [])]

    def chapter_at(t):
        for cid, a, b in ch_spans:
            if a - 0.01 <= t <= b + 0.01:
                return cid
        return None
    for raw in raw_cues:
        try:
            c = normalize_cue(raw)
        except (KeyError, ValueError) as e:
            warns.append(f"cue atlandı: {e}")
            continue
        if c.get("off"):
            continue
        if "t" in c and c["t"] is not None:
            t = float(c["t"])
        else:
            t = DD.anchor_time(c["anchor"], sent)
            if t is None:
                if c.get("ch") and ch_spans and c["ch"] not in {x[0] for x in ch_spans}:
                    continue            # bölüm bu parçada (henüz) yok: sessizce atla (ses gelince çözülür)
                warns.append(f"çapa çözülemedi, atlandı: {c.get('id', c['name'])} {c['anchor']}")
                continue
        t -= float(c.get("lead") or 0.0)
        dur = c.get("dur")
        if c.get("end_anchor") is not None:
            te = DD.anchor_time(c["end_anchor"], sent)
            if te is None:
                warns.append(f"bitiş çapası çözülemedi, atlandı: {c.get('id', c['name'])} {c['end_anchor']}")
                continue
            dur = max(0.2, te - t)
        ch = c.get("ch") or chapter_at(t)
        if c["name"] in ALWAYS_AVOID:
            warns.append(f"POLİTİKA: '{c['name']}' kullanılmaz ({ALWAYS_AVOID[c['name']]}); cue atlandı: {c.get('id', '')} t={t:.2f}")
            continue
        if ch in POLICY_FORBID and c["name"] in POLICY_FORBID[ch] and not c.get("kaynakli"):
            warns.append(f"POLİTİKA: {POLICY_NOTE[ch]}; '{c['name']}' atlandı (t={t:.2f}). Kaynak gösterilirse cue'ya \"kaynakli\": true ekleyin.")
            continue
        for (qa, qb) in quiet_zones:
            if qa - 0.6 <= t <= qb and not c.get("sessizlik_izni") and c["name"] not in ("door_bronze", "lock_click", "door_bolt", "gate_thud"):
                warns.append(f"bilgi: '{c['name']}' müzik sessizlik bölgesinde başlıyor (t={t:.2f}; bölge {qa:.1f}–{qb:.1f}); bilinçliyse \"sessizlik_izni\": true")
        d = dict(t=t, name=c["name"], gain_db=float(c["gain_db"]), pan=float(c["pan"]), seed=int(c["seed"]), dur=(None if dur is None else float(dur)),
                 loop=bool(c["loop"]), params=dict(c.get("params") or {}))
        for k in ("duck_db", "fade_in", "fade_out"):
            if c.get(k) is not None:
                d[k] = c[k]
        if c.get("id"):
            d["id"] = c["id"]
        if c.get("note"):
            d["note"] = c["note"]
        d["ch"] = ch
        out.append(d)
    for w in warns:
        warn("  UYARI (sfx):", w)
    return out, warns


# ───────────────────────── ses köprüsü / J-kesme kancaları ─────────────────────────
def j_cut(name, t_pic, lead=0.4, **kw):
    """J-kesme: sesi görüntüden `lead` sn ÖNCE başlat. t_pic = yeni çekimin başladığı an (sn). Döner: cue sözlüğü (kanonik)."""
    d = dict(name=name, t=float(t_pic) - float(lead), gain_db=-22.0, pan=0.0, seed=0, dur=None, loop=False, params={})
    d.update(kw)
    return d


def l_cut(name, t_cut, tail=0.6, dur=None, **kw):
    """L-kesme: eski çekimin sesi kesmeden `tail` sn sonra da sürer (cue t_cut'tan önce başlamış olmalı; dur = t_cut − t_başlangıç + tail)."""
    d = dict(name=name, t=float(t_cut) - float(dur or 2.0) + float(tail), gain_db=-22.0, pan=0.0, seed=0, dur=float(dur or 2.0), loop=False, params={})
    d.update(kw)
    return d


def ses_koprusu(name_out, name_in, t_cut, tail=0.5, lead=0.4, **kw):
    """İki çekim arasında ses köprüsü: giden sesin kuyruğu t_cut'tan sonra `tail` sn sürer; gelen ses t_cut'tan `lead` sn önce girer. [cue, cue] döner."""
    return [l_cut(name_out, t_cut, tail=tail, **kw), j_cut(name_in, t_cut, lead=lead, **kw)]


# ───────────────────────── motor geçişi → ses eşlemesi ─────────────────────────
# ad: (sfx adı, süre ('tr' = geçiş süresi | sn), tepe_oranı (sesin tepe noktası, ses süresi içinde), seviye dB, varsayılan parametreler)
TRANSITION_MAP = {
    "fade":     None,
    "yikama":   ("wash_swell", "tr", 0.45, -23.0, {}),
    "sayfa":    ("page_turn", 1.1, 0.35, -20.0, {}),
    "giornata": ("plaster_scrape", "tr", 0.5, -23.0, {}),
    "dip":      ("dip_drop", 2.6, 0.12, -20.0, {}),
    "zoom":     ("zoom_rush", 0.9, 0.80, -24.0, {}),
    "whip":     ("whoosh_dir", 0.7, 0.45, -20.0, {"soft": False}),
    "wipe":     ("whoosh_dir", 0.9, 0.5, -24.0, {"soft": True}),
    "iris":     ("iris_ring", 1.2, 0.35, -21.0, {"obj": "florin"}),
    "slide":    ("slide_glide", "tr", 0.5, -24.0, {"dir": "r"}),
    "zoomthru": ("zoom_rush_long", 1.5, 0.80, -22.0, {}),
    "carry":    ("cloth_sweep", "tr", 0.5, -23.0, {"dir": "r"}),
    "light":    ("light_swell", 2.6, 0.35, -22.0, {}),
    "candle":   ("candle_out_in", 3.0, 0.15, -21.0, {}),
}
# ağır/ciddi bölümlerde geçiş sesleri kısılır (dB); sessizlik kapılarında hiç çalmaz
TRANSITION_CH_TRIM = {"c7": -5.0, "c9": -2.0, "c10": -4.0, "c11": -4.0, "c12": -2.0, "c15": -3.0, "c16": -2.0}


def transition_cues(shots, quiet_zones=(), chapter_of=None):
    """Çekim listesinden otomatik geçiş sesleri. shots: [{t0, t1, tr: (ad, süre, opts)|None, link, kind, label}] (t0/t1 parça ekseni; tr = Program'ın tr_eff'i).
    place='before': geçiş gelen çekimin başında BİTER ([t0−d, t0]); place='after': gelen çekimin ilk d sn'sinde sürer ([t0, t0+d]).
    link='audio' (ses köprüsü) ise otomatik ses atlanır: sahne yazarı açık cue verir. Sessizlik kapılarında (müzik çekilen yıldız anlar) çalmaz.
    Döner: [cue sözlüğü (kanonik)]."""
    out = []
    for i, s in enumerate(shots):
        tr = s.get("tr")
        if not tr:
            continue
        name, d, opts = tr[0], float(tr[1]), (tr[2] if len(tr) > 2 else {}) or {}
        spec = TRANSITION_MAP.get(name)
        if spec is None:
            continue
        if s.get("link") == "audio":
            continue
        if str(s.get("label", "")).startswith(("bölüm kartı", "ana başlık", "bitiş ekranı")):
            continue        # kartların kendi ses tasarımı var (chapter_stinger / title_hit)
        snd, dur, peak, gdb, prm = spec
        prm = dict(prm)
        if name == "iris" and opts.get("obj"):
            prm["obj"] = opts["obj"]
        if name in ("slide", "carry", "whip", "wipe") and opts.get("dir") in ("r", "l"):
            prm["dir"] = opts["dir"]
        if name in ("slide", "carry") and opts.get("dir") in ("u", "d"):
            prm["dir"] = "r"
        place = opts.get("place", "before")
        t_a, t_b = (s["t0"], s["t0"] + d) if place == "after" else (s["t0"] - d, s["t0"])
        mid = 0.5 * (t_a + t_b)
        sd = d if dur == "tr" else float(dur)
        sd = max(sd, 0.4)
        t_start = mid - peak * sd
        if any(qa - 0.6 <= mid <= qb for (qa, qb) in quiet_zones):
            continue
        ch = chapter_of(mid) if chapter_of else None
        g = gdb + TRANSITION_CH_TRIM.get(ch, 0.0)
        out.append(dict(t=round(t_start, 3), name=snd, gain_db=round(g, 2), pan=0.0, seed=1000 + i, dur=(round(sd, 3) if dur == "tr" or snd in ("page_turn",) else None),
                        loop=False, params=prm, id=f"gecis-{i}-{name}", note=f"geçiş '{name}' ({s.get('label', '')})", ch=ch))
    return out


def shots_from_program(prog):
    """compose.Program → transition_cues girdisi (duck-typed: prog.shots[i].t0/t1/tr_eff/link/kind/label, prog.t_off). Görüntü motoruna bağımlılık yok."""
    off = float(getattr(prog, "t_off", 0.0) or 0.0)
    out = []
    for s in prog.shots:
        out.append(dict(t0=float(s.t0) - off, t1=float(s.t1) - off, tr=getattr(s, "tr_eff", None), link=getattr(s, "link", None),
                        kind=getattr(s, "kind", ""), label=getattr(s, "label", "")))
    return out


def sfx_hints_from_program(prog):
    """Çekimlere ileride eklenecek `sfx=` ipucu (shot(..., sfx=[...])). Her öğe: (ad, dt[, seviye]) demeti ya da cue sözlüğü.
    dt / sözlükte 't': ÇEKİM BAŞINDAN saniye (mutlak istenirse sözlüğe "mutlak": true) ya da çapa listesi (["c7s17","sözcük",-0.1]).
    Döner: ham cue listesi (resolve_cues girdisi). Çekimde `sfx` yoksa boş."""
    off = float(getattr(prog, "t_off", 0.0) or 0.0)
    raw = []
    for s in prog.shots:
        for h in (getattr(s, "sfx", None) or []):
            if isinstance(h, dict):
                c = dict(h)
                if "t" in c and not c.pop("mutlak", False):
                    c["t"] = float(s.t0) - off + float(c["t"])
            else:
                c = dict(ad=h[0], seviye=(h[2] if len(h) > 2 else -20))
                if isinstance(h[1], (int, float)):
                    c["t"] = float(s.t0) - off + float(h[1])
                else:
                    c["capa"] = h[1]
            c.setdefault("kaynak", f"çekim #{getattr(s, 'i', '?')} {getattr(s, 'kind', '')} '{getattr(s, 'label', '')}'")
            raw.append(c)
    return raw


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
