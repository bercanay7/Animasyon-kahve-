"""scipy yerine yalnız numpy (bu kapta scipy yok, kurulum izni yok). score.py'nin kullandığı alt küme:
butter + sosfilt (FFT ile sıfır fazlı Butterworth genlik yanıtı), lfilter (1 ve 2 kutuplu özyineli: kesilmiş dürtü yanıtıyla katlama),
fft (rfft/irfft/next_fast_len), ikili morfoloji ve 1B en büyük/en küçük süzgeçleri.
Fark: filtreler sıfır fazlı (nedensel değil); sentez için duyulur bir fark yaratmaz."""
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def next_fast_len(n, real=True):
    n = int(n); m = 1
    while m < n: m *= 2
    # 2'nin kuvveti ile 3·2^k arasından küçüğü
    m3 = 3
    while m3 < n: m3 *= 2
    return min(m, m3)


class fft:
    next_fast_len = staticmethod(next_fast_len)
    @staticmethod
    def rfft(x, n=None, axis=-1, workers=None): return np.fft.rfft(x, n=n, axis=axis)
    @staticmethod
    def irfft(x, n=None, axis=-1, workers=None): return np.fft.irfft(x, n=n, axis=axis)


def butter(order, f, kind, fs=48000, output='sos'):
    return (kind, f, fs, order)


def sosfilt(sos, x, axis=0):
    kind, f, fs, order = sos
    x = np.asarray(x, np.float64)
    n = x.shape[axis]
    if n < 4: return x.copy()
    L = next_fast_len(n + 64)
    X = np.fft.rfft(x, n=L, axis=axis)
    fr = np.fft.rfftfreq(L, 1.0 / fs)
    lpf = lambda fc: 1.0 / np.sqrt(1.0 + (fr / fc) ** (2 * order))
    hpf = lambda fc: 1.0 / np.sqrt(1.0 + (fc / np.maximum(fr, 1e-6)) ** (2 * order))
    if kind == 'lowpass': H = lpf(f)
    elif kind == 'highpass': H = hpf(f)
    else: H = hpf(f[0]) * lpf(f[1])
    shp = [1] * X.ndim; shp[axis] = -1
    y = np.fft.irfft(X * H.reshape(shp), n=L, axis=axis)
    return np.take(y, np.arange(n), axis=axis)


def _conv(x, h):
    n = len(x); L = next_fast_len(n + len(h))
    return np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(h, L), L)[:n]


def lfilter(b, a, x, zi=None):
    x = np.asarray(x, np.float64); n = len(x)
    if len(a) == 2:                                   # y[n] = b0 x[n] - a1 y[n-1]
        p = -a[1]
        m = int(min(n, max(16, np.log(1e-7) / np.log(max(abs(p), 1e-9)))))
        h = b[0] * p ** np.arange(m)
        y = _conv(x, h)
        if zi is not None: y = y + zi[0] * p ** np.arange(n)
        return (y, None) if zi is not None else y
    if len(a) == 3:                                   # iki kutuplu rezonatör
        a1, a2 = a[1], a[2]
        r = np.sqrt(max(a2, 1e-12)); c = np.clip(-a1 / (2 * r), -1, 1); w = np.arccos(c)
        m = int(min(n, max(32, np.log(1e-7) / np.log(max(r, 1e-9)))))
        k = np.arange(m)
        h = b[0] * r ** k * (np.sin((k + 1) * w) / np.sin(w) if abs(np.sin(w)) > 1e-9 else (k + 1))
        y = _conv(x, h)
        return (y, None) if zi is not None else y
    raise NotImplementedError('lfilter: yalnız 1 ve 2 kutuplu')


def maximum_filter1d(x, size):
    p = size // 2; xp = np.pad(x, (p, size - 1 - p), mode='edge'); return sliding_window_view(xp, size).max(axis=1)


def minimum_filter1d(x, size):
    p = size // 2; xp = np.pad(x, (p, size - 1 - p), mode='edge'); return sliding_window_view(xp, size).min(axis=1)


def binary_dilation(x, structure):
    k = len(structure); return np.convolve(np.asarray(x, float), np.ones(k), 'same') > 0


def binary_erosion(x, structure):
    k = len(structure); return np.convolve(np.asarray(x, float), np.ones(k), 'same') >= k - 1e-9


def binary_closing(x, structure):
    return binary_erosion(binary_dilation(x, structure), structure)
