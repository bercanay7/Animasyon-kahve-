"""
ses_dsp.py — Şarlken ses hattı (muzik.py / sfx.py / miks.py) için ortak DSP yapı taşları.
Yalnızca numpy + scipy. Harici örnek/ses dosyası YOK; her şey sentezdir.

İçerik: yardımcılar, süzgeçler (RBJ biquad), zarflar, stereo, seamless loop, algoritmik salon reverb'ü (IR + fftconvolve),
Karplus–Strong tel (blok-vektörel), dalga tablosu osilatörü, WAV G/Ç, BS.1770 ölçüm (LUFS, true-peak),
sıkıştırıcı ve true-peak duyarlı lookahead limiter.
"""
import os
import wave
import zlib

import numpy as np
from scipy import signal as sg
from scipy.ndimage import minimum_filter1d, uniform_filter1d
from scipy.signal import butter, fftconvolve, lfilter, resample_poly, sosfilt, sosfiltfilt, tf2sos

SR = 48000
PI2 = 2.0 * np.pi


# ───────────────────────── temel yardımcılar ─────────────────────────
def tt(d, sr=SR):
    """d saniyelik zaman ekseni."""
    return np.arange(int(round(d * sr))) / sr


def rng_for(*parts):
    """Kararlı (platformdan bağımsız) tohum: aynı parça → aynı rastgele akış."""
    return np.random.default_rng(zlib.crc32(repr(parts).encode("utf-8")) & 0xFFFFFFFF)


def db2lin(db):
    return 10.0 ** (np.asarray(db, dtype=np.float64) / 20.0)


def lin2db(x, floor=1e-12):
    return 20.0 * np.log10(np.maximum(np.abs(x), floor))


def midi_hz(m):
    return 440.0 * 2.0 ** ((np.asarray(m, dtype=np.float64) - 69.0) / 12.0)


def white(rng, n):
    return rng.standard_normal(int(n))


def pink(rng, n):
    """1/f gürültü (FFT şekillendirme); birim std."""
    n = int(n)
    X = np.fft.rfft(rng.standard_normal(n))
    f = np.arange(len(X), dtype=np.float64)
    f[0] = 1.0
    X = X / np.sqrt(f)
    X[0] = 0
    y = np.fft.irfft(X, n)
    return y / (np.std(y) + 1e-12)


def rms_db(x):
    x = np.asarray(x, dtype=np.float64)
    return float(10 * np.log10(np.mean(x * x) + 1e-18))


def peak_norm(x, peak_db=-3.0):
    """Tepeyi peak_db dBFS'e getirir (x float, mono/stereo)."""
    p = np.max(np.abs(x)) + 1e-12
    return (x * (db2lin(peak_db) / p)).astype(np.float32)


# ───────────────────────── süzgeçler ─────────────────────────
def _sos(kind, fc, order, sr=SR):
    if kind == "band":
        return butter(order, [fc[0], min(fc[1], sr * 0.49)], "band", fs=sr, output="sos")
    return butter(order, min(fc, sr * 0.49), kind, fs=sr, output="sos")


def lp(x, fc, order=2, sr=SR):
    return sosfilt(_sos("low", fc, order, sr), x, axis=0)


def hp(x, fc, order=2, sr=SR):
    return sosfilt(_sos("high", fc, order, sr), x, axis=0)


def bp(x, lo, hi, order=2, sr=SR):
    return sosfilt(_sos("band", (lo, hi), order, sr), x, axis=0)


def lpz(x, fc, order=2, sr=SR):
    """Sıfır faz (ileri-geri) alçak geçiren."""
    return sosfiltfilt(_sos("low", fc, order, sr), x, axis=0)


def hpz(x, fc, order=2, sr=SR):
    return sosfiltfilt(_sos("high", fc, order, sr), x, axis=0)


def bpz(x, lo, hi, order=2, sr=SR):
    return sosfiltfilt(_sos("band", (lo, hi), order, sr), x, axis=0)


def periodic_filter(sos, x):
    """Periyodik (döngü) sinyal için IIR: 3 kopya üzerinde süz, ortadakini al → dikişsiz."""
    n = len(x)
    y = sosfilt(sos, np.concatenate([x, x, x]), axis=0)
    return y[n:2 * n]


def biquad(kind, f0, gain_db=0.0, Q=0.7071, sr=SR):
    """RBJ biquad → (1,6) sos. kind: peak, lowshelf, highshelf, lp, hp, bp, notch, allpass."""
    A = 10 ** (gain_db / 40.0)
    w0 = PI2 * f0 / sr
    cw, sw = np.cos(w0), np.sin(w0)
    al = sw / (2 * Q)
    if kind == "peak":
        b = [1 + al * A, -2 * cw, 1 - al * A]
        a = [1 + al / A, -2 * cw, 1 - al / A]
    elif kind == "lowshelf":
        sA = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) - (A - 1) * cw + sA), 2 * A * ((A - 1) - (A + 1) * cw), A * ((A + 1) - (A - 1) * cw - sA)]
        a = [(A + 1) + (A - 1) * cw + sA, -2 * ((A - 1) + (A + 1) * cw), (A + 1) + (A - 1) * cw - sA]
    elif kind == "highshelf":
        sA = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) + (A - 1) * cw + sA), -2 * A * ((A - 1) + (A + 1) * cw), A * ((A + 1) + (A - 1) * cw - sA)]
        a = [(A + 1) - (A - 1) * cw + sA, 2 * ((A - 1) - (A + 1) * cw), (A + 1) - (A - 1) * cw - sA]
    elif kind == "lp":
        b = [(1 - cw) / 2, 1 - cw, (1 - cw) / 2]
        a = [1 + al, -2 * cw, 1 - al]
    elif kind == "hp":
        b = [(1 + cw) / 2, -(1 + cw), (1 + cw) / 2]
        a = [1 + al, -2 * cw, 1 - al]
    elif kind == "bp":
        b = [al, 0, -al]
        a = [1 + al, -2 * cw, 1 - al]
    elif kind == "notch":
        b = [1, -2 * cw, 1]
        a = [1 + al, -2 * cw, 1 - al]
    elif kind == "allpass":
        b = [1 - al, -2 * cw, 1 + al]
        a = [1 + al, -2 * cw, 1 - al]
    else:
        raise ValueError(kind)
    b = np.array(b, dtype=np.float64)
    a = np.array(a, dtype=np.float64)
    return np.concatenate([b / a[0], a / a[0]])[None, :]


