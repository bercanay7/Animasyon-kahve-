"""29 Ekim filmi için ek sentez efektler (kredi harcamadan, numpy/scipy). tools/mix.py bunları SYNTH'e ekler.
Her işlev 48 kHz mono numpy dizisi döndürür; rastgelelik mix.py'nin olay başına tohumlanan `rng`sinden gelir."""
import numpy as np
from scipy import signal
SR = 48000
_R = {'rng': np.random.default_rng(1)}
def set_rng(r): _R['rng'] = r
def _n(n): return _R['rng'].standard_normal(n)
def _bp(x, lo, hi, o=2): return signal.sosfilt(signal.butter(o, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def _lp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'lowpass', fs=SR, output='sos'), x)
def _hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'highpass', fs=SR, output='sos'), x)
def _env(n, a, r):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
def _norm(x, p=.9): m = np.abs(x).max(); return x / m * p if m > 0 else x
def _slow(n, rate, seed_mul=1.0):
    """yavaş değişen 0..1 eğri (dalga, rüzgâr esintisi)"""
    k = max(4, int(n / SR * rate) + 4); pts = _R['rng'].random(k)
    return np.interp(np.arange(n), np.linspace(0, n, k), pts)

def s_sea(len=10, **_):
    n = int(len * SR); t = np.arange(n) / SR
    # dalga: 6–9 sn periyotlu kabarma + köpük (yüksek bant) + dip uğultu
    sw = .5 + .5 * np.sin(2 * np.pi * t / 7.3 + 1.1) ** 3
    body = _lp(_n(n), 500) * (.35 + .65 * sw)
    foam = _bp(_n(n), 1500, 6000) * np.clip(sw - .55, 0, 1) ** 1.5 * 2.2
    return _norm(body + foam + .3 * _lp(_n(n), 120), .6)
def s_wind(len=10, **_):
    n = int(len * SR); g = _slow(n, .35)
    x = _bp(_n(n), 180, 900) * (.3 + .7 * g) + _bp(_n(n), 900, 2600) * .25 * g ** 2
    return _norm(x, .5)
def s_crowd(len=6, **_):
    """uzak kalabalık uğultusu: çok sayıda ses-benzeri biçimlendirici gürültü"""
    n = int(len * SR); x = np.zeros(n)
    for k in range(14):
        f0 = 300 + 900 * _R['rng'].random(); am = _slow(n, 3 + 4 * _R['rng'].random())
        x += _bp(_n(n), f0 * .8, f0 * 1.25) * (am > .45) * am
    x = _lp(x, 2500)
    return _norm(x, .55)
def s_cheer(len=3, **_):
    n = int(len * SR); x = s_crowd(len=len) * 1.0 + _bp(_n(n), 600, 3500) * .4
    e = np.minimum(1, np.arange(n) / (.35 * SR)) * np.exp(-np.maximum(0, np.arange(n) / SR - len * .5) * 1.5)
    return _norm(x * e, .8)
def s_typewriter(len=1.2, rate=11, **_):
    """daktilo: düzensiz tuş vuruşları + sonda zil yok (damga yazarken)"""
    n = int(len * SR); x = np.zeros(n); tt = 0.0
    while tt < len - .05:
        i = int(tt * SR); m = int(.035 * SR)
        k = (_bp(_n(m), 1800, 7000) * _env(m, .0005, .006) + .6 * _bp(_n(m), 300, 900) * _env(m, .001, .012))
        x[i:i + m] += k[:max(0, min(m, n - i))] * (.7 + .3 * _R['rng'].random())
        tt += (1 / rate) * (.6 + .8 * _R['rng'].random())
    return _norm(x, .8)
def s_carriage(**_):
    """daktilo satır başı: kısa zil + kayma"""
    n = int(.6 * SR); t = np.arange(n) / SR
    bell = (np.sin(2 * np.pi * 2350 * t) + .4 * np.sin(2 * np.pi * 5100 * t)) * _env(n, .001, .18)
    slide = _bp(_n(n), 800, 3000) * np.clip((t - .08) / .05, 0, 1) * np.exp(-np.maximum(0, t - .1) * 9) * .5
    return _norm(bell * .6 + slide, .7)
def s_telegraph(len=2.0, **_):
    """telgraf alıcısı: mors benzeri tık–tak (vuruş ve bırakma)"""
    n = int(len * SR); x = np.zeros(n); tt = 0.02
    def click(i, f, g):
        m = int(.02 * SR); c = (np.sin(2 * np.pi * f * np.arange(m) / SR) * .5 + _bp(_n(m), 1500, 5000)) * _env(m, .0003, .004) * g
        x[i:i + m] += c[:max(0, min(m, n - i))]
    while tt < len - .1:
        d = .06 if _R['rng'].random() < .55 else .18
        click(int(tt * SR), 900, 1.0); click(int((tt + d) * SR), 650, .55)
        tt += d + .07 + (.2 if _R['rng'].random() < .2 else 0)
    return _norm(x, .75)
