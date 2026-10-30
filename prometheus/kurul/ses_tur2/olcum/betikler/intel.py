import sys, numpy as np, json, re, soundfile as sf
from scipy import signal
from common import *
vo = np.load('vo.npy', mmap_mode='r'); mu = np.load('mu.npy', mmap_mode='r'); mup = np.load('mu_preduck.npy', mmap_mode='r')
N = len(vo); FR = 0.02; h = int(FR * SR); nf = N // h
def fpow(x):  # (N,) -> frame power
    x = np.asarray(x[:nf * h], np.float64)
    return (x * x).reshape(nf, h).mean(1)
def band(x, lo, hi):
    if lo is None: sos = signal.butter(4, hi, 'lowpass', fs=SR, output='sos')
    elif hi is None: sos = signal.butter(4, lo, 'highpass', fs=SR, output='sos')
    else: sos = signal.butter(4, [lo, hi], 'bandpass', fs=SR, output='sos')
    return signal.sosfilt(sos, x)
BANDS = {'bb': (None, None), 'k': 'k', '1-4k': (1000, 4000), 'phone': (300, 8000), 'mid220-3800': (220, 3800),
         'o250': (177, 354), 'o500': (354, 707), 'o1k': (707, 1414), 'o2k': (1414, 2828), 'o4k': (2828, 5657), 'o8k': (5657, 11314)}
PV, PM, PP = {}, {}, {}
for name, b in BANDS.items():
    if b == 'k':
        PV[name] = fpow(kfilt(np.asarray(vo))); kk = kfilt(np.asarray(mu)); PM[name] = (fpow(kk[0]) + fpow(kk[1])) / 2; del kk
        kk = kfilt(np.asarray(mup)); PP[name] = (fpow(kk[0]) + fpow(kk[1])) / 2; del kk
    elif b == (None, None):
        PV[name] = fpow(vo); PM[name] = (fpow(mu[0]) + fpow(mu[1])) / 2; PP[name] = (fpow(mup[0]) + fpow(mup[1])) / 2
    else:
        PV[name] = fpow(band(np.asarray(vo), *b)); PM[name] = (fpow(band(np.asarray(mu[0]), *b)) + fpow(band(np.asarray(mu[1]), *b))) / 2
        PP[name] = (fpow(band(np.asarray(mup[0]), *b)) + fpow(band(np.asarray(mup[1]), *b))) / 2
    print('band', name, flush=True)
np.savez('frames.npz', **{f'v_{k}': v for k, v in PV.items()}, **{f'm_{k}': v for k, v in PM.items()}, **{f'p_{k}': v for k, v in PP.items()})