def eq_apply(x, bands, sr=SR):
    """bands: [(kind, f0, gain_db, Q), ...] → sıralı biquad zinciri."""
    sos = np.concatenate([biquad(k, f, g, q, sr) for (k, f, g, q) in bands], axis=0)
    return sosfilt(sos, x, axis=0)


def eq_response(bands, freqs, sr=SR):
    """Biquad zincirinin genlik yanıtı (dB)."""
    sos = np.concatenate([biquad(k, f, g, q, sr) for (k, f, g, q) in bands], axis=0)
    w, h = sg.sosfreqz(sos, worN=freqs, fs=sr)
    return 20 * np.log10(np.abs(h) + 1e-12)


def resonator(x, f, bw, sr=SR):
    """İki kutuplu rezonatör (tepe kazancı ≈ 1): formant / gövde rezonansı için."""
    r = np.exp(-np.pi * bw / sr)
    th = PI2 * f / sr
    a = [1.0, -2 * r * np.cos(th), r * r]
    b = [(1 - r) * np.sqrt(1 - 2 * r * np.cos(2 * th) + r * r)]
    return lfilter(b, a, x)


def resonator_tv(x, f, bw, block=256, sr=SR):
    """Zamanla değişen rezonatör: f skaler ya da len(x) uzunluğunda dizi (Hz). Blok başına katsayı, süzgeç durumu taşınır."""
    f = np.broadcast_to(np.asarray(f, dtype=np.float64), (len(x),))
    y = np.empty(len(x))
    zi = np.zeros(2)
    r = np.exp(-np.pi * bw / sr)
    for i in range(0, len(x), block):
        th = PI2 * float(np.mean(f[i:i + block])) / sr
        a = [1.0, -2 * r * np.cos(th), r * r]
        b = [(1 - r) * np.sqrt(1 - 2 * r * np.cos(2 * th) + r * r)]
        y[i:i + block], zi = lfilter(b, a, x[i:i + block], zi=zi)
    return y


# ───────────────────────── zarflar / geçişler ─────────────────────────
def env_exp(n, tau, sr=SR):
    return np.exp(-np.arange(int(n)) / (tau * sr))


def fade_edges(x, fin=0.0, fout=0.0, sr=SR):
    """Kosinüs kenar geçişleri (yerinde değil; kopya döner)."""
    y = np.array(x, dtype=np.float64, copy=True)
    n = len(y)
    a = min(int(fin * sr), n)
    b = min(int(fout * sr), n)
    if a > 1:
        r = 0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a)
        y[:a] *= r if y.ndim == 1 else r[:, None]
    if b > 1:
        r = 0.5 + 0.5 * np.cos(np.pi * np.arange(b) / b)
        y[n - b:] *= r if y.ndim == 1 else r[:, None]
    return y


def adsr(n, a, d, s, r, sr=SR):
    """Doğrusal-üstel karışık basit ADSR (n örnek; r son r saniye)."""
    n = int(n)
    na, nd, nr = int(a * sr), int(d * sr), int(r * sr)
    e = np.ones(n)
    if na > 0:
        e[:na] = 0.5 - 0.5 * np.cos(np.pi * np.arange(min(na, n)) / na)[:n]
    if nd > 0 and na < n:
        m = min(nd, n - na)
        e[na:na + m] = s + (1 - s) * np.exp(-3.0 * np.arange(m) / nd)
        e[na + m:] = s
    elif na < n:
        e[na:] = s
    if nr > 0 and nr < n:
        e[n - nr:] *= 0.5 + 0.5 * np.cos(np.pi * np.arange(nr) / nr)
    return e


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


# ───────────────────────── stereo ─────────────────────────
def pan_gains(pan):
    """Sabit güç pan: pan∈[-1,1] → (gl, gr). Merkez 0 dB (√2 normalli)."""
    a = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    return np.cos(a) * np.sqrt(2.0), np.sin(a) * np.sqrt(2.0)


def to_stereo(x, pan=0.0):
    gl, gr = pan_gains(pan)
    x = np.asarray(x)
    return np.stack([x * gl, x * gr], axis=1)


def decorrelate(x, rng, amount=0.5, sr=SR):
    """Mono → yapay stereo: kısa farklı gecikmeli all-pass zincirleri (L/R farklı)."""
    out = []
    for ch in range(2):
        y = x
        for k in range(3):
            f = rng.uniform(300, 2400)
            q = rng.uniform(0.6, 1.4)
            y = sosfilt(biquad("allpass", f, 0, q, sr), y)
        d = int(rng.uniform(0.0002, 0.0011) * sr)
        y = np.concatenate([np.zeros(d), y])[:len(x)]
        out.append(amount * y + (1 - amount) * x)
    return np.stack(out, axis=1)