def s_whistle(len=2.4, rate=1.0, **_):
    """vapur düdüğü: alçak, iki harmonikli, nefesli (rate: perde çarpanı; 1 = Sol3 196 Hz, 1.1225 = La3 220 Hz)"""
    n = int(len * SR); t = np.arange(n) / SR
    f = 196 * rate * (1 + .004 * np.sin(2 * np.pi * 5 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + .6 * np.sin(2 * ph) + .35 * np.sin(3 * ph) + .2 * np.sin(5 * ph)
    x += _bp(_n(n), 300, 1400) * .25
    e = np.minimum(1, t / .25) * np.minimum(1, (len - t) / .5)
    return _norm(_lp(x * e, 2200), .7)
def s_cannon(**_):
    """uzak top: kısa çatlama + uzun alçak gürleme"""
    n = int(3.5 * SR); t = np.arange(n) / SR
    crack = _bp(_n(n), 300, 2500) * _env(n, .001, .05) * .5
    rum = _lp(_n(n), 90, 4) * _env(n, .02, .9) * 3
    return _norm(crack + rum, .9)
def s_bell(**_):
    """okul zili (el zili): metal çan, birkaç sallama"""
    n = int(1.6 * SR); x = np.zeros(n); t0 = 0
    for k in range(4):
        i = int((k * .22) * SR); m = n - i; tt = np.arange(m) / SR
        c = sum(a * np.sin(2 * np.pi * f * tt) for f, a in [(1180, 1), (2950, .5), (4400, .25), (6100, .12)]) * _env(m, .001, .35)
        x[i:] += c * (1 - k * .15)
    return _norm(x, .7)
def s_press(**_):
    """baskı makinesi: merdane kayması + kalıp oturma vuruşu"""
    n = int(.9 * SR); t = np.arange(n) / SR
    roll = _bp(_n(n), 120, 900) * np.sin(np.pi * np.clip(t / .7, 0, 1)) * .5
    clack = (_bp(_n(n), 400, 3000) * _env(n, .0005, .02) + _lp(_n(n), 200) * _env(n, .001, .08) * 1.6)
    clack = np.roll(clack, int(.62 * SR)); clack[:int(.62 * SR)] = 0
    return _norm(roll + clack, .8)
def s_chalk(len=.8, **_):
    n = int(len * SR); g = (_slow(n, 18) > .35).astype(float)
    g = np.convolve(g, np.ones(240) / 240, 'same')
    return _norm(_bp(_n(n), 2500, 8000) * g * .6 + _bp(_n(n), 600, 1500) * g * .3, .5)
def s_steps(len=3, rate=1.7, **_):
    n = int(len * SR); x = np.zeros(n); tt = .05
    while tt < len - .1:
        i = int(tt * SR); m = int(.12 * SR)
        k = _lp(_n(m), 400) * _env(m, .002, .03) + _bp(_n(m), 800, 3000) * _env(m, .001, .01) * .4
        x[i:i + m] += k[:max(0, min(m, n - i))]; tt += 1 / rate * (.92 + .16 * _R['rng'].random())
    return _norm(x, .7)

def s_train(len=5, rate=1.0, **_):
    """uzak buharlı tren: tekerlek turu başına 4 püf (vurgulu), ray ek yeri tık-tıkı, alçak gürültü; uzaklık için 3 kHz alçak geçiren"""
    n = int(len * SR); x = np.zeros(n); r = _R['rng']
    per = 1 / (3.2 * rate); tt = .03; k = 0
    while tt < len - .05:
        i = int(tt * SR); m = min(int(.25 * SR), n - i)
        if m > 0:
            ch = _bp(_n(m), 250, 2400) * _env(m, .006, .085) * (1.0, .6, .8, .55)[k % 4] * (.85 + .3 * r.random())
            x[i:i + m] += ch
        tt += per * (.97 + .06 * r.random()); k += 1
    tt = .4
    while tt < len - .2:
        for d in (0, .13):
            i = int((tt + d) * SR); m = min(int(.05 * SR), n - i)
            if m > 0: x[i:i + m] += _bp(_n(m), 300, 1500) * _env(m, .0005, .012) * .5
        tt += 1.1 * (.95 + .1 * r.random())
    x += _lp(_n(n), 150, 4) * .35
    return _norm(_lp(x, 3000), .7)

EXTRA = dict(train=s_train, sea=s_sea, wind=s_wind, crowd=s_crowd, cheer=s_cheer, typewriter=s_typewriter, carriage=s_carriage, telegraph=s_telegraph,
             whistle=s_whistle, cannon=s_cannon, bell=s_bell, press=s_press, chalk=s_chalk, steps=s_steps)
EXTRA_LOOP = {'sea', 'wind', 'crowd'}