def make_loop(x, n, xf):
    """x (>= n+xf örnek) → n örneklik dikişsiz döngü (eşit güçlü çapraz geçişle son kısım başa karıştırılır)."""
    xf = int(xf)
    head = np.array(x[:n], dtype=np.float64, copy=True)
    tail = np.asarray(x[n:n + xf], dtype=np.float64)
    u = np.arange(xf) / xf
    fi, fo = np.sin(u * np.pi / 2), np.cos(u * np.pi / 2)
    if head.ndim == 2:
        fi, fo = fi[:, None], fo[:, None]
    head[:xf] = head[:xf] * fi + tail * fo
    return head


def tile_to(x, n):
    """Döngüyü n örneğe kadar tekrar eder (dikişsiz döngü varsayımıyla)."""
    reps = int(np.ceil(n / len(x)))
    return np.concatenate([x] * reps, axis=0)[:n]


# ───────────────────────── algoritmik salon reverb'ü ─────────────────────────
def hall_ir(rt60=2.2, sr=SR, seed=11, predelay=0.024, er_level=0.55, bands=None):
    """Sentezlenmiş stereo salon impuls yanıtı: erken yansımalar + bant bazlı üstel sönümlü gürültü kuyruğu.
    RT60 orta bant için; bas daha uzun, tiz daha kısa sönümlenir (gerçek salon gibi). Enerji ≈ 1'e normalli."""
    rng = rng_for("hall_ir", seed, rt60)
    if bands is None:
        bands = [(25, 220, 1.25), (220, 1800, 1.0), (1800, 5500, 0.62), (5500, 16000, 0.30)]
    n = int(sr * (predelay + rt60 * 1.35))
    t = np.arange(n) / sr
    ir = np.zeros((n, 2))
    pd = int(predelay * sr)
    for ch in range(2):
        w = rng.standard_normal(n)
        tail = np.zeros(n)
        for lo, hi, mult in bands:
            b = bpz(w, lo, hi, 2, sr)
            tail += b * np.exp(-6.9078 * np.maximum(t - predelay, 0) / (rt60 * mult))
        # yoğunluk yükselişi: ilk 40 ms'de seyrek → yoğun
        ramp = 1 - np.exp(-np.maximum(t - predelay, 0) / 0.035)
        tail *= ramp
        tail[:pd] = 0
        # erken yansımalar (seyrek darbeler)
        er = np.zeros(n)
        k = 18
        times = predelay + np.sort(rng.uniform(0.004, 0.095, k))
        for j, tm in enumerate(times):
            i = int(tm * sr)
            if i < n:
                er[i] += (1 if rng.random() < 0.5 else -1) * er_level * np.exp(-(tm - predelay) / 0.05) * (0.5 + 0.5 * rng.random())
        er = lpz(er, 6500, 2, sr)
        ir[:, ch] = tail + er * np.max(np.abs(tail)) * 1.2
    ir /= np.sqrt(np.sum(ir ** 2) / 2)  # kanal başına enerji 1
    return ir.astype(np.float32)


def reverb_wet(x, ir):
    """x: mono veya (n,2) gönderim → (n+m-1, 2) ıslak çıkış (yalnız ıslak). Konvolüsyon: scipy fftconvolve."""
    s = x if x.ndim == 1 else (x[:, 0] + x[:, 1]) * np.sqrt(0.5)
    wl = fftconvolve(s.astype(np.float64), ir[:, 0].astype(np.float64), mode="full")
    wr = fftconvolve(s.astype(np.float64), ir[:, 1].astype(np.float64), mode="full")
    return np.stack([wl, wr], axis=1).astype(np.float32)


# ───────────────────────── Karplus–Strong tel (blok-vektörel) ─────────────────────────
def ks_string(f0, dur, rng, S=0.5, t60=3.0, bright=0.5, pick=0.18, damp=0.0, vel=0.8, sr=SR):
    """Genişletilmiş Karplus–Strong: gecikme hattı N örnek, döngüde 2-tepeli ortalama (S), isteğe bağlı tek kutuplu sönüm
    ve kesirli gecikme için birinci derece all-pass. Gecikme hattı N blok halinde işlenir (lfilter + durum taşıma),
    böylece Python döngüsü yalnızca dur·f0 kadar. f0: Hz, dur: sn (toplam üretilen uzunluk), t60: temel için 60 dB sönüm süresi.
    bright: 0 (mat) … 1 (parlak) uyarım; pick: pena konumu (tel boyunun kesri); vel: genlik 0..1."""
    n_total = int(dur * sr)
    L = sr / f0
    d_damp = damp / (1 - damp) if damp > 0 else 0.0
    N = int(np.floor(L - S - d_damp - 0.5))
    N = max(N, 4)
    tau = L - S - d_damp - N  # all-pass gecikmesi (0.5..1.5)
    c = (1 - tau) / (1 + tau)
    # döngü süzgeci: ((1-S) + S z^-1) · (c + z^-1)/(1 + c z^-1) · (1-damp)/(1-damp z^-1)
    num = np.convolve(np.convolve([1 - S, S], [c, 1.0]), [1 - damp])
    den = np.convolve([1.0, c], [1.0, -damp])
    g = 10 ** (-3.0 / (f0 * t60))
    # uyarım: gürültü patlaması, pena konumu tarağı, parlaklık alçak geçireni
    e = rng.standard_normal(N)
    a = 0.92 * (1 - bright) ** 0.8
    if a > 0:
        e = lfilter([1 - a], [1, -a], e)
    p = max(1, int(round(pick * N)))
    e = e - np.roll(e, p)
    e -= e.mean()
    e *= vel / (np.max(np.abs(e)) + 1e-9)
    nblk = int(np.ceil(n_total / N)) + 1
    out = np.empty(nblk * N)
    out[:N] = e
    zi = np.zeros(max(len(num), len(den)) - 1)
    prev = e
    for k in range(1, nblk):
        v, zi = lfilter(num, den, prev, zi=zi)
        prev = g * v
        out[k * N:(k + 1) * N] = prev
    return out[:n_total]


# ───────────────────────── dalga tablosu osilatörü ─────────────────────────
TABLE_SIZE = 4096


def additive_table(f0, amp_fn, rng=None, phase="random", max_hz=None, sr=SR, size=TABLE_SIZE):
    """Harmonik genlikleri amp_fn(freq_hz) ile belirlenen tek periyotluk tablo (RMS=0.3'e normalli).
    f0 yüksek tutulur: harmonikler max_hz altında kalır (alias yok)."""
    if max_hz is None:
        max_hz = sr * 0.42
    H = int(min(size // 2 - 1, max_hz // f0))
    k = np.arange(1, H + 1)
    a = np.asarray(amp_fn(k * f0), dtype=np.float64)
    if phase == "random":
        ph = (rng or np.random.default_rng(1)).uniform(0, PI2, H)
    elif phase == "zero":
        ph = np.zeros(H)
    else:  # "saw": sinüs fazı
        ph = -np.pi / 2 * np.ones(H)
    spec = np.zeros(size // 2 + 1, dtype=np.complex128)
    spec[k] = a * np.exp(1j * ph)
    tab = np.fft.irfft(spec, size)
    tab *= 0.3 / (np.sqrt(np.mean(tab ** 2)) + 1e-12)
    return tab


def wt_osc(tab, freq, n=None, phase0=0.0, sr=SR):
    """Tablo osilatörü, doğrusal aradeğerlemeli. freq: skaler veya dizi (Hz); n skaler freq için gerekli."""
    f = np.asarray(freq, dtype=np.float64)
    if f.ndim == 0:
        f = np.full(int(n), float(f))
    ph = phase0 + np.cumsum(f) / sr
    pos = (ph % 1.0) * len(tab)
    i0 = pos.astype(np.int64)
    fr = pos - i0
    i1 = (i0 + 1) % len(tab)
    return tab[i0] * (1 - fr) + tab[i1] * fr


def vibrato(n, rate, depth_cents, delay=0.0, rise=0.5, rng=None, sr=SR):
    """Frekans çarpanı dizisi (≈1 civarı): rate Hz, depth_cents tepe; delay sn sonra rise sn'de açılır."""
    t = np.arange(int(n)) / sr
    ph0 = (rng.uniform(0, PI2) if rng is not None else 0.0)
    amt = np.clip((t - delay) / max(rise, 1e-3), 0, 1)
    r = rate * (1 + 0.04 * np.sin(PI2 * 0.23 * t + ph0))
    lfo = np.sin(PI2 * np.cumsum(r) / sr + ph0)
    return 2.0 ** (depth_cents / 1200.0 * amt * lfo)


# ───────────────────────── WAV G/Ç ─────────────────────────
def read_wav(path):
    """PCM 8/16/24/32-bit veya float32 WAV → (float32 [n,ch], sr)."""
    with wave.open(path, "rb") as w:
        sr, ch, sw, n = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
        raw = w.readframes(n)
    if sw == 2:
        x = np.frombuffer(raw, "<i2").astype(np.float32) / 32768.0
    elif sw == 3:
        b = np.frombuffer(raw, np.uint8).reshape(-1, 3).astype(np.int32)
        v = (b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16))
        v = np.where(v & 0x800000, v - 0x1000000, v)
        x = v.astype(np.float32) / 8388608.0
    elif sw == 4:
        x = np.frombuffer(raw, "<i4").astype(np.float32) / 2147483648.0
    elif sw == 1:
        x = (np.frombuffer(raw, np.uint8).astype(np.float32) - 128) / 128.0
    else:
        raise ValueError(f"WAV örnek genişliği {sw}")
    return x.reshape(-1, ch), sr


def write_wav(path, x, sr=SR, bits=16, dither=True, seed=0):
    """float [-1,1] (n,) veya (n,ch) → PCM WAV. 16-bit'te TPDF dither. Büyük diziler parça parça yazılır."""
    x = np.asarray(x)
    if x.ndim == 1:
        x = x[:, None]
    n, ch = x.shape
    rng = np.random.default_rng(1234 + seed)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(ch)
        w.setframerate(sr)
        w.setsampwidth(bits // 8)
        step = 1 << 20
        for i in range(0, n, step):
            seg = x[i:i + step].astype(np.float64)
            if bits == 16:
                if dither:
                    seg = seg * 32767.0 + (rng.random(seg.shape) - rng.random(seg.shape))
                else:
                    seg = seg * 32767.0
                w.writeframes(np.clip(np.rint(seg), -32768, 32767).astype("<i2").tobytes())
            elif bits == 24:
                v = np.clip(np.rint(seg * 8388607.0), -8388608, 8388607).astype(np.int32)
                b = np.stack([v & 255, (v >> 8) & 255, (v >> 16) & 255], axis=-1).astype(np.uint8)
                w.writeframes(b.tobytes())
            else:
                raise ValueError(bits)


# ───────────────────────── BS.1770 ölçümleri ─────────────────────────
def _k_sos(sr):
    f0, G, Q = 1681.974450955533, 3.999843853973347, 0.7071752369554196
    K = np.tan(np.pi * f0 / sr)
    Vh = 10 ** (G / 20.0)
    Vb = Vh ** 0.4996667741545416
    a0 = 1 + K / Q + K * K
    b = [(Vh + Vb * K / Q + K * K) / a0, 2 * (K * K - Vh) / a0, (Vh - Vb * K / Q + K * K) / a0]
    a = [1.0, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0]
    f1, Q1 = 38.13547087602444, 0.5003270373238773
    K1 = np.tan(np.pi * f1 / sr)
    a01 = 1 + K1 / Q1 + K1 * K1
    b1 = [1.0, -2.0, 1.0]
    a1 = [1.0, 2 * (K1 * K1 - 1) / a01, (1 - K1 / Q1 + K1 * K1) / a01]
    return np.concatenate([tf2sos(b, a), tf2sos(b1, a1)], axis=0)


def k_weighted_power(x, sr=SR):
    """x (n,) veya (n,ch) → K-ağırlıklı kare toplamı (kanal ağırlığı 1) float64 (n,)."""
    x = np.asarray(x)
    if x.ndim == 1:
        x = x[:, None]
    sos = _k_sos(sr)
    p = np.zeros(len(x))
    for c in range(x.shape[1]):
        y = sosfilt(sos, x[:, c].astype(np.float64))
        p += y * y
    return p


def loudness_stats(x, sr=SR, p=None):
    """Entegre LUFS (kapılı), kısa-dönem (3 s) tepe, anlık (400 ms) tepe, LRA. x: float (n,) veya (n,2)."""
    if p is None:
        p = k_weighted_power(x, sr)
    W, H = int(0.4 * sr), int(0.1 * sr)
    cs = np.concatenate([[0.0], np.cumsum(p)])
    nb = (len(p) - W) // H + 1
    if nb < 1:
        return dict(integrated=-70.0, shortterm_max=-70.0, momentary_max=-70.0, lra=0.0)
    idx = np.arange(nb) * H
    ms = (cs[idx + W] - cs[idx]) / W
    lk = -0.691 + 10 * np.log10(ms + 1e-18)
    g1 = lk > -70.0
    if not np.any(g1):
        return dict(integrated=-70.0, shortterm_max=-70.0, momentary_max=float(lk.max()), lra=0.0)
    rel = -0.691 + 10 * np.log10(np.mean(ms[g1]) + 1e-18) - 10.0
    g2 = g1 & (lk > rel)
    integ = -0.691 + 10 * np.log10(np.mean(ms[g2]) + 1e-18)
    # kısa dönem: 3 s pencere, 0.1 s adım
    W3 = int(3.0 * sr)
    nb3 = (len(p) - W3) // H + 1
    if nb3 >= 1:
        i3 = np.arange(nb3) * H
        ms3 = (cs[i3 + W3] - cs[i3]) / W3
        st = -0.691 + 10 * np.log10(ms3 + 1e-18)
        st_gate = st[st > -70.0]
        if len(st_gate):
            rel3 = -0.691 + 10 * np.log10(np.mean(10 ** ((st_gate + 0.691) / 10)) + 1e-18) - 20.0
            sel = st_gate[st_gate > rel3]
            lra = float(np.percentile(sel, 95) - np.percentile(sel, 10)) if len(sel) > 1 else 0.0
        else:
            lra = 0.0
        stmax = float(st.max())
    else:
        lra, stmax = 0.0, float(lk.max())
    return dict(integrated=float(integ), shortterm_max=stmax, momentary_max=float(lk.max()), lra=lra)


def true_peak_db(x, os=4, chunk=1 << 21):
    """4× aşırı örneklemeyle true-peak (dBTP). x: (n,) veya (n,ch) float."""
    x = np.asarray(x)
    if x.ndim == 1:
        x = x[:, None]
    pk = 0.0
    n = len(x)
    pad = 64
    for c in range(x.shape[1]):
        for s in range(0, n, chunk):
            a, b = max(0, s - pad), min(n, s + chunk + pad)
            seg = x[a:b, c].astype(np.float64)
            if np.max(np.abs(seg)) < 0.05 * max(pk, 1e-9) and pk > 0:
                continue
            up = resample_poly(seg, os, 1)
            lo, hi = (s - a) * os, (s - a + min(chunk, n - s)) * os
            pk = max(pk, float(np.max(np.abs(up[lo:hi]))))
    return float(20 * np.log10(pk + 1e-12))


def tp_envelope(x, os=4, chunk=1 << 21):
    """Örnek başına true-peak zarfı (max |4× aşırı örneklenmiş| her örnek aralığında). x: (n,2) → (n,)"""
    x = np.asarray(x)
    if x.ndim == 1:
        x = x[:, None]
    n = len(x)
    out = np.zeros(n)
    pad = 64
    for c in range(x.shape[1]):
        for s in range(0, n, chunk):
            a, b = max(0, s - pad), min(n, s + chunk + pad)
            seg = x[a:b, c].astype(np.float64)
            up = np.abs(resample_poly(seg, os, 1))
            lo = (s - a) * os
            m = min(chunk, n - s)
            core = up[lo:lo + m * os].reshape(m, os).max(axis=1)
            out[s:s + m] = np.maximum(out[s:s + m], core)
    return out


# ───────────────────────── dinamik işlemciler ─────────────────────────
def _smooth_ar(target, a_att, a_rel, init=0.0):
    """Asimetrik (saldırı/bırakma) tek kutuplu yumuşatma; hedef dB cinsinden gain azaltma (negatif).
    Hedef düştüğünde (daha çok azaltma) saldırı, yükseldiğinde bırakma katsayısı."""
    out = np.empty_like(target)
    g = init
    for i in range(len(target)):
        t = target[i]
        c = a_att if t < g else a_rel
        g = c * g + (1.0 - c) * t
        out[i] = g
    return out


def compressor(x, thr_db=-24.0, ratio=2.0, attack=0.010, release=0.120, knee_db=6.0, hop=24, sr=SR, makeup_db=0.0):
    """İleri beslemeli tepe-algılamalı sıkıştırıcı (mono veya (n,ch) bağlı). Algılama hop örnek bloklarında yapılır
    (hop=24 → 2 kHz), kazanç doğrusal aradeğerlenir. Döner: (y, gr_db_dizisi(hop hızında))."""
    x = np.asarray(x)
    mono = x if x.ndim == 1 else np.max(np.abs(x), axis=1)
    n = len(mono)
    nh = n // hop + 1
    pad = np.zeros(nh * hop)
    pad[:n] = np.abs(mono)
    ph = pad.reshape(nh, hop).max(axis=1)
    lvl = 20 * np.log10(ph + 1e-9)
    over = lvl - thr_db
    k = knee_db
    slope = 1.0 / ratio - 1.0
    gr = np.where(over <= -k / 2, 0.0,
                  np.where(over >= k / 2, slope * over, slope * (over + k / 2) ** 2 / (2 * k)))
    dt = hop / sr
    a_att, a_rel = np.exp(-dt / attack), np.exp(-dt / release)
    grs = _smooth_ar(gr, a_att, a_rel)
    # hop merkezlerine göre doğrusal aradeğerleme
    centers = (np.arange(nh) + 0.5) * hop
    g_db = np.interp(np.arange(n), centers, grs) + makeup_db
    g = 10 ** (g_db / 20.0)
    y = x * (g if x.ndim == 1 else g[:, None])
    return y.astype(x.dtype if x.dtype == np.float32 else np.float64), grs


def _decay_max(L, a, blk=2048):
    """L_out[i] = max(L[i], a·L_out[i−1]) özyinelemesinin vektörel (blok blok) çözümü — üstel bırakmalı tepe tutma."""
    n = len(L)
    out = np.empty(n)
    carry = 0.0
    idx = np.arange(blk, dtype=np.float64)
    pw = a ** (-idx)
    for s0 in range(0, n, blk):
        m = min(blk, n - s0)
        cm = np.maximum.accumulate(L[s0:s0 + m] * pw[:m])
        o = np.maximum(cm / pw[:m], carry * a ** (idx[:m] + 1))
        out[s0:s0 + m] = o
        carry = o[-1]
    return out


def hop_peaks(x, hop=24, os=4, chunk=None):
    """x (n,ch) → hop başına true-peak (max |4× aşırı örneklenmiş|) (nh,) ve (varsa) hop başına örnek tepe. Bellek dostu, parça parça."""
    x = np.asarray(x)
    if x.ndim == 1:
        x = x[:, None]
    n = len(x)
    nh = n // hop + 1
    out = np.zeros(nh * hop)
    chunk = chunk or hop * 87381
    pad = 64
    for c in range(x.shape[1]):
        for s0 in range(0, n, chunk):
            a, b = max(0, s0 - pad), min(n, s0 + chunk + pad)
            seg = x[a:b, c].astype(np.float64)
            up = np.abs(resample_poly(seg, os, 1))
            lo = (s0 - a) * os
            m = min(chunk, n - s0)
            core = up[lo:lo + m * os].reshape(m, os).max(axis=1)
            out[s0:s0 + m] = np.maximum(out[s0:s0 + m], core)
    return out.reshape(nh, hop).max(axis=1)


def k_power_hop(x, hop=24, sr=SR, chunk=None):
    """x (n,ch) → hop başına K-ağırlıklı kare toplamı (kanallar toplanmış) (nh,). Süzgeç durumu parçalar arası taşınır."""
    x = np.asarray(x)
    if x.ndim == 1:
        x = x[:, None]
    n = len(x)
    nh = n // hop + 1
    out = np.zeros(nh * hop)
    sos = _k_sos(sr)
    chunk = chunk or hop * 87381
    for c in range(x.shape[1]):
        zi = np.zeros((sos.shape[0], 2))
        for s0 in range(0, n, chunk):
            seg = x[s0:s0 + chunk, c].astype(np.float64)
            y, zi = sosfilt(sos, seg, zi=zi)
            out[s0:s0 + len(seg)] += y * y
    return out.reshape(nh, hop).sum(axis=1)


def lufs_from_hop_power(pw, hop=24, sr=SR):
    """hop başına (kanal toplamlı) K-ağırlıklı güç toplamlarından entegre LUFS (kapılı). Blok 400 ms, adım 100 ms."""
    W = int(round(0.4 * sr / hop))
    H = int(round(0.1 * sr / hop))
    cs = np.concatenate([[0.0], np.cumsum(pw)])
    nb = (len(pw) - W) // H + 1
    if nb < 1:
        return -70.0
    idx = np.arange(nb) * H
    ms = (cs[idx + W] - cs[idx]) / (W * hop)
    lk = -0.691 + 10 * np.log10(ms + 1e-18)
    g1 = lk > -70.0
    if not np.any(g1):
        return -70.0
    rel = -0.691 + 10 * np.log10(np.mean(ms[g1]) + 1e-18) - 10.0
    g2 = g1 & (lk > rel)
    return float(-0.691 + 10 * np.log10(np.mean(ms[g2]) + 1e-18))


def limiter_curve(ph, ceil_lin, hop=24, lookahead=0.008, release=0.120, sr=SR):
    """hop başına tepe (ph, doğrusal) → hop düzeyinde kazanç eğrisi g (nh,), ≤ 1.
    Komşu hop minimumu → ileri bakış minimum + aynı genişlikte hareketli ortalama (tepe öncesi yumuşak iniş garantisi) →
    üstel bırakma (vektörel). Doğrusal aradeğerleme güvencesi için komşu min alınır."""
    req = np.minimum(1.0, ceil_lin / (ph + 1e-12))
    prev = np.concatenate([[req[0]], req[:-1]])
    nxt = np.concatenate([req[1:], [req[-1]]])
    r2 = np.minimum(req, np.minimum(prev, nxt))
    la = max(1, int(round(lookahead / (hop / sr))))
    w = 2 * la + 1
    gmin = minimum_filter1d(r2, size=w, mode="nearest")
    gsm = uniform_filter1d(gmin, size=w, mode="nearest")
    a = np.exp(-(hop / sr) / release)
    return 1.0 - _decay_max(1.0 - gsm, a)


def apply_hop_gain(x, g, gain_lin=1.0, hop=24, chunk=1 << 22):
    """x (n,ch) float32 → x·gain_lin·g(t) (g hop merkezlerinde, doğrusal aradeğerleme). Yeni dizi döner."""
    n = len(x)
    y = np.empty(x.shape, dtype=np.float32)
    centers = (np.arange(len(g)) + 0.5) * hop
    for s0 in range(0, n, chunk):
        e = min(n, s0 + chunk)
        gl = np.interp(np.arange(s0, e), centers, g) * gain_lin
        y[s0:e] = x[s0:e] * gl.astype(np.float32)[:, None]
    return y


def limiter(x, ceiling_db=-1.2, lookahead=0.008, release=0.120, hop=24, sr=SR):
    """True-peak duyarlı, ileri bakışlı yumuşak limiter (x: (n,2)). Döner: (y float32, gr_db_dizisi(hop hızında))."""
    ph = hop_peaks(x, hop)
    g = limiter_curve(ph, 10 ** (ceiling_db / 20.0), hop, lookahead, release, sr)
    return apply_hop_gain(x, g, 1.0, hop), 20 * np.log10(g + 1e-12)


# ───────────────────────── ortak sentez sesleri (müzik + SFX) ─────────────────────────
# (oran, genlik, T60[sn] — f=400 Hz'lik çan için), vurgu notası = "prime"
_BELL_PARTIALS = [(0.5, 0.55, 9.0), (1.0, 1.0, 7.0), (1.19, 0.80, 5.0), (1.5, 0.45, 4.2), (2.0, 0.70, 4.5),
                  (2.51, 0.35, 3.0), (3.0, 0.25, 2.5), (4.17, 0.20, 1.8), (5.43, 0.12, 1.2), (6.8, 0.07, 0.8)]


def bell_tone(f, dur, vel=0.8, rng=None, ring=1.0, strike=0.5, partials=None, sr=SR):
    """Kilise çanı / tubular çan: eğri-küçük-üçlü kısmi yapısı, her kısmi çift (vuruş/titreşim), çarpma gürültüsü.
    f: vuruş (prime) notası Hz. ring: sönüm ölçeği. Döner: mono float64."""
    rng = rng or np.random.default_rng(3)
    n = int(dur * sr)
    t = np.arange(n) / sr
    scale = ring * (400.0 / max(f, 60.0)) ** 0.45
    out = np.zeros(n)
    for (r, a, t60) in (partials or _BELL_PARTIALS):
        fr = f * r
        if fr > 18000:
            continue
        df = rng.uniform(0.12, 0.65) * (f / 400.0) ** 0.5
        env = np.exp(-6.9078 * t / (t60 * scale))
        if env[-1] > 0.02:
            env = env * np.minimum(1.0, (n - 1 - np.arange(n)) / (0.05 * sr))
        for sgn in (-1, 1):
            out += 0.5 * a * np.sin(PI2 * (fr + sgn * df) * t + rng.uniform(0, PI2)) * env
    cl = bp(rng.standard_normal(n), 1800, 6500, 2, sr) * np.exp(-t / 0.005)
    cl += 0.6 * np.sin(PI2 * f * 3.1 * t) * np.exp(-t / 0.02)
    out += strike * 0.35 * cl
    out *= np.minimum(1.0, t / 0.0015)
    return out * vel


def gong_tone(f0, dur, vel=0.8, rng=None, sr=SR, modes=52, bloom=1.0):
    """Tam-tam / gong: ~50 uyumsuz mod, yüksek modlar gecikmeli yükselir ('çiçeklenme'), çiftli kısmi vuruşu + gürültü yatağı."""
    rng = rng or np.random.default_rng(5)
    n = int(dur * sr)
    t = np.arange(n) / sr
    r = np.sort(np.exp(rng.uniform(0.0, np.log(24.0), modes)))
    r[:3] = [1.0, 1.52, 2.09]
    out = np.zeros(n)
    for ri in r:
        fr = f0 * ri
        if fr > 15000:
            continue
        a = ri ** -0.42 * rng.uniform(0.45, 1.0)
        t60 = rng.uniform(5.0, 10.0) * ri ** -0.33
        tg = 0.012 * ri ** 0.95 * bloom
        env = (1 - np.exp(-t / tg)) * np.exp(-6.9078 * t / t60)
        df = rng.uniform(0.25, 1.7)
        out += 0.5 * a * (np.sin(PI2 * (fr - df) * t + rng.uniform(0, PI2)) + np.sin(PI2 * (fr + df) * t + rng.uniform(0, PI2))) * env
    nz = bp(rng.standard_normal(n), 140, 3600, 2, sr) * (1 - np.exp(-t / 0.10)) * np.exp(-t / 1.7)
    out += 0.16 * nz
    out = lp(out, 9500, 2, sr) * np.minimum(1.0, t / 0.002)
    out *= np.minimum(1.0, (n - 1 - np.arange(n)) / (0.08 * sr))
    return out * vel / (np.max(np.abs(out)) + 1e-9) * 0.9


def drum_hit(kind, f=110.0, vel=0.8, rng=None, sr=SR):
    """Çerçeve davulu vuruşları: 'dum' (merkez, alçak), 'tek' (kenar, tok-tiz), 'ka' (hafif tokat). Mono float64 (≈0.5 sn)."""
    rng = rng or np.random.default_rng(7)
    if kind == "dum":
        d = 0.75
        t = np.arange(int(d * sr)) / sr
        fr = f * (1 + 0.55 * np.exp(-t / 0.028))
        ph = PI2 * np.cumsum(fr) / sr
        body = np.sin(ph) * np.exp(-t / 0.15) + 0.45 * np.sin(1.59 * ph) * np.exp(-t / 0.075) + 0.25 * np.sin(2.14 * ph) * np.exp(-t / 0.05)
        sl = bp(rng.standard_normal(len(t)), 250, 2400, 2, sr) * np.exp(-t / 0.018) * 0.55
        sk = hp(rng.standard_normal(len(t)), 1600, 2, sr) * np.exp(-t / 0.008) * 0.22
        y = body + sl + sk
    elif kind == "tek":
        d = 0.35
        t = np.arange(int(d * sr)) / sr
        fr = f * 3.1
        body = np.sin(PI2 * fr * t) * np.exp(-t / 0.045) + 0.4 * np.sin(PI2 * fr * 1.9 * t) * np.exp(-t / 0.03)
        sl = bp(rng.standard_normal(len(t)), 1500, 5200, 2, sr) * np.exp(-t / 0.02) * 0.75
        y = 0.7 * body + sl
    else:  # ka
        d = 0.3
        t = np.arange(int(d * sr)) / sr
        body = np.sin(PI2 * f * 1.9 * t) * np.exp(-t / 0.035)
        sl = bp(rng.standard_normal(len(t)), 700, 3600, 2, sr) * np.exp(-t / 0.032)
        y = 0.45 * body + 0.9 * sl
    y *= np.minimum(1.0, np.arange(len(y)) / (0.0008 * sr))
    y *= np.minimum(1.0, (len(y) - 1 - np.arange(len(y))) / (0.02 * sr))
    return y * vel / (np.max(np.abs(y)) + 1e-9) * 0.9


def tef_hit(vel=0.7, rng=None, sr=SR, dur=0.38):
    """Tef / def zilleri: yüksek frekanslı sönümlü rezonanslar + gürültü kıvılcımı."""
    rng = rng or np.random.default_rng(9)
    n = int(dur * sr)
    t = np.arange(n) / sr
    y = np.zeros(n)
    for _ in range(9):
        fr = rng.uniform(3800, 11000)
        y += rng.uniform(0.3, 1.0) * np.sin(PI2 * fr * t + rng.uniform(0, PI2)) * np.exp(-t / rng.uniform(0.04, 0.16))
    y += hp(rng.standard_normal(n), 5000, 2, sr) * np.exp(-t / 0.03) * 1.3
    y += 0.5 * np.sin(PI2 * 190 * t) * np.exp(-t / 0.03)
    y *= np.minimum(1.0, t / 0.0006) * np.minimum(1.0, (n - 1 - np.arange(n)) / (0.03 * sr))
    return y * vel / (np.max(np.abs(y)) + 1e-9) * 0.8


def timpani_hit(f=73.0, vel=0.9, rng=None, sr=SR, dur=2.4):
    """Timpani: membran kipleri (1, 1.5, 1.99, 2.44, 2.9), başlangıçta perde düşüşü, sopa darbesi."""
    rng = rng or np.random.default_rng(11)
    n = int(dur * sr)
    t = np.arange(n) / sr
    y = np.zeros(n)
    for r, a, tau in [(1.0, 1.0, 0.9), (1.5, 0.55, 0.55), (1.99, 0.42, 0.40), (2.44, 0.25, 0.30), (2.9, 0.16, 0.22)]:
        fr = f * r * (1 + 0.07 * np.exp(-t / 0.05))
        y += a * np.sin(PI2 * np.cumsum(fr) / sr + rng.uniform(0, PI2)) * np.exp(-t / tau)
    y += 0.5 * bp(rng.standard_normal(n), 180, 1800, 2, sr) * np.exp(-t / 0.012)
    y *= np.minimum(1.0, t / 0.001) * np.minimum(1.0, (n - 1 - np.arange(n)) / (0.1 * sr))
    return y * vel / (np.max(np.abs(y)) + 1e-9) * 0.9


def sub_boom(f_start=78.0, f_end=26.0, dur=4.5, vel=0.9, sr=SR, drive=1.6):
    """Alt-bas patlaması: üstel perde düşüşü + hafif doyum (harmonik), uzun sönüm."""
    n = int(dur * sr)
    t = np.arange(n) / sr
    f = f_end + (f_start - f_end) * np.exp(-t / 0.35)
    y = np.sin(PI2 * np.cumsum(f) / sr) * np.exp(-t / 1.1)
    y = np.tanh(drive * y) / np.tanh(drive)
    y *= np.minimum(1.0, t / 0.004) * np.minimum(1.0, (n - 1 - np.arange(n)) / (0.2 * sr))
    return y * vel


def noise_riser(dur, f0=250.0, f1=7000.0, rng=None, sr=SR, nb=14, curve=1.6, peak_at=1.0):
    """Yükselen filtreli gürültü: logaritmik aralıklı bantlar sırayla belirir (süpürme etkisi). Mono, [0,1] zarflı."""
    rng = rng or np.random.default_rng(13)
    n = int(dur * sr)
    t = np.arange(n) / sr
    w = rng.standard_normal(n)
    cs = np.exp(np.linspace(np.log(f0), np.log(f1), nb))
    out = np.zeros(n)
    for i, c in enumerate(cs):
        pos = ((i + 0.5) / nb) ** (1 / curve) * peak_at * dur
        g = np.exp(-0.5 * ((t - pos) / (0.16 * dur + 0.05)) ** 2)
        out += bp(w, c / 1.25, min(c * 1.25, sr * 0.45), 2, sr) * g
    out *= (t / dur) ** 1.4
    return out / (np.max(np.abs(out)) + 1e-9)
